#!/usr/bin/env python3
"""Black-box isolation and mutation tests for the OEIS v5.5 audit checker."""

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
from typing import Any


REPO = Path(__file__).resolve().parents[4]
CHECKER = REPO / "Docs/catalog/v5/tools/check_oeis_audit_v5_5.py"
CURATION_REL = Path("Docs/catalog/v5/curation/oeis_v5_5")
SOURCE_RECEIPT_REL = Path(
    "Docs/catalog/v5/sources/oeis-conjectures-4c866362-receipt.json"
)
V1_SOURCE_REL = Path(
    "Docs/catalog/v5/sources/oeis-conjectures-4c866362-candidates.jsonl"
)
V2_SURVIVORS_NAME = "v2/survivors.jsonl"
V2_AUDIT_NAME = "v2/consolidation-audit.json"
COMBINED_NAME = "combined-survivors.jsonl"
AUDIT_RECEIPT_REL = CURATION_REL / "audit-receipt.json"

NON_CURATION_FILES = (
    Path("Docs/catalog/v5/sources/oeis-conjectures-4c866362-source.tar.gz"),
    V1_SOURCE_REL,
    Path("Docs/catalog/v5/sources/oeis-conjectures-4c866362-all-conjectur-v2.jsonl"),
    SOURCE_RECEIPT_REL,
    Path("Docs/catalog/v5/Current_Release.json"),
    Path("Docs/catalog/v5/releases/5.3/Claim_Catalog.json"),
    Path("Docs/catalog/v5/releases/5.3/Strict_Conjecture_Ledger.json"),
    Path("Docs/catalog/v5/releases/5.4/Claim_Catalog.json"),
    Path("Docs/catalog/v5/releases/5.4/Claim_ID_Registry.json"),
    Path("Docs/catalog/v5/releases/5.4/Coverage_Ledger.json"),
    Path("Docs/catalog/v5/releases/5.4/Migration_v4_to_v5.json"),
    Path("Docs/catalog/v5/releases/5.4/Open_Claim_List.json"),
    Path("Docs/catalog/v5/releases/5.4/Release_Manifest.json"),
    Path("Docs/catalog/v5/releases/5.4/Stage5_Claim_ID_Registry.json"),
    Path("Docs/catalog/v5/releases/5.4/Strict_Conjecture_Ledger.json"),
    Path("Docs/catalog/v5/releases/5.4/Theorem_List.json"),
    Path("Docs/catalog/v5/tools/migrate_oeis_audit_v5_5.py"),
    Path("Docs/catalog/v5/tools/check_oeis_audit_v5_5.py"),
    Path("Docs/tools/extract_oeis_conjectures_v5.py"),
    Path("Docs/tools/extract_oeis_conjectures_v5_v2.py"),
)


def canonical(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, payload: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def rewrite_json(path: Path, value: dict[str, Any]) -> None:
    atomic_write(path, canonical(value))


def rewrite_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    atomic_write(path, b"".join(canonical(row) for row in rows))


def binding(root: Path, relative: Path, rows: int | None = None) -> dict[str, Any]:
    path = root / relative
    value: dict[str, Any] = {
        "path": relative.as_posix(),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }
    if rows is not None:
        value["rows"] = rows
    return value


def mirror_files() -> list[Path]:
    curation = [
        path.relative_to(REPO)
        for path in (REPO / CURATION_REL).rglob("*")
        if path.is_file()
    ]
    return sorted(set(curation) | set(NON_CURATION_FILES))


def make_mirror(root: Path) -> None:
    for relative in mirror_files():
        source = REPO / relative
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(source, target)
        except OSError:
            shutil.copy2(source, target)


def tree_snapshot(root: Path) -> dict[str, tuple[str, int]]:
    return {
        path.relative_to(root).as_posix(): (sha256_file(path), path.stat().st_size)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def rebind_audit_artifacts(root: Path, names: set[str]) -> None:
    receipt_path = root / AUDIT_RECEIPT_REL
    receipt = load_json(receipt_path)
    for name in names:
        relative = CURATION_REL / name
        old = receipt["artifacts"][name]
        rows = None
        if "rows" in old:
            rows = sum(
                1 for line in (root / relative).read_bytes().splitlines() if line.strip()
            )
        receipt["artifacts"][name] = binding(root, relative, rows)
    rewrite_json(receipt_path, receipt)


def coordinated_v2_review_change(
    root: Path, changes: dict[str, dict[str, Any]],
) -> None:
    """Change review judgments and consistently refresh every derived hash/projection."""

    review_dir = root / CURATION_REL / "v2/reviews"
    key_to_review: dict[str, Path] = {}
    changed_review_paths: set[Path] = set()
    for review_path in sorted(review_dir.glob("review-v2-*.jsonl")):
        rows = load_jsonl(review_path)
        changed = False
        for row in rows:
            key = row["candidate_key"]
            key_to_review[key] = review_path
            if key in changes:
                row.update(changes[key])
                changed = True
        if changed:
            rewrite_jsonl(review_path, rows)
            changed_review_paths.add(review_path)

    if set(changes) - set(key_to_review):
        raise AssertionError("mutation key is absent from v2 reviews")

    review_sha = {path: sha256_file(path) for path in changed_review_paths}
    survivor_path = root / CURATION_REL / V2_SURVIVORS_NAME
    survivors = load_jsonl(survivor_path)
    for row in survivors:
        key = row["candidate_key"]
        review_path = key_to_review[key]
        if review_path in changed_review_paths:
            row["source_review_sha256"] = review_sha[review_path]
        for field in ("a_numbers", "importance_tier", "exact_claim_text", "semantic_summary"):
            if field in changes.get(key, {}):
                row[field] = changes[key][field]
    rewrite_jsonl(survivor_path, survivors)

    combined_path = root / CURATION_REL / COMBINED_NAME
    combined = load_jsonl(combined_path)
    v2_projection = [{
        **row,
        "audit_layer": "v2_literal_stem_extension",
        "candidate_only": True,
        "grants_catalog_entry": False,
        "grants_strict_conjecture_credit": False,
    } for row in survivors]
    rewrite_jsonl(combined_path, [*combined[:199], *v2_projection])

    v2_audit_path = root / CURATION_REL / V2_AUDIT_NAME
    v2_audit = load_json(v2_audit_path)
    for row in v2_audit["inputs"]["available_reviews"]:
        path = root / row["path"]
        if path in changed_review_paths:
            row["sha256"] = review_sha[path]
    rewrite_json(v2_audit_path, v2_audit)

    artifact_names = {
        path.relative_to(root / CURATION_REL).as_posix()
        for path in changed_review_paths
    }
    artifact_names.update({V2_SURVIVORS_NAME, V2_AUDIT_NAME, COMBINED_NAME})
    rebind_audit_artifacts(root, artifact_names)


class OEISAuditV55BlackBoxTests(unittest.TestCase):
    maxDiff = None

    def fresh_root(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="oeis-v55-test-")
        root = Path(temporary.name)
        make_mirror(root)
        (root / "foreign-cwd").mkdir()
        return temporary, root

    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(CHECKER), "--repo-root", str(root)],
            cwd=root / "foreign-cwd",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def assert_rejected(self, root: Path, message: str | None = None) -> str:
        result = self.run_checker(root)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        if message is not None:
            self.assertIn(message, result.stdout)
        return result.stdout

    def test_complete_mirror_passes_from_foreign_cwd(self) -> None:
        temporary, root = self.fresh_root()
        with temporary:
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("source=622 v1=199 v2=69 combined=268", result.stdout)

    def test_missing_mirror_input_cannot_fall_back_to_real_repository(self) -> None:
        temporary, root = self.fresh_root()
        with temporary:
            (root / V1_SOURCE_REL).unlink()
            self.assert_rejected(root, "missing repository file")

    def test_checker_is_strictly_read_only(self) -> None:
        temporary, root = self.fresh_root()
        with temporary:
            before = tree_snapshot(root)
            first = self.run_checker(root)
            middle = tree_snapshot(root)
            second = self.run_checker(root)
            after = tree_snapshot(root)
            self.assertEqual(first.returncode, 0, first.stdout)
            self.assertEqual(second.returncode, 0, second.stdout)
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(before, middle)
            self.assertEqual(before, after)

    def test_resealed_nonliteral_exact_claim_is_rejected(self) -> None:
        temporary, root = self.fresh_root()
        with temporary:
            survivor = load_jsonl(root / CURATION_REL / V2_SURVIVORS_NAME)[0]
            coordinated_v2_review_change(root, {
                survivor["candidate_key"]: {
                    "exact_claim_text": (
                        "MUTATION: this assertion is absent from the frozen OEIS source."
                    ),
                },
            })
            self.assert_rejected(root, "literal frozen source substring")

    def test_resealed_survivor_key_tier_and_count_mutations_are_rejected(self) -> None:
        for mutation in ("key", "tier", "count"):
            with self.subTest(mutation=mutation):
                temporary, root = self.fresh_root()
                with temporary:
                    survivor_path = root / CURATION_REL / V2_SURVIVORS_NAME
                    combined_path = root / CURATION_REL / COMBINED_NAME
                    survivors = load_jsonl(survivor_path)
                    combined = load_jsonl(combined_path)
                    if mutation == "key":
                        old_key = survivors[0]["candidate_key"]
                        new_key = old_key[:-1] + ("0" if old_key[-1] != "0" else "1")
                        survivors[0]["candidate_key"] = new_key
                        combined[199]["candidate_key"] = new_key
                        rewrite_jsonl(survivor_path, survivors)
                        rewrite_jsonl(combined_path, combined)
                        rebind_audit_artifacts(
                            root, {V2_SURVIVORS_NAME, COMBINED_NAME}
                        )
                        self.assert_rejected(root, "survivor identity/order")
                    elif mutation == "tier":
                        high = next(row for row in survivors if row["importance_tier"] == "high")
                        medium = next(
                            row for row in survivors if row["importance_tier"] == "medium"
                        )
                        coordinated_v2_review_change(root, {
                            high["candidate_key"]: {"importance_tier": "medium"},
                            medium["candidate_key"]: {"importance_tier": "high"},
                        })
                        self.assert_rejected(root, "survivor tier assignment")
                    else:
                        removed_key = survivors.pop()["candidate_key"]
                        combined = [
                            row for row in combined if row["candidate_key"] != removed_key
                        ]
                        rewrite_jsonl(survivor_path, survivors)
                        rewrite_jsonl(combined_path, combined)
                        rebind_audit_artifacts(
                            root, {V2_SURVIVORS_NAME, COMBINED_NAME}
                        )
                        self.assert_rejected(root, "survivor identity/order")

    def test_nonzero_formal_addition_and_strict_credit_are_rejected(self) -> None:
        for mutation in ("formal", "strict"):
            with self.subTest(mutation=mutation):
                temporary, root = self.fresh_root()
                with temporary:
                    receipt_path = root / AUDIT_RECEIPT_REL
                    receipt = load_json(receipt_path)
                    if mutation == "formal":
                        v2_audit_path = root / CURATION_REL / V2_AUDIT_NAME
                        v2_audit = load_json(v2_audit_path)
                        v2_audit["final_gate"]["formal_release_additions_counted"] = 1
                        rewrite_json(v2_audit_path, v2_audit)
                        receipt["artifacts"][V2_AUDIT_NAME] = binding(
                            root, CURATION_REL / V2_AUDIT_NAME
                        )
                        receipt["counts"]["formal_release_additions"] = 1
                    else:
                        receipt["counts"]["strict_credits_granted"] = 1
                    rewrite_json(receipt_path, receipt)
                    self.assert_rejected(root)

    def test_resealed_parent_and_frozen_source_mutations_are_rejected(self) -> None:
        for mutation in ("parent", "source"):
            with self.subTest(mutation=mutation):
                temporary, root = self.fresh_root()
                with temporary:
                    audit_path = root / AUDIT_RECEIPT_REL
                    audit = load_json(audit_path)
                    if mutation == "parent":
                        relative = Path(
                            "Docs/catalog/v5/releases/5.4/Release_Manifest.json"
                        )
                        parent = load_json(root / relative)
                        parent["release"] = "5.4-mutated"
                        rewrite_json(root / relative, parent)
                        audit["parent_release_5_4"]["release_manifest"] = binding(
                            root, relative
                        )
                    else:
                        rows = load_jsonl(root / V1_SOURCE_REL)
                        rows[0]["candidate_only"] = False
                        rewrite_jsonl(root / V1_SOURCE_REL, rows)
                        source_receipt_path = root / SOURCE_RECEIPT_REL
                        source_receipt = load_json(source_receipt_path)
                        source_receipt["artifacts"]["v1_candidates"] = binding(
                            root, V1_SOURCE_REL, 602
                        )
                        rewrite_json(source_receipt_path, source_receipt)
                        audit["source"]["v1_candidates"] = binding(
                            root, V1_SOURCE_REL, 602
                        )
                        audit["source"]["source_receipt"] = binding(
                            root, SOURCE_RECEIPT_REL
                        )
                    rewrite_json(audit_path, audit)
                    self.assert_rejected(root, "pinned input drift")


if __name__ == "__main__":
    unittest.main()
