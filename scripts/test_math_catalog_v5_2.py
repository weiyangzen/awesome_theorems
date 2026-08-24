#!/usr/bin/env python3
"""Independent contract and mutation tests for the Stage5 5.2 release.

The tests deliberately treat ``check_math_catalog_v5_2.py`` as a black-box
executable.  They do not import the release generator, source extractor, or
curation builder.  Mutated packages are assembled below a temporary repo root;
release artifacts, the manifest, and the current-release pointer are resealed
where appropriate so that the checker must enforce the mathematical/catalog
invariant rather than merely notice a stale outer hash.
"""

from __future__ import annotations

import ast
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
from typing import Any, Callable, Iterable, Mapping
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check_math_catalog_v5_2.py"
CATALOG_REL = Path("Docs/catalog/v5")
RELEASE_REL = CATALOG_REL / "releases/5.2"
SUCCESSOR_RELEASE_REL = CATALOG_REL / "releases/5.3"
PARENT_REL = CATALOG_REL / "releases/5.1"
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
MOVING_SOFA_S5_ID = "S5-CLM-00005311"
MOVING_SOFA_ATV_ID = "ATV-00005311"
VERSIONED_ARXIV_RE = re.compile(r"^[0-9]{4}\.[0-9]{4,5}v[1-9][0-9]*$")


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
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
        raise AssertionError(f"expected JSON object: {path}")
    return value


def seal_document(value: dict[str, Any]) -> dict[str, Any]:
    value["authority_sha256"] = hash_without(value, "authority_sha256")
    return value


def write_document(path: Path, value: dict[str, Any]) -> None:
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


def strict_row_count(ledger: Mapping[str, Any]) -> int:
    return len(ledger["strict_credits"]) + len(ledger["credit_corrections"])


def mirror_catalog_tree(destination_root: Path) -> None:
    """Make a cheap mirror using hard links, copied before every mutation."""

    source = ROOT / "Docs/catalog"
    destination = destination_root / "Docs/catalog"
    for item in sorted(source.rglob("*")):
        relative = item.relative_to(source)
        target = destination / relative
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(item, target)


def materialize(root: Path, relative: Path) -> Path:
    """Replace one mirrored hard link with a private mutable copy."""

    target = root / relative
    source = ROOT / relative
    if target.is_symlink():
        target.unlink()
    elif target.exists():
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
        return strict_row_count(document)
    raise AssertionError(f"unknown release artifact: {name}")


def rebind_manifest_and_current(root: Path, changed_names: Iterable[str]) -> None:
    """Rebind changed artifacts, release root, and the direct/successor pointer."""

    changed = set(changed_names)
    release_dir = root / RELEASE_REL
    manifest_path = materialize(root, RELEASE_REL / MANIFEST_NAME)
    manifest = load_json(manifest_path)
    by_name = {row["path"]: row for row in manifest["artifacts"]}
    if set(by_name) != set(RELEASE_FILES):
        raise AssertionError("unexpected v5.2 manifest inventory")

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

    rebind_current(root, manifest_path)


def rebind_current(root: Path, v52_manifest_path: Path) -> None:
    """Bind Current either directly to 5.2 or through its exact 5.3 successor."""

    current_path = materialize(root, CURRENT_REL)
    current = load_json(current_path)
    v52_manifest = load_json(v52_manifest_path)
    if current.get("release") == "5.2":
        current.clear()
        current.update(
            {
                "schema_version": "awesome-theorems/stage5-current-release/5.2",
                "release": "5.2",
                "release_root_sha256": v52_manifest["release_root_sha256"],
                "manifest_sha256": sha256_file(v52_manifest_path),
                "manifest_path": "releases/5.2/Release_Manifest.json",
            }
        )
    elif current.get("release") == "5.3":
        successor_manifest_path = materialize(
            root, SUCCESSOR_RELEASE_REL / MANIFEST_NAME
        )
        successor_manifest = load_json(successor_manifest_path)
        successor_manifest["parent_release"] = "5.2"
        successor_manifest["parent_release_root_sha256"] = v52_manifest[
            "release_root_sha256"
        ]
        seal_document(successor_manifest)
        write_document(successor_manifest_path, successor_manifest)
        current.clear()
        current.update(
            {
                "schema_version": "awesome-theorems/stage5-current-release/5.3",
                "release": "5.3",
                "release_root_sha256": successor_manifest[
                    "release_root_sha256"
                ],
                "manifest_sha256": sha256_file(successor_manifest_path),
                "manifest_path": "releases/5.3/Release_Manifest.json",
            }
        )
    else:
        raise AssertionError("test fixture Current must point to 5.2 or 5.3")
    seal_document(current)
    write_document(current_path, current)


def point_current_directly_to_v52(root: Path) -> None:
    current_path = materialize(root, CURRENT_REL)
    manifest_path = root / RELEASE_REL / MANIFEST_NAME
    manifest = load_json(manifest_path)
    current = seal_document(
        {
            "schema_version": "awesome-theorems/stage5-current-release/5.2",
            "release": "5.2",
            "release_root_sha256": manifest["release_root_sha256"],
            "manifest_sha256": sha256_file(manifest_path),
            "manifest_path": "releases/5.2/Release_Manifest.json",
        }
    )
    write_document(current_path, current)


def reseal_artifact(root: Path, name: str, document: dict[str, Any]) -> None:
    path = materialize(root, RELEASE_REL / name)
    seal_document(document)
    write_document(path, document)


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


class MathCatalogV52Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not CHECKER_PATH.is_file():
            raise AssertionError(f"missing independent checker: {CHECKER_PATH}")
        cls.parent_catalog = load_json(ROOT / PARENT_REL / "Claim_Catalog.json")
        cls.catalog = load_json(ROOT / RELEASE_REL / "Claim_Catalog.json")
        cls.strict = load_json(
            ROOT / RELEASE_REL / "Strict_Conjecture_Ledger.json"
        )
        cls.manifest = load_json(ROOT / RELEASE_REL / MANIFEST_NAME)
        cls.successor_manifest = load_json(
            ROOT / SUCCESSOR_RELEASE_REL / MANIFEST_NAME
        )
        cls.current = load_json(ROOT / CURRENT_REL)
        cls.new_rows = [
            row
            for row in cls.catalog["records"]
            if row.get("origin_release") == "5.2"
        ]

    def assert_checker_rejects(
        self, mutate: Callable[[Path], None], label: str
    ) -> str:
        with tempfile.TemporaryDirectory(prefix="at-v52-test-") as directory:
            temporary_root = Path(directory)
            mirror_catalog_tree(temporary_root)
            mutate(temporary_root)
            result = run_checker(temporary_root)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("Traceback (most recent call last)", result.stdout)
        self.assertIn("FAIL", result.stdout, f"{label}: {result.stdout}")
        return result.stdout

    def test_independent_checker_imports_no_generator_or_extractor(self) -> None:
        tree = ast.parse(CHECKER_PATH.read_text(encoding="utf-8"))
        imported: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        forbidden = [
            name
            for name in imported
            if "generat" in name.lower() or "extract" in name.lower()
        ]
        self.assertEqual(forbidden, [])

    def test_checker_passes_canonical_and_mirrored_release(self) -> None:
        canonical = run_checker(ROOT)
        self.assertEqual(canonical.returncode, 0, canonical.stdout)
        self.assertIn("PASS", canonical.stdout)
        with tempfile.TemporaryDirectory(prefix="at-v52-baseline-") as directory:
            temporary_root = Path(directory)
            mirror_catalog_tree(temporary_root)
            mirrored = run_checker(temporary_root)
        self.assertEqual(mirrored.returncode, 0, mirrored.stdout)
        self.assertIn("PASS", mirrored.stdout)
        with tempfile.TemporaryDirectory(prefix="at-v52-direct-") as directory:
            temporary_root = Path(directory)
            mirror_catalog_tree(temporary_root)
            point_current_directly_to_v52(temporary_root)
            direct = run_checker(temporary_root)
        self.assertEqual(direct.returncode, 0, direct.stdout)
        self.assertIn("PASS", direct.stdout)

    def test_current_rejects_future_or_wrong_successor_pointers(self) -> None:
        def future_mutation(root: Path) -> None:
            current_path = materialize(root, CURRENT_REL)
            current = load_json(current_path)
            current["schema_version"] = "awesome-theorems/stage5-current-release/5.4"
            current["release"] = "5.4"
            current["manifest_path"] = "releases/5.4/Release_Manifest.json"
            seal_document(current)
            write_document(current_path, current)

        self.assert_checker_rejects(future_mutation, "future Current pointer")

        def wrong_parent_mutation(root: Path) -> None:
            successor_path = materialize(
                root, SUCCESSOR_RELEASE_REL / MANIFEST_NAME
            )
            successor = load_json(successor_path)
            successor["parent_release_root_sha256"] = "0" * 64
            seal_document(successor)
            write_document(successor_path, successor)
            current_path = materialize(root, CURRENT_REL)
            current = load_json(current_path)
            current["manifest_sha256"] = sha256_file(successor_path)
            seal_document(current)
            write_document(current_path, current)

        self.assert_checker_rejects(
            wrong_parent_mutation, "wrong authenticated successor parent"
        )

    def test_parent_prefix_is_exact_and_mutation_is_rejected(self) -> None:
        parent_rows = self.parent_catalog["records"]
        child_rows = self.catalog["records"]
        self.assertEqual(len(parent_rows), 2_500)
        self.assertEqual(child_rows[: len(parent_rows)], parent_rows)

        def mutate(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            catalog["records"][0]["display_name"] += " [tampered parent]"
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(mutate, "parent-prefix mutation")

    def test_exact_strict_count_is_1000_and_count_mutation_is_rejected(self) -> None:
        credits = self.strict["strict_credits"]
        self.assertEqual(
            self.strict["authority_sha256"],
            hash_without(self.strict, "authority_sha256"),
        )
        self.assertTrue(
            all(
                row["row_sha256"] == hash_without(row, "row_sha256")
                for row in credits
            )
        )
        self.assertEqual(len(credits), 1_000)
        self.assertEqual(
            self.strict["counts"],
            {
                "effective_strict_credits": 1_000,
                "effective_parent_credits": 400,
                "origin_5_2_credits": 600,
                "credit_corrections": 1,
            },
        )
        self.assertEqual(len({row["stage_claim_id"] for row in credits}), 1_000)
        self.assertEqual(len({row["variant_id"] for row in credits}), 1_000)

        def mutate(root: Path) -> None:
            strict = copy.deepcopy(self.strict)
            victim = strict["strict_credits"].pop()
            branch = victim["credit_source_branch"]
            strict["counts"]["effective_strict_credits"] -= 1
            if branch == "origin_5_2_curated_latex_environment":
                strict["counts"]["origin_5_2_credits"] -= 1
            else:
                strict["counts"]["effective_parent_credits"] -= 1
            rows = strict["strict_credits"]
            strict["set_digests"]["effective_s5_id_set_sha256"] = set_digest(
                row["stage_claim_id"] for row in rows
            )
            strict["set_digests"]["effective_variant_id_set_sha256"] = set_digest(
                row["variant_id"] for row in rows
            )
            strict["set_digests"]["effective_parent_s5_id_set_sha256"] = set_digest(
                row["stage_claim_id"]
                for row in rows
                if row["credit_source_branch"]
                == "effective_parent_5_1_direct_prop"
            )
            strict["set_digests"]["origin_5_2_s5_id_set_sha256"] = set_digest(
                row["stage_claim_id"]
                for row in rows
                if row["credit_source_branch"]
                == "origin_5_2_curated_latex_environment"
            )
            reseal_artifact(root, "Strict_Conjecture_Ledger.json", strict)
            rebind_manifest_and_current(root, ["Strict_Conjecture_Ledger.json"])

        self.assert_checker_rejects(mutate, "strict-count mutation")

    def test_moving_sofa_credit_is_revoked_and_regrant_is_rejected(self) -> None:
        credits = self.strict["strict_credits"]
        self.assertNotIn(MOVING_SOFA_S5_ID, {row["stage_claim_id"] for row in credits})
        self.assertNotIn(MOVING_SOFA_ATV_ID, {row["variant_id"] for row in credits})
        self.assertEqual(len(self.strict["credit_corrections"]), 1)
        correction = self.strict["credit_corrections"][0]
        self.assertEqual(correction["stage_claim_id"], MOVING_SOFA_S5_ID)
        self.assertEqual(correction["variant_id"], MOVING_SOFA_ATV_ID)
        self.assertEqual(correction["disposition"], "strict_credit_revoked")
        self.assertIs(correction["grants_strict_conjecture_credit"], False)
        parent_target = next(
            row
            for row in self.parent_catalog["records"]
            if row["stage_claim_id"] == MOVING_SOFA_S5_ID
        )
        self.assertEqual(
            correction["parent_record_sha256"],
            sha256_bytes(canonical_json_bytes(parent_target)),
        )

        def mutate(root: Path) -> None:
            strict = copy.deepcopy(self.strict)
            strict["credit_corrections"][0][
                "grants_strict_conjecture_credit"
            ] = True
            reseal_artifact(root, "Strict_Conjecture_Ledger.json", strict)
            rebind_manifest_and_current(root, ["Strict_Conjecture_Ledger.json"])

        self.assert_checker_rejects(mutate, "MovingSofa regrant mutation")

    def test_new_600_ids_are_contiguous_and_id_mutation_is_rejected(self) -> None:
        self.assertEqual(len(self.new_rows), 600)
        expected_atv = [f"ATV-{ordinal:08d}" for ordinal in range(5_985, 6_585)]
        expected_s5 = [f"S5-CLM-{ordinal:08d}" for ordinal in range(5_985, 6_585)]
        self.assertEqual([row["variant_id"] for row in self.new_rows], expected_atv)
        self.assertEqual([row["stage_claim_id"] for row in self.new_rows], expected_s5)
        origin_credits = [
            row
            for row in self.strict["strict_credits"]
            if row["credit_source_branch"]
            == "origin_5_2_curated_latex_environment"
        ]
        self.assertEqual(
            sorted(row["stage_claim_id"] for row in origin_credits), expected_s5
        )

        def mutate(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            catalog["records"][2_500]["variant_id"] = "ATV-99999999"
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(mutate, "new-ID mutation")

    def test_manifest_inventory_and_release_root_tampering_are_rejected(self) -> None:
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
        self.assertEqual(
            self.current["manifest_path"], "releases/5.3/Release_Manifest.json"
        )
        self.assertEqual(
            self.successor_manifest["parent_release"], "5.2"
        )
        self.assertEqual(
            self.successor_manifest["parent_release_root_sha256"], computed_root
        )
        self.assertEqual(
            self.current["release_root_sha256"],
            self.successor_manifest["release_root_sha256"],
        )
        self.assertEqual(
            self.current["manifest_sha256"],
            sha256_file(ROOT / SUCCESSOR_RELEASE_REL / MANIFEST_NAME),
        )

        def root_mutation(root: Path) -> None:
            manifest_path = materialize(root, RELEASE_REL / MANIFEST_NAME)
            manifest = load_json(manifest_path)
            manifest["release_root_sha256"] = "0" * 64
            seal_document(manifest)
            write_document(manifest_path, manifest)
            rebind_current(root, manifest_path)

        self.assert_checker_rejects(root_mutation, "release-root mutation")

        def inventory_mutation(root: Path) -> None:
            manifest_path = materialize(root, RELEASE_REL / MANIFEST_NAME)
            manifest = load_json(manifest_path)
            manifest["artifacts"][0]["sha256"] = "f" * 64
            manifest["release_root_sha256"] = release_root(manifest["artifacts"])
            seal_document(manifest)
            write_document(manifest_path, manifest)
            rebind_current(root, manifest_path)

        self.assert_checker_rejects(inventory_mutation, "manifest inventory mutation")

    def test_rights_and_versioned_locators_are_exact_and_mutations_are_rejected(
        self,
    ) -> None:
        for row in self.new_rows:
            locator = row["source_locator"]
            rights = row["rights"]
            paper = row["paper"]
            arxiv_id = locator["arxiv_id"]
            self.assertRegex(arxiv_id, VERSIONED_ARXIV_RE)
            self.assertEqual(locator["source_url"], f"https://arxiv.org/e-print/{arxiv_id}")
            self.assertEqual(paper["arxiv_id"], arxiv_id)
            self.assertEqual(paper["source_url"], locator["source_url"])
            self.assertEqual(rights["spdx_expression"], "CC-BY-4.0")
            self.assertEqual(rights["license_family"], "cc_by")
            self.assertIs(rights["publication_text_allowed"], True)
            self.assertIs(rights["text_withheld"], False)
            self.assertEqual(rights["attribution_arxiv_id"], arxiv_id)
            self.assertEqual(rights["attribution_authors"], paper["authors"])
            self.assertEqual(rights["attribution_title"], paper["title"])
            self.assertEqual(rights["source_refs"], [row["source_id"]])

        def rights_mutation(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            row = catalog["records"][2_500]
            # Keep the closed-schema license constants intact and forge a
            # syntactically valid attribution instead.  Recompute both nested
            # hashes so rejection requires the source/rights cross-binding.
            row["rights"]["attribution_title"] += " [wrong attribution]"
            attribution = {
                "attribution_authors": row["rights"]["attribution_authors"],
                "attribution_title": row["rights"]["attribution_title"],
                "attribution_arxiv_id": row["rights"]["attribution_arxiv_id"],
            }
            row["rights"]["attribution_payload_sha256"] = sha256_bytes(
                canonical_json_bytes(attribution)
            )
            row["rights"]["rights_payload_sha256"] = hash_without(
                row["rights"], "rights_payload_sha256"
            )
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(rights_mutation, "rights mutation")

        def locator_mutation(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            row = catalog["records"][2_500]
            unversioned = row["source_locator"]["arxiv_id"].split("v", 1)[0]
            row["source_locator"]["arxiv_id"] = unversioned
            row["source_locator"]["source_url"] = (
                f"https://arxiv.org/e-print/{unversioned}"
            )
            row["paper"]["arxiv_id"] = unversioned
            row["paper"]["source_url"] = row["source_locator"]["source_url"]
            row["rights"]["attribution_arxiv_id"] = unversioned
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(locator_mutation, "unversioned locator mutation")

    def test_semantic_keys_are_unique_and_duplicate_mutation_is_rejected(self) -> None:
        semantic_keys = [row["semantic_key"] for row in self.new_rows]
        self.assertEqual(len(semantic_keys), 600)
        self.assertEqual(len(set(semantic_keys)), 600)
        self.assertEqual(
            self.manifest["accepted_set_digests"]["semantic_key_set_sha256"],
            set_digest(semantic_keys),
        )

        def mutate(root: Path) -> None:
            catalog = copy.deepcopy(self.catalog)
            left, right = catalog["records"][2_500:2_502]
            right["semantic_key"] = left["semantic_key"]
            right["dedupe"]["semantic_key"] = left["semantic_key"]
            right["dedupe"]["semantic_key_sha256"] = sha256_bytes(
                left["semantic_key"].encode("utf-8")
            )
            right["dedupe"]["identity_payload_sha256"] = sha256_bytes(
                canonical_json_bytes(
                    {
                        "semantic_key": right["semantic_key"],
                        "content_hash": right["source_locator"]["content_hash"],
                        "statement_sha256": right["mathematical_statement"][
                            "statement_sha256"
                        ],
                        "source_record_sha256": right["source_locator"][
                            "source_record_sha256"
                        ],
                    }
                )
            )
            right["allocation"]["allocation_request_sha256"] = sha256_bytes(
                canonical_json_bytes(
                    {
                        "origin_release": right["origin_release"],
                        "source_id": right["source_id"],
                        "content_hash": right["source_locator"]["content_hash"],
                        "semantic_key": right["semantic_key"],
                        "statement_sha256": right["mathematical_statement"][
                            "statement_sha256"
                        ],
                        "family_action": right["allocation"]["family_action"],
                    }
                )
            )
            right["semantic_payload_sha256"] = sha256_bytes(
                canonical_json_bytes(
                    {
                        "record_role": right["record_role"],
                        "atomicity": right["atomicity"],
                        "truth_apt": right["truth_apt"],
                        "category": right["category"],
                        "current_claim_kind": right["current_claim_kind"],
                        "semantic_key": right["semantic_key"],
                        "statement_sha256": right["mathematical_statement"][
                            "statement_sha256"
                        ],
                    }
                )
            )
            reseal_artifact(root, "Claim_Catalog.json", catalog)
            rebind_manifest_and_current(root, ["Claim_Catalog.json"])

        self.assert_checker_rejects(mutate, "duplicate semantic-key mutation")


if __name__ == "__main__":
    unittest.main()
