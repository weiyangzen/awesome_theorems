#!/usr/bin/env python3
"""Black-box and mutation tests for the repository-owned AimPL audit checker."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[4]
SOURCE_REL = Path("Docs/catalog/v5/sources/aimpl")
CURATION_REL = Path("Docs/catalog/v5/curation/aimpl_v5_5")
TOOLS_REL = Path("Docs/catalog/v5/tools")
CHECKER_REL = TOOLS_REL / "check_aimpl_audit_v5_5.py"

MIRROR_FILES = [
    SOURCE_REL / "aimpl-source-snapshot.tar.gz",
    SOURCE_REL / "source-manifest.json",
    SOURCE_REL / "candidates.jsonl",
    SOURCE_REL / "asset-receipt.json",
    CURATION_REL / "review-a.jsonl",
    CURATION_REL / "review-b.jsonl",
    CURATION_REL / "review-ledger.jsonl",
    CURATION_REL / "review-summary.json",
    CURATION_REL / "cross-dedupe-retrieval.jsonl",
    CURATION_REL / "cross-dedupe-retrieval-summary.json",
    CURATION_REL / "crosscheck-conjecturebench-302.jsonl",
    CURATION_REL / "crosscheck-oeis-602.jsonl",
    CURATION_REL / "audit-receipt.json",
    Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json"),
    Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json"),
    TOOLS_REL / "extract_aimpl_conjectures_v5_5.py",
    TOOLS_REL / "build_aimpl_review_b_v5_5.py",
    TOOLS_REL / "build_aimpl_cross_dedupe_v5_5.py",
    TOOLS_REL / "finalize_aimpl_audit_v5_5.py",
    CHECKER_REL,
]


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_json(path: Path, value: object) -> None:
    path.write_bytes(canonical(value))


def write_jsonl(path: Path, values: list[dict]) -> None:
    path.write_bytes(b"".join(canonical(value) for value in values))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(mirror: Path, path: Path, rows: int | None = None) -> dict[str, object]:
    value: dict[str, object] = {
        "path": path.relative_to(mirror).as_posix(),
        "sha256": digest(path),
        "size_bytes": path.stat().st_size,
    }
    if rows is not None:
        value["rows"] = rows
    return value


def tree_state(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class AimPLAuditCheckerTests(unittest.TestCase):
    maxDiff = None

    def make_mirror(self, base: Path) -> Path:
        mirror = base / "mirror"
        for relative in MIRROR_FILES:
            source = REPO / relative
            destination = mirror / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        return mirror

    def run_checker(self, mirror: Path, foreign_cwd: Path) -> subprocess.CompletedProcess[str]:
        foreign_cwd.mkdir(parents=True, exist_ok=True)
        return subprocess.run(
            [sys.executable, str(mirror / CHECKER_REL), "--repo-root", str(mirror)],
            cwd=foreign_cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def rebind_candidate_chain(self, mirror: Path) -> None:
        candidates = mirror / SOURCE_REL / "candidates.jsonl"
        asset_receipt_path = mirror / SOURCE_REL / "asset-receipt.json"
        retrieval_summary_path = mirror / CURATION_REL / "cross-dedupe-retrieval-summary.json"
        summary_path = mirror / CURATION_REL / "review-summary.json"
        audit_path = mirror / CURATION_REL / "audit-receipt.json"

        asset_receipt = load_json(asset_receipt_path)
        asset_receipt["candidates"] = binding(mirror, candidates, 59)
        write_json(asset_receipt_path, asset_receipt)

        retrieval_summary = load_json(retrieval_summary_path)
        retrieval_summary["inputs"]["aimpl_candidates"] = binding(mirror, candidates, 59)
        write_json(retrieval_summary_path, retrieval_summary)

        summary = load_json(summary_path)
        summary["inputs"]["candidates"] = binding(mirror, candidates, 59)
        summary["inputs"]["source_asset_receipt"] = binding(mirror, asset_receipt_path)
        summary["inputs"]["cross_dedupe_retrieval_summary"] = binding(
            mirror, retrieval_summary_path,
        )
        write_json(summary_path, summary)

        audit = load_json(audit_path)
        audit["artifacts"]["candidates"] = binding(mirror, candidates, 59)
        audit["artifacts"]["source_asset_receipt"] = binding(mirror, asset_receipt_path)
        audit["artifacts"]["cross_dedupe_retrieval_summary"] = binding(
            mirror, retrieval_summary_path,
        )
        audit["artifacts"]["review_summary"] = binding(mirror, summary_path)
        write_json(audit_path, audit)

    def test_pristine_mirror_passes_from_foreign_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            mirror = self.make_mirror(base)
            result = self.run_checker(mirror, base / "foreign-cwd")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                "pages=495 candidates=59 high=13 medium=30 reject=14 pending=2 strict_credit=0",
                result.stdout,
            )

    def test_repo_root_is_authoritative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            mirror = self.make_mirror(base)
            (mirror / CURATION_REL / "crosscheck-conjecturebench-302.jsonl").unlink()
            result = self.run_checker(mirror, base / "foreign-cwd")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing repository file", result.stderr)

    def test_checker_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            mirror = self.make_mirror(base)
            before = tree_state(mirror)
            result = self.run_checker(mirror, base / "foreign-cwd")
            after = tree_state(mirror)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(after, before)
            self.assertFalse((mirror / "Docs/catalog/v5/releases/5.5").exists())

    def test_resealed_candidate_tag_mutation_is_rejected_by_source_replay(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            mirror = self.make_mirror(base)
            candidates_path = mirror / SOURCE_REL / "candidates.jsonl"
            candidates = load_jsonl(candidates_path)
            candidates[0]["exact_source"]["problem_tag"] = "theorem"
            write_jsonl(candidates_path, candidates)
            self.rebind_candidate_chain(mirror)

            result = self.run_checker(mirror, base / "foreign-cwd")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("problem tag does not match frozen object", result.stderr)
            self.assertNotIn("receipt mismatch", result.stderr)

    def test_resealed_nonliteral_accepted_claim_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            mirror = self.make_mirror(base)
            review_a_path = mirror / CURATION_REL / "review-a.jsonl"
            ledger_path = mirror / CURATION_REL / "review-ledger.jsonl"
            summary_path = mirror / CURATION_REL / "review-summary.json"
            audit_path = mirror / CURATION_REL / "audit-receipt.json"

            reviews = load_jsonl(review_a_path)
            reviews[0]["exact_claim_html"] = "A fabricated claim absent from the frozen source."
            write_jsonl(review_a_path, reviews)
            ledger = load_jsonl(ledger_path)
            ledger[0]["initial_review"]["exact_claim_html"] = reviews[0]["exact_claim_html"]
            write_jsonl(ledger_path, ledger)

            summary = load_json(summary_path)
            summary["inputs"]["review_a"] = binding(mirror, review_a_path, 30)
            summary["review_ledger_sha256"] = digest(ledger_path)
            write_json(summary_path, summary)

            audit = load_json(audit_path)
            audit["artifacts"]["review_a"] = binding(mirror, review_a_path, 30)
            audit["artifacts"]["review_ledger"] = binding(mirror, ledger_path, 59)
            audit["artifacts"]["review_summary"] = binding(mirror, summary_path)
            write_json(audit_path, audit)

            result = self.run_checker(mirror, base / "foreign-cwd")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("accepted exact claim is not a literal body substring", result.stderr)
            self.assertNotIn("receipt mismatch", result.stderr)

    def test_resealed_strict_credit_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            mirror = self.make_mirror(base)
            asset_receipt_path = mirror / SOURCE_REL / "asset-receipt.json"
            summary_path = mirror / CURATION_REL / "review-summary.json"
            audit_path = mirror / CURATION_REL / "audit-receipt.json"

            asset_receipt = load_json(asset_receipt_path)
            asset_receipt["strict_credit_granted"] = 1
            write_json(asset_receipt_path, asset_receipt)
            summary = load_json(summary_path)
            summary["inputs"]["source_asset_receipt"] = binding(mirror, asset_receipt_path)
            write_json(summary_path, summary)
            audit = load_json(audit_path)
            audit["artifacts"]["source_asset_receipt"] = binding(mirror, asset_receipt_path)
            audit["artifacts"]["review_summary"] = binding(mirror, summary_path)
            write_json(audit_path, audit)

            result = self.run_checker(mirror, base / "foreign-cwd")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source asset receipt grants strict credit", result.stderr)


if __name__ == "__main__":
    unittest.main()
