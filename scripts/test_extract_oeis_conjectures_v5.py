#!/usr/bin/env python3
"""Regression tests for the review-only OEIS conjecture candidate source."""

from __future__ import annotations

import gzip
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
EXTRACTOR_PATH = ROOT / "Docs/tools/extract_oeis_conjectures_v5.py"

SPEC = importlib.util.spec_from_file_location(
    "extract_oeis_conjectures_v5", EXTRACTOR_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load extractor at {EXTRACTOR_PATH}")
extractor = importlib.util.module_from_spec(SPEC)
# Dataclasses resolve annotations through sys.modules during module execution.
sys.modules[SPEC.name] = extractor
SPEC.loader.exec_module(extractor)


def encode_test_archive(
    files: dict[str, bytes],
    *,
    pax_headers: dict[str, str] | None = None,
    renamed: dict[str, str] | None = None,
    member_types: dict[str, bytes] | None = None,
    member_pax_headers: dict[str, dict[str, str]] | None = None,
    global_pax_before: tuple[str, dict[str, str]] | None = None,
    gzip_mtime: int = 0,
    member_mtime: int = 0,
) -> bytes:
    """Build a test tar while retaining the extractor's exact member count."""

    renamed = renamed or {}
    member_types = member_types or {}
    member_pax_headers = member_pax_headers or {}
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", compresslevel=9, fileobj=output, mtime=gzip_mtime
    ) as compressed:
        with tarfile.open(
            fileobj=compressed,
            mode="w",
            format=tarfile.PAX_FORMAT,
            pax_headers=(
                dict(extractor.PAX_HEADERS)
                if pax_headers is None
                else dict(pax_headers)
            ),
        ) as archive:
            for relative in sorted(files):
                if global_pax_before is not None and relative == global_pax_before[0]:
                    pax_payload = encode_pax_records(global_pax_before[1])
                    pax_member = tarfile.TarInfo("pax_global_header")
                    pax_member.type = tarfile.XGLTYPE
                    pax_member.size = len(pax_payload)
                    archive.addfile(pax_member, io.BytesIO(pax_payload))
                archive_name = renamed.get(
                    relative, f"{extractor.ARCHIVE_ROOT}/{relative}"
                )
                info = tarfile.TarInfo(archive_name)
                info.mode = 0o444
                info.mtime = member_mtime
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                info.pax_headers = dict(member_pax_headers.get(relative, {}))
                requested_type = member_types.get(relative)
                if requested_type is not None:
                    info.type = requested_type
                    info.linkname = "README.md"
                    info.size = 0
                    archive.addfile(info)
                    continue
                payload = files[relative]
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
    return output.getvalue()


def encode_pax_records(headers: dict[str, str]) -> bytes:
    records: list[bytes] = []
    for key, value in headers.items():
        body = f"{key}={value}\n".encode("utf-8")
        length = len(body) + 2
        while True:
            record = str(length).encode("ascii") + b" " + body
            if len(record) == length:
                records.append(record)
                break
            length = len(record)
    return b"".join(records)


class ExtractOeisConjecturesV5Tests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.archive_bytes = extractor.DEFAULT_SOURCE_ARCHIVE.read_bytes()
        cls.candidate_bytes = extractor.DEFAULT_CANDIDATE_ASSET.read_bytes()
        cls.bundle = extractor.load_source_archive(extractor.DEFAULT_SOURCE_ARCHIVE)
        cls.result = extractor.extract_candidates(cls.bundle)
        cls.rows = extractor.load_candidate_asset(extractor.DEFAULT_CANDIDATE_ASSET)
        cls.files = dict(cls.bundle.files)

    def temporary_bytes(self, payload: bytes, name: str) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / name
        path.write_bytes(payload)
        return path

    def assert_archive_rejected(
        self,
        payload: bytes,
        message: str,
        *,
        enforce_canonical_bytes: bool = False,
    ) -> None:
        path = self.temporary_bytes(payload, "source.tar.gz")
        with self.assertRaisesRegex(extractor.ExtractionError, message):
            extractor.load_source_archive(
                path,
                enforce_asset_lock=False,
                enforce_inventory_lock=False,
                enforce_canonical_bytes=enforce_canonical_bytes,
            )

    def test_vendored_asset_digests_sizes_and_cardinality(self) -> None:
        self.assertEqual(len(self.archive_bytes), extractor.SOURCE_ARCHIVE_SIZE_BYTES)
        self.assertEqual(
            extractor.sha256_bytes(self.archive_bytes),
            "85ac265ad3c7ab294a18a3874e33a139fa9afdba8b6dfba86ea03aefd7ab3a1e",
        )
        self.assertEqual(
            len(self.candidate_bytes), extractor.CANDIDATE_ASSET_SIZE_BYTES
        )
        self.assertEqual(
            extractor.sha256_bytes(self.candidate_bytes),
            "7b426d78bcbd05389e129553ba2030690fd5b5309666a9819db0c6f9ae1cf3b3",
        )
        self.assertEqual(len(self.rows), 602)

    def test_pinned_source_provenance_inventory_and_license(self) -> None:
        self.assertEqual(len(self.bundle.files), 624)
        self.assertEqual(len(self.bundle.entries), 622)
        self.assertEqual(
            self.bundle.archive_sha256, extractor.SOURCE_ARCHIVE_SHA256
        )
        self.assertEqual(
            self.bundle.uncompressed_size_bytes,
            extractor.SOURCE_UNCOMPRESSED_SIZE_BYTES,
        )
        self.assertEqual(
            self.bundle.inventory_sha256, extractor.SOURCE_INVENTORY_SHA256
        )
        self.assertEqual(
            self.bundle.path_set_sha256, extractor.SOURCE_PATH_SET_SHA256
        )
        self.assertIn(
            extractor.LICENSE_NAME,
            self.bundle.files[extractor.README_PATH].decode("utf-8"),
        )
        self.assertEqual(
            self.bundle.files[extractor.TIME_PATH].decode("utf-8").strip(),
            extractor.PINNED_EXPORT_TIME,
        )

    def test_extraction_counts_are_exact_and_noninflating(self) -> None:
        counts = self.result.summary["counts"]
        self.assertEqual(
            counts,
            {
                "candidate_occurrences": 626,
                "entries_with_candidates": 541,
                "marker_lines": 665,
                "resolution_quarantined": 39,
                "source_regular_files": 624,
                "source_sequence_entries": 622,
                "unique_candidates": 602,
            },
        )
        self.assertEqual(len(self.result.occurrences), 626)
        self.assertEqual(len(self.result.quarantined), 39)
        self.assertEqual(len(self.result.entries_with_candidates), 541)
        self.assertEqual(len(self.result.candidates), 602)

    def test_candidate_rows_are_canonical_ordered_and_unique(self) -> None:
        self.assertEqual(
            self.candidate_bytes, extractor.encode_candidates(self.result.candidates)
        )
        self.assertEqual(self.rows, list(self.result.candidates))
        normalized = [row["normalized_text"] for row in self.rows]
        keys = [row["candidate_key"] for row in self.rows]
        self.assertEqual(normalized, sorted(normalized))
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(
            extractor.sha256_bytes(
                extractor.canonical_json_bytes(sorted(keys))
            ),
            extractor.CANDIDATE_KEY_SET_SHA256,
        )
        for raw_line, row in zip(self.candidate_bytes.splitlines(keepends=True), self.rows):
            self.assertEqual(raw_line, extractor.canonical_json_line(row))

    def test_candidates_are_locations_only_and_never_grant_credit(self) -> None:
        occurrences = 0
        a_numbers: set[str] = set()
        for row in self.rows:
            self.assertIs(row["candidate_only"], True)
            self.assertIs(row["grants_catalog_entry"], False)
            self.assertIs(row["grants_strict_conjecture_credit"], False)
            self.assertIs(
                row["dedupe_boundary"]["semantic_deduplication_performed"],
                False,
            )
            self.assertEqual(
                row["status_boundary"]["current_open_status"],
                "not_independently_reviewed",
            )
            self.assertEqual(row["occurrence_count"], len(row["locations"]))
            self.assertEqual(
                row["a_number_count"],
                len({location["a_number"] for location in row["locations"]}),
            )
            for location in row["locations"]:
                self.assertIn(location["field"], {"%N", "%C", "%F"})
                self.assertEqual(
                    extractor.normalize_candidate_text(location["original_text"]),
                    row["normalized_text"],
                )
                a_numbers.add(location["a_number"])
                occurrences += 1
        self.assertEqual(occurrences, 626)
        self.assertEqual(len(a_numbers), 541)
        self.assertIs(
            self.result.summary["status_boundary"][
                "candidate_asset_grants_strict_conjecture_credit"
            ],
            False,
        )

    def test_cli_check_and_summary_replay_the_vendored_assets(self) -> None:
        checked = subprocess.run(
            [sys.executable, str(EXTRACTOR_PATH), "--check"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            checked.stdout.strip(),
            "PASS extract_oeis_conjectures_v5 source=622 occurrences=626 candidates=602",
        )
        summary = subprocess.run(
            [sys.executable, str(EXTRACTOR_PATH), "--summary-only"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(json.loads(summary.stdout), self.result.summary)

    def test_archive_byte_tampering_is_rejected_by_the_asset_lock(self) -> None:
        tampered = bytearray(self.archive_bytes)
        tampered[-9] ^= 1
        path = self.temporary_bytes(bytes(tampered), "tampered.tar.gz")
        with self.assertRaisesRegex(extractor.ExtractionError, "archive SHA-256"):
            extractor.load_source_archive(path)

    def test_unsafe_traversal_and_absolute_tar_paths_are_rejected(self) -> None:
        relative = sorted(self.files)[0]
        traversal = encode_test_archive(
            self.files,
            renamed={relative: f"{extractor.ARCHIVE_ROOT}/../escape"},
        )
        self.assert_archive_rejected(traversal, "unsafe tar member path")

        absolute = encode_test_archive(
            self.files,
            renamed={relative: "/absolute/escape"},
        )
        self.assert_archive_rejected(absolute, "unsafe tar member path")

    def test_raw_double_slash_dot_segment_and_trailing_slash_are_rejected(self) -> None:
        relative = sorted(self.files)[0]
        unsafe_names = {
            "double_slash": f"{extractor.ARCHIVE_ROOT}//{relative}",
            "dot_segment": f"{extractor.ARCHIVE_ROOT}/./{relative}",
            "trailing_slash": f"{extractor.ARCHIVE_ROOT}/{relative}/",
        }
        for label, unsafe_name in unsafe_names.items():
            with self.subTest(label=label):
                archive = encode_test_archive(
                    self.files, renamed={relative: unsafe_name}
                )
                self.assert_archive_rejected(archive, "unsafe tar member path")

    def test_symlink_hardlink_and_duplicate_members_are_rejected(self) -> None:
        relative = sorted(self.files)[0]
        symlink = encode_test_archive(
            self.files, member_types={relative: tarfile.SYMTYPE}
        )
        self.assert_archive_rejected(symlink, "not a regular file")

        hardlink = encode_test_archive(
            self.files, member_types={relative: tarfile.LNKTYPE}
        )
        self.assert_archive_rejected(hardlink, "not a regular file")

        first, last = sorted(self.files)[0], sorted(self.files)[-1]
        duplicate = encode_test_archive(
            self.files,
            renamed={last: f"{extractor.ARCHIVE_ROOT}/{first}"},
        )
        self.assert_archive_rejected(duplicate, "duplicate source tar member")

    def test_wrong_pax_commit_and_tree_are_rejected(self) -> None:
        for field in (
            "awesome-theorems.commit",
            "awesome-theorems.tree_sha1",
        ):
            with self.subTest(field=field):
                pax = dict(extractor.PAX_HEADERS)
                pax[field] = "0" * 40
                archive = encode_test_archive(self.files, pax_headers=pax)
                self.assert_archive_rejected(archive, "source PAX provenance")

    def test_member_and_midstream_global_pax_overrides_are_rejected(self) -> None:
        relative = sorted(self.files)[len(self.files) // 2]
        for field in (
            "awesome-theorems.commit",
            "awesome-theorems.tree_sha1",
        ):
            with self.subTest(kind="member", field=field):
                archive = encode_test_archive(
                    self.files,
                    member_pax_headers={relative: {field: "0" * 40}},
                )
                self.assert_archive_rejected(
                    archive, "source member PAX provenance override"
                )
            with self.subTest(kind="midstream_global", field=field):
                archive = encode_test_archive(
                    self.files,
                    global_pax_before=(relative, {field: "0" * 40}),
                )
                self.assert_archive_rejected(
                    archive, "source global PAX provenance"
                )

    def test_compressed_member_and_tar_stream_limits_are_preflighted(self) -> None:
        path = self.temporary_bytes(self.archive_bytes, "source.tar.gz")
        with mock.patch.object(
            extractor,
            "MAX_SOURCE_ARCHIVE_COMPRESSED_BYTES",
            len(self.archive_bytes) - 1,
        ):
            with self.assertRaisesRegex(
                extractor.ExtractionError, "compressed bytes|input limit"
            ):
                extractor.load_source_archive(
                    path,
                    enforce_asset_lock=False,
                    enforce_inventory_lock=False,
                    enforce_canonical_bytes=False,
                )

        relative = sorted(self.files)[0]
        files = dict(self.files)
        files[relative] = b"\0" * (extractor.MAX_MEMBER_BYTES + 1)
        archive = encode_test_archive(files)
        self.assert_archive_rejected(archive, "unsafe source member size")

        with mock.patch.object(extractor, "MAX_TAR_STREAM_BYTES", 1_024):
            with self.assertRaisesRegex(
                extractor.ExtractionError, "tar stream exceeds"
            ):
                extractor.load_source_archive(
                    path,
                    enforce_asset_lock=False,
                    enforce_inventory_lock=False,
                    enforce_canonical_bytes=False,
                )

    def test_cli_exposes_no_byte_lock_disable_switch(self) -> None:
        attempted = subprocess.run(
            [
                sys.executable,
                str(EXTRACTOR_PATH),
                "--check",
                "--no-asset-lock",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(attempted.returncode, 0)
        self.assertIn("unrecognized arguments", attempted.stderr)

    def test_wrong_readme_license_and_export_time_are_rejected(self) -> None:
        files = dict(self.files)
        files[extractor.README_PATH] = b"No reusable-content license here.\n"
        archive = encode_test_archive(files)
        with mock.patch.object(
            extractor,
            "README_SHA256",
            extractor.sha256_bytes(files[extractor.README_PATH]),
        ), mock.patch.object(
            extractor,
            "README_BLOB_SHA1",
            extractor.git_blob_sha1(files[extractor.README_PATH]),
        ):
            self.assert_archive_rejected(archive, "lacks the pinned .* license evidence")

        files = dict(self.files)
        files[extractor.TIME_PATH] = b"2026-08-10T03:00:15-04:00\n"
        archive = encode_test_archive(files)
        self.assert_archive_rejected(archive, "OEIS export timestamp")

    def test_wrong_embedded_identifier_and_directory_mapping_are_rejected(self) -> None:
        sequence_path = next(
            relative for relative in sorted(self.files) if relative.endswith(".seq")
        )
        a_number = Path(sequence_path).stem
        replacement = "A999999" if a_number != "A999999" else "A999998"
        files = dict(self.files)
        files[sequence_path] = files[sequence_path].replace(
            a_number.encode("ascii"), replacement.encode("ascii"), 1
        )
        archive = encode_test_archive(files)
        self.assert_archive_rejected(archive, "embedded identifier")

        wrong_directory = sequence_path.replace(
            f"seq/{a_number[:4]}/", "seq/A999/", 1
        )
        archive = encode_test_archive(
            self.files,
            renamed={sequence_path: f"{extractor.ARCHIVE_ROOT}/{wrong_directory}"},
        )
        self.assert_archive_rejected(archive, "directory/identifier mismatch")

    def test_noncanonical_source_archive_is_rejected(self) -> None:
        archive = encode_test_archive(self.files, member_mtime=1)
        self.assert_archive_rejected(
            archive, "source archive bytes are not canonical", enforce_canonical_bytes=True
        )

    def test_candidate_jsonl_tamper_noncanonical_bytes_and_missing_lf_fail(self) -> None:
        tampered_rows = list(self.rows)
        tampered_rows[0] = dict(tampered_rows[0])
        key = tampered_rows[0]["candidate_key"]
        tampered_rows[0]["candidate_key"] = key[:-1] + (
            "0" if key[-1] != "0" else "1"
        )
        tampered = extractor.encode_candidates(tampered_rows)
        path = self.temporary_bytes(tampered, "tampered.jsonl")
        with self.assertRaisesRegex(extractor.ExtractionError, "asset SHA-256"):
            extractor.load_candidate_asset(path)

        lines = self.candidate_bytes.splitlines()
        first = json.loads(lines[0])
        lines[0] = json.dumps(first, ensure_ascii=False).encode("utf-8")
        noncanonical = b"\n".join(lines) + b"\n"
        path = self.temporary_bytes(noncanonical, "noncanonical.jsonl")
        with self.assertRaisesRegex(extractor.ExtractionError, "not canonical"):
            extractor.load_candidate_asset(path, enforce_asset_lock=False)

        path = self.temporary_bytes(self.candidate_bytes[:-1], "missing-lf.jsonl")
        with self.assertRaisesRegex(extractor.ExtractionError, "lacks one final LF"):
            extractor.load_candidate_asset(path, enforce_asset_lock=False)

    def test_source_archive_builder_is_byte_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "source"
            for relative, payload in self.files.items():
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
            first = Path(temporary) / "first.tar.gz"
            second = Path(temporary) / "second.tar.gz"
            report_first = extractor.build_source_archive(root, first)
            report_second = extractor.build_source_archive(root, second)
            self.assertEqual(report_first, report_second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first.read_bytes(), self.archive_bytes)


if __name__ == "__main__":
    unittest.main()
