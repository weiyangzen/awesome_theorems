#!/usr/bin/env python3
"""Black-box tests for the exact-statement/reference quality overlay."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]
CURATION = ROOT / "Docs/catalog/v5/curation/theorem_quality_v5_5"
BASE = CURATION / "landmark-ledger-0-1199.json"
REVIEW = CURATION / "reviews/wiki-reference-review-000-066.json"
SUBREVIEWS = [
    CURATION / "reviews/wiki-reference-subreview-000-016.json",
    CURATION / "reviews/wiki-reference-subreview-017-065.json",
]
OVERLAY = CURATION / "landmark-overlay-000-066.json"
AGGREGATE = CURATION / "landmark-ledger-0-1199-overlay-000-066.json"
REVIEW_BUILDER = ROOT / "Docs/catalog/v5/tools/build_theorem_quality_wiki_review_000_066_v5_5.py"
REVIEW_CHECKER = ROOT / "Docs/catalog/v5/tools/check_theorem_quality_wiki_review_000_066_v5_5.py"
OVERLAY_BUILDER = ROOT / "Docs/catalog/v5/tools/build_theorem_quality_landmark_overlay_v5_5.py"
OVERLAY_CHECKER = ROOT / "Docs/catalog/v5/tools/check_theorem_quality_landmark_overlay_v5_5.py"
BASE_SHA256 = "51c5607cd4289f8340745879b8b134673bbd44e873cebc82e2da59f0ba6c1471"


class TheoremQualityWikiOverlayTests(unittest.TestCase):
    def run_tool(self, tool: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(tool), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_review_and_overlay_are_reproducible_and_independently_valid(self) -> None:
        review_before = REVIEW.read_bytes()
        built_review = self.run_tool(REVIEW_BUILDER)
        self.assertEqual(built_review.returncode, 0, built_review.stderr)
        self.assertEqual(REVIEW.read_bytes(), review_before)
        checked_review = self.run_tool(REVIEW_CHECKER)
        self.assertEqual(checked_review.returncode, 0, checked_review.stderr)
        review_result = json.loads(checked_review.stdout)
        self.assertTrue(review_result["deterministic_rebuild"])
        self.assertEqual(review_result["eligible_existing_quality_credit"], 30)
        self.assertEqual(review_result["new_catalog_entries"], 0)

        built_overlay = self.run_tool(OVERLAY_BUILDER, "--check")
        self.assertEqual(built_overlay.returncode, 0, built_overlay.stderr)
        checked_overlay = self.run_tool(OVERLAY_CHECKER)
        self.assertEqual(checked_overlay.returncode, 0, checked_overlay.stderr)
        overlay_result = json.loads(checked_overlay.stdout)
        self.assertTrue(overlay_result["overall_pass"])
        self.assertEqual(overlay_result["base_existing_quality"], 439)
        self.assertEqual(overlay_result["current_existing_quality"], 469)
        self.assertEqual(overlay_result["existing_quality_delta"], 30)
        self.assertEqual(overlay_result["new_release_theorems"], 0)

    def test_artifacts_are_repository_relative_and_never_grant_release_credit(self) -> None:
        for path in [REVIEW, *SUBREVIEWS, OVERLAY, AGGREGATE]:
            payload = path.read_bytes()
            self.assertNotIn(b"/tmp/", payload, path.name)
            self.assertNotIn(b"/home/", payload, path.name)

        review = json.loads(REVIEW.read_text(encoding="utf-8"))
        self.assertEqual(review["counts"]["eligible_existing_quality_credit"], 30)
        self.assertEqual(review["counts"]["new_catalog_entries"], 0)
        self.assertEqual(review["counts"]["formal_proofs_claimed"], 0)
        for row in review["records"]:
            self.assertFalse(row["grants_new_catalog_entry"])
            self.assertFalse(row["formal_proof_claimed"])
            if row["decision"] == "eligible":
                self.assertIsNotNone(row["evidence"])
                self.assertIsNotNone(row["reference_evidence"])
                self.assertFalse(row["reference_evidence"]["automatic_credit"])

        overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
        aggregate = json.loads(AGGREGATE.read_text(encoding="utf-8"))
        self.assertTrue(overlay["scope"]["base_ledger_is_frozen"])
        self.assertEqual(overlay["counts"]["existing_quality_credit_delta"], 30)
        self.assertEqual(overlay["counts"]["new_release_theorem_credit_delta"], 0)
        self.assertEqual(aggregate["counts"]["base_existing_quality_credits"], 439)
        self.assertEqual(aggregate["counts"]["current_existing_quality_credits"], 469)
        self.assertEqual(aggregate["counts"]["new_release_theorem_credits"], 0)

        import hashlib

        self.assertEqual(hashlib.sha256(BASE.read_bytes()).hexdigest(), BASE_SHA256)

    def test_overlay_credit_escalation_mutation_is_rejected(self) -> None:
        payload = OVERLAY.read_bytes()
        needle = b'"grants_new_release_theorem_credit":false'
        self.assertIn(needle, payload)
        with tempfile.TemporaryDirectory() as directory:
            mutated = Path(directory) / "landmark-overlay.json"
            mutated.write_bytes(
                payload.replace(
                    needle,
                    b'"grants_new_release_theorem_credit":true',
                    1,
                )
            )
            result = self.run_tool(OVERLAY_CHECKER, "--overlay", str(mutated))
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
