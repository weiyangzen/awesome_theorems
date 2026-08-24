#!/usr/bin/env python3
"""Extract every ``conjectur`` field line in the pinned 622-entry OEIS subset.

This is the version-2 discovery profile for the independent OEIS candidate
source.  It deliberately preserves the narrower version-1 asset unchanged.
Within the same content-addressed archive it retains every ``%N``, ``%C``, or
``%F`` source field whose text contains the ASCII-case-insensitive literal stem
``conjectur``.  Possible resolution language is recorded only as a review hint;
it never removes a line.

The word ``all`` in this profile means all matches *within the pinned 622-entry
archive and three named fields*.  The archive is not a complete OEIS dump and
this layer makes no OEIS-wide completeness claim.  A source line is one
occurrence, regardless of how many times the stem appears.  A candidate is an
exact normalized-line group, not an atomic or semantically deduplicated
mathematical proposition.  Every row is review-only and grants no catalog or
strict-conjecture credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
V1_EXTRACTOR_PATH = Path(__file__).with_name("extract_oeis_conjectures_v5.py")

_V1_SPEC = importlib.util.spec_from_file_location(
    "awesome_theorems_oeis_conjectures_v5_v1", V1_EXTRACTOR_PATH
)
if _V1_SPEC is None or _V1_SPEC.loader is None:
    raise RuntimeError(f"cannot load version-1 extractor: {V1_EXTRACTOR_PATH}")
v1 = importlib.util.module_from_spec(_V1_SPEC)
sys.modules[_V1_SPEC.name] = v1
_V1_SPEC.loader.exec_module(v1)


DEFAULT_SOURCE_ARCHIVE = v1.DEFAULT_SOURCE_ARCHIVE
DEFAULT_V1_CANDIDATE_ASSET = v1.DEFAULT_CANDIDATE_ASSET
DEFAULT_CANDIDATE_ASSET = (
    REPO_ROOT
    / "Docs/catalog/v5/sources/"
    "oeis-conjectures-4c866362-all-conjectur-v2.jsonl"
)

SCHEMA_VERSION = (
    "awesome-theorems/oeis-all-conjectur-within-pinned-622-candidate/"
    "5.5-source-layer-v2"
)
SUMMARY_SCHEMA_VERSION = (
    "awesome-theorems/oeis-all-conjectur-within-pinned-622-summary/"
    "5.5-source-layer-v2"
)
EXTRACTOR_VERSION = "2.0.0"
DISCOVERY_PROFILE_ID = "oeis-pinned-622-ncf-all-conjectur-v2"
MAX_CANDIDATE_ASSET_BYTES = 16 * 1024 * 1024

SOURCE_ARCHIVE_SHA256 = v1.SOURCE_ARCHIVE_SHA256
SOURCE_ARCHIVE_SIZE_BYTES = v1.SOURCE_ARCHIVE_SIZE_BYTES
V1_CANDIDATE_ASSET_SHA256 = v1.CANDIDATE_ASSET_SHA256
V1_CANDIDATE_KEY_SET_SHA256 = v1.CANDIDATE_KEY_SET_SHA256

# Filled after deterministic generation.  Normal checking rejects zero locks.
CANDIDATE_ASSET_SHA256 = "18da1f5881f0410f2c38dc8362271b536db11c4509d58812942a11981181ec3d"
CANDIDATE_ASSET_SIZE_BYTES = 3_733_739
CANDIDATE_KEY_SET_SHA256 = (
    "5c28cb9863046900fe865aa76fddf2d1d65ef326dccea7c6f0ba28a11b30300a"
)

EXPECTED_SOURCE_LINE_OCCURRENCES = 1_141
EXPECTED_LITERAL_STEM_MATCHES = 1_304
EXPECTED_UNIQUE_CANDIDATES = 1_101
EXPECTED_ENTRIES_WITH_MATCHES = 611
EXPECTED_RAW_TEXT_UNIQUE = 1_104
EXPECTED_MULTI_OCCURRENCE_GROUPS = 23
EXPECTED_EXTRA_GROUPED_OCCURRENCES = 40
EXPECTED_POSSIBLE_RESOLUTION_LINES = 68
EXPECTED_LEGACY_NARROW_MARKER_LINES = 665
EXPECTED_V1_CANDIDATE_KEYS = 602
EXPECTED_KEY_INTERSECTION_WITH_V1 = 602
EXPECTED_V2_ONLY_KEYS = 499
EXPECTED_V1_ONLY_KEYS = 0
EXPECTED_FIELD_COUNTS = {"%C": 875, "%F": 220, "%N": 46}
EXPECTED_WORD_FORM_COUNTS = {
    "conjectural": 17,
    "conjecturally": 16,
    "conjecture": 849,
    "conjectured": 372,
    "conjectures": 50,
}

DISCOVERY_RE = re.compile(r"conjectur", re.IGNORECASE | re.ASCII)
WORD_FORM_RE = re.compile(r"\bconjectur[a-z]*\b", re.IGNORECASE | re.ASCII)
POSSIBLE_UNRESOLVED_LANGUAGE_RE = re.compile(
    r"\b(?:unproved|unproven|open|unknown|unresolved|unsolved)\b|"
    r"\b(?:not|never)\b(?:\W+\w+){0,3}\W+\bproved\b",
    re.IGNORECASE | re.ASCII,
)


class ExtractionError(RuntimeError):
    """The v2 discovery contract, replay bytes, or pinned inputs drifted."""


@dataclass(frozen=True)
class ExtractionResult:
    candidates: tuple[dict[str, Any], ...]
    occurrences: tuple[dict[str, Any], ...]
    entries_with_matches: tuple[str, ...]
    summary: dict[str, Any]


def sha256_bytes(payload: bytes) -> str:
    return v1.sha256_bytes(payload)


def canonical_json_bytes(value: Any) -> bytes:
    return v1.canonical_json_bytes(value)


def canonical_json_line(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def encode_candidates(candidates: Iterable[Mapping[str, Any]]) -> bytes:
    return b"".join(canonical_json_line(row) for row in candidates)


def _require_equal(observed: Any, expected: Any, label: str) -> None:
    if observed != expected:
        raise ExtractionError(f"{label} is {observed!r}, expected {expected!r}")


def _require_sealed() -> None:
    if CANDIDATE_ASSET_SIZE_BYTES <= 0 or CANDIDATE_ASSET_SHA256 == "0" * 64:
        raise ExtractionError("v2 candidate asset locks have not been sealed")


def load_source_archive(path: Path = DEFAULT_SOURCE_ARCHIVE) -> Any:
    """Load the shared source with all version-1 byte/canonical locks enabled."""

    try:
        bundle = v1.load_source_archive(path)
    except v1.ExtractionError as error:
        raise ExtractionError(f"pinned source rejected: {error}") from error
    _require_equal(bundle.archive_sha256, SOURCE_ARCHIVE_SHA256, "source SHA-256")
    _require_equal(bundle.archive_size_bytes, SOURCE_ARCHIVE_SIZE_BYTES, "source size")
    return bundle


def load_v1_candidate_rows(path: Path = DEFAULT_V1_CANDIDATE_ASSET) -> list[dict[str, Any]]:
    """Load the sealed narrow-profile rows used for exact key comparison."""

    try:
        rows = v1.load_candidate_asset(path)
    except v1.ExtractionError as error:
        raise ExtractionError(f"version-1 candidate asset rejected: {error}") from error
    keys = [row.get("candidate_key") for row in rows]
    _require_equal(len(keys), EXPECTED_V1_CANDIDATE_KEYS, "version-1 key count")
    _require_equal(len(set(keys)), len(keys), "version-1 unique key count")
    _require_equal(
        sha256_bytes(canonical_json_bytes(sorted(keys))),
        V1_CANDIDATE_KEY_SET_SHA256,
        "version-1 key-set SHA-256",
    )
    return rows


def _location(entry: Any, field: Any) -> dict[str, Any]:
    possible_resolution = v1.RESOLUTION_QUARANTINE_RE.search(field.text) is not None
    possible_unresolved = (
        POSSIBLE_UNRESOLVED_LANGUAGE_RE.search(field.text) is not None
    )
    return {
        "a_number": entry.a_number,
        "blob_sha1": entry.blob_sha1,
        "entry_url": f"https://oeis.org/{entry.a_number}",
        "field": field.field,
        "file_sha256": entry.file_sha256,
        "legacy_v1_discovery": {
            "narrow_marker_matched": v1.MARKER_RE.search(field.text) is not None,
            "resolution_term_matched": possible_resolution,
        },
        "line_number": field.line_number,
        "literal_stem_match_count": len(DISCOVERY_RE.findall(field.text)),
        "original_text": field.text,
        "path": entry.path,
        "raw_commit_url": (
            "https://raw.githubusercontent.com/oeis/oeisdata/"
            f"{v1.PINNED_COMMIT}/{entry.path}"
        ),
        "review_hints": {
            "hints_are_non_dispositive": True,
            "hints_are_nonexhaustive": True,
            "possible_resolution_language": possible_resolution,
            "possible_unresolved_language": possible_unresolved,
            "retained_regardless_of_hints": True,
        },
    }


def extract_candidates(
    bundle: Any,
    v1_rows: Sequence[Mapping[str, Any]],
) -> ExtractionResult:
    """Extract every literal-stem source line without status-based filtering."""

    v1_keys = {str(row["candidate_key"]) for row in v1_rows}
    occurrences: list[dict[str, Any]] = []
    entries_with_matches: set[str] = set()
    field_counts: Counter[str] = Counter()
    word_forms: Counter[str] = Counter()
    raw_texts: set[str] = set()

    for entry in bundle.entries:
        for field in entry.fields:
            if field.field not in {"%N", "%C", "%F"}:
                continue
            if DISCOVERY_RE.search(field.text) is None:
                continue
            location = _location(entry, field)
            normalized = v1.normalize_candidate_text(field.text)
            if not normalized:
                raise ExtractionError(
                    f"{entry.path}:{field.line_number}: empty normalized candidate"
                )
            entries_with_matches.add(entry.a_number)
            field_counts[field.field] += 1
            raw_texts.add(field.text)
            word_forms.update(
                match.group(0).lower() for match in WORD_FORM_RE.finditer(field.text)
            )
            occurrences.append(
                {
                    **location,
                    "normalized_text": normalized,
                    "normalized_text_sha256": sha256_bytes(
                        normalized.encode("utf-8")
                    ),
                }
            )

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for occurrence in occurrences:
        groups[occurrence["normalized_text"]].append(occurrence)

    candidates: list[dict[str, Any]] = []
    for normalized, group in sorted(groups.items()):
        locations = sorted(
            (
                {
                    key: value
                    for key, value in occurrence.items()
                    if key not in {"normalized_text", "normalized_text_sha256"}
                }
                for occurrence in group
            ),
            key=lambda row: (
                row["a_number"],
                row["field"],
                row["line_number"],
                row["original_text"],
            ),
        )
        normalized_sha = sha256_bytes(normalized.encode("utf-8"))
        candidate_key = f"oeis-normalized/{normalized_sha}"
        candidates.append(
            {
                "a_number_count": len({row["a_number"] for row in locations}),
                "candidate_key": candidate_key,
                "candidate_only": True,
                "candidate_type": "literal_conjectur_field_line_group",
                "dedupe_boundary": {
                    "exact_normalized_text_grouped": True,
                    "normalization_can_merge_distinct_raw_lines": True,
                    "normalized_key_is_not_semantic_identity": True,
                    "semantic_deduplication_performed": False,
                },
                "discovery_boundary": {
                    "archive_population_is_not_oeis_complete": True,
                    "fields": ["%C", "%F", "%N"],
                    "literal_ascii_case_insensitive_stem": "conjectur",
                    "scan_complete_within_pinned_archive_and_fields": True,
                    "source_line_is_occurrence_unit": True,
                    "source_subset_selection_completeness_proven": False,
                },
                "discovery_profile_id": DISCOVERY_PROFILE_ID,
                "grants_catalog_entry": False,
                "grants_strict_conjecture_credit": False,
                "legacy_narrow_v1": {
                    "candidate_asset_sha256": V1_CANDIDATE_ASSET_SHA256,
                    "candidate_key_present": candidate_key in v1_keys,
                },
                "license_spdx": v1.LICENSE_SPDX,
                "locations": locations,
                "normalized_text": normalized,
                "normalized_text_sha256": normalized_sha,
                "occurrence_count": len(locations),
                "review_hint_location_counts": {
                    "possible_resolution_language": sum(
                        bool(row["review_hints"]["possible_resolution_language"])
                        for row in locations
                    ),
                    "possible_unresolved_language": sum(
                        bool(row["review_hints"]["possible_unresolved_language"])
                        for row in locations
                    ),
                },
                "schema_version": SCHEMA_VERSION,
                "source": {
                    "archive_sha256": SOURCE_ARCHIVE_SHA256,
                    "commit": v1.PINNED_COMMIT,
                    "commit_timestamp": v1.PINNED_COMMIT_TIMESTAMP,
                    "export_time": v1.PINNED_EXPORT_TIME,
                    "license_evidence_blob_sha1": v1.README_BLOB_SHA1,
                    "license_evidence_path": v1.README_PATH,
                    "license_evidence_sha256": v1.README_SHA256,
                    "repository_url": v1.SOURCE_REPOSITORY,
                    "source_id": v1.SOURCE_ID,
                    "tree_sha1": v1.PINNED_TREE_SHA1,
                },
                "status_boundary": {
                    "atomicity_status": "not_independently_reviewed",
                    "current_open_status": "not_independently_reviewed",
                    "importance_or_frontier_status": "not_independently_reviewed",
                    "literal_marker_is_not_status_evidence": True,
                    "review_hints_are_nonexhaustive": True,
                    "review_hints_are_not_status_evidence": True,
                },
            }
        )

    _require_equal(
        len(occurrences),
        EXPECTED_SOURCE_LINE_OCCURRENCES,
        "source-line occurrence count",
    )
    _require_equal(
        sum(row["literal_stem_match_count"] for row in occurrences),
        EXPECTED_LITERAL_STEM_MATCHES,
        "literal-stem match count",
    )
    _require_equal(len(candidates), EXPECTED_UNIQUE_CANDIDATES, "candidate count")
    _require_equal(
        len(entries_with_matches),
        EXPECTED_ENTRIES_WITH_MATCHES,
        "entries-with-matches count",
    )
    _require_equal(len(raw_texts), EXPECTED_RAW_TEXT_UNIQUE, "raw-text unique count")
    _require_equal(dict(sorted(field_counts.items())), EXPECTED_FIELD_COUNTS, "field counts")
    _require_equal(dict(sorted(word_forms.items())), EXPECTED_WORD_FORM_COUNTS, "word forms")

    possible_resolution_lines = sum(
        bool(row["review_hints"]["possible_resolution_language"])
        for row in occurrences
    )
    _require_equal(
        possible_resolution_lines,
        EXPECTED_POSSIBLE_RESOLUTION_LINES,
        "possible-resolution line count",
    )
    legacy_narrow_lines = sum(
        bool(row["legacy_v1_discovery"]["narrow_marker_matched"])
        for row in occurrences
    )
    _require_equal(
        legacy_narrow_lines,
        EXPECTED_LEGACY_NARROW_MARKER_LINES,
        "legacy narrow-marker line count",
    )

    group_sizes = Counter(len(group) for group in groups.values())
    multi_groups = sum(count for size, count in group_sizes.items() if size > 1)
    grouped_extras = sum((size - 1) * count for size, count in group_sizes.items())
    _require_equal(
        multi_groups, EXPECTED_MULTI_OCCURRENCE_GROUPS, "multi-occurrence group count"
    )
    _require_equal(
        grouped_extras,
        EXPECTED_EXTRA_GROUPED_OCCURRENCES,
        "extra grouped-occurrence count",
    )

    candidate_keys = {row["candidate_key"] for row in candidates}
    _require_equal(len(candidate_keys), len(candidates), "unique candidate-key count")
    key_set_sha = sha256_bytes(canonical_json_bytes(sorted(candidate_keys)))
    _require_equal(key_set_sha, CANDIDATE_KEY_SET_SHA256, "candidate-key set SHA-256")
    intersection = candidate_keys & v1_keys
    v2_only = candidate_keys - v1_keys
    v1_only = v1_keys - candidate_keys
    _require_equal(
        len(intersection),
        EXPECTED_KEY_INTERSECTION_WITH_V1,
        "key intersection with version 1",
    )
    _require_equal(len(v2_only), EXPECTED_V2_ONLY_KEYS, "version-2-only key count")
    _require_equal(len(v1_only), EXPECTED_V1_ONLY_KEYS, "version-1-only key count")

    encoded = encode_candidates(candidates)
    summary = {
        "candidate_asset_sha256": sha256_bytes(encoded),
        "candidate_key_set_sha256": key_set_sha,
        "counts": {
            "entries_with_matches": len(entries_with_matches),
            "extra_grouped_occurrences": grouped_extras,
            "field_occurrences": dict(sorted(field_counts.items())),
            "legacy_narrow_marker_lines": legacy_narrow_lines,
            "literal_stem_matches": sum(
                row["literal_stem_match_count"] for row in occurrences
            ),
            "multi_occurrence_groups": multi_groups,
            "possible_resolution_language_lines_retained": possible_resolution_lines,
            "raw_text_unique": len(raw_texts),
            "source_line_occurrences": len(occurrences),
            "unique_normalized_candidates": len(candidates),
            "word_forms": dict(sorted(word_forms.items())),
        },
        "discovery_boundary": {
            "archive_population_is_not_oeis_complete": True,
            "fields": ["%C", "%F", "%N"],
            "literal_ascii_case_insensitive_stem": "conjectur",
            "scan_complete_within_pinned_archive_and_fields": True,
            "source_line_is_occurrence_unit": True,
            "source_subset_selection_completeness_proven": False,
        },
        "discovery_profile_id": DISCOVERY_PROFILE_ID,
        "extractor_version": EXTRACTOR_VERSION,
        "legacy_narrow_v1_comparison": {
            "intersection_candidate_keys": len(intersection),
            "v1_candidate_asset_sha256": V1_CANDIDATE_ASSET_SHA256,
            "v1_candidate_keys": len(v1_keys),
            "v1_key_set_sha256": V1_CANDIDATE_KEY_SET_SHA256,
            "v1_only_candidate_keys": len(v1_only),
            "v2_candidate_keys": len(candidate_keys),
            "v2_only_candidate_keys": len(v2_only),
        },
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "source": {
            "archive_sha256": bundle.archive_sha256,
            "archive_size_bytes": bundle.archive_size_bytes,
            "commit": v1.PINNED_COMMIT,
            "commit_timestamp": v1.PINNED_COMMIT_TIMESTAMP,
            "export_time": v1.PINNED_EXPORT_TIME,
            "inventory_sha256": bundle.inventory_sha256,
            "license_spdx": v1.LICENSE_SPDX,
            "path_set_sha256": bundle.path_set_sha256,
            "repository_url": v1.SOURCE_REPOSITORY,
            "source_id": v1.SOURCE_ID,
            "tree_sha1": v1.PINNED_TREE_SHA1,
            "uncompressed_size_bytes": bundle.uncompressed_size_bytes,
        },
        "status_boundary": {
            "candidate_asset_grants_catalog_entry": False,
            "candidate_asset_grants_strict_conjecture_credit": False,
            "current_open_status_independently_reviewed": False,
            "importance_independently_reviewed": False,
            "possible_resolution_language_is_non_dispositive": True,
            "semantic_deduplication_performed": False,
        },
    }
    return ExtractionResult(
        candidates=tuple(candidates),
        occurrences=tuple(occurrences),
        entries_with_matches=tuple(sorted(entries_with_matches)),
        summary=summary,
    )


def _parse_candidate_payload(payload: bytes) -> list[dict[str, Any]]:
    if not payload.endswith(b"\n"):
        raise ExtractionError("candidate JSONL lacks one final LF")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(payload.splitlines(), start=1):
        try:
            row = json.loads(line)
        except (UnicodeError, json.JSONDecodeError) as error:
            raise ExtractionError(
                f"candidate line {line_number} is invalid JSON: {error}"
            ) from error
        if not isinstance(row, dict):
            raise ExtractionError(f"candidate line {line_number} is not an object")
        rows.append(row)
    _require_equal(len(rows), EXPECTED_UNIQUE_CANDIDATES, "candidate JSONL row count")
    if encode_candidates(rows) != payload:
        raise ExtractionError("candidate JSONL bytes are not canonical")
    return rows


def load_candidate_asset(
    path: Path,
    *,
    bundle: Any,
    v1_rows: Sequence[Mapping[str, Any]],
    enforce_asset_lock: bool = True,
) -> list[dict[str, Any]]:
    if enforce_asset_lock:
        _require_sealed()
    try:
        payload = v1._read_bounded_file(
            path,
            label="OEIS v2 candidate asset",
            max_bytes=MAX_CANDIDATE_ASSET_BYTES,
            expected_size=(CANDIDATE_ASSET_SIZE_BYTES if enforce_asset_lock else None),
        )
    except v1.ExtractionError as error:
        raise ExtractionError(str(error)) from error
    if enforce_asset_lock:
        _require_equal(
            sha256_bytes(payload), CANDIDATE_ASSET_SHA256, "candidate asset SHA-256"
        )
    rows = _parse_candidate_payload(payload)
    expected = extract_candidates(bundle, v1_rows)
    if rows != list(expected.candidates):
        raise ExtractionError("candidate rows do not replay from the pinned source")
    return rows


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        temporary.write_bytes(payload)
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def check_assets(source: Path, v1_asset: Path, candidates: Path) -> ExtractionResult:
    bundle = load_source_archive(source)
    v1_rows = load_v1_candidate_rows(v1_asset)
    result = extract_candidates(bundle, v1_rows)
    load_candidate_asset(candidates, bundle=bundle, v1_rows=v1_rows)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE_ARCHIVE)
    parser.add_argument("--v1-candidates", type=Path, default=DEFAULT_V1_CANDIDATE_ASSET)
    parser.add_argument("--output", type=Path, default=DEFAULT_CANDIDATE_ASSET)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)

    if args.check:
        if args.summary_only:
            raise ExtractionError("--check and --summary-only are mutually exclusive")
        result = check_assets(args.source, args.v1_candidates, args.output)
        print(
            "PASS extract_oeis_conjectures_v5_v2 "
            f"occurrences={EXPECTED_SOURCE_LINE_OCCURRENCES} "
            f"candidates={EXPECTED_UNIQUE_CANDIDATES} "
            f"v1_intersection={EXPECTED_KEY_INTERSECTION_WITH_V1} "
            f"v2_only={EXPECTED_V2_ONLY_KEYS}"
        )
        return 0

    bundle = load_source_archive(args.source)
    v1_rows = load_v1_candidate_rows(args.v1_candidates)
    result = extract_candidates(bundle, v1_rows)
    if args.summary_only:
        print(canonical_json_bytes(result.summary).decode("utf-8"))
        return 0
    payload = encode_candidates(result.candidates)
    _atomic_write(args.output, payload)
    print(
        "PASS extract_oeis_conjectures_v5_v2 write "
        f"occurrences={EXPECTED_SOURCE_LINE_OCCURRENCES} "
        f"candidates={EXPECTED_UNIQUE_CANDIDATES} "
        f"sha256={sha256_bytes(payload)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ExtractionError, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL extract_oeis_conjectures_v5_v2: {error}", file=sys.stderr)
        raise SystemExit(1)
