#!/usr/bin/env python3
"""Black-box mutation tests for the important-mathlib inventory checker."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from typing import Any, Callable, Mapping


ROOT = Path(__file__).resolve().parents[4]
CHECKER_REL = Path("Docs/catalog/v5/tools/check_mathlib_important_inventory_v5_5.py")
LEDGER_REL = Path("Docs/catalog/v5/curation/theorem_quality_v5_5/mathlib-important-inventory-1000.json")
INPUT_RELS = (
    Path("Docs/catalog/v5/sources/mathlib-theorems-8a178386.json"),
    Path("Docs/catalog/v5/curation/Mathlib_Theorem_Curation_v5_3.json"),
    Path("Docs/catalog/v5/curation/Mathlib_Theorem_Curation_v5_4.json"),
    Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json"),
)
ORIGINAL_LEDGER_SHA = "a3db9bcd31feb8f2ea4ac07c0b60076446af25b3e4045c2938851440fb974f92"
ORIGINAL_AUTHORITY = "0b4d7c43f91e3c57104665c579fabf7b8a27282b10d95670dea9ccb3bbaf11d2"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return digest(canonical({key: item for key, item in value.items() if key not in ignored}))


def set_digest(values: list[str]) -> str:
    return digest(canonical(sorted(values)))


class MathlibImportantInventoryTests(unittest.TestCase):
    def mirror(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="mathlib-important-")
        root = Path(temporary.name) / "mirror"
        for relative in INPUT_RELS:
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.link(ROOT / relative, destination)
        for relative in (CHECKER_REL, LEDGER_REL):
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)
        return temporary, root

    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        cwd = root.parent / "foreign-cwd"
        cwd.mkdir(exist_ok=True)
        return subprocess.run(
            [sys.executable, str(root / CHECKER_REL), "--repo-root", str(root)],
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )

    def mutate_and_reseal(self, root: Path, mutation: Callable[[dict[str, Any]], None]) -> None:
        ledger_path = root / LEDGER_REL
        document = json.loads(ledger_path.read_text(encoding="utf-8"))
        mutation(document)
        document["set_digests"]["row_sha256_set_sha256"] = set_digest([row["row_sha256"] for row in document["records"]])
        document["authority_sha256"] = hash_without(document, "authority_sha256")
        ledger_path.write_bytes(canonical(document) + b"\n")
        checker_path = root / CHECKER_REL
        checker = checker_path.read_text(encoding="utf-8")
        checker = checker.replace(ORIGINAL_LEDGER_SHA, digest(ledger_path.read_bytes()))
        checker = checker.replace(ORIGINAL_AUTHORITY, document["authority_sha256"])
        checker_path.write_text(checker, encoding="utf-8")

    def assert_fails(self, result: subprocess.CompletedProcess[str], fragment: str) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        output = result.stdout + result.stderr
        self.assertIn(fragment, output)
        self.assertNotIn("Traceback", output)

    def test_pristine_foreign_cwd_passes(self) -> None:
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)
        result = self.run_checker(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("important=1000 named=180 module_main=820 new=0", result.stdout)

    def test_resealed_new_theorem_credit_escalation_fails(self) -> None:
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)

        def mutation(document: dict[str, Any]) -> None:
            row = document["records"][0]
            row["grants_new_theorem_identity_credit"] = True
            row["row_sha256"] = hash_without(row, "row_sha256")

        self.mutate_and_reseal(root, mutation)
        self.assert_fails(self.run_checker(root), "new credit escalation")

    def test_resealed_quality_tier_substitution_fails(self) -> None:
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)

        def mutation(document: dict[str, Any]) -> None:
            row = document["records"][0]
            row["quality_tier"] = "human_documented_mathlib_module_main_result"
            row["row_sha256"] = hash_without(row, "row_sha256")

        self.mutate_and_reseal(root, mutation)
        self.assert_fails(self.run_checker(root), "quality tier mismatch")

    def test_resealed_false_as_zero_count_fails(self) -> None:
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)

        def mutation(document: dict[str, Any]) -> None:
            document["counts"]["new_theorem_identity_credits"] = False

        self.mutate_and_reseal(root, mutation)
        self.assert_fails(self.run_checker(root), "new theorem count drifted")


if __name__ == "__main__":
    unittest.main()
