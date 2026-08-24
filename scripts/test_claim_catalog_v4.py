#!/usr/bin/env python3
"""Independent invariants and mutation tests for the Stage4 claim catalog.

The generator is deliberately imported as a library for in-memory mutation
tests, but the frozen universes below are recomputed from the Stage2 authority
and the Stage3 audit by this test module.  This keeps the acceptance oracle
independent from the production manifest parser.
"""

from __future__ import annotations

import copy
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "Docs" / "tools" / "generate_claim_catalog_v4.py"
CHECKER_PATH = ROOT / "scripts" / "check_claim_catalog_v4.py"
V2_DIR = ROOT / "Docs" / "catalog"
V4_DIR = V2_DIR / "v4"
AUDIT_PATH = (
    ROOT / "Docs" / "reviews" / "Stage3_v3_18_Agent_Critical_Audit_2026-08-10.md"
)

SPEC = importlib.util.spec_from_file_location(
    "generate_claim_catalog_v4", GENERATOR_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import the Stage4 catalog generator")
generator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generator
SPEC.loader.exec_module(generator)

CHECKER_SPEC = importlib.util.spec_from_file_location(
    "check_claim_catalog_v4", CHECKER_PATH
)
if CHECKER_SPEC is None or CHECKER_SPEC.loader is None:
    raise RuntimeError("cannot import the independent Stage4 catalog checker")
catalog_checker = importlib.util.module_from_spec(CHECKER_SPEC)
sys.modules[CHECKER_SPEC.name] = catalog_checker
CHECKER_SPEC.loader.exec_module(catalog_checker)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def independently_reseal(document: dict) -> dict:
    """Recompute the public, unkeyed artifact seal without the generator."""

    resealed = dict(document)
    resealed.pop("authority_sha256", None)
    resealed["authority_sha256"] = sha256_bytes(canonical_json_bytes(resealed))
    return resealed


def independent_stable_digest(namespace: str, value: object) -> str:
    """Reproduce a namespaced digest without calling generator code."""

    return sha256_bytes(
        namespace.encode("utf-8") + b"\0" + canonical_json_bytes(value)
    )


def independently_recount_and_reseal(document: dict) -> dict:
    """Refresh mutable envelope fields after an adversarial row mutation.

    Only the prior-lifecycle and repair artifacts exercised below are
    supported.  Keeping this oracle in the test prevents the attack from
    failing merely because a public count or unkeyed authority seal is stale.
    """

    value = copy.deepcopy(document)
    artifact = value["artifact"]
    if artifact == "Claim_ID_Registry_v4.json":
        value["counts"] = {
            "families_allocated": len(value["families"]),
            "legacy_aliases": len(value["legacy_aliases"]),
            "occurrences_allocated": len(value["variants"]),
            "redirects": len(value["redirects"]),
            "senses_allocated": len(value["senses"]),
            "splits": len(value["splits"]),
            "stage4_additions": sum(
                row.get("curation_key") is not None for row in value["variants"]
            ),
            "variants_allocated": len(value["variants"]),
        }
    elif artifact == "Claim_ID_Migration_v2_to_v4.json":
        migrations = value["migrations"]
        baseline = sum(row.get("v2_variant_id") is not None for row in migrations)
        value["counts"] = {
            "baseline_carry": baseline,
            "folded_occurrences": len(value["folded_occurrence_ids"]),
            "legacy_aliases": len(value["legacy_alias_migrations"]),
            "migrations": len(migrations),
            "new_stage4": len(migrations) - baseline,
        }
    elif artifact == "Candidate_Dispositions_v4.json":
        rows = value["dispositions"]
        origins = Counter(row.get("origin") for row in rows)
        dispositions = Counter(row.get("disposition") for row in rows)
        value["counts"] = {
            "collision": dispositions["collision"],
            "existing_family": dispositions["existing_family"],
            "frozen": len(rows) - origins["stage4_discovery"],
            "new_family": dispositions["new_family"],
            "nonclaim": dispositions["nonclaim"],
            "stage4_discovery": origins["stage4_discovery"],
            "total": len(rows),
            "v2_collision": origins["v2_collision"],
            "v2_missing": origins["v2_missing"],
            "v3_delta": origins["v3_delta"],
        }
    elif artifact == "Repair_Proposal_Dispositions_v4.json":
        rows = value["dispositions"]
        domains = Counter(row.get("domain") for row in rows)
        dispositions = Counter(row.get("disposition") for row in rows)
        value["counts"] = {
            "applied_by_explicit_curation": dispositions[
                "applied_by_explicit_curation"
            ],
            "computer_science": domains["computer_science"],
            "mathematics": domains["mathematics"],
            "physics": domains["physics"],
            "proposal_only_preserved": dispositions["proposal_only_preserved"],
            "total": len(rows),
        }
    else:
        raise AssertionError(f"unsupported recount artifact: {artifact}")

    value["authoritative_inputs_sha256"] = independent_stable_digest(
        "awesome-theorems/stage4-authoritative-inputs/v4",
        value["authoritative_inputs"],
    )
    return independently_reseal(value)


class OverrideChecker(catalog_checker.Checker):
    """Run the independent checker over generated/mutated in-memory outputs."""

    def __init__(
        self,
        json_overrides: dict[str, dict],
        text_overrides: dict[str, str],
    ) -> None:
        super().__init__(ROOT, require_complete=True)
        self.json_overrides = json_overrides
        self.text_overrides = text_overrides

    def load_json(self, relative: Path | str, *, required: bool = True) -> object:
        name = Path(relative).name
        if name in self.json_overrides:
            return self.json_overrides[name]
        return super().load_json(relative, required=required)

    def load_text(self, relative: Path | str, *, required: bool = True) -> str:
        name = Path(relative).name
        if name in self.text_overrides:
            return self.text_overrides[name]
        return super().load_text(relative, required=required)


def id_ordinal(identifier: str) -> int:
    match = re.fullmatch(r"(?:ATO|ATF|ATS|ATV)-([0-9]{8})", identifier)
    if match is None:
        match = re.fullmatch(r"S4-CLM-([0-9]{8})", identifier)
    if match is None:
        raise AssertionError(f"malformed typed identifier: {identifier!r}")
    return int(match.group(1))


def independent_audit_delta_keys() -> set[str]:
    """Read only the fenced key lists in audit section 4.

    This intentionally does not call the generator's audit parser.  Restricting
    the match to the bounded section prevents later prose examples from silently
    expanding the frozen denominator.
    """

    text = AUDIT_PATH.read_text(encoding="utf-8")
    section = text.split("## 4. Mandatory bounded candidate delta", 1)[1]
    section = section.split("## 5.", 1)[0]
    return set(
        re.findall(
            r"(?m)^missing\.(?:math|physics|cs)\.[a-z0-9_]+$", section
        )
    )


def generated_documents() -> tuple[dict[Path, str], dict[str, dict]]:
    rendered = generator.build_artifacts()
    documents: dict[str, dict] = {}
    for path, payload in rendered.items():
        name = Path(path).name
        if name.endswith(".json"):
            documents[name] = json.loads(payload)
    return rendered, documents


def document_payload(document: dict) -> dict:
    payload = document.get("payload")
    return payload if isinstance(payload, dict) else document


def first_list(document: dict, *keys: str) -> list:
    for key in keys:
        value = document.get(key)
        if isinstance(value, list):
            return value
    raise AssertionError(f"none of {keys!r} is a list")


def row_atv_id(row: dict) -> str | None:
    for key in ("atv_id", "variant_id", "canonical_variant_id"):
        value = row.get(key)
        if isinstance(value, str):
            return value
    if row.get("record_type") == "ATV":
        value = row.get("record_id")
        return value if isinstance(value, str) else None
    return None


def row_stage_id(row: dict) -> str | None:
    for key in ("stage_claim_id", "stage_id", "s4_id"):
        value = row.get(key)
        if isinstance(value, str):
            return value
    return None


def material_status(row: dict) -> str | None:
    value = row.get("material_status")
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("status", "value"):
            if isinstance(value.get(key), str):
                return value[key]
    statuses = row.get("statuses")
    if isinstance(statuses, dict):
        human = statuses.get("human_truth")
        if isinstance(human, dict) and isinstance(human.get("status"), str):
            return human["status"]
    return None


def is_atomic_truth_claim(row: dict) -> bool:
    claim_kind = row.get("claim_kind")
    nested_atomicity = claim_kind.get("atomicity") if isinstance(claim_kind, dict) else None
    nested_truth = claim_kind.get("truth_apt") if isinstance(claim_kind, dict) else None
    atomicity = row.get("atomicity", nested_atomicity)
    truth = row.get("truth_apt", nested_truth)
    return (
        row.get("lifecycle", "active") == "active"
        and not row.get("lifecycle_target_stage_ids", [])
        and row.get("record_role", "claim") == "claim"
        and atomicity == "atomic"
        and truth in (True, "truth_apt")
    )


def projection_ids(document: dict) -> list[str]:
    payload = document_payload(document)
    for key in (
        "stage_claim_ids",
        "theorem_stage_ids",
        "open_or_conditional_stage_ids",
        "ids",
    ):
        value = payload.get(key)
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            return value
    rows = first_list(payload, "records", "rows", "entries", "claims")
    result = [row_stage_id(row) for row in rows if isinstance(row, dict)]
    if any(value is None for value in result):
        raise AssertionError("projection row lacks its Stage4 claim ID")
    return [value for value in result if value is not None]


class ClaimCatalogV4Tests(unittest.TestCase):
    """Set-equality, migration, projection, and fail-closed tests."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.v2_source = load_json(V2_DIR / "Source_Records_v2.json")
        cls.v2_registry = load_json(V2_DIR / "Claim_ID_Registry_v2.json")
        cls.v2_relations = load_json(V2_DIR / "Claim_Relations_v2.json")
        cls.v2_coverage = load_json(V2_DIR / "Coverage_Candidates_v2.json")
        cls.manifest = load_json(generator.MANIFEST_PATH)
        cls.fragments = [
            load_json(ROOT / relative) for relative in cls.manifest["fragments"]
        ]
        cls.inputs = generator.load_inputs()
        cls.rendered, cls.documents = generated_documents()
        cls.rendered_text_by_name = {
            Path(path).name: payload
            for path, payload in cls.rendered.items()
            if Path(path).suffix == ".md"
        }

        cls.baseline_ato_ids = {
            row["occurrence_id"] for row in cls.v2_source["records"]
        }
        cls.baseline_atv_ids = {
            row["variant_id"] for row in cls.v2_registry["variants"]
        }
        cls.legacy_alias_targets = {
            row["alias_id"]: row["target_variant_id"]
            for row in cls.v2_registry["legacy_aliases"]
        }
        cls.v2_candidate_keys = {
            row["candidate_key"]
            for group in ("missing_candidates", "present_collisions")
            for row in cls.v2_coverage[group]
        }
        cls.audit_delta_keys = independent_audit_delta_keys()

        folded: set[str] = set()
        for cluster in cls.v2_relations["legacy_exact_match_clusters"]:
            survivor = cluster["legacy_survivor_occurrence_id"]
            folded.update(
                member["occurrence_id"]
                for member in cluster["members"]
                if member["occurrence_id"] != survivor
            )
        cls.folded_occurrence_ids = folded

    def document(self, name: str) -> dict:
        return self.documents[name]

    def payload(self, name: str) -> dict:
        return document_payload(self.document(name))

    def mutable_artifact(self, name: str) -> tuple[dict[str, dict], dict]:
        """Copy only one large artifact; all untouched documents stay shared."""

        documents = dict(self.documents)
        documents[name] = copy.deepcopy(self.documents[name])
        return documents, document_payload(documents[name])

    def run_independent_checker(
        self,
        json_overrides: dict[str, dict] | None = None,
        text_overrides: dict[str, str] | None = None,
    ) -> OverrideChecker:
        documents = dict(self.documents)
        documents.update(json_overrides or {})
        texts = dict(self.rendered_text_by_name)
        texts.update(text_overrides or {})
        checker = OverrideChecker(documents, texts)
        catalog_checker.run(checker)
        return checker

    def assert_independent_rejected(
        self,
        json_overrides: dict[str, dict],
        expected_error: str,
    ) -> list[str]:
        checker = self.run_independent_checker(json_overrides)
        self.assertTrue(checker.errors, "independent checker accepted a resealed mutation")
        self.assertTrue(
            any(expected_error in error for error in checker.errors),
            f"expected error containing {expected_error!r}; got {checker.errors!r}",
        )
        self.assertFalse(
            any("stale authority_sha256" in error for error in checker.errors),
            f"mutation was not correctly resealed: {checker.errors!r}",
        )
        return checker.errors

    def assert_rejected(self, documents: dict[str, dict]) -> None:
        """A structurally legal-looking cross-document mutation must fail closed."""

        resealed = dict(documents)
        for name, document in documents.items():
            if document is not self.documents.get(name):
                resealed[name] = generator.seal_document(name, document)
        with self.assertRaises(generator.CatalogError):
            # A mutation may fail either its local document contract (for
            # example, recomputed counts) or a cross-artifact invariant.  Both
            # are valid fail-closed outcomes after a correct reseal.
            for name, document in resealed.items():
                generator.validate_document(name, document)
            generator.validate_artifacts(resealed, self.manifest, self.inputs)

    def test_independent_frozen_oracles_have_expected_exact_denominators(self) -> None:
        self.assertEqual(len(self.baseline_ato_ids), 3338)
        self.assertEqual(len(self.baseline_atv_ids), 3338)
        self.assertEqual(len(self.legacy_alias_targets), 3262)
        self.assertEqual(len(self.folded_occurrence_ids), 76)
        self.assertEqual(len(self.v2_candidate_keys), 98)
        self.assertEqual(len(self.audit_delta_keys), 56)
        self.assertTrue(self.v2_candidate_keys.isdisjoint(self.audit_delta_keys))

        ato_by_domain: dict[str, set[str]] = {}
        for row in self.v2_source["records"]:
            domain = row["raw_fields"]["discipline"]
            ato_by_domain.setdefault(domain, set()).add(row["occurrence_id"])
        self.assertEqual(
            {key: len(value) for key, value in ato_by_domain.items()},
            {"数学": 1666, "物理": 1272, "计算机科学": 400},
        )

        aliases_by_prefix = {
            prefix: sum(alias.startswith(prefix) for alias in self.legacy_alias_targets)
            for prefix in ("THM-M-", "THM-P-", "THM-C-")
        }
        self.assertEqual(
            aliases_by_prefix,
            {"THM-M-": 1601, "THM-P-": 1263, "THM-C-": 398},
        )

    def test_manifest_dispositions_are_exact_98_plus_56_key_union(self) -> None:
        rows = [
            row
            for fragment in self.fragments
            for row in fragment["dispositions"]
        ]
        keys = [row["candidate_key"] for row in rows]
        self.assertEqual(len(keys), len(set(keys)), "candidate disposition duplicated")
        frozen_keys = {
            row["candidate_key"]
            for row in rows
            if row["origin"] != "stage4_discovery"
        }
        self.assertEqual(
            frozen_keys, self.v2_candidate_keys | self.audit_delta_keys
        )
        self.assertEqual(
            {row["candidate_key"] for row in self.v2_coverage["missing_candidates"]},
            {
                row["candidate_key"]
                for fragment in self.fragments
                for row in fragment["dispositions"]
                if row["origin"] == "v2_missing"
            },
        )
        self.assertEqual(
            {row["candidate_key"] for row in self.v2_coverage["present_collisions"]},
            {
                row["candidate_key"]
                for fragment in self.fragments
                for row in fragment["dispositions"]
                if row["origin"] == "v2_collision"
            },
        )
        projected_rows = self.payload("Candidate_Dispositions_v4.json")[
            "dispositions"
        ]
        projected_keys = [row["candidate_key"] for row in projected_rows]
        self.assertEqual(len(projected_keys), len(set(projected_keys)))
        self.assertEqual(
            {
                row["candidate_key"]
                for row in projected_rows
                if row["origin"] != "stage4_discovery"
            },
            self.v2_candidate_keys | self.audit_delta_keys,
        )

    def test_compound_cryptographic_candidates_have_atomic_children(self) -> None:
        dispositions = {
            row["candidate_key"]: row
            for fragment in self.fragments
            for row in fragment["dispositions"]
        }
        additions = {
            row["curation_key"]: row
            for fragment in self.fragments
            for row in fragment["additions"]
        }
        expected = {
            "missing.cs.cdh_ddh_assumptions": [
                "cs.cdh_assumption",
                "cs.ddh_assumption",
                "cs.cdh_assumption.profile_v1",
                "cs.ddh_assumption.profile_v1",
            ],
            "missing.cs.lwe_sis_assumptions": [
                "cs.search_lwe_assumption",
                "cs.decision_lwe_assumption",
                "cs.sis_assumption",
                "cs.search_lwe_assumption.profile_v1",
                "cs.decision_lwe_assumption.profile_v1",
                "cs.sis_assumption.profile_v1",
            ],
        }
        for candidate_key, child_keys in expected.items():
            disposition = dispositions[candidate_key]
            self.assertEqual(disposition["disposition"], "nonclaim")
            self.assertEqual(disposition["child_keys"], child_keys)
            self.assertEqual(len(child_keys), len(set(child_keys)))
            for child_key in child_keys:
                child = additions[child_key]
                self.assertEqual(child["candidate_keys"], [candidate_key])
                self.assertEqual(child["record_role"], "claim")
                self.assertEqual(child["claim_kind"], "assumption")
                self.assertEqual(child["atomicity"], "atomic")
                self.assertNotIn("evidence_inherited", child)

        projected = {
            row["candidate_key"]: row
            for row in self.payload("Candidate_Dispositions_v4.json")["dispositions"]
        }
        catalog_by_key = {
            row["curation_key"]: row
            for row in self.payload("Claim_Catalog_v4.json")["records"]
            if row.get("curation_key")
        }
        for candidate_key, child_keys in expected.items():
            row = projected[candidate_key]
            self.assertEqual(
                [child["curation_key"] for child in row["children"]], child_keys
            )
            self.assertEqual(len(row["allocated_atv_ids"]), len(child_keys))
            self.assertTrue(
                all(id_ordinal(value) > 3338 for value in row["allocated_atv_ids"])
            )
            for child_key in child_keys:
                record = catalog_by_key[child_key]
                self.assertEqual(record["record_role"], "claim")
                self.assertEqual(record["current_claim_kind"], "assumption")
                self.assertEqual(record["atomicity"], "atomic")

    def test_pristine_documents_pass_public_validation_interfaces(self) -> None:
        generator.validate_manifest(self.manifest, self.inputs)
        for name, document in self.documents.items():
            generator.validate_document(name, document)
        generator.validate_artifacts(self.documents, self.manifest, self.inputs)

    def test_check_mode_is_read_only(self) -> None:
        paths = sorted(
            {
                Path(path)
                for path in generator.OUTPUT_PATHS
                if Path(path).is_file()
            }
        )
        self.assertTrue(paths, "generator declares no existing output paths")
        before = {
            path: (
                path.read_bytes(),
                path.stat().st_mtime_ns,
                path.stat().st_ino,
            )
            for path in paths
        }
        result = subprocess.run(
            [sys.executable, str(GENERATOR_PATH), "--check"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS", result.stdout)
        after = {
            path: (
                path.read_bytes(),
                path.stat().st_mtime_ns,
                path.stat().st_ino,
            )
            for path in paths
        }
        self.assertEqual(after, before, "--check rewrote an output artifact")

    def test_published_release_rejects_bootstrap_replacement_without_writes(self) -> None:
        paths = tuple(Path(path) for path in generator.OUTPUT_PATHS)
        before = {
            path: (path.read_bytes(), path.stat().st_mtime_ns, path.stat().st_ino)
            for path in paths
        }
        result = subprocess.run(
            [
                sys.executable,
                str(GENERATOR_PATH),
                "--bootstrap-replace-unreleased",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("released", result.stdout)
        after = {
            path: (path.read_bytes(), path.stat().st_mtime_ns, path.stat().st_ino)
            for path in paths
        }
        self.assertEqual(after, before, "release guard rewrote an output artifact")

    def test_build_is_deterministic_and_matches_committed_artifacts(self) -> None:
        first = generator.build_artifacts()
        second = generator.build_artifacts()
        self.assertEqual(first, second)
        self.assertEqual(set(first), set(generator.OUTPUT_PATHS))
        for path, rendered in first.items():
            self.assertEqual(Path(path).read_text(encoding="utf-8"), rendered)

    def test_public_build_accepts_only_the_current_root_and_loaded_generation(self) -> None:
        trusted = generator.load_inputs()
        expected = generator.build_artifacts()
        self.assertEqual(generator.build_artifacts(inputs=trusted), expected)
        self.assertEqual(
            generator.build_artifacts(
                manifest=trusted["manifest"],
                inputs=trusted,
            ),
            expected,
        )

        effective = generator.validate_manifest(trusted["manifest"], trusted)
        with self.assertRaisesRegex(
            generator.CatalogError,
            "manifest.*differs|effective.*forbidden|override",
        ):
            generator.build_artifacts(manifest=effective, inputs=trusted)

        mutated_inputs = copy.deepcopy(trusted)
        mutated_inputs["catalog_v2"]["records"][0]["identity"][
            "preferred_label"
        ] += " [in-memory authority drift]"
        with self.assertRaisesRegex(
            generator.CatalogError,
            "loaded inputs differ|authoritative objects|prior lifecycle bytes",
        ):
            generator.build_artifacts(inputs=mutated_inputs)

    def test_generation_snapshot_cas_fails_before_first_replace(self) -> None:
        """A stale input or prior-output view must never partially publish."""

        outputs = generator.build_artifacts()
        current_snapshot = generator.capture_generation_snapshot(self.manifest)
        output_paths = tuple(Path(path) for path in generator.OUTPUT_PATHS)
        self.assertEqual(len(output_paths), 13)
        before_bytes = {path: path.read_bytes() for path in output_paths}
        before_staged = set(V4_DIR.glob(".*.tmp"))

        for snapshot_group, expected_detail in (
            ("authoritative_inputs", "authoritative inputs"),
            ("previous_outputs", "prior output/allocator snapshot"),
        ):
            with self.subTest(snapshot_group=snapshot_group):
                stale_snapshot = copy.deepcopy(current_snapshot)
                victim = next(
                    row for row in stale_snapshot[snapshot_group] if row["exists"]
                )
                victim["sha256"] = (
                    "0" * 64 if victim["sha256"] != "0" * 64 else "1" * 64
                )
                replace = mock.Mock(
                    side_effect=AssertionError(
                        "os.replace was called before the generation CAS passed"
                    )
                )
                with mock.patch.object(generator.os, "replace", replace):
                    with self.assertRaisesRegex(
                        generator.CatalogError,
                        rf"Stage4 generation snapshot CAS failed: {re.escape(expected_detail)}",
                    ):
                        generator.write_artifacts(outputs, stale_snapshot)

                replace.assert_not_called()
                self.assertEqual(
                    {path: path.read_bytes() for path in output_paths},
                    before_bytes,
                    "a failed generation CAS changed a published artifact",
                )
                self.assertEqual(
                    set(V4_DIR.glob(".*.tmp")),
                    before_staged,
                    "a failed generation CAS left staged temporary files behind",
                )

    def test_stage4_generation_lock_excludes_an_independent_process(self) -> None:
        """The V4 directory flock is process-wide writer mutual exclusion."""

        contender = """
import fcntl
import os
import sys

descriptor = os.open(sys.argv[1], os.O_RDONLY)
try:
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("BLOCKED")
    else:
        print("ENTERED")
        fcntl.flock(descriptor, fcntl.LOCK_UN)
finally:
    os.close(descriptor)
"""

        # Isolate this primitive-level test from legitimate concurrent Stage4
        # checker/generator processes in the shared worktree.  The production
        # function still opens and flocks its configured directory inode.
        with tempfile.TemporaryDirectory() as temporary:
            isolated_v4 = Path(temporary) / "v4"
            with mock.patch.object(generator, "V4_DIR", isolated_v4):
                with generator.stage4_generation_lock(exclusive=True):
                    blocked = subprocess.run(
                        [sys.executable, "-c", contender, str(isolated_v4)],
                        cwd=ROOT,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        timeout=10,
                        check=False,
                    )
                self.assertEqual(blocked.returncode, 0, blocked.stdout)
                self.assertEqual(blocked.stdout.strip(), "BLOCKED", blocked.stdout)

                entered = subprocess.run(
                    [sys.executable, "-c", contender, str(isolated_v4)],
                    cwd=ROOT,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    timeout=10,
                    check=False,
                )
                self.assertEqual(entered.returncode, 0, entered.stdout)
                self.assertEqual(entered.stdout.strip(), "ENTERED", entered.stdout)

    def test_baseline_occurrences_aliases_and_folded_set_are_conserved(self) -> None:
        source = self.payload("Source_Records_v4.json")
        source_rows = first_list(source, "records", "source_occurrences")
        occurrence_ids = [row["occurrence_id"] for row in source_rows]
        self.assertEqual(len(occurrence_ids), len(set(occurrence_ids)))
        self.assertEqual(
            set(source["baseline_occurrence_ids"]), self.baseline_ato_ids
        )
        self.assertEqual(len(source["baseline_occurrence_ids"]), 3338)
        self.assertEqual(
            set(occurrence_ids) & self.baseline_ato_ids,
            self.baseline_ato_ids,
        )

        universe = source.get("universe", source)
        folded = universe.get(
            "folded_occurrence_ids",
            universe.get("baseline_folded_occurrence_ids"),
        )
        self.assertIsInstance(folded, list)
        self.assertEqual(set(folded), self.folded_occurrence_ids)
        self.assertEqual(len(folded), 76)

        registry = self.payload("Claim_ID_Registry_v4.json")
        registry_variant_ids = {row["variant_id"] for row in registry["variants"]}
        self.assertEqual(
            registry_variant_ids & self.baseline_atv_ids, self.baseline_atv_ids
        )
        alias_rows = first_list(registry, "legacy_aliases")
        aliases = {
            row["alias_id"]: row.get(
                "historical_atv_id", row.get("target_variant_id")
            )
            for row in alias_rows
        }
        self.assertEqual(aliases, self.legacy_alias_targets)

        migration = self.payload("Claim_ID_Migration_v2_to_v4.json")
        historical = {
            row["alias_id"]: row["historical_target_variant_id"]
            for row in migration["legacy_alias_migrations"]
        }
        self.assertEqual(historical, self.legacy_alias_targets)
        self.assertTrue(
            all(row["rebound"] is False for row in migration["legacy_alias_migrations"])
        )

    def test_atv_and_stage4_numbering_are_a_bijection_with_equal_ordinals(self) -> None:
        catalog_rows = first_list(
            self.payload("Claim_Catalog_v4.json"), "records", "claims"
        )
        catalog_atv = [
            value
            for row in catalog_rows
            if (value := row_atv_id(row)) is not None
        ]
        self.assertEqual(len(catalog_atv), len(set(catalog_atv)))
        self.assertTrue(self.baseline_atv_ids <= set(catalog_atv))

        numbering = self.payload("Stage4_Claim_ID_Registry_v4.json")
        rows = first_list(numbering, "mappings", "rows", "numbering", "records")
        pairs: list[tuple[str, str]] = []
        for row in rows:
            atv_id = row_atv_id(row)
            stage_id = row_stage_id(row)
            self.assertIsNotNone(atv_id)
            self.assertIsNotNone(stage_id)
            assert atv_id is not None and stage_id is not None
            self.assertRegex(atv_id, r"^ATV-[0-9]{8}$")
            self.assertRegex(stage_id, r"^S4-CLM-[0-9]{8}$")
            self.assertEqual(id_ordinal(atv_id), id_ordinal(stage_id))
            pairs.append((atv_id, stage_id))
        self.assertEqual(len(pairs), len({atv for atv, _stage in pairs}))
        self.assertEqual(len(pairs), len({stage for _atv, stage in pairs}))
        self.assertEqual({atv for atv, _stage in pairs}, set(catalog_atv))

        mapping = dict(pairs)
        self.assertEqual(
            self.legacy_alias_targets["THM-M-0387"], "ATV-00000393"
        )
        self.assertEqual(mapping["ATV-00000393"], "S4-CLM-00000393")
        migration_alias = next(
            row
            for row in self.payload("Claim_ID_Migration_v2_to_v4.json")[
                "legacy_alias_migrations"
            ]
            if row["alias_id"] == "THM-M-0387"
        )
        self.assertEqual(
            migration_alias,
            {
                "alias_id": "THM-M-0387",
                "historical_target_variant_id": "ATV-00000393",
                "historical_stage_claim_id": "S4-CLM-00000393",
                "rebound": False,
            },
        )

    def test_new_typed_ids_are_unique_append_only_suffixes(self) -> None:
        registry = self.payload("Claim_ID_Registry_v4.json")
        contracts = {
            "ATO": ("occurrences", 3338, "occurrence_id"),
            "ATF": ("families", 3119, "family_id"),
            "ATS": ("senses", 3338, "sense_id"),
            "ATV": ("variants", 3338, "variant_id"),
        }
        source_rows = first_list(
            self.payload("Source_Records_v4.json"), "records", "source_occurrences"
        )
        for namespace, (field, old_highwater, id_field) in contracts.items():
            rows = source_rows if namespace == "ATO" else first_list(registry, field)
            identifiers = [row[id_field] for row in rows]
            self.assertEqual(len(identifiers), len(set(identifiers)))
            new_ordinals = sorted(
                id_ordinal(identifier)
                for identifier in identifiers
                if id_ordinal(identifier) > old_highwater
            )
            self.assertTrue(new_ordinals, f"Stage4 allocated no new {namespace} IDs")
            self.assertEqual(
                new_ordinals,
                list(range(old_highwater + 1, max(new_ordinals) + 1)),
            )

    def test_splits_have_no_default_and_inherit_no_evidence(self) -> None:
        registry = self.payload("Claim_ID_Registry_v4.json")
        migrations = self.payload("Claim_ID_Migration_v2_to_v4.json")
        split_rows: list[dict] = []
        split_rows.extend(
            row
            for row in registry.get("splits", [])
            if isinstance(row, dict)
        )
        for row in first_list(migrations, "mappings", "migrations", "rows"):
            action = row.get("action", row.get("migration_action"))
            resolution = row.get("current_resolution")
            if action == "split" or (
                isinstance(resolution, dict) and resolution.get("kind") == "split"
            ):
                split_rows.append(row)
        self.assertTrue(split_rows, "Stage4 contains no executable split fixture")
        forbidden_defaults = {
            "default_child",
            "default_child_id",
            "default_target",
            "preferred_child",
        }
        for row in split_rows:
            serialized = json.dumps(row, ensure_ascii=False, sort_keys=True)
            if "child_variant_ids" in row:
                self.assertGreaterEqual(len(row["child_variant_ids"]), 2)
                self.assertEqual(
                    len(row["child_variant_ids"]), len(set(row["child_variant_ids"]))
                )
            for key in forbidden_defaults:
                if key in row:
                    self.assertIn(row[key], (None, "", False))
            for key in (
                "evidence_inherited",
                "inherits_evidence",
                "proof_inherited",
                "status_inherited",
                "receipt_inherited",
                "evidence_inheritance",
            ):
                if key in row:
                    self.assertIn(row[key], (False, None, [], {}, "none"))
            self.assertNotRegex(serialized, r'"default_child"\s*:\s*"S4-CLM-')
            resolution = row.get("current_resolution")
            if isinstance(resolution, dict) and resolution.get("kind") == "split":
                self.assertIsNone(resolution.get("default_child"))
                self.assertIs(resolution.get("evidence_inherited"), False)
                self.assertGreaterEqual(
                    len(resolution.get("target_stage_claim_ids", [])), 2
                )

    def test_theorem_open_and_status_json_are_strict_catalog_projections(self) -> None:
        catalog_rows = first_list(
            self.payload("Claim_Catalog_v4.json"), "records", "claims"
        )
        numbering_rows = first_list(
            self.payload("Stage4_Claim_ID_Registry_v4.json"),
            "mappings",
            "rows",
            "numbering",
            "records",
        )
        stage_by_atv = {
            row_atv_id(row): row_stage_id(row) for row in numbering_rows
        }
        expected_theorem: set[str] = set()
        expected_open: set[str] = set()
        expected_status: dict[str, set[str]] = {}
        theorem_kinds = {
            "theorem",
            "lemma",
            "result",
            "complexity_result",
            "undecidability_result",
            "no_go_theorem",
            "reconstruction_theorem",
            "representation_theorem",
            "structure_theorem",
            "sum_rule",
            "model_consequence",
            "identity",
            "inequality",
            "law",
        }
        open_kinds = {"conjecture", "hypothesis", "open_problem", "assumption"}
        open_statuses = {
            "open",
            "unresolved",
            "independent",
            "partial",
            "partially_resolved",
            "disputed",
            "conditional_open",
        }
        status_aliases = {
            "proven": "proved",
            "established": "proved",
            "true": "proved",
            "resolved_proved": "proved",
            "confirmed": "proved",
            "unresolved": "open",
            "open_problem": "open",
            "disproved": "refuted",
            "false": "refuted",
            "counterexample": "refuted",
            "independence": "independent",
            "partially_resolved": "partial",
            "contested": "disputed",
            "conditional_open": "conditional",
            "conditional_assumption": "conditional",
            "assumption": "conditional",
            "unreviewed": "unknown",
            "missing": "unknown",
            "none": "unknown",
            "": "unknown",
        }
        for row in catalog_rows:
            atv_id = row_atv_id(row)
            if atv_id is None:
                continue
            stage_id = stage_by_atv[atv_id]
            assert stage_id is not None
            raw_status = (material_status(row) or "unknown").strip().casefold()
            bucket = status_aliases.get(raw_status, raw_status.replace(" ", "_") or "unknown")
            expected_status.setdefault(bucket, set()).add(stage_id)
            eligible = is_atomic_truth_claim(row) and not row.get("split_children")
            is_open = eligible and bucket in {
                "open",
                "partial",
                "independent",
                "conditional",
                "disputed",
            }
            if eligible and bucket == "proved":
                expected_theorem.add(stage_id)
            if is_open:
                expected_open.add(stage_id)

        theorem = projection_ids(self.document("Theorem_List_v4.json"))
        open_claims = projection_ids(
            self.document("Conjecture_Hypothesis_Open_List_v4.json")
        )
        self.assertEqual(len(theorem), len(set(theorem)))
        self.assertEqual(len(open_claims), len(set(open_claims)))
        self.assertEqual(set(theorem), expected_theorem)
        self.assertEqual(set(open_claims), expected_open)
        self.assertTrue(set(theorem).isdisjoint(open_claims))

        status_document = self.document("Status_Index_v4.json")
        status_rows = first_list(status_document, "records")
        self.assertEqual(len(status_rows), len(catalog_rows))
        self.assertEqual(
            {row["stage_claim_id"] for row in status_rows},
            {stage_by_atv[row_atv_id(row)] for row in catalog_rows},
        )
        observed_status: dict[str, set[str]] = {}
        for row in status_rows:
            observed_status.setdefault(row["status_bucket"], set()).add(
                row["stage_claim_id"]
            )
        self.assertEqual(observed_status, expected_status)
        self.assertEqual(
            status_document["counts"]["buckets"],
            {key: len(value) for key, value in sorted(expected_status.items())},
        )

        rendered_by_name = {Path(path).name: text for path, text in self.rendered.items()}
        md_contracts = (
            ("Theorem_List_v4.md", set(theorem)),
            ("Conjecture_Hypothesis_Open_List_v4.md", set(open_claims)),
        )
        for name, expected in md_contracts:
            ids = re.findall(r"(?<![A-Za-z0-9-])S4-CLM-[0-9]{8}(?![0-9])", rendered_by_name[name])
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(set(ids), expected)

    def test_every_stage4_source_reference_resolves(self) -> None:
        declared_sources: dict[str, str] = {}
        for document in self.documents.values():
            payload = document_payload(document)
            for row in payload.get("sources", payload.get("source_assets", [])):
                source_id = row.get("source_id", row.get("source_asset_id"))
                locator = row.get("locator", row.get("path", row.get("url")))
                if isinstance(source_id, str) and isinstance(locator, str):
                    declared_sources[source_id] = locator

        def resolve(value: str) -> None:
            locator = declared_sources.get(value, value)
            parsed = urlparse(locator)
            if parsed.scheme in {"http", "https"}:
                self.assertTrue(parsed.netloc, locator)
                return
            if parsed.scheme == "doi":
                self.assertTrue(parsed.path, locator)
                return
            relative = Path(locator.split("#", 1)[0])
            self.assertFalse(relative.is_absolute(), locator)
            self.assertNotIn("..", relative.parts, locator)
            self.assertTrue((ROOT / relative).is_file(), locator)

        self.assertTrue(declared_sources)
        for locator in declared_sources.values():
            resolve(locator)

        refs_seen = 0

        def walk(value: object) -> None:
            nonlocal refs_seen
            if isinstance(value, dict):
                for key, child in value.items():
                    if key == "source_refs" or key.endswith("_source_refs"):
                        self.assertIsInstance(child, list)
                        for ref in child:
                            self.assertIsInstance(ref, str)
                            refs_seen += 1
                            resolve(ref)
                    else:
                        walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        for name, document in self.documents.items():
            walk(document_payload(document))
        self.assertGreater(refs_seen, 0)

    def test_all_baseline_byte_locators_still_resolve_exact_raw_blocks(self) -> None:
        assets: dict[str, bytes] = {}
        for item in self.v2_source["source_snapshot"]["files"]:
            path = ROOT / item["path"]
            payload = path.read_bytes()
            self.assertEqual(len(payload), item["size_bytes"])
            self.assertEqual(sha256_bytes(payload), item["sha256"])
            assets[item["path"]] = payload
        for row in self.v2_source["records"]:
            locator = row["current_locator"]
            payload = assets[locator["path"]]
            start = locator["byte_start"]
            end = locator["byte_end_exclusive"]
            self.assertGreater(end, start)
            self.assertLessEqual(end, len(payload))
            self.assertEqual(
                sha256_bytes(payload[start:end]), locator["raw_block_sha256"]
            )

    def test_manifest_drop_and_count_preserving_substitution_are_rejected(self) -> None:
        effective = generator.validate_manifest(self.manifest, self.inputs)

        dropped = copy.deepcopy(effective)
        dropped["dispositions"].pop(0)
        with self.assertRaises(generator.CatalogError):
            generator._build_artifacts_from_loaded(dropped, self.inputs)

        substituted = copy.deepcopy(effective)
        victim = substituted["dispositions"][0]
        victim["candidate_key"] = "missing.math.count_preserving_substitute"
        victim["origin"] = "stage4_discovery"
        with self.assertRaises(generator.CatalogError):
            generator._build_artifacts_from_loaded(substituted, self.inputs)

    def test_dropped_baseline_occurrence_is_rejected_after_resealing(self) -> None:
        documents, source = self.mutable_artifact("Source_Records_v4.json")
        index = next(
            index
            for index, row in enumerate(source["records"])
            if row["occurrence_id"] in self.baseline_ato_ids
        )
        source["records"].pop(index)
        self.assert_rejected(documents)

    def test_count_preserving_baseline_id_substitution_is_rejected(self) -> None:
        documents, source = self.mutable_artifact("Source_Records_v4.json")
        victim = next(
            row
            for row in source["records"]
            if row["occurrence_id"] in self.baseline_ato_ids
        )
        victim["occurrence_id"] = "ATO-99999999"
        self.assertEqual(len(source["records"]), len(self.payload("Source_Records_v4.json")["records"]))
        self.assert_rejected(documents)

    def test_candidate_drop_and_count_preserving_key_substitution_are_rejected(self) -> None:
        dropped, candidate = self.mutable_artifact("Candidate_Dispositions_v4.json")
        candidate["dispositions"].pop(0)
        self.assert_rejected(dropped)
        del dropped, candidate

        substituted, candidate = self.mutable_artifact("Candidate_Dispositions_v4.json")
        original_count = len(candidate["dispositions"])
        candidate["dispositions"][0]["candidate_key"] = (
            "missing.cs.count_preserving_substitute"
        )
        self.assertEqual(len(candidate["dispositions"]), original_count)
        self.assert_rejected(substituted)

    def test_candidate_child_allocation_mismatch_is_rejected(self) -> None:
        documents, candidate = self.mutable_artifact("Candidate_Dispositions_v4.json")
        victim = next(
            row for row in candidate["dispositions"] if row["allocated_atv_ids"]
        )
        victim["allocated_atv_ids"][0] = "ATV-00000001"
        self.assert_rejected(documents)

    def test_numbering_ordinal_mismatch_is_rejected(self) -> None:
        documents, stage = self.mutable_artifact("Stage4_Claim_ID_Registry_v4.json")
        stage["mappings"][0]["stage_claim_id"] = "S4-CLM-99999999"
        self.assert_rejected(documents)

    def test_historical_alias_rebinding_is_rejected(self) -> None:
        documents, registry = self.mutable_artifact("Claim_ID_Registry_v4.json")
        alias = next(
            row for row in registry["legacy_aliases"] if row["alias_id"] == "THM-M-0387"
        )
        alias["target_variant_id"] = "ATV-00000001"
        self.assert_rejected(documents)

    def test_split_default_and_evidence_inheritance_mutations_are_rejected(self) -> None:
        defaulted, registry = self.mutable_artifact("Claim_ID_Registry_v4.json")
        splits = registry["splits"]
        self.assertTrue(splits)
        splits[0]["default_child"] = splits[0]["child_variant_ids"][0]
        self.assert_rejected(defaulted)
        del defaulted, registry, splits

        inherited, registry = self.mutable_artifact("Claim_ID_Registry_v4.json")
        splits = registry["splits"]
        splits[0]["evidence_inherited"] = True
        self.assert_rejected(inherited)

    def test_projection_drop_and_count_preserving_substitution_are_rejected(self) -> None:
        dropped, theorem = self.mutable_artifact("Theorem_List_v4.json")
        self.assertTrue(theorem["records"])
        theorem["records"].pop(0)
        theorem["stage_claim_ids"].pop(0)
        self.assert_rejected(dropped)
        del dropped, theorem

        substituted, status = self.mutable_artifact("Status_Index_v4.json")
        original_count = len(status["records"])
        status["records"][0] = copy.deepcopy(status["records"][1])
        status["stage_claim_ids"][0] = status["stage_claim_ids"][1]
        self.assertEqual(len(status["records"]), original_count)
        self.assert_rejected(substituted)

    def test_pristine_generated_outputs_pass_independent_checker(self) -> None:
        checker = self.run_independent_checker()
        self.assertEqual(checker.errors, [], checker.errors)
        self.assertIn(
            "global_baseline_semantic_completion=false",
            checker.notes,
        )

    def test_manifest_closed_enums_and_real_calendar_dates_fail_closed(self) -> None:
        effective = generator.validate_manifest(self.manifest, self.inputs)
        mutations = {
            "claim_kind": lambda value: value["additions"][0].__setitem__(
                "claim_kind", "invented_claim_kind"
            ),
            "atomicity": lambda value: value["additions"][0].__setitem__(
                "atomicity", "almost_atomic"
            ),
            "material_status": lambda value: value["additions"][0][
                "material_status"
            ].__setitem__("status", "probably_proved"),
            "rights_status": lambda value: value["additions"][0].__setitem__(
                "rights_status", "rights_maybe_known"
            ),
            "historical_kind": lambda value: value["additions"][0].__setitem__(
                "historical_kind", "historic_typo"
            ),
            "owner_domain": lambda value: value["additions"][0].__setitem__(
                "owner_domain", "maths"
            ),
            "review_date": lambda value: value.__setitem__(
                "review_date", "9999-99-99"
            ),
            "status_as_of": lambda value: value["additions"][0][
                "material_status"
            ].__setitem__("as_of", "9999-99-99"),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                value = copy.deepcopy(effective)
                mutate(value)
                with self.assertRaises(generator.CatalogError):
                    generator.validate_manifest(value, self.inputs)

    def test_every_artifact_rejects_resealed_declared_count_mutation(self) -> None:
        self.assertEqual(
            set(self.documents),
            {Path(path).name for path in generator.JSON_OUTPUT_PATHS},
        )
        for name, document in self.documents.items():
            with self.subTest(artifact=name):
                tampered = dict(document)
                tampered["counts"] = dict(document["counts"])
                numeric_key = next(
                    key
                    for key, value in tampered["counts"].items()
                    if isinstance(value, int) and not isinstance(value, bool)
                )
                tampered["counts"][numeric_key] += 1
                tampered = independently_reseal(tampered)
                self.assertEqual(
                    tampered["authority_sha256"],
                    generator.document_authority(tampered),
                )
                with self.assertRaisesRegex(generator.CatalogError, "counts differ"):
                    generator.validate_document(name, tampered)

    def test_repair_artifact_resealed_semantic_mutations_fail_closed(self) -> None:
        """All 623 proposal rows remain exact, inert, and source-derived."""

        name = "Repair_Proposal_Dispositions_v4.json"

        def assert_independent_semantic_rejection(document: dict) -> None:
            self.assertEqual(
                document["authority_sha256"],
                generator.document_authority(document),
            )
            checker = self.run_independent_checker({name: document})
            self.assertTrue(checker.errors, "repair mutation passed the independent checker")
            self.assertFalse(
                any("stale authority_sha256" in error for error in checker.errors),
                checker.errors,
            )
            self.assertTrue(
                any("repair" in error.casefold() for error in checker.errors),
                checker.errors,
            )

        for mutation in (
            "pending",
            "content",
            "proposal_hash",
            "truth_credit",
            "drop",
            "duplicate",
        ):
            with self.subTest(mutation=mutation):
                repair = copy.deepcopy(self.document(name))
                rows = repair["dispositions"]
                victim = rows[0]
                if mutation == "pending":
                    victim["disposition"] = "pending"
                elif mutation == "content":
                    content_field = next(
                        field
                        for field, value in victim["proposal"].items()
                        if isinstance(value, str) and value
                    )
                    victim["proposal"][content_field] += " [coordinated content drift]"
                    victim["proposal_sha256"] = independent_stable_digest(
                        "awesome-theorems/stage4-repair-proposal/v4",
                        victim["proposal"],
                    )
                elif mutation == "proposal_hash":
                    victim["proposal_sha256"] = (
                        "0" * 64
                        if victim["proposal_sha256"] != "0" * 64
                        else "1" * 64
                    )
                elif mutation == "truth_credit":
                    victim["grants_truth_credit"] = True
                elif mutation == "drop":
                    rows.pop(0)
                elif mutation == "duplicate":
                    rows.append(copy.deepcopy(victim))
                else:
                    raise AssertionError(mutation)

                repair = independently_recount_and_reseal(repair)
                generator.validate_document(name, repair)
                assert_independent_semantic_rejection(repair)

        count_mutation = copy.deepcopy(self.document(name))
        count_mutation["counts"]["total"] += 1
        count_mutation = independently_reseal(count_mutation)
        self.assertEqual(
            count_mutation["authority_sha256"],
            generator.document_authority(count_mutation),
        )
        with self.assertRaisesRegex(generator.CatalogError, "counts differ"):
            generator.validate_document(name, count_mutation)
        assert_independent_semantic_rejection(count_mutation)

    def test_repair_artifact_payload_cannot_mask_resealed_top_level_mutation(self) -> None:
        """A pristine injected payload cannot shadow a hostile signed envelope."""

        name = "Repair_Proposal_Dispositions_v4.json"
        pristine = copy.deepcopy(self.document(name))
        smuggled = copy.deepcopy(pristine)
        smuggled["dispositions"][0]["disposition"] = "pending"
        smuggled["payload"] = copy.deepcopy(pristine)
        smuggled = independently_recount_and_reseal(smuggled)

        self.assertEqual(smuggled["dispositions"][0]["disposition"], "pending")
        self.assertEqual(smuggled["payload"], pristine)
        self.assertEqual(
            smuggled["authority_sha256"],
            generator.document_authority(smuggled),
        )
        generator.validate_document(name, smuggled)

        checker = self.run_independent_checker({name: smuggled})
        self.assertTrue(
            checker.errors,
            "checker accepted a pristine payload that masked hostile top-level repair bytes",
        )
        self.assertFalse(
            any("stale authority_sha256" in error for error in checker.errors),
            checker.errors,
        )
        self.assertTrue(
            any(
                "payload" in error.casefold() or "repair" in error.casefold()
                for error in checker.errors
            ),
            checker.errors,
        )

    def test_independent_checker_rejects_resealed_baseline_atf_mutation(self) -> None:
        registry = copy.deepcopy(self.document("Claim_ID_Registry_v4.json"))
        victim = next(
            row
            for row in registry["families"]
            if row["family_id"] == "ATF-00000001"
        )
        victim["lexical_title_key"] += "-tampered"
        registry = independently_reseal(registry)
        self.assert_independent_rejected(
            {"Claim_ID_Registry_v4.json": registry},
            "Stage4 ATF registry mutates baseline rows",
        )

    def test_independent_checker_rejects_resealed_catalog_authority_mutations(self) -> None:
        catalog = self.document("Claim_Catalog_v4.json")
        victim_index = next(
            index
            for index, row in enumerate(catalog["records"])
            if row.get("curation_key") and row.get("record_role") == "claim"
        )

        statement_mutation = copy.deepcopy(catalog)
        statement_victim = statement_mutation["records"][victim_index]
        statement_victim["statement"]["natural_language"] += (
            " [coordinated same-ID tamper]"
        )
        tampered_text = statement_victim["statement"]["natural_language"]
        status_mutation = copy.deepcopy(self.document("Status_Index_v4.json"))
        status_victim = next(
            row
            for row in status_mutation["records"]
            if row["variant_id"] == statement_victim["variant_id"]
        )
        status_victim["statement"]["natural_language"] = tampered_text
        statement_mutation = independently_reseal(statement_mutation)
        status_mutation = independently_reseal(status_mutation)
        self.assert_independent_rejected(
            {
                "Claim_Catalog_v4.json": statement_mutation,
                "Status_Index_v4.json": status_mutation,
            },
            "differs from authoritative synthesis at field 'statement'",
        )

        rights_mutation = copy.deepcopy(catalog)
        rights = rights_mutation["records"][victim_index]["rights_status"]
        rights_mutation["records"][victim_index]["rights_status"] = (
            "citation_only_rights_unresolved"
            if rights == "bibliographic_metadata_only"
            else "bibliographic_metadata_only"
        )
        rights_mutation = independently_reseal(rights_mutation)
        self.assert_independent_rejected(
            {"Claim_Catalog_v4.json": rights_mutation},
            "differs from authoritative synthesis at field 'rights_status'",
        )

        count_mutation = dict(catalog)
        count_mutation["counts"] = dict(catalog["counts"])
        count_mutation["counts"]["records"] += 1
        count_mutation = independently_reseal(count_mutation)
        self.assert_independent_rejected(
            {"Claim_Catalog_v4.json": count_mutation},
            "catalog counts differ from authoritative synthesis",
        )

    def test_independent_checker_rejects_same_id_projection_content_mutation(self) -> None:
        theorem = copy.deepcopy(self.document("Theorem_List_v4.json"))
        self.assertTrue(theorem["records"])
        original_id = theorem["records"][0]["stage_claim_id"]
        theorem["records"][0]["preferred_label"] += " [same-ID tamper]"
        self.assertEqual(theorem["records"][0]["stage_claim_id"], original_id)
        theorem = independently_reseal(theorem)
        self.assert_independent_rejected(
            {"Theorem_List_v4.json": theorem},
            "theorem projection row[0] differs from authoritative synthesis",
        )

    def test_previous_v4_nonsemantic_changes_preserve_allocated_ato_birth_rows(self) -> None:
        prior_source = self.inputs["previous_v4"]["Source_Records_v4.json"]
        prior_registry = self.inputs["previous_v4"]["Claim_ID_Registry_v4.json"]
        prior_source_by_key = {
            row["curation_key"]: row
            for row in prior_source["records"]
            if row.get("curation_key")
        }
        prior_variant_by_key = {
            row["curation_key"]: row
            for row in prior_registry["variants"]
            if row.get("curation_key")
        }
        self.assertTrue(prior_source_by_key)

        effective = generator.validate_manifest(self.manifest, self.inputs)
        victim = next(
            row
            for row in effective["additions"]
            if row["curation_key"] in prior_source_by_key
            and isinstance(row["preferred_label"], str)
            and row["record_role"] == "claim"
            and row["material_status"]["status"] == "proved"
        )
        key = victim["curation_key"]
        new_label = victim["preferred_label"] + " — metadata relabel"
        victim["preferred_label"] = new_label
        victim["aliases"] = [*victim["aliases"], "metadata-only alias"]
        victim["material_status"] = {
            **victim["material_status"],
            "status": "open",
            "basis": victim["material_status"]["basis"] + " Metadata-only status event.",
        }

        with self.assertRaisesRegex(
            generator.CatalogError,
            "manifest.*differs|effective.*forbidden|override",
        ):
            generator.build_artifacts(effective, self.inputs)

        # The private helper keeps deep allocator invariants testable without
        # reopening the public manifest/inventory override channel.
        rendered = generator._build_artifacts_from_loaded(effective, self.inputs)
        rebuilt = {
            Path(path).name: json.loads(payload)
            for path, payload in rendered.items()
            if Path(path).suffix == ".json"
        }
        rebuilt_source_by_key = {
            row["curation_key"]: row
            for row in rebuilt["Source_Records_v4.json"]["records"]
            if row.get("curation_key")
        }
        for prior_key, prior_row in prior_source_by_key.items():
            self.assertEqual(
                rebuilt_source_by_key[prior_key],
                prior_row,
                f"nonsemantic regeneration rewrote ATO birth row {prior_key}",
            )

        rebuilt_variant = next(
            row
            for row in rebuilt["Claim_ID_Registry_v4.json"]["variants"]
            if row.get("curation_key") == key
        )
        rebuilt_catalog = next(
            row
            for row in rebuilt["Claim_Catalog_v4.json"]["records"]
            if row.get("curation_key") == key
        )
        self.assertEqual(
            rebuilt_variant["variant_id"], prior_variant_by_key[key]["variant_id"]
        )
        self.assertEqual(
            rebuilt_catalog["source_occurrence_id"],
            prior_source_by_key[key]["occurrence_id"],
        )
        self.assertEqual(rebuilt_catalog["preferred_label"], new_label)
        self.assertIn("metadata-only alias", rebuilt_catalog["aliases"])
        self.assertEqual(rebuilt_catalog["material_status"]["status"], "open")

    def test_prior_v4_coordinated_blum_lifecycle_erasure_is_rejected(self) -> None:
        """Four re-sealed views plus a manifest cannot erase a prior redirect."""

        inputs = copy.deepcopy(self.inputs)
        previous = inputs["previous_v4"]
        source_name = "Source_Records_v4.json"
        registry_name = "Claim_ID_Registry_v4.json"
        candidate_name = "Candidate_Dispositions_v4.json"
        migration_name = "Claim_ID_Migration_v2_to_v4.json"
        blum_key = "cs.blum_speedup.exact_v1"
        candidate_key = "missing.cs.blum_speedup"
        source_variant = "ATV-00003390"

        registry = previous[registry_name]
        redirect = next(
            row
            for row in registry["redirects"]
            if row.get("curation_key") == blum_key
        )
        self.assertEqual(redirect["source_variant_id"], source_variant)
        registry["redirects"].remove(redirect)
        previous[registry_name] = independently_recount_and_reseal(registry)

        candidates = previous[candidate_name]
        candidate = next(
            row
            for row in candidates["dispositions"]
            if row.get("candidate_key") == candidate_key
        )
        candidates["dispositions"].remove(candidate)
        previous[candidate_name] = independently_recount_and_reseal(candidates)

        migration = previous[migration_name]
        migration_row = next(
            row for row in migration["migrations"] if row["variant_id"] == source_variant
        )
        self.assertEqual(migration_row["current_resolution"]["kind"], "redirect")
        previous[migration_name] = independently_recount_and_reseal(migration)
        previous[source_name] = independently_reseal(previous[source_name])

        for name in (source_name, registry_name, candidate_name, migration_name):
            generator.validate_document(name, previous[name])

        effective = generator.validate_manifest(self.manifest, self.inputs)
        addition = next(
            row for row in effective["additions"] if row["curation_key"] == blum_key
        )
        self.assertEqual(addition["lineage"][0]["relation_type"], "supersedes")
        addition["lineage"] = []

        with self.assertRaises(generator.CatalogError) as caught:
            generator._build_artifacts_from_loaded(effective, inputs)
        message = str(caught.exception)
        self.assertRegex(message, "prior|lifecycle|migration|redirect")
        self.assertNotRegex(message, "authority digest|counts differ|input digest is stale")

    def test_prior_v4_sealed_lifecycle_anchor_rejects_mutation_and_deletion(self) -> None:
        name = "Claim_ID_Registry_v4.json"
        anchored_ids = set(generator.SEALED_LIFECYCLE_ROW_SHA256)
        self.assertEqual(len(anchored_ids), 12)

        for mutation in ("field_change", "delete"):
            with self.subTest(mutation=mutation):
                inputs = copy.deepcopy(self.inputs)
                registry = inputs["previous_v4"][name]
                rows = [*registry["redirects"], *registry["splits"]]
                victim = next(
                    row
                    for row in rows
                    if row.get("redirect_id", row.get("split_id")) in anchored_ids
                )
                lifecycle_id = victim.get("redirect_id", victim.get("split_id"))
                if mutation == "field_change":
                    self.assertEqual(victim["lifecycle"], "active")
                    victim["lifecycle"] = "retired"
                else:
                    collection = (
                        registry["redirects"]
                        if "redirect_id" in victim
                        else registry["splits"]
                    )
                    collection.remove(victim)
                registry = independently_recount_and_reseal(registry)
                generator.validate_document(name, registry)
                inputs["previous_v4"][name] = registry

                with self.assertRaisesRegex(
                    generator.CatalogError,
                    rf"sealed lifecycle|{re.escape(str(lifecycle_id))}|removes|mutates",
                ):
                    generator._build_artifacts_from_loaded(
                        inputs["manifest"], inputs
                    )

    def test_prior_v4_resealed_migration_cannot_drop_an_input_inventory_entry(self) -> None:
        inputs = copy.deepcopy(self.inputs)
        name = "Claim_ID_Migration_v2_to_v4.json"
        migration = inputs["previous_v4"][name]
        self.assertGreater(len(migration["authoritative_inputs"]), 1)
        migration["authoritative_inputs"].pop()
        migration = independently_recount_and_reseal(migration)
        generator.validate_document(name, migration)
        inputs["previous_v4"][name] = migration

        with self.assertRaises(generator.CatalogError) as caught:
            generator._build_artifacts_from_loaded(inputs["manifest"], inputs)
        message = str(caught.exception)
        self.assertRegex(message, "prior|input|inventory|snapshot")
        self.assertNotRegex(message, "authority digest|counts differ|input digest is stale")

    def test_prior_v4_registry_and_migration_lifecycle_views_are_bidirectional(self) -> None:
        name = "Claim_ID_Migration_v2_to_v4.json"

        reverse_orphan_inputs = copy.deepcopy(self.inputs)
        reverse_orphan = reverse_orphan_inputs["previous_v4"][name]
        active_source = "ATV-00000001"
        redirect_target = "ATV-00003482"
        prior_registry = reverse_orphan_inputs["previous_v4"][
            "Claim_ID_Registry_v4.json"
        ]
        lifecycle_sources = {
            row["source_variant_id"] for row in prior_registry["redirects"]
        } | {row["source_variant_id"] for row in prior_registry["splits"]}
        self.assertNotIn(active_source, lifecycle_sources)
        orphan_row = next(
            row
            for row in reverse_orphan["migrations"]
            if row["variant_id"] == active_source
        )
        orphan_row["current_resolution"] = {
            "kind": "redirect",
            "target_stage_claim_ids": [redirect_target.replace("ATV-", "S4-CLM-")],
            "default_child": None,
            "evidence_inherited": False,
        }
        reverse_orphan = independently_recount_and_reseal(reverse_orphan)
        generator.validate_document(name, reverse_orphan)
        reverse_orphan_inputs["previous_v4"][name] = reverse_orphan

        with self.subTest(direction="migration_without_registry_edge"):
            with self.assertRaises(generator.CatalogError) as caught:
                generator._build_artifacts_from_loaded(
                    reverse_orphan_inputs["manifest"], reverse_orphan_inputs
                )
            self.assertRegex(str(caught.exception), "migration|lifecycle|orphan|registry")
            self.assertNotRegex(
                str(caught.exception),
                "authority digest|counts differ|input digest is stale",
            )

        omitted_inputs = copy.deepcopy(self.inputs)
        omitted = omitted_inputs["previous_v4"][name]
        redirect_source = "ATV-00003390"
        self.assertTrue(
            any(
                row["source_variant_id"] == redirect_source
                for row in omitted_inputs["previous_v4"][
                    "Claim_ID_Registry_v4.json"
                ]["redirects"]
            )
        )
        omitted["migrations"] = [
            row for row in omitted["migrations"] if row["variant_id"] != redirect_source
        ]
        omitted = independently_recount_and_reseal(omitted)
        generator.validate_document(name, omitted)
        omitted_inputs["previous_v4"][name] = omitted

        with self.subTest(direction="registry_edge_without_migration"):
            with self.assertRaises(generator.CatalogError) as caught:
                generator._build_artifacts_from_loaded(
                    omitted_inputs["manifest"], omitted_inputs
                )
            self.assertRegex(str(caught.exception), "migration|lifecycle|absent|registry")
            self.assertNotRegex(
                str(caught.exception),
                "authority digest|counts differ|input digest is stale",
            )

    def test_prior_v4_candidate_history_rejects_duplicate_drop_and_terminal_drift(self) -> None:
        name = "Candidate_Dispositions_v4.json"
        blum_candidate = "missing.cs.blum_speedup"

        def candidate_inputs(mutation: str) -> dict:
            inputs = copy.deepcopy(self.inputs)
            document = inputs["previous_v4"][name]
            rows = document["dispositions"]
            victim = next(
                row for row in rows if row["candidate_key"] == blum_candidate
            )
            if mutation == "duplicate":
                rows.append(copy.deepcopy(victim))
            elif mutation == "drop":
                rows.remove(victim)
            elif mutation == "target_drift":
                # Preserve a self-consistent terminal view while deleting the
                # historical broad allocation from the candidate target set.
                victim["target_atv_ids"] = ["ATV-00003482"]
                victim["target_stage_ids"] = ["S4-CLM-00003482"]
            elif mutation == "terminal_drift":
                victim["terminal_atv_ids"] = ["ATV-00003390"]
                victim["terminal_stage_ids"] = ["S4-CLM-00003390"]
                victim["terminal_children"] = [
                    {
                        "curation_key": "cs.blum_speedup",
                        "variant_id": "ATV-00003390",
                        "stage_claim_id": "S4-CLM-00003390",
                        "lifecycle": "active",
                    }
                ]
            else:
                raise AssertionError(mutation)
            document = independently_recount_and_reseal(document)
            generator.validate_document(name, document)
            inputs["previous_v4"][name] = document
            return inputs

        for mutation in ("duplicate", "drop", "target_drift", "terminal_drift"):
            with self.subTest(mutation=mutation):
                mutated_inputs = candidate_inputs(mutation)
                with self.assertRaises(generator.CatalogError) as caught:
                    generator._build_artifacts_from_loaded(
                        mutated_inputs["manifest"], mutated_inputs
                    )
                self.assertRegex(
                    str(caught.exception),
                    "candidate|lifecycle|duplicate|removed|terminal",
                )
                self.assertNotRegex(
                    str(caught.exception),
                    "authority digest|counts differ|input digest is stale",
                )

    def test_prior_v4_redirect_cannot_be_removed_from_effective_manifest(self) -> None:
        effective = generator.validate_manifest(self.manifest, self.inputs)
        victim = next(
            row
            for row in effective["additions"]
            if any(
                relation.get("relation_type") == "supersedes"
                for relation in row["lineage"]
            )
        )
        victim["lineage"] = []
        with self.assertRaisesRegex(
            generator.CatalogError,
            "prior.*redirect|redirect.*removed|lifecycle.*redirect",
        ):
            generator._build_artifacts_from_loaded(effective, self.inputs)

    def test_prior_v4_redirect_cannot_be_rebound_to_another_source(self) -> None:
        effective = generator.validate_manifest(self.manifest, self.inputs)
        prior_registry = self.inputs["previous_v4"]["Claim_ID_Registry_v4.json"]
        prior_redirect_sources = {
            row["source_variant_id"] for row in prior_registry["redirects"]
        }
        victim = next(
            row
            for row in effective["additions"]
            if any(
                relation.get("relation_type") == "supersedes"
                for relation in row["lineage"]
            )
        )
        replacement_source = next(
            row["variant_id"]
            for row in prior_registry["variants"]
            if row.get("curation_key")
            and row["curation_key"] != victim["curation_key"]
            and row["variant_id"] not in prior_redirect_sources
        )
        victim["lineage"][0]["target_atv_id"] = replacement_source
        with self.assertRaisesRegex(
            generator.CatalogError,
            "prior.*redirect|redirect.*rebound|lifecycle.*redirect",
        ):
            generator._build_artifacts_from_loaded(effective, self.inputs)

    def test_prior_v4_split_cannot_be_removed_from_effective_manifest(self) -> None:
        effective = generator.validate_manifest(self.manifest, self.inputs)
        disposition = next(
            row
            for row in effective["dispositions"]
            if row["candidate_key"] == "regression.cs.owf_converse"
        )
        disposition["resolution_action"] = "retain_children_as_lineage_only"
        overlay = next(
            row
            for row in effective["overlays"]
            if row.get("target_atv_id") == "ATV-00003109"
            and row.get("child_keys")
            == ["cs.owf_implies_p_ne_np", "cs.p_ne_np_implies_owf"]
        )
        overlay["child_keys"] = []
        overlay["change_class"] = "lineage_instruction"
        with self.assertRaisesRegex(
            generator.CatalogError,
            "prior.*split|split.*removed|lifecycle.*split",
        ):
            generator._build_artifacts_from_loaded(effective, self.inputs)

    def test_prior_v4_split_cannot_be_rebound_to_another_source(self) -> None:
        effective = generator.validate_manifest(self.manifest, self.inputs)
        old_source = "ATV-00003109"
        new_source = "ATV-00003110"
        disposition = next(
            row
            for row in effective["dispositions"]
            if row["candidate_key"] == "regression.cs.owf_converse"
        )
        self.assertEqual(disposition["existing_atv_ids"], [old_source])
        disposition["existing_atv_ids"] = [new_source]
        overlay = next(
            row
            for row in effective["overlays"]
            if row.get("target_atv_id") == old_source
            and row.get("child_keys")
            == ["cs.owf_implies_p_ne_np", "cs.p_ne_np_implies_owf"]
        )
        overlay["target_atv_id"] = new_source
        overlay["legacy_id"] = "THM-C-0172"
        for child_key in overlay["child_keys"]:
            child = next(
                row
                for row in effective["additions"]
                if row["curation_key"] == child_key
            )
            self.assertEqual(child["lineage"][0]["target_atv_id"], old_source)
            child["lineage"][0]["target_atv_id"] = new_source
        with self.assertRaisesRegex(
            generator.CatalogError,
            "prior.*split|split.*rebound|lifecycle.*split|prior candidate.*target ATV history drifted",
        ):
            generator._build_artifacts_from_loaded(effective, self.inputs)

    def test_independent_checker_rejects_manifest_fragment_parent_traversal(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["fragments"][-1] = (
            "Docs/catalog/v4/fragments/../fragments/Regression_Fixtures_v4.json"
        )
        checker = catalog_checker.Checker(ROOT, require_complete=True)
        catalog_checker.load_v4_fragments(checker, manifest)
        self.assertTrue(
            any("unsafe path" in error for error in checker.errors),
            checker.errors,
        )

    def test_sealed_manifest_without_both_allocator_files_fails_closed(self) -> None:
        self.assertEqual(self.manifest["policy"]["release_state"], "sealed")
        with tempfile.TemporaryDirectory() as temporary:
            missing_root = Path(temporary)
            with mock.patch.object(
                generator,
                "SOURCE_RECORDS_V4_PATH",
                missing_root / "missing-source.json",
            ), mock.patch.object(
                generator,
                "REGISTRY_V4_PATH",
                missing_root / "missing-registry.json",
            ):
                with self.assertRaisesRegex(
                    generator.CatalogError,
                    "sealed Stage4 manifest has no allocator state",
                ):
                    generator.load_inputs()

    def test_p_vs_np_existing_atv_gains_computer_science_membership_only(self) -> None:
        catalog_rows = self.payload("Claim_Catalog_v4.json")["records"]
        p_vs_np = next(
            row for row in catalog_rows if row["variant_id"] == "ATV-00000746"
        )
        self.assertEqual(
            p_vs_np["membership_domains"],
            ["computer_science", "mathematics"],
        )
        self.assertEqual(p_vs_np["owner_domain"], "mathematics")
        self.assertIn(
            "cs.p_vs_np_computer_science_membership", p_vs_np["overlay_keys"]
        )
        self.assertIn("missing.cs.p_vs_np_occurrence", p_vs_np["candidate_keys"])
        self.assertIn("src.cs.clay_pnp", p_vs_np["source_refs"])

        disposition = next(
            row
            for row in self.payload("Candidate_Dispositions_v4.json")["dispositions"]
            if row["candidate_key"] == "missing.cs.p_vs_np_occurrence"
        )
        self.assertEqual(disposition["existing_atv_ids"], ["ATV-00000746"])
        self.assertEqual(disposition["allocated_atv_ids"], [])
        self.assertEqual(disposition["target_atv_ids"], ["ATV-00000746"])
        self.assertFalse(
            any(
                row.get("curation_key") == "cs.p_vs_np_computer_science_membership"
                for row in self.payload("Source_Records_v4.json")["records"]
            )
        )

    def test_crypto_generic_rows_redirect_to_five_precise_current_profiles(self) -> None:
        profile_to_old = {
            "cs.cdh_assumption.profile_v1": (
                "cs.cdh_assumption",
                "ATV-00003392",
            ),
            "cs.ddh_assumption.profile_v1": (
                "cs.ddh_assumption",
                "ATV-00003398",
            ),
            "cs.search_lwe_assumption.profile_v1": (
                "cs.search_lwe_assumption",
                "ATV-00003415",
            ),
            "cs.decision_lwe_assumption.profile_v1": (
                "cs.decision_lwe_assumption",
                "ATV-00003399",
            ),
            "cs.sis_assumption.profile_v1": (
                "cs.sis_assumption",
                "ATV-00003417",
            ),
        }
        catalog_by_key = {
            row["curation_key"]: row
            for row in self.payload("Claim_Catalog_v4.json")["records"]
            if row.get("curation_key")
        }
        redirect_by_source = {
            row["source_variant_id"]: row
            for row in self.payload("Claim_ID_Registry_v4.json")["redirects"]
        }
        migration_by_variant = {
            row["variant_id"]: row
            for row in self.payload("Claim_ID_Migration_v2_to_v4.json")["migrations"]
        }
        open_ids = set(
            projection_ids(self.document("Conjecture_Hypothesis_Open_List_v4.json"))
        )
        expected_old_ids = {old_id for _old_key, old_id in profile_to_old.values()}
        crypto_redirects = {
            source_id: row
            for source_id, row in redirect_by_source.items()
            if row.get("curation_key") in profile_to_old
            and row.get("relation_type") == "supersedes"
        }
        self.assertEqual(set(crypto_redirects), expected_old_ids)

        target_ids: set[str] = set()
        for profile_key, (old_key, old_id) in profile_to_old.items():
            with self.subTest(profile=profile_key):
                old = catalog_by_key[old_key]
                profile = catalog_by_key[profile_key]
                self.assertEqual(old["variant_id"], old_id)
                self.assertEqual(old["lifecycle"], "redirected")
                self.assertEqual(
                    old["lifecycle_target_stage_ids"],
                    [profile["stage_claim_id"]],
                )
                self.assertEqual(old["redirected_by_curation_key"], profile_key)
                self.assertNotIn(old["stage_claim_id"], open_ids)

                self.assertEqual(profile["lifecycle"], "active")
                self.assertEqual(profile["record_role"], "claim")
                self.assertEqual(profile["atomicity"], "atomic")
                self.assertIs(profile["truth_apt"], True)
                self.assertEqual(profile["material_status"]["status"], "open")
                self.assertIn(profile["stage_claim_id"], open_ids)
                target_ids.add(profile["variant_id"])

                redirect = crypto_redirects[old_id]
                self.assertEqual(redirect["target_variant_id"], profile["variant_id"])
                self.assertEqual(redirect["curation_key"], profile_key)
                self.assertEqual(redirect["relation_type"], "supersedes")
                self.assertIsNone(redirect["default_child"])
                self.assertIs(redirect["evidence_inherited"], False)
                self.assertEqual(
                    migration_by_variant[old_id]["current_resolution"],
                    {
                        "kind": "redirect",
                        "target_stage_claim_ids": [profile["stage_claim_id"]],
                        "default_child": None,
                        "evidence_inherited": False,
                    },
                )
                self.assertEqual(
                    migration_by_variant[profile["variant_id"]]["current_resolution"][
                        "kind"
                    ],
                    "current",
                )
        self.assertEqual(len(target_ids), 5)
        self.assertTrue(expected_old_ids.isdisjoint(target_ids))

    def test_blum_busy_beaver_and_rao_exact_rows_supersede_broad_rows(self) -> None:
        exact_to_broad = {
            "cs.blum_speedup.exact_v1": (
                "cs.blum_speedup",
                "ATV-00003390",
            ),
            "cs.busy_beaver_step_domination.exact_v1": (
                "cs.busy_beaver_domination",
                "ATV-00003391",
            ),
            "math.statistics.rao_blackwell_rd_convex_loss.exact_v1": (
                "math.statistics.rao_blackwell_convex_loss",
                "ATV-00003468",
            ),
        }
        catalog_by_key = {
            row["curation_key"]: row
            for row in self.payload("Claim_Catalog_v4.json")["records"]
            if row.get("curation_key")
        }
        redirect_by_key = {
            row["curation_key"]: row
            for row in self.payload("Claim_ID_Registry_v4.json")["redirects"]
            if row.get("relation_type") == "supersedes"
        }
        migration_by_variant = {
            row["variant_id"]: row
            for row in self.payload("Claim_ID_Migration_v2_to_v4.json")["migrations"]
        }
        theorem_ids = set(projection_ids(self.document("Theorem_List_v4.json")))

        for exact_key, (broad_key, broad_id) in exact_to_broad.items():
            with self.subTest(exact=exact_key):
                broad = catalog_by_key[broad_key]
                exact = catalog_by_key[exact_key]
                self.assertEqual(broad["variant_id"], broad_id)
                self.assertEqual(broad["lifecycle"], "redirected")
                self.assertEqual(
                    broad["lifecycle_target_stage_ids"],
                    [exact["stage_claim_id"]],
                )
                self.assertEqual(broad["redirected_by_curation_key"], exact_key)
                self.assertNotIn(broad["stage_claim_id"], theorem_ids)

                self.assertEqual(exact["lifecycle"], "active")
                self.assertEqual(exact["record_role"], "claim")
                self.assertEqual(exact["atomicity"], "atomic")
                self.assertIs(exact["truth_apt"], True)
                self.assertEqual(exact["material_status"]["status"], "proved")
                self.assertIn(exact["stage_claim_id"], theorem_ids)

                redirect = redirect_by_key[exact_key]
                self.assertEqual(redirect["source_variant_id"], broad_id)
                self.assertEqual(redirect["target_variant_id"], exact["variant_id"])
                self.assertIsNone(redirect["default_child"])
                self.assertIs(redirect["evidence_inherited"], False)
                self.assertEqual(
                    migration_by_variant[broad_id]["current_resolution"],
                    {
                        "kind": "redirect",
                        "target_stage_claim_ids": [exact["stage_claim_id"]],
                        "default_child": None,
                        "evidence_inherited": False,
                    },
                )
                self.assertEqual(
                    migration_by_variant[exact["variant_id"]]["current_resolution"][
                        "kind"
                    ],
                    "current",
                )

    def test_non_truth_apt_unknown_row_cannot_be_promoted_to_current_proved(self) -> None:
        documents, catalog = self.mutable_artifact("Claim_Catalog_v4.json")
        victim = next(
            row
            for row in catalog["records"]
            if row.get("truth_apt") == "unknown"
            and row.get("record_role") == "unreviewed_source_variant"
        )
        proved = {
            "status": "proved",
            "as_of": self.manifest["review_date"],
            "basis": "Synthetic mutation must never grant truth credit.",
            "source_refs": [],
        }
        victim["material_status"] = proved
        victim["status_events"] = [copy.deepcopy(proved)]
        resealed = dict(documents)
        resealed["Claim_Catalog_v4.json"] = generator.seal_document(
            "Claim_Catalog_v4.json", documents["Claim_Catalog_v4.json"]
        )
        generator.validate_document(
            "Claim_Catalog_v4.json", resealed["Claim_Catalog_v4.json"]
        )
        with self.assertRaisesRegex(
            generator.CatalogError, "non-atomic/non-truth-apt"
        ):
            generator.validate_artifacts(resealed, self.manifest, self.inputs)


if __name__ == "__main__":
    unittest.main()
