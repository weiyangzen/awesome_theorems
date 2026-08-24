#!/usr/bin/env python3
"""Regression test for the independently checked 1962--1977 seed review."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


REPO = Path(__file__).resolve().parents[4]
CHECKER = REPO / "Docs/catalog/v5/tools/check_putnam_seed_review_1962_1977_v5_6.py"


class PutnamSeedReview1962To1977Test(unittest.TestCase):
    def test_independent_checker(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("rows=192", result.stdout)
        self.assertIn("remaining_full_grid=576", result.stdout)


if __name__ == "__main__":
    unittest.main()
