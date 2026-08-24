#!/usr/bin/env python3
"""Build the immutable, append-only Stage5 mathematics release 5.3.

Release 5.3 consumes a pinned mathlib theorem-source artifact and a sealed
curation authority.  A source record grants theorem credit only when both the
runtime declaration kind and the literal source syntax kind are ``theorem``;
source-level ``lemma`` declarations never count toward the 500-row quota.

The generator is standalone and standard-library-only.  It authenticates the
immutable 5.2 parent and every versioned 5.3 authority before allocation.  A
publish holds an exclusive advisory lock across authority reads, allocation,
immutable-directory publication, and the compare-and-swap update of
``Current_Release.json``.
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
import unicodedata


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_ROOT = REPO_ROOT / "Docs/catalog/v5"
RELEASE = "5.3"
PARENT_RELEASE = "5.2"
REVIEW_DATE = "2026-08-10"
SOURCE_ID = "SRC-MATH-V5-MATHLIB-8A178386"

CONTRACT_PATH = CATALOG_ROOT / "Stage5_Math_Expansion_Contract_v5_3.json"
SCHEMA_PATH = CATALOG_ROOT / "Math_Claim_Record_Schema_v5_3.json"
SOURCE_REGISTRY_PATH = CATALOG_ROOT / "Math_Source_Registry_v5_3.json"
PARENT_RECEIPT_PATH = CATALOG_ROOT / "V5_2_Parent_Receipt_v5_3.json"
CURATION_PATH = CATALOG_ROOT / "curation/Mathlib_Theorem_Curation_v5_3.json"
SOURCE_PATH = CATALOG_ROOT / "sources/mathlib-theorems-8a178386.json"
PARENT_DIR = CATALOG_ROOT / "releases" / PARENT_RELEASE

SOURCE_FILE_SHA256 = "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a"
SOURCE_FILE_SIZE = 6_316_287
SOURCE_CONTENT_DIGEST = "dd49c8322d8eded995c84a235fd458fc093a187230323f87bea78049ae90e53b"
MATHLIB_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"

RELEASE_FILES = (
    "Claim_Catalog.json",
    "Claim_ID_Registry.json",
    "Stage5_Claim_ID_Registry.json",
    "Migration_v4_to_v5.json",
    "Theorem_List.json",
    "Open_Claim_List.json",
    "Coverage_Ledger.json",
    "Strict_Conjecture_Ledger.json",
)
MANIFEST_NAME = "Release_Manifest.json"
CURRENT_NAME = "Current_Release.json"
LOCK_NAME = ".Current_Release.lock"

PARENT_ATV_HIGH_WATERMARK = 6_584
PARENT_ATF_HIGH_WATERMARK = 6_354
NEW_ROWS = 500
LAST_ATV_ORDINAL = 7_084
LAST_ATF_ORDINAL = 6_854

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")


class GenerationError(RuntimeError):
    """An authenticated input or generated invariant failed closed."""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def pretty_source_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
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
        canonical_json_bytes(
            {key: item for key, item in value.items() if key not in omitted}
        )
    )


def document_sha256(value: Mapping[str, Any]) -> str:
    return hash_without(value, "authority_sha256")


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result.pop("authority_sha256", None)
    result["authority_sha256"] = document_sha256(result)
    return result


def seal_field(
    value: Mapping[str, Any], field: str, *also_omit: str
) -> dict[str, Any]:
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
        raise GenerationError(f"JSON document must be an object: {path}")
    return value, raw


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GenerationError(message)


def verify_seal(value: Mapping[str, Any], label: str) -> str:
    observed = value.get("authority_sha256")
    require(
        isinstance(observed, str) and SHA256_RE.fullmatch(observed) is not None,
        f"missing or invalid authority_sha256 in {label}",
    )
    expected = document_sha256(value)
    require(observed == expected, f"stale authority_sha256 in {label}")
    return observed


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
        raise GenerationError(f"path is outside repository: {path}") from error


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
    """Validate the closed Draft 2020-12 subset used by the 5.3 schema."""
    reference = schema.get("$ref")
    if reference is not None:
        if not isinstance(reference, str) or not reference.startswith("#/"):
            raise GenerationError(
                f"unsupported schema reference at {location}: {reference}"
            )
        target: Any = root
        for component in reference[2:].split("/"):
            target = target[
                component.replace("~1", "/").replace("~0", "~")
            ]
        validate_schema_instance(value, target, root, location)
        return
    for subschema in schema.get("allOf", []):
        validate_schema_instance(value, subschema, root, location)
    one_of = schema.get("oneOf")
    if isinstance(one_of, list):
        matches = 0
        for subschema in one_of:
            try:
                validate_schema_instance(value, subschema, root, location)
            except GenerationError:
                continue
            matches += 1
        if matches != 1:
            raise GenerationError(f"schema oneOf mismatch at {location}")
    negated = schema.get("not")
    if isinstance(negated, dict):
        try:
            validate_schema_instance(value, negated, root, location)
        except GenerationError:
            pass
        else:
            raise GenerationError(f"schema not mismatch at {location}")
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
        accepted = (
            [expected_type] if isinstance(expected_type, str) else expected_type
        )
        if not any(_json_type_matches(value, item) for item in accepted):
            raise GenerationError(
                f"schema type mismatch at {location}: {accepted}"
            )
    if isinstance(value, dict):
        required = schema.get("required", [])
        missing = [item for item in required if item not in value]
        if missing:
            raise GenerationError(
                f"schema missing fields at {location}: {missing}"
            )
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            if extras:
                raise GenerationError(
                    f"schema extra fields at {location}: {extras}"
                )
        for key, item in value.items():
            child = properties.get(key)
            if isinstance(child, dict):
                validate_schema_instance(item, child, root, f"{location}.{key}")
    if isinstance(value, list):
        minimum = schema.get("minItems")
        maximum = schema.get("maxItems")
        if minimum is not None and len(value) < minimum:
            raise GenerationError(f"schema minItems mismatch at {location}")
        if maximum is not None and len(value) > maximum:
            raise GenerationError(f"schema maxItems mismatch at {location}")
        if schema.get("uniqueItems") and len(
            {canonical_json_bytes(item) for item in value}
        ) != len(value):
            raise GenerationError(f"schema uniqueItems mismatch at {location}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_schema_instance(
                    item, item_schema, root, f"{location}[{index}]"
                )
        contains = schema.get("contains")
        if isinstance(contains, dict):
            matches = 0
            for index, item in enumerate(value):
                try:
                    validate_schema_instance(
                        item, contains, root, f"{location}[{index}]"
                    )
                except GenerationError:
                    continue
                matches += 1
            minimum_contains = int(schema.get("minContains", 1))
            maximum_contains = schema.get("maxContains")
            if matches < minimum_contains or (
                maximum_contains is not None
                and matches > int(maximum_contains)
            ):
                raise GenerationError(f"schema contains mismatch at {location}")
    if isinstance(value, str):
        if len(value) < int(schema.get("minLength", 0)):
            raise GenerationError(f"schema minLength mismatch at {location}")
        pattern = schema.get("pattern")
        if pattern is not None and re.search(pattern, value) is None:
            raise GenerationError(
                f"schema pattern mismatch at {location}: {value!r}"
            )
        format_name = schema.get("format")
        if format_name == "date" and re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value
        ) is None:
            raise GenerationError(f"schema date mismatch at {location}")
        if format_name == "date-time" and re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
            r"(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})",
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
    corrections = document.get("credit_corrections")
    if isinstance(strict_credits, list) and isinstance(corrections, list):
        return len(strict_credits) + len(corrections)
    for key in ("records", "variants", "mappings", "migrations", "rows"):
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


def verify_parent_release(
    contract: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    parent_contract = contract["parent"]
    require(
        parent_contract["release"] == PARENT_RELEASE,
        "contract parent release drifted",
    )
    manifest_path = REPO_ROOT / parent_contract["manifest_path"]
    require(
        manifest_path == PARENT_DIR / MANIFEST_NAME,
        "parent manifest path drifted",
    )
    manifest, manifest_raw = load_json(manifest_path)
    verify_seal(manifest, str(manifest_path))
    require(
        sha256_bytes(manifest_raw) == parent_contract["manifest_file_sha256"],
        "parent manifest file SHA-256 drifted",
    )
    require(
        manifest["authority_sha256"]
        == parent_contract["manifest_authority_sha256"],
        "parent manifest authority drifted",
    )
    require(
        manifest["release_root_sha256"]
        == parent_contract["release_root_sha256"],
        "parent release root differs from contract",
    )
    inventory = manifest.get("artifacts")
    require(isinstance(inventory, list), "parent artifact inventory is invalid")
    require(
        {row.get("path") for row in inventory} == set(RELEASE_FILES),
        "parent artifact set drifted",
    )
    require(
        {item.name for item in PARENT_DIR.iterdir() if item.is_file()}
        == set(RELEASE_FILES) | {MANIFEST_NAME}
        and all(item.is_file() for item in PARENT_DIR.iterdir()),
        "parent release directory is not the exact immutable artifact set",
    )
    documents: dict[str, dict[str, Any]] = {}
    for entry in inventory:
        name = entry["path"]
        path = PARENT_DIR / name
        raw = path.read_bytes()
        require(len(raw) == entry["size_bytes"], f"parent size drift: {name}")
        require(
            sha256_bytes(raw) == entry["sha256"],
            f"parent artifact hash drift: {name}",
        )
        value, _ = load_json(path)
        verify_seal(value, str(path))
        require(
            primary_row_count(value) == entry["row_count"],
            f"parent row count drift: {name}",
        )
        documents[name] = value
    require(
        release_root(inventory) == manifest["release_root_sha256"],
        "parent release root does not recompute",
    )
    catalog = documents["Claim_Catalog.json"]
    registry = documents["Claim_ID_Registry.json"]
    require(len(catalog["records"]) == 3_100, "parent catalog is not 3,100 rows")
    require(
        catalog["counts"]["cumulative_theorems"] == 1_500
        and catalog["counts"]["cumulative_open_claims"] == 1_600,
        "parent theorem/open counts drifted",
    )
    require(
        registry["namespace_high_watermarks"]["ATV"]
        == PARENT_ATV_HIGH_WATERMARK
        and registry["namespace_high_watermarks"]["ATF"]
        == PARENT_ATF_HIGH_WATERMARK,
        "parent identity high-watermarks drifted",
    )
    documents[MANIFEST_NAME] = manifest
    return documents


def load_source_artifact() -> tuple[
    dict[str, Any], list[dict[str, Any]], dict[str, int], dict[str, str]
]:
    source, raw = load_json(SOURCE_PATH)
    require(len(raw) == SOURCE_FILE_SIZE, "mathlib source artifact size drifted")
    require(
        sha256_bytes(raw) == SOURCE_FILE_SHA256,
        "mathlib source artifact file SHA-256 drifted",
    )
    observed_content_digest = source.get("content_digest_before_self_field")
    source_without_digest = {
        key: value
        for key, value in source.items()
        if key != "content_digest_before_self_field"
    }
    require(
        observed_content_digest
        == sha256_bytes(pretty_source_json_bytes(source_without_digest))
        == SOURCE_CONTENT_DIGEST,
        "mathlib source artifact self-digest drifted",
    )
    require(
        source.get("schema_version")
        == "awesome-theorems/mathlib-theorem-source/1.0",
        "mathlib source artifact schema drifted",
    )
    require(
        source["source_snapshot"]["commit"] == MATHLIB_COMMIT
        and source["source_snapshot"]["license"] == "Apache-2.0"
        and source["source_snapshot"]["module_cache_complete"] is True,
        "mathlib source snapshot pin or license drifted",
    )
    records = source.get("records")
    require(
        isinstance(records, list) and len(records) == 1_500,
        "mathlib source artifact must contain 1,500 records",
    )
    expected_fields = {
        "source_record_id",
        "selection_rank",
        "selection_cohort",
        "declaration",
        "display_label",
        "exact_curated_summary",
        "declaration_kind",
        "source_syntax_kind",
        "formal_type",
        "formal_type_sha256",
        "declaration_docstring",
        "formal_docstring",
        "formal_docstring_origin",
        "formal_docstring_sha256",
        "formal_proof_state",
        "raw_category",
        "raw_status",
        "material_status",
        "msc2020",
        "proof_evidence",
        "source",
        "importance_signals",
        "rights",
    }
    indexes: dict[str, int] = {}
    hashes: dict[str, str] = {}
    declarations: set[str] = set()
    literal_theorems = 0
    literal_lemmas = 0
    for source_index, row in enumerate(records):
        selection_rank = source_index + 1
        require(
            isinstance(row, dict),
            f"source record {selection_rank} is not an object",
        )
        require(
            set(row) == expected_fields,
            f"source record {selection_rank} field set drifted",
        )
        source_record_id = row["source_record_id"]
        require(
            isinstance(source_record_id, str) and source_record_id not in indexes,
            f"source record {selection_rank} has duplicate/invalid ID",
        )
        require(
            row["selection_rank"] == selection_rank,
            f"source record {selection_rank} selection rank drifted",
        )
        require(
            isinstance(row["declaration"], str)
            and row["declaration"] not in declarations,
            f"source record {selection_rank} has duplicate/invalid declaration",
        )
        declarations.add(row["declaration"])
        require(
            row["formal_type_sha256"]
            == sha256_bytes(row["formal_type"].encode("utf-8"))
            and row["formal_docstring_sha256"]
            == sha256_bytes(row["formal_docstring"].encode("utf-8")),
            f"source record {selection_rank} statement/docstring hash drifted",
        )
        proof = row["proof_evidence"]
        require(
            row["formal_proof_state"] == "kernel_checked_sorry_free"
            and row["raw_status"] == "lean_checked_thmInfo_sorry_free"
            and row["material_status"]["status"] == "proved_formal"
            and proof["uses_sorry"] is False
            and proof["verification"]
            == "lean_checked_environment_thmInfo_and_collectAxioms_without_sorryAx",
            f"source record {selection_rank} fails kernel/sorry-free proof gate",
        )
        require(
            row["declaration_kind"] == row["source_syntax_kind"]
            == row["raw_category"],
            f"source record {selection_rank} declaration-kind fields disagree",
        )
        if row["declaration_kind"] == "theorem":
            literal_theorems += 1
        elif row["declaration_kind"] == "lemma":
            literal_lemmas += 1
        else:
            raise GenerationError(
                f"source record {selection_rank} has unsupported literal declaration kind"
            )
        require(
            row["source"]["module"] == proof["compiled_module"],
            f"source record {selection_rank} module/proof binding drifted",
        )
        require(
            row["rights"]
            == {
                "attribution": "The mathlib Community",
                "source_license": "Apache-2.0",
                "use": "formal_statement_docstring_and_bibliographic_metadata",
            },
            f"source record {selection_rank} rights drifted",
        )
        indexes[source_record_id] = source_index
        hashes[source_record_id] = sha256_bytes(canonical_json_bytes(row))
    require(
        literal_theorems == 1_235 and literal_lemmas == 265,
        "literal theorem/lemma partition drifted",
    )
    require(
        source["counts"]["selected_total"] == 1_500
        and source["counts"]["selected_baseline"] == 1_000
        and source["counts"]["selected_dynamic_expansion"] == 500,
        "mathlib source declared selection counts drifted",
    )
    return source, records, indexes, hashes


def verify_parent_receipt(
    receipt: Mapping[str, Any], parent: Mapping[str, Mapping[str, Any]]
) -> None:
    verify_seal(receipt, str(PARENT_RECEIPT_PATH))
    binding = receipt["parent_release"]
    manifest = parent[MANIFEST_NAME]
    require(
        binding["release"] == PARENT_RELEASE
        and binding["release_root_sha256"] == manifest["release_root_sha256"]
        and binding["manifest_file_sha256"]
        == sha256_file(PARENT_DIR / MANIFEST_NAME)
        and binding["manifest_authority_sha256"]
        == manifest["authority_sha256"],
        "5.2 parent receipt manifest binding drifted",
    )
    inventory = receipt["artifact_inventory"]
    require(
        isinstance(inventory, list)
        and {row["path"] for row in inventory} == set(RELEASE_FILES),
        "5.2 parent receipt artifact set drifted",
    )
    for row in inventory:
        name = row["path"]
        document = parent[name]
        path = PARENT_DIR / name
        require(
            row["file_sha256"] == sha256_file(path)
            and row["size_bytes"] == path.stat().st_size
            and row["row_count"] == primary_row_count(document)
            and row["authority_sha256"] == document["authority_sha256"],
            f"5.2 parent receipt artifact binding drifted: {name}",
        )
    identity = receipt["identity_boundary"]
    require(
        identity["variant_high_watermark"] == PARENT_ATV_HIGH_WATERMARK
        and identity["occurrence_high_watermark"]
        == PARENT_ATV_HIGH_WATERMARK
        and identity["sense_high_watermark"] == PARENT_ATV_HIGH_WATERMARK
        and identity["family_high_watermark"] == PARENT_ATF_HIGH_WATERMARK
        and identity["first_child_variant_ordinal"]
        == PARENT_ATV_HIGH_WATERMARK + 1,
        "5.2 parent receipt identity boundary drifted",
    )
    counts = receipt["claim_count_boundary"]
    require(
        counts["catalog_records"] == 3_100
        and counts["theorem_records"] == 1_500
        and counts["open_claim_records"] == 1_600
        and counts["effective_strict_conjecture_credits"] == 1_000,
        "5.2 parent receipt claim-count boundary drifted",
    )
    strict = parent["Strict_Conjecture_Ledger.json"]
    strict_boundary = receipt["strict_credit_boundary"]
    require(
        strict_boundary["ledger_file_sha256"]
        == sha256_file(PARENT_DIR / "Strict_Conjecture_Ledger.json")
        and strict_boundary["ledger_authority_sha256"]
        == strict["authority_sha256"]
        and strict_boundary["effective_s5_id_set_sha256"]
        == strict["set_digests"]["effective_s5_id_set_sha256"]
        and strict_boundary["effective_variant_id_set_sha256"]
        == strict["set_digests"]["effective_variant_id_set_sha256"]
        and strict_boundary["effective_credit_count"]
        == len(strict["strict_credits"])
        == 1_000
        and strict_boundary["credit_correction_count"]
        == len(strict["credit_corrections"])
        == 1,
        "5.2 parent receipt strict-credit boundary drifted",
    )


def has_importance_signal(row: Mapping[str, Any], kind: str) -> bool:
    return any(
        isinstance(signal, dict) and signal.get("kind") == kind
        for signal in row["importance_signals"]
    )


def expected_selection(
    records: Sequence[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, str],
]:
    """Rebuild the frozen two-phase literal-theorem selection.

    Returns selected rows in release-rank order, the canonical source winner
    keyed by every source-record ID, and the winner ID for every duplicate
    loser.  The replay applies all three closed identity gates: exact formal
    type, whitespace-normalized formal type, and normalized full declaration
    name.
    """
    literal = [
        row
        for row in records
        if row["declaration_kind"] == "theorem"
        and row["source_syntax_kind"] == "theorem"
    ]
    require(len(literal) == 1_235, "literal theorem pool drifted")
    by_formal_type: dict[str, list[dict[str, Any]]] = {}
    for row in literal:
        by_formal_type.setdefault(row["formal_type_sha256"], []).append(row)
    require(
        len(by_formal_type) == 1_231
        and sum(len(group) > 1 for group in by_formal_type.values()) == 3
        and sum(len(group) - 1 for group in by_formal_type.values()) == 4,
        "exact formal-type duplicate facts drifted",
    )
    winners: dict[str, dict[str, Any]] = {}
    duplicate_losers: dict[str, str] = {}
    winner_rows: list[dict[str, Any]] = []
    seen_normalized_types: dict[str, dict[str, Any]] = {}
    seen_names: dict[str, dict[str, Any]] = {}
    duplicate_order = sorted(
        literal,
        key=lambda row: (
            -int(has_importance_signal(row, "mathlib_1000_theorems")),
            int(row["selection_rank"]),
            str(row["source_record_id"]),
        ),
    )
    for row in duplicate_order:
        source_record_id = str(row["source_record_id"])
        normalized_type = normalized_formal_type_sha256(str(row["formal_type"]))
        normalized_name = normalize_declaration_name(str(row["declaration"]))
        winner = seen_normalized_types.get(normalized_type)
        if winner is None:
            winner = seen_names.get(normalized_name)
        if winner is not None:
            winners[source_record_id] = winner
            duplicate_losers[source_record_id] = str(winner["source_record_id"])
            continue
        winners[source_record_id] = row
        seen_normalized_types[normalized_type] = row
        seen_names[normalized_name] = row
        winner_rows.append(row)
    require(
        len(winner_rows) == 1_231 and len(duplicate_losers) == 4,
        "three-gate source dedupe facts drifted",
    )
    for loser_id, winner_id in duplicate_losers.items():
        loser = next(
            row for row in literal if row["source_record_id"] == loser_id
        )
        winner = winners[loser_id]
        require(
            loser["formal_type_sha256"] == winner["formal_type_sha256"]
            or normalized_formal_type_sha256(str(loser["formal_type"]))
            == normalized_formal_type_sha256(str(winner["formal_type"]))
            or normalize_declaration_name(str(loser["declaration"]))
            == normalize_declaration_name(str(winner["declaration"])),
            f"source duplicate {loser_id} lacks an identity-gate match to {winner_id}",
        )
    phase_one = sorted(
        (
            row
            for row in winner_rows
            if has_importance_signal(row, "mathlib_1000_theorems")
        ),
        key=lambda row: (
            int(row["selection_rank"]),
            str(row["source_record_id"]),
        ),
    )
    require(len(phase_one) == 180, "mathlib 1000-theorems phase count drifted")
    phase_one_ids = {row["source_record_id"] for row in phase_one}
    buckets: dict[str, list[dict[str, Any]]] = {}
    for row in winner_rows:
        if row["source_record_id"] in phase_one_ids:
            continue
        if not has_importance_signal(row, "mathlib_module_main_result"):
            continue
        pieces = str(row["source"]["module"]).split(".")
        require(
            len(pieces) >= 2 and pieces[0] == "Mathlib" and pieces[1],
            f"invalid Mathlib module for {row['source_record_id']}",
        )
        buckets.setdefault(pieces[1], []).append(row)
    for bucket in buckets.values():
        bucket.sort(
            key=lambda row: (
                int(row["selection_rank"]),
                str(row["source_record_id"]),
            )
        )
    roots = sorted(buckets)
    require(len(roots) == 21, "phase-two module-root bucket count drifted")
    offsets = {root: 0 for root in roots}
    phase_two: list[dict[str, Any]] = []
    while len(phase_two) < 320:
        advanced = False
        for root in roots:
            offset = offsets[root]
            bucket = buckets[root]
            if offset >= len(bucket):
                continue
            phase_two.append(bucket[offset])
            offsets[root] += 1
            advanced = True
            if len(phase_two) == 320:
                break
        require(advanced, "phase-two balanced pool exhausted before 320 rows")
    selected = phase_one + phase_two
    require(
        len(selected) == NEW_ROWS
        and len({row["source_record_id"] for row in selected}) == NEW_ROWS
        and len({row["declaration"] for row in selected}) == NEW_ROWS
        and len({row["formal_type_sha256"] for row in selected}) == NEW_ROWS,
        "expected mathlib selected set is not 500-way unique",
    )
    return selected, winners, duplicate_losers


def theorem_predicate(row: Mapping[str, Any]) -> bool:
    base = bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "theorem"
        and row.get("current_claim_kind") == "theorem"
        and row.get("material_status") == "proved"
    )
    if not base:
        return False
    if row.get("origin_release") == RELEASE:
        formal = row.get("formal_statement", {})
        proof = row.get("proof_evidence", {})
        return bool(
            formal.get("declaration_kind") == "theorem"
            and formal.get("source_syntax_kind") == "theorem"
            and proof.get("formal_proof_state") == "kernel_checked_sorry_free"
            and proof.get("uses_sorry") is False
        )
    return row.get("declaration_kind") == "theorem"


def open_predicate(row: Mapping[str, Any]) -> bool:
    base = bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("current_claim_kind")
        in {"conjecture", "hypothesis", "open_problem"}
        and row.get("material_status")
        in {"open", "partial", "independent", "disputed"}
    )
    if not base:
        return False
    if row.get("origin_release") == "5.2":
        return row.get("source_block", {}).get("language") == "LaTeX"
    return row.get("declaration_kind") == "theorem"


def new_registry_rows(
    rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in rows:
        request = row["allocation"]["allocation_request_sha256"]
        display_titles = list(
            dict.fromkeys([row["display_name"]] + list(row["aliases"]))
        )
        families.append(
            {
                "family_id": row["family_id"],
                "curation_key": row["curation_key"],
                "display_titles": display_titles,
                "member_occurrence_ids": [row["occurrence_id"]],
                "historical_member_occurrence_ids": [row["occurrence_id"]],
                "idempotency_request_sha256": request,
                "identity_state": "stage5_mathlib_exact_formal_type_family",
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
                "identity_state": "stage5_mathlib_exact_formal_type_sense",
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
                "identity_state": "stage5_mathlib_exact_formal_type_variant",
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
    require(
        len(families) == len(senses) == len(variants) == NEW_ROWS,
        "new registry-row cardinality drifted",
    )
    allocation_policy = copy.deepcopy(parent["allocation_policy"])
    allocation_policy.update(
        {
            "release_5_3_first_new_atv_ordinal": PARENT_ATV_HIGH_WATERMARK
            + 1,
            "release_5_3_new_family_first_atf_ordinal": PARENT_ATF_HIGH_WATERMARK
            + 1,
        }
    )
    document = {
        "schema_version": "awesome-theorems/claim-id-registry/5.3",
        "artifact": "Claim_ID_Registry.json",
        "release": RELEASE,
        "parent_registry_authority_sha256": parent["authority_sha256"],
        "baseline_registry_authority_sha256": parent[
            "baseline_registry_authority_sha256"
        ],
        "authoritative_inputs": copy.deepcopy(inputs),
        "allocation_policy": allocation_policy,
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
            "stage5_additions": parent["counts"]["stage5_additions"]
            + NEW_ROWS,
            "legacy_aliases": len(parent.get("legacy_aliases", [])),
            "redirects": len(parent.get("redirects", [])),
            "splits": len(parent.get("splits", [])),
        },
    }
    result = seal(document)
    require(
        result["families"][: len(parent["families"])] == parent["families"]
        and result["senses"][: len(parent["senses"])] == parent["senses"]
        and result["variants"][: len(parent["variants"])]
        == parent["variants"],
        "claim-registry parent prefix changed",
    )
    return result


def build_stage_registry(
    parent: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    additions = [
        {
            "ordinal": ordinal(row["variant_id"], ATV_RE, "variant ID"),
            "variant_id": row["variant_id"],
            "predecessor_stage_claim_id": None,
            "stage_claim_id": row["stage_claim_id"],
            "lifecycle": "current",
        }
        for row in rows
    ]
    require(
        [row["ordinal"] for row in additions]
        == list(range(PARENT_ATV_HIGH_WATERMARK + 1, LAST_ATV_ORDINAL + 1)),
        "new Stage5 mappings are not contiguous",
    )
    mappings = copy.deepcopy(parent["mappings"]) + additions
    result = seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-id-registry/5.3",
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
        "Stage5 mapping parent prefix changed",
    )
    return result


def build_migration(
    parent: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    additions: list[dict[str, Any]] = []
    for row in rows:
        item_ordinal = ordinal(row["variant_id"], ATV_RE, "variant ID")
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
            "schema_version": "awesome-theorems/migration-v4-to-v5/5.3",
            "artifact": "Migration_v4_to_v5.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "v4_import_receipt": copy.deepcopy(parent["v4_import_receipt"]),
            "counts": {
                "historical_bindings": parent["counts"][
                    "historical_bindings"
                ],
                "new_allocations": parent["counts"]["new_allocations"]
                + NEW_ROWS,
                "migrations": len(migrations),
            },
            "migrations": migrations,
        }
    )
    require(
        result["migrations"][: len(parent["migrations"])]
        == parent["migrations"],
        "migration parent prefix changed",
    )
    return result


def build_catalog(
    parent: Mapping[str, Any],
    rows: Sequence[dict[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    records = copy.deepcopy(parent["records"]) + list(rows)
    require(
        records[: len(parent["records"])] == parent["records"],
        "catalog parent records changed",
    )
    require(len(records) == 3_600, "cumulative catalog is not 3,600 rows")
    require(
        len({row["variant_id"] for row in records}) == len(records)
        and len({row["stage_claim_id"] for row in records}) == len(records),
        "catalog identity IDs are not unique",
    )
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-catalog/5.3",
            "artifact": "Claim_Catalog.json",
            "release": RELEASE,
            "catalog_scope": parent["catalog_scope"],
            "authoritative_inputs": copy.deepcopy(inputs),
            "counts": {
                "records": len(records),
                "origin_theorems": sum(theorem_predicate(row) for row in rows),
                "origin_open_claims": sum(open_predicate(row) for row in rows),
                "cumulative_theorems": sum(
                    theorem_predicate(row) for row in records
                ),
                "cumulative_open_claims": sum(
                    open_predicate(row) for row in records
                ),
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
            "schema_version": "awesome-theorems/stage5-query-projection/5.3",
            "artifact": name,
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
            "stage_claim_ids": [row["stage_claim_id"] for row in records],
            "counts": {"records": len(records)},
            "records": records,
        }
    )


def normalize_declaration_name(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().strip()


def normalized_formal_type(value: str) -> str:
    return " ".join(value.split())


def normalized_formal_type_sha256(value: str) -> str:
    return sha256_bytes(normalized_formal_type(value).encode("utf-8"))


def module_root(row: Mapping[str, Any]) -> str:
    pieces = str(row["source"]["module"]).split(".")
    require(
        len(pieces) >= 2 and pieces[0] == "Mathlib" and bool(pieces[1]),
        f"invalid Mathlib module: {row['source']['module']!r}",
    )
    return pieces[1]


def importance_signal_kinds(row: Mapping[str, Any]) -> set[str]:
    signals = row.get("importance_signals")
    require(
        isinstance(signals, list) and bool(signals),
        f"source row {row.get('source_record_id')} lacks importance signals",
    )
    kinds = {
        str(signal.get("kind"))
        for signal in signals
        if isinstance(signal, dict)
    }
    require(
        kinds
        and kinds <= {"mathlib_1000_theorems", "mathlib_module_main_result"},
        f"source row {row.get('source_record_id')} has invalid importance signals",
    )
    return kinds


def importance_tier(row: Mapping[str, Any]) -> str:
    kinds = importance_signal_kinds(row)
    if kinds == {"mathlib_1000_theorems", "mathlib_module_main_result"}:
        return "docs_1000_and_module_main"
    if kinds == {"mathlib_1000_theorems"}:
        return "docs_1000"
    require(
        kinds == {"mathlib_module_main_result"},
        "source row has no recognized importance tier",
    )
    return "module_main_result"


def verify_authorities() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    contract, _contract_raw = load_json(CONTRACT_PATH)
    verify_seal(contract, str(CONTRACT_PATH))
    require(contract.get("release") == RELEASE, "wrong 5.3 contract release")
    require(
        contract.get("review_date") == REVIEW_DATE,
        "5.3 contract review date drifted",
    )
    bindings = contract.get("versioned_authorities")
    require(isinstance(bindings, dict), "5.3 authority bindings are malformed")
    values: dict[str, dict[str, Any]] = {}
    for key, path in (
        ("record_schema", SCHEMA_PATH),
        ("source_registry", SOURCE_REGISTRY_PATH),
        ("parent_receipt", PARENT_RECEIPT_PATH),
    ):
        specification = bindings.get(key)
        require(isinstance(specification, dict), f"missing authority binding {key}")
        require(
            specification.get("path") == relative_path(path),
            f"{key} authority path drifted",
        )
        value, raw = load_json(path)
        verify_seal(value, str(path))
        require(
            specification.get("size_bytes") == len(raw),
            f"{key} authority size drifted",
        )
        require(
            specification.get("file_sha256") == sha256_bytes(raw),
            f"{key} authority file hash drifted",
        )
        require(
            specification.get("authority_sha256")
            == value["authority_sha256"],
            f"{key} authority seal differs from contract",
        )
        values[key] = value

    schema = values["record_schema"]
    source_registry = values["source_registry"]
    receipt = values["parent_receipt"]
    require(
        schema.get("$id")
        == "urn:awesome-theorems:schema:stage5-math-claim-record:5.3",
        "5.3 record-schema ID drifted",
    )
    require(
        source_registry.get("schema_version")
        == "awesome-theorems/stage5-math-source-registry/5.3",
        "5.3 source-registry schema drifted",
    )
    source_matches = [
        row
        for row in source_registry.get("sources", [])
        if isinstance(row, dict) and row.get("source_id") == SOURCE_ID
    ]
    require(
        len(source_matches) == 1,
        "5.3 source registry lacks exactly one pinned mathlib source",
    )
    registered_asset = source_matches[0].get("asset", {})
    require(
        registered_asset.get("path") == relative_path(SOURCE_PATH)
        and registered_asset.get("sha256") == SOURCE_FILE_SHA256
        and registered_asset.get("size_bytes") == SOURCE_FILE_SIZE
        and registered_asset.get("record_count") == 1_500
        and registered_asset.get("content_digest_before_self_field")
        == SOURCE_CONTENT_DIGEST,
        "source-registry mathlib asset binding drifted",
    )

    curation, curation_raw = load_json(CURATION_PATH)
    verify_seal(curation, str(CURATION_PATH))
    curation_binding = bindings.get("mathlib_curation_ledger")
    require(
        isinstance(curation_binding, dict)
        and curation_binding.get("path") == relative_path(CURATION_PATH),
        "curation authority path drifted",
    )
    if curation_binding.get("file_sha256") is not None:
        require(
            curation_binding["file_sha256"] == sha256_bytes(curation_raw),
            "contract curation file hash drifted",
        )
    if curation_binding.get("authority_sha256") is not None:
        require(
            curation_binding["authority_sha256"]
            == curation["authority_sha256"],
            "contract curation authority drifted",
        )
    ledger_contract = contract.get("curation_ledger_contract")
    require(isinstance(ledger_contract, dict), "curation contract is malformed")
    require(
        ledger_contract.get("path") == relative_path(CURATION_PATH)
        and ledger_contract.get("schema_version")
        == "awesome-theorems/mathlib-theorem-curation/5.3",
        "curation contract identity drifted",
    )
    require(
        set(ledger_contract.get("top_level_required_fields", []))
        == set(curation),
        "curation top-level field closure drifted",
    )
    return contract, schema, source_registry, receipt, curation


def parent_identity_indexes(
    parent_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    exact_types: dict[str, str] = {}
    normalized_types: dict[str, str] = {}
    names: dict[str, str] = {}
    for row in sorted(parent_rows, key=lambda item: str(item["variant_id"])):
        variant_id = str(row["variant_id"])
        formal_type = row.get("formal_type")
        if not isinstance(formal_type, str):
            formal_statement = row.get("formal_statement")
            if isinstance(formal_statement, dict):
                candidate = formal_statement.get("formal_type")
                if not isinstance(candidate, str):
                    candidate = formal_statement.get("declaration_type")
                formal_type = candidate if isinstance(candidate, str) else None
        formal_digest = row.get("formal_type_sha256")
        if not isinstance(formal_digest, str):
            formal_statement = row.get("formal_statement")
            if isinstance(formal_statement, dict):
                candidate = formal_statement.get("formal_type_sha256")
                if not isinstance(candidate, str):
                    candidate = formal_statement.get("declaration_type_sha256")
                formal_digest = candidate if isinstance(candidate, str) else None
        if isinstance(formal_digest, str):
            exact_types[formal_digest] = min(
                exact_types.get(formal_digest, variant_id), variant_id
            )
        if isinstance(formal_type, str):
            normalized_key = normalized_formal_type_sha256(formal_type)
            normalized_types[normalized_key] = min(
                normalized_types.get(normalized_key, variant_id), variant_id
            )
        declaration = row.get("qualified_name")
        if not isinstance(declaration, str):
            formal_statement = row.get("formal_statement")
            if isinstance(formal_statement, dict):
                candidate = formal_statement.get("declaration")
                if not isinstance(candidate, str):
                    candidate = formal_statement.get("qualified_declaration")
                declaration = candidate if isinstance(candidate, str) else None
        if isinstance(declaration, str):
            name_key = normalize_declaration_name(declaration)
            names[name_key] = min(names.get(name_key, variant_id), variant_id)
    return exact_types, normalized_types, names


def verify_curation(
    contract: Mapping[str, Any],
    curation: Mapping[str, Any],
    records: Sequence[dict[str, Any]],
    source_hashes: Mapping[str, str],
    parent_rows: Sequence[Mapping[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    ledger_contract = contract["curation_ledger_contract"]
    require(
        curation.get("schema_version")
        == "awesome-theorems/mathlib-theorem-curation/5.3"
        and curation.get("source_id") == SOURCE_ID
        and curation.get("source_asset_sha256") == SOURCE_FILE_SHA256,
        "curation identity or source binding drifted",
    )
    require(
        curation.get("source_registry_authority_sha256")
        == contract["versioned_authorities"]["source_registry"][
            "authority_sha256"
        ]
        and curation.get("parent_receipt_authority_sha256")
        == contract["versioned_authorities"]["parent_receipt"][
            "authority_sha256"
        ],
        "curation authority-chain binding drifted",
    )
    rows = curation.get("candidate_dispositions")
    require(
        isinstance(rows, list) and len(rows) == 1_500,
        "curation must conserve exactly 1,500 source rows",
    )
    required_fields = set(ledger_contract["candidate_disposition_required_fields"])
    allowed_dispositions = set(ledger_contract["disposition_enum"])
    allowed_reasons = set(ledger_contract["reason_code_enum"])

    selected, winner_for_id, duplicate_losers = expected_selection(records)
    selected_rank = {
        str(row["source_record_id"]): rank
        for rank, row in enumerate(selected, start=1)
    }
    exact_parent, normalized_parent, named_parent = parent_identity_indexes(
        parent_rows
    )
    parent_links: dict[str, str] = {}
    for source in records:
        if source["declaration_kind"] != "theorem":
            continue
        candidates = {
            value
            for value in (
                exact_parent.get(str(source["formal_type_sha256"])),
                normalized_parent.get(
                    normalized_formal_type_sha256(str(source["formal_type"]))
                ),
                named_parent.get(
                    normalize_declaration_name(str(source["declaration"]))
                ),
            )
            if value is not None
        }
        if candidates:
            parent_links[str(source["source_record_id"])] = min(candidates)
    require(not parent_links, "mathlib theorem pool intersects the 5.2 parent")

    expected_rows: list[dict[str, Any]] = []
    accepted: list[tuple[dict[str, Any], dict[str, Any]]] = []
    source_by_id = {str(row["source_record_id"]): row for row in records}
    for source_index, source in enumerate(records):
        source_record_id = str(source["source_record_id"])
        canonical_id = duplicate_losers.get(source_record_id)
        canonical_source = (
            source_by_id[canonical_id] if canonical_id is not None else None
        )
        if source["declaration_kind"] == "lemma":
            disposition = "rejected_nonliteral_lemma"
            reason = "literal_declaration_kind_is_lemma"
        elif canonical_id is not None:
            require(canonical_source is not None, "missing canonical source row")
            if normalize_declaration_name(str(source["declaration"])) == (
                normalize_declaration_name(str(canonical_source["declaration"]))
            ):
                disposition = "rejected_source_name_duplicate"
                reason = "normalized_declaration_name_duplicate"
            else:
                disposition = "rejected_source_semantic_duplicate"
                reason = "normalized_formal_type_duplicate"
        elif source_record_id in selected_rank:
            disposition = "accepted_new_kernel_checked_theorem"
            reason = (
                "selected_docs_1000_priority_seed"
                if selected_rank[source_record_id] <= 180
                else "selected_module_main_round_robin_fill"
            )
        else:
            disposition = "eligible_not_selected"
            reason = "viable_theorem_outside_exact_500_selection"
        grants = disposition == "accepted_new_kernel_checked_theorem"
        rank = selected_rank.get(source_record_id) if grants else None
        item_ordinal = PARENT_ATV_HIGH_WATERMARK + rank if rank else None
        semantic_key = (
            "mathlib-theorem-semantic/" + str(source["formal_type_sha256"])
        )
        if canonical_source is not None:
            if source["formal_type_sha256"] == canonical_source["formal_type_sha256"]:
                duplicate_rationale = (
                    "Exact equality of the pinned pretty-printed formal_type SHA-256; "
                    "the higher-ranked source row is the sole canonical candidate."
                )
            elif normalized_formal_type_sha256(str(source["formal_type"])) == (
                normalized_formal_type_sha256(str(canonical_source["formal_type"]))
            ):
                duplicate_rationale = (
                    "Equality after whitespace normalization of the pinned formal_type; "
                    "the higher-ranked source row is the sole canonical candidate."
                )
            else:
                duplicate_rationale = (
                    "Equality of the normalized full declaration name; the higher-ranked "
                    "source row is the sole canonical candidate."
                )
            canonical_semantic_key = (
                "mathlib-theorem-semantic/"
                + str(canonical_source["formal_type_sha256"])
            )
        else:
            duplicate_rationale = None
            canonical_semantic_key = None
        expected: dict[str, Any] = {
            "candidate_key": f"mathlib:{source_record_id}",
            "source_index": source_index,
            "source_record_id": source_record_id,
            "source_record_sha256": source_hashes[source_record_id],
            "declaration": source["declaration"],
            "declaration_kind": source["declaration_kind"],
            "source_syntax_kind": source["source_syntax_kind"],
            "selection_rank": source["selection_rank"],
            "selection_cohort": source["selection_cohort"],
            "formal_proof_state": source["formal_proof_state"],
            "formal_type_sha256": source["formal_type_sha256"],
            "formal_docstring_sha256": source["formal_docstring_sha256"],
            "proof_evidence_payload_sha256": sha256_bytes(
                canonical_json_bytes(source["proof_evidence"])
            ),
            "importance_payload_sha256": sha256_bytes(
                canonical_json_bytes(source["importance_signals"])
            ),
            "rights_payload_sha256": sha256_bytes(
                canonical_json_bytes(source["rights"])
            ),
            "semantic_key": semantic_key,
            "semantic_key_method": "exact_formal_type_sha256_v1",
            "semantic_key_payload_sha256": sha256_bytes(
                canonical_json_bytes(
                    {
                        "method": "exact_formal_type_sha256_v1",
                        "formal_type_sha256": source["formal_type_sha256"],
                    }
                )
            ),
            "disposition": disposition,
            "reason_code": reason,
            "accepted_rank": rank,
            "target_variant_id": (
                f"ATV-{item_ordinal:08d}" if item_ordinal is not None else None
            ),
            "target_s5_id": (
                f"S5-CLM-{item_ordinal:08d}"
                if item_ordinal is not None
                else None
            ),
            "canonical_source_record_id": canonical_id,
            "duplicate_of_semantic_key": canonical_semantic_key,
            "duplicate_of_variant_id": None,
            "dedupe_rationale": duplicate_rationale,
            "dedupe_confidence": "exact" if canonical_id is not None else None,
            "dedupe_reviewer": (
                "deterministic_exact_identity_v1"
                if canonical_id is not None
                else None
            ),
            "grants_catalog_entry": grants,
            "grants_theorem_credit": grants,
        }
        expected["row_sha256"] = hash_without(expected, "row_sha256")
        require(set(expected) == required_fields, "curation row contract drifted")
        observed = rows[source_index]
        require(
            isinstance(observed, dict) and set(observed) == required_fields,
            f"curation row {source_index} field closure drifted",
        )
        require(
            observed.get("disposition") in allowed_dispositions
            and observed.get("reason_code") in allowed_reasons,
            f"curation row {source_index} has invalid terminal disposition",
        )
        require(
            observed == expected,
            f"curation row {source_index} differs from deterministic replay",
        )
        expected_rows.append(expected)
        if grants:
            accepted.append((observed, source))

    accepted.sort(key=lambda pair: int(pair[0]["accepted_rank"]))
    require(
        [source for _ledger, source in accepted] == selected,
        "curation accepted order differs from deterministic selection",
    )
    disposition_counts = Counter(row["disposition"] for row in expected_rows)
    accepted_sources = [source for _ledger, source in accepted]
    selected_by_root = Counter(module_root(row) for row in accepted_sources)
    selected_by_tier = Counter(importance_tier(row) for row in accepted_sources)
    expected_counts = {
        "source_rows": 1_500,
        "candidate_disposition_rows": 1_500,
        "eligible_literal_theorems": 1_235,
        "pre_eligibility_excluded_lemmas": 265,
        "literal_theorems": 1_235,
        "literal_lemmas": 265,
        "kernel_checked_sorry_free": 1_500,
        "accepted": 500,
        "nonaccepted_eligible": 735,
        "nonaccepted_total": 1_000,
        "docs_1000_priority_seed": 180,
        "module_main_balanced_fill": 320,
        "source_semantic_duplicate_rows": 4,
        "parent_duplicate_rows": 0,
        "selected_branches": len(selected_by_root),
        "selected_with_docs_1000_signal": sum(
            has_importance_signal(row, "mathlib_1000_theorems")
            for row in accepted_sources
        ),
        "selected_with_module_main_signal": sum(
            has_importance_signal(row, "mathlib_module_main_result")
            for row in accepted_sources
        ),
        "by_disposition": dict(sorted(disposition_counts.items())),
        "selected_by_module_root": dict(sorted(selected_by_root.items())),
        "selected_by_importance_tier": dict(sorted(selected_by_tier.items())),
    }
    require(curation.get("counts") == expected_counts, "curation counts drifted")
    accepted_rows = [row for row, _source in accepted]
    expected_digests = {
        "candidate_row_sha256_set_sha256": set_digest(
            str(row["row_sha256"]) for row in expected_rows
        ),
        "candidate_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"]) for row in expected_rows
        ),
        "eligible_theorem_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"])
            for row in expected_rows
            if row["declaration_kind"] == "theorem"
        ),
        "excluded_lemma_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"])
            for row in expected_rows
            if row["disposition"] == "rejected_nonliteral_lemma"
        ),
        "nonaccepted_eligible_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"])
            for row in expected_rows
            if row["declaration_kind"] == "theorem"
            and row["disposition"] != "accepted_new_kernel_checked_theorem"
        ),
        "selected_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"]) for row in accepted_rows
        ),
        "selected_declaration_set_sha256": set_digest(
            str(row["declaration"]) for row in accepted_rows
        ),
        "selected_formal_type_sha256_set_sha256": set_digest(
            str(row["formal_type_sha256"]) for row in accepted_rows
        ),
        "selected_semantic_key_set_sha256": set_digest(
            str(row["semantic_key"]) for row in accepted_rows
        ),
        "selected_variant_id_set_sha256": set_digest(
            str(row["target_variant_id"]) for row in accepted_rows
        ),
        "selected_s5_id_set_sha256": set_digest(
            str(row["target_s5_id"]) for row in accepted_rows
        ),
    }
    require(
        curation.get("set_digests") == expected_digests,
        "curation set digests drifted",
    )
    return accepted


def build_claim_row(
    ledger_row: Mapping[str, Any],
    source: Mapping[str, Any],
    parent_registry_authority: str,
    parent_release_root: str,
    curation_authority: str,
    schema: Mapping[str, Any],
) -> dict[str, Any]:
    rank = int(ledger_row["accepted_rank"])
    atv_ordinal = PARENT_ATV_HIGH_WATERMARK + rank
    atf_ordinal = PARENT_ATF_HIGH_WATERMARK + rank
    source_record_id = str(source["source_record_id"])
    source_record_hash = sha256_bytes(canonical_json_bytes(source))
    semantic_key = str(ledger_row["semantic_key"])
    statement_type = str(source["formal_type"])
    statement_type_hash = str(source["formal_type_sha256"])
    source_data = source["source"]
    root = module_root(source)

    source_locator = {
        "source_id": SOURCE_ID,
        "artifact_path": relative_path(SOURCE_PATH),
        "artifact_sha256": SOURCE_FILE_SHA256,
        "artifact_size_bytes": SOURCE_FILE_SIZE,
        "record_index": ledger_row["source_index"],
        "source_record_id": source_record_id,
        "source_record_sha256": source_record_hash,
        "mathlib_commit": MATHLIB_COMMIT,
        "module": source_data["module"],
        "source_path": source_data["path"],
        "source_sha256": source_data["source_sha256"],
        "url": source_data["url"],
        "source_range": copy.deepcopy(source_data["range"]),
        "selection_range": copy.deepcopy(source_data["selection_range"]),
    }
    formal_statement = {
        "language": "Lean4",
        "completeness": "exact_runtime_formal_type_and_source_locator",
        "declaration": source["declaration"],
        "declaration_kind": source["declaration_kind"],
        "source_syntax_kind": source["source_syntax_kind"],
        "module": source_data["module"],
        "formal_type": statement_type,
        "formal_type_sha256": statement_type_hash,
        "formal_docstring": source["formal_docstring"],
        "formal_docstring_origin": source["formal_docstring_origin"],
        "formal_docstring_sha256": source["formal_docstring_sha256"],
    }
    mathematical_statement = seal_field(
        {
            "completeness": "exact_formal",
            "language": "Lean4",
            "natural_language": source["exact_curated_summary"],
            "formal_type": statement_type,
            "formal_type_sha256": statement_type_hash,
        },
        "statement_sha256",
    )
    selection_phase = str(ledger_row["reason_code"])
    theorem_selection = {
        "source_record_id": source_record_id,
        "selection_cohort": source["selection_cohort"],
        "selection_rank": source["selection_rank"],
        "display_label": source["display_label"],
        "exact_curated_summary": source["exact_curated_summary"],
        "importance_signals": copy.deepcopy(source["importance_signals"]),
        "selection_phase": selection_phase,
        "phase_rank": rank if rank <= 180 else rank - 180,
        "module_root": root,
    }
    curator_disposition = {
        "curation_ledger_path": relative_path(CURATION_PATH),
        "curation_ledger_file_sha256": sha256_file(CURATION_PATH),
        "curation_ledger_authority_sha256": curation_authority,
        "source_index": ledger_row["source_index"],
        "source_record_id": source_record_id,
        "curation_row_sha256": ledger_row["row_sha256"],
        "disposition": ledger_row["disposition"],
        "reason_code": ledger_row["reason_code"],
        "accepted_rank": rank,
        "target_variant_id": ledger_row["target_variant_id"],
        "target_s5_id": ledger_row["target_s5_id"],
        "grants_catalog_entry": ledger_row["grants_catalog_entry"],
        "grants_theorem_credit": ledger_row["grants_theorem_credit"],
        "semantic_key": semantic_key,
    }
    status_detail = {
        "source_material_status": source["material_status"]["status"],
        "status_as_of_commit": source["material_status"]["as_of_commit"],
        "basis": source["material_status"]["basis"],
        "source_refs": [SOURCE_ID],
        "evidence_level": "kernel_checked_sorry_free_at_pinned_commit",
        "later_commit_status_not_inferred": True,
    }
    classification = {
        "msc2020_code": source["msc2020"]["code"],
        "basis": source["msc2020"]["basis"],
        "status": (
            "source_curated_exact"
            if source["msc2020"]["basis"] == "1000_plus_curated"
            else "machine_root_crosswalk"
        ),
        "module_root": root,
    }
    provenance = {
        "formal_source_ref": SOURCE_ID,
        "source_refs": [SOURCE_ID],
        "extraction_mode": "pinned_mathlib_runtime_extraction",
        "extractor_path": "Docs/tools/extract_mathlib_theorems_v5.py",
        "extractor_version": "1.1.0",
        "extractor_file_sha256": (
            "0e26af2b6740abf4626f3cf43d84fb8f7e1f1a6104096e71f1f9b1f2c33189af"
        ),
        "source_asset_sha256": SOURCE_FILE_SHA256,
        "source_record_id": source_record_id,
        "source_record_sha256": source_record_hash,
        "mathlib_commit": MATHLIB_COMMIT,
        "exact_source_replay_required": True,
    }
    has_docs_signal = has_importance_signal(source, "mathlib_1000_theorems")
    rights = seal_field(
        {
            "formal_code_terms": "Apache-2.0",
            "docstring_terms": "Apache-2.0",
            "optional_metadata_terms": (
                "Unlicense" if has_docs_signal else "not_applicable"
            ),
            "status": "cleared_with_attribution",
            "redistribution_mode": "apache_2_0_with_attribution",
            "attribution": ["The mathlib Community"],
            "source_refs": [SOURCE_ID],
            "mathlib_license_sha256": (
                "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
            ),
            "catalog_relicenses_source": False,
        },
        "rights_payload_sha256",
    )
    source_proof = source["proof_evidence"]
    proof_evidence = seal_field(
        {
            "formal_proof_state": source["formal_proof_state"],
            "verification": source_proof["verification"],
            "uses_sorry": source_proof["uses_sorry"],
            "compiled_module": source_proof["compiled_module"],
            "ilean_path": source_proof["ilean_path"],
            "ilean_sha256": source_proof["ilean_sha256"],
            "olean_path": source_proof["olean_path"],
            "olean_sha256": source_proof["olean_sha256"],
            "batch_axiom_dependency_union": copy.deepcopy(
                source_proof["batch_axiom_dependency_union"]
            ),
            "axiom_evidence_scope": (
                "batch_union_not_per_declaration_exact_dependencies"
            ),
            "mathlib_commit": MATHLIB_COMMIT,
        },
        "proof_payload_sha256",
    )
    importance = {
        "tier": "source_signaled_mathlib_theorem",
        "basis": (
            "mathlib_1000_formalized_signal"
            if has_docs_signal
            else "mathlib_module_main_result_signal"
        ),
        "rationale": (
            "Selected from the pinned formalized mathlib 1000-theorems signal."
            if has_docs_signal
            else "Selected from a pinned mathlib module Main-result signal."
        ),
        "evidence_level": "source_documentation_signal",
        "independent_universal_ranking_claimed": False,
    }
    dedupe = {
        "normalized_declaration_key": normalize_declaration_name(
            str(source["declaration"])
        ),
        "formal_type_sha256": statement_type_hash,
        "source_record_sha256": source_record_hash,
        "semantic_key": semantic_key,
        "candidate_atv_ids": [],
        "parent_catalog_file_sha256": sha256_file(
            PARENT_DIR / "Claim_Catalog.json"
        ),
        "verdict": "unique_after_source_and_parent_curation",
        "validation_status": "machine_replayed_and_manifest_bound_curation",
        "duplicate_grants_quota": False,
        "no_evidence_or_status_inheritance": True,
    }
    allocation_request = {
        "origin_release": RELEASE,
        "source_id": SOURCE_ID,
        "source_record_id": source_record_id,
        "source_record_sha256": source_record_hash,
        "semantic_key": semantic_key,
        "statement_sha256": mathematical_statement["statement_sha256"],
        "family_action": "new_family",
    }
    allocation = {
        "parent_registry_authority_sha256": parent_registry_authority,
        "parent_release_root_sha256": parent_release_root,
        "allocation_request_sha256": sha256_bytes(
            canonical_json_bytes(allocation_request)
        ),
        "transaction_id": f"S5-ALLOC-{atv_ordinal:08d}",
        "family_action": "new_family",
        "append_only": True,
    }
    aliases = list(
        dict.fromkeys(
            value
            for value in (
                str(source["declaration"]),
                str(source["exact_curated_summary"]),
            )
            if value != str(source["display_label"])
        )
    )
    row: dict[str, Any] = {
        "schema_version": "awesome-theorems/stage5-math-claim-record/5.3",
        "release_id": RELEASE,
        "origin_stage": "Stage5",
        "origin_release": RELEASE,
        "curation_key": f"mathlib/{source_record_id}",
        "allocation": allocation,
        "occurrence_id": f"ATO-{atv_ordinal:08d}",
        "family_id": f"ATF-{atf_ordinal:08d}",
        "sense_id": f"ATS-{atv_ordinal:08d}",
        "variant_id": f"ATV-{atv_ordinal:08d}",
        "stage_claim_id": f"S5-CLM-{atv_ordinal:08d}",
        "display_name": source["display_label"],
        "aliases": aliases,
        "owner_domain": "mathematics",
        "membership_domains": ["mathematics"],
        "record_role": "claim",
        "claim_kind": "theorem",
        "current_claim_kind": "theorem",
        "historical_kind": "theorem",
        "atomicity": "atomic",
        "truth_apt": True,
        "category": "theorem",
        "material_status": "proved",
        "source_id": SOURCE_ID,
        "source_locator": source_locator,
        "formal_statement": formal_statement,
        "theorem_selection": theorem_selection,
        "curator_disposition": curator_disposition,
        "mathematical_statement": mathematical_statement,
        "status_detail": status_detail,
        "classification": classification,
        "provenance": provenance,
        "rights": rights,
        "dedupe": dedupe,
        "proof_evidence": proof_evidence,
        "importance": importance,
        "lifecycle": "active",
        "lineage": [],
        "semantic_key": semantic_key,
    }
    row["content_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "formal_statement": formal_statement,
                "mathematical_statement": mathematical_statement,
            }
        )
    )
    row["source_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "source_locator": source_locator,
                "theorem_selection": theorem_selection,
                "provenance": provenance,
            }
        )
    )
    row["proof_payload_sha256"] = proof_evidence["proof_payload_sha256"]
    row["semantic_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(
            {
                "record_role": row["record_role"],
                "atomicity": row["atomicity"],
                "truth_apt": row["truth_apt"],
                "category": row["category"],
                "current_claim_kind": row["current_claim_kind"],
                "semantic_key": semantic_key,
                "statement_sha256": mathematical_statement["statement_sha256"],
            }
        )
    )
    validate_schema_instance(row, schema, schema)
    require(
        row["variant_id"] == ledger_row["target_variant_id"]
        and row["stage_claim_id"] == ledger_row["target_s5_id"],
        "claim allocation differs from curation targets",
    )
    require(
        set(row) == set(schema["required"]) == set(schema["properties"]),
        "generated claim-record field closure drifted",
    )
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
        "parent_receipt": authority_binding(PARENT_RECEIPT_PATH, receipt),
        "curation_ledger": authority_binding(CURATION_PATH, curation),
        "mathlib_asset": {
            "path": relative_path(SOURCE_PATH),
            "file_sha256": sha256_file(SOURCE_PATH),
            "size_bytes": SOURCE_PATH.stat().st_size,
            "content_digest_before_self_field": SOURCE_CONTENT_DIGEST,
            "mathlib_commit": MATHLIB_COMMIT,
        },
        "parent_release": {
            "release": PARENT_RELEASE,
            "release_root_sha256": parent[MANIFEST_NAME][
                "release_root_sha256"
            ],
            "manifest_file_sha256": sha256_file(PARENT_DIR / MANIFEST_NAME),
            "manifest_authority_sha256": parent[MANIFEST_NAME][
                "authority_sha256"
            ],
            "registry_authority_sha256": parent["Claim_ID_Registry.json"][
                "authority_sha256"
            ],
        },
    }


def build_coverage(
    parent: Mapping[str, Any],
    curation: Mapping[str, Any],
    new_rows: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    additions: list[dict[str, Any]] = []
    for row in curation["candidate_dispositions"]:
        additions.append(
            {
                "candidate_key": row["candidate_key"],
                "source_id": SOURCE_ID,
                "source_index": row["source_index"],
                "source_record_id": row["source_record_id"],
                "source_record_sha256": row["source_record_sha256"],
                "declaration": row["declaration"],
                "declaration_kind": row["declaration_kind"],
                "source_syntax_kind": row["source_syntax_kind"],
                "formal_type_sha256": row["formal_type_sha256"],
                "semantic_key": row["semantic_key"],
                "disposition": row["disposition"],
                "reason_code": row["reason_code"],
                "accepted_rank": row["accepted_rank"],
                "target_variant_id": row["target_variant_id"],
                "target_s5_id": row["target_s5_id"],
                "canonical_source_record_id": row[
                    "canonical_source_record_id"
                ],
                "duplicate_of_semantic_key": row[
                    "duplicate_of_semantic_key"
                ],
                "duplicate_of_variant_id": row["duplicate_of_variant_id"],
                "grants_catalog_entry": row["grants_catalog_entry"],
                "grants_theorem_credit": row["grants_theorem_credit"],
                "origin_release": RELEASE,
                "curation_row_sha256": row["row_sha256"],
            }
        )
    candidates = copy.deepcopy(parent["candidate_dispositions"]) + additions
    require(
        candidates[: len(parent["candidate_dispositions"])]
        == parent["candidate_dispositions"],
        "coverage candidate parent prefix changed",
    )
    new_by_code: dict[str, list[Mapping[str, Any]]] = {}
    for row in new_rows:
        new_by_code.setdefault(str(row["classification"]["msc2020_code"]), []).append(
            row
        )
    coverage_rows: list[dict[str, Any]] = []
    for parent_row in parent["msc_coverage"]:
        row = copy.deepcopy(parent_row)
        code = str(row["msc_top_class"])
        additions_for_code = new_by_code.pop(code, [])
        new_ids = sorted(str(item["stage_claim_id"]) for item in additions_for_code)
        row["current_theorem_s5_ids"] = sorted(
            list(row["current_theorem_s5_ids"]) + new_ids
        )
        row["origin_theorem_s5_ids"] = new_ids
        row["origin_open_s5_ids"] = []
        if additions_for_code:
            row["source_ids"] = sorted(set(row["source_ids"]) | {SOURCE_ID})
        exact_count = sum(
            item["classification"]["basis"] == "1000_plus_curated"
            for item in additions_for_code
        )
        crosswalk_count = len(additions_for_code) - exact_count
        row["classification_basis_counts"]["source_annotation"] += exact_count
        row["classification_basis_counts"]["machine_crosswalk"] += crosswalk_count
        counts = row["counts"]
        counts["current_theorems"] = len(row["current_theorem_s5_ids"])
        counts["current_open"] = len(row["current_open_s5_ids"])
        counts["origin_theorems"] = len(new_ids)
        counts["origin_open"] = 0
        counts["open_reserve"] = len(row["open_reserve_candidate_keys"])
        classified = (
            counts["current_theorems"]
            + counts["current_open"]
            + counts["open_reserve"]
        )
        if classified == 0:
            row["scarcity"] = "zero"
            row["scarcity_reason"] = (
                "No current or open-reserve member has this primary source annotation."
            )
        elif classified < 10:
            row["scarcity"] = "thin"
            row["scarcity_reason"] = (
                "Fewer than ten current-plus-reserve members have this primary class."
            )
        else:
            row["scarcity"] = "adequate_in_source_inventory"
            row["scarcity_reason"] = (
                "At least ten current-plus-reserve members have this primary class."
            )
        coverage_rows.append(row)
    require(not new_by_code, f"new records use unknown MSC classes: {sorted(new_by_code)}")
    disposition_counts = Counter(item["disposition"] for item in additions)
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-coverage-ledger/5.3",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "candidate_dispositions": candidates,
            "msc_coverage": coverage_rows,
            "counts": {
                "candidate_dispositions": len(candidates),
                "msc_coverage": len(coverage_rows),
                "origin_5_3_candidates": len(additions),
                "origin_5_3_accepted_new_theorems": disposition_counts[
                    "accepted_new_kernel_checked_theorem"
                ],
                "origin_5_3_literal_lemma_noncredit": disposition_counts[
                    "rejected_nonliteral_lemma"
                ],
                "origin_5_3_source_duplicate_noncredit": disposition_counts[
                    "rejected_source_semantic_duplicate"
                ],
                "origin_5_3_eligible_not_selected": disposition_counts[
                    "eligible_not_selected"
                ],
            },
        }
    )


def build_strict_ledger(
    parent: Mapping[str, Any], parent_root: str
) -> dict[str, Any]:
    credits = copy.deepcopy(parent["strict_credits"])
    corrections = copy.deepcopy(parent["credit_corrections"])
    counts = copy.deepcopy(parent["counts"])
    digests = copy.deepcopy(parent["set_digests"])
    require(
        len(credits) == counts["effective_strict_credits"] == 1_000
        and len(corrections) == counts["credit_corrections"] == 1,
        "parent strict-credit cardinality drifted",
    )
    require(
        set_digest(row["stage_claim_id"] for row in credits)
        == digests["effective_s5_id_set_sha256"]
        and set_digest(row["variant_id"] for row in credits)
        == digests["effective_variant_id_set_sha256"],
        "parent strict-credit set digests drifted",
    )
    result = seal(
        {
            "schema_version": "awesome-theorems/stage5-strict-conjecture-ledger/5.3",
            "release": RELEASE,
            "parent_release_root_sha256": parent_root,
            "parent_strict_ledger_file_sha256": sha256_file(
                PARENT_DIR / "Strict_Conjecture_Ledger.json"
            ),
            "parent_strict_ledger_authority_sha256": parent[
                "authority_sha256"
            ],
            "strict_credits": credits,
            "credit_corrections": corrections,
            "counts": counts,
            "set_digests": digests,
        }
    )
    require(
        result["strict_credits"] == parent["strict_credits"]
        and result["credit_corrections"] == parent["credit_corrections"]
        and result["counts"] == parent["counts"]
        and result["set_digests"] == parent["set_digests"],
        "5.3 strict-credit inheritance changed parent values",
    )
    return result


def package_release(
    artifacts: Mapping[str, Mapping[str, Any]],
    inputs: Mapping[str, Any],
    curation: Mapping[str, Any],
) -> tuple[dict[str, bytes], str]:
    require(set(artifacts) == set(RELEASE_FILES), "generated artifact set drifted")
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
    strict = artifacts["Strict_Conjecture_Ledger.json"]
    digests = curation["set_digests"]
    manifest = seal(
        {
            "schema_version": "awesome-theorems/stage5-release-manifest/5.3",
            "release": RELEASE,
            "parent_release": PARENT_RELEASE,
            "parent_release_root_sha256": inputs["parent_release"][
                "release_root_sha256"
            ],
            "release_root_sha256": root,
            "authoritative_inputs": copy.deepcopy(inputs),
            "accepted_set_digests": {
                "source_record_id_set_sha256": digests[
                    "selected_source_record_id_set_sha256"
                ],
                "declaration_set_sha256": digests[
                    "selected_declaration_set_sha256"
                ],
                "formal_type_sha256_set_sha256": digests[
                    "selected_formal_type_sha256_set_sha256"
                ],
                "semantic_key_set_sha256": digests[
                    "selected_semantic_key_set_sha256"
                ],
                "variant_id_set_sha256": digests[
                    "selected_variant_id_set_sha256"
                ],
                "s5_id_set_sha256": digests["selected_s5_id_set_sha256"],
            },
            "strict_credit_binding": {
                "path": "Strict_Conjecture_Ledger.json",
                "file_sha256": sha256_bytes(
                    encoded["Strict_Conjecture_Ledger.json"]
                ),
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
                "cumulative_open_claims": catalog_counts[
                    "cumulative_open_claims"
                ],
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
    curation: Mapping[str, Any],
) -> None:
    for name, value in artifacts.items():
        require(
            value.get("authority_sha256") == document_sha256(value),
            f"generated seal stale: {name}",
        )
    catalog = artifacts["Claim_Catalog.json"]
    parent_catalog = parent["Claim_Catalog.json"]
    require(
        catalog["records"][:3_100] == parent_catalog["records"]
        and catalog["records"][3_100:] == list(new_rows),
        "catalog parent prefix or addition order drifted",
    )
    require(
        catalog["counts"]
        == {
            "records": 3_600,
            "origin_theorems": 500,
            "origin_open_claims": 0,
            "cumulative_theorems": 2_000,
            "cumulative_open_claims": 1_600,
        },
        "catalog counts drifted",
    )
    theorem = artifacts["Theorem_List.json"]
    open_list = artifacts["Open_Claim_List.json"]
    require(
        theorem["counts"]["records"] == 2_000
        and theorem["records"][:1_500] == parent["Theorem_List.json"]["records"]
        and theorem["records"][1_500:] == list(new_rows),
        "theorem projection drifted",
    )
    require(
        open_list["counts"]["records"] == 1_600
        and open_list["records"] == parent["Open_Claim_List.json"]["records"]
        and open_list["stage_claim_ids"]
        == parent["Open_Claim_List.json"]["stage_claim_ids"],
        "open-claim projection changed",
    )
    expected_atv = [
        f"ATV-{value:08d}"
        for value in range(PARENT_ATV_HIGH_WATERMARK + 1, LAST_ATV_ORDINAL + 1)
    ]
    expected_atf = [
        f"ATF-{value:08d}"
        for value in range(PARENT_ATF_HIGH_WATERMARK + 1, LAST_ATF_ORDINAL + 1)
    ]
    require(
        [row["variant_id"] for row in new_rows] == expected_atv
        and [row["occurrence_id"] for row in new_rows]
        == [value.replace("ATV-", "ATO-") for value in expected_atv]
        and [row["sense_id"] for row in new_rows]
        == [value.replace("ATV-", "ATS-") for value in expected_atv]
        and [row["family_id"] for row in new_rows] == expected_atf
        and [row["stage_claim_id"] for row in new_rows]
        == [
            f"S5-CLM-{value:08d}"
            for value in range(
                PARENT_ATV_HIGH_WATERMARK + 1, LAST_ATV_ORDINAL + 1
            )
        ],
        "new identity suffixes drifted",
    )
    registry = artifacts["Claim_ID_Registry.json"]
    require(
        registry["namespace_high_watermarks"]
        == {
            "ATF": LAST_ATF_ORDINAL,
            "ATO": LAST_ATV_ORDINAL,
            "ATS": LAST_ATV_ORDINAL,
            "ATV": LAST_ATV_ORDINAL,
        },
        "registry high-watermarks drifted",
    )
    for artifact_name, key in (
        ("Claim_ID_Registry.json", "variants"),
        ("Stage5_Claim_ID_Registry.json", "mappings"),
        ("Migration_v4_to_v5.json", "migrations"),
    ):
        parent_rows = parent[artifact_name][key]
        require(
            artifacts[artifact_name][key][: len(parent_rows)] == parent_rows,
            f"{artifact_name} parent prefix drifted",
        )
    accepted = sorted(
        (
            row
            for row in curation["candidate_dispositions"]
            if row["grants_catalog_entry"] is True
        ),
        key=lambda row: int(row["accepted_rank"]),
    )
    require(
        [row["theorem_selection"]["source_record_id"] for row in new_rows]
        == [row["source_record_id"] for row in accepted]
        and [row["semantic_key"] for row in new_rows]
        == [row["semantic_key"] for row in accepted],
        "catalog additions differ from accepted curation set",
    )
    require(
        all(theorem_predicate(row) for row in new_rows)
        and not any(open_predicate(row) for row in new_rows),
        "new rows fail exact theorem/open predicates",
    )
    coverage = artifacts["Coverage_Ledger.json"]
    parent_coverage = parent["Coverage_Ledger.json"]
    require(
        coverage["candidate_dispositions"][: len(parent_coverage["candidate_dispositions"])]
        == parent_coverage["candidate_dispositions"],
        "coverage candidate parent prefix drifted",
    )
    strict = artifacts["Strict_Conjecture_Ledger.json"]
    parent_strict = parent["Strict_Conjecture_Ledger.json"]
    for field in ("strict_credits", "credit_corrections", "counts", "set_digests"):
        require(
            strict[field] == parent_strict[field],
            f"strict ledger inherited {field} changed",
        )


def build_all() -> tuple[dict[str, bytes], str, dict[str, Any]]:
    contract, schema, sources, receipt, curation = verify_authorities()
    require(
        tuple(contract["release_layout"]["non_manifest_artifacts"])
        == RELEASE_FILES,
        "contract release artifact order/set differs from generator",
    )
    parent = verify_parent_release(contract)
    verify_parent_receipt(receipt, parent)
    _source, source_rows, _source_indexes, source_hashes = load_source_artifact()
    accepted = verify_curation(
        contract,
        curation,
        source_rows,
        source_hashes,
        parent["Claim_Catalog.json"]["records"],
    )
    parent_registry = parent["Claim_ID_Registry.json"]
    parent_root = parent[MANIFEST_NAME]["release_root_sha256"]
    new_rows = [
        build_claim_row(
            ledger_row,
            source_row,
            parent_registry["authority_sha256"],
            parent_root,
            curation["authority_sha256"],
            schema,
        )
        for ledger_row, source_row in accepted
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
            parent["Coverage_Ledger.json"], curation, new_rows, inputs
        ),
        "Strict_Conjecture_Ledger.json": build_strict_ledger(
            parent["Strict_Conjecture_Ledger.json"], parent_root
        ),
    }
    validate_generated(artifacts, parent, new_rows, curation)
    package, root = package_release(artifacts, inputs, curation)
    return package, root, {
        "selected": len(new_rows),
        "catalog_records": catalog["counts"]["records"],
        "theorems": artifacts["Theorem_List.json"]["counts"]["records"],
        "open_claims": artifacts["Open_Claim_List.json"]["counts"]["records"],
        "strict_credits": artifacts["Strict_Conjecture_Ledger.json"]["counts"][
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
        f"release artifact set differs at {path}: "
        f"files={sorted(actual_names)}, non_files={sorted(non_files)}",
    )
    for name in sorted(expected):
        try:
            observed = (path / name).read_bytes()
        except OSError as error:
            raise GenerationError(
                f"cannot read release artifact {path / name}: {error}"
            ) from error
        require(
            observed == expected[name],
            f"immutable release byte drift: {path / name}",
        )


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
        require(
            current.get("release_root_sha256") == expected_root,
            "current 5.3 root differs from generated root",
        )
        require(
            current.get("manifest_sha256")
            == sha256_bytes(expected_package[MANIFEST_NAME]),
            "current 5.3 manifest hash differs from generated manifest",
        )
        compare_release(output_root / "releases" / RELEASE, expected_package)
        return "already_current"
    require(
        current_release == PARENT_RELEASE,
        f"compare-and-swap parent is {current_release}, expected {PARENT_RELEASE}",
    )
    parent_manifest = PARENT_DIR / MANIFEST_NAME
    parent_manifest_value, _ = load_json(parent_manifest)
    require(
        current.get("release_root_sha256")
        == parent_manifest_value["release_root_sha256"],
        "compare-and-swap parent root drifted",
    )
    require(
        current.get("manifest_sha256") == sha256_file(parent_manifest),
        "compare-and-swap parent manifest drifted",
    )
    output_parent = output_root / "releases" / PARENT_RELEASE
    require(
        (output_parent / MANIFEST_NAME).is_file()
        and (output_parent / "Claim_ID_Registry.json").is_file(),
        "output root lacks compare-and-swap parent files",
    )
    require(
        sha256_file(output_parent / MANIFEST_NAME) == sha256_file(parent_manifest),
        "output parent manifest differs from canonical parent",
    )
    output_registry, _ = load_json(output_parent / "Claim_ID_Registry.json")
    canonical_registry, _ = load_json(PARENT_DIR / "Claim_ID_Registry.json")
    verify_seal(output_registry, str(output_parent / "Claim_ID_Registry.json"))
    require(
        output_registry["authority_sha256"]
        == canonical_registry["authority_sha256"],
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


def update_current(
    output_root: Path, package: Mapping[str, bytes], root: str
) -> None:
    pointer = seal(
        {
            "schema_version": "awesome-theorems/stage5-current-release/5.3",
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
        help="Stage5 catalog root receiving releases/5.3 and Current_Release.json",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="compare the existing immutable 5.3 release byte-for-byte",
    )
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="authenticate and build entirely in memory without writing",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    output_root = args.output_root.resolve()
    try:
        if args.dry_run:
            _package, root, counts = build_all()
            print(
                "PASS generate_math_catalog_v5_3 --dry-run "
                f"release={RELEASE} root={root} "
                f"counts={json.dumps(counts, sort_keys=True, separators=(',', ':'))}"
            )
            return 0
        if args.check:
            package, root, _counts = build_all()
            compare_release(output_root / "releases" / RELEASE, package)
            print(
                f"PASS generate_math_catalog_v5_3 --check "
                f"release={RELEASE} root={root}"
            )
            return 0
        with exclusive_writer_lock(output_root):
            package, root, _counts = build_all()
            cas_state = verify_current_cas(output_root, package, root)
            if cas_state != "already_current":
                publish_release(output_root, package)
                compare_release(output_root / "releases" / RELEASE, package)
                update_current(output_root, package, root)
        print(f"PASS generate_math_catalog_v5_3 release={RELEASE} root={root}")
        return 0
    except (
        GenerationError,
        OSError,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
    ) as error:
        print(f"FAIL generate_math_catalog_v5_3: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
