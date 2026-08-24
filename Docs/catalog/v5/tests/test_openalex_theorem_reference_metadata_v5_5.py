#!/usr/bin/env python3
"""Black-box and deep-mutation tests for the independent OpenAlex checker."""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from typing import Any, Callable, Mapping


REPO_ROOT = Path(__file__).resolve().parents[4]
CHECKER_REL = Path("Docs/catalog/v5/tools/check_openalex_theorem_reference_metadata_v5_5.py")
INPUT_REL = Path("Docs/catalog/v5/curation/Thousand_Plus_Reference_Candidates_v5_5.json")
METADATA_REL = Path("Docs/catalog/v5/sources/openalex-thousand-plus-doi-metadata-20260810.json.gz")
ORIGINAL_METADATA_SHA = "e3d490619eac4e16bdf24478c74de2024d32d3ec0d603f3ac4a102ad4c206486"
ORIGINAL_AUTHORITY = "4a6abb7d9f22dbca688eed164116b429beacb15a643465bf424f41d0e0e3f565"


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
    ignored = set(fields)
    return digest(canonical({key: item for key, item in value.items() if key not in ignored}))


def set_digest(values: list[str]) -> str:
    return digest(canonical(sorted(values)))


def tree_digest(root: Path) -> str:
    rows = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        rows.append((path.relative_to(root).as_posix(), digest(path.read_bytes())))
    return digest(canonical(rows))


class OpenAlexMetadataAuditTests(unittest.TestCase):
    def make_mirror(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="openalex-audit-")
        root = Path(temporary.name) / "mirror"
        for relative in (CHECKER_REL, INPUT_REL, METADATA_REL):
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO_ROOT / relative, destination)
        return temporary, root

    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        foreign_cwd = root.parent / "foreign-cwd"
        foreign_cwd.mkdir(exist_ok=True)
        return subprocess.run(
            [sys.executable, str(root / CHECKER_REL), "--repo-root", str(root)],
            cwd=foreign_cwd,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )

    def mutate_and_reseal(self, root: Path, mutation: Callable[[dict[str, Any]], None], *, mtime: int = 0) -> None:
        metadata_path = root / METADATA_REL
        with gzip.open(metadata_path, "rt", encoding="utf-8") as stream:
            document = json.load(stream)
        mutation(document)
        document["set_digests"]["row_sha256_set_sha256"] = set_digest(
            [record["row_sha256"] for record in document["records"]]
        )
        document["authority_sha256"] = hash_without(document, "authority_sha256")
        payload = canonical(document) + b"\n"
        with metadata_path.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=mtime, compresslevel=9) as stream:
                stream.write(payload)
        new_metadata_sha = digest(metadata_path.read_bytes())
        checker_path = root / CHECKER_REL
        checker = checker_path.read_text(encoding="utf-8")
        checker = checker.replace(ORIGINAL_METADATA_SHA, new_metadata_sha)
        checker = checker.replace(ORIGINAL_AUTHORITY, document["authority_sha256"])
        checker_path.write_text(checker, encoding="utf-8")

    def assert_semantic_failure(self, result: subprocess.CompletedProcess[str], fragment: str) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        combined = result.stdout + result.stderr
        self.assertIn(fragment, combined)
        self.assertNotIn("Traceback", combined)

    def test_pristine_mirror_passes_from_foreign_cwd_and_is_read_only(self) -> None:
        temporary, root = self.make_mirror()
        self.addCleanup(temporary.cleanup)
        before = tree_digest(root)
        result = self.run_checker(root)
        after = tree_digest(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("resolved=2618 ambiguous=23 missing=14 quality_credit=0", result.stdout)
        self.assertEqual(before, after)

    def test_resealed_count_type_confusion_is_rejected(self) -> None:
        temporary, root = self.make_mirror()
        self.addCleanup(temporary.cleanup)

        def mutation(document: dict[str, Any]) -> None:
            document["counts"]["quality_credits"] = False

        self.mutate_and_reseal(root, mutation)
        self.assert_semantic_failure(self.run_checker(root), "counts.quality_credits must be integer 0")

    def test_resealed_ambiguous_match_with_wrong_doi_is_rejected(self) -> None:
        temporary, root = self.make_mirror()
        self.addCleanup(temporary.cleanup)

        def mutation(document: dict[str, Any]) -> None:
            record = next(item for item in document["records"] if item.get("ambiguous") is True)
            match = record["matches"][0]
            match["normalized_doi"] = "10.0000/not-the-parent-doi"
            match["row_sha256"] = hash_without(match, "row_sha256")
            record["row_sha256"] = hash_without(record, "row_sha256")

        self.mutate_and_reseal(root, mutation)
        self.assert_semantic_failure(self.run_checker(root), "DOI mismatch")

    def test_resealed_quality_credit_escalation_is_rejected(self) -> None:
        temporary, root = self.make_mirror()
        self.addCleanup(temporary.cleanup)

        def mutation(document: dict[str, Any]) -> None:
            record = next(item for item in document["records"] if isinstance(item.get("openalex_id"), str))
            record["evidence_boundary"]["quality_credit_granted"] = True
            record["row_sha256"] = hash_without(record, "row_sha256")

        self.mutate_and_reseal(root, mutation)
        self.assert_semantic_failure(self.run_checker(root), "evidence boundary drifted")

    def test_resealed_nonzero_gzip_mtime_is_rejected(self) -> None:
        temporary, root = self.make_mirror()
        self.addCleanup(temporary.cleanup)
        self.mutate_and_reseal(root, lambda document: None, mtime=1)
        self.assert_semantic_failure(self.run_checker(root), "gzip mtime must be zero")


if __name__ == "__main__":
    unittest.main()
