#!/usr/bin/env python3
"""Black-box contract and mutation tests for Stage5 release 5.3.

This module intentionally imports no catalog generator, extractor, curation
builder, or checker implementation.  The independent v5.3 checker is invoked
only as a subprocess.  Mutations live below a temporary repository root; the
test mirror uses hard links for speed and always unlinks a target before a
write, so the canonical catalog is never modified.
"""

from __future__ import annotations

import ast
from collections import Counter
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Callable, Iterable, Mapping, Sequence
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts/check_math_catalog_v5_3.py"
CATALOG_REL = Path("Docs/catalog/v5")
SOURCE_REL = CATALOG_REL / "sources/mathlib-theorems-8a178386.json"
CURATION_REL = CATALOG_REL / "curation/Mathlib_Theorem_Curation_v5_3.json"
RELEASE_REL = CATALOG_REL / "releases/5.3"
PARENT_REL = CATALOG_REL / "releases/5.2"
CURRENT_REL = CATALOG_REL / "Current_Release.json"

RELEASE_FILES = (
    "Claim_Catalog.json",
    "Claim_ID_Registry.json",
    "Stage5_Claim_ID_Registry.json",
    "Migration_v4_to_v5.json",
    "Theorem_List.json",
    "Open_Claim_List.json",
    "Coverage_Ledger.json",
    "Strict_Conjecture_Ledger.json",
)
MANIFEST_NAME = "Release_Manifest.json"
MATHLIB_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
SOURCE_SHA256 = "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a"
SOURCE_SIZE_BYTES = 6_316_287
SOURCE_ID = "SRC-MATH-V5-MATHLIB-8A178386"
DOCS_SIGNAL = "mathlib_1000_theorems"
MODULE_MAIN_SIGNAL = "mathlib_module_main_result"
FIRST_NEW_ORDINAL = 6_585
LAST_NEW_ORDINAL = 7_084
COMMIT_URL_RE = re.compile(
    rf"^https://github\.com/leanprover-community/mathlib4/blob/"
    rf"{MATHLIB_COMMIT}/Mathlib/.+\.lean#L[0-9]+-L[0-9]+$"
)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def encoded_document(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return sha256_bytes(
        canonical_json_bytes(
            {key: item for key, item in value.items() if key not in omitted}
        )
    )


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical_json_bytes(sorted(values)))


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected a JSON object: {path}")
    return value


def seal_document(value: dict[str, Any]) -> dict[str, Any]:
    value["authority_sha256"] = hash_without(value, "authority_sha256")
    return value


def write_document(path: Path, value: Mapping[str, Any]) -> None:
    path.write_bytes(encoded_document(value))


def release_root(inventory: Iterable[Mapping[str, Any]]) -> str:
    payload = sorted(
        (
            {
                "path": str(row["path"]),
                "sha256": str(row["sha256"]),
                "size_bytes": int(row["size_bytes"]),
            }
            for row in inventory
        ),
        key=lambda row: row["path"],
    )
    return sha256_bytes(canonical_json_bytes(payload))


def mirror_catalog_tree(destination_root: Path) -> None:
    source = ROOT / "Docs/catalog"
    destination = destination_root / "Docs/catalog"
    for item in sorted(source.rglob("*")):
        target = destination / item.relative_to(source)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(item, target)


def materialize(root: Path, relative: Path) -> Path:
    """Break one hard link before returning a private writable copy."""

    target = root / relative
    source = ROOT / relative
    if target.is_symlink() or target.exists():
        target.unlink()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target


def primary_row_count(name: str, document: Mapping[str, Any]) -> int:
    if name == "Claim_Catalog.json":
        return len(document["records"])
    if name == "Claim_ID_Registry.json":
        return len(document["variants"])
    if name == "Stage5_Claim_ID_Registry.json":
        return len(document["mappings"])
    if name == "Migration_v4_to_v5.json":
        for key in ("migrations", "records", "rows"):
            if isinstance(document.get(key), list):
                return len(document[key])
    if name in {"Theorem_List.json", "Open_Claim_List.json"}:
        return len(document["records"])
    if name == "Coverage_Ledger.json":
        return len(document["candidate_dispositions"]) + len(
            document["msc_coverage"]
        )
    if name == "Strict_Conjecture_Ledger.json":
        return len(document["strict_credits"]) + len(
            document["credit_corrections"]
        )
    raise AssertionError(f"unknown release artifact: {name}")


def reseal_artifact(root: Path, name: str, document: dict[str, Any]) -> None:
    path = materialize(root, RELEASE_REL / name)
    seal_document(document)
    write_document(path, document)


def update_current_for_manifest(root: Path, manifest: Mapping[str, Any]) -> None:
    manifest_path = root / RELEASE_REL / MANIFEST_NAME
    current_path = materialize(root, CURRENT_REL)
    current = load_json(current_path)
    current["release"] = "5.3"
    current["manifest_path"] = f"releases/5.3/{MANIFEST_NAME}"
    current["release_root_sha256"] = manifest["release_root_sha256"]
    current["manifest_sha256"] = sha256_file(manifest_path)
    seal_document(current)
    write_document(current_path, current)


def rebind_manifest_and_current(root: Path, changed_names: Iterable[str]) -> None:
    changed = set(changed_names)
    release_dir = root / RELEASE_REL
    manifest_path = materialize(root, RELEASE_REL / MANIFEST_NAME)
    manifest = load_json(manifest_path)
    by_name = {row["path"]: row for row in manifest["artifacts"]}
    if set(by_name) != set(RELEASE_FILES):
        raise AssertionError("unexpected v5.3 manifest inventory")
    for name in changed:
        artifact_path = release_dir / name
        document = load_json(artifact_path)
        entry = by_name[name]
        entry["sha256"] = sha256_file(artifact_path)
        entry["size_bytes"] = artifact_path.stat().st_size
        entry["row_count"] = primary_row_count(name, document)
    if "Strict_Conjecture_Ledger.json" in changed:
        strict_path = release_dir / "Strict_Conjecture_Ledger.json"
        strict = load_json(strict_path)
        binding = manifest["strict_credit_binding"]
        binding["file_sha256"] = sha256_file(strict_path)
        binding["authority_sha256"] = strict["authority_sha256"]
        binding["effective_s5_id_set_sha256"] = strict["set_digests"][
            "effective_s5_id_set_sha256"
        ]
        binding["effective_variant_id_set_sha256"] = strict["set_digests"][
            "effective_variant_id_set_sha256"
        ]
        manifest["counts"]["effective_strict_conjecture_credits"] = strict[
            "counts"
        ]["effective_strict_credits"]
    manifest["release_root_sha256"] = release_root(manifest["artifacts"])
    seal_document(manifest)
    write_document(manifest_path, manifest)
    update_current_for_manifest(root, manifest)


def find_input_binding(
    manifest: Mapping[str, Any], relative_path: Path
) -> dict[str, Any]:
    matches = [
        row
        for row in manifest["authoritative_inputs"].values()
        if isinstance(row, dict) and row.get("path") == relative_path.as_posix()
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"manifest has {len(matches)} bindings for {relative_path.as_posix()}"
        )
    return matches[0]


def rebind_curation_manifest_and_current(
    root: Path, curation: dict[str, Any]
) -> None:
    curation_path = materialize(root, CURATION_REL)
    seal_document(curation)
    write_document(curation_path, curation)

    manifest_path = materialize(root, RELEASE_REL / MANIFEST_NAME)
    manifest = load_json(manifest_path)
    binding = find_input_binding(manifest, CURATION_REL)
    binding["file_sha256"] = sha256_file(curation_path)
    binding["size_bytes"] = curation_path.stat().st_size
    binding["authority_sha256"] = curation["authority_sha256"]

    accepted = [
        row
        for row in curation["candidate_dispositions"]
        if row["disposition"] == "accepted_new_kernel_checked_theorem"
    ]
    digest_sources = {
        "source_record_id_set_sha256": set_digest(
            str(row["source_record_id"]) for row in accepted
        ),
        "declaration_set_sha256": set_digest(
            str(row["declaration"]) for row in accepted
        ),
        "formal_type_sha256_set_sha256": set_digest(
            str(row["formal_type_sha256"]) for row in accepted
        ),
        "semantic_key_set_sha256": set_digest(
            str(row["semantic_key"]) for row in accepted
        ),
        "variant_id_set_sha256": set_digest(
            str(row["target_variant_id"]) for row in accepted
        ),
        "s5_id_set_sha256": set_digest(
            str(row["target_s5_id"]) for row in accepted
        ),
    }
    accepted_binding = manifest.get("accepted_set_digests")
    if isinstance(accepted_binding, dict):
        for key, value in digest_sources.items():
            if key in accepted_binding:
                accepted_binding[key] = value
    seal_document(manifest)
    write_document(manifest_path, manifest)
    update_current_for_manifest(root, manifest)


def run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER_PATH), "--root", str(root)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=300,
    )


def signal_kinds(source_row: Mapping[str, Any]) -> set[str]:
    return {
        str(signal["kind"])
        for signal in source_row["importance_signals"]
        if isinstance(signal, dict) and isinstance(signal.get("kind"), str)
    }


def module_root(source_row: Mapping[str, Any]) -> str:
    pieces = str(source_row["source"]["module"]).split(".")
    if len(pieces) < 2 or pieces[0] != "Mathlib" or not pieces[1]:
        raise AssertionError(f"invalid Mathlib module: {pieces!r}")
    return pieces[1]


def importance_tier(source_row: Mapping[str, Any]) -> str:
    kinds = signal_kinds(source_row)
    if kinds == {DOCS_SIGNAL, MODULE_MAIN_SIGNAL}:
        return "docs_1000_and_module_main"
    if DOCS_SIGNAL in kinds:
        return "docs_1000"
    if MODULE_MAIN_SIGNAL in kinds:
        return "module_main_result"
    raise AssertionError(f"source row has no recognized importance signal: {source_row}")


def rebuild_selection(
    source_rows: Sequence[dict[str, Any]],
) -> tuple[list[dict[str, Any]], set[str], dict[str, str]]:
    """Independently replay the exact-formal-type and two-phase selection."""

    literal = [
        row
        for row in source_rows
        if row["declaration_kind"] == "theorem"
        and row["source_syntax_kind"] == "theorem"
    ]
    by_formal_type: dict[str, list[dict[str, Any]]] = {}
    for row in literal:
        by_formal_type.setdefault(str(row["formal_type_sha256"]), []).append(row)
    winners: list[dict[str, Any]] = []
    duplicate_losers: dict[str, str] = {}
    for group in by_formal_type.values():
        ordered = sorted(
            group,
            key=lambda row: (
                -int(DOCS_SIGNAL in signal_kinds(row)),
                int(row["selection_rank"]),
                str(row["source_record_id"]),
            ),
        )
        winners.append(ordered[0])
        for loser in ordered[1:]:
            duplicate_losers[str(loser["source_record_id"])] = str(
                ordered[0]["source_record_id"]
            )
    phase_one = sorted(
        (row for row in winners if DOCS_SIGNAL in signal_kinds(row)),
        key=lambda row: (
            int(row["selection_rank"]),
            str(row["source_record_id"]),
        ),
    )
    phase_one_ids = {str(row["source_record_id"]) for row in phase_one}
    buckets: dict[str, list[dict[str, Any]]] = {}
    for row in winners:
        if str(row["source_record_id"]) in phase_one_ids:
            continue
        if MODULE_MAIN_SIGNAL not in signal_kinds(row):
            continue
        buckets.setdefault(module_root(row), []).append(row)
    for bucket in buckets.values():
        bucket.sort(
            key=lambda row: (
                int(row["selection_rank"]),
                str(row["source_record_id"]),
            )
        )
    offsets = {root: 0 for root in buckets}
    phase_two: list[dict[str, Any]] = []
    roots = sorted(buckets)
    while len(phase_two) < 320:
        advanced = False
        for root in roots:
            offset = offsets[root]
            if offset >= len(buckets[root]):
                continue
            phase_two.append(buckets[root][offset])
            offsets[root] += 1
            advanced = True
            if len(phase_two) == 320:
                break
        if not advanced:
            raise AssertionError("balanced selection exhausted before 320 rows")
    return phase_one + phase_two, phase_one_ids, duplicate_losers


def recompute_curation(curation: dict[str, Any], source: Mapping[str, Any]) -> None:
    rows = curation["candidate_dispositions"]
    source_rows = source["records"]
    by_id = {str(row["source_record_id"]): row for row in source_rows}
    accepted = [
        row
        for row in rows
        if row["disposition"] == "accepted_new_kernel_checked_theorem"
    ]
    dispositions = Counter(str(row["disposition"]) for row in rows)
    selected_sources = [by_id[str(row["source_record_id"])] for row in accepted]
    counts = curation["counts"]
    counts.update(
        {
            "source_rows": len(rows),
            "candidate_disposition_rows": len(rows),
            "eligible_literal_theorems": sum(
                row["declaration_kind"] == "theorem" for row in source_rows
            ),
            "pre_eligibility_excluded_lemmas": sum(
                row["declaration_kind"] == "lemma" for row in source_rows
            ),
            "literal_theorems": sum(
                row["declaration_kind"] == "theorem" for row in source_rows
            ),
            "literal_lemmas": sum(
                row["declaration_kind"] == "lemma" for row in source_rows
            ),
            "kernel_checked_sorry_free": sum(
                row["formal_proof_state"] == "kernel_checked_sorry_free"
                for row in source_rows
            ),
            "accepted": len(accepted),
            "nonaccepted_eligible": sum(
                row["declaration_kind"] == "theorem"
                and row["disposition"]
                != "accepted_new_kernel_checked_theorem"
                for row in rows
            ),
            "nonaccepted_total": len(rows) - len(accepted),
            "docs_1000_priority_seed": sum(
                DOCS_SIGNAL in signal_kinds(row) for row in selected_sources
            ),
            "module_main_balanced_fill": sum(
                DOCS_SIGNAL not in signal_kinds(row) for row in selected_sources
            ),
            "source_semantic_duplicate_rows": sum(
                row["disposition"]
                in {
                    "rejected_source_semantic_duplicate",
                    "rejected_source_name_duplicate",
                }
                for row in rows
            ),
            "parent_duplicate_rows": sum(
                row["disposition"] == "rejected_parent_duplicate" for row in rows
            ),
            "selected_branches": len(
                {module_root(row) for row in selected_sources}
            ),
            "selected_with_docs_1000_signal": sum(
                DOCS_SIGNAL in signal_kinds(row) for row in selected_sources
            ),
            "selected_with_module_main_signal": sum(
                MODULE_MAIN_SIGNAL in signal_kinds(row) for row in selected_sources
            ),
            "by_disposition": dict(sorted(dispositions.items())),
            "selected_by_module_root": dict(
                sorted(Counter(module_root(row) for row in selected_sources).items())
            ),
            "selected_by_importance_tier": dict(
                sorted(Counter(importance_tier(row) for row in selected_sources).items())
            ),
        }
    )
    digests = {
        "candidate_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"]) for row in rows
        ),
        "eligible_theorem_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"])
            for row in rows
            if row["declaration_kind"] == "theorem"
        ),
        "excluded_lemma_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"])
            for row in rows
            if row["disposition"] == "rejected_nonliteral_lemma"
        ),
        "nonaccepted_eligible_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"])
            for row in rows
            if row["declaration_kind"] == "theorem"
            and row["disposition"] != "accepted_new_kernel_checked_theorem"
        ),
        "selected_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"]) for row in accepted
        ),
        "selected_declaration_set_sha256": set_digest(
            str(row["declaration"]) for row in accepted
        ),
        "selected_formal_type_sha256_set_sha256": set_digest(
            str(row["formal_type_sha256"]) for row in accepted
        ),
        "selected_semantic_key_set_sha256": set_digest(
            str(row["semantic_key"]) for row in accepted
        ),
        "selected_variant_id_set_sha256": set_digest(
            str(row["target_variant_id"]) for row in accepted
        ),
        "selected_s5_id_set_sha256": set_digest(
            str(row["target_s5_id"]) for row in accepted
        ),
        "candidate_row_sha256_set_sha256": set_digest(
            str(row["row_sha256"]) for row in rows
        ),
    }
    curation["set_digests"] = digests


def make_nonaccepted(row: dict[str, Any]) -> None:
    row["disposition"] = "eligible_not_selected"
    row["reason_code"] = "viable_theorem_outside_exact_500_selection"
    row["accepted_rank"] = None
    row["target_variant_id"] = None
    row["target_s5_id"] = None
    row["canonical_source_record_id"] = None
    row["duplicate_of_semantic_key"] = None
    row["duplicate_of_variant_id"] = None
    row["dedupe_rationale"] = None
    row["dedupe_confidence"] = None
    row["dedupe_reviewer"] = None
    row["grants_catalog_entry"] = False
    row["grants_theorem_credit"] = False
    row["row_sha256"] = hash_without(row, "row_sha256")


def make_accepted(
    row: dict[str, Any], source_row: Mapping[str, Any], allocation: Mapping[str, Any]
) -> None:
    row["disposition"] = "accepted_new_kernel_checked_theorem"
    row["reason_code"] = (
        "selected_docs_1000_priority_seed"
        if DOCS_SIGNAL in signal_kinds(source_row)
        else "selected_module_main_round_robin_fill"
    )
    row["accepted_rank"] = allocation["accepted_rank"]
    row["target_variant_id"] = allocation["target_variant_id"]
    row["target_s5_id"] = allocation["target_s5_id"]
    row["canonical_source_record_id"] = None
    row["duplicate_of_semantic_key"] = None
    row["duplicate_of_variant_id"] = None
    row["dedupe_rationale"] = None
    row["dedupe_confidence"] = None
    row["dedupe_reviewer"] = None
    row["grants_catalog_entry"] = True
    row["grants_theorem_credit"] = True
    row["row_sha256"] = hash_without(row, "row_sha256")


class MathCatalogV53Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        required = (
            CHECKER_PATH,
            ROOT / RELEASE_REL / MANIFEST_NAME,
            ROOT / SOURCE_REL,
            ROOT / CURATION_REL,
        )
        missing = [str(path) for path in required if not path.is_file()]
        if missing:
            raise AssertionError("v5.3 inputs are not published: " + ", ".join(missing))
        cls.source = load_json(ROOT / SOURCE_REL)
        cls.source_rows = cls.source["records"]
        cls.source_by_id = {
            str(row["source_record_id"]): row for row in cls.source_rows
        }
        cls.curation = load_json(ROOT / CURATION_REL)
        cls.parent_catalog = load_json(ROOT / PARENT_REL / "Claim_Catalog.json")
        cls.catalog = load_json(ROOT / RELEASE_REL / "Claim_Catalog.json")
        cls.parent_strict = load_json(
            ROOT / PARENT_REL / "Strict_Conjecture_Ledger.json"
        )
        cls.strict = load_json(
            ROOT / RELEASE_REL / "Strict_Conjecture_Ledger.json"
        )
        cls.parent_open = load_json(ROOT / PARENT_REL / "Open_Claim_List.json")
        cls.open_list = load_json(ROOT / RELEASE_REL / "Open_Claim_List.json")
        cls.manifest = load_json(ROOT / RELEASE_REL / MANIFEST_NAME)
        cls.current = load_json(ROOT / CURRENT_REL)
        cls.new_rows = [
            row
            for row in cls.catalog["records"]
            if row.get("origin_release") == "5.3"
        ]
        cls.expected_selected, cls.docs_seed_ids, cls.duplicate_losers = (
            rebuild_selection(cls.source_rows)
        )

    def assert_checker_rejects(
        self, mutate: Callable[[Path], None], label: str
    ) -> str:
        with tempfile.TemporaryDirectory(prefix="at-v53-test-") as directory:
            temporary_root = Path(directory)
            mirror_catalog_tree(temporary_root)
            mutate(temporary_root)
            result = run_checker(temporary_root)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("Traceback (most recent call last)", result.stdout)
        self.assertIn("FAIL", result.stdout, f"{label}: {result.stdout}")
        return result.stdout

    def test_checker_is_independent_and_passes_canonical_and_mirror(self) -> None:
        tree = ast.parse(CHECKER_PATH.read_text(encoding="utf-8"))
        imported: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        self.assertEqual(
            [
                name
                for name in imported
                if any(token in name.lower() for token in ("generat", "extract", "builder"))
            ],
            [],
        )
        canonical = run_checker(ROOT)
        self.assertEqual(canonical.returncode, 0, canonical.stdout)
        self.assertIn("PASS check_math_catalog_v5_3", canonical.stdout)
        with tempfile.TemporaryDirectory(prefix="at-v53-baseline-") as directory:
            temporary_root = Path(directory)
            mirror_catalog_tree(temporary_root)
            mirrored = run_checker(temporary_root)
        self.assertEqual(mirrored.returncode, 0, mirrored.stdout)
        self.assertIn("PASS check_math_catalog_v5_3", mirrored.stdout)

    def test_exact_500_new_and_cumulative_2000_theorems(self) -> None:
        self.assertEqual(len(self.parent_catalog["records"]), 3_100)
        self.assertEqual(len(self.catalog["records"]), 3_600)
        self.assertEqual(len(self.new_rows), 500)
        self.assertTrue(
            all(
                row["claim_kind"] == "theorem"
                and row["current_claim_kind"] == "theorem"
                and row["category"] == "theorem"
                and row["material_status"] == "proved"
                for row in self.new_rows
            )
        )
        self.assertEqual(
            self.catalog["counts"],
            {
                "records": 3_600,
                "origin_theorems": 500,
                "origin_open_claims": 0,
                "cumulative_theorems": 2_000,
                "cumulative_open_claims": 1_600,
            },
        )
        theorem_projection = load_json(ROOT / RELEASE_REL / "Theorem_List.json")
        self.assertEqual(len(theorem_projection["records"]), 2_000)

        def mutate(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            catalog["records"].pop()
            catalog["counts"]["records"] = 3_599
            catalog["counts"]["origin_theorems"] = 499
            catalog["counts"]["cumulative_theorems"] = 1_999
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(mutate, "499-row theorem mutation")

    def test_literal_lemmas_never_receive_theorem_credit(self) -> None:
        source_lemmas = [
            row
            for row in self.source_rows
            if row["declaration_kind"] == "lemma"
            or row["source_syntax_kind"] == "lemma"
        ]
        self.assertEqual(len(source_lemmas), 265)
        by_id = {
            str(row["source_record_id"]): row
            for row in self.curation["candidate_dispositions"]
        }
        for source_row in source_lemmas:
            row = by_id[str(source_row["source_record_id"])]
            self.assertEqual(row["disposition"], "rejected_nonliteral_lemma")
            self.assertIs(row["grants_catalog_entry"], False)
            self.assertIs(row["grants_theorem_credit"], False)
            self.assertIsNone(row["accepted_rank"])
            self.assertIsNone(row["target_variant_id"])
            self.assertIsNone(row["target_s5_id"])
        self.assertTrue(
            all(row["formal_statement"]["declaration_kind"] == "theorem" for row in self.new_rows)
        )

        def mutate(root: Path) -> None:
            curation = copy.deepcopy(self.curation)
            rows = curation["candidate_dispositions"]
            lemma = next(row for row in rows if row["declaration_kind"] == "lemma")
            accepted = next(
                row
                for row in rows
                if row["disposition"] == "accepted_new_kernel_checked_theorem"
            )
            allocation = {
                key: accepted[key]
                for key in ("accepted_rank", "target_variant_id", "target_s5_id")
            }
            make_nonaccepted(accepted)
            make_accepted(
                lemma,
                self.source_by_id[str(lemma["source_record_id"])],
                allocation,
            )
            recompute_curation(curation, self.source)
            rebind_curation_manifest_and_current(root, curation)

        self.assert_checker_rejects(mutate, "lemma-credit mutation")

    def test_kernel_checked_sorry_free_boundary_and_mutation(self) -> None:
        self.assertTrue(
            all(
                row["proof_evidence"]["formal_proof_state"]
                == "kernel_checked_sorry_free"
                and row["proof_evidence"]["uses_sorry"] is False
                and "sorryAx"
                not in row["proof_evidence"]["batch_axiom_dependency_union"]
                for row in self.new_rows
            )
        )
        self.assertTrue(
            all(
                self.source_by_id[row["theorem_selection"]["source_record_id"]][
                    "formal_proof_state"
                ]
                == "kernel_checked_sorry_free"
                and self.source_by_id[row["theorem_selection"]["source_record_id"]][
                    "proof_evidence"
                ]["uses_sorry"]
                is False
                for row in self.new_rows
            )
        )

        def mutate(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            row = catalog["records"][3_100]
            proof = row["proof_evidence"]
            proof["uses_sorry"] = True
            proof["batch_axiom_dependency_union"].append("sorryAx")
            proof["proof_payload_sha256"] = hash_without(
                proof, "proof_payload_sha256"
            )
            row["proof_payload_sha256"] = proof["proof_payload_sha256"]
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(mutate, "uses_sorry mutation")

    def test_four_source_duplicates_are_excluded_and_recredit_is_rejected(self) -> None:
        literal = [
            row
            for row in self.source_rows
            if row["declaration_kind"] == "theorem"
            and row["source_syntax_kind"] == "theorem"
        ]
        groups = Counter(str(row["formal_type_sha256"]) for row in literal)
        self.assertEqual(sum(count > 1 for count in groups.values()), 3)
        self.assertEqual(sum(count - 1 for count in groups.values()), 4)
        self.assertEqual(len(self.duplicate_losers), 4)
        by_id = {
            str(row["source_record_id"]): row
            for row in self.curation["candidate_dispositions"]
        }
        for loser_id, winner_id in self.duplicate_losers.items():
            row = by_id[loser_id]
            self.assertEqual(row["disposition"], "rejected_source_semantic_duplicate")
            self.assertEqual(row["canonical_source_record_id"], winner_id)
            self.assertIs(row["grants_theorem_credit"], False)
            self.assertIsNone(row["target_variant_id"])

        def mutate(root: Path) -> None:
            curation = copy.deepcopy(self.curation)
            rows = curation["candidate_dispositions"]
            duplicate = next(
                row
                for row in rows
                if row["disposition"] == "rejected_source_semantic_duplicate"
            )
            accepted = next(
                row
                for row in reversed(rows)
                if row["disposition"] == "accepted_new_kernel_checked_theorem"
            )
            allocation = {
                key: accepted[key]
                for key in ("accepted_rank", "target_variant_id", "target_s5_id")
            }
            make_nonaccepted(accepted)
            make_accepted(
                duplicate,
                self.source_by_id[str(duplicate["source_record_id"])],
                allocation,
            )
            recompute_curation(curation, self.source)
            rebind_curation_manifest_and_current(root, curation)

        self.assert_checker_rejects(mutate, "source-duplicate credit mutation")

    def test_docs_seed_180_and_balanced_fill_320_replay_exactly(self) -> None:
        self.assertEqual(len(self.expected_selected), 500)
        self.assertEqual(len(self.docs_seed_ids), 180)
        self.assertEqual(self.curation["counts"]["docs_1000_priority_seed"], 180)
        self.assertEqual(self.curation["counts"]["module_main_balanced_fill"], 320)
        accepted = sorted(
            (
                row
                for row in self.curation["candidate_dispositions"]
                if row["disposition"] == "accepted_new_kernel_checked_theorem"
            ),
            key=lambda row: int(row["accepted_rank"]),
        )
        expected_ids = [str(row["source_record_id"]) for row in self.expected_selected]
        self.assertEqual([row["source_record_id"] for row in accepted], expected_ids)
        self.assertEqual(
            [row["theorem_selection"]["source_record_id"] for row in self.new_rows],
            expected_ids,
        )
        self.assertEqual(
            Counter(row["theorem_selection"]["selection_phase"] for row in self.new_rows),
            Counter(
                {
                    "selected_docs_1000_priority_seed": 180,
                    "selected_module_main_round_robin_fill": 320,
                }
            ),
        )

        def mutate(root: Path) -> None:
            curation = copy.deepcopy(self.curation)
            rows = curation["candidate_dispositions"]
            seed = next(
                row
                for row in rows
                if row["disposition"] == "accepted_new_kernel_checked_theorem"
                and row["reason_code"] == "selected_docs_1000_priority_seed"
            )
            outsider = next(
                row for row in rows if row["disposition"] == "eligible_not_selected"
            )
            allocation = {
                key: seed[key]
                for key in ("accepted_rank", "target_variant_id", "target_s5_id")
            }
            make_nonaccepted(seed)
            make_accepted(
                outsider,
                self.source_by_id[str(outsider["source_record_id"])],
                allocation,
            )
            recompute_curation(curation, self.source)
            rebind_curation_manifest_and_current(root, curation)

        self.assert_checker_rejects(mutate, "two-phase selection mutation")

    def test_parent_prefix_is_exact_and_mutation_is_rejected(self) -> None:
        parent_rows = self.parent_catalog["records"]
        self.assertEqual(self.catalog["records"][:3_100], parent_rows)

        def mutate(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            catalog["records"][0]["display_name"] += " [tampered parent]"
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(mutate, "parent-prefix mutation")

    def test_new_ids_are_exactly_6585_through_7084(self) -> None:
        expected_atv = [
            f"ATV-{ordinal:08d}"
            for ordinal in range(FIRST_NEW_ORDINAL, LAST_NEW_ORDINAL + 1)
        ]
        expected_s5 = [
            f"S5-CLM-{ordinal:08d}"
            for ordinal in range(FIRST_NEW_ORDINAL, LAST_NEW_ORDINAL + 1)
        ]
        self.assertEqual([row["variant_id"] for row in self.new_rows], expected_atv)
        self.assertEqual([row["stage_claim_id"] for row in self.new_rows], expected_s5)
        registry = load_json(ROOT / RELEASE_REL / "Claim_ID_Registry.json")
        stage = load_json(ROOT / RELEASE_REL / "Stage5_Claim_ID_Registry.json")
        self.assertEqual(
            [row["variant_id"] for row in registry["variants"][-500:]], expected_atv
        )
        self.assertEqual(
            [row["stage_claim_id"] for row in stage["mappings"][-500:]], expected_s5
        )

        def mutate(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            catalog["records"][3_100]["variant_id"] = "ATV-99999999"
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(mutate, "new-ID mutation")

    def test_rights_and_commit_locators_are_bound_and_mutations_fail(self) -> None:
        self.assertEqual(sha256_file(ROOT / SOURCE_REL), SOURCE_SHA256)
        self.assertEqual((ROOT / SOURCE_REL).stat().st_size, SOURCE_SIZE_BYTES)
        for row in self.new_rows:
            locator = row["source_locator"]
            rights = row["rights"]
            self.assertEqual(locator["source_id"], SOURCE_ID)
            self.assertEqual(locator["artifact_sha256"], SOURCE_SHA256)
            self.assertEqual(locator["artifact_size_bytes"], SOURCE_SIZE_BYTES)
            self.assertEqual(locator["mathlib_commit"], MATHLIB_COMMIT)
            self.assertRegex(locator["url"], COMMIT_URL_RE)
            self.assertEqual(locator["source_path"], self.source_by_id[locator["source_record_id"]]["source"]["path"])
            self.assertEqual(rights["formal_code_terms"], "Apache-2.0")
            self.assertEqual(rights["docstring_terms"], "Apache-2.0")
            self.assertEqual(rights["status"], "cleared_with_attribution")
            self.assertIn("The mathlib Community", rights["attribution"])
            self.assertIs(rights["catalog_relicenses_source"], False)
            self.assertEqual(row["provenance"]["mathlib_commit"], MATHLIB_COMMIT)
            self.assertEqual(row["proof_evidence"]["mathlib_commit"], MATHLIB_COMMIT)

        def rights_mutation(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            row = catalog["records"][3_100]
            row["rights"]["attribution"].append("A forged attribution")
            row["rights"]["rights_payload_sha256"] = hash_without(
                row["rights"], "rights_payload_sha256"
            )
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(rights_mutation, "rights mutation")

        def commit_mutation(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            row = catalog["records"][3_100]
            forged = "0" * 40
            row["source_locator"]["mathlib_commit"] = forged
            row["source_locator"]["url"] = row["source_locator"]["url"].replace(
                MATHLIB_COMMIT, forged
            )
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(commit_mutation, "commit-locator mutation")

    def test_strict_1000_and_open_problem_599_are_unchanged(self) -> None:
        self.assertEqual(len(self.strict["strict_credits"]), 1_000)
        self.assertEqual(len(self.strict["credit_corrections"]), 1)
        for field in ("strict_credits", "credit_corrections", "counts", "set_digests"):
            self.assertEqual(self.strict[field], self.parent_strict[field])
        open_problems = [
            row
            for row in self.catalog["records"]
            if row.get("current_claim_kind") == "open_problem"
        ]
        self.assertEqual(len(open_problems), 599)
        self.assertEqual(self.open_list["records"], self.parent_open["records"])
        self.assertEqual(
            self.open_list["stage_claim_ids"], self.parent_open["stage_claim_ids"]
        )
        self.assertEqual(len(self.open_list["records"]), 1_600)

        def strict_mutation(root: Path) -> None:
            strict = copy.deepcopy(self.strict)
            strict["strict_credits"].pop()
            strict["counts"]["effective_strict_credits"] = 999
            credits = strict["strict_credits"]
            strict["set_digests"]["effective_s5_id_set_sha256"] = set_digest(
                str(row["stage_claim_id"]) for row in credits
            )
            strict["set_digests"]["effective_variant_id_set_sha256"] = set_digest(
                str(row["variant_id"]) for row in credits
            )
            reseal_artifact(root, "Strict_Conjecture_Ledger.json", strict)
            rebind_manifest_and_current(root, ["Strict_Conjecture_Ledger.json"])

        self.assert_checker_rejects(strict_mutation, "strict-credit mutation")

        def open_mutation(root: Path) -> None:
            projection = copy.deepcopy(self.open_list)
            victim_index = next(
                index
                for index, row in enumerate(projection["records"])
                if row.get("current_claim_kind") == "open_problem"
            )
            projection["records"].pop(victim_index)
            projection["stage_claim_ids"].pop(victim_index)
            reseal_artifact(root, "Open_Claim_List.json", projection)
            rebind_manifest_and_current(root, ["Open_Claim_List.json"])

        self.assert_checker_rejects(open_mutation, "open-problem projection mutation")

    def test_manifest_release_root_and_current_pointer_mutations_fail(self) -> None:
        self.assertEqual(
            self.manifest["authority_sha256"],
            hash_without(self.manifest, "authority_sha256"),
        )
        by_name = {row["path"]: row for row in self.manifest["artifacts"]}
        self.assertEqual(set(by_name), set(RELEASE_FILES))
        for name in RELEASE_FILES:
            path = ROOT / RELEASE_REL / name
            self.assertEqual(by_name[name]["sha256"], sha256_file(path))
            self.assertEqual(by_name[name]["size_bytes"], path.stat().st_size)
        computed_root = release_root(self.manifest["artifacts"])
        self.assertEqual(self.manifest["release_root_sha256"], computed_root)
        self.assertEqual(self.current["release"], "5.3")
        self.assertEqual(self.current["release_root_sha256"], computed_root)
        self.assertEqual(
            self.current["manifest_sha256"],
            sha256_file(ROOT / RELEASE_REL / MANIFEST_NAME),
        )

        def root_mutation(root: Path) -> None:
            manifest_path = materialize(root, RELEASE_REL / MANIFEST_NAME)
            manifest = load_json(manifest_path)
            manifest["release_root_sha256"] = "0" * 64
            seal_document(manifest)
            write_document(manifest_path, manifest)
            update_current_for_manifest(root, manifest)

        self.assert_checker_rejects(root_mutation, "release-root mutation")

        def current_mutation(root: Path) -> None:
            current_path = materialize(root, CURRENT_REL)
            current = load_json(current_path)
            current["manifest_sha256"] = "f" * 64
            seal_document(current)
            write_document(current_path, current)

        self.assert_checker_rejects(current_mutation, "current-pointer mutation")


if __name__ == "__main__":
    unittest.main()
