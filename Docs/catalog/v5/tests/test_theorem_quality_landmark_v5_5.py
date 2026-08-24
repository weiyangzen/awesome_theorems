#!/usr/bin/env python3
"""Focused black-box tests for the repository-owned landmark review ledger."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]
CURATION = ROOT / "Docs/catalog/v5/curation/theorem_quality_v5_5"
LEDGER = CURATION / "landmark-ledger-0-1199.json"
BUILDER = ROOT / "Docs/catalog/v5/tools/build_theorem_quality_landmark_v5_5.py"
CHECKER = ROOT / "Docs/catalog/v5/tools/check_theorem_quality_landmark_v5_5.py"


class TheoremQualityLandmarkTests(unittest.TestCase):
    def run_tool(self, tool: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(tool), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_repository_ledger_is_reproducible_and_independently_valid(self) -> None:
        build = self.run_tool(BUILDER, "--check")
        self.assertEqual(build.returncode, 0, build.stderr)
        self.assertIn("new=0", build.stdout)
        checked = self.run_tool(CHECKER)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        result = json.loads(checked.stdout)
        self.assertTrue(result["overall_pass"])
        self.assertEqual(result["rows"], 1200)
        self.assertEqual(result["new_release_theorems"], 0)

    def test_official_artifacts_have_no_ephemeral_paths_or_release_credit(self) -> None:
        paths = [LEDGER, *sorted((CURATION / "reviews").glob("review-*.jsonl"))]
        self.assertEqual(len(paths), 7)
        for path in paths:
            payload = path.read_bytes()
            self.assertNotIn(b"/tmp/", payload, path.name)
            self.assertNotIn(b"/home/sansha/", payload, path.name)
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertTrue(ledger["scope"]["not_a_release_append"])
        self.assertEqual(ledger["counts"]["new_release_theorem_credits"], 0)
        self.assertEqual(ledger["counts"]["strict_conjecture_credits"], 0)

    def test_ledger_mutation_is_rejected(self) -> None:
        payload = LEDGER.read_bytes()
        needle = b'"grants_new_release_theorem_credit":false'
        self.assertIn(needle, payload)
        with tempfile.TemporaryDirectory() as directory:
            mutated = Path(directory) / "landmark-ledger.json"
            mutated.write_bytes(payload.replace(needle, b'"grants_new_release_theorem_credit":true', 1))
            result = self.run_tool(CHECKER, "--ledger", str(mutated))
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
