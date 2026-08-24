#!/usr/bin/env python3
"""Build the sealed OpenConjecture curation authority for Stage5 release 5.2.

The four review shards and the cross-candidate/parent dedupe audit are durable
human-curation inputs.  This program does not infer new reviews.  It verifies
those inputs against both pinned OpenConjecture assets and the immutable 5.1
catalog, applies the frozen selection rule, and writes the exact 889-row
partition required by the 5.2 expansion contract.

``--check`` is read-only: it rebuilds the authority and compares its canonical
bytes with the requested output.  A normal write uses a same-directory atomic
replacement followed by file and directory fsync.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_ROOT = REPO_ROOT / "Docs/catalog/v5"

DEFAULT_REVIEW_PATHS = tuple(
    CATALOG_ROOT / f"curation/reviews/review-{suffix}.jsonl"
    for suffix in ("a", "b", "c", "d")
)
DEFAULT_CROSS_DEDUPE_PATH = (
    CATALOG_ROOT / "curation/reviews/cross-dedupe.json"
)
DEFAULT_ELIGIBLE_PATH = (
    CATALOG_ROOT / "sources/openconjecture-fa03d85-cc-by-real-conf090.jsonl"
)
DEFAULT_FULL_PATH = (
    CATALOG_ROOT / "sources/openconjecture-fa03d85-public.jsonl"
)
DEFAULT_PARENT_CATALOG_PATH = CATALOG_ROOT / "releases/5.1/Claim_Catalog.json"
DEFAULT_CONTRACT_PATH = CATALOG_ROOT / "Stage5_Math_Expansion_Contract_v5_2.json"
DEFAULT_SOURCE_REGISTRY_PATH = CATALOG_ROOT / "Math_Source_Registry_v5_2.json"
DEFAULT_OUTPUT_PATH = (
    CATALOG_ROOT / "curation/OpenConjecture_Curation_v5_2.json"
)

SCHEMA_VERSION = "awesome-theorems/openconjecture-curation/5.2"
SOURCE_ID = "SRC-MATH-V5-OPENCONJECTURE-FA03D85"
EXPECTED_CANDIDATES = 889
EXPECTED_ACCEPTED = 600
FIRST_NEW_ORDINAL = 5_985
LAST_NEW_ORDINAL = 6_584

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")
DEFAULT_ARXIV_RE = re.compile(
    r"^(?P<base>[0-9]{4}\.[0-9]{4,5})v(?P<version>[1-9][0-9]*)$"
)

REVIEW_FIELDS = {
    "id",
    "content_hash",
    "decision",
    "reason_codes",
    "semantic_key",
    "atomic_statement_summary",
    "importance_assessment",
    "notes",
}
LEDGER_REVIEW_FIELDS = {
    "atomic_statement_summary",
    "importance_assessment",
    "review_reason_codes",
    "review_notes",
    "review_fragment_sha256",
}


class CurationError(RuntimeError):
    """A pinned input, review boundary, or generated invariant failed."""


def canonical_json_bytes(value: Any) -> bytes:
    """Return the contract's canonical JSON representation."""

    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise CurationError(f"value is not canonical-JSON serializable: {error}") from error


def encoded_document(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return sha256_bytes(
        canonical_json_bytes(
            {key: item for key, item in value.items() if key not in omitted}
        )
    )


def artifact_authority(value: Mapping[str, Any]) -> str:
    return hash_without(value, "authority_sha256")


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical_json_bytes(sorted(values)))


def _reject_constant(value: str) -> None:
    raise CurationError(f"non-finite JSON number is forbidden: {value}")


def _object_without_duplicate_keys(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CurationError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def strict_json_value(payload: bytes, label: str) -> Any:
    try:
        return json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise CurationError(f"invalid JSON in {label}: {error}") from error


def load_json_object(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise CurationError(f"cannot read {path}: {error}") from error
    value = strict_json_value(payload, str(path))
    if not isinstance(value, dict):
        raise CurationError(f"{path} must contain one JSON object")
    return value, payload


def verify_authority(value: Mapping[str, Any], label: str) -> str:
    observed = value.get("authority_sha256")
    if not isinstance(observed, str) or SHA256_RE.fullmatch(observed) is None:
        raise CurationError(f"{label} has no valid authority_sha256")
    expected = artifact_authority(value)
    if observed != expected:
        raise CurationError(f"{label} has a stale authority_sha256")
    return observed


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CurationError(f"{label} must be an object")
    return value


def _require_rows(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise CurationError(f"{label} must be an array of objects")
    return value


def _require_string(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        qualifier = "a string" if allow_empty else "a non-empty string"
        raise CurationError(f"{label} must be {qualifier}")
    return value


def _require_positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CurationError(f"{label} must be a positive integer")
    return value


def _require_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CurationError(f"{label} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise CurationError(f"{label} must be a finite number")
    return result


def _verify_file_spec(path: Path, payload: bytes, spec: Mapping[str, Any], label: str) -> None:
    expected_size = spec.get("size_bytes")
    expected_hash = spec.get("sha256")
    if expected_size != len(payload):
        raise CurationError(
            f"{label} size is {len(payload)}, expected {expected_size!r}"
        )
    observed_hash = sha256_bytes(payload)
    if expected_hash != observed_hash:
        raise CurationError(
            f"{label} SHA-256 is {observed_hash}, expected {expected_hash!r}"
        )


def load_jsonl(
    path: Path,
    *,
    specification: Mapping[str, Any] | None = None,
    canonical_lines: bool = False,
) -> tuple[list[dict[str, Any]], bytes]:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise CurationError(f"cannot read JSONL input {path}: {error}") from error
    if specification is not None:
        _verify_file_spec(path, payload, specification, str(path))
    if not payload.endswith(b"\n"):
        raise CurationError(f"{path} must end with exactly one record LF")
    raw_lines = payload[:-1].split(b"\n")
    if not raw_lines or any(not line for line in raw_lines):
        raise CurationError(f"{path} contains a blank JSONL row")
    if specification is not None and len(raw_lines) != specification.get("record_count"):
        raise CurationError(
            f"{path} has {len(raw_lines)} rows, expected "
            f"{specification.get('record_count')!r}"
        )
    rows: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(raw_lines, start=1):
        value = strict_json_value(raw_line, f"{path}:{line_number}")
        if not isinstance(value, dict):
            raise CurationError(f"{path}:{line_number} is not a JSON object")
        if canonical_lines and raw_line != canonical_json_bytes(value):
            raise CurationError(f"{path}:{line_number} is not canonical JSON")
        rows.append(value)
    return rows, payload


def verify_versioned_authorities(
    contract_path: Path,
    source_registry_path: Path,
    parent_catalog_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract, _contract_payload = load_json_object(contract_path)
    verify_authority(contract, str(contract_path))
    if contract.get("schema_version") != "awesome-theorems/stage5-math-expansion-contract/5.2":
        raise CurationError("unexpected Stage5 v5.2 contract schema")
    if contract.get("release") != "5.2":
        raise CurationError("curation builder requires release 5.2")

    registry, registry_payload = load_json_object(source_registry_path)
    registry_authority = verify_authority(registry, str(source_registry_path))
    registry_binding = _require_object(
        _require_object(contract.get("versioned_authorities"), "contract.versioned_authorities").get(
            "source_registry"
        ),
        "contract.versioned_authorities.source_registry",
    )
    observed_registry_file_hash = sha256_bytes(registry_payload)
    if registry_binding.get("file_sha256") != observed_registry_file_hash:
        raise CurationError(
            "contract/source-registry file SHA-256 binding drifted: "
            f"observed {observed_registry_file_hash}"
        )
    if registry_binding.get("authority_sha256") != registry_authority:
        raise CurationError("contract/source-registry authority binding drifted")

    sources = _require_rows(registry.get("sources"), "source_registry.sources")
    matching = [row for row in sources if row.get("source_id") == SOURCE_ID]
    if len(matching) != 1:
        raise CurationError(f"source registry must contain exactly one {SOURCE_ID} row")
    source_registry_row = matching[0]

    parent, parent_payload = load_json_object(parent_catalog_path)
    parent_authority = verify_authority(parent, str(parent_catalog_path))
    parent_binding = _require_object(contract.get("parent"), "contract.parent")
    _verify_file_spec(
        parent_catalog_path,
        parent_payload,
        {
            "size_bytes": len(parent_payload),
            "sha256": parent_binding.get("claim_catalog_file_sha256"),
        },
        "parent 5.1 Claim_Catalog",
    )
    if parent_binding.get("claim_catalog_authority_sha256") != parent_authority:
        raise CurationError("contract/parent-catalog authority binding drifted")
    expected_parent_count = parent_binding.get("catalog_records")
    records = _require_rows(parent.get("records"), "parent_catalog.records")
    if len(records) != expected_parent_count:
        raise CurationError(
            f"parent catalog has {len(records)} rows, expected {expected_parent_count!r}"
        )
    return contract, registry, source_registry_row, parent


def _asset_specs(
    contract: Mapping[str, Any], source_registry_row: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    contract_assets = _require_object(contract.get("source_assets"), "contract.source_assets")
    registry_assets = _require_object(
        source_registry_row.get("assets"), "source_registry.source.assets"
    )
    result: list[dict[str, Any]] = []
    for key in ("upstream_public_jsonl", "eligible_pool_jsonl"):
        contract_spec = _require_object(contract_assets.get(key), f"contract.source_assets.{key}")
        registry_spec = _require_object(registry_assets.get(key), f"source_registry.assets.{key}")
        for field in ("path", "sha256", "size_bytes", "record_count"):
            if contract_spec.get(field) != registry_spec.get(field):
                raise CurationError(f"contract/source-registry asset binding differs: {key}.{field}")
        result.append(contract_spec)
    return result[0], result[1]


def _source_requirements(contract: Mapping[str, Any]) -> tuple[dict[str, Any], re.Pattern[str]]:
    policy = _require_object(
        contract.get("source_admission_policy"), "contract.source_admission_policy"
    )
    requirements = _require_object(
        policy.get("all_required_source_fields"),
        "contract.source_admission_policy.all_required_source_fields",
    )
    pattern = _require_string(
        policy.get("versioned_arxiv_id_pattern"),
        "contract.source_admission_policy.versioned_arxiv_id_pattern",
    )
    try:
        arxiv_re = re.compile(pattern)
    except re.error as error:
        raise CurationError(f"invalid contract arXiv pattern: {error}") from error
    return requirements, arxiv_re


def source_is_eligible(
    row: Mapping[str, Any],
    requirements: Mapping[str, Any],
    arxiv_re: re.Pattern[str] = DEFAULT_ARXIV_RE,
    *,
    include_version: bool = True,
) -> bool:
    """Apply every frozen rights, label, confidence, and body admission gate."""

    confidence = row.get("latest_label_confidence")
    base = bool(
        row.get("latest_label") == requirements.get("latest_label")
        and row.get("latest_label_model") == requirements.get("latest_label_model")
        and row.get("latest_assessment_version")
        == requirements.get("latest_assessment_version")
        and isinstance(confidence, (int, float))
        and not isinstance(confidence, bool)
        and math.isfinite(float(confidence))
        and float(confidence)
        >= float(requirements.get("minimum_latest_label_confidence", math.inf))
        and isinstance(row.get("body_tex"), str)
        and bool(str(row["body_tex"]).strip())
        and row.get("license_family") == requirements.get("license_family")
        and row.get("license_url") == requirements.get("license_url")
        and row.get("normalized_license_url")
        == requirements.get("normalized_license_url")
        and row.get("publication_decision")
        == requirements.get("publication_decision")
        and row.get("publication_text_allowed")
        is requirements.get("publication_text_allowed")
        and row.get("publication_text_reason")
        == requirements.get("publication_text_reason")
        and row.get("publication_policy_version")
        == requirements.get("publication_policy_version")
        and row.get("text_withheld") is requirements.get("text_withheld")
    )
    if not base or not include_version:
        return base
    arxiv_id = row.get("arxiv_id")
    source_url = row.get("source_url")
    return bool(
        isinstance(arxiv_id, str)
        and arxiv_re.fullmatch(arxiv_id) is not None
        and isinstance(source_url, str)
        and source_url.endswith(arxiv_id)
    )


# Compatibility-friendly short name used by mutation tests and callers.
is_eligible = source_is_eligible


def _version_key(row: Mapping[str, Any], arxiv_re: re.Pattern[str]) -> tuple[str, int, str, int]:
    arxiv_id = str(row.get("arxiv_id", ""))
    match = arxiv_re.fullmatch(arxiv_id)
    if match is None:
        raise CurationError(f"eligible row has unversioned arXiv id {arxiv_id!r}")
    try:
        base, raw_version = arxiv_id.rsplit("v", 1)
        version = int(raw_version)
    except ValueError as error:
        raise CurationError(f"cannot parse versioned arXiv id {arxiv_id!r}") from error
    return base, version, str(row.get("updated_at", "")), int(row["id"])


def _validate_pool_row(row: Mapping[str, Any], label: str) -> None:
    record_id = _require_positive_int(row.get("id"), f"{label}.id")
    content_hash = _require_string(row.get("content_hash"), f"{label}.content_hash")
    if SHA256_RE.fullmatch(content_hash) is None:
        raise CurationError(f"{label}.content_hash is not a lowercase SHA-256")
    _require_string(row.get("arxiv_id"), f"{label}.arxiv_id")
    _require_string(row.get("source_url"), f"{label}.source_url")
    _require_string(row.get("body_tex"), f"{label}.body_tex")
    _require_string(row.get("plain_text"), f"{label}.plain_text", allow_empty=True)
    _require_number(row.get("latest_label_confidence"), f"{label}.latest_label_confidence")
    _require_number(
        row.get("latest_interestingness_score"),
        f"{label}.latest_interestingness_score",
    )
    _require_number(
        row.get("latest_interestingness_confidence"),
        f"{label}.latest_interestingness_confidence",
    )
    categories = row.get("categories")
    if not isinstance(categories, list) or not all(
        isinstance(item, str) and item.strip() for item in categories
    ):
        raise CurationError(f"{label}.categories must be an array of non-empty strings")
    primary = _require_string(
        row.get("primary_category"), f"{label}.primary_category", allow_empty=True
    )
    if (not categories and primary) or (categories and not primary):
        raise CurationError(f"{label} has inconsistent category/primary_category metadata")
    if primary and primary not in categories:
        raise CurationError(f"{label}.primary_category is absent from categories")
    authors = row.get("authors")
    if not isinstance(authors, list) or not authors or not all(
        isinstance(item, str) and item.strip() for item in authors
    ):
        raise CurationError(f"{label}.authors must be a non-empty string array")
    # Make error locations retain the useful source id even though it is not
    # otherwise needed below.
    del record_id


def load_and_verify_source_assets(
    contract: Mapping[str, Any],
    source_registry_row: Mapping[str, Any],
    full_path: Path,
    eligible_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, str]]:
    full_spec, eligible_spec = _asset_specs(contract, source_registry_row)
    full, _full_payload = load_jsonl(
        full_path, specification=full_spec, canonical_lines=False
    )
    pool, eligible_payload = load_jsonl(
        eligible_path, specification=eligible_spec, canonical_lines=True
    )
    requirements, arxiv_re = _source_requirements(contract)

    full_by_id: dict[int, dict[str, Any]] = {}
    for line_number, row in enumerate(full, start=1):
        record_id = _require_positive_int(row.get("id"), f"{full_path}:{line_number}.id")
        if record_id in full_by_id:
            raise CurationError(f"full source duplicates id {record_id}")
        full_by_id[record_id] = row

    before_version = [
        row
        for row in full
        if source_is_eligible(row, requirements, arxiv_re, include_version=False)
    ]
    expected_before = _require_object(
        contract.get("source_admission_policy"), "contract.source_admission_policy"
    ).get("eligible_before_versioned_locator_and_dedupe")
    if len(before_version) != expected_before:
        raise CurationError(
            f"source admission has {len(before_version)} pre-locator rows, "
            f"expected {expected_before!r}"
        )

    winners: dict[str, dict[str, Any]] = {}
    for row in before_version:
        if not source_is_eligible(row, requirements, arxiv_re, include_version=True):
            continue
        content_hash = row.get("content_hash")
        if not isinstance(content_hash, str) or SHA256_RE.fullmatch(content_hash) is None:
            raise CurationError("source-eligible row has an invalid content_hash")
        previous = winners.get(content_hash)
        if previous is None or _version_key(previous, arxiv_re) < _version_key(row, arxiv_re):
            winners[content_hash] = row
    rebuilt = sorted(winners.values(), key=lambda row: str(row["content_hash"]))
    if rebuilt != pool:
        raise CurationError("eligible pool does not exactly rebuild from the full JSONL")

    curation_contract = _require_object(
        contract.get("curation_ledger_contract"), "contract.curation_ledger_contract"
    )
    expected_rows = curation_contract.get("candidate_rows")
    if expected_rows != EXPECTED_CANDIDATES or len(pool) != EXPECTED_CANDIDATES:
        raise CurationError(
            f"curation requires exactly {EXPECTED_CANDIDATES} source rows; "
            f"contract={expected_rows!r}, pool={len(pool)}"
        )

    by_hash: dict[str, dict[str, Any]] = {}
    source_hashes: dict[str, str] = {}
    observed_ids: set[int] = set()
    hashes_in_order: list[str] = []
    for line_number, row in enumerate(pool, start=1):
        label = f"{eligible_path}:{line_number}"
        _validate_pool_row(row, label)
        if not source_is_eligible(row, requirements, arxiv_re, include_version=True):
            raise CurationError(f"{label} fails the frozen source-admission policy")
        record_id = int(row["id"])
        if record_id in observed_ids:
            raise CurationError(f"eligible pool duplicates id {record_id}")
        observed_ids.add(record_id)
        if full_by_id.get(record_id) != row:
            raise CurationError(f"eligible row id {record_id} differs from its full-source row")
        content_hash = str(row["content_hash"])
        if content_hash in by_hash:
            raise CurationError(f"eligible pool duplicates content hash {content_hash}")
        by_hash[content_hash] = row
        source_hashes[content_hash] = sha256_bytes(canonical_json_bytes(row))
        hashes_in_order.append(content_hash)
    if hashes_in_order != sorted(hashes_in_order):
        raise CurationError("eligible pool is not content-hash sorted")
    expected_pool_hash = _require_object(
        contract.get("source_assets"), "contract.source_assets"
    )["eligible_pool_jsonl"]["sha256"]
    if sha256_bytes(eligible_payload) != expected_pool_hash:
        raise CurationError("eligible pool byte hash differs from contract")
    expected_set = _require_object(
        contract.get("source_assets"), "contract.source_assets"
    )["eligible_pool_jsonl"].get("content_hash_set_sha256")
    if set_digest(hashes_in_order) != expected_set:
        raise CurationError("eligible content-hash set digest differs from contract")
    return pool, by_hash, source_hashes


def load_reviews(
    review_paths: Sequence[Path],
    pool: Sequence[Mapping[str, Any]],
) -> tuple[
    dict[int, dict[str, Any]],
    dict[int, str],
    dict[int, str],
]:
    if not review_paths:
        raise CurationError("at least one durable review fragment is required")
    pool_by_id = {int(row["id"]): row for row in pool}
    pool_hashes = {str(row["content_hash"]) for row in pool}
    reviews: dict[int, dict[str, Any]] = {}
    fragment_hash_by_id: dict[int, str] = {}
    shard_by_id: dict[int, str] = {}
    observed_hashes: set[str] = set()
    for path in review_paths:
        rows, payload = load_jsonl(path, canonical_lines=False)
        fragment_hash = sha256_bytes(payload)
        shard_match = re.fullmatch(r"review-([A-Za-z0-9_-]+)", path.stem)
        shard = shard_match.group(1) if shard_match else path.stem
        for line_number, row in enumerate(rows, start=1):
            label = f"{path}:{line_number}"
            if set(row) != REVIEW_FIELDS:
                raise CurationError(
                    f"{label} review field set differs: "
                    f"missing={sorted(REVIEW_FIELDS - set(row))}, "
                    f"extra={sorted(set(row) - REVIEW_FIELDS)}"
                )
            record_id = _require_positive_int(row.get("id"), f"{label}.id")
            if record_id in reviews:
                raise CurationError(f"review fragments duplicate source id {record_id}")
            content_hash = _require_string(row.get("content_hash"), f"{label}.content_hash")
            if SHA256_RE.fullmatch(content_hash) is None:
                raise CurationError(f"{label}.content_hash is invalid")
            if content_hash in observed_hashes:
                raise CurationError(f"review fragments duplicate content hash {content_hash}")
            source = pool_by_id.get(record_id)
            if source is None or source.get("content_hash") != content_hash:
                raise CurationError(
                    f"{label} does not align with the eligible source id/content_hash"
                )
            decision = row.get("decision")
            if decision not in {"accept", "reject", "needs_split"}:
                raise CurationError(f"{label}.decision is invalid: {decision!r}")
            importance = row.get("importance_assessment")
            if importance not in {"high", "medium", "low"}:
                raise CurationError(f"{label}.importance_assessment is invalid")
            reason_codes = row.get("reason_codes")
            if (
                not isinstance(reason_codes, list)
                or not reason_codes
                or not all(isinstance(code, str) and code.strip() for code in reason_codes)
                or len(reason_codes) != len(set(reason_codes))
            ):
                raise CurationError(f"{label}.reason_codes must be unique non-empty strings")
            notes = _require_string(row.get("notes"), f"{label}.notes")
            review_semantic_key = row.get("semantic_key")
            review_summary = row.get("atomic_statement_summary")
            if review_semantic_key is None or review_summary is None:
                if not (
                    decision == "reject"
                    and review_semantic_key is None
                    and review_summary is None
                ):
                    raise CurationError(
                        f"{label} may omit semantic payload only for a rejected nonclaim"
                    )
                row = dict(row)
                row["semantic_key"] = f"nonclaim/{content_hash}"
                row["atomic_statement_summary"] = notes
            else:
                _require_string(review_semantic_key, f"{label}.semantic_key")
                _require_string(review_summary, f"{label}.atomic_statement_summary")
            reviews[record_id] = row
            observed_hashes.add(content_hash)
            fragment_hash_by_id[record_id] = fragment_hash
            shard_by_id[record_id] = shard
    if len(reviews) != EXPECTED_CANDIDATES:
        raise CurationError(
            f"review fragments contain {len(reviews)} rows, expected {EXPECTED_CANDIDATES}"
        )
    if set(reviews) != set(pool_by_id) or observed_hashes != pool_hashes:
        raise CurationError("review fragments are not an exact id/content-hash pool partition")
    return reviews, fragment_hash_by_id, shard_by_id


def final_semantic_key(review: Mapping[str, Any]) -> str:
    payload = {
        "review_semantic_key": review["semantic_key"],
        "atomic_statement_summary": review["atomic_statement_summary"],
    }
    return "openconjecture-semantic/" + sha256_bytes(canonical_json_bytes(payload))


def semantic_key_payload_sha256(review: Mapping[str, Any]) -> str:
    semantic_key = final_semantic_key(review)
    return sha256_bytes(
        canonical_json_bytes(
            {
                "semantic_key": semantic_key,
                "atomic_statement_summary": review["atomic_statement_summary"],
            }
        )
    )


def _base_review_eligible(review: Mapping[str, Any], source: Mapping[str, Any]) -> bool:
    return bool(
        review.get("decision") == "accept"
        and review.get("importance_assessment") in {"high", "medium"}
        and float(source["latest_interestingness_score"]) >= 0.50
    )


def _parent_variant_index(parent: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(_require_rows(parent.get("records"), "parent.records")):
        variant_id = _require_string(row.get("variant_id"), f"parent.records[{index}].variant_id")
        match = ATV_RE.fullmatch(variant_id)
        if match is None:
            raise CurationError(f"parent has invalid variant id {variant_id!r}")
        if variant_id in result:
            raise CurationError(f"parent duplicates variant id {variant_id}")
        result[variant_id] = row
    if not result or max(int(ATV_RE.fullmatch(key).group(1)) for key in result) != FIRST_NEW_ORDINAL - 1:  # type: ignore[union-attr]
        raise CurationError("parent catalog ATV high-watermark is not 5984")
    return result


def load_cross_dedupe(
    path: Path,
    reviews: Mapping[int, Mapping[str, Any]],
    pool_by_id: Mapping[int, Mapping[str, Any]],
    shard_by_id: Mapping[int, str],
    parent: Mapping[str, Any],
) -> tuple[dict[int, tuple[str | None, str | None]], set[int], dict[str, Any]]:
    cross, _payload = load_json_object(path)
    if cross.get("schema_version") != "openconjecture-cross-dedupe-v1":
        raise CurationError("cross-dedupe schema_version is unsupported")
    base_ids = {
        record_id
        for record_id, review in reviews.items()
        if _base_review_eligible(review, pool_by_id[record_id])
    }
    if cross.get("eligible_count") != len(base_ids):
        raise CurationError("cross-dedupe eligible_count differs from aligned reviews")

    shard_counts = Counter(shard_by_id[item] for item in base_ids)
    declared_shards = cross.get("eligible_counts_by_shard")
    if not isinstance(declared_shards, dict) or declared_shards != dict(sorted(shard_counts.items())):
        raise CurationError("cross-dedupe eligible_counts_by_shard differs from reviews")

    expected_missing_categories = {
        item for item in base_ids if not str(pool_by_id[item].get("primary_category", ""))
    }
    missing_categories_raw = cross.get("missing_category_ids")
    if not isinstance(missing_categories_raw, list) or any(
        isinstance(item, bool) or not isinstance(item, int)
        for item in missing_categories_raw
    ):
        raise CurationError("cross-dedupe missing_category_ids must be an integer array")
    if len(missing_categories_raw) != len(set(missing_categories_raw)):
        raise CurationError("cross-dedupe duplicates a missing-category id")
    if set(missing_categories_raw) != expected_missing_categories:
        raise CurationError("cross-dedupe missing_category_ids differs from source metadata")

    missing_context_raw = cross.get("missing_context_ids")
    if not isinstance(missing_context_raw, list) or any(
        isinstance(item, bool) or not isinstance(item, int)
        for item in missing_context_raw
    ):
        raise CurationError("cross-dedupe missing_context_ids must be an integer array")
    if len(missing_context_raw) != len(set(missing_context_raw)):
        raise CurationError("cross-dedupe duplicates a missing-context id")
    missing_context = set(missing_context_raw)
    if not missing_context <= base_ids:
        raise CurationError("cross-dedupe missing_context_ids contains an ineligible review")

    parent_variants = _parent_variant_index(parent)
    groups = _require_rows(cross.get("groups"), "cross_dedupe.groups")
    links: dict[int, tuple[str | None, str | None]] = {}
    canonical_candidate_ids: set[int] = set()
    parent_group_ids: set[str] = set()
    internal_removed: set[int] = set()
    parent_removed: set[int] = set()
    for index, group in enumerate(groups):
        label = f"cross_dedupe.groups[{index}]"
        has_candidate = "canonical_candidate_id" in group
        has_parent = "parent_variant_id" in group
        if has_candidate == has_parent:
            raise CurationError(
                f"{label} must contain exactly one canonical_candidate_id or parent_variant_id"
            )
        duplicates = group.get("duplicate_candidate_ids")
        if (
            not isinstance(duplicates, list)
            or not duplicates
            or any(isinstance(item, bool) or not isinstance(item, int) for item in duplicates)
            or len(duplicates) != len(set(duplicates))
        ):
            raise CurationError(f"{label}.duplicate_candidate_ids is invalid")
        _require_string(group.get("rationale"), f"{label}.rationale")
        confidence = group.get("confidence")
        if isinstance(confidence, str):
            _require_string(confidence, f"{label}.confidence")
        elif isinstance(confidence, (int, float)) and not isinstance(confidence, bool):
            value = _require_number(confidence, f"{label}.confidence")
            if not 0.0 <= value <= 1.0:
                raise CurationError(f"{label}.confidence must be in [0,1]")
        else:
            raise CurationError(f"{label}.confidence is invalid")

        canonical_semantic: str | None = None
        parent_variant: str | None = None
        if has_candidate:
            canonical = _require_positive_int(
                group.get("canonical_candidate_id"), f"{label}.canonical_candidate_id"
            )
            if canonical not in base_ids:
                raise CurationError(f"{label} canonical candidate is not review-eligible")
            if canonical in duplicates:
                raise CurationError(f"{label} canonical candidate is also a duplicate")
            if canonical in canonical_candidate_ids:
                raise CurationError(f"candidate {canonical} is canonical in multiple groups")
            canonical_candidate_ids.add(canonical)
            canonical_semantic = final_semantic_key(reviews[canonical])
            internal_removed.update(duplicates)
        else:
            parent_variant = _require_string(
                group.get("parent_variant_id"), f"{label}.parent_variant_id"
            )
            if ATV_RE.fullmatch(parent_variant) is None or parent_variant not in parent_variants:
                raise CurationError(f"{label} cites unknown parent variant {parent_variant!r}")
            if parent_variant in parent_group_ids:
                raise CurationError(f"parent variant {parent_variant} has multiple groups")
            parent_group_ids.add(parent_variant)
            parent_removed.update(duplicates)
        for duplicate in duplicates:
            if duplicate not in base_ids:
                raise CurationError(f"{label} duplicate candidate {duplicate} is not review-eligible")
            if duplicate in links:
                raise CurationError(f"candidate {duplicate} is duplicated by multiple groups")
            links[duplicate] = (canonical_semantic, parent_variant)

    if canonical_candidate_ids & set(links):
        raise CurationError("a cross-dedupe canonical candidate is duplicated by another group")
    if internal_removed & parent_removed:
        raise CurationError("internal and parent duplicate groups overlap")

    expected_values = {
        "internal_duplicate_group_count": len(canonical_candidate_ids),
        "internal_duplicate_rows_removed": len(internal_removed),
        "parent_duplicate_group_count": len(parent_group_ids),
        "parent_duplicate_rows_removed": len(parent_removed),
        "internal_unique_count": len(base_ids - internal_removed),
        "viable_unique_count": len(base_ids - set(links)),
    }
    for field, expected in expected_values.items():
        if cross.get(field) != expected:
            raise CurationError(
                f"cross-dedupe {field}={cross.get(field)!r}, expected {expected}"
            )
    return links, missing_context, cross


def selection_key(
    review: Mapping[str, Any], source: Mapping[str, Any]
) -> tuple[int, float, float, float, str]:
    importance = review.get("importance_assessment")
    if importance not in {"high", "medium"}:
        raise CurationError("selection_key requires high/medium importance")
    return (
        0 if importance == "high" else 1,
        -_require_number(
            source.get("latest_interestingness_score"), "latest_interestingness_score"
        ),
        -_require_number(
            source.get("latest_interestingness_confidence"),
            "latest_interestingness_confidence",
        ),
        -_require_number(source.get("latest_label_confidence"), "latest_label_confidence"),
        str(source["content_hash"]),
    )


def select_candidates(
    reviews: Mapping[int, Mapping[str, Any]],
    pool_by_id: Mapping[int, Mapping[str, Any]],
    duplicate_ids: set[int],
    missing_context_ids: set[int],
    count: int = EXPECTED_ACCEPTED,
) -> tuple[list[int], set[int]]:
    eligible = [
        record_id
        for record_id, review in reviews.items()
        if _base_review_eligible(review, pool_by_id[record_id])
        and record_id not in duplicate_ids
        and record_id not in missing_context_ids
    ]
    semantic_keys = [final_semantic_key(reviews[item]) for item in eligible]
    if len(semantic_keys) != len(set(semantic_keys)):
        raise CurationError("viable review rows do not have unique normalized semantic keys")
    if len(eligible) < count:
        raise CurationError(
            f"only {len(eligible)} semantically unique candidates survive; need {count}"
        )

    rank = lambda item: selection_key(reviews[item], pool_by_id[item])
    by_category: dict[str, list[int]] = defaultdict(list)
    for record_id in eligible:
        category = str(pool_by_id[record_id].get("primary_category", ""))
        if category:
            by_category[category].append(record_id)

    selected: list[int] = []
    selected_set: set[int] = set()
    seeded: set[int] = set()
    for category in sorted(by_category):
        for record_id in sorted(by_category[category], key=rank)[:3]:
            if record_id not in selected_set:
                selected.append(record_id)
                selected_set.add(record_id)
                seeded.add(record_id)
    for record_id in sorted(eligible, key=rank):
        if len(selected) == count:
            break
        if record_id not in selected_set:
            selected.append(record_id)
            selected_set.add(record_id)
    if len(selected) != count or len(selected_set) != count:
        raise CurationError(f"selection produced {len(selected)} rows, expected {count}")
    if any(not str(pool_by_id[item].get("primary_category", "")) for item in seeded):
        raise CurationError("an unclassified candidate entered the category seed")
    return selected, seeded


def model_label_object(source: Mapping[str, Any]) -> dict[str, Any]:
    value = {
        "label_model": source["latest_label_model"],
        "label": source["latest_label"],
        "label_confidence": source["latest_label_confidence"],
        "assessment_version": source["latest_assessment_version"],
        "label_rationale": source["latest_label_rationale"],
        "evidence_snippet": source["latest_evidence_snippet"],
        "labeled_at": source["latest_labeled_at"],
        "interestingness_score": source["latest_interestingness_score"],
        "interestingness_confidence": source["latest_interestingness_confidence"],
        "interestingness_rationale": source["latest_interestingness_rationale"],
        "viability_score": source["latest_viability_score"],
        "viability_confidence": source["latest_viability_confidence"],
        "viability_rationale": source["latest_viability_rationale"],
        "source_model_assertion_not_independent_status_review": True,
        "source_model_assertion_not_proof": True,
    }
    value["model_label_payload_sha256"] = hash_without(
        value, "model_label_payload_sha256"
    )
    return value


def rights_object(source: Mapping[str, Any]) -> dict[str, Any]:
    attribution = {
        "attribution_authors": list(source["authors"]),
        "attribution_title": source["title"],
        "attribution_arxiv_id": source["arxiv_id"],
    }
    value = {
        "spdx_expression": "CC-BY-4.0",
        "license_family": source["license_family"],
        "license_url": source["license_url"],
        "normalized_license_url": source["normalized_license_url"],
        "publication_decision": source["publication_decision"],
        "publication_text_allowed": source["publication_text_allowed"],
        "publication_text_reason": source["publication_text_reason"],
        "publication_policy_version": source["publication_policy_version"],
        "text_withheld": source["text_withheld"],
        **attribution,
        "attribution_payload_sha256": sha256_bytes(canonical_json_bytes(attribution)),
        "redistribution_mode": "verbatim_cc_by_4_0_with_per_record_attribution",
        "catalog_relicenses_source": False,
        "source_refs": [SOURCE_ID],
    }
    value["rights_payload_sha256"] = hash_without(value, "rights_payload_sha256")
    return value


NONCLAIM_REASON_MARKERS = {
    "not_truth_apt",
    "not_strictly_truth_apt",
    "not_stably_truth_apt",
    "non_truth_apt_approximation",
    "pure_question",
    "pure_questions",
    "question_only",
    "question_form",
    "not_proposition",
    "not_author_asserted_conjecture",
}
STATUS_REASON_MARKERS = {
    "solved",
    "proved",
    "refuted",
    "proved_lemma_bundle",
    "outdated_overlap",
    "not_in_published_text",
    "not_presented_in_paper",
    "commented_out_source",
}


def _review_rejection(review: Mapping[str, Any]) -> tuple[str, str]:
    reasons = set(review["reason_codes"])
    if "semantic_duplicate" in reasons:
        return "rejected_semantic_duplicate", "review_identified_semantic_duplicate"
    if reasons & STATUS_REASON_MARKERS:
        return "rejected_status_boundary", "review_failed_open_status_boundary"
    if reasons & NONCLAIM_REASON_MARKERS:
        return "rejected_nonclaim", "review_failed_truth_apt_claim_boundary"
    return (
        "rejected_incoherent_source_block",
        "review_found_source_block_not_release_coherent",
    )


def _disposition_for(
    record_id: int,
    review: Mapping[str, Any],
    source: Mapping[str, Any],
    selected_ranks: Mapping[int, int],
    seeded_ids: set[int],
    duplicate_links: Mapping[int, tuple[str | None, str | None]],
    missing_context_ids: set[int],
) -> tuple[str, str]:
    if record_id in missing_context_ids:
        return (
            "rejected_incoherent_source_block",
            "cross_audit_missing_context_for_whole_exact_source_block",
        )
    if record_id in duplicate_links:
        if duplicate_links[record_id][1] is not None:
            return "rejected_semantic_duplicate", "semantic_duplicate_of_parent_variant"
        return "rejected_semantic_duplicate", "semantic_duplicate_of_curated_candidate"
    if review["decision"] == "needs_split":
        return (
            "rejected_incoherent_source_block",
            "whole_exact_source_block_requires_split",
        )
    if review["decision"] == "reject":
        return _review_rejection(review)
    if float(source["latest_interestingness_score"]) < 0.50:
        return "rejected_below_interest_floor", "source_interestingness_below_0_50"
    if review["importance_assessment"] not in {"high", "medium"}:
        return "eligible_not_selected", "curator_importance_below_medium"
    if record_id in selected_ranks:
        if record_id in seeded_ids:
            return "accepted_new_strict_open_claim", "selected_category_seed"
        return "accepted_new_strict_open_claim", "selected_global_rank_fill"
    return "eligible_not_selected", "ranked_beyond_exact_600"


def build_candidate_rows(
    contract: Mapping[str, Any],
    pool: Sequence[dict[str, Any]],
    source_hashes: Mapping[str, str],
    reviews: Mapping[int, Mapping[str, Any]],
    fragment_hash_by_id: Mapping[int, str],
    duplicate_links: Mapping[int, tuple[str | None, str | None]],
    missing_context_ids: set[int],
) -> tuple[list[dict[str, Any]], int, int]:
    pool_by_id = {int(row["id"]): row for row in pool}
    selected, seeded = select_candidates(
        reviews,
        pool_by_id,
        set(duplicate_links),
        missing_context_ids,
        EXPECTED_ACCEPTED,
    )
    selected_ranks = {record_id: rank for rank, record_id in enumerate(selected, start=1)}
    required_fields = set(
        _require_object(
            contract.get("curation_ledger_contract"), "contract.curation_ledger_contract"
        ).get("required_candidate_fields", [])
    )
    generated_fields = required_fields | LEDGER_REVIEW_FIELDS
    required_generated = {
        "candidate_key",
        "source_record_id",
        "source_record_sha256",
        "content_hash",
        "body_tex_sha256",
        "arxiv_id",
        "interestingness_score",
        "semantic_key",
        "semantic_key_payload_sha256",
        "disposition",
        "reason_code",
        "selected_rank",
        "target_variant_id",
        "target_s5_id",
        "duplicate_of_semantic_key",
        "duplicate_of_variant_id",
        "grants_catalog_entry",
        "grants_strict_conjecture_credit",
        "rights_payload_sha256",
        "model_label_payload_sha256",
        "row_sha256",
    } | LEDGER_REVIEW_FIELDS
    if not required_fields <= required_generated:
        raise CurationError(
            "contract requires unsupported candidate fields: "
            f"{sorted(required_fields - required_generated)}"
        )
    if generated_fields != required_generated:
        # The writer deliberately emits one closed, review-bearing row shape.
        # This catches a contract which silently removes a core ledger field.
        missing = required_generated - generated_fields
        if missing - LEDGER_REVIEW_FIELDS:
            raise CurationError(f"contract omits core candidate fields: {sorted(missing)}")

    rows: list[dict[str, Any]] = []
    for source in pool:
        record_id = int(source["id"])
        review = reviews[record_id]
        content_hash = str(source["content_hash"])
        disposition, reason_code = _disposition_for(
            record_id,
            review,
            source,
            selected_ranks,
            seeded,
            duplicate_links,
            missing_context_ids,
        )
        accepted = disposition == "accepted_new_strict_open_claim"
        rank = selected_ranks.get(record_id) if accepted else None
        if accepted and rank is None:
            raise CurationError("accepted row has no selected rank")
        ordinal = FIRST_NEW_ORDINAL + int(rank) - 1 if rank is not None else None
        duplicate_semantic, duplicate_variant = duplicate_links.get(
            record_id, (None, None)
        )
        row: dict[str, Any] = {
            "candidate_key": f"openconjecture:{content_hash}",
            "source_record_id": record_id,
            "source_record_sha256": source_hashes[content_hash],
            "content_hash": content_hash,
            "body_tex_sha256": sha256_bytes(str(source["body_tex"]).encode("utf-8")),
            "arxiv_id": source["arxiv_id"],
            "interestingness_score": source["latest_interestingness_score"],
            "semantic_key": final_semantic_key(review),
            "semantic_key_payload_sha256": semantic_key_payload_sha256(review),
            "disposition": disposition,
            "reason_code": reason_code,
            "selected_rank": rank,
            "target_variant_id": f"ATV-{ordinal:08d}" if ordinal is not None else None,
            "target_s5_id": f"S5-CLM-{ordinal:08d}" if ordinal is not None else None,
            "duplicate_of_semantic_key": duplicate_semantic,
            "duplicate_of_variant_id": duplicate_variant,
            "grants_catalog_entry": accepted,
            "grants_strict_conjecture_credit": accepted,
            "rights_payload_sha256": rights_object(source)["rights_payload_sha256"],
            "model_label_payload_sha256": model_label_object(source)[
                "model_label_payload_sha256"
            ],
            "atomic_statement_summary": review["atomic_statement_summary"],
            "importance_assessment": review["importance_assessment"],
            "review_reason_codes": list(review["reason_codes"]),
            "review_notes": review["notes"],
            "review_fragment_sha256": fragment_hash_by_id[record_id],
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        if set(row) != required_generated:
            raise CurationError(
                f"generated candidate {record_id} has wrong field set: "
                f"missing={sorted(required_generated - set(row))}, "
                f"extra={sorted(set(row) - required_generated)}"
            )
        rows.append(row)
    return rows, len(seeded), EXPECTED_ACCEPTED - len(seeded)


def validate_generated_ledger(
    document: Mapping[str, Any],
    contract: Mapping[str, Any],
    pool: Sequence[Mapping[str, Any]],
) -> None:
    ledger_contract = _require_object(
        contract.get("curation_ledger_contract"), "contract.curation_ledger_contract"
    )
    required_top = set(ledger_contract.get("required_top_level_fields", []))
    if set(document) != required_top:
        raise CurationError(
            f"generated ledger top-level fields differ from contract: "
            f"missing={sorted(required_top - set(document))}, "
            f"extra={sorted(set(document) - required_top)}"
        )
    if document.get("authority_sha256") != artifact_authority(document):
        raise CurationError("generated ledger has a stale authority_sha256")
    if document.get("schema_version") != SCHEMA_VERSION:
        raise CurationError("generated ledger schema_version drifted")
    if document.get("source_id") != SOURCE_ID:
        raise CurationError("generated ledger source_id drifted")
    registry_binding = _require_object(
        _require_object(contract.get("versioned_authorities"), "contract.versioned_authorities").get(
            "source_registry"
        ),
        "contract.versioned_authorities.source_registry",
    )
    if document.get("source_registry_authority_sha256") != registry_binding.get(
        "authority_sha256"
    ):
        raise CurationError("generated ledger source-registry binding drifted")
    contract_assets = _require_object(contract.get("source_assets"), "contract.source_assets")
    if document.get("eligible_pool_sha256") != contract_assets["eligible_pool_jsonl"].get(
        "sha256"
    ):
        raise CurationError("generated ledger eligible-pool binding drifted")
    rows = _require_rows(document.get("candidate_dispositions"), "candidate_dispositions")
    if len(rows) != EXPECTED_CANDIDATES:
        raise CurationError("generated ledger does not have exactly 889 candidate rows")
    expected_fields = set(ledger_contract.get("required_candidate_fields", [])) | LEDGER_REVIEW_FIELDS
    pool_by_hash = {str(row["content_hash"]): row for row in pool}
    pool_hashes = set(pool_by_hash)
    allowed_dispositions = set(ledger_contract.get("disposition_enum", []))
    observed_hashes: set[str] = set()
    accepted: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        if set(row) != expected_fields:
            raise CurationError(f"generated row {index} field closure drifted")
        if row.get("row_sha256") != hash_without(row, "row_sha256"):
            raise CurationError(f"generated row {index} hash drifted")
        content_hash = row.get("content_hash")
        if not isinstance(content_hash, str) or content_hash not in pool_hashes:
            raise CurationError(f"generated row {index} is outside eligible pool")
        if content_hash in observed_hashes:
            raise CurationError(f"generated ledger duplicates content hash {content_hash}")
        observed_hashes.add(content_hash)
        source = pool_by_hash[content_hash]
        if row.get("candidate_key") != f"openconjecture:{content_hash}":
            raise CurationError(f"generated row {index} candidate key drifted")
        if row.get("source_record_id") != source.get("id"):
            raise CurationError(f"generated row {index} source id drifted")
        if row.get("source_record_sha256") != sha256_bytes(canonical_json_bytes(source)):
            raise CurationError(f"generated row {index} source hash drifted")
        if row.get("body_tex_sha256") != sha256_bytes(
            str(source["body_tex"]).encode("utf-8")
        ):
            raise CurationError(f"generated row {index} body hash drifted")
        if row.get("arxiv_id") != source.get("arxiv_id"):
            raise CurationError(f"generated row {index} arXiv id drifted")
        if row.get("interestingness_score") != source.get("latest_interestingness_score"):
            raise CurationError(f"generated row {index} interestingness score drifted")
        if row.get("rights_payload_sha256") != rights_object(source)[
            "rights_payload_sha256"
        ]:
            raise CurationError(f"generated row {index} rights hash drifted")
        if row.get("model_label_payload_sha256") != model_label_object(source)[
            "model_label_payload_sha256"
        ]:
            raise CurationError(f"generated row {index} model-label hash drifted")
        if row.get("disposition") not in allowed_dispositions:
            raise CurationError(f"generated row {index} disposition is invalid")
        if not isinstance(row.get("atomic_statement_summary"), str) or not str(
            row["atomic_statement_summary"]
        ).strip():
            raise CurationError(f"generated row {index} summary is invalid")
        if row.get("importance_assessment") not in {"high", "medium", "low"}:
            raise CurationError(f"generated row {index} importance is invalid")
        review_codes = row.get("review_reason_codes")
        if (
            not isinstance(review_codes, list)
            or not review_codes
            or not all(isinstance(code, str) and code for code in review_codes)
            or len(review_codes) != len(set(review_codes))
        ):
            raise CurationError(f"generated row {index} review codes are invalid")
        if not isinstance(row.get("review_notes"), str):
            raise CurationError(f"generated row {index} review notes are invalid")
        fragment_sha = row.get("review_fragment_sha256")
        if not isinstance(fragment_sha, str) or SHA256_RE.fullmatch(fragment_sha) is None:
            raise CurationError(f"generated row {index} review fragment hash is invalid")
        if row.get("semantic_key_payload_sha256") != sha256_bytes(
            canonical_json_bytes(
                {
                    "semantic_key": row.get("semantic_key"),
                    "atomic_statement_summary": row.get("atomic_statement_summary"),
                }
            )
        ):
            raise CurationError(f"generated row {index} semantic payload hash drifted")
        if row.get("disposition") == "accepted_new_strict_open_claim":
            if float(source["latest_interestingness_score"]) < 0.50:
                raise CurationError(f"accepted row {index} is below the interest floor")
            if row.get("importance_assessment") not in {"high", "medium"}:
                raise CurationError(f"accepted row {index} lacks high/medium importance")
            accepted.append(row)
        else:
            if any(
                row.get(field) is not None
                for field in ("selected_rank", "target_variant_id", "target_s5_id")
            ):
                raise CurationError(f"nonaccepted row {index} has an allocation")
            if row.get("grants_catalog_entry") is not False or row.get(
                "grants_strict_conjecture_credit"
            ) is not False:
                raise CurationError(f"nonaccepted row {index} grants release credit")
    if observed_hashes != pool_hashes:
        raise CurationError("generated ledger is not an exact eligible-pool partition")
    if len(accepted) != EXPECTED_ACCEPTED:
        raise CurationError("generated ledger does not accept exactly 600 rows")
    ranks = {row["selected_rank"] for row in accepted}
    if ranks != set(range(1, EXPECTED_ACCEPTED + 1)):
        raise CurationError("accepted selected ranks are not exactly 1..600")
    accepted_semantics = [str(row["semantic_key"]) for row in accepted]
    if len(accepted_semantics) != len(set(accepted_semantics)):
        raise CurationError("accepted semantic keys are not unique")
    for row in accepted:
        rank = int(row["selected_rank"])
        ordinal = FIRST_NEW_ORDINAL + rank - 1
        if row.get("target_variant_id") != f"ATV-{ordinal:08d}" or row.get(
            "target_s5_id"
        ) != f"S5-CLM-{ordinal:08d}":
            raise CurationError("accepted allocation is not rank/ordinal aligned")
        if row.get("grants_catalog_entry") is not True or row.get(
            "grants_strict_conjecture_credit"
        ) is not True:
            raise CurationError("accepted row does not grant both required credits")
        if row.get("duplicate_of_semantic_key") is not None or row.get(
            "duplicate_of_variant_id"
        ) is not None:
            raise CurationError("accepted row carries duplicate linkage")
    if max(int(ATV_RE.fullmatch(str(row["target_variant_id"])).group(1)) for row in accepted) != LAST_NEW_ORDINAL:  # type: ignore[union-attr]
        raise CurationError("accepted allocation does not end at ATV-00006584")

    counts = _require_object(document.get("counts"), "counts")
    dispositions = Counter(str(row["disposition"]) for row in rows)
    if counts.get("candidates") != EXPECTED_CANDIDATES:
        raise CurationError("ledger candidate count drifted")
    if counts.get("accepted") != EXPECTED_ACCEPTED:
        raise CurationError("ledger accepted count drifted")
    if counts.get("nonaccepted") != EXPECTED_CANDIDATES - EXPECTED_ACCEPTED:
        raise CurationError("ledger nonaccepted count drifted")
    if counts.get("by_disposition") != dict(sorted(dispositions.items())):
        raise CurationError("ledger disposition counts drifted")

    digests = _require_object(document.get("set_digests"), "set_digests")
    expected_digests = {
        "eligible_content_hash_set_sha256": set_digest(pool_hashes),
        "accepted_content_hash_set_sha256": set_digest(
            str(row["content_hash"]) for row in accepted
        ),
        "accepted_semantic_key_set_sha256": set_digest(accepted_semantics),
        "accepted_s5_id_set_sha256": set_digest(
            str(row["target_s5_id"]) for row in accepted
        ),
    }
    if digests != expected_digests:
        raise CurationError("generated ledger set digests drifted")


def build_curation(
    *,
    review_paths: Sequence[Path] = DEFAULT_REVIEW_PATHS,
    cross_dedupe_path: Path = DEFAULT_CROSS_DEDUPE_PATH,
    eligible_path: Path = DEFAULT_ELIGIBLE_PATH,
    full_path: Path = DEFAULT_FULL_PATH,
    parent_catalog_path: Path = DEFAULT_PARENT_CATALOG_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
    source_registry_path: Path = DEFAULT_SOURCE_REGISTRY_PATH,
) -> dict[str, Any]:
    contract, _registry, source_registry_row, parent = verify_versioned_authorities(
        contract_path, source_registry_path, parent_catalog_path
    )
    pool, _pool_by_hash, source_hashes = load_and_verify_source_assets(
        contract, source_registry_row, full_path, eligible_path
    )
    pool_by_id = {int(row["id"]): row for row in pool}
    reviews, fragment_hash_by_id, shard_by_id = load_reviews(review_paths, pool)
    duplicate_links, missing_context_ids, cross = load_cross_dedupe(
        cross_dedupe_path, reviews, pool_by_id, shard_by_id, parent
    )
    rows, seeded_count, global_fill_count = build_candidate_rows(
        contract,
        pool,
        source_hashes,
        reviews,
        fragment_hash_by_id,
        duplicate_links,
        missing_context_ids,
    )
    dispositions = Counter(str(row["disposition"]) for row in rows)
    decisions = Counter(str(review["decision"]) for review in reviews.values())
    contract_assets = _require_object(contract.get("source_assets"), "contract.source_assets")
    registry_binding = _require_object(
        _require_object(contract.get("versioned_authorities"), "contract.versioned_authorities").get(
            "source_registry"
        ),
        "contract.versioned_authorities.source_registry",
    )
    accepted = [row for row in rows if row["disposition"] == "accepted_new_strict_open_claim"]
    document: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "source_id": SOURCE_ID,
        "source_registry_authority_sha256": registry_binding["authority_sha256"],
        "eligible_pool_sha256": contract_assets["eligible_pool_jsonl"]["sha256"],
        "candidate_dispositions": rows,
        "counts": {
            "candidates": len(rows),
            "accepted": len(accepted),
            "nonaccepted": len(rows) - len(accepted),
            "by_disposition": dict(sorted(dispositions.items())),
            "review_fragments": len(review_paths),
            "by_review_decision": dict(sorted(decisions.items())),
            "cross_dedupe_groups": len(cross["groups"]),
            "missing_context_rejections": len(missing_context_ids),
            "category_seeded": seeded_count,
            "global_rank_fill": global_fill_count,
        },
        "set_digests": {
            "eligible_content_hash_set_sha256": set_digest(
                str(row["content_hash"]) for row in pool
            ),
            "accepted_content_hash_set_sha256": set_digest(
                str(row["content_hash"]) for row in accepted
            ),
            "accepted_semantic_key_set_sha256": set_digest(
                str(row["semantic_key"]) for row in accepted
            ),
            "accepted_s5_id_set_sha256": set_digest(
                str(row["target_s5_id"]) for row in accepted
            ),
        },
    }
    document["authority_sha256"] = artifact_authority(document)
    validate_generated_ledger(document, contract, pool)
    return document


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--review",
        action="append",
        dest="review_paths",
        type=Path,
        help="durable review JSONL fragment (repeatable; defaults to review-a..d)",
    )
    parser.add_argument(
        "--reviews-dir",
        type=Path,
        help="directory containing exactly review-a.jsonl through review-d.jsonl",
    )
    parser.add_argument("--cross-dedupe", type=Path, default=DEFAULT_CROSS_DEDUPE_PATH)
    parser.add_argument("--eligible-jsonl", type=Path, default=DEFAULT_ELIGIBLE_PATH)
    parser.add_argument(
        "--full-jsonl",
        "--upstream-jsonl",
        dest="full_jsonl",
        type=Path,
        default=DEFAULT_FULL_PATH,
    )
    parser.add_argument("--parent-catalog", type=Path, default=DEFAULT_PARENT_CATALOG_PATH)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT_PATH)
    parser.add_argument("--source-registry", type=Path, default=DEFAULT_SOURCE_REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument(
        "--check", action="store_true", help="compare output bytes without writing"
    )
    args = parser.parse_args(argv)
    if args.review_paths and args.reviews_dir is not None:
        parser.error("--review and --reviews-dir are mutually exclusive")
    if args.reviews_dir is not None:
        args.review_paths = [
            args.reviews_dir / f"review-{suffix}.jsonl"
            for suffix in ("a", "b", "c", "d")
        ]
    elif not args.review_paths:
        args.review_paths = list(DEFAULT_REVIEW_PATHS)
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        document = build_curation(
            review_paths=tuple(args.review_paths),
            cross_dedupe_path=args.cross_dedupe,
            eligible_path=args.eligible_jsonl,
            full_path=args.full_jsonl,
            parent_catalog_path=args.parent_catalog,
            contract_path=args.contract,
            source_registry_path=args.source_registry,
        )
        payload = encoded_document(document)
        if args.check:
            try:
                observed = args.output.read_bytes()
            except OSError as error:
                raise CurationError(f"cannot read curation output for --check: {error}") from error
            if observed != payload:
                raise CurationError("curation output bytes differ from deterministic rebuild")
            action = "checked"
        else:
            atomic_write(args.output, payload)
            action = "wrote"
        print(
            f"PASS build_openconjecture_curation_v5_2 ({action}) "
            f"candidates={document['counts']['candidates']} "
            f"accepted={document['counts']['accepted']} "
            f"authority_sha256={document['authority_sha256']}"
        )
        return 0
    except (CurationError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"FAIL build_openconjecture_curation_v5_2: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
