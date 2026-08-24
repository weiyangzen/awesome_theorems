#!/usr/bin/env python3
"""Black-box and adversarial tests for the frontier qualification checker."""

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
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[4]
CHECKER_REL = Path(
    "Docs/catalog/v5/tools/check_frontier_theorem_qualification_v5_5.py"
)
QUALIFICATION_REL = Path(
    "Docs/catalog/v5/curation/Frontier_Theorem_Qualification_v5_5.json"
)
ACCEPTANCE_REL = Path(
    "Docs/catalog/v5/curation/Frontier_Theorem_Qualification_Acceptance_v5_5.json"
)
REVIEW_DIR_REL = Path(
    "Docs/catalog/v5/curation/frontier_theorem_reviews_v5_5"
)
FIXED_RELS = (
    Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json"),
    Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json"),
    Path(
        "Docs/catalog/v5/curation/theorem_quality_v5_5/"
        "mathlib-important-inventory-1000.json"
    ),
    Path(
        "Docs/catalog/v5/curation/erdos_parent_join_v5_5/"
        "resolved-theorem-max2-selected.jsonl"
    ),
    Path(
        "Docs/catalog/v5/curation/erdos_parent_join_v5_5/"
        "resolved-theorem-supplemental.jsonl"
    ),
    Path("Docs/catalog/v5/curation/Frontier_Theorem_Candidate_Queue_v5_5.json"),
    Path(
        "Docs/catalog/v5/curation/"
        "Frontier_Theorem_Supplemental_Candidate_Queue_v5_5.json"
    ),
)
IMPORTANT_REL = FIXED_RELS[2]


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return digest(canonical({key: item for key, item in value.items() if key not in omitted}))


def set_digest(values: list[str]) -> str:
    return digest(canonical(sorted(values)))


class FrontierQualificationTests(unittest.TestCase):
    def mirror(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="frontier-qualification-")
        root = Path(temporary.name) / "mirror"
        for relative in FIXED_RELS:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(ROOT / relative, target)
        for source in sorted((ROOT / REVIEW_DIR_REL).glob("*.jsonl")):
            relative = source.relative_to(ROOT)
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        target = root / CHECKER_REL
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / CHECKER_REL, target)
        if (ROOT / QUALIFICATION_REL).is_file():
            for relative in (QUALIFICATION_REL, ACCEPTANCE_REL):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
        return temporary, root

    def run_checker(
        self,
        root: Path,
        *,
        receipt_json: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        foreign = root.parent / "foreign-cwd"
        foreign.mkdir(exist_ok=True)
        command = [
            sys.executable,
            str(root / CHECKER_REL),
            "--repo-root",
            str(root),
        ]
        if receipt_json:
            command.append("--receipt-json")
        return subprocess.run(
            command,
            cwd=foreign,
            text=True,
            capture_output=True,
            timeout=90,
            check=False,
        )

    def assert_fails(
        self,
        result: subprocess.CompletedProcess[str],
        fragment: str,
    ) -> None:
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(fragment, output)
        self.assertNotIn("Traceback", output)

    def load_qualification(self, root: Path) -> dict[str, Any]:
        return json.loads((root / QUALIFICATION_REL).read_text(encoding="utf-8"))

    def reseal_qualification(self, root: Path, document: dict[str, Any]) -> None:
        credits = document["accepted_credits"]
        document["set_digests"] = {
            "accepted_stage_claim_id_set_sha256": set_digest(
                [row["stage_claim_id"] for row in credits]
            ),
            "accepted_variant_id_set_sha256": set_digest(
                [row["variant_id"] for row in credits]
            ),
            "accepted_semantic_key_set_sha256": set_digest(
                [row["semantic_key"] for row in credits]
            ),
            "accepted_row_sha256_set_sha256": set_digest(
                [row["row_sha256"] for row in credits]
            ),
        }
        document["authority_sha256"] = hash_without(document, "authority_sha256")
        (root / QUALIFICATION_REL).write_bytes(canonical(document) + b"\n")

    def require_baseline(self) -> None:
        if not (ROOT / QUALIFICATION_REL).is_file():
            self.skipTest("qualification baseline has not been generated yet")

    def test_pristine_passes_or_incomplete_inputs_fail_clearly(self) -> None:
        result = self.run_checker(ROOT)
        output = result.stdout + result.stderr
        if (ROOT / QUALIFICATION_REL).is_file():
            self.assertEqual(result.returncode, 0, output)
            self.assertIn("PASS frontier theorem qualification", result.stdout)
            self.assertNotIn("Traceback", output)
        else:
            self.assertNotEqual(result.returncode, 0, output)
            self.assertTrue(
                "review coverage incomplete" in output
                or "qualification artifact missing" in output,
                output,
            )
            self.assertNotIn("Traceback", output)

    def test_pristine_receipt_json_is_closed_and_resealed(self) -> None:
        self.require_baseline()
        result = self.run_checker(ROOT, receipt_json=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["findings"], [])
        self.assertEqual(receipt["review_manifest"]["files"], 13)
        self.assertEqual(receipt["review_manifest"]["rows"], 917)
        self.assertEqual(
            receipt["checker"]["file_sha256"],
            digest((ROOT / CHECKER_REL).read_bytes()),
        )
        self.assertEqual(
            receipt["qualification"]["file_sha256"],
            digest((ROOT / QUALIFICATION_REL).read_bytes()),
        )
        self.assertEqual(
            receipt["authority_sha256"],
            hash_without(receipt, "authority_sha256"),
        )
        self.assertEqual(
            (ROOT / ACCEPTANCE_REL).read_bytes(),
            canonical(receipt) + b"\n",
        )

    def test_outer_resealed_new_identity_credit_escalation_fails(self) -> None:
        self.require_baseline()
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)
        document = self.load_qualification(root)
        row = document["accepted_credits"][0]
        row["grants_new_theorem_identity_credit"] = True
        row["row_sha256"] = hash_without(row, "row_sha256")
        self.reseal_qualification(root, document)
        self.assert_fails(self.run_checker(root), "new theorem credit escalation")

    def test_outer_resealed_important_overlap_fails(self) -> None:
        self.require_baseline()
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)
        document = self.load_qualification(root)
        important = json.loads((root / IMPORTANT_REL).read_text(encoding="utf-8"))
        row = document["accepted_credits"][0]
        row["stage_claim_id"] = important["records"][0]["stage_claim_id"]
        row["row_sha256"] = hash_without(row, "row_sha256")
        self.reseal_qualification(root, document)
        self.assert_fails(self.run_checker(root), "overlaps important inventory")

    def test_outer_resealed_semantic_duplicate_fails(self) -> None:
        self.require_baseline()
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)
        document = self.load_qualification(root)
        first, second = document["accepted_credits"][:2]
        second["semantic_key"] = first["semantic_key"]
        second["row_sha256"] = hash_without(second, "row_sha256")
        self.reseal_qualification(root, document)
        self.assert_fails(self.run_checker(root), "semantic duplicate")

    def test_outer_resealed_review_file_hash_substitution_fails(self) -> None:
        self.require_baseline()
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)
        document = self.load_qualification(root)
        document["inputs"]["review_ledgers"][0]["file_sha256"] = "0" * 64
        self.reseal_qualification(root, document)
        self.assert_fails(self.run_checker(root), "review ledger file hash mismatch")

    def test_resealed_review_identity_substitution_fails_candidate_replay(self) -> None:
        self.require_baseline()
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)
        review = root / REVIEW_DIR_REL / "nonerdos_001_085.jsonl"
        original_review_sha = digest(review.read_bytes())
        rows = [json.loads(line) for line in review.read_text(encoding="utf-8").splitlines()]
        rows[0]["stage_claim_id"] = rows[1]["stage_claim_id"]
        rows[0]["review_row_sha256"] = hash_without(rows[0], "review_row_sha256")
        payload = b"".join(canonical(row) + b"\n" for row in rows)
        review.write_bytes(payload)
        checker = root / CHECKER_REL
        checker_text = checker.read_text(encoding="utf-8")
        self.assertIn(original_review_sha, checker_text)
        checker.write_text(
            checker_text.replace(original_review_sha, digest(payload)),
            encoding="utf-8",
        )
        document = self.load_qualification(root)
        relative = review.relative_to(root).as_posix()
        item = next(
            entry
            for entry in document["inputs"]["review_ledgers"]
            if entry["path"] == relative
        )
        item.update(
            {
                "file_sha256": digest(payload),
                "size_bytes": len(payload),
                "rows": len(rows),
            }
        )
        self.reseal_qualification(root, document)
        self.assert_fails(self.run_checker(root), "candidate binding mismatch: stage_claim_id")

    def test_outer_resealed_gate_tamper_fails_fixed_review_hash(self) -> None:
        self.require_baseline()
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)
        review = root / REVIEW_DIR_REL / "nonerdos_086_170.jsonl"
        rows = [json.loads(line) for line in review.read_text(encoding="utf-8").splitlines()]
        rows[0]["gates"]["rights"]["evidence"].append("resealed adversarial evidence")
        rows[0]["row_sha256"] = hash_without(rows[0], "row_sha256")
        payload = b"".join(canonical(row) + b"\n" for row in rows)
        review.write_bytes(payload)
        document = self.load_qualification(root)
        relative = review.relative_to(root).as_posix()
        item = next(
            entry
            for entry in document["inputs"]["review_ledgers"]
            if entry["path"] == relative
        )
        item.update(
            {
                "file_sha256": digest(payload),
                "size_bytes": len(payload),
                "rows": len(rows),
            }
        )
        self.reseal_qualification(root, document)
        self.assert_fails(self.run_checker(root), "fixed review ledger hash drifted")

    def test_missing_review_batch_fails_coverage(self) -> None:
        self.require_baseline()
        temporary, root = self.mirror()
        self.addCleanup(temporary.cleanup)
        batches = sorted((root / REVIEW_DIR_REL).glob("nonerdos_supplemental_*.jsonl"))
        self.assertGreaterEqual(len(batches), 2)
        batches[-1].unlink()
        self.assert_fails(self.run_checker(root), "review coverage incomplete")


if __name__ == "__main__":
    unittest.main()
