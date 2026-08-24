#!/usr/bin/env python3
"""Replay and black-box mutation tests for non-Erdos ranks 1--85."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]
BUILDER_REL = Path("Docs/catalog/v5/tools/build_frontier_theorem_review_nonerdos_001_085_v5_5.py")
CHECKER_REL = Path("Docs/catalog/v5/tools/check_frontier_theorem_review_nonerdos_001_085_v5_5.py")
LEDGER_REL = Path("Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5/nonerdos_001_085.jsonl")
SUMMARY_REL = Path("Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5/nonerdos_001_085_summary.json")


class FrontierReviewNonErdos001085Tests(unittest.TestCase):
    def run_checker(
        self,
        root: Path = ROOT,
        *,
        ledger: Path | None = None,
        summary: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        cmd = [sys.executable, str(root / CHECKER_REL), "--repo-root", str(root)]
        if ledger is not None:
            cmd += ["--jsonl", str(ledger)]
        if summary is not None:
            cmd += ["--receipt", str(summary)]
        return subprocess.run(
            cmd,
            cwd=root.parent,
            text=True,
            capture_output=True,
            timeout=45,
            check=False,
        )

    def assert_fails(self, result: subprocess.CompletedProcess[str], fragment: str) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        output = result.stdout + result.stderr
        self.assertIn(fragment, output)
        self.assertNotIn("Traceback", output)

    def test_pristine_passes(self) -> None:
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["eligible_existing_frontier_credit"], 41)
        self.assertEqual(payload["grants_new_theorem_credit"], 0)

    def test_checker_does_not_import_builder(self) -> None:
        checker = (ROOT / CHECKER_REL).read_text(encoding="utf-8")
        self.assertNotIn("build_frontier_theorem_review_nonerdos_001_085_v5_5", checker)

    def test_builder_replays_byte_identically(self) -> None:
        with tempfile.TemporaryDirectory(prefix="frontier-review-replay-") as directory:
            output = Path(directory)
            result = subprocess.run(
                [sys.executable, str(ROOT / BUILDER_REL), "--repo-root", str(ROOT), "--output-dir", str(output)],
                cwd=ROOT.parent,
                text=True,
                capture_output=True,
                timeout=45,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((output / LEDGER_REL.name).read_bytes(), (ROOT / LEDGER_REL).read_bytes())
            self.assertEqual((output / SUMMARY_REL.name).read_bytes(), (ROOT / SUMMARY_REL).read_bytes())

    def test_new_theorem_credit_mutation_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="frontier-review-mutation-") as directory:
            ledger = Path(directory) / LEDGER_REL.name
            data = (ROOT / LEDGER_REL).read_text(encoding="utf-8")
            ledger.write_text(data.replace('"grants_new_theorem_credit":false', '"grants_new_theorem_credit":true', 1), encoding="utf-8")
            result = self.run_checker(ledger=ledger, summary=ROOT / SUMMARY_REL)
            self.assert_fails(result, "review JSONL fixed authority mismatch")

    def test_decision_mutation_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="frontier-review-mutation-") as directory:
            ledger = Path(directory) / LEDGER_REL.name
            data = (ROOT / LEDGER_REL).read_text(encoding="utf-8")
            ledger.write_text(data.replace('"decision":"eligible_existing_frontier_credit"', '"decision":"pending"', 1), encoding="utf-8")
            result = self.run_checker(ledger=ledger, summary=ROOT / SUMMARY_REL)
            self.assert_fails(result, "review JSONL fixed authority mismatch")

    def test_source_binding_mutation_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="frontier-review-mutation-") as directory:
            ledger = Path(directory) / LEDGER_REL.name
            data = (ROOT / LEDGER_REL).read_text(encoding="utf-8")
            ledger.write_text(data.replace('"source_archive_sha256":"51535', '"source_archive_sha256":"61535', 1), encoding="utf-8")
            result = self.run_checker(ledger=ledger, summary=ROOT / SUMMARY_REL)
            self.assert_fails(result, "review JSONL fixed authority mismatch")

    def test_summary_mutation_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="frontier-review-mutation-") as directory:
            summary = Path(directory) / SUMMARY_REL.name
            data = (ROOT / SUMMARY_REL).read_text(encoding="utf-8")
            summary.write_text(data.replace('"grants_new_theorem_credit": 0', '"grants_new_theorem_credit": 1', 1), encoding="utf-8")
            result = self.run_checker(ledger=ROOT / LEDGER_REL, summary=summary)
            self.assert_fails(result, "receipt authority hash mismatch")

    def test_repo_relative_provenance_has_no_machine_paths(self) -> None:
        for relative in (BUILDER_REL, CHECKER_REL, LEDGER_REL, SUMMARY_REL):
            data = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("/" + "tmp/", data)
            self.assertNotIn("/" + "home/", data)


if __name__ == "__main__":
    unittest.main()
