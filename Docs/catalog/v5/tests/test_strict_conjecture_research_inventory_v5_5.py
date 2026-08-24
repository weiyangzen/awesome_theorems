#!/usr/bin/env python3
"""Black-box mutation tests for the strict research-conjecture inventory."""

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
CHECKER = Path("Docs/catalog/v5/tools/check_strict_conjecture_research_inventory_v5_5.py")
LEDGER = Path("Docs/catalog/v5/curation/conjecture_quality_v5_5/strict-research-inventory-1000.json")
INPUTS = (
    Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json"),
    Path("Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json"),
    Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json"),
    Path("Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz"),
    Path("Docs/catalog/v5/sources/openconjecture-fa03d85-cc-by-real-conf090.jsonl"),
    Path("Docs/catalog/v5/curation/OpenConjecture_Curation_v5_2.json"),
)
LEDGER_SHA = "9a76a5632d8b99a5034adb8a0f2e481f2bb642903edea475049e9d477796d80c"
AUTHORITY = "0bc736749dbf9d823bd2b2c66066171c71e0f7369cd1c25d75a653f3f715a1f8"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def without(value: Mapping[str, Any], field: str) -> str:
    return digest(canonical({key: item for key, item in value.items() if key != field}))


def digest_set(values: list[str]) -> str:
    return digest(canonical(sorted(values)))


class StrictConjectureResearchInventoryTests(unittest.TestCase):
    def mirror(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="strict-research-")
        root = Path(temporary.name) / "mirror"
        for relative in INPUTS:
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.link(ROOT / relative, destination)
        for relative in (CHECKER, LEDGER):
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, destination)
        return temporary, root

    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        cwd = root.parent / "foreign-cwd"
        cwd.mkdir(exist_ok=True)
        return subprocess.run(
            [sys.executable, str(root / CHECKER), "--repo-root", str(root)],
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )

    def mutate(self, root: Path, change: Callable[[dict[str, Any]], None]) -> None:
        ledger_path = root / LEDGER
        document = json.loads(ledger_path.read_text(encoding="utf-8"))
        change(document)
        document["set_digests"]["row_sha256_set_sha256"] = digest_set([row["row_sha256"] for row in document["records"]])
        document["authority_sha256"] = without(document, "authority_sha256")
        ledger_path.write_bytes(canonical(document) + b"\n")
        checker_path = root / CHECKER
        checker = checker_path.read_text(encoding="utf-8")
        checker = checker.replace(LEDGER_SHA, digest(ledger_path.read_bytes()))
        checker = checker.replace(AUTHORITY, document["authority_sha256"])
        checker_path.write_text(checker, encoding="utf-8")

    def assert_failure(self, result: subprocess.CompletedProcess[str], fragment: str) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        output = result.stdout + result.stderr
        self.assertIn(fragment, output)
        self.assertNotIn("Traceback", output)

    def test_pristine_mirror_passes_from_foreign_cwd(self) -> None:
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)
        result = self.run_checker(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("strict_research=1000 formal_frontier=400 openconjecture=600 new=0", result.stdout)

    def test_resealed_new_identity_credit_escalation_fails(self) -> None:
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)

        def change(document: dict[str, Any]) -> None:
            row = document["records"][0]
            row["grants_new_conjecture_identity_credit"] = True
            row["row_sha256"] = without(row, "row_sha256")

        self.mutate(root, change)
        self.assert_failure(self.run_checker(root), "new conjecture credit escalation")

    def test_resealed_source_quality_tier_substitution_fails(self) -> None:
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)

        def change(document: dict[str, Any]) -> None:
            row = document["records"][0]
            row["quality_tier"] = "source_curated_high_research_conjecture"
            row["row_sha256"] = without(row, "row_sha256")

        self.mutate(root, change)
        self.assert_failure(self.run_checker(root), "Formal quality tier mismatch")

    def test_resealed_false_as_zero_status_count_fails(self) -> None:
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)

        def change(document: dict[str, Any]) -> None:
            document["counts"]["independent_current_literature_status_reviews"] = False

        self.mutate(root, change)
        self.assert_failure(self.run_checker(root), "independent current status reviews must be integer 0")


if __name__ == "__main__":
    unittest.main()
