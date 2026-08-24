#!/usr/bin/env python3
"""Build the immutable, append-only Stage5 mathematics release 5.2.

This generator is deliberately standalone.  It authenticates release 5.1,
the versioned 5.2 authorities, both pinned OpenConjecture JSONL assets, and the
external curation ledger before constructing any release bytes.  Publishing
uses an exclusive advisory lock, an immutable-directory rename, and a
compare-and-swap update of ``Current_Release.json``.

The source contains LaTeX conjecture environments.  No Lean declaration,
formalization, elaboration, kernel check, proof, or independent current-status
review is manufactured by this program.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from typing import Any, Iterable, Iterator, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_ROOT = REPO_ROOT / "Docs/catalog/v5"
RELEASE = "5.2"
PARENT_RELEASE = "5.1"
REVIEW_DATE = "2026-08-10"
SOURCE_ID = "SRC-MATH-V5-OPENCONJECTURE-FA03D85"

CONTRACT_PATH = CATALOG_ROOT / "Stage5_Math_Expansion_Contract_v5_2.json"
SCHEMA_PATH = CATALOG_ROOT / "Math_Claim_Record_Schema_v5_2.json"
SOURCE_REGISTRY_PATH = CATALOG_ROOT / "Math_Source_Registry_v5_2.json"
STRICT_RECEIPT_PATH = CATALOG_ROOT / "V5_1_Strict_Conjecture_Receipt_v5_2.json"
CURATION_PATH = (
    CATALOG_ROOT / "curation/OpenConjecture_Curation_v5_2.json"
)
UPSTREAM_PATH = (
    CATALOG_ROOT / "sources/openconjecture-fa03d85-public.jsonl"
)
POOL_PATH = (
    CATALOG_ROOT / "sources/openconjecture-fa03d85-cc-by-real-conf090.jsonl"
)
PARENT_DIR = CATALOG_ROOT / "releases" / PARENT_RELEASE

UPSTREAM_SHA256 = "8cf0a7ce4baff47769fe1ca0c40b11eed0767480c858c208a7beae8f5829dd14"
UPSTREAM_SIZE_BYTES = 9_695_990
POOL_SHA256 = "8a698e3af53ca0605a2a8ecd2e3a9944ad84157440a86f3c319effaf9792c6ce"
POOL_SIZE_BYTES = 2_490_006
GITHUB_COMMIT = "d2e3afe62098611fabd7236998acc73f64e4b3b7"
HUGGINGFACE_COMMIT = "fa03d85db95e6edad4ff751b490704fa8a0d9358"

BASE_RELEASE_FILES = (
    "Claim_Catalog.json",
    "Claim_ID_Registry.json",
    "Stage5_Claim_ID_Registry.json",
    "Migration_v4_to_v5.json",
    "Theorem_List.json",
    "Open_Claim_List.json",
    "Coverage_Ledger.json",
)
# Release 5.2 adds an explicit effective-credit surface.  It is generated,
# sealed, and release-root-bound; the external curation ledger remains an input.
STRICT_LEDGER_NAME = "Strict_Conjecture_Ledger.json"
RELEASE_FILES = BASE_RELEASE_FILES + (STRICT_LEDGER_NAME,)
MANIFEST_NAME = "Release_Manifest.json"
CURRENT_NAME = "Current_Release.json"
LOCK_NAME = ".Current_Release.lock"

PARENT_ATV_HIGH_WATERMARK = 5_984
PARENT_ATF_HIGH_WATERMARK = 5_754
NEW_ROWS = 600
LAST_ATV_ORDINAL = 6_584
LAST_ATF_ORDINAL = 6_354

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SEMANTIC_KEY_RE = re.compile(r"^openconjecture-semantic/[0-9a-f]{64}$")
ARXIV_RE = re.compile(r"^(?P<base>[0-9]{4}\.[0-9]{4,5})v(?P<version>[1-9][0-9]*)$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")


class GenerationError(RuntimeError):
    """An authenticated input or generated invariant failed closed."""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def encoded_document(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise GenerationError(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return sha256_bytes(
        canonical_json_bytes({key: item for key, item in value.items() if key not in omitted})
    )


def document_sha256(value: Mapping[str, Any]) -> str:
    return hash_without(value, "authority_sha256")


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result.pop("authority_sha256", None)
    result["authority_sha256"] = document_sha256(result)
    return result


def seal_field(value: Mapping[str, Any], field: str, *also_omit: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    result[field] = hash_without(result, field, *also_omit)
    return result


def load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GenerationError(f"cannot load JSON object {path}: {error}") from error
    if not isinstance(value, dict):
        raise GenerationError(f"JSON authority must be an object: {path}")
    return value, raw


def verify_seal(value: Mapping[str, Any], label: str) -> str:
    observed = value.get("authority_sha256")
    if not isinstance(observed, str) or not SHA256_RE.fullmatch(observed):
        raise GenerationError(f"missing or invalid authority_sha256 in {label}")
    expected = document_sha256(value)
    if observed != expected:
        raise GenerationError(f"stale authority_sha256 in {label}")
    return observed


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GenerationError(message)


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical_json_bytes(sorted(values)))


def ordinal(identifier: str, pattern: re.Pattern[str], label: str) -> int:
    match = pattern.fullmatch(identifier)
    if match is None:
        raise GenerationError(f"invalid {label}: {identifier!r}")
    return int(match.group(1))


def relative_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError as error:
        raise GenerationError(f"authority path is outside repository: {path}") from error


def authority_binding(path: Path, value: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "path": relative_path(path),
        "file_sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
        "authority_sha256": value["authority_sha256"],
    }


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise GenerationError(f"unsupported JSON Schema type {expected!r}")


def validate_schema_instance(
    value: Any,
    schema: Mapping[str, Any],
    root: Mapping[str, Any],
    location: str = "$",
) -> None:
    """Validate the closed subset of Draft 2020-12 used by the 5.2 schema."""
    reference = schema.get("$ref")
    if reference is not None:
        if not isinstance(reference, str) or not reference.startswith("#/"):
            raise GenerationError(f"unsupported schema reference at {location}: {reference}")
        target: Any = root
        for component in reference[2:].split("/"):
            target = target[component.replace("~1", "/").replace("~0", "~")]
        validate_schema_instance(value, target, root, location)
        return
    for subschema in schema.get("allOf", []):
        validate_schema_instance(value, subschema, root, location)
    conditional = schema.get("if")
    if isinstance(conditional, dict):
        try:
            validate_schema_instance(value, conditional, root, location)
        except GenerationError:
            matches_condition = False
        else:
            matches_condition = True
        branch = schema.get("then" if matches_condition else "else")
        if isinstance(branch, dict):
            validate_schema_instance(value, branch, root, location)
    if "const" in schema and value != schema["const"]:
        raise GenerationError(f"schema const mismatch at {location}")
    if "enum" in schema and value not in schema["enum"]:
        raise GenerationError(f"schema enum mismatch at {location}: {value!r}")
    expected_type = schema.get("type")
    if expected_type is not None:
        accepted = [expected_type] if isinstance(expected_type, str) else expected_type
        if not any(_json_type_matches(value, item) for item in accepted):
            raise GenerationError(f"schema type mismatch at {location}: {accepted}")
    if isinstance(value, dict):
        required = schema.get("required", [])
        missing = [item for item in required if item not in value]
        if missing:
            raise GenerationError(f"schema missing fields at {location}: {missing}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            if extras:
                raise GenerationError(f"schema extra fields at {location}: {extras}")
        for key, item in value.items():
            child = properties.get(key)
            if isinstance(child, dict):
                validate_schema_instance(item, child, root, f"{location}.{key}")
    if isinstance(value, list):
        minimum = schema.get("minItems")
        if minimum is not None and len(value) < minimum:
            raise GenerationError(f"schema minItems mismatch at {location}")
        maximum = schema.get("maxItems")
        if maximum is not None and len(value) > maximum:
            raise GenerationError(f"schema maxItems mismatch at {location}")
        if schema.get("uniqueItems") and len({canonical_json_bytes(x) for x in value}) != len(value):
            raise GenerationError(f"schema uniqueItems mismatch at {location}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_schema_instance(item, item_schema, root, f"{location}[{index}]")
        contains = schema.get("contains")
        if isinstance(contains, dict):
            matches = 0
            for index, item in enumerate(value):
                try:
                    validate_schema_instance(item, contains, root, f"{location}[{index}]")
                except GenerationError:
                    continue
                matches += 1
            minimum_contains = int(schema.get("minContains", 1))
            maximum_contains = schema.get("maxContains")
            if matches < minimum_contains or (
                maximum_contains is not None and matches > int(maximum_contains)
            ):
                raise GenerationError(f"schema contains mismatch at {location}")
    if isinstance(value, str):
        if len(value) < int(schema.get("minLength", 0)):
            raise GenerationError(f"schema minLength mismatch at {location}")
        pattern = schema.get("pattern")
        if pattern is not None and re.search(pattern, value) is None:
            raise GenerationError(f"schema pattern mismatch at {location}: {value!r}")
        format_name = schema.get("format")
        if format_name == "date" and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:
            raise GenerationError(f"schema date mismatch at {location}")
        if format_name == "date-time" and re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})",
            value,
        ) is None:
            raise GenerationError(f"schema date-time mismatch at {location}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise GenerationError(f"schema minimum mismatch at {location}")
        if "maximum" in schema and value > schema["maximum"]:
            raise GenerationError(f"schema maximum mismatch at {location}")


def primary_row_count(document: Mapping[str, Any]) -> int:
    candidates = document.get("candidate_dispositions")
    coverage = document.get("msc_coverage")
    if isinstance(candidates, list) and isinstance(coverage, list):
        return len(candidates) + len(coverage)
    strict_credits = document.get("strict_credits")
    credit_corrections = document.get("credit_corrections")
    if isinstance(strict_credits, list) and isinstance(credit_corrections, list):
        return len(strict_credits) + len(credit_corrections)
    for key in (
        "records",
        "variants",
        "mappings",
        "migrations",
        "entries",
        "rows",
    ):
        rows = document.get(key)
        if isinstance(rows, list):
            return len(rows)
    return 0


def release_root(inventory: Sequence[Mapping[str, Any]]) -> str:
    payload = [
        {
            "path": row["path"],
            "sha256": row["sha256"],
            "size_bytes": row["size_bytes"],
        }
        for row in sorted(inventory, key=lambda item: str(item["path"]))
    ]
    return sha256_bytes(canonical_json_bytes(payload))


def verify_parent_release(contract: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    parent_contract = contract["parent"]
    require(parent_contract["release"] == PARENT_RELEASE, "contract parent release drifted")
    manifest_path = REPO_ROOT / parent_contract["manifest_path"]
    require(manifest_path == PARENT_DIR / MANIFEST_NAME, "parent manifest path drifted")
    manifest, manifest_raw = load_json(manifest_path)
    verify_seal(manifest, str(manifest_path))
    require(
        sha256_bytes(manifest_raw) == parent_contract["manifest_file_sha256"],
        "parent manifest file SHA-256 drifted",
    )
    require(
        manifest["authority_sha256"] == parent_contract["manifest_authority_sha256"],
        "parent manifest authority drifted",
    )
    require(manifest.get("release") == PARENT_RELEASE, "wrong parent manifest release")
    require(
        manifest.get("release_root_sha256") == parent_contract["release_root_sha256"],
        "parent release root differs from contract",
    )
    inventory = manifest.get("artifacts")
    require(isinstance(inventory, list), "parent manifest artifact inventory is invalid")
    names = {item.get("path") for item in inventory}
    require(names == set(BASE_RELEASE_FILES), "parent artifact name set drifted")
    actual_names = {item.name for item in PARENT_DIR.iterdir() if item.is_file()}
    non_files = [item.name for item in PARENT_DIR.iterdir() if not item.is_file()]
    require(
        actual_names == set(BASE_RELEASE_FILES) | {MANIFEST_NAME} and not non_files,
        "parent release directory is not the exact immutable artifact set",
    )
    documents: dict[str, dict[str, Any]] = {}
    rebuilt: list[dict[str, Any]] = []
    for entry in inventory:
        name = entry["path"]
        path = PARENT_DIR / name
        raw = path.read_bytes()
        require(len(raw) == entry["size_bytes"], f"parent artifact size drift: {name}")
        require(sha256_bytes(raw) == entry["sha256"], f"parent artifact hash drift: {name}")
        value, _ = load_json(path)
        verify_seal(value, str(path))
        require(primary_row_count(value) == entry["row_count"], f"parent row count drift: {name}")
        rebuilt.append(entry)
        documents[name] = value
    require(
        release_root(rebuilt) == parent_contract["release_root_sha256"],
        "parent release root does not recompute",
    )
    catalog = documents["Claim_Catalog.json"]
    registry = documents["Claim_ID_Registry.json"]
    require(len(catalog.get("records", [])) == 2_500, "parent catalog is not 2,500 rows")
    require(
        sha256_file(PARENT_DIR / "Claim_Catalog.json")
        == parent_contract["claim_catalog_file_sha256"],
        "parent catalog bytes drifted",
    )
    require(
        catalog["authority_sha256"] == parent_contract["claim_catalog_authority_sha256"],
        "parent catalog authority drifted",
    )
    require(
        registry["authority_sha256"]
        == parent_contract["claim_id_registry_authority_sha256"],
        "parent registry authority drifted",
    )
    require(
        registry["namespace_high_watermarks"]["ATV"] == PARENT_ATV_HIGH_WATERMARK,
        "parent ATV high-watermark drifted",
    )
    documents[MANIFEST_NAME] = manifest
    return documents


def verify_authorities() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    contract, contract_raw = load_json(CONTRACT_PATH)
    verify_seal(contract, str(CONTRACT_PATH))
    require(contract.get("release") == RELEASE, "wrong 5.2 contract release")
    authorities: dict[str, dict[str, Any]] = {}
    path_by_key = {
        "record_schema": SCHEMA_PATH,
        "source_registry": SOURCE_REGISTRY_PATH,
        "parent_strict_receipt": STRICT_RECEIPT_PATH,
    }
    for key, path in path_by_key.items():
        specification = contract["versioned_authorities"][key]
        require(relative_path(path) == specification["path"], f"{key} path drifted")
        value, raw = load_json(path)
        verify_seal(value, str(path))
        require(sha256_bytes(raw) == specification["file_sha256"], f"{key} file hash drifted")
        require(
            value["authority_sha256"] == specification["authority_sha256"],
            f"{key} authority hash drifted",
        )
        authorities[key] = value
    schema = authorities["record_schema"]
    sources = authorities["source_registry"]
    receipt = authorities["parent_strict_receipt"]
    require(
        sources["sources"][0]["source_id"] == SOURCE_ID,
        "v5.2 source-registry source ID drifted",
    )
    curation, _ = load_json(CURATION_PATH)
    verify_seal(curation, str(CURATION_PATH))
    curation_contract = contract["curation_ledger_contract"]
    require(relative_path(CURATION_PATH) == curation_contract["path"], "curation path drifted")
    if curation_contract.get("authority_sha256") is not None:
        require(
            curation["authority_sha256"]
            == curation_contract["authority_sha256"],
            "curation authority differs from the contract binding",
        )
    if curation_contract.get("file_sha256") is not None:
        require(
            sha256_file(CURATION_PATH) == curation_contract["file_sha256"],
            "curation file differs from the contract binding",
        )
    expected_top = set(curation_contract["required_top_level_fields"])
    require(set(curation) == expected_top, "curation ledger top-level field set drifted")
    return contract, schema, sources, receipt, curation


def _parse_jsonl(path: Path, specification: Mapping[str, Any], canonical: bool) -> tuple[list[dict[str, Any]], list[bytes]]:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise GenerationError(f"cannot read JSONL asset {path}: {error}") from error
    require(len(payload) == specification["size_bytes"], f"asset size drifted: {path}")
    require(sha256_bytes(payload) == specification["sha256"], f"asset SHA-256 drifted: {path}")
    require(payload.endswith(b"\n"), f"JSONL asset lacks final LF: {path}")
    raw_lines = payload[:-1].split(b"\n")
    require(len(raw_lines) == specification["record_count"], f"JSONL count drifted: {path}")
    require(all(raw_lines), f"JSONL asset contains blank line: {path}")
    rows: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(raw_lines, start=1):
        try:
            row = json.loads(raw_line.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise GenerationError(f"{path}:{line_number}: invalid JSON: {error}") from error
        require(isinstance(row, dict), f"{path}:{line_number}: row is not an object")
        if canonical:
            require(
                raw_line == canonical_json_bytes(row),
                f"{path}:{line_number}: eligible-pool line is not canonical JSON",
            )
        rows.append(row)
    return rows, raw_lines


def _source_gate(row: Mapping[str, Any], include_version: bool) -> bool:
    base = bool(
        row.get("latest_label") == "real_open_conjecture"
        and row.get("latest_label_model") == "gpt-5-mini"
        and row.get("latest_assessment_version") == "gpt5mini-v5-open-exact-v1"
        and isinstance(row.get("latest_label_confidence"), (int, float))
        and not isinstance(row.get("latest_label_confidence"), bool)
        and float(row["latest_label_confidence"]) >= 0.9
        and isinstance(row.get("body_tex"), str)
        and bool(row["body_tex"].strip())
        and row.get("license_family") == "cc_by"
        and row.get("license_url") == "http://creativecommons.org/licenses/by/4.0/"
        and row.get("normalized_license_url") == "https://creativecommons.org/licenses/by/4.0/"
        and row.get("publication_decision") == "publish_text"
        and row.get("publication_text_allowed") is True
        and row.get("publication_text_reason") == "creativecommons_license_treated_as_publishable"
        and row.get("publication_policy_version") == "hf-publication-v2"
        and row.get("text_withheld") is False
    )
    if not base or not include_version:
        return base
    arxiv_id = row.get("arxiv_id")
    return bool(
        isinstance(arxiv_id, str)
        and ARXIV_RE.fullmatch(arxiv_id)
        and isinstance(row.get("source_url"), str)
        and row["source_url"].endswith(arxiv_id)
    )


def _version_key(row: Mapping[str, Any]) -> tuple[str, int, str, int]:
    arxiv_id = str(row["arxiv_id"])
    match = ARXIV_RE.fullmatch(arxiv_id)
    require(match is not None, f"unversioned arXiv ID in eligible row: {arxiv_id}")
    return (
        match.group("base"),
        int(match.group("version")),
        str(row.get("updated_at", "")),
        int(row["id"]),
    )


def load_and_verify_sources(contract: Mapping[str, Any]) -> tuple[
    list[dict[str, Any]], dict[str, tuple[int, int]], dict[str, str]
]:
    assets = contract["source_assets"]
    require(
        assets["upstream_public_jsonl"]["sha256"] == UPSTREAM_SHA256
        and assets["upstream_public_jsonl"]["size_bytes"]
        == UPSTREAM_SIZE_BYTES
        and assets["eligible_pool_jsonl"]["sha256"] == POOL_SHA256
        and assets["eligible_pool_jsonl"]["size_bytes"] == POOL_SIZE_BYTES
        and assets["pins"]["github_commit"] == GITHUB_COMMIT
        and assets["pins"]["huggingface_commit"] == HUGGINGFACE_COMMIT,
        "source asset pins differ from the closed 5.2 record schema",
    )
    upstream, _upstream_raw = _parse_jsonl(
        UPSTREAM_PATH, assets["upstream_public_jsonl"], canonical=False
    )
    pool, _pool_raw = _parse_jsonl(
        POOL_PATH, assets["eligible_pool_jsonl"], canonical=True
    )
    ids: dict[int, tuple[int, dict[str, Any]]] = {}
    for line_number, row in enumerate(upstream, start=1):
        record_id = row.get("id")
        require(
            isinstance(record_id, int) and not isinstance(record_id, bool) and record_id > 0,
            f"upstream line {line_number}: invalid source id",
        )
        require(record_id not in ids, f"duplicate upstream source id {record_id}")
        ids[record_id] = (line_number, row)
    before = [row for row in upstream if _source_gate(row, include_version=False)]
    require(len(before) == 931, "source admission count before locator gate drifted")
    winners: dict[str, dict[str, Any]] = {}
    for row in before:
        if not _source_gate(row, include_version=True):
            continue
        content_hash = row.get("content_hash")
        require(isinstance(content_hash, str) and SHA256_RE.fullmatch(content_hash), "invalid content hash")
        previous = winners.get(content_hash)
        if previous is None or _version_key(previous) < _version_key(row):
            winners[content_hash] = row
    rebuilt = sorted(winners.values(), key=lambda row: str(row["content_hash"]))
    require(rebuilt == pool, "eligible-pool rows do not exactly rebuild from upstream")
    require(len(pool) == 889, "eligible pool is not exactly 889 rows")
    content_hashes = [str(row["content_hash"]) for row in pool]
    require(len(set(content_hashes)) == len(content_hashes), "eligible content hashes are not unique")
    require(content_hashes == sorted(content_hashes), "eligible pool is not content-hash sorted")
    require(
        set_digest(content_hashes) == assets["eligible_pool_jsonl"]["content_hash_set_sha256"],
        "eligible content-hash set digest drifted",
    )
    require(
        sum(float(row["latest_interestingness_score"]) >= 0.50 for row in pool) == 742,
        "interestingness-floor pool count drifted",
    )
    locators: dict[str, tuple[int, int]] = {}
    source_hashes: dict[str, str] = {}
    for pool_line, row in enumerate(pool, start=1):
        record_id = int(row["id"])
        require(record_id in ids, f"pool row id {record_id} absent upstream")
        upstream_line, upstream_row = ids[record_id]
        require(upstream_row == row, f"pool row {pool_line} differs from upstream line {upstream_line}")
        content_hash = str(row["content_hash"])
        locators[content_hash] = (upstream_line, pool_line)
        source_hashes[content_hash] = sha256_bytes(canonical_json_bytes(row))
    return pool, locators, source_hashes


def paper_object(source: Mapping[str, Any]) -> dict[str, Any]:
    value = {
        "arxiv_id": source["arxiv_id"],
        "title": source["title"],
        "authors": list(source["authors"]),
        "published_at": source["published_at"],
        "updated_at": source["updated_at"],
        "categories": list(source["categories"]),
        "primary_category": source["primary_category"],
        "doi": source["doi"],
        "journal_ref": source["journal_ref"],
        "comments": source["comments"],
        "abs_url": source["abs_url"],
        "pdf_url": source["pdf_url"],
        "source_url": source["source_url"],
    }
    return seal_field(value, "metadata_payload_sha256")


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
    return seal_field(value, "model_label_payload_sha256")


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
    return seal_field(value, "rights_payload_sha256")


def verify_curation(
    contract: Mapping[str, Any],
    curation: Mapping[str, Any],
    pool: Sequence[dict[str, Any]],
    source_hashes: Mapping[str, str],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    ledger_contract = contract["curation_ledger_contract"]
    require(curation.get("schema_version") == "awesome-theorems/openconjecture-curation/5.2", "curation schema drifted")
    require(curation.get("source_id") == SOURCE_ID, "curation source ID drifted")
    require(
        curation.get("source_registry_authority_sha256")
        == contract["versioned_authorities"]["source_registry"]["authority_sha256"],
        "curation source-registry binding drifted",
    )
    require(
        curation.get("eligible_pool_sha256") == contract["source_assets"]["eligible_pool_jsonl"]["sha256"],
        "curation eligible-pool binding drifted",
    )
    dispositions = curation.get("candidate_dispositions")
    require(isinstance(dispositions, list) and len(dispositions) == 889, "curation must contain 889 rows")
    required_fields = set(ledger_contract["required_candidate_fields"]) | {
        "atomic_statement_summary",
        "importance_assessment",
        "review_reason_codes",
        "review_notes",
        "review_fragment_sha256",
    }
    allowed_dispositions = set(ledger_contract["disposition_enum"])
    pool_by_hash = {str(row["content_hash"]): row for row in pool}
    observed_hashes: set[str] = set()
    accepted: list[tuple[dict[str, Any], dict[str, Any]]] = []
    accepted_semantics: set[str] = set()
    accepted_ranks: set[int] = set()
    for index, raw_row in enumerate(dispositions, start=1):
        require(isinstance(raw_row, dict), f"curation row {index} is not an object")
        require(set(raw_row) == required_fields, f"curation row {index} field set drifted")
        row = dict(raw_row)
        require(row["row_sha256"] == hash_without(row, "row_sha256"), f"curation row {index} hash drifted")
        require(
            isinstance(row["atomic_statement_summary"], str)
            and bool(row["atomic_statement_summary"].strip()),
            f"curation row {index} lacks an atomic statement summary",
        )
        require(
            row["importance_assessment"] in {"high", "medium", "low"},
            f"curation row {index} has invalid importance assessment",
        )
        review_codes = row["review_reason_codes"]
        require(
            isinstance(review_codes, list)
            and bool(review_codes)
            and all(isinstance(value, str) and value for value in review_codes)
            and len(review_codes) == len(set(review_codes)),
            f"curation row {index} has invalid review reason codes",
        )
        require(
            isinstance(row["review_notes"], str),
            f"curation row {index} has invalid review notes",
        )
        require(
            isinstance(row["review_fragment_sha256"], str)
            and SHA256_RE.fullmatch(row["review_fragment_sha256"]) is not None,
            f"curation row {index} has invalid review-fragment digest",
        )
        content_hash = row["content_hash"]
        require(isinstance(content_hash, str) and content_hash in pool_by_hash, f"curation row {index} is outside pool")
        require(content_hash not in observed_hashes, f"duplicate curation content hash {content_hash}")
        observed_hashes.add(content_hash)
        source = pool_by_hash[content_hash]
        source_sha = source_hashes[content_hash]
        body_sha = sha256_bytes(str(source["body_tex"]).encode("utf-8"))
        require(row["candidate_key"] == f"openconjecture:{content_hash}", f"curation candidate key drift at row {index}")
        require(row["source_record_id"] == source["id"], f"curation source id mismatch at row {index}")
        require(row["source_record_sha256"] == source_sha, f"curation source hash mismatch at row {index}")
        require(row["body_tex_sha256"] == body_sha, f"curation body hash mismatch at row {index}")
        require(row["arxiv_id"] == source["arxiv_id"], f"curation arXiv mismatch at row {index}")
        require(
            row["interestingness_score"] == source["latest_interestingness_score"],
            f"curation score mismatch at row {index}",
        )
        require(
            row["rights_payload_sha256"] == rights_object(source)["rights_payload_sha256"],
            f"curation rights hash mismatch at row {index}",
        )
        require(
            row["model_label_payload_sha256"]
            == model_label_object(source)["model_label_payload_sha256"],
            f"curation model-label hash mismatch at row {index}",
        )
        require(row["disposition"] in allowed_dispositions, f"invalid curation disposition at row {index}")
        is_accepted = row["disposition"] == "accepted_new_strict_open_claim"
        if is_accepted:
            semantic_key = row["semantic_key"]
            require(isinstance(semantic_key, str) and SEMANTIC_KEY_RE.fullmatch(semantic_key), f"invalid accepted semantic key at row {index}")
            summary = row.get("atomic_statement_summary")
            require(
                isinstance(summary, str) and bool(summary.strip()),
                f"accepted semantic payload lacks an atomic summary at row {index}",
            )
            require(
                row["semantic_key_payload_sha256"]
                == sha256_bytes(
                    canonical_json_bytes(
                        {
                            "semantic_key": semantic_key,
                            "atomic_statement_summary": summary,
                        }
                    )
                ),
                f"semantic-key payload hash mismatch at row {index}",
            )
            require(semantic_key not in accepted_semantics, f"duplicate accepted semantic key {semantic_key}")
            accepted_semantics.add(semantic_key)
            rank = row["selected_rank"]
            require(isinstance(rank, int) and not isinstance(rank, bool) and 1 <= rank <= NEW_ROWS, f"invalid selected rank at row {index}")
            require(rank not in accepted_ranks, f"duplicate selected rank {rank}")
            accepted_ranks.add(rank)
            expected_ordinal = PARENT_ATV_HIGH_WATERMARK + rank
            require(row["target_variant_id"] == f"ATV-{expected_ordinal:08d}", f"target ATV/rank mismatch at row {index}")
            require(row["target_s5_id"] == f"S5-CLM-{expected_ordinal:08d}", f"target S5/rank mismatch at row {index}")
            require(row["grants_catalog_entry"] is True and row["grants_strict_conjecture_credit"] is True, f"accepted grants mismatch at row {index}")
            require(float(source["latest_interestingness_score"]) >= 0.50, f"accepted row below interest floor at row {index}")
            require(
                row.get("importance_assessment") in {"high", "medium"},
                f"accepted row lacks high/medium curator importance at row {index}",
            )
            require(
                not any("split" in value.casefold() for value in review_codes)
                and "split" not in str(row["reason_code"]).casefold(),
                f"needs-split row selected at row {index}",
            )
            require(row["duplicate_of_semantic_key"] is None and row["duplicate_of_variant_id"] is None, f"accepted duplicate linkage at row {index}")
            accepted.append((row, source))
        else:
            require(row["selected_rank"] is None, f"nonaccepted selected rank at row {index}")
            require(row["target_variant_id"] is None and row["target_s5_id"] is None, f"nonaccepted target ID at row {index}")
            require(row["grants_catalog_entry"] is False and row["grants_strict_conjecture_credit"] is False, f"nonaccepted grant at row {index}")
    require(observed_hashes == set(pool_by_hash), "curation is not an exact pool partition")
    require(len(accepted) == NEW_ROWS, "curation does not accept exactly 600 rows")
    require(accepted_ranks == set(range(1, NEW_ROWS + 1)), "selected ranks are not exactly 1..600")
    accepted.sort(key=lambda pair: int(pair[0]["selected_rank"]))
    counts = curation.get("counts")
    require(isinstance(counts, dict), "curation counts is not an object")
    observed_counts = Counter(row["disposition"] for row in dispositions)
    if "candidates" in counts:
        require(counts["candidates"] == 889, "curation candidate count drifted")
    if "accepted" in counts:
        require(counts["accepted"] == 600, "curation accepted count drifted")
    if "nonaccepted" in counts:
        require(counts["nonaccepted"] == 289, "curation nonaccepted count drifted")
    by_disposition = counts.get("by_disposition")
    if by_disposition is not None:
        require(
            isinstance(by_disposition, dict)
            and set(observed_counts) <= set(by_disposition) <= allowed_dispositions
            and all(
                isinstance(value, int)
                and not isinstance(value, bool)
                and value == observed_counts[key]
                for key, value in by_disposition.items()
            ),
            "curation disposition counts drifted",
        )
    digests = curation.get("set_digests")
    require(isinstance(digests, dict), "curation set_digests is not an object")
    expected_sets = {
        "eligible_content_hash_set_sha256": set_digest(pool_by_hash),
        "accepted_content_hash_set_sha256": set_digest(row["content_hash"] for row, _ in accepted),
        "accepted_semantic_key_set_sha256": set_digest(row["semantic_key"] for row, _ in accepted),
        "accepted_s5_id_set_sha256": set_digest(row["target_s5_id"] for row, _ in accepted),
    }
    for key, expected in expected_sets.items():
        if key in digests:
            require(digests[key] == expected, f"curation set digest drifted: {key}")
    require(
        {"accepted_content_hash_set_sha256", "accepted_semantic_key_set_sha256", "accepted_s5_id_set_sha256"}
        <= set(digests),
        "curation omits a required accepted-set digest",
    )
    return accepted


def source_locator_object(
    source: Mapping[str, Any],
    upstream_line: int,
    pool_line: int,
    source_record_sha256: str,
) -> dict[str, Any]:
    return {
        "source_id": SOURCE_ID,
        "upstream_asset_path": relative_path(UPSTREAM_PATH),
        "upstream_asset_sha256": UPSTREAM_SHA256,
        "upstream_asset_size_bytes": UPSTREAM_SIZE_BYTES,
        "eligible_pool_path": relative_path(POOL_PATH),
        "eligible_pool_sha256": POOL_SHA256,
        "eligible_pool_size_bytes": POOL_SIZE_BYTES,
        "github_commit": GITHUB_COMMIT,
        "huggingface_commit": HUGGINGFACE_COMMIT,
        "upstream_line_number": upstream_line,
        "eligible_pool_line_number": pool_line,
        "source_record_id": source["id"],
        "source_record_sha256": source_record_sha256,
        "arxiv_id": source["arxiv_id"],
        "source_url": source["source_url"],
        "source_file": source["source_file"],
        "index_in_file": source["index_in_file"],
        "line_start": source["start_line"],
        "line_end": source["end_line"],
        "content_hash": source["content_hash"],
    }


def build_claim_row(
    ledger_row: Mapping[str, Any],
    source: Mapping[str, Any],
    locators: Mapping[str, tuple[int, int]],
    source_hashes: Mapping[str, str],
    parent_registry_authority: str,
    parent_release_root: str,
    curation_authority: str,
    schema: Mapping[str, Any],
) -> dict[str, Any]:
    content_hash = str(source["content_hash"])
    source_sha = source_hashes[content_hash]
    upstream_line, pool_line = locators[content_hash]
    rank = int(ledger_row["selected_rank"])
    atv_ordinal = PARENT_ATV_HIGH_WATERMARK + rank
    atf_ordinal = PARENT_ATF_HIGH_WATERMARK + rank
    semantic_key = str(ledger_row["semantic_key"])
    body_tex = str(source["body_tex"])
    plain_text = str(source["plain_text"])
    body_sha = sha256_bytes(body_tex.encode("utf-8"))
    plain_sha = sha256_bytes(plain_text.encode("utf-8"))

    locator = source_locator_object(
        source, upstream_line, pool_line, source_sha
    )
    source_block = {
        "language": "LaTeX",
        "block_kind": "source_conjecture_environment",
        "extraction_scope": "exact_upstream_body_tex_field",
        "body_tex": body_tex,
        "body_tex_sha256": body_sha,
        "plain_text": plain_text,
        "plain_text_sha256": plain_sha,
        "content_hash": content_hash,
        "source_record_sha256": source_sha,
    }
    paper = paper_object(source)
    model_label = model_label_object(source)
    rights = rights_object(source)
    curator_disposition = {
        "ledger_path": relative_path(CURATION_PATH),
        "ledger_authority_sha256": curation_authority,
        "ledger_row_sha256": ledger_row["row_sha256"],
        "candidate_key": ledger_row["candidate_key"],
        "selected_rank": rank,
        "disposition": "accepted_new_strict_open_claim",
        "basis": "curator_accepted_after_closed_source_semantic_nonclaim_and_rights_gates",
        "grants_release_entry": True,
        "grants_strict_conjecture_credit": True,
        "human_status_review_performed": False,
        "duplicate_of_variant_id": None,
        "reviewed_as_of": REVIEW_DATE,
    }
    curator_disposition["disposition_payload_sha256"] = hash_without(
        curator_disposition, "ledger_row_sha256", "disposition_payload_sha256"
    )
    mathematical_statement = {
        "language": "LaTeX",
        "representation": "verbatim_source_conjecture_block",
        "completeness": "exact_source_body_tex_plus_upstream_plain_text",
        "component_extraction_status": "not_separately_parsed",
        "body_tex": body_tex,
        "body_tex_sha256": body_sha,
        "plain_text": plain_text,
        "plain_text_sha256": plain_sha,
    }
    mathematical_statement = seal_field(
        mathematical_statement, "statement_sha256"
    )
    statement_sha = mathematical_statement["statement_sha256"]
    status_detail = seal_field(
        {
            "status_as_of": REVIEW_DATE,
            "basis": "pinned OpenConjecture source/model label preserved as a source assertion",
            "evidence_level": "source_dataset_model_assertion",
            "source_refs": [SOURCE_ID],
            "resolution_criterion": "prove or refute the exact source LaTeX conjecture block under its stated context",
            "independent_current_status_review": False,
        },
        "status_payload_sha256",
    )
    categories = list(source["categories"])
    primary_category = str(source["primary_category"])
    classification_status = (
        "source_metadata_missing"
        if not categories and not primary_category
        else "source_metadata_only"
    )
    classification = seal_field(
        {
            "source_categories": categories,
            "source_primary_category": primary_category,
            "classification_system": "arXiv",
            "classification_status": classification_status,
            "msc_codes": [],
            "msc_status": "unassigned",
        },
        "classification_payload_sha256",
    )
    provenance = seal_field(
        {
            "source_refs": [SOURCE_ID],
            "extraction_mode": "exact_jsonl_record_and_verbatim_latex_block",
            "extractor_version": "1.0.0",
            "extractor_schema_version": "awesome-theorems/openconjecture-eligible-pool/5.2",
            "source_record_sha256": source_sha,
            "eligible_pool_sha256": POOL_SHA256,
            "curation_ledger_path": relative_path(CURATION_PATH),
            "curation_ledger_authority_sha256": curation_authority,
            "curation_ledger_row_sha256": ledger_row["row_sha256"],
            "source_assertion_not_independent_truth_review": True,
            "no_formalization_claimed": True,
        },
        "provenance_payload_sha256",
    )
    allocation_request = {
        "origin_release": RELEASE,
        "source_id": SOURCE_ID,
        "content_hash": content_hash,
        "semantic_key": semantic_key,
        "statement_sha256": statement_sha,
        "family_action": "new_family",
    }
    allocation = {
        "parent_release_root_sha256": parent_release_root,
        "parent_registry_authority_sha256": parent_registry_authority,
        "allocation_request_sha256": sha256_bytes(
            canonical_json_bytes(allocation_request)
        ),
        "transaction_id": f"S5-ALLOC-{atv_ordinal:08d}",
        "family_action": "new_family",
        "append_only": True,
    }
    normalized_latex = " ".join(body_tex.split())
    identity_payload = {
        "semantic_key": semantic_key,
        "content_hash": content_hash,
        "statement_sha256": statement_sha,
        "source_record_sha256": source_sha,
    }
    dedupe = {
        "identity_payload_sha256": sha256_bytes(canonical_json_bytes(identity_payload)),
        "semantic_key": semantic_key,
        "semantic_key_sha256": sha256_bytes(semantic_key.encode("utf-8")),
        "content_hash": content_hash,
        "body_tex_sha256": body_sha,
        "normalized_latex_sha256": sha256_bytes(normalized_latex.encode("utf-8")),
        "source_record_sha256": source_sha,
        "candidate_atv_ids": [],
        "verdict": "unique_new_claim",
        "validation_status": "independent_machine_validated_exact",
        "content_hash_unique_in_eligible_pool": True,
        "semantic_key_unique_in_release": True,
        "duplicate_grants_quota": False,
        "no_evidence_or_status_inheritance": True,
    }
    display_name = str(ledger_row["atomic_statement_summary"])
    row: dict[str, Any] = {
        "schema_version": "awesome-theorems/stage5-math-claim-record/5.2",
        "release_id": RELEASE,
        "origin_stage": "Stage5",
        "origin_release": RELEASE,
        "curation_key": f"openconjecture/{content_hash}",
        "allocation": allocation,
        "occurrence_id": f"ATO-{atv_ordinal:08d}",
        "family_id": f"ATF-{atf_ordinal:08d}",
        "sense_id": f"ATS-{atv_ordinal:08d}",
        "variant_id": f"ATV-{atv_ordinal:08d}",
        "stage_claim_id": f"S5-CLM-{atv_ordinal:08d}",
        "display_name": display_name,
        "aliases": [str(source["title"])],
        "owner_domain": "mathematics",
        "membership_domains": ["mathematics"],
        "record_role": "claim",
        "claim_kind": "conjecture",
        "current_claim_kind": "conjecture",
        "historical_kind": "conjecture",
        "atomicity": "atomic",
        "atomicity_detail": {
            "allocation_unit": "one_exact_source_conjecture_environment",
            "whole_coherent_compound_block_allowed": True,
            "logical_irreducibility_asserted": False,
        },
        "truth_apt": True,
        "category": "open_claim",
        "material_status": "open",
        "source_id": SOURCE_ID,
        "source_locator": locator,
        "source_block": source_block,
        "paper": paper,
        "model_label": model_label,
        "curator_disposition": curator_disposition,
        "mathematical_statement": mathematical_statement,
        "status_detail": status_detail,
        "classification": classification,
        "provenance": provenance,
        "rights": rights,
        "dedupe": dedupe,
        "frontier": {
            "class": "source_model_asserted_open_frontier",
            "as_of": REVIEW_DATE,
            "basis": "pinned OpenConjecture real_open_conjecture label",
            "source_refs": [SOURCE_ID],
            "evidence_level": "source_model_label",
            "independent_review": False,
        },
        "importance": {
            "tier": "source_scored_research_interest",
            "basis": "source_model_interestingness_signal_only",
            "source_score": source["latest_interestingness_score"],
            "source_score_confidence": source["latest_interestingness_confidence"],
            "rationale": source["latest_interestingness_rationale"],
            "independent_ranking": False,
        },
        "lifecycle": "active",
        "lineage": [],
        "semantic_key": semantic_key,
    }
    row["content_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "source_block": row["source_block"],
                "mathematical_statement": row["mathematical_statement"],
            }
        )
    )
    row["source_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "source_locator": row["source_locator"],
                "paper": row["paper"],
                "model_label": row["model_label"],
            }
        )
    )
    row["semantic_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "record_role": row["record_role"],
                "atomicity": row["atomicity"],
                "truth_apt": row["truth_apt"],
                "category": row["category"],
                "current_claim_kind": row["current_claim_kind"],
                "semantic_key": row["semantic_key"],
                "statement_sha256": statement_sha,
            }
        )
    )
    validate_schema_instance(row, schema, schema)
    forbidden = set(
        (
            "qualified_name",
            "module",
            "namespace",
            "declaration_kind",
            "formal_shape",
            "formal_proof_state",
            "formal_declaration",
            "formal_type",
            "formal_docstring",
            "formal_statement",
        )
    )
    require(not (forbidden & set(row)), "a generated LaTeX row contains a fake Lean field")
    return row


def authoritative_inputs(
    contract: Mapping[str, Any],
    schema: Mapping[str, Any],
    sources: Mapping[str, Any],
    receipt: Mapping[str, Any],
    curation: Mapping[str, Any],
    parent: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "contract": authority_binding(CONTRACT_PATH, contract),
        "record_schema": authority_binding(SCHEMA_PATH, schema),
        "source_registry": authority_binding(SOURCE_REGISTRY_PATH, sources),
        "parent_strict_receipt": authority_binding(STRICT_RECEIPT_PATH, receipt),
        "curation_ledger": authority_binding(CURATION_PATH, curation),
        "upstream_asset": {
            "path": relative_path(UPSTREAM_PATH),
            "file_sha256": sha256_file(UPSTREAM_PATH),
            "size_bytes": UPSTREAM_PATH.stat().st_size,
        },
        "eligible_pool": {
            "path": relative_path(POOL_PATH),
            "file_sha256": sha256_file(POOL_PATH),
            "size_bytes": POOL_PATH.stat().st_size,
        },
        "parent_release": {
            "release": PARENT_RELEASE,
            "release_root_sha256": parent[MANIFEST_NAME]["release_root_sha256"],
            "manifest_file_sha256": sha256_file(PARENT_DIR / MANIFEST_NAME),
            "manifest_authority_sha256": parent[MANIFEST_NAME]["authority_sha256"],
            "registry_authority_sha256": parent["Claim_ID_Registry.json"]["authority_sha256"],
        },
    }


def new_registry_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]
]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in rows:
        request = row["allocation"]["allocation_request_sha256"]
        families.append(
            {
                "family_id": row["family_id"],
                "curation_key": row["curation_key"],
                "display_titles": [row["display_name"]] + list(row["aliases"]),
                "member_occurrence_ids": [row["occurrence_id"]],
                "historical_member_occurrence_ids": [row["occurrence_id"]],
                "idempotency_request_sha256": request,
                "identity_state": "stage5_curated_latex_exact_family",
                "lifecycle": "current",
                "semantic_equivalence_asserted": True,
            }
        )
        senses.append(
            {
                "sense_id": row["sense_id"],
                "family_id": row["family_id"],
                "bootstrap_occurrence_id": row["occurrence_id"],
                "curation_key": row["curation_key"],
                "idempotency_request_sha256": request,
                "identity_state": "stage5_curated_latex_exact_sense",
                "lifecycle": "current",
            }
        )
        variants.append(
            {
                "variant_id": row["variant_id"],
                "sense_id": row["sense_id"],
                "bootstrap_occurrence_id": row["occurrence_id"],
                "curation_key": row["curation_key"],
                "idempotency_request_sha256": request,
                "semantic_payload_sha256": row["semantic_payload_sha256"],
                "identity_state": "stage5_curated_latex_exact_variant",
                "lifecycle": "current",
            }
        )
    return families, senses, variants


def build_registry(
    parent: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    families, senses, variants = new_registry_rows(rows)
    require(len(families) == NEW_ROWS, "new registry-row cardinality drifted")
    document = {
        "schema_version": "awesome-theorems/claim-id-registry/5.2",
        "artifact": "Claim_ID_Registry.json",
        "release": RELEASE,
        "parent_registry_authority_sha256": parent["authority_sha256"],
        "baseline_registry_authority_sha256": parent["baseline_registry_authority_sha256"],
        "authoritative_inputs": copy.deepcopy(inputs),
        "allocation_policy": {
            **copy.deepcopy(parent["allocation_policy"]),
            "release_5_2_first_new_atv_ordinal": PARENT_ATV_HIGH_WATERMARK + 1,
            "release_5_2_new_family_first_atf_ordinal": PARENT_ATF_HIGH_WATERMARK + 1,
        },
        "namespace_high_watermarks": {
            "ATF": LAST_ATF_ORDINAL,
            "ATO": LAST_ATV_ORDINAL,
            "ATS": LAST_ATV_ORDINAL,
            "ATV": LAST_ATV_ORDINAL,
        },
        "families": copy.deepcopy(parent["families"]) + families,
        "senses": copy.deepcopy(parent["senses"]) + senses,
        "variants": copy.deepcopy(parent["variants"]) + variants,
        "legacy_aliases": copy.deepcopy(parent.get("legacy_aliases", [])),
        "redirects": copy.deepcopy(parent.get("redirects", [])),
        "splits": copy.deepcopy(parent.get("splits", [])),
        "family_membership_extensions": copy.deepcopy(
            parent.get("family_membership_extensions", [])
        ),
        "counts": {
            "families": len(parent["families"]) + NEW_ROWS,
            "senses": len(parent["senses"]) + NEW_ROWS,
            "variants": len(parent["variants"]) + NEW_ROWS,
            "stage4_variants": parent["counts"]["stage4_variants"],
            "stage5_additions": parent["counts"]["stage5_additions"] + NEW_ROWS,
            "legacy_aliases": len(parent.get("legacy_aliases", [])),
            "redirects": len(parent.get("redirects", [])),
            "splits": len(parent.get("splits", [])),
        },
    }
    result = seal(document)
    require(result["families"][: len(parent["families"])] == parent["families"], "family prefix changed")
    require(result["senses"][: len(parent["senses"])] == parent["senses"], "sense prefix changed")
    require(result["variants"][: len(parent["variants"])] == parent["variants"], "variant prefix changed")
    return result


def build_stage_registry(
    parent: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    additions = [
        {
            "ordinal": ordinal(str(row["variant_id"]), ATV_RE, "variant ID"),
            "variant_id": row["variant_id"],
            "predecessor_stage_claim_id": None,
            "stage_claim_id": row["stage_claim_id"],
            "lifecycle": "current",
        }
        for row in rows
    ]
    mappings = copy.deepcopy(parent["mappings"]) + additions
    require(
        [item["ordinal"] for item in additions]
        == list(range(PARENT_ATV_HIGH_WATERMARK + 1, LAST_ATV_ORDINAL + 1)),
        "new stage mappings are not contiguous",
    )
    result = seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-id-registry/5.2",
            "artifact": "Stage5_Claim_ID_Registry.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "numbering_policy": parent["numbering_policy"],
            "counts": {"mappings": len(mappings)},
            "mappings": mappings,
        }
    )
    require(
        result["mappings"][: len(parent["mappings"])] == parent["mappings"],
        "Stage5 mapping prefix changed",
    )
    return result


def build_migration(
    parent: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    additions: list[dict[str, Any]] = []
    for row in rows:
        item_ordinal = ordinal(str(row["variant_id"]), ATV_RE, "variant ID")
        additions.append(
            {
                "ordinal": item_ordinal,
                "variant_id": row["variant_id"],
                "v4_variant_id": None,
                "s4_claim_id": None,
                "stage_claim_id": row["stage_claim_id"],
                "migration_action": "new_stage5_allocation",
                "predecessor_record_sha256": None,
                "current_resolution": {
                    "kind": "current",
                    "terminal_atv_ids": [row["variant_id"]],
                    "terminal_s5_ids": [row["stage_claim_id"]],
                    "default_child": None,
                    "evidence_inherited": False,
                },
            }
        )
    migrations = copy.deepcopy(parent["migrations"]) + additions
    result = seal(
        {
            "schema_version": "awesome-theorems/migration-v4-to-v5/5.2",
            "artifact": "Migration_v4_to_v5.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "v4_import_receipt": copy.deepcopy(parent["v4_import_receipt"]),
            "counts": {
                "historical_bindings": parent["counts"]["historical_bindings"],
                "new_allocations": parent["counts"]["new_allocations"] + NEW_ROWS,
                "migrations": len(migrations),
            },
            "migrations": migrations,
        }
    )
    require(
        result["migrations"][: len(parent["migrations"])] == parent["migrations"],
        "migration prefix changed",
    )
    return result


def theorem_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "theorem"
        and row.get("current_claim_kind") == "theorem"
        and row.get("material_status") == "proved"
        and row.get("declaration_kind") == "theorem"
    )


def open_predicate(row: Mapping[str, Any]) -> bool:
    base = bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("current_claim_kind") in {"conjecture", "hypothesis", "open_problem"}
        and row.get("material_status") in {"open", "partial", "independent", "disputed"}
    )
    if not base:
        return False
    # Inherited records are Lean-native; 5.2 records are intentionally LaTeX-native.
    if row.get("origin_release") == RELEASE:
        return row.get("source_block", {}).get("language") == "LaTeX"
    return row.get("declaration_kind") == "theorem"


def build_catalog(
    parent: Mapping[str, Any],
    rows: Sequence[dict[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    parent_rows = parent["records"]
    records = copy.deepcopy(parent_rows) + list(rows)
    require(records[: len(parent_rows)] == parent_rows, "parent catalog records changed")
    require(len(records) == 3_100, "cumulative catalog must contain 3,100 rows")
    require(len({row["variant_id"] for row in records}) == len(records), "catalog ATV IDs are not unique")
    require(len({row["stage_claim_id"] for row in records}) == len(records), "catalog S5 IDs are not unique")
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-catalog/5.2",
            "artifact": "Claim_Catalog.json",
            "release": RELEASE,
            "catalog_scope": parent["catalog_scope"],
            "authoritative_inputs": copy.deepcopy(inputs),
            "counts": {
                "records": len(records),
                "origin_theorems": sum(theorem_predicate(row) for row in rows),
                "origin_open_claims": sum(open_predicate(row) for row in rows),
                "cumulative_theorems": sum(theorem_predicate(row) for row in records),
                "cumulative_open_claims": sum(open_predicate(row) for row in records),
            },
            "records": records,
        }
    )


def build_projection(
    name: str,
    catalog_rows: Sequence[dict[str, Any]],
    predicate: Any,
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    records = [row for row in catalog_rows if predicate(row)]
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-query-projection/5.2",
            "artifact": name,
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
            "stage_claim_ids": [row["stage_claim_id"] for row in records],
            "counts": {"records": len(records)},
            "records": records,
        }
    )


def build_coverage(
    parent: Mapping[str, Any],
    curation: Mapping[str, Any],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    additions: list[dict[str, Any]] = []
    for row in curation["candidate_dispositions"]:
        additions.append(
            {
                "candidate_key": row["candidate_key"],
                "source_id": SOURCE_ID,
                "source_record_id": row["source_record_id"],
                "source_record_sha256": row["source_record_sha256"],
                "content_hash": row["content_hash"],
                "semantic_key": row["semantic_key"],
                "disposition": row["disposition"],
                "reason_code": row["reason_code"],
                "target_variant_id": row["target_variant_id"],
                "target_s5_id": row["target_s5_id"],
                "duplicate_of_variant_id": row["duplicate_of_variant_id"],
                "grants_catalog_entry": row["grants_catalog_entry"],
                "grants_strict_conjecture_credit": row[
                    "grants_strict_conjecture_credit"
                ],
                "origin_release": RELEASE,
                "curation_row_sha256": row["row_sha256"],
            }
        )
    candidates = copy.deepcopy(parent["candidate_dispositions"]) + additions
    observed = Counter(item["disposition"] for item in additions)
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-coverage-ledger/5.2",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "candidate_dispositions": candidates,
            # 5.2 preserves the exact MSC coverage surface because the new source
            # supplies arXiv categories, not reviewed MSC assignments.
            "msc_coverage": copy.deepcopy(parent["msc_coverage"]),
            "counts": {
                "candidate_dispositions": len(candidates),
                "msc_coverage": len(parent["msc_coverage"]),
                "origin_5_2_candidates": len(additions),
                "origin_5_2_accepted_new_claims": observed[
                    "accepted_new_strict_open_claim"
                ],
                "origin_5_2_nonaccepted": len(additions)
                - observed["accepted_new_strict_open_claim"],
            },
        }
    )


def parent_syntactic_strict(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("origin_stage") == "Stage5"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("claim_kind") == "conjecture"
        and row.get("current_claim_kind") == "conjecture"
        and row.get("declaration_kind") == "theorem"
        and row.get("formal_shape") == "direct_prop"
        and row.get("material_status") == "open"
        and row.get("lifecycle") == "active"
    )


def record_evidence_components(row: Mapping[str, Any]) -> dict[str, str]:
    if row.get("origin_release") == RELEASE:
        content_hash = str(row["content_payload_sha256"])
        source_hash = str(row["source_payload_sha256"])
        rights_hash = str(row["rights"]["rights_payload_sha256"])
    else:
        content_hash = sha256_bytes(
            canonical_json_bytes(
                {
                    "formal_statement": row.get("formal_statement"),
                    "mathematical_statement": row.get("mathematical_statement"),
                }
            )
        )
        source_hash = sha256_bytes(
            canonical_json_bytes(
                {
                    "source_id": row.get("source_id"),
                    "locator": row.get("locator"),
                    "formal_statement": row.get("formal_statement"),
                    "provenance": row.get("provenance"),
                }
            )
        )
        rights_hash = sha256_bytes(canonical_json_bytes(row["rights"]))
    return {
        "record_sha256": sha256_bytes(canonical_json_bytes(row)),
        "content_payload_sha256": content_hash,
        "source_payload_sha256": source_hash,
        "rights_payload_sha256": rights_hash,
        "allocation_request_sha256": str(
            row["allocation"]["allocation_request_sha256"]
        ),
    }


def strict_credit_row(row: Mapping[str, Any], branch: str) -> dict[str, Any]:
    components = record_evidence_components(row)
    semantic_key = row.get("semantic_key")
    if not isinstance(semantic_key, str):
        semantic_key = "formal-conjectures-semantic/" + str(
            row["semantic_payload_sha256"]
        )
    value = {
        "stage_claim_id": row["stage_claim_id"],
        "variant_id": row["variant_id"],
        "origin_release": row["origin_release"],
        "credit_source_branch": branch,
        "semantic_key": semantic_key,
        "grants_strict_conjecture_credit": True,
        "evidence_sha256": sha256_bytes(canonical_json_bytes(components)),
    }
    return seal_field(value, "row_sha256")


def verify_parent_strict_receipt(
    parent_rows: Sequence[Mapping[str, Any]], receipt: Mapping[str, Any]
) -> tuple[list[Mapping[str, Any]], dict[str, Any]]:
    parent_binding = receipt["parent_release"]
    require(parent_binding["release"] == PARENT_RELEASE, "strict receipt parent release drifted")
    require(
        parent_binding["release_root_sha256"]
        == json.loads((PARENT_DIR / MANIFEST_NAME).read_text(encoding="utf-8"))[
            "release_root_sha256"
        ],
        "strict receipt parent root drifted",
    )
    require(
        parent_binding["manifest_file_sha256"]
        == sha256_file(PARENT_DIR / MANIFEST_NAME),
        "strict receipt parent manifest hash drifted",
    )
    require(
        parent_binding["claim_catalog_file_sha256"]
        == sha256_file(PARENT_DIR / "Claim_Catalog.json"),
        "strict receipt parent catalog hash drifted",
    )
    strict_rows = sorted(
        (row for row in parent_rows if parent_syntactic_strict(row)),
        key=lambda row: str(row["stage_claim_id"]),
    )
    strict_s5 = [str(row["stage_claim_id"]) for row in strict_rows]
    strict_atv = [str(row["variant_id"]) for row in strict_rows]
    rebuild = receipt["rebuild"]
    require(len(strict_rows) == rebuild["syntactic_strict_count"] == 401, "parent syntactic strict count drifted")
    require(set_digest(strict_s5) == rebuild["syntactic_strict_s5_id_set_sha256"], "parent strict S5 set digest drifted")
    require(set_digest(strict_atv) == rebuild["syntactic_strict_atv_id_set_sha256"], "parent strict ATV set digest drifted")
    open_rows = [row for row in parent_rows if open_predicate(row)]
    non_strict_s5 = sorted(
        str(row["stage_claim_id"])
        for row in open_rows
        if not parent_syntactic_strict(row)
    )
    require(len(non_strict_s5) == rebuild["non_strict_open_count"] == 599, "parent non-strict count drifted")
    require(set_digest(non_strict_s5) == rebuild["non_strict_open_s5_id_set_sha256"], "parent non-strict set digest drifted")
    corrections = receipt["effective_5_2_credit_corrections"]
    require(isinstance(corrections, list) and len(corrections) == 1, "strict receipt correction set drifted")
    correction = corrections[0]
    require(correction["stage_claim_id"] == "S5-CLM-00005311", "MovingSofa S5 correction drifted")
    require(correction["variant_id"] == "ATV-00005311", "MovingSofa ATV correction drifted")
    require(
        correction["effective_release"] == RELEASE
        and correction["effective_strict_credit"] is False
        and correction["disposition"] == "strict_credit_revoked"
        and correction["identity_changed"] is False
        and correction["parent_record_changed"] is False
        and correction["material_status_change_asserted"] is False
        and correction["proof_or_refutation_asserted"] is False,
        "MovingSofa correction semantics drifted",
    )
    require(
        set_digest([correction["stage_claim_id"]])
        == receipt["effective_parent_credit"]["revoked_s5_id_set_sha256"],
        "revoked strict-credit set digest drifted",
    )
    by_s5 = {str(row["stage_claim_id"]): row for row in strict_rows}
    require(correction["stage_claim_id"] in by_s5, "MovingSofa is not a syntactic strict parent row")
    target = by_s5[correction["stage_claim_id"]]
    require(
        sha256_bytes(canonical_json_bytes(target)) == correction["parent_record_sha256"],
        "MovingSofa parent-record hash drifted",
    )
    effective = [row for row in strict_rows if row["stage_claim_id"] != correction["stage_claim_id"]]
    effective_s5 = [str(row["stage_claim_id"]) for row in effective]
    require(len(effective) == 400, "effective parent strict set is not 400")
    require(
        set_digest(effective_s5)
        == receipt["effective_parent_credit"]["effective_strict_s5_id_set_sha256"],
        "effective parent strict digest drifted",
    )
    return effective, correction


def build_strict_ledger(
    parent_rows: Sequence[Mapping[str, Any]],
    new_rows: Sequence[Mapping[str, Any]],
    receipt: Mapping[str, Any],
    curation: Mapping[str, Any],
    parent_root: str,
) -> dict[str, Any]:
    effective_parent, receipt_correction = verify_parent_strict_receipt(
        parent_rows, receipt
    )
    credits = [
        strict_credit_row(row, "effective_parent_5_1_direct_prop")
        for row in effective_parent
    ] + [
        strict_credit_row(row, "origin_5_2_curated_latex_environment")
        for row in new_rows
    ]
    credits.sort(key=lambda row: str(row["stage_claim_id"]))
    require(len(credits) == 1_000, "effective strict-credit ledger is not 1,000 rows")
    require(len({row["stage_claim_id"] for row in credits}) == 1_000, "strict S5 IDs are not unique")
    require(len({row["variant_id"] for row in credits}) == 1_000, "strict ATV IDs are not unique")
    correction = {
        "stage_claim_id": receipt_correction["stage_claim_id"],
        "variant_id": receipt_correction["variant_id"],
        "disposition": "strict_credit_revoked",
        "effective_release": RELEASE,
        "grants_strict_conjecture_credit": False,
        "parent_record_sha256": receipt_correction["parent_record_sha256"],
        "receipt_authority_sha256": receipt["authority_sha256"],
    }
    document = {
        "schema_version": "awesome-theorems/stage5-strict-conjecture-ledger/5.2",
        "release": RELEASE,
        "parent_release_root_sha256": parent_root,
        "parent_strict_receipt_authority_sha256": receipt["authority_sha256"],
        "curation_ledger_authority_sha256": curation["authority_sha256"],
        "strict_credits": credits,
        "credit_corrections": [correction],
        "counts": {
            "effective_strict_credits": len(credits),
            "effective_parent_credits": len(effective_parent),
            "origin_5_2_credits": len(new_rows),
            "credit_corrections": 1,
        },
        "set_digests": {
            "effective_s5_id_set_sha256": set_digest(
                row["stage_claim_id"] for row in credits
            ),
            "effective_variant_id_set_sha256": set_digest(
                row["variant_id"] for row in credits
            ),
            "effective_parent_s5_id_set_sha256": set_digest(
                row["stage_claim_id"] for row in credits
                if row["credit_source_branch"] == "effective_parent_5_1_direct_prop"
            ),
            "origin_5_2_s5_id_set_sha256": set_digest(
                row["stage_claim_id"] for row in credits
                if row["credit_source_branch"]
                == "origin_5_2_curated_latex_environment"
            ),
        },
    }
    required_top = set(
        (
            "schema_version",
            "release",
            "parent_release_root_sha256",
            "parent_strict_receipt_authority_sha256",
            "curation_ledger_authority_sha256",
            "strict_credits",
            "credit_corrections",
            "counts",
            "set_digests",
            "authority_sha256",
        )
    )
    result = seal(document)
    require(set(result) == required_top, "strict ledger top-level field set drifted")
    return result


def package_release(
    artifacts: Mapping[str, Mapping[str, Any]],
    inputs: Mapping[str, Any],
    curation: Mapping[str, Any],
) -> tuple[dict[str, bytes], str]:
    require(set(artifacts) == set(RELEASE_FILES), "generated artifact name set drifted")
    encoded = {name: encoded_document(artifacts[name]) for name in RELEASE_FILES}
    inventory = [
        {
            "path": name,
            "sha256": sha256_bytes(encoded[name]),
            "size_bytes": len(encoded[name]),
            "row_count": primary_row_count(artifacts[name]),
        }
        for name in sorted(RELEASE_FILES)
    ]
    root = release_root(inventory)
    catalog_counts = artifacts["Claim_Catalog.json"]["counts"]
    strict = artifacts[STRICT_LEDGER_NAME]
    curation_digests = curation["set_digests"]
    manifest = seal(
        {
            "schema_version": "awesome-theorems/stage5-release-manifest/5.2",
            "release": RELEASE,
            "parent_release": PARENT_RELEASE,
            "parent_release_root_sha256": inputs["parent_release"][
                "release_root_sha256"
            ],
            "release_root_sha256": root,
            "authoritative_inputs": copy.deepcopy(inputs),
            "accepted_set_digests": {
                "content_hash_set_sha256": curation_digests[
                    "accepted_content_hash_set_sha256"
                ],
                "semantic_key_set_sha256": curation_digests[
                    "accepted_semantic_key_set_sha256"
                ],
                "s5_id_set_sha256": curation_digests[
                    "accepted_s5_id_set_sha256"
                ],
            },
            "strict_credit_binding": {
                "path": STRICT_LEDGER_NAME,
                "file_sha256": sha256_bytes(encoded[STRICT_LEDGER_NAME]),
                "authority_sha256": strict["authority_sha256"],
                "effective_s5_id_set_sha256": strict["set_digests"][
                    "effective_s5_id_set_sha256"
                ],
                "effective_variant_id_set_sha256": strict["set_digests"][
                    "effective_variant_id_set_sha256"
                ],
            },
            "artifacts": inventory,
            "counts": {
                "non_manifest_artifacts": len(inventory),
                "catalog_records": catalog_counts["records"],
                "origin_theorems": catalog_counts["origin_theorems"],
                "origin_open_claims": catalog_counts["origin_open_claims"],
                "cumulative_theorems": catalog_counts["cumulative_theorems"],
                "cumulative_open_claims": catalog_counts["cumulative_open_claims"],
                "effective_strict_conjecture_credits": strict["counts"][
                    "effective_strict_credits"
                ],
            },
        }
    )
    encoded[MANIFEST_NAME] = encoded_document(manifest)
    return encoded, root


def validate_generated(
    artifacts: Mapping[str, Mapping[str, Any]],
    parent: Mapping[str, Mapping[str, Any]],
    new_rows: Sequence[Mapping[str, Any]],
) -> None:
    for name, value in artifacts.items():
        require(value["authority_sha256"] == document_sha256(value), f"generated seal stale: {name}")
    catalog = artifacts["Claim_Catalog.json"]
    parent_catalog = parent["Claim_Catalog.json"]
    require(catalog["records"][:2_500] == parent_catalog["records"], "parent record equality failed")
    require(catalog["records"][2_500:] == list(new_rows), "catalog addition order drifted")
    require(catalog["counts"] == {
        "records": 3_100,
        "origin_theorems": 0,
        "origin_open_claims": 600,
        "cumulative_theorems": 1_500,
        "cumulative_open_claims": 1_600,
    }, "catalog counts drifted")
    theorem = artifacts["Theorem_List.json"]
    open_list = artifacts["Open_Claim_List.json"]
    require(theorem["counts"]["records"] == 1_500, "theorem projection is not 1,500")
    require(open_list["counts"]["records"] == 1_600, "open projection is not 1,600")
    require(theorem["records"] == parent["Theorem_List.json"]["records"], "theorem parent projection changed")
    require(open_list["records"][:1_000] == parent["Open_Claim_List.json"]["records"], "open parent projection changed")
    require(open_list["records"][1_000:] == list(new_rows), "open projection additions drifted")
    registry = artifacts["Claim_ID_Registry.json"]
    require(registry["namespace_high_watermarks"] == {
        "ATF": LAST_ATF_ORDINAL,
        "ATO": LAST_ATV_ORDINAL,
        "ATS": LAST_ATV_ORDINAL,
        "ATV": LAST_ATV_ORDINAL,
    }, "registry high-watermarks drifted")
    expected_atv = [f"ATV-{value:08d}" for value in range(5_985, 6_585)]
    expected_atf = [f"ATF-{value:08d}" for value in range(5_755, 6_355)]
    require([row["variant_id"] for row in new_rows] == expected_atv, "new ATV suffix drifted")
    require([row["family_id"] for row in new_rows] == expected_atf, "new ATF suffix drifted")
    require([row["occurrence_id"] for row in new_rows] == [value.replace("ATV-", "ATO-") for value in expected_atv], "new ATO suffix drifted")
    require([row["sense_id"] for row in new_rows] == [value.replace("ATV-", "ATS-") for value in expected_atv], "new ATS suffix drifted")
    require([row["stage_claim_id"] for row in new_rows] == [f"S5-CLM-{value:08d}" for value in range(5_985, 6_585)], "new S5 suffix drifted")
    require(len({row["semantic_key"] for row in new_rows}) == 600, "new semantic keys are not unique")
    require(len({row["source_locator"]["content_hash"] for row in new_rows}) == 600, "new content hashes are not unique")


def build_all() -> tuple[dict[str, bytes], str, dict[str, Any]]:
    contract, schema, sources, receipt, curation = verify_authorities()
    require(
        tuple(contract["release_layout"]["non_manifest_artifacts"])
        == RELEASE_FILES,
        "contract release artifact order/set differs from generator",
    )
    parent = verify_parent_release(contract)
    pool, locators, source_hashes = load_and_verify_sources(contract)
    accepted = verify_curation(contract, curation, pool, source_hashes)
    parent_registry = parent["Claim_ID_Registry.json"]
    parent_root = parent[MANIFEST_NAME]["release_root_sha256"]
    new_rows = [
        build_claim_row(
            ledger_row,
            source,
            locators,
            source_hashes,
            parent_registry["authority_sha256"],
            parent_root,
            curation["authority_sha256"],
            schema,
        )
        for ledger_row, source in accepted
    ]
    inputs = authoritative_inputs(
        contract, schema, sources, receipt, curation, parent
    )
    catalog = build_catalog(parent["Claim_Catalog.json"], new_rows, inputs)
    artifacts: dict[str, dict[str, Any]] = {
        "Claim_Catalog.json": catalog,
        "Claim_ID_Registry.json": build_registry(
            parent["Claim_ID_Registry.json"], new_rows, inputs
        ),
        "Stage5_Claim_ID_Registry.json": build_stage_registry(
            parent["Stage5_Claim_ID_Registry.json"], new_rows, inputs
        ),
        "Migration_v4_to_v5.json": build_migration(
            parent["Migration_v4_to_v5.json"], new_rows, inputs
        ),
        "Theorem_List.json": build_projection(
            "Theorem_List.json", catalog["records"], theorem_predicate, inputs
        ),
        "Open_Claim_List.json": build_projection(
            "Open_Claim_List.json", catalog["records"], open_predicate, inputs
        ),
        "Coverage_Ledger.json": build_coverage(
            parent["Coverage_Ledger.json"], curation, inputs
        ),
        STRICT_LEDGER_NAME: build_strict_ledger(
            parent["Claim_Catalog.json"]["records"],
            new_rows,
            receipt,
            curation,
            parent_root,
        ),
    }
    validate_generated(artifacts, parent, new_rows)
    package, root = package_release(artifacts, inputs, curation)
    return package, root, {
        "selected": len(new_rows),
        "catalog_records": len(catalog["records"]),
        "theorems": artifacts["Theorem_List.json"]["counts"]["records"],
        "open_claims": artifacts["Open_Claim_List.json"]["counts"]["records"],
        "strict_credits": artifacts[STRICT_LEDGER_NAME]["counts"][
            "effective_strict_credits"
        ],
    }


def compare_release(path: Path, expected: Mapping[str, bytes]) -> None:
    if not path.is_dir():
        raise GenerationError(f"release directory is missing: {path}")
    actual_names = {item.name for item in path.iterdir() if item.is_file()}
    non_files = [item.name for item in path.iterdir() if not item.is_file()]
    require(
        actual_names == set(expected) and not non_files,
        f"release artifact set differs at {path}: files={sorted(actual_names)}, non_files={sorted(non_files)}",
    )
    for name in sorted(expected):
        try:
            observed = (path / name).read_bytes()
        except OSError as error:
            raise GenerationError(f"cannot read release artifact {path / name}: {error}") from error
        require(observed == expected[name], f"immutable release byte drift: {path / name}")


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


@contextmanager
def exclusive_writer_lock(output_root: Path) -> Iterator[None]:
    output_root.mkdir(parents=True, exist_ok=True)
    lock_path = output_root / LOCK_NAME
    descriptor = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _release_version(value: str) -> tuple[int, ...]:
    try:
        return tuple(int(item) for item in value.split("."))
    except ValueError as error:
        raise GenerationError(f"invalid current release version: {value!r}") from error


def verify_current_cas(
    output_root: Path, expected_package: Mapping[str, bytes], expected_root: str
) -> str:
    current_path = output_root / CURRENT_NAME
    current, _ = load_json(current_path)
    verify_seal(current, str(current_path))
    current_release = current.get("release")
    require(isinstance(current_release, str), "Current_Release release is invalid")
    current_version = _release_version(current_release)
    target_version = _release_version(RELEASE)
    if current_version > target_version:
        raise GenerationError(
            f"refusing release downgrade: current={current_release}, target={RELEASE}"
        )
    if current_release == RELEASE:
        require(current.get("release_root_sha256") == expected_root, "current 5.2 root differs from generated root")
        require(current.get("manifest_sha256") == sha256_bytes(expected_package[MANIFEST_NAME]), "current 5.2 manifest hash differs")
        compare_release(output_root / "releases" / RELEASE, expected_package)
        return "already_current"
    require(current_release == PARENT_RELEASE, f"compare-and-swap parent is {current_release}, expected {PARENT_RELEASE}")
    expected_parent_root = json.loads(
        (PARENT_DIR / MANIFEST_NAME).read_text(encoding="utf-8")
    )["release_root_sha256"]
    require(current.get("release_root_sha256") == expected_parent_root, "compare-and-swap parent root drifted")
    expected_parent_manifest_sha = sha256_file(PARENT_DIR / MANIFEST_NAME)
    require(current.get("manifest_sha256") == expected_parent_manifest_sha, "compare-and-swap parent manifest drifted")
    output_parent_manifest = output_root / "releases" / PARENT_RELEASE / MANIFEST_NAME
    output_parent_registry = output_root / "releases" / PARENT_RELEASE / "Claim_ID_Registry.json"
    require(output_parent_manifest.is_file() and output_parent_registry.is_file(), "output root lacks the compare-and-swap parent release")
    require(sha256_file(output_parent_manifest) == expected_parent_manifest_sha, "output parent manifest differs from canonical parent")
    output_registry, _ = load_json(output_parent_registry)
    verify_seal(output_registry, str(output_parent_registry))
    require(
        output_registry["authority_sha256"]
        == json.loads((PARENT_DIR / "Claim_ID_Registry.json").read_text(encoding="utf-8"))["authority_sha256"],
        "compare-and-swap parent registry authority drifted",
    )
    return "parent_current"


def publish_release(output_root: Path, package: Mapping[str, bytes]) -> None:
    releases = output_root / "releases"
    target = releases / RELEASE
    releases.mkdir(parents=True, exist_ok=True)
    if target.exists():
        compare_release(target, package)
        return
    temporary = Path(tempfile.mkdtemp(prefix=f".{RELEASE}.tmp-", dir=releases))
    try:
        # The manifest is the commit marker and is written last in the private tree.
        for name in list(sorted(RELEASE_FILES)) + [MANIFEST_NAME]:
            path = temporary / name
            with path.open("xb") as stream:
                stream.write(package[name])
                stream.flush()
                os.fsync(stream.fileno())
        fsync_directory(temporary)
        try:
            os.rename(temporary, target)
        except OSError:
            if target.exists():
                compare_release(target, package)
                shutil.rmtree(temporary)
            else:
                raise
        fsync_directory(releases)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


def update_current(output_root: Path, package: Mapping[str, bytes], root: str) -> None:
    pointer = seal(
        {
            "schema_version": "awesome-theorems/stage5-current-release/5.2",
            "release": RELEASE,
            "release_root_sha256": root,
            "manifest_sha256": sha256_bytes(package[MANIFEST_NAME]),
            "manifest_path": f"releases/{RELEASE}/{MANIFEST_NAME}",
        }
    )
    payload = encoded_document(pointer)
    descriptor, raw_path = tempfile.mkstemp(
        prefix=".Current_Release.tmp-", dir=output_root
    )
    temporary = Path(raw_path)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, output_root / CURRENT_NAME)
        fsync_directory(output_root)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", choices=(RELEASE,), default=RELEASE)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=CATALOG_ROOT,
        help="Stage5 catalog root receiving releases/5.2 and Current_Release.json",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check", action="store_true", help="compare the existing immutable 5.2 release byte-for-byte"
    )
    mode.add_argument(
        "--dry-run", action="store_true", help="authenticate and build entirely in memory without writing"
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    output_root = args.output_root.resolve()
    try:
        if args.dry_run:
            package, root, counts = build_all()
            print(
                "PASS generate_math_catalog_v5_2 --dry-run "
                f"release={RELEASE} root={root} "
                f"counts={json.dumps(counts, sort_keys=True, separators=(',', ':'))}"
            )
            return 0
        if args.check:
            package, root, _counts = build_all()
            compare_release(output_root / "releases" / RELEASE, package)
            print(
                f"PASS generate_math_catalog_v5_2 --check release={RELEASE} root={root}"
            )
            return 0
        with exclusive_writer_lock(output_root):
            # Allocation and every authority read occur while the single-writer
            # lease is held, so the CAS cannot publish a package built against
            # a different parent transaction.
            package, root, _counts = build_all()
            cas_state = verify_current_cas(output_root, package, root)
            if cas_state != "already_current":
                publish_release(output_root, package)
                # Recheck the immutable directory before committing the pointer.
                compare_release(output_root / "releases" / RELEASE, package)
                update_current(output_root, package, root)
        print(f"PASS generate_math_catalog_v5_2 release={RELEASE} root={root}")
        return 0
    except (GenerationError, OSError, ValueError, TypeError, KeyError, IndexError) as error:
        print(f"FAIL generate_math_catalog_v5_2: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
