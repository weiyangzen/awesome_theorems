#!/usr/bin/env python3
"""Independent and mutation tests for the full Putnam 5.6 source freeze."""

from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / "Docs/catalog/v5/tools/freeze_full_putnam_source_v5_6.py"
CURATION = ROOT / "Docs/catalog/v5/curation/putnambench_v5_6"

spec = importlib.util.spec_from_file_location("freeze_full_putnam_source_v5_6", TOOL)
assert spec is not None and spec.loader is not None
freezer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = freezer
spec.loader.exec_module(freezer)


GOLDEN_FILES = {
    "Full_Putnam_Source_Inventory_v5_6.json": "245c448bccec0f73087d4b38b3124124c34dd27a3e5d5531a545084a9ed5b643",
    "Full_Putnam_Source_Candidates_v5_6.jsonl": "615c3db2c950f793669b77a23396a87318a8a956312876704e959c3f083b59ff",
    "Full_Putnam_Seed_Problems_v5_6.jsonl": "cfdde7b8117565f0fc7ea6e7fbad2ad42971aca97f09074b539b586dc7a97c8c",
    "PutnamGAP_Source_Locator_Manifest_v5_6.jsonl": "72a28d27099145506a4f779bb3b1941af0414dbff1956fa6052e604b1c00d085",
    "Kedlaya_2025_Source_Locator_Manifest_v5_6.jsonl": "3e80a1c1931a1ee362a3defb95577e3378d2483742b2b3a7be5980512686d51a",
}


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(name: str) -> list[dict]:
    payload = (CURATION / name).read_bytes()
    assert payload.endswith(b"\n")
    return [json.loads(line) for line in payload.splitlines()]


class FullPutnamFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = json.loads((CURATION / "Full_Putnam_Source_Inventory_v5_6.json").read_text())
        cls.candidates = load_jsonl("Full_Putnam_Source_Candidates_v5_6.jsonl")
        cls.problems = load_jsonl("Full_Putnam_Seed_Problems_v5_6.jsonl")
        cls.pg_manifest = load_jsonl("PutnamGAP_Source_Locator_Manifest_v5_6.jsonl")
        cls.kedlaya_manifest = load_jsonl("Kedlaya_2025_Source_Locator_Manifest_v5_6.jsonl")
        cls.pb_problems = load_jsonl("PutnamBench_Source_Problems_v5_6.jsonl")

    def make_repo_copy(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        destination = root / "Docs/catalog/v5/curation/putnambench_v5_6"
        destination.mkdir(parents=True)
        for name in [*GOLDEN_FILES, "PutnamBench_Source_Inventory_v5_6.json", "PutnamBench_Source_Problems_v5_6.jsonl"]:
            shutil.copyfile(CURATION / name, destination / name)
        return temporary, root

    def mutate_jsonl(self, root: Path, name: str, row_index: int, field: str, value: object) -> None:
        path = root / "Docs/catalog/v5/curation/putnambench_v5_6" / name
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        rows[row_index][field] = value
        path.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows))

    def test_01_repository_only_checker_passes(self) -> None:
        inventory, candidates, problems, pg_rows, kedlaya_rows = freezer.validate_repo_only(ROOT)
        self.assertEqual(inventory["authority_sha256"], "08fb966f533d6ab0f29b08f02ef55de77752f20471bcec3c65915a518df7df84")
        self.assertEqual((len(candidates), len(problems), len(pg_rows), len(kedlaya_rows)), (1063, 768, 1051, 12))

    def test_02_golden_file_digests(self) -> None:
        self.assertEqual({name: sha_file(CURATION / name) for name in GOLDEN_FILES}, GOLDEN_FILES)

    def test_03_candidate_partition_is_exact(self) -> None:
        self.assertEqual(Counter(row["source_branch"] for row in self.candidates), Counter({"putnamgap": 1051, "kedlaya_2025": 12}))
        self.assertEqual(Counter(row["disposition"] for row in self.candidates), Counter({"mapped_in_scope_coordinate": 768, "out_of_scope_pre_1962": 295}))
        self.assertEqual(len({row["source_candidate_id"] for row in self.candidates}), 1063)

    def test_04_grid_projection_is_exact(self) -> None:
        expected = {
            f"putnam_{year}_{section}{number}"
            for year in range(1962, 2026)
            for section in ("a", "b")
            for number in range(1, 7)
        }
        self.assertEqual({row["problem_key"] for row in self.problems}, expected)
        self.assertTrue(all(len(row["source_candidate_ids"]) == 1 for row in self.problems))
        self.assertEqual(Counter(row["source_branch"] for row in self.problems), Counter({"putnamgap": 756, "kedlaya_2025": 12}))

    def test_05_putnambench_subset_and_complement_are_exact(self) -> None:
        pb_by_key = {row["problem_key"]: row for row in self.pb_problems}
        full_by_key = {row["problem_key"]: row for row in self.problems}
        self.assertEqual(len(pb_by_key), 675)
        self.assertEqual(len(set(full_by_key) - set(pb_by_key)), 93)
        for key, pb in pb_by_key.items():
            self.assertEqual(full_by_key[key]["putnambench_problem_row_sha256"], pb["row_sha256"])
            self.assertEqual(full_by_key[key]["formal_variant_ids"], pb["formal_variant_ids"])

    def test_06_putnamgap_native_ids_and_decoded_field_hash_contract(self) -> None:
        self.assertEqual(self.pg_manifest[0]["source_candidate_id"].split("/")[-1], self.pg_manifest[0]["native_index"])
        self.assertEqual(self.pg_manifest[-1]["native_index"], "2024-B-6")
        self.assertEqual(
            self.inventory["set_digests"]["putnamgap_candidate_id_set_sha256"],
            "b92d3ea93f5efe6b1d24a4713abcf2b1c31bb1598a3946ec6f680728d7cf3aa7",
        )
        self.assertTrue(all(row["record_locator"]["statement_pointer"] == "/question" for row in self.pg_manifest))
        self.assertTrue(all(row["record_locator"]["solution_pointer"] == "/solution" for row in self.pg_manifest))

    def test_07_kedlaya_twelve_item_hashes_are_golden(self) -> None:
        labels = [f"{section}{number}" for section in ("A", "B") for number in range(1, 7)]
        self.assertEqual([row["statement_binding"]["item_label"] for row in self.kedlaya_manifest], labels)
        for row, label in zip(self.kedlaya_manifest, labels, strict=True):
            self.assertEqual(
                (row["statement_binding"]["item_body_sha256"], row["solution_binding"]["item_body_sha256"]),
                freezer.KEDLAYA_EXPECTED_HASHES[label],
            )

    def test_08_rights_do_not_expand_component_licenses(self) -> None:
        registry = self.inventory["rights"]["registry"]
        self.assertFalse(registry[freezer.PUTNAMGAP_RIGHTS_ID]["putnamgap_cc_by_4_0_applies_to_original_problem_or_solution_text"])
        self.assertFalse(registry[freezer.KEDLAYA_RIGHTS_ID]["mirror_mit_license_applies_to_problem_or_solution_text"])
        policy = self.inventory["rights"]["catalog_release_policy"]
        self.assertFalse(policy["exact_original_problem_text_redistributed"])
        self.assertFalse(policy["exact_canonical_solution_text_redistributed"])

    def test_09_derived_rows_are_prose_free_closed_schemas(self) -> None:
        forbidden = {"question", "solution", "statement", "proof", "problem_text", "solution_text"}
        for collection in (self.candidates, self.problems, self.pg_manifest, self.kedlaya_manifest):
            for row in collection:
                self.assertTrue(forbidden.isdisjoint(row))
                self.assertNotIn("informal_statement", row)
                self.assertNotIn("informal_solution", row)

    def test_10_cli_check_works_from_foreign_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(TOOL), "--check"],
                cwd=directory,
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("grid=768", result.stdout)

    def test_11_candidate_mutation_fails_closed(self) -> None:
        temporary, root = self.make_repo_copy()
        try:
            self.mutate_jsonl(root, "Full_Putnam_Source_Candidates_v5_6.jsonl", 0, "source_year", 1963)
            with self.assertRaises(freezer.FreezeError):
                freezer.validate_repo_only(root)
        finally:
            temporary.cleanup()

    def test_12_manifest_hash_mutation_fails_closed(self) -> None:
        temporary, root = self.make_repo_copy()
        try:
            self.mutate_jsonl(root, "PutnamGAP_Source_Locator_Manifest_v5_6.jsonl", 500, "rights_id", "CC-BY-4.0")
            with self.assertRaises(freezer.FreezeError):
                freezer.validate_repo_only(root)
        finally:
            temporary.cleanup()

    def test_13_seed_projection_mutation_fails_closed(self) -> None:
        temporary, root = self.make_repo_copy()
        try:
            self.mutate_jsonl(root, "Full_Putnam_Seed_Problems_v5_6.jsonl", 400, "source_candidate_ids", [])
            with self.assertRaises(freezer.FreezeError):
                freezer.validate_repo_only(root)
        finally:
            temporary.cleanup()

    def test_14_inventory_authority_mutation_fails_closed(self) -> None:
        temporary, root = self.make_repo_copy()
        try:
            path = root / "Docs/catalog/v5/curation/putnambench_v5_6/Full_Putnam_Source_Inventory_v5_6.json"
            document = json.loads(path.read_text())
            document["authority_sha256"] = "0" * 64
            path.write_text(json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n")
            with self.assertRaises(freezer.FreezeError):
                freezer.validate_repo_only(root)
        finally:
            temporary.cleanup()

    def test_15_embedded_archive_is_rejected(self) -> None:
        temporary, root = self.make_repo_copy()
        try:
            path = root / "Docs/catalog/v5/curation/putnambench_v5_6/source.tar.gz"
            path.write_bytes(b"not an archive")
            with self.assertRaises(freezer.FreezeError):
                freezer.validate_repo_only(root)
        finally:
            temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
