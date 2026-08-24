from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from Docs.catalog.v5.tools import (
    check_theorem_quality_landmark_overlay_067_133_v5_5 as overlay_checker,
)


ROOT = Path(__file__).resolve().parents[4]
REVIEW_CHECKER = ROOT / "Docs/catalog/v5/tools/check_theorem_quality_wiki_review_067_133_v5_5.py"
OVERLAY_BUILDER = ROOT / "Docs/catalog/v5/tools/build_theorem_quality_landmark_overlay_067_133_v5_5.py"
OVERLAY = ROOT / "Docs/catalog/v5/curation/theorem_quality_v5_5/landmark-overlay-067-133.json"


class TheoremQualityWikiOverlay067133Test(unittest.TestCase):
    def test_range_review_independent_checker(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REVIEW_CHECKER)], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["eligible_existing_quality_credit"], 27)
        self.assertEqual(report["new_catalog_entries"], 0)
        self.assertEqual(report["release_theorems"], 2500)
        self.assertEqual(report["release_strict_conjectures"], 1000)

    def test_chained_overlay_rebuild_and_checker(self) -> None:
        result = subprocess.run(
            [sys.executable, str(OVERLAY_BUILDER), "--check"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        report = overlay_checker.check(ROOT)
        self.assertEqual(report["prior_existing_quality"], 469)
        self.assertEqual(report["current_existing_quality"], 496)
        self.assertEqual(report["layer_existing_quality_delta"], 27)
        self.assertEqual(report["new_release_theorems"], 0)
        self.assertEqual(report["strict_conjecture_credits"], 0)

    def test_recomputed_inventory_credit_tamper_is_rejected(self) -> None:
        payload = json.loads(OVERLAY.read_text(encoding="utf-8"))
        payload["scope"]["new_release_theorem_credit_granted"] = 1
        payload["authority_sha256"] = overlay_checker.hash_without(
            payload, "authority_sha256"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered-overlay.json"
            path.write_bytes(overlay_checker.canonical(payload) + b"\n")
            with self.assertRaises(overlay_checker.CheckError):
                overlay_checker.check(ROOT, overlay_path=path)


if __name__ == "__main__":
    unittest.main()
