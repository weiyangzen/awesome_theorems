#!/usr/bin/env python3
"""Independent mutation tests for the Putnam seed-crosswalk aggregator."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]
TOOL = ROOT / "Docs/catalog/v5/tools/build_putnam_seed_crosswalk_v5_6.py"
CURATION_REL = Path("Docs/catalog/v5/curation/putnambench_v5_6")

spec = importlib.util.spec_from_file_location("build_putnam_seed_crosswalk_v5_6", TOOL)
assert spec is not None and spec.loader is not None
builder = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = builder
spec.loader.exec_module(builder)


SOURCE_FILES = (
    "Full_Putnam_Source_Inventory_v5_6.json",
    "Full_Putnam_Seed_Problems_v5_6.jsonl",
    "Full_Putnam_Source_Candidates_v5_6.jsonl",
    "PutnamGAP_Source_Locator_Manifest_v5_6.jsonl",
    "Kedlaya_2025_Source_Locator_Manifest_v5_6.jsonl",
    "PutnamBench_Source_Problems_v5_6.jsonl",
    "PutnamBench_Formal_Declaration_Asset_v5_6.jsonl",
)


class SeedCrosswalkTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        destination = root / CURATION_REL
        review_destination = destination / "seed-reviews"
        review_destination.mkdir(parents=True)
        source = ROOT / CURATION_REL
        for name in SOURCE_FILES:
            shutil.copyfile(source / name, destination / name)
        for path in sorted((source / "seed-reviews").glob("*.jsonl")):
            shutil.copyfile(path, review_destination / path.name)
        shutil.copyfile(source / "seed-crosswalk-progress.json", destination / "seed-crosswalk-progress.json")
        return temporary, root

    def rewrite_review(self, root: Path, filename: str, problem_key: str, mutate) -> None:
        path = root / CURATION_REL / "seed-reviews" / filename
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        matches = [row for row in rows if row["problem_key"] == problem_key]
        self.assertEqual(len(matches), 1)
        mutate(matches[0])
        matches[0]["row_sha256"] = builder.hash_without(matches[0], "row_sha256")
        path.write_bytes(builder.encoded_jsonl(rows))

    def test_01_current_progress_is_exact_and_zero_credit(self) -> None:
        collection = builder.collect_reviews(ROOT)
        progress = builder.build_progress(ROOT, collection)
        reviewed = len(collection["selected"])
        propositions = len(collection["semantics"])
        self.assertEqual(progress["counts"]["unique_reviewed_seed_keys"], reviewed)
        self.assertEqual(progress["counts"]["reviewed_benchmark_propositions"], propositions)
        self.assertEqual(progress["counts"]["missing_seed_keys"], 768 - reviewed)
        self.assertGreaterEqual(propositions, reviewed)
        self.assertLess(reviewed, 768)
        self.assertEqual(progress["counts"]["catalog_entries_granted"], 0)
        self.assertEqual(progress["counts"]["theorem_credits_granted"], 0)
        self.assertFalse(progress["gates"]["seed_crosswalk_write_authorized"])
        self.assertEqual(progress["authority_sha256"], builder.hash_without(progress, "authority_sha256"))

    def test_02_progress_file_is_byte_deterministic(self) -> None:
        collection = builder.collect_reviews(ROOT)
        expected = builder.encoded_json(builder.build_progress(ROOT, collection))
        actual = (ROOT / CURATION_REL / "seed-crosswalk-progress.json").read_bytes()
        self.assertEqual(actual, expected)

    def test_03_incomplete_reviews_cannot_build_crosswalk(self) -> None:
        collection = builder.collect_reviews(ROOT)
        reviewed = len(collection["selected"])
        with self.assertRaisesRegex(builder.CrosswalkError, rf"reviewed={reviewed}/768 missing={768-reviewed}"):
            builder.build_crosswalk_rows(ROOT, collection)
        self.assertFalse((ROOT / CURATION_REL / "seed-crosswalk.jsonl").exists())

    def test_04_exact_duplicate_aggregate_rows_are_not_double_counted(self) -> None:
        collection = builder.collect_reviews(ROOT)
        self.assertEqual(
            collection["raw_rows"],
            len(collection["selected"]) + collection["duplicate_occurrences"],
        )
        self.assertGreaterEqual(len(collection["semantics"]), len(collection["selected"]))

    def test_05_resealed_question_hash_mutation_fails(self) -> None:
        temporary, root = self.make_repo()
        try:
            self.rewrite_review(
                root, "1962-1969.jsonl", "putnam_1962_a1",
                lambda row: row["source_binding"].__setitem__("question_value_sha256_utf8", "0" * 64),
            )
            with self.assertRaisesRegex(builder.CrosswalkError, "question hash drifted"):
                builder.collect_reviews(root)
        finally:
            temporary.cleanup()

    def test_06_resealed_semantic_key_mutation_fails(self) -> None:
        temporary, root = self.make_repo()
        try:
            self.rewrite_review(
                root, "1962-1969.jsonl", "putnam_1962_a1",
                lambda row: row["claim_review"].__setitem__("semantic_key", "putnam-seed-semantic-v1/" + "0" * 64),
            )
            with self.assertRaisesRegex(builder.CrosswalkError, "semantic-key formula drifted"):
                builder.collect_reviews(root)
        finally:
            temporary.cleanup()

    def test_07_resealed_split_exhaustiveness_mutation_fails(self) -> None:
        temporary, root = self.make_repo()
        try:
            self.rewrite_review(
                root, "1962-1969.jsonl", "putnam_1963_a1",
                lambda row: row["claim_review"]["multipart_handling"].__setitem__("all_parts_accounted_for", False),
            )
            with self.assertRaisesRegex(builder.CrosswalkError, "split exhaustiveness drifted"):
                builder.collect_reviews(root)
        finally:
            temporary.cleanup()

    def test_08_resealed_formal_header_mutation_fails(self) -> None:
        temporary, root = self.make_repo()
        try:
            self.rewrite_review(
                root, "1962-1969.jsonl", "putnam_1962_a1",
                lambda row: row["putnambench_binding"]["formal_headers"][0].__setitem__("header_sha256", "0" * 64),
            )
            with self.assertRaisesRegex(builder.CrosswalkError, "formal header bytes/language drifted"):
                builder.collect_reviews(root)
        finally:
            temporary.cleanup()

    def test_09_resealed_credit_mutation_fails(self) -> None:
        temporary, root = self.make_repo()
        try:
            self.rewrite_review(
                root, "1962-1969.jsonl", "putnam_1962_a1",
                lambda row: row.__setitem__("grants_theorem_credit", True),
            )
            with self.assertRaisesRegex(builder.CrosswalkError, "zero-credit/publication boundary drifted"):
                builder.collect_reviews(root)
        finally:
            temporary.cleanup()

    def test_10_conflicting_duplicate_review_fails(self) -> None:
        temporary, root = self.make_repo()
        try:
            # The same key remains unchanged in the aggregate file, so this is
            # a sealed but conflicting leaf/aggregate duplicate.
            self.rewrite_review(
                root, "1962-1969.jsonl", "putnam_1962_a1",
                lambda row: row["claim_review"].__setitem__("review_rationale", "Conflicting independently sealed rationale."),
            )
            with self.assertRaisesRegex(builder.CrosswalkError, "conflicting duplicate seed reviews"):
                builder.collect_reviews(root)
        finally:
            temporary.cleanup()

    def test_11_cli_crosswalk_mode_fails_without_writing(self) -> None:
        temporary, root = self.make_repo()
        try:
            reviewed = len(builder.collect_reviews(root)["selected"])
            result = subprocess.run(
                [sys.executable, str(TOOL), "--write-crosswalk", "--repo-root", str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(f"reviewed={reviewed}/768 missing={768-reviewed}", result.stderr)
            self.assertFalse((root / CURATION_REL / "seed-crosswalk.jsonl").exists())
        finally:
            temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
