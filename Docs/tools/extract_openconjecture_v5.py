#!/usr/bin/env python3
"""Build the rights-safe OpenConjecture pool used by the Stage5 extension.

The upstream public JSONL contains both redistributable text and rows whose
text is withheld or governed by terms that this repository does not adopt.
This extractor therefore verifies one immutable upstream snapshot and emits
only rows which satisfy every frozen admission rule:

* the paper author used a conjecture environment (an invariant of the pinned
  OpenConjecture extractor), and the dataset labels it ``real_open_conjecture``;
* the model label confidence is at least 0.90;
* the exact conjecture body is present;
* the paper records CC-BY-4.0, with publication of the text allowed; and
* the upstream raw conjecture-block hash is unique.

The emitted pool is not itself a claim that the open status was independently
surveyed.  It preserves that status as a dated source/model assertion.  The
release generator applies its own deterministic ranking to this pool.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Sequence


SCHEMA_VERSION = "awesome-theorems/openconjecture-eligible-pool/5.2"
EXTRACTOR_VERSION = "1.0.0"

UPSTREAM_GITHUB_COMMIT = "d2e3afe62098611fabd7236998acc73f64e4b3b7"
UPSTREAM_HF_COMMIT = "fa03d85db95e6edad4ff751b490704fa8a0d9358"
UPSTREAM_SHA256 = "8cf0a7ce4baff47769fe1ca0c40b11eed0767480c858c208a7beae8f5829dd14"
UPSTREAM_SIZE_BYTES = 9_695_990
UPSTREAM_RECORDS = 4_415

EXPECTED_ELIGIBLE_BEFORE_DEDUPE = 931
EXPECTED_ELIGIBLE_AFTER_DEDUPE = 889
DEFAULT_RELEASE_SELECTION = 600

REQUIRED_LICENSE_URL = "http://creativecommons.org/licenses/by/4.0/"
REQUIRED_NORMALIZED_LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"
REQUIRED_LICENSE_FAMILY = "cc_by"
REQUIRED_LABEL = "real_open_conjecture"
REQUIRED_LABEL_MODEL = "gpt-5-mini"
REQUIRED_ASSESSMENT_VERSION = "gpt5mini-v5-open-exact-v1"
REQUIRED_PUBLICATION_POLICY = "hf-publication-v2"
MIN_LABEL_CONFIDENCE = 0.90

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ARXIV_VERSION_RE = re.compile(r"^(?P<base>[0-9]{4}\.[0-9]{4,5})v(?P<version>[1-9][0-9]*)$")


class ExtractionError(RuntimeError):
    """The pinned input or an admission invariant failed."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json_line(record: dict[str, Any]) -> bytes:
    return (
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _require_string(record: dict[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ExtractionError(f"record {record.get('id')!r} has invalid {field}")
    return value


def _require_number(record: dict[str, Any], field: str) -> float:
    value = record.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ExtractionError(f"record {record.get('id')!r} has invalid {field}")
    return float(value)


def validate_record(record: dict[str, Any], line_number: int) -> None:
    record_id = record.get("id")
    if isinstance(record_id, bool) or not isinstance(record_id, int) or record_id <= 0:
        raise ExtractionError(f"line {line_number}: invalid id")
    for field in (
        "arxiv_id",
        "title",
        "source_file",
        "source_url",
        "content_hash",
        "latest_label",
        "latest_label_model",
        "latest_assessment_version",
        "license_family",
        "publication_decision",
        "publication_policy_version",
    ):
        _require_string(record, field)
    for field in ("license_url", "normalized_license_url"):
        if not isinstance(record.get(field), str):
            raise ExtractionError(f"line {line_number}: invalid {field}")
    if not SHA256_RE.fullmatch(str(record["content_hash"])):
        raise ExtractionError(f"line {line_number}: invalid content_hash")
    if not isinstance(record.get("authors"), list) or not all(
        isinstance(value, str) and value.strip() for value in record["authors"]
    ):
        raise ExtractionError(f"line {line_number}: invalid authors")
    if not isinstance(record.get("categories"), list) or not all(
        isinstance(value, str) and value.strip() for value in record["categories"]
    ):
        raise ExtractionError(f"line {line_number}: invalid categories")
    for field in ("start_line", "end_line", "index_in_file"):
        value = record.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ExtractionError(f"line {line_number}: invalid {field}")
    if record["end_line"] < record["start_line"]:
        raise ExtractionError(f"line {line_number}: reversed source line range")
    _require_number(record, "latest_label_confidence")
    _require_number(record, "latest_interestingness_score")
    _require_number(record, "latest_interestingness_confidence")


def load_upstream(path: Path) -> list[dict[str, Any]]:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise ExtractionError(f"cannot read upstream snapshot: {error}") from error
    if len(payload) != UPSTREAM_SIZE_BYTES:
        raise ExtractionError(
            f"upstream size is {len(payload)}, expected {UPSTREAM_SIZE_BYTES}"
        )
    observed_sha = sha256_bytes(payload)
    if observed_sha != UPSTREAM_SHA256:
        raise ExtractionError(
            f"upstream SHA-256 is {observed_sha}, expected {UPSTREAM_SHA256}"
        )
    raw_lines = payload.splitlines()
    if len(raw_lines) != UPSTREAM_RECORDS:
        raise ExtractionError(
            f"upstream has {len(raw_lines)} records, expected {UPSTREAM_RECORDS}"
        )
    records: list[dict[str, Any]] = []
    seen_ids: set[int] = set()
    for line_number, raw_line in enumerate(raw_lines, start=1):
        try:
            value = json.loads(raw_line)
        except (UnicodeError, json.JSONDecodeError) as error:
            raise ExtractionError(f"line {line_number}: invalid JSON: {error}") from error
        if not isinstance(value, dict):
            raise ExtractionError(f"line {line_number}: record is not an object")
        validate_record(value, line_number)
        record_id = int(value["id"])
        if record_id in seen_ids:
            raise ExtractionError(f"line {line_number}: duplicate id {record_id}")
        seen_ids.add(record_id)
        records.append(value)
    return records


def is_eligible(record: dict[str, Any]) -> bool:
    return bool(
        record["latest_label"] == REQUIRED_LABEL
        and record["latest_label_model"] == REQUIRED_LABEL_MODEL
        and record["latest_assessment_version"] == REQUIRED_ASSESSMENT_VERSION
        and float(record["latest_label_confidence"]) >= MIN_LABEL_CONFIDENCE
        and isinstance(record.get("body_tex"), str)
        and record["body_tex"].strip()
        and record["license_url"] == REQUIRED_LICENSE_URL
        and record["normalized_license_url"] == REQUIRED_NORMALIZED_LICENSE_URL
        and record["license_family"] == REQUIRED_LICENSE_FAMILY
        and record["publication_decision"] == "publish_text"
        and record.get("publication_text_allowed") is True
        and record["publication_policy_version"] == REQUIRED_PUBLICATION_POLICY
        and record.get("text_withheld") is False
        # Unversioned arXiv URLs are moving locators.  They are useful for
        # discovery but cannot enter an immutable, independently replayable
        # release pool.
        and ARXIV_VERSION_RE.fullmatch(str(record["arxiv_id"])) is not None
        and str(record["source_url"]).endswith(str(record["arxiv_id"]))
    )


def arxiv_version_key(record: dict[str, Any]) -> tuple[str, int, str, int]:
    arxiv_id = str(record["arxiv_id"])
    match = ARXIV_VERSION_RE.fullmatch(arxiv_id)
    if match is None:
        # The fixed snapshot includes some legacy identifiers.  They remain
        # deterministic but lose to a normal versioned identifier on a hash tie.
        return (arxiv_id, 0, str(record.get("updated_at", "")), int(record["id"]))
    return (
        match.group("base"),
        int(match.group("version")),
        str(record.get("updated_at", "")),
        int(record["id"]),
    )


def build_pool(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    rights_and_status_eligible = [
        record
        for record in records
        if record["latest_label"] == REQUIRED_LABEL
        and record["latest_label_model"] == REQUIRED_LABEL_MODEL
        and record["latest_assessment_version"] == REQUIRED_ASSESSMENT_VERSION
        and float(record["latest_label_confidence"]) >= MIN_LABEL_CONFIDENCE
        and isinstance(record.get("body_tex"), str)
        and record["body_tex"].strip()
        and record["license_url"] == REQUIRED_LICENSE_URL
        and record["normalized_license_url"] == REQUIRED_NORMALIZED_LICENSE_URL
        and record["license_family"] == REQUIRED_LICENSE_FAMILY
        and record["publication_decision"] == "publish_text"
        and record.get("publication_text_allowed") is True
        and record["publication_policy_version"] == REQUIRED_PUBLICATION_POLICY
        and record.get("text_withheld") is False
    ]
    if len(rights_and_status_eligible) != EXPECTED_ELIGIBLE_BEFORE_DEDUPE:
        raise ExtractionError(
            f"eligible pool has {len(rights_and_status_eligible)} rows before locator gate, "
            f"expected {EXPECTED_ELIGIBLE_BEFORE_DEDUPE}"
        )
    eligible = [record for record in rights_and_status_eligible if is_eligible(record)]
    by_hash: dict[str, dict[str, Any]] = {}
    for record in eligible:
        digest = str(record["content_hash"])
        previous = by_hash.get(digest)
        if previous is None or arxiv_version_key(previous) < arxiv_version_key(record):
            by_hash[digest] = record
    pool = sorted(by_hash.values(), key=lambda record: str(record["content_hash"]))
    if len(pool) != EXPECTED_ELIGIBLE_AFTER_DEDUPE:
        raise ExtractionError(
            f"eligible pool has {len(pool)} rows after dedupe, "
            f"expected {EXPECTED_ELIGIBLE_AFTER_DEDUPE}"
        )
    return pool


def release_selection_key(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -float(record["latest_interestingness_score"]),
        -float(record["latest_interestingness_confidence"]),
        -float(record["latest_label_confidence"]),
        str(record["content_hash"]),
        int(record["id"]),
    )


def select_release_rows(
    pool: Iterable[dict[str, Any]], count: int = DEFAULT_RELEASE_SELECTION
) -> list[dict[str, Any]]:
    ordered = sorted(pool, key=release_selection_key)
    if len(ordered) < count:
        raise ExtractionError(f"pool has {len(ordered)} rows; release needs {count}")
    return ordered[:count]


def encode_pool(pool: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json_line(record) for record in pool)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="pinned upstream public JSONL")
    parser.add_argument("--output", required=True, type=Path, help="derived CC-BY eligible pool")
    parser.add_argument(
        "--check", action="store_true", help="compare output bytes instead of writing them"
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        records = load_upstream(args.input)
        pool = build_pool(records)
        payload = encode_pool(pool)
        selected = select_release_rows(pool)
        if args.check:
            try:
                observed = args.output.read_bytes()
            except OSError as error:
                raise ExtractionError(f"cannot read derived pool: {error}") from error
            if observed != payload:
                raise ExtractionError("derived eligible-pool bytes differ")
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(payload)
        print(
            "PASS extract_openconjecture_v5 "
            f"schema={SCHEMA_VERSION} upstream={len(records)} pool={len(pool)} "
            f"selected={len(selected)} pool_sha256={sha256_bytes(payload)} "
            f"minimum_selected_interestingness="
            f"{min(float(row['latest_interestingness_score']) for row in selected):.2f}"
        )
        return 0
    except (ExtractionError, OSError, ValueError, TypeError, KeyError) as error:
        print(f"FAIL extract_openconjecture_v5: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
