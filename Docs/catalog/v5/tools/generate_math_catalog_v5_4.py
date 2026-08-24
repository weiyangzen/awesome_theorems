#!/usr/bin/env python3
"""Materialize the immutable append-only Stage5 mathematics release 5.4.

Release 5.4 preserves every 5.3 record/identity/migration row, appends the
500 exact residual mathlib theorem selections sealed by the 5.4 curation
ledger, carries the 1,600 open claims and effective 1,000 strict-conjecture
credits unchanged, then compare-and-swaps ``Current_Release.json`` from 5.3.

Only Python's standard library is required.  The established 5.3 generator is
loaded solely for its already-reviewed single-mathlib-record constructor and
canonical helpers; this module owns all 5.4 authority, append, root, manifest,
publish, readable and validation logic.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any, Iterable, Iterator, Mapping, Sequence
import unicodedata


REPO_ROOT = Path(__file__).resolve().parents[4]
V5_ROOT = REPO_ROOT / "Docs/catalog/v5"
PARENT_DIR = V5_ROOT / "releases/5.3"
RELEASE_DIR = V5_ROOT / "releases/5.4"
READABLE_DIR = V5_ROOT / "readable/5.4"
SOURCE_PATH = V5_ROOT / "sources/mathlib-theorems-8a178386.json"
CURATION_PATH = V5_ROOT / "curation/Mathlib_Theorem_Curation_v5_4.json"
CONTRACT_PATH = V5_ROOT / "Stage5_Math_Expansion_Contract_v5_4.json"
SCHEMA_PATH = V5_ROOT / "Math_Claim_Record_Schema_v5_4.json"
SOURCE_REGISTRY_PATH = V5_ROOT / "Math_Source_Registry_v5_4.json"
PARENT_RECEIPT_PATH = V5_ROOT / "V5_3_Parent_Receipt_v5_4.json"
CURRENT_PATH = V5_ROOT / "Current_Release.json"
LOCK_PATH = V5_ROOT / ".Current_Release.lock"
LEGACY_GENERATOR_PATH = REPO_ROOT / "Docs/tools/generate_math_catalog_v5_3.py"
LEGACY_SCHEMA_PATH = V5_ROOT / "Math_Claim_Record_Schema_v5_3.json"

RELEASE = "5.4"
PARENT_RELEASE = "5.3"
SOURCE_ID = "SRC-MATH-V5-MATHLIB-8A178386"
SOURCE_SHA256 = "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a"
SOURCE_SIZE_BYTES = 6_316_287
SOURCE_CONTENT_DIGEST = "dd49c8322d8eded995c84a235fd458fc093a187230323f87bea78049ae90e53b"
MATHLIB_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
PARENT_ROOT = "9ec5a097c0286b6751b02e89d18c400aab655021ba1ad4843eadba5a69fc41fa"
PARENT_MANIFEST_SHA256 = "8384deebd8ff33cf06c592ed443fd3ed78a4a294c4cea106362705e95954419a"
PARENT_CATALOG_SHA256 = "957da23fbd1e50244912fb6dbb76fbf663e7970ace3f6da8b19407929211a8bb"
PARENT_ATV_HIGH = 7_084
PARENT_ATF_HIGH = 6_854
LAST_ATV = 7_584
LAST_ATF = 7_354
NEW_ROWS = 500

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
ALL_RELEASE_FILES = frozenset((*RELEASE_FILES, MANIFEST_NAME))
AUTHORITY_POLICY = (
    "sha256 over UTF-8 json.dumps(value, ensure_ascii=False, sort_keys=True, "
    "separators=(',', ':')) after removing only the top-level authority_sha256 field"
)
EXPECTED_ROOT_COUNTS = {
    "Algebra": 13,
    "Analysis": 103,
    "FieldTheory": 64,
    "LinearAlgebra": 17,
    "MeasureTheory": 77,
    "NumberTheory": 67,
    "RingTheory": 103,
    "Topology": 56,
}

ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
ATF_RE = re.compile(r"^ATF-([0-9]{8})$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")


class GenerationError(RuntimeError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise GenerationError(f"not canonical-JSON serializable: {error}") from error


def encoded_document(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return sha256_bytes(
        canonical_json_bytes({key: item for key, item in value.items() if key not in omitted})
    )


def seal(value: Mapping[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(dict(value))
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def verify_seal(value: Mapping[str, Any], label: str) -> None:
    if value.get("authority_sha256") != hash_without(value, "authority_sha256"):
        raise GenerationError(f"{label} has stale authority_sha256")


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical_json_bytes(sorted(values)))


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


def validate_closed_record_schema(
    row: Mapping[str, Any], schema: Mapping[str, Any], label: str
) -> None:
    """Replay the closed top-level JSON Schema subset used by 5.4.

    The record schema deliberately keeps the nested proof/source rules outside
    JSON Schema.  Those rules are replayed separately by
    :func:`validate_new_claim_row`; this function makes sure the legacy
    constructor cannot bypass the closed top-level contract.
    """
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        raise GenerationError("5.4 claim schema is not a closed object schema")
    required = schema.get("required")
    properties = schema.get("properties")
    if not isinstance(required, list) or not isinstance(properties, dict):
        raise GenerationError("5.4 claim schema required/properties are malformed")
    if len(required) != len(set(required)) or set(required) != set(properties):
        raise GenerationError("5.4 claim schema field closure drifted")
    if set(row) != set(required):
        missing = sorted(set(required) - set(row))
        extra = sorted(set(row) - set(required))
        raise GenerationError(f"{label} schema field closure mismatch: missing={missing} extra={extra}")
    for field, specification in properties.items():
        if not isinstance(specification, dict):
            raise GenerationError(f"5.4 schema property {field} is malformed")
        value = row[field]
        if "const" in specification and value != specification["const"]:
            raise GenerationError(f"{label}.{field} violates schema const")
        expected_type = specification.get("type")
        if isinstance(expected_type, str) and not _json_type_matches(value, expected_type):
            raise GenerationError(f"{label}.{field} violates schema type {expected_type}")
        minimum = specification.get("minLength")
        if isinstance(minimum, int) and isinstance(value, str) and len(value) < minimum:
            raise GenerationError(f"{label}.{field} violates schema minLength")
        pattern = specification.get("pattern")
        if isinstance(pattern, str) and (not isinstance(value, str) or re.fullmatch(pattern, value) is None):
            raise GenerationError(f"{label}.{field} violates schema pattern")


def validate_schema_instance(
    value: Any,
    schema: Mapping[str, Any],
    root: Mapping[str, Any],
    location: str = "$",
) -> None:
    """Validate the deeply closed Draft 2020-12 subset used by 5.4."""
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
            condition = False
        else:
            condition = True
        branch = schema.get("then" if condition else "else")
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
        missing = [item for item in schema.get("required", []) if item not in value]
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
        maximum = schema.get("maxItems")
        if minimum is not None and len(value) < minimum:
            raise GenerationError(f"schema minItems mismatch at {location}")
        if maximum is not None and len(value) > maximum:
            raise GenerationError(f"schema maxItems mismatch at {location}")
        if schema.get("uniqueItems") and len({canonical_json_bytes(item) for item in value}) != len(value):
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
        if schema.get("format") == "date" and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:
            raise GenerationError(f"schema date mismatch at {location}")
        if schema.get("format") == "date-time" and re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})",
            value,
        ) is None:
            raise GenerationError(f"schema date-time mismatch at {location}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise GenerationError(f"schema minimum mismatch at {location}")
        if "maximum" in schema and value > schema["maximum"]:
            raise GenerationError(f"schema maximum mismatch at {location}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GenerationError(f"cannot load {path}: {error}") from error
    if not isinstance(value, dict):
        raise GenerationError(f"{path} must contain one JSON object")
    return value


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def artifact_binding(path: Path, value: Mapping[str, Any]) -> dict[str, Any]:
    expected = encoded_document(value)
    payload = path.read_bytes() if path.is_file() else expected
    if payload != expected:
        raise GenerationError(f"authority bytes are not canonical/expected: {path}")
    return {
        "path": relative(path),
        "file_sha256": sha256_bytes(payload),
        "size_bytes": len(payload),
        "authority_sha256": value["authority_sha256"],
    }


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
        value = document.get(key)
        if isinstance(value, list):
            return len(value)
    return 0


def release_root(inventory: Sequence[Mapping[str, Any]]) -> str:
    normalized = [
        {"path": row["path"], "sha256": row["sha256"], "size_bytes": row["size_bytes"]}
        for row in sorted(inventory, key=lambda row: str(row["path"]))
    ]
    return sha256_bytes(canonical_json_bytes(normalized))


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def load_legacy_generator() -> Any:
    spec = importlib.util.spec_from_file_location("stage5_v53_record_constructor", LEGACY_GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise GenerationError("cannot load 5.3 record constructor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.RELEASE = RELEASE
    module.PARENT_RELEASE = PARENT_RELEASE
    module.PARENT_DIR = PARENT_DIR
    module.CURATION_PATH = CURATION_PATH
    module.PARENT_ATV_HIGH_WATERMARK = PARENT_ATV_HIGH
    module.PARENT_ATF_HIGH_WATERMARK = PARENT_ATF_HIGH
    module.LAST_ATV_ORDINAL = LAST_ATV
    module.LAST_ATF_ORDINAL = LAST_ATF
    module.NEW_ROWS = NEW_ROWS
    # The legacy constructor hard-codes its own 5.3 schema_version before this
    # module applies the 5.4 residual-selection fields.  Suppress only that
    # premature check; validate_schema_instance below replays the complete,
    # deeply closed 5.4 schema after every 5.4 mutation.
    module.validate_schema_instance = lambda *_args, **_kwargs: None
    return module


def parent_artifact_inventory() -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    for name in sorted(ALL_RELEASE_FILES):
        path = PARENT_DIR / name
        document = load_json(path)
        verify_seal(document, str(path))
        inventory.append(
            {
                "path": name,
                "file_sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
                "row_count": primary_row_count(document),
                "authority_sha256": document["authority_sha256"],
            }
        )
    return inventory


def build_schema() -> dict[str, Any]:
    old = load_json(LEGACY_SCHEMA_PATH)
    schema = copy.deepcopy(old)
    schema.pop("authority_sha256", None)
    schema["$id"] = "urn:awesome-theorems:schema:stage5-math-claim-record:5.4"
    schema["title"] = "Stage5 5.4 residual pinned-mathlib literal theorem record"
    schema["description"] = (
        "Deeply closed schema for one origin-5.4 theorem selected from the exact "
        "5.3 residual mathlib pool. Every nested proof, source, curation, identity, "
        "rights, classification and payload field remains closed and independently replayed."
    )
    properties = schema["properties"]
    properties["schema_version"] = {"const": "awesome-theorems/stage5-math-claim-record/5.4"}
    properties["release_id"] = {"const": RELEASE}
    properties["origin_release"] = {"const": RELEASE}
    definitions = schema["$defs"]
    definitions["allocation"]["properties"]["parent_registry_authority_sha256"] = {
        "const": "0f3e83d01ddf507dcc3e374f76b5ce7b6310b2598a5be9c4b6e3f572d06229d2"
    }
    definitions["allocation"]["properties"]["parent_release_root_sha256"] = {
        "const": PARENT_ROOT
    }
    selection = definitions["theorem_selection"]["properties"]
    selection["selection_phase"] = {"const": "selected_remaining_module_root_round_robin"}
    selection["phase_rank"] = {"type": "integer", "minimum": 1, "maximum": 500}
    disposition = definitions["curator_disposition"]["properties"]
    disposition["curation_ledger_path"] = {"const": relative(CURATION_PATH)}
    disposition["reason_code"] = {"const": "selected_remaining_module_root_round_robin"}
    definitions["dedupe"]["properties"]["parent_catalog_file_sha256"] = {
        "const": PARENT_CATALOG_SHA256
    }
    return seal(schema)


def build_source_registry() -> dict[str, Any]:
    parent = load_json(V5_ROOT / "Math_Source_Registry_v5_3.json")
    verify_seal(parent, "Math_Source_Registry_v5_3.json")
    parent_path = V5_ROOT / "Math_Source_Registry_v5_3.json"
    parent_sources = copy.deepcopy(parent["sources"])
    if len(parent_sources) != 1 or parent_sources[0].get("source_id") != SOURCE_ID:
        raise GenerationError("5.3 source registry does not expose the exact pinned mathlib row")
    parent_source_sha256 = sha256_bytes(canonical_json_bytes(parent_sources[0]))
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-math-source-registry/5.4",
            "registry_status": "pinned_mathlib_residual_source_ready_for_5_4_append",
            "reviewed_as_of": "2026-08-10",
            "authority_hash_policy": AUTHORITY_POLICY,
            "parent_registry": {
                "path": relative(parent_path),
                "file_sha256": sha256_file(parent_path),
                "authority_sha256": parent["authority_sha256"],
                "source_rows_rewritten": False,
                "resolution_rule": "All 5.3 source rows remain canonical byte-semantic rows; 5.4 adds only an explicitly versioned release-use policy extension.",
            },
            "source_record_contract": copy.deepcopy(parent["source_record_contract"]),
            "sources": parent_sources,
            "source_policy_extensions": [
                {
                    "extension_id": "SRC-POLICY-MATHLIB-RESIDUAL-5.4",
                    "source_id": SOURCE_ID,
                    "applies_to_release": RELEASE,
                    "parent_source_registry_path": relative(parent_path),
                    "parent_source_row_sha256": parent_source_sha256,
                    "source_row_reused_without_rewrite": True,
                    "asset_identity_reused": {
                        "path": relative(SOURCE_PATH),
                        "sha256": SOURCE_SHA256,
                        "size_bytes": SOURCE_SIZE_BYTES,
                        "record_count": 1_500,
                        "mathlib_commit": MATHLIB_COMMIT,
                    },
                    "residual_selection": {
                        "parent_curation_path": relative(V5_ROOT / "curation/Mathlib_Theorem_Curation_v5_3.json"),
                        "parent_disposition": "eligible_not_selected",
                        "residual_unique_literal_theorems": 731,
                        "accepted_in_5_4": 500,
                        "remaining_after_5_4": 231,
                        "literal_lemma_grants_quota": False,
                        "identity_gates": [
                            "exact_formal_type_sha256",
                            "whitespace_normalized_formal_type",
                            "NFKC_casefolded_full_declaration_name",
                        ],
                    },
                    "release_use_eligibility": "eligible_for_5_4_residual_literal_theorem_append_only_under_sealed_curation",
                    "inherits_parent_proof_rights_locator_and_dedupe_policy": True,
                }
            ],
            "counts": {
                "inherited_source_rows": 1,
                "new_source_rows": 0,
                "source_policy_extensions": 1,
                "asset_rows": 1_500,
                "parent_literal_lemma_noncredit_rows": 265,
                "residual_literal_theorem_rows": 731,
                "exact_release_acceptance_rows": 500,
            },
            "source_readiness": {
                "mathlib_ready_for_residual_literal_theorem_only_5_4_intake": True,
                "release_completion_not_asserted_by_registry": True,
                "literal_lemma_grants_quota": False,
                "source_row_semantics_remain_the_5_3_authority": True,
            },
        }
    )


def build_parent_receipt() -> dict[str, Any]:
    manifest = load_json(PARENT_DIR / MANIFEST_NAME)
    registry = load_json(PARENT_DIR / "Claim_ID_Registry.json")
    catalog = load_json(PARENT_DIR / "Claim_Catalog.json")
    strict = load_json(PARENT_DIR / "Strict_Conjecture_Ledger.json")
    for label, document in (
        ("manifest", manifest),
        ("registry", registry),
        ("catalog", catalog),
        ("strict", strict),
    ):
        verify_seal(document, f"5.3 {label}")
    if manifest["release_root_sha256"] != PARENT_ROOT or sha256_file(
        PARENT_DIR / MANIFEST_NAME
    ) != PARENT_MANIFEST_SHA256:
        raise GenerationError("5.3 parent manifest binding drifted")
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-parent-release-receipt/5.4",
            "artifact": "V5_3_Parent_Receipt_v5_4.json",
            "receipt_status": "sealed_5_3_parent_boundary_for_5_4_mathlib_append",
            "reviewed_as_of": "2026-08-10",
            "authority_hash_policy": AUTHORITY_POLICY,
            "parent_release": {
                "release": PARENT_RELEASE,
                "release_root_sha256": PARENT_ROOT,
                "manifest_path": relative(PARENT_DIR / MANIFEST_NAME),
                "manifest_file_sha256": PARENT_MANIFEST_SHA256,
                "manifest_authority_sha256": manifest["authority_sha256"],
                "parent_bytes_are_immutable": True,
                "append_only_child_required": True,
            },
            "artifact_inventory": parent_artifact_inventory(),
            "identity_boundary": {
                "variant_high_watermark": PARENT_ATV_HIGH,
                "occurrence_high_watermark": PARENT_ATV_HIGH,
                "sense_high_watermark": PARENT_ATV_HIGH,
                "family_high_watermark": PARENT_ATF_HIGH,
                "catalog_records": len(catalog["records"]),
                "registry_variants": len(registry["variants"]),
                "first_child_variant_ordinal": PARENT_ATV_HIGH + 1,
                "parent_array_elements_must_be_canonical_byte_equal": True,
            },
            "claim_count_boundary": {
                "catalog_records": len(catalog["records"]),
                "theorem_records": len(load_json(PARENT_DIR / "Theorem_List.json")["records"]),
                "open_claim_records": len(load_json(PARENT_DIR / "Open_Claim_List.json")["records"]),
                "effective_strict_conjecture_credits": len(strict["strict_credits"]),
            },
            "strict_credit_boundary": {
                "ledger_file_sha256": sha256_file(PARENT_DIR / "Strict_Conjecture_Ledger.json"),
                "ledger_authority_sha256": strict["authority_sha256"],
                "set_digests": copy.deepcopy(strict["set_digests"]),
                "child_must_preserve_exact_credit_rows_and_corrections": True,
            },
        }
    )


def build_contract(
    schema: Mapping[str, Any], source_registry: Mapping[str, Any], receipt: Mapping[str, Any], curation: Mapping[str, Any]
) -> dict[str, Any]:
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-math-expansion-contract/5.4",
            "contract_status": "normative_5_4_residual_mathlib_literal_theorem_append_contract",
            "stage": "Stage5",
            "release": RELEASE,
            "review_date": "2026-08-10",
            "authority_hash_policy": AUTHORITY_POLICY,
            "parent": {
                "release": PARENT_RELEASE,
                "release_root_sha256": PARENT_ROOT,
                "manifest_file_sha256": PARENT_MANIFEST_SHA256,
                "variant_high_watermark": PARENT_ATV_HIGH,
                "family_high_watermark": PARENT_ATF_HIGH,
                "catalog_records": 3_600,
                "theorem_records": 2_000,
                "open_claim_records": 1_600,
                "effective_strict_conjecture_credits": 1_000,
            },
            "versioned_authorities": {
                "record_schema": artifact_binding(SCHEMA_PATH, schema),
                "source_registry": artifact_binding(SOURCE_REGISTRY_PATH, source_registry),
                "parent_receipt": artifact_binding(PARENT_RECEIPT_PATH, receipt),
                "curation_ledger": artifact_binding(CURATION_PATH, curation),
            },
            "source_and_selection": {
                "source_id": SOURCE_ID,
                "asset_path": relative(SOURCE_PATH),
                "asset_sha256": SOURCE_SHA256,
                "parent_curation_disposition": "eligible_not_selected",
                "residual_denominator": 731,
                "selection": "bytewise module-root round-robin over buckets ordered by selection_rank then source_record_id",
                "expected_selected_by_module_root": EXPECTED_ROOT_COUNTS,
                "three_identity_gates": [
                    "exact formal type hash",
                    "whitespace-normalized formal type",
                    "NFKC-casefolded full declaration name",
                ],
                "literal_lemma_is_theorem_credit": False,
            },
            "release_counts": {
                "origin_5_4_records": 500,
                "origin_5_4_theorems": 500,
                "origin_5_4_open_claims": 0,
                "cumulative_catalog_records": 4_100,
                "cumulative_theorem_records": 2_500,
                "cumulative_open_claim_records": 1_600,
                "effective_strict_conjecture_credits": 1_000,
                "all_counts_recomputed_from_explicit_rows": True,
            },
            "identity_allocation": {
                "ATO": [7_085, 7_584],
                "ATS": [7_085, 7_584],
                "ATV": [7_085, 7_584],
                "S5_CLM": [7_085, 7_584],
                "ATF": [6_855, 7_354],
                "append_only": True,
                "parent_prefix_rewrite_forbidden": True,
            },
            "release_layout": {
                "release_root": relative(RELEASE_DIR),
                "non_manifest_artifacts": list(RELEASE_FILES),
                "manifest_name": MANIFEST_NAME,
                "manifest_excluded_from_release_root": True,
                "release_root_formula": "sha256(canonical_json(sorted([{path,sha256,size_bytes}], key=path)))",
            },
            "acceptance_commands": [
                "python3 Docs/catalog/v5/tools/build_mathlib_theorem_curation_v5_4.py --check",
                "python3 Docs/catalog/v5/tools/generate_math_catalog_v5_4.py --check",
                "python3 Docs/catalog/v5/tools/check_math_catalog_v5_4.py --prepublish",
                "python3 -m unittest Docs.catalog.v5.tests.test_math_catalog_v5_4",
                "python3 Docs/tools/render_math_catalog_v5.py --release 5.4 --check",
                "python3 Docs/catalog/v5/tools/generate_math_catalog_v5_4.py --publish-current",
                "python3 Docs/catalog/v5/tools/check_math_catalog_v5_4.py",
            ],
        }
    )


def expected_authorities() -> dict[Path, dict[str, Any]]:
    curation = load_json(CURATION_PATH)
    verify_seal(curation, str(CURATION_PATH))
    if curation.get("schema_version") != "awesome-theorems/mathlib-theorem-curation/5.4":
        raise GenerationError("5.4 curation schema drifted")
    schema = build_schema()
    sources = build_source_registry()
    receipt = build_parent_receipt()
    contract = build_contract(schema, sources, receipt, curation)
    return {
        SCHEMA_PATH: schema,
        SOURCE_REGISTRY_PATH: sources,
        PARENT_RECEIPT_PATH: receipt,
        CONTRACT_PATH: contract,
    }


def materialize_authorities(authorities: Mapping[Path, Mapping[str, Any]], *, check: bool) -> None:
    for path, document in authorities.items():
        payload = encoded_document(document)
        if check:
            if not path.is_file() or path.read_bytes() != payload:
                raise GenerationError(f"versioned authority is missing/stale: {path}")
        elif path.exists():
            if path.read_bytes() != payload:
                raise GenerationError(f"refusing to rewrite unequal versioned authority: {path}")
        else:
            atomic_write(path, payload)


def load_parent() -> dict[str, dict[str, Any]]:
    if sha256_file(PARENT_DIR / MANIFEST_NAME) != PARENT_MANIFEST_SHA256:
        raise GenerationError("5.3 manifest bytes drifted")
    parent: dict[str, dict[str, Any]] = {}
    for name in ALL_RELEASE_FILES:
        path = PARENT_DIR / name
        document = load_json(path)
        verify_seal(document, str(path))
        parent[name] = document
    manifest = parent[MANIFEST_NAME]
    if manifest.get("release_root_sha256") != PARENT_ROOT:
        raise GenerationError("5.3 release root drifted")
    inventory = manifest.get("artifacts")
    if not isinstance(inventory, list) or release_root(inventory) != PARENT_ROOT:
        raise GenerationError("5.3 release root does not recompute")
    for binding in inventory:
        path = PARENT_DIR / binding["path"]
        if (
            sha256_file(path) != binding["sha256"]
            or path.stat().st_size != binding["size_bytes"]
        ):
            raise GenerationError(f"5.3 artifact binding drifted: {path.name}")
    return parent


def source_by_id() -> dict[str, dict[str, Any]]:
    if sha256_file(SOURCE_PATH) != SOURCE_SHA256 or SOURCE_PATH.stat().st_size != SOURCE_SIZE_BYTES:
        raise GenerationError("fixed mathlib source bytes drifted")
    document = load_json(SOURCE_PATH)
    rows = document.get("records")
    if not isinstance(rows, list) or len(rows) != 1_500:
        raise GenerationError("mathlib source denominator drifted")
    result = {row["source_record_id"]: row for row in rows if isinstance(row, dict)}
    if len(result) != 1_500:
        raise GenerationError("mathlib source IDs are not unique")
    return result


def validate_new_claim_row(
    row: Mapping[str, Any],
    ledger_row: Mapping[str, Any],
    source: Mapping[str, Any],
    parent_registry_authority: str,
    curation: Mapping[str, Any],
    schema: Mapping[str, Any],
) -> None:
    """Recompute every source-derived nested object and payload binding."""
    source_id = str(source["source_record_id"])
    label = f"5.4 claim {source_id}"
    validate_closed_record_schema(row, schema, label)
    validate_schema_instance(row, schema, schema, label)
    if ledger_row.get("row_sha256") != hash_without(ledger_row, "row_sha256"):
        raise GenerationError(f"{label} is bound to a stale curation row")
    source_hash = sha256_bytes(canonical_json_bytes(source))
    rank = int(ledger_row["accepted_rank"])
    atv_ordinal = PARENT_ATV_HIGH + rank
    atf_ordinal = PARENT_ATF_HIGH + rank
    source_data = source["source"]
    proof_source = source["proof_evidence"]
    root_parts = str(source_data["module"]).split(".")
    if len(root_parts) < 2 or root_parts[0] != "Mathlib" or not root_parts[1]:
        raise GenerationError(f"{label} has invalid Mathlib module")
    root = root_parts[1]
    semantic_key = "mathlib-theorem-semantic/" + str(source["formal_type_sha256"])

    expected_source_locator = {
        "source_id": SOURCE_ID,
        "artifact_path": relative(SOURCE_PATH),
        "artifact_sha256": SOURCE_SHA256,
        "artifact_size_bytes": SOURCE_SIZE_BYTES,
        "record_index": ledger_row["source_index"],
        "source_record_id": source_id,
        "source_record_sha256": source_hash,
        "mathlib_commit": MATHLIB_COMMIT,
        "module": source_data["module"],
        "source_path": source_data["path"],
        "source_sha256": source_data["source_sha256"],
        "url": source_data["url"],
        "source_range": source_data["range"],
        "selection_range": source_data["selection_range"],
    }
    expected_formal = {
        "language": "Lean4",
        "completeness": "exact_runtime_formal_type_and_source_locator",
        "declaration": source["declaration"],
        "declaration_kind": source["declaration_kind"],
        "source_syntax_kind": source["source_syntax_kind"],
        "module": source_data["module"],
        "formal_type": source["formal_type"],
        "formal_type_sha256": source["formal_type_sha256"],
        "formal_docstring": source["formal_docstring"],
        "formal_docstring_origin": source["formal_docstring_origin"],
        "formal_docstring_sha256": source["formal_docstring_sha256"],
    }
    expected_mathematical = {
        "completeness": "exact_formal",
        "language": "Lean4",
        "natural_language": source["exact_curated_summary"],
        "formal_type": source["formal_type"],
        "formal_type_sha256": source["formal_type_sha256"],
    }
    expected_mathematical["statement_sha256"] = sha256_bytes(
        canonical_json_bytes(expected_mathematical)
    )
    expected_selection = {
        "source_record_id": source_id,
        "selection_cohort": source["selection_cohort"],
        "selection_rank": source["selection_rank"],
        "display_label": source["display_label"],
        "exact_curated_summary": source["exact_curated_summary"],
        "importance_signals": source["importance_signals"],
        "selection_phase": "selected_remaining_module_root_round_robin",
        "phase_rank": rank,
        "module_root": root,
    }
    expected_curator = {
        "curation_ledger_path": relative(CURATION_PATH),
        "curation_ledger_file_sha256": sha256_file(CURATION_PATH),
        "curation_ledger_authority_sha256": curation["authority_sha256"],
        "source_index": ledger_row["source_index"],
        "source_record_id": source_id,
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
    expected_status = {
        "source_material_status": source["material_status"]["status"],
        "status_as_of_commit": source["material_status"]["as_of_commit"],
        "basis": source["material_status"]["basis"],
        "source_refs": [SOURCE_ID],
        "evidence_level": "kernel_checked_sorry_free_at_pinned_commit",
        "later_commit_status_not_inferred": True,
    }
    expected_classification = {
        "msc2020_code": source["msc2020"]["code"],
        "basis": source["msc2020"]["basis"],
        "status": (
            "source_curated_exact"
            if source["msc2020"]["basis"] == "1000_plus_curated"
            else "machine_root_crosswalk"
        ),
        "module_root": root,
    }
    expected_provenance = {
        "formal_source_ref": SOURCE_ID,
        "source_refs": [SOURCE_ID],
        "extraction_mode": "pinned_mathlib_runtime_extraction",
        "extractor_path": "Docs/tools/extract_mathlib_theorems_v5.py",
        "extractor_version": "1.1.0",
        "extractor_file_sha256": "0e26af2b6740abf4626f3cf43d84fb8f7e1f1a6104096e71f1f9b1f2c33189af",
        "source_asset_sha256": SOURCE_SHA256,
        "source_record_id": source_id,
        "source_record_sha256": source_hash,
        "mathlib_commit": MATHLIB_COMMIT,
        "exact_source_replay_required": True,
    }
    signal_kinds = {
        str(signal.get("kind"))
        for signal in source["importance_signals"]
        if isinstance(signal, dict)
    }
    has_docs_signal = "mathlib_1000_theorems" in signal_kinds
    expected_rights = {
        "formal_code_terms": "Apache-2.0",
        "docstring_terms": "Apache-2.0",
        "optional_metadata_terms": "Unlicense" if has_docs_signal else "not_applicable",
        "status": "cleared_with_attribution",
        "redistribution_mode": "apache_2_0_with_attribution",
        "attribution": ["The mathlib Community"],
        "source_refs": [SOURCE_ID],
        "mathlib_license_sha256": "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1",
        "catalog_relicenses_source": False,
    }
    expected_rights["rights_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(expected_rights)
    )
    expected_proof = {
        "formal_proof_state": source["formal_proof_state"],
        "verification": proof_source["verification"],
        "uses_sorry": proof_source["uses_sorry"],
        "compiled_module": proof_source["compiled_module"],
        "ilean_path": proof_source["ilean_path"],
        "ilean_sha256": proof_source["ilean_sha256"],
        "olean_path": proof_source["olean_path"],
        "olean_sha256": proof_source["olean_sha256"],
        "batch_axiom_dependency_union": proof_source["batch_axiom_dependency_union"],
        "axiom_evidence_scope": "batch_union_not_per_declaration_exact_dependencies",
        "mathlib_commit": MATHLIB_COMMIT,
    }
    expected_proof["proof_payload_sha256"] = sha256_bytes(
        canonical_json_bytes(expected_proof)
    )
    expected_importance = {
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
    expected_dedupe = {
        "normalized_declaration_key": unicodedata.normalize(
            "NFKC", str(source["declaration"])
        ).casefold().strip(),
        "formal_type_sha256": source["formal_type_sha256"],
        "source_record_sha256": source_hash,
        "semantic_key": semantic_key,
        "candidate_atv_ids": [],
        "parent_catalog_file_sha256": sha256_file(PARENT_DIR / "Claim_Catalog.json"),
        "verdict": "unique_after_source_and_parent_curation",
        "validation_status": "machine_replayed_and_manifest_bound_curation",
        "duplicate_grants_quota": False,
        "no_evidence_or_status_inheritance": True,
    }
    allocation_request = {
        "origin_release": RELEASE,
        "source_id": SOURCE_ID,
        "source_record_id": source_id,
        "source_record_sha256": source_hash,
        "semantic_key": semantic_key,
        "statement_sha256": expected_mathematical["statement_sha256"],
        "family_action": "new_family",
    }
    expected_allocation = {
        "parent_registry_authority_sha256": parent_registry_authority,
        "parent_release_root_sha256": PARENT_ROOT,
        "allocation_request_sha256": sha256_bytes(canonical_json_bytes(allocation_request)),
        "transaction_id": f"S5-ALLOC-{atv_ordinal:08d}",
        "family_action": "new_family",
        "append_only": True,
    }
    nested = {
        "allocation": expected_allocation,
        "source_locator": expected_source_locator,
        "formal_statement": expected_formal,
        "theorem_selection": expected_selection,
        "curator_disposition": expected_curator,
        "mathematical_statement": expected_mathematical,
        "status_detail": expected_status,
        "classification": expected_classification,
        "provenance": expected_provenance,
        "rights": expected_rights,
        "dedupe": expected_dedupe,
        "proof_evidence": expected_proof,
        "importance": expected_importance,
    }
    for field, expected in nested.items():
        if row[field] != expected:
            raise GenerationError(f"{label}.{field} differs from its pinned source derivation")

    aliases = list(
        dict.fromkeys(
            value
            for value in (str(source["declaration"]), str(source["exact_curated_summary"]))
            if value != str(source["display_label"])
        )
    )
    expected_scalars: dict[str, Any] = {
        "release_id": RELEASE,
        "curation_key": f"mathlib/{source_id}",
        "occurrence_id": f"ATO-{atv_ordinal:08d}",
        "family_id": f"ATF-{atf_ordinal:08d}",
        "sense_id": f"ATS-{atv_ordinal:08d}",
        "variant_id": f"ATV-{atv_ordinal:08d}",
        "stage_claim_id": f"S5-CLM-{atv_ordinal:08d}",
        "display_name": source["display_label"],
        "aliases": aliases,
        "membership_domains": ["mathematics"],
        "lineage": [],
        "semantic_key": semantic_key,
    }
    for field, expected in expected_scalars.items():
        if row[field] != expected:
            raise GenerationError(f"{label}.{field} allocation/source binding drifted")

    payloads = {
        "content_payload_sha256": sha256_bytes(
            canonical_json_bytes(
                {"formal_statement": expected_formal, "mathematical_statement": expected_mathematical}
            )
        ),
        "source_payload_sha256": sha256_bytes(
            canonical_json_bytes(
                {
                    "source_locator": expected_source_locator,
                    "theorem_selection": expected_selection,
                    "provenance": expected_provenance,
                }
            )
        ),
        "proof_payload_sha256": expected_proof["proof_payload_sha256"],
        "semantic_payload_sha256": sha256_bytes(
            canonical_json_bytes(
                {
                    "record_role": "claim",
                    "atomicity": "atomic",
                    "truth_apt": True,
                    "category": "theorem",
                    "current_claim_kind": "theorem",
                    "semantic_key": semantic_key,
                    "statement_sha256": expected_mathematical["statement_sha256"],
                }
            )
        ),
    }
    for field, expected in payloads.items():
        if row[field] != expected:
            raise GenerationError(f"{label}.{field} is stale")
    ledger_bindings = {
        "source_record_sha256": source_hash,
        "formal_type_sha256": source["formal_type_sha256"],
        "proof_evidence_payload_sha256": sha256_bytes(canonical_json_bytes(source["proof_evidence"])),
        "importance_payload_sha256": sha256_bytes(canonical_json_bytes(source["importance_signals"])),
        "rights_payload_sha256": sha256_bytes(canonical_json_bytes(source["rights"])),
        "semantic_key": semantic_key,
        "module_root": root,
        "target_variant_id": row["variant_id"],
        "target_s5_id": row["stage_claim_id"],
    }
    for field, expected in ledger_bindings.items():
        if ledger_row.get(field) != expected:
            raise GenerationError(f"{label} curation binding {field} drifted")
    if (
        source.get("declaration_kind") != "theorem"
        or source.get("source_syntax_kind") != "theorem"
        or ledger_row.get("grants_catalog_entry") is not True
        or ledger_row.get("grants_theorem_credit") is not True
    ):
        raise GenerationError(f"{label} fails literal-theorem quota gate")


def build_new_records(
    parent: Mapping[str, Mapping[str, Any]],
    curation: Mapping[str, Any],
    schema: Mapping[str, Any],
) -> list[dict[str, Any]]:
    rows = curation.get("candidate_dispositions")
    if not isinstance(rows, list) or len(rows) != 731:
        raise GenerationError("5.4 curation must conserve exactly 731 residual rows")
    accepted = sorted(
        (row for row in rows if isinstance(row, dict) and row.get("grants_theorem_credit") is True),
        key=lambda row: int(row["accepted_rank"]),
    )
    if len(accepted) != NEW_ROWS or [row["accepted_rank"] for row in accepted] != list(
        range(1, NEW_ROWS + 1)
    ):
        raise GenerationError("5.4 curation accepted rank set drifted")
    sources = source_by_id()
    legacy_schema = load_json(LEGACY_SCHEMA_PATH)
    legacy = load_legacy_generator()
    parent_registry = parent["Claim_ID_Registry.json"]
    result: list[dict[str, Any]] = []
    for ledger_row in accepted:
        source = sources.get(ledger_row["source_record_id"])
        if source is None:
            raise GenerationError("accepted curation source row is missing")
        row = legacy.build_claim_row(
            ledger_row,
            source,
            parent_registry["authority_sha256"],
            PARENT_ROOT,
            curation["authority_sha256"],
            legacy_schema,
        )
        row["schema_version"] = "awesome-theorems/stage5-math-claim-record/5.4"
        row["theorem_selection"]["selection_phase"] = "selected_remaining_module_root_round_robin"
        row["theorem_selection"]["phase_rank"] = ledger_row["accepted_rank"]
        row["source_payload_sha256"] = sha256_bytes(
            canonical_json_bytes(
                {
                    "source_locator": row["source_locator"],
                    "theorem_selection": row["theorem_selection"],
                    "provenance": row["provenance"],
                }
            )
        )
        validate_new_claim_row(
            row,
            ledger_row,
            source,
            parent_registry["authority_sha256"],
            curation,
            schema,
        )
        result.append(row)
    if [row["variant_id"] for row in result] != [
        f"ATV-{ordinal:08d}" for ordinal in range(7_085, 7_585)
    ]:
        raise GenerationError("new ATV allocation range drifted")
    if [row["family_id"] for row in result] != [
        f"ATF-{ordinal:08d}" for ordinal in range(6_855, 7_355)
    ]:
        raise GenerationError("new ATF allocation range drifted")
    if Counter(row["classification"]["module_root"] for row in result) != Counter(
        EXPECTED_ROOT_COUNTS
    ):
        raise GenerationError("new theorem root distribution drifted")
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
        and (
            row.get("origin_release") != RELEASE
            or (
                row.get("formal_statement", {}).get("declaration_kind") == "theorem"
                and row.get("formal_statement", {}).get("source_syntax_kind") == "theorem"
                and row.get("proof_evidence", {}).get("formal_proof_state")
                == "kernel_checked_sorry_free"
                and row.get("proof_evidence", {}).get("uses_sorry") is False
            )
        )
    )


def open_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("lifecycle") == "active"
        and row.get("record_role") == "claim"
        and row.get("atomicity") == "atomic"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("current_claim_kind") in {"conjecture", "hypothesis", "open_problem"}
        and row.get("material_status") in {"open", "partial", "independent", "disputed"}
    )


def authoritative_inputs(
    authorities: Mapping[Path, Mapping[str, Any]], curation: Mapping[str, Any], parent: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    return {
        "contract": artifact_binding(CONTRACT_PATH, authorities[CONTRACT_PATH]),
        "record_schema": artifact_binding(SCHEMA_PATH, authorities[SCHEMA_PATH]),
        "source_registry": artifact_binding(SOURCE_REGISTRY_PATH, authorities[SOURCE_REGISTRY_PATH]),
        "parent_receipt": artifact_binding(PARENT_RECEIPT_PATH, authorities[PARENT_RECEIPT_PATH]),
        "curation_ledger": artifact_binding(CURATION_PATH, curation),
        "mathlib_asset": {
            "path": relative(SOURCE_PATH),
            "file_sha256": SOURCE_SHA256,
            "size_bytes": SOURCE_SIZE_BYTES,
            "content_digest_before_self_field": SOURCE_CONTENT_DIGEST,
            "mathlib_commit": MATHLIB_COMMIT,
        },
        "parent_release": {
            "release": PARENT_RELEASE,
            "release_root_sha256": PARENT_ROOT,
            "manifest_file_sha256": PARENT_MANIFEST_SHA256,
            "manifest_authority_sha256": parent[MANIFEST_NAME]["authority_sha256"],
            "registry_authority_sha256": parent["Claim_ID_Registry.json"]["authority_sha256"],
        },
    }


def new_registry_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    families: list[dict[str, Any]] = []
    senses: list[dict[str, Any]] = []
    variants: list[dict[str, Any]] = []
    for row in rows:
        request = row["allocation"]["allocation_request_sha256"]
        display_titles = list(dict.fromkeys([row["display_name"], *row["aliases"]]))
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


def build_artifacts(
    parent: Mapping[str, Mapping[str, Any]], new_rows: Sequence[dict[str, Any]], inputs: Mapping[str, Any], curation: Mapping[str, Any]
) -> dict[str, dict[str, Any]]:
    parent_catalog = parent["Claim_Catalog.json"]
    records = copy.deepcopy(parent_catalog["records"]) + copy.deepcopy(list(new_rows))
    catalog = seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-catalog/5.4",
            "artifact": "Claim_Catalog.json",
            "release": RELEASE,
            "catalog_scope": parent_catalog["catalog_scope"],
            "authoritative_inputs": copy.deepcopy(inputs),
            "counts": {
                "records": len(records),
                "origin_theorems": sum(theorem_predicate(row) for row in new_rows),
                "origin_open_claims": sum(open_predicate(row) for row in new_rows),
                "cumulative_theorems": sum(theorem_predicate(row) for row in records),
                "cumulative_open_claims": sum(open_predicate(row) for row in records),
            },
            "records": records,
        }
    )

    parent_registry = parent["Claim_ID_Registry.json"]
    families, senses, variants = new_registry_rows(new_rows)
    allocation_policy = copy.deepcopy(parent_registry["allocation_policy"])
    allocation_policy.update(
        {
            "release_5_4_first_new_atv_ordinal": 7_085,
            "release_5_4_new_family_first_atf_ordinal": 6_855,
        }
    )
    registry = seal(
        {
            "schema_version": "awesome-theorems/claim-id-registry/5.4",
            "artifact": "Claim_ID_Registry.json",
            "release": RELEASE,
            "parent_registry_authority_sha256": parent_registry["authority_sha256"],
            "baseline_registry_authority_sha256": parent_registry["baseline_registry_authority_sha256"],
            "authoritative_inputs": copy.deepcopy(inputs),
            "allocation_policy": allocation_policy,
            "namespace_high_watermarks": {"ATF": LAST_ATF, "ATO": LAST_ATV, "ATS": LAST_ATV, "ATV": LAST_ATV},
            "families": copy.deepcopy(parent_registry["families"]) + families,
            "senses": copy.deepcopy(parent_registry["senses"]) + senses,
            "variants": copy.deepcopy(parent_registry["variants"]) + variants,
            "legacy_aliases": copy.deepcopy(parent_registry["legacy_aliases"]),
            "redirects": copy.deepcopy(parent_registry["redirects"]),
            "splits": copy.deepcopy(parent_registry["splits"]),
            "family_membership_extensions": copy.deepcopy(parent_registry["family_membership_extensions"]),
            "counts": {
                "families": len(parent_registry["families"]) + len(families),
                "senses": len(parent_registry["senses"]) + len(senses),
                "variants": len(parent_registry["variants"]) + len(variants),
                "stage4_variants": parent_registry["counts"]["stage4_variants"],
                "stage5_additions": parent_registry["counts"]["stage5_additions"] + len(new_rows),
                "legacy_aliases": len(parent_registry["legacy_aliases"]),
                "redirects": len(parent_registry["redirects"]),
                "splits": len(parent_registry["splits"]),
            },
        }
    )

    parent_stage = parent["Stage5_Claim_ID_Registry.json"]
    new_mappings = [
        {
            "ordinal": int(ATV_RE.fullmatch(row["variant_id"]).group(1)),
            "variant_id": row["variant_id"],
            "predecessor_stage_claim_id": None,
            "stage_claim_id": row["stage_claim_id"],
            "lifecycle": "current",
        }
        for row in new_rows
    ]
    mappings = copy.deepcopy(parent_stage["mappings"]) + new_mappings
    stage_registry = seal(
        {
            "schema_version": "awesome-theorems/stage5-claim-id-registry/5.4",
            "artifact": "Stage5_Claim_ID_Registry.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "numbering_policy": parent_stage["numbering_policy"],
            "counts": {"mappings": len(mappings)},
            "mappings": mappings,
        }
    )

    parent_migration = parent["Migration_v4_to_v5.json"]
    new_migrations = [
        {
            "ordinal": int(ATV_RE.fullmatch(row["variant_id"]).group(1)),
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
        for row in new_rows
    ]
    migrations = copy.deepcopy(parent_migration["migrations"]) + new_migrations
    migration = seal(
        {
            "schema_version": "awesome-theorems/migration-v4-to-v5/5.4",
            "artifact": "Migration_v4_to_v5.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "v4_import_receipt": copy.deepcopy(parent_migration["v4_import_receipt"]),
            "counts": {
                "historical_bindings": parent_migration["counts"]["historical_bindings"],
                "new_allocations": parent_migration["counts"]["new_allocations"] + len(new_rows),
                "migrations": len(migrations),
            },
            "migrations": migrations,
        }
    )

    theorem_rows = [row for row in records if theorem_predicate(row)]
    open_rows = [row for row in records if open_predicate(row)]
    theorem = seal(
        {
            "schema_version": "awesome-theorems/stage5-query-projection/5.4",
            "artifact": "Theorem_List.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
            "stage_claim_ids": [row["stage_claim_id"] for row in theorem_rows],
            "counts": {"records": len(theorem_rows)},
            "records": theorem_rows,
        }
    )
    open_list = seal(
        {
            "schema_version": "awesome-theorems/stage5-query-projection/5.4",
            "artifact": "Open_Claim_List.json",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "query": "pure predicate over Claim_Catalog.json; records copied byte-semantically",
            "stage_claim_ids": [row["stage_claim_id"] for row in open_rows],
            "counts": {"records": len(open_rows)},
            "records": open_rows,
        }
    )

    parent_coverage = parent["Coverage_Ledger.json"]
    parent_candidates_by_source = {
        row["source_record_id"]: row
        for row in parent_coverage["candidate_dispositions"]
        if row.get("source_id") == SOURCE_ID
        and isinstance(row.get("source_record_id"), str)
        and row.get("disposition") == "eligible_not_selected"
    }
    if len(parent_candidates_by_source) != 731:
        raise GenerationError("5.3 coverage lacks the exact 731-row residual state")
    coverage_additions: list[dict[str, Any]] = []
    for row in curation["candidate_dispositions"]:
        parent_candidate = parent_candidates_by_source.get(row["source_record_id"])
        if parent_candidate is None:
            raise GenerationError("5.4 coverage row lacks its 5.3 residual predecessor")
        coverage_additions.append(
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
                "canonical_source_record_id": None,
                "duplicate_of_semantic_key": None,
                "duplicate_of_variant_id": None,
                "grants_catalog_entry": row["grants_catalog_entry"],
                "grants_theorem_credit": row["grants_theorem_credit"],
                "origin_release": RELEASE,
                "curation_row_sha256": row["row_sha256"],
                "parent_curation_row_sha256": row["parent_curation_row_sha256"],
                "supersedes_candidate_key": parent_candidate["candidate_key"],
                "transition_from_disposition": parent_candidate["disposition"],
            }
        )
    candidates = copy.deepcopy(parent_coverage["candidate_dispositions"]) + coverage_additions
    by_code: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in new_rows:
        by_code[str(row["classification"]["msc2020_code"])].append(row)
    msc_rows: list[dict[str, Any]] = []
    for parent_row in parent_coverage["msc_coverage"]:
        row = copy.deepcopy(parent_row)
        code = str(row["msc_top_class"])
        additions = by_code.pop(code, [])
        new_ids = sorted(item["stage_claim_id"] for item in additions)
        row["current_theorem_s5_ids"] = sorted([*row["current_theorem_s5_ids"], *new_ids])
        row["origin_theorem_s5_ids"] = new_ids
        row["origin_open_s5_ids"] = []
        if additions:
            row["source_ids"] = sorted(set(row["source_ids"]) | {SOURCE_ID})
        exact = sum(item["classification"]["basis"] == "1000_plus_curated" for item in additions)
        row["classification_basis_counts"]["source_annotation"] += exact
        row["classification_basis_counts"]["machine_crosswalk"] += len(additions) - exact
        row["counts"]["current_theorems"] = len(row["current_theorem_s5_ids"])
        row["counts"]["current_open"] = len(row["current_open_s5_ids"])
        row["counts"]["origin_theorems"] = len(new_ids)
        row["counts"]["origin_open"] = 0
        row["counts"]["open_reserve"] = len(row["open_reserve_candidate_keys"])
        classified = row["counts"]["current_theorems"] + row["counts"]["current_open"] + row["counts"]["open_reserve"]
        if classified == 0:
            row["scarcity"] = "zero"
            row["scarcity_reason"] = "No current or open-reserve member has this primary source annotation."
        elif classified < 10:
            row["scarcity"] = "thin"
            row["scarcity_reason"] = "Fewer than ten current-plus-reserve members have this primary class."
        else:
            row["scarcity"] = "adequate_in_source_inventory"
            row["scarcity_reason"] = "At least ten current-plus-reserve members have this primary class."
        msc_rows.append(row)
    if by_code:
        raise GenerationError(f"new rows use unknown MSC roots: {sorted(by_code)}")
    dispositions = Counter(row["disposition"] for row in coverage_additions)
    coverage = seal(
        {
            "schema_version": "awesome-theorems/stage5-coverage-ledger/5.4",
            "release": RELEASE,
            "authoritative_inputs": copy.deepcopy(inputs),
            "effective_state_policy": {
                "identity_fields": ["source_id", "source_record_id"],
                "supersession_field": "supersedes_candidate_key",
                "effective_rule": "A candidate row is effective exactly when no later appended row names its candidate_key in supersedes_candidate_key.",
                "historical_parent_rows_are_immutable": True,
                "release_5_4_rows_supersede_exact_5_3_residual_rows": True,
            },
            "candidate_dispositions": candidates,
            "msc_coverage": msc_rows,
            "counts": {
                "candidate_dispositions": len(candidates),
                "msc_coverage": len(msc_rows),
                "origin_5_4_candidates": len(coverage_additions),
                "origin_5_4_accepted_new_theorems": dispositions["accepted_new_kernel_checked_theorem"],
                "origin_5_4_literal_lemma_noncredit": sum(row["declaration_kind"] == "lemma" for row in coverage_additions),
                "origin_5_4_eligible_not_selected": dispositions["eligible_not_selected_after_5_4"],
            },
        }
    )

    parent_strict = parent["Strict_Conjecture_Ledger.json"]
    strict = seal(
        {
            "schema_version": "awesome-theorems/stage5-strict-conjecture-ledger/5.4",
            "release": RELEASE,
            "parent_release_root_sha256": PARENT_ROOT,
            "parent_strict_ledger_file_sha256": sha256_file(PARENT_DIR / "Strict_Conjecture_Ledger.json"),
            "parent_strict_ledger_authority_sha256": parent_strict["authority_sha256"],
            "strict_credits": copy.deepcopy(parent_strict["strict_credits"]),
            "credit_corrections": copy.deepcopy(parent_strict["credit_corrections"]),
            "counts": copy.deepcopy(parent_strict["counts"]),
            "set_digests": copy.deepcopy(parent_strict["set_digests"]),
        }
    )
    artifacts = {
        "Claim_Catalog.json": catalog,
        "Claim_ID_Registry.json": registry,
        "Stage5_Claim_ID_Registry.json": stage_registry,
        "Migration_v4_to_v5.json": migration,
        "Theorem_List.json": theorem,
        "Open_Claim_List.json": open_list,
        "Coverage_Ledger.json": coverage,
        "Strict_Conjecture_Ledger.json": strict,
    }
    validate_artifacts(artifacts, parent, new_rows, curation)
    return artifacts


def validate_artifacts(
    artifacts: Mapping[str, Mapping[str, Any]], parent: Mapping[str, Mapping[str, Any]], new_rows: Sequence[Mapping[str, Any]], curation: Mapping[str, Any]
) -> None:
    if set(artifacts) != set(RELEASE_FILES):
        raise GenerationError("artifact set drifted")
    for name, document in artifacts.items():
        verify_seal(document, name)
    catalog = artifacts["Claim_Catalog.json"]
    if catalog["records"][:3_600] != parent["Claim_Catalog.json"]["records"] or catalog["records"][3_600:] != list(new_rows):
        raise GenerationError("catalog parent canonical-byte prefix changed")
    recomputed_counts = {
        "records": len(catalog["records"]),
        "origin_theorems": sum(theorem_predicate(row) for row in new_rows),
        "origin_open_claims": sum(open_predicate(row) for row in new_rows),
        "cumulative_theorems": sum(theorem_predicate(row) for row in catalog["records"]),
        "cumulative_open_claims": sum(open_predicate(row) for row in catalog["records"]),
    }
    if catalog["counts"] != recomputed_counts or recomputed_counts != {
        "records": 4_100,
        "origin_theorems": 500,
        "origin_open_claims": 0,
        "cumulative_theorems": 2_500,
        "cumulative_open_claims": 1_600,
    }:
        raise GenerationError(f"catalog counts drifted: {recomputed_counts}")
    theorem = artifacts["Theorem_List.json"]
    open_list = artifacts["Open_Claim_List.json"]
    if theorem["records"][:2_000] != parent["Theorem_List.json"]["records"] or theorem["records"][2_000:] != list(new_rows):
        raise GenerationError("theorem projection parent prefix/suffix drifted")
    if open_list["records"] != parent["Open_Claim_List.json"]["records"]:
        raise GenerationError("open projection changed")
    for artifact_name, key in (
        ("Claim_ID_Registry.json", "families"),
        ("Claim_ID_Registry.json", "senses"),
        ("Claim_ID_Registry.json", "variants"),
        ("Stage5_Claim_ID_Registry.json", "mappings"),
        ("Migration_v4_to_v5.json", "migrations"),
        ("Coverage_Ledger.json", "candidate_dispositions"),
    ):
        child_rows = artifacts[artifact_name][key]
        parent_rows = parent[artifact_name][key]
        if child_rows[: len(parent_rows)] != parent_rows:
            raise GenerationError(f"{artifact_name}.{key} parent prefix changed")
    registry = artifacts["Claim_ID_Registry.json"]
    if registry["namespace_high_watermarks"] != {"ATF": 7_354, "ATO": 7_584, "ATS": 7_584, "ATV": 7_584}:
        raise GenerationError("registry high-watermarks drifted")
    if len({row["variant_id"] for row in catalog["records"]}) != 4_100:
        raise GenerationError("catalog variant IDs are not unique")
    if len({row["stage_claim_id"] for row in catalog["records"]}) != 4_100:
        raise GenerationError("catalog Stage5 IDs are not unique")
    selected = sorted(
        (row for row in curation["candidate_dispositions"] if row["grants_theorem_credit"]),
        key=lambda row: row["accepted_rank"],
    )
    if [row["curator_disposition"]["source_record_id"] for row in new_rows] != [row["source_record_id"] for row in selected]:
        raise GenerationError("catalog additions differ from curation accepted set")
    if any(row["formal_statement"]["source_syntax_kind"] != "theorem" for row in new_rows):
        raise GenerationError("literal lemma received theorem credit")
    coverage_rows = artifacts["Coverage_Ledger.json"]["candidate_dispositions"]
    candidate_keys = [row.get("candidate_key") for row in coverage_rows]
    if not all(isinstance(key, str) and key for key in candidate_keys) or len(
        candidate_keys
    ) != len(set(candidate_keys)):
        raise GenerationError("coverage candidate_key values are not globally unique")
    parent_coverage_rows = parent["Coverage_Ledger.json"]["candidate_dispositions"]
    parent_by_key = {row["candidate_key"]: row for row in parent_coverage_rows}
    superseded_keys: set[str] = set()
    for row, curation_row in zip(
        coverage_rows[len(parent_coverage_rows) :], curation["candidate_dispositions"]
    ):
        predecessor = parent_by_key.get(row.get("supersedes_candidate_key"))
        if (
            predecessor is None
            or predecessor.get("source_id") != SOURCE_ID
            or predecessor.get("source_record_id") != row.get("source_record_id")
            or predecessor.get("disposition") != "eligible_not_selected"
            or row.get("transition_from_disposition") != "eligible_not_selected"
            or row.get("parent_curation_row_sha256")
            != curation_row.get("parent_curation_row_sha256")
        ):
            raise GenerationError("coverage supersession/effective-state linkage drifted")
        superseded_keys.add(str(row["supersedes_candidate_key"]))
    if len(superseded_keys) != 731:
        raise GenerationError("coverage does not supersede exactly 731 distinct parent states")
    strict = artifacts["Strict_Conjecture_Ledger.json"]
    parent_strict = parent["Strict_Conjecture_Ledger.json"]
    for field in ("strict_credits", "credit_corrections", "counts", "set_digests"):
        if strict[field] != parent_strict[field]:
            raise GenerationError(f"strict-conjecture {field} changed")


def package_release(
    artifacts: Mapping[str, Mapping[str, Any]], inputs: Mapping[str, Any], curation: Mapping[str, Any]
) -> tuple[dict[str, bytes], str, dict[str, Any]]:
    package = {name: encoded_document(artifacts[name]) for name in RELEASE_FILES}
    inventory = [
        {
            "path": name,
            "sha256": sha256_bytes(package[name]),
            "size_bytes": len(package[name]),
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
            "schema_version": "awesome-theorems/stage5-release-manifest/5.4",
            "release": RELEASE,
            "parent_release": PARENT_RELEASE,
            "parent_release_root_sha256": PARENT_ROOT,
            "release_root_sha256": root,
            "authoritative_inputs": copy.deepcopy(inputs),
            "accepted_set_digests": {
                "source_record_id_set_sha256": digests["selected_source_record_id_set_sha256"],
                "declaration_set_sha256": digests["selected_declaration_set_sha256"],
                "formal_type_sha256_set_sha256": digests["selected_formal_type_sha256_set_sha256"],
                "semantic_key_set_sha256": digests["selected_semantic_key_set_sha256"],
                "variant_id_set_sha256": digests["selected_variant_id_set_sha256"],
                "s5_id_set_sha256": digests["selected_s5_id_set_sha256"],
            },
            "strict_credit_binding": {
                "path": "Strict_Conjecture_Ledger.json",
                "file_sha256": sha256_bytes(package["Strict_Conjecture_Ledger.json"]),
                "authority_sha256": strict["authority_sha256"],
                "effective_s5_id_set_sha256": strict["set_digests"]["effective_s5_id_set_sha256"],
                "effective_variant_id_set_sha256": strict["set_digests"]["effective_variant_id_set_sha256"],
            },
            "artifacts": inventory,
            "counts": {
                "non_manifest_artifacts": len(inventory),
                "catalog_records": catalog_counts["records"],
                "origin_theorems": catalog_counts["origin_theorems"],
                "origin_open_claims": catalog_counts["origin_open_claims"],
                "cumulative_theorems": catalog_counts["cumulative_theorems"],
                "cumulative_open_claims": catalog_counts["cumulative_open_claims"],
                "effective_strict_conjecture_credits": strict["counts"]["effective_strict_credits"],
            },
        }
    )
    package[MANIFEST_NAME] = encoded_document(manifest)
    return package, root, manifest


def expected_current(root: str, manifest_payload: bytes, manifest: Mapping[str, Any]) -> dict[str, Any]:
    return seal(
        {
            "schema_version": "awesome-theorems/stage5-current-release/5.4",
            "release": RELEASE,
            "manifest_path": "releases/5.4/Release_Manifest.json",
            "manifest_sha256": sha256_bytes(manifest_payload),
            "release_root_sha256": root,
        }
    )


def compare_package(package: Mapping[str, bytes]) -> None:
    observed_files = {path.name for path in RELEASE_DIR.iterdir() if path.is_file()} if RELEASE_DIR.is_dir() else set()
    if observed_files != set(package):
        raise GenerationError(f"release 5.4 file set differs: {observed_files}")
    for name, payload in package.items():
        path = RELEASE_DIR / name
        if path.read_bytes() != payload:
            raise GenerationError(f"release artifact is stale: {path}")


def fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


@contextmanager
def exclusive_writer_lock() -> Iterator[None]:
    V5_ROOT.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(LOCK_PATH, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def publish_directory(target: Path, payloads: Mapping[str, bytes]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if not any(target.iterdir()):
            target.rmdir()
        else:
            observed = {path.name for path in target.iterdir() if path.is_file()}
            if observed != set(payloads) or any((target / name).read_bytes() != payload for name, payload in payloads.items()):
                raise GenerationError(f"refusing to rewrite unequal immutable directory: {target}")
            return
    temporary = Path(tempfile.mkdtemp(prefix=f".{target.name}.tmp-", dir=target.parent))
    try:
        for name, payload in sorted(payloads.items()):
            path = temporary / name
            with path.open("xb") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
        fsync_directory(temporary)
        try:
            os.rename(temporary, target)
        except OSError:
            if target.exists():
                observed = {path.name for path in target.iterdir() if path.is_file()}
                if observed != set(payloads) or any((target / name).read_bytes() != payload for name, payload in payloads.items()):
                    raise GenerationError(f"concurrent unequal immutable publish: {target}")
                shutil.rmtree(temporary)
            else:
                raise
        fsync_directory(target.parent)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


def authenticated_parent_pointer() -> dict[str, Any]:
    return {
        "authority_sha256": "c0b48bd538a3109e7695a96fb3ffc16b5a3047ab41e13b5e8d3ccfae2ec785bf",
        "manifest_path": "releases/5.3/Release_Manifest.json",
        "manifest_sha256": PARENT_MANIFEST_SHA256,
        "release": PARENT_RELEASE,
        "release_root_sha256": PARENT_ROOT,
        "schema_version": "awesome-theorems/stage5-current-release/5.3",
    }


def verify_current_cas(package: Mapping[str, bytes], root: str, target: Mapping[str, Any]) -> str:
    pointer = load_json(CURRENT_PATH)
    verify_seal(pointer, str(CURRENT_PATH))
    release = pointer.get("release")
    if release == RELEASE:
        if pointer != target:
            raise GenerationError("Current_Release 5.4 differs from generated target pointer")
        compare_package(package)
        return "already_current"
    if pointer != authenticated_parent_pointer():
        raise GenerationError("Current_Release is not the exact authenticated 5.3 CAS parent")
    parent_manifest = PARENT_DIR / MANIFEST_NAME
    parent_registry = PARENT_DIR / "Claim_ID_Registry.json"
    if sha256_file(parent_manifest) != PARENT_MANIFEST_SHA256:
        raise GenerationError("CAS parent manifest bytes drifted")
    manifest = load_json(parent_manifest)
    registry = load_json(parent_registry)
    verify_seal(manifest, str(parent_manifest))
    verify_seal(registry, str(parent_registry))
    if manifest.get("release_root_sha256") != PARENT_ROOT:
        raise GenerationError("CAS parent release root drifted")
    canonical_registry = load_json(V5_ROOT / "releases/5.3/Claim_ID_Registry.json")
    if registry.get("authority_sha256") != canonical_registry.get("authority_sha256"):
        raise GenerationError("CAS parent registry authority drifted")
    return "parent_current"


def publish(package: Mapping[str, bytes]) -> None:
    publish_directory(RELEASE_DIR, package)
    compare_package(package)


def validate_readable_projection() -> None:
    command = [
        os.sys.executable,
        str(REPO_ROOT / "Docs/tools/render_math_catalog_v5.py"),
        "--release",
        RELEASE,
        "--check",
    ]
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stdout.strip()
        raise GenerationError(f"detailed readable 5.4 acceptance failed: {detail}")


def publish_current(package: Mapping[str, bytes], current: Mapping[str, Any], root: str) -> None:
    state = verify_current_cas(package, root, current)
    if state == "already_current":
        return
    compare_package(package)
    validate_readable_projection()
    atomic_write(CURRENT_PATH, encoded_document(current))


def build_all() -> tuple[
    dict[Path, dict[str, Any]], dict[str, bytes], dict[str, Any], str, dict[str, Any]
]:
    authorities = expected_authorities()
    parent = load_parent()
    curation = load_json(CURATION_PATH)
    verify_seal(curation, str(CURATION_PATH))
    new_rows = build_new_records(parent, curation, authorities[SCHEMA_PATH])
    inputs = authoritative_inputs(authorities, curation, parent)
    artifacts = build_artifacts(parent, new_rows, inputs, curation)
    package, root, manifest = package_release(artifacts, inputs, curation)
    current = expected_current(root, package[MANIFEST_NAME], manifest)
    return authorities, package, current, root, {
        "catalog": len(artifacts["Claim_Catalog.json"]["records"]),
        "theorems": len(artifacts["Theorem_List.json"]["records"]),
        "open": len(artifacts["Open_Claim_List.json"]["records"]),
        "strict": len(artifacts["Strict_Conjecture_Ledger.json"]["strict_credits"]),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--publish-current",
        action="store_true",
        help="after independent prepublish acceptance, CAS Current_Release from 5.3 to 5.4",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.check and args.publish_current:
            raise GenerationError("--check and --publish-current are mutually exclusive")
        with exclusive_writer_lock():
            authorities, package, current, root, counts = build_all()
            materialize_authorities(authorities, check=args.check or args.publish_current)
            if args.check:
                compare_package(package)
                verify_current_cas(package, root, current)
            elif args.publish_current:
                compare_package(package)
                publish_current(package, current, root)
            else:
                require_parent = verify_current_cas(package, root, current)
                if require_parent == "already_current":
                    compare_package(package)
                else:
                    publish(package)
        if args.check:
            print(
                f"PASS release 5.4 deterministic check: root={root} "
                f"catalog={counts['catalog']} theorem={counts['theorems']} "
                f"open={counts['open']} strict={counts['strict']}"
            )
        elif args.publish_current:
            print(f"PUBLISHED Current_Release 5.4: root={root}")
        else:
            print(
                f"STAGED release 5.4 (Current remains 5.3): root={root} catalog={counts['catalog']} "
                f"theorem={counts['theorems']} open={counts['open']} strict={counts['strict']}"
            )
        return 0
    except (GenerationError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"ERROR: {error}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
