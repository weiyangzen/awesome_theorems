#!/usr/bin/env python3
"""Build the sealed mathlib theorem curation authority for Stage5 v5.3.

The source authority contains 1,500 kernel-checked declarations, including
1,235 literal ``theorem`` declarations and 265 literal ``lemma`` declarations.
Release 5.3 admits only the former.  It removes exact or whitespace-normalized
formal-type duplicates and normalized declaration-name duplicates, including
matches against parent 5.2.  It then accepts every deduplicated docs/1000 row
in selection-rank/source-ID order and fills the remaining places with repeated
bytewise module-root sweeps whose buckets use the same row order.

Every source row receives one disposition.  ``--check`` performs a read-only
byte comparison; a normal build atomically replaces the sealed JSON authority.
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
import unicodedata
from typing import Any, Iterable, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_ROOT = REPO_ROOT / "Docs/catalog/v5"
SOURCE_PATH = CATALOG_ROOT / "sources/mathlib-theorems-8a178386.json"
SOURCE_REGISTRY_PATH = CATALOG_ROOT / "Math_Source_Registry_v5_3.json"
PARENT_RECEIPT_PATH = CATALOG_ROOT / "V5_2_Parent_Receipt_v5_3.json"
PARENT_MANIFEST_PATH = CATALOG_ROOT / "releases/5.2/Release_Manifest.json"
PARENT_CATALOG_PATH = CATALOG_ROOT / "releases/5.2/Claim_Catalog.json"
OUTPUT_PATH = CATALOG_ROOT / "curation/Mathlib_Theorem_Curation_v5_3.json"

SCHEMA_VERSION = "awesome-theorems/mathlib-theorem-curation/5.3"
SOURCE_SCHEMA_VERSION = "awesome-theorems/mathlib-theorem-source/1.0"
SOURCE_ID = "SRC-MATH-V5-MATHLIB-8A178386"
RELEASE = "5.3"
PARENT_RELEASE = "5.2"

SOURCE_FILE_SHA256 = "236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a"
SOURCE_SIZE_BYTES = 6_316_287
SOURCE_CONTENT_DIGEST = "dd49c8322d8eded995c84a235fd458fc093a187230323f87bea78049ae90e53b"
SOURCE_COMMIT = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
SOURCE_ROWS = 1_500
SOURCE_LITERAL_THEOREMS = 1_235
SOURCE_LITERAL_LEMMAS = 265

PARENT_RELEASE_ROOT_SHA256 = "edee3a3e5f29a345a16fb526654aecfeaeaaf62da0e0101ed5e9bd2cbb374e2e"
PARENT_MANIFEST_FILE_SHA256 = "7e592793402c09f8f1e63871ea1cc19569c049652eeabfb453df7cf7eb2d2bab"
PARENT_MANIFEST_AUTHORITY_SHA256 = "1a4a2270b32b616e04cc62697b60c5de083e343c5ebe0cc4b6849141015388bc"
PARENT_CATALOG_FILE_SHA256 = "cb40df5487b1dd14abea62e625d9c9dca840b2b78292efe2a7dcfbbba3f27f82"
PARENT_CATALOG_AUTHORITY_SHA256 = "76a1d44720c8265d52271d9e600fa586ac99cbf57deb54589809b47658a87300"
PARENT_CATALOG_ROWS = 3_100
PARENT_ATV_HIGH_WATERMARK = 6_584

SELECTED_ROWS = 500
FIRST_NEW_ORDINAL = PARENT_ATV_HIGH_WATERMARK + 1
LAST_NEW_ORDINAL = PARENT_ATV_HIGH_WATERMARK + SELECTED_ROWS

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")
SOURCE_RECORD_ID_RE = re.compile(r"^ML4-[0-9A-F]{20}$")

DOCS_SIGNAL = "mathlib_1000_theorems"
MODULE_MAIN_SIGNAL = "mathlib_module_main_result"
ALLOWED_SIGNAL_KINDS = {DOCS_SIGNAL, MODULE_MAIN_SIGNAL}

SOURCE_ROW_FIELDS = {
    "declaration",
    "declaration_docstring",
    "declaration_kind",
    "display_label",
    "exact_curated_summary",
    "formal_docstring",
    "formal_docstring_origin",
    "formal_docstring_sha256",
    "formal_proof_state",
    "formal_type",
    "formal_type_sha256",
    "importance_signals",
    "material_status",
    "msc2020",
    "proof_evidence",
    "raw_category",
    "raw_status",
    "rights",
    "selection_cohort",
    "selection_rank",
    "source",
    "source_record_id",
    "source_syntax_kind",
}

CANDIDATE_FIELDS = {
    "candidate_key",
    "source_index",
    "source_record_id",
    "source_record_sha256",
    "declaration",
    "declaration_kind",
    "source_syntax_kind",
    "selection_rank",
    "selection_cohort",
    "formal_proof_state",
    "formal_type_sha256",
    "formal_docstring_sha256",
    "proof_evidence_payload_sha256",
    "importance_payload_sha256",
    "rights_payload_sha256",
    "semantic_key",
    "semantic_key_method",
    "semantic_key_payload_sha256",
    "disposition",
    "reason_code",
    "accepted_rank",
    "target_variant_id",
    "target_s5_id",
    "canonical_source_record_id",
    "duplicate_of_semantic_key",
    "duplicate_of_variant_id",
    "dedupe_rationale",
    "dedupe_confidence",
    "dedupe_reviewer",
    "grants_catalog_entry",
    "grants_theorem_credit",
    "row_sha256",
}

DISPOSITIONS = {
    "accepted_new_kernel_checked_theorem",
    "rejected_nonliteral_lemma",
    "rejected_proof_boundary",
    "rejected_source_semantic_duplicate",
    "rejected_source_name_duplicate",
    "rejected_parent_duplicate",
    "eligible_not_selected",
}


class CurationError(RuntimeError):
    """A source, parent, selection, or seal invariant failed closed."""


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
        raise CurationError(f"value is not canonical-JSON serializable: {error}") from error


def source_pretty_json_bytes(value: Any) -> bytes:
    """Reproduce the v1 mathlib extractor's self-digest encoding."""

    try:
        return (
            json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise CurationError(f"source value is not JSON serializable: {error}") from error


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


def strict_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise CurationError(f"invalid JSON in {label}: {error}") from error
    if not isinstance(value, dict):
        raise CurationError(f"{label} must contain one JSON object")
    return value


def load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise CurationError(f"cannot read {path}: {error}") from error
    return strict_json_bytes(payload, str(path)), payload


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


def verify_seal(document: Mapping[str, Any], label: str) -> str:
    observed = document.get("authority_sha256")
    if not isinstance(observed, str) or SHA256_RE.fullmatch(observed) is None:
        raise CurationError(f"{label} has no valid authority_sha256")
    expected = artifact_authority(document)
    if observed != expected:
        raise CurationError(f"{label} has a stale authority_sha256")
    return observed


def normalize_declaration_name(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().strip()


def declaration_name_key_sha256(value: str) -> str:
    return sha256_bytes(normalize_declaration_name(value).encode("utf-8"))


def normalized_formal_type(value: str) -> str:
    return " ".join(value.split())


def normalized_formal_type_sha256(value: str) -> str:
    return sha256_bytes(normalized_formal_type(value).encode("utf-8"))


def semantic_key(row: Mapping[str, Any]) -> str:
    return "mathlib-theorem-semantic/" + str(row["formal_type_sha256"])


def importance_signal_kinds(row: Mapping[str, Any]) -> tuple[str, ...]:
    signals = row.get("importance_signals")
    if not isinstance(signals, list) or not signals:
        raise CurationError(
            f"source row {row.get('source_record_id')!r} lacks importance signals"
        )
    kinds: set[str] = set()
    for index, signal in enumerate(signals):
        if not isinstance(signal, dict):
            raise CurationError(f"importance_signals[{index}] is not an object")
        kind = _require_string(signal.get("kind"), f"importance_signals[{index}].kind")
        if kind not in ALLOWED_SIGNAL_KINDS:
            raise CurationError(f"unsupported importance signal kind {kind!r}")
        kinds.add(kind)
    return tuple(sorted(kinds))


def importance_tier(row: Mapping[str, Any]) -> str:
    kinds = set(importance_signal_kinds(row))
    if kinds == {DOCS_SIGNAL, MODULE_MAIN_SIGNAL}:
        return "docs_1000_and_module_main"
    if DOCS_SIGNAL in kinds:
        return "docs_1000"
    if MODULE_MAIN_SIGNAL in kinds:
        return "module_main_result"
    raise CurationError("source row has no recognized importance tier")


def duplicate_winner_rank(row: Mapping[str, Any]) -> tuple[int, int, str]:
    """The source-registry order for an exact formal-type component."""

    return (
        0 if DOCS_SIGNAL in importance_signal_kinds(row) else 1,
        _require_positive_int(row.get("selection_rank"), "selection_rank"),
        str(row["source_record_id"]),
    )


def module_root(row: Mapping[str, Any]) -> str:
    source = _require_object(row.get("source"), "source row source")
    module = _require_string(source.get("module"), "source.module")
    pieces = module.split(".")
    if len(pieces) < 2 or pieces[0] != "Mathlib" or not pieces[1]:
        raise CurationError(f"invalid mathlib module {module!r}")
    return pieces[1]


def validate_truth_gate(row: Mapping[str, Any], label: str) -> None:
    formal_type = _require_string(row.get("formal_type"), f"{label}.formal_type")
    formal_sha = _require_string(
        row.get("formal_type_sha256"), f"{label}.formal_type_sha256"
    )
    if SHA256_RE.fullmatch(formal_sha) is None:
        raise CurationError(f"{label}.formal_type_sha256 is invalid")
    if sha256_bytes(formal_type.encode("utf-8")) != formal_sha:
        raise CurationError(f"{label}.formal_type_sha256 does not bind formal_type")
    if row.get("formal_proof_state") != "kernel_checked_sorry_free":
        raise CurationError(f"{label} is not kernel_checked_sorry_free")
    proof = _require_object(row.get("proof_evidence"), f"{label}.proof_evidence")
    if proof.get("uses_sorry") is not False:
        raise CurationError(f"{label} proof evidence permits sorry")
    if proof.get("verification") != (
        "lean_checked_environment_thmInfo_and_collectAxioms_without_sorryAx"
    ):
        raise CurationError(f"{label} has an unexpected proof verification mode")
    axioms = proof.get("batch_axiom_dependency_union")
    if not isinstance(axioms, list) or "sorryAx" in axioms:
        raise CurationError(f"{label} has invalid axiom dependency evidence")
    status = _require_object(row.get("material_status"), f"{label}.material_status")
    if status.get("status") != "proved_formal" or status.get("as_of_commit") != SOURCE_COMMIT:
        raise CurationError(f"{label} material status is not pinned proved_formal")
    if row.get("raw_status") != "lean_checked_thmInfo_sorry_free":
        raise CurationError(f"{label}.raw_status drifted")


def load_source(path: Path = SOURCE_PATH) -> tuple[dict[str, Any], list[dict[str, Any]], bytes]:
    source, payload = load_json(path)
    if len(payload) != SOURCE_SIZE_BYTES:
        raise CurationError(
            f"mathlib source size is {len(payload)}, expected {SOURCE_SIZE_BYTES}"
        )
    observed_file_sha = sha256_bytes(payload)
    if observed_file_sha != SOURCE_FILE_SHA256:
        raise CurationError(
            f"mathlib source SHA-256 is {observed_file_sha}, expected {SOURCE_FILE_SHA256}"
        )
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise CurationError("mathlib source schema_version drifted")
    declared_content_digest = source.get("content_digest_before_self_field")
    body = dict(source)
    body.pop("content_digest_before_self_field", None)
    rebuilt_content_digest = sha256_bytes(source_pretty_json_bytes(body))
    if (
        declared_content_digest != SOURCE_CONTENT_DIGEST
        or rebuilt_content_digest != SOURCE_CONTENT_DIGEST
    ):
        raise CurationError("mathlib source self-digest drifted")
    snapshot = _require_object(source.get("source_snapshot"), "source.source_snapshot")
    if snapshot.get("commit") != SOURCE_COMMIT:
        raise CurationError("mathlib source commit drifted")
    if snapshot.get("license") != "Apache-2.0":
        raise CurationError("mathlib source license drifted")
    rows = _require_rows(source.get("records"), "source.records")
    if len(rows) != SOURCE_ROWS:
        raise CurationError(f"mathlib source has {len(rows)} rows, expected {SOURCE_ROWS}")
    seen_ids: set[str] = set()
    seen_ranks: set[int] = set()
    seen_declarations: set[str] = set()
    kinds: Counter[str] = Counter()
    for index, row in enumerate(rows):
        label = f"source.records[{index}]"
        if set(row) != SOURCE_ROW_FIELDS:
            raise CurationError(f"{label} field closure drifted")
        source_record_id = _require_string(row.get("source_record_id"), f"{label}.source_record_id")
        if SOURCE_RECORD_ID_RE.fullmatch(source_record_id) is None:
            raise CurationError(f"{label}.source_record_id is invalid")
        if source_record_id in seen_ids:
            raise CurationError(f"source duplicates source_record_id {source_record_id}")
        seen_ids.add(source_record_id)
        selection_rank = _require_positive_int(row.get("selection_rank"), f"{label}.selection_rank")
        if selection_rank in seen_ranks:
            raise CurationError(f"source duplicates selection_rank {selection_rank}")
        seen_ranks.add(selection_rank)
        declaration = _require_string(row.get("declaration"), f"{label}.declaration")
        normalized_name = normalize_declaration_name(declaration)
        if normalized_name in seen_declarations:
            raise CurationError(f"source duplicates normalized declaration name {declaration!r}")
        seen_declarations.add(normalized_name)
        declaration_kind = row.get("declaration_kind")
        if declaration_kind not in {"theorem", "lemma"}:
            raise CurationError(f"{label}.declaration_kind is not theorem/lemma")
        if (
            row.get("source_syntax_kind") != declaration_kind
            or row.get("raw_category") != declaration_kind
        ):
            raise CurationError(f"{label} literal declaration kind fields disagree")
        validate_truth_gate(row, label)
        importance_signal_kinds(row)
        module_root(row)
        rights = _require_object(row.get("rights"), f"{label}.rights")
        if rights.get("source_license") != "Apache-2.0":
            raise CurationError(f"{label} rights license drifted")
        kinds[str(declaration_kind)] += 1
    if seen_ranks != set(range(1, SOURCE_ROWS + 1)):
        raise CurationError("source selection ranks are not exactly 1..1500")
    if kinds != Counter({"theorem": SOURCE_LITERAL_THEOREMS, "lemma": SOURCE_LITERAL_LEMMAS}):
        raise CurationError(f"source literal declaration counts drifted: {dict(kinds)}")
    counts = _require_object(source.get("counts"), "source.counts")
    if counts.get("selected_total") != SOURCE_ROWS:
        raise CurationError("source declared selected_total drifted")
    return source, rows, payload


def load_parent(
    manifest_path: Path = PARENT_MANIFEST_PATH,
    catalog_path: Path = PARENT_CATALOG_PATH,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], bytes, bytes]:
    manifest, manifest_payload = load_json(manifest_path)
    catalog, catalog_payload = load_json(catalog_path)
    if sha256_bytes(manifest_payload) != PARENT_MANIFEST_FILE_SHA256:
        raise CurationError("parent 5.2 manifest file SHA-256 drifted")
    if sha256_bytes(catalog_payload) != PARENT_CATALOG_FILE_SHA256:
        raise CurationError("parent 5.2 catalog file SHA-256 drifted")
    if verify_seal(manifest, str(manifest_path)) != PARENT_MANIFEST_AUTHORITY_SHA256:
        raise CurationError("parent 5.2 manifest authority drifted")
    if verify_seal(catalog, str(catalog_path)) != PARENT_CATALOG_AUTHORITY_SHA256:
        raise CurationError("parent 5.2 catalog authority drifted")
    if (
        manifest.get("release") != PARENT_RELEASE
        or manifest.get("release_root_sha256") != PARENT_RELEASE_ROOT_SHA256
    ):
        raise CurationError("parent 5.2 release identity drifted")
    if catalog.get("release") != PARENT_RELEASE:
        raise CurationError("parent Claim_Catalog release drifted")
    manifest_catalog = [
        row
        for row in _require_rows(manifest.get("artifacts"), "parent_manifest.artifacts")
        if row.get("path") == "Claim_Catalog.json"
    ]
    if len(manifest_catalog) != 1:
        raise CurationError("parent manifest has no unique Claim_Catalog binding")
    if (
        manifest_catalog[0].get("sha256") != PARENT_CATALOG_FILE_SHA256
        or manifest_catalog[0].get("size_bytes") != len(catalog_payload)
    ):
        raise CurationError("parent manifest/catalog byte binding drifted")
    records = _require_rows(catalog.get("records"), "parent_catalog.records")
    if len(records) != PARENT_CATALOG_ROWS:
        raise CurationError("parent catalog row count drifted")
    seen_variants: set[str] = set()
    maximum_ordinal = 0
    for index, row in enumerate(records):
        variant_id = _require_string(row.get("variant_id"), f"parent.records[{index}].variant_id")
        match = ATV_RE.fullmatch(variant_id)
        if match is None or variant_id in seen_variants:
            raise CurationError(f"parent has invalid/duplicate variant id {variant_id!r}")
        seen_variants.add(variant_id)
        maximum_ordinal = max(maximum_ordinal, int(match.group(1)))
    if maximum_ordinal != PARENT_ATV_HIGH_WATERMARK:
        raise CurationError("parent catalog ATV high-watermark drifted")
    return manifest, catalog, records, manifest_payload, catalog_payload


def load_versioned_bindings(
    source_registry_path: Path = SOURCE_REGISTRY_PATH,
    parent_receipt_path: Path = PARENT_RECEIPT_PATH,
) -> tuple[dict[str, Any], dict[str, Any], str, str]:
    registry, _registry_payload = load_json(source_registry_path)
    receipt, _receipt_payload = load_json(parent_receipt_path)
    registry_authority = verify_seal(registry, str(source_registry_path))
    receipt_authority = verify_seal(receipt, str(parent_receipt_path))
    if registry.get("schema_version") != "awesome-theorems/stage5-math-source-registry/5.3":
        raise CurationError("v5.3 source-registry schema drifted")
    sources = _require_rows(registry.get("sources"), "source_registry.sources")
    matches = [row for row in sources if row.get("source_id") == SOURCE_ID]
    if len(matches) != 1:
        raise CurationError(f"source registry must contain one {SOURCE_ID} row")
    source = matches[0]
    asset = _require_object(source.get("asset"), "source_registry.source.asset")
    expected_asset = {
        "path": "Docs/catalog/v5/sources/mathlib-theorems-8a178386.json",
        "sha256": SOURCE_FILE_SHA256,
        "size_bytes": SOURCE_SIZE_BYTES,
        "record_count": SOURCE_ROWS,
        "schema_version": SOURCE_SCHEMA_VERSION,
        "content_digest_before_self_field": SOURCE_CONTENT_DIGEST,
    }
    for field, expected in expected_asset.items():
        if asset.get(field) != expected:
            raise CurationError(f"source registry asset.{field} drifted")
    facts = _require_object(source.get("content_facts"), "source_registry.source.content_facts")
    expected_facts = {
        "literal_theorem_records": SOURCE_LITERAL_THEOREMS,
        "literal_lemma_records": SOURCE_LITERAL_LEMMAS,
        "unique_literal_theorem_formal_type_sha256": 1_231,
        "duplicate_formal_type_groups": 3,
        "duplicate_formal_type_excess_rows": 4,
        "parent_5_2_exact_formal_type_sha256_intersections": 0,
        "exact_release_acceptance_count": SELECTED_ROWS,
    }
    for field, expected in expected_facts.items():
        if facts.get(field) != expected:
            raise CurationError(f"source registry content_facts.{field} drifted")
    inventory = _require_object(
        source.get("selection_inventory"), "source_registry.source.selection_inventory"
    )
    expected_inventory = {
        "phase_1_raw_literal_theorems": 181,
        "phase_1_duplicate_losers": 1,
        "phase_1_accepted": 180,
        "phase_2_module_root_buckets": 21,
        "phase_2_accepted": 320,
        "two_phase_total_accepted": SELECTED_ROWS,
        "curation_candidate_rows": SOURCE_ROWS,
        "nonliteral_lemma_rows": SOURCE_LITERAL_LEMMAS,
        "eligible_literal_theorem_rows": SOURCE_LITERAL_THEOREMS,
        "accepted_literal_theorem_rows": SELECTED_ROWS,
        "nonaccepted_eligible_literal_theorem_rows": SOURCE_LITERAL_THEOREMS
        - SELECTED_ROWS,
    }
    for field, expected in expected_inventory.items():
        if inventory.get(field) != expected:
            raise CurationError(f"source registry selection_inventory.{field} drifted")

    if receipt.get("schema_version") != "awesome-theorems/stage5-parent-release-receipt/5.3":
        raise CurationError("v5.3 parent-receipt schema drifted")
    parent = _require_object(receipt.get("parent_release"), "parent_receipt.parent_release")
    if (
        parent.get("release") != PARENT_RELEASE
        or parent.get("release_root_sha256") != PARENT_RELEASE_ROOT_SHA256
        or parent.get("manifest_file_sha256") != PARENT_MANIFEST_FILE_SHA256
        or parent.get("manifest_authority_sha256")
        != PARENT_MANIFEST_AUTHORITY_SHA256
    ):
        raise CurationError("v5.3 parent receipt does not bind the exact 5.2 parent")
    identity = _require_object(
        receipt.get("identity_boundary"), "parent_receipt.identity_boundary"
    )
    if (
        identity.get("variant_high_watermark") != PARENT_ATV_HIGH_WATERMARK
        or identity.get("first_child_variant_ordinal") != FIRST_NEW_ORDINAL
    ):
        raise CurationError("v5.3 parent receipt identity boundary drifted")
    return registry, receipt, registry_authority, receipt_authority


def parent_identity_indexes(
    parent_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    by_exact_type: dict[str, str] = {}
    by_normalized_type: dict[str, str] = {}
    by_name: dict[str, str] = {}
    ordered = sorted(parent_rows, key=lambda row: str(row["variant_id"]))
    for row in ordered:
        variant_id = str(row["variant_id"])
        formal_sha = row.get("formal_type_sha256")
        formal_type = row.get("formal_type")
        qualified_name = row.get("qualified_name")
        if isinstance(formal_sha, str) and SHA256_RE.fullmatch(formal_sha):
            by_exact_type.setdefault(formal_sha, variant_id)
        if isinstance(formal_type, str) and formal_type:
            by_normalized_type.setdefault(
                normalized_formal_type_sha256(formal_type), variant_id
            )
        if isinstance(qualified_name, str) and qualified_name:
            by_name.setdefault(normalize_declaration_name(qualified_name), variant_id)
    return by_exact_type, by_normalized_type, by_name


def resolve_duplicates(
    source_rows: Sequence[Mapping[str, Any]],
    parent_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, str], dict[str, str], list[Mapping[str, Any]]]:
    """Return source-duplicate links, parent links, and viable theorem rows."""

    exact_parent, normalized_parent, name_parent = parent_identity_indexes(parent_rows)
    literal_theorems = [row for row in source_rows if row["declaration_kind"] == "theorem"]
    source_links: dict[str, str] = {}
    parent_links: dict[str, str] = {}
    seen_semantics: dict[str, str] = {}
    seen_names: dict[str, str] = {}
    viable: list[Mapping[str, Any]] = []
    for row in sorted(literal_theorems, key=duplicate_winner_rank):
        source_record_id = str(row["source_record_id"])
        normalized_type = normalized_formal_type_sha256(str(row["formal_type"]))
        name = normalize_declaration_name(str(row["declaration"]))
        parent_candidates = {
            value
            for value in (
                exact_parent.get(str(row["formal_type_sha256"])),
                normalized_parent.get(normalized_type),
                name_parent.get(name),
            )
            if value is not None
        }
        if parent_candidates:
            parent_links[source_record_id] = min(parent_candidates)
            continue
        if normalized_type in seen_semantics:
            source_links[source_record_id] = seen_semantics[normalized_type]
            continue
        if name in seen_names:
            source_links[source_record_id] = seen_names[name]
            continue
        seen_semantics[normalized_type] = source_record_id
        seen_names[name] = source_record_id
        viable.append(row)
    return source_links, parent_links, viable


def select_balanced(
    viable: Sequence[Mapping[str, Any]], count: int = SELECTED_ROWS
) -> tuple[list[Mapping[str, Any]], set[str]]:
    """Seed every docs/1000 row, then round-robin fill module roots."""

    queues: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    seed = sorted(
        [row for row in viable if DOCS_SIGNAL in importance_signal_kinds(row)],
        key=lambda row: (int(row["selection_rank"]), str(row["source_record_id"])),
    )
    if len(seed) > count:
        raise CurationError(
            f"docs/1000 seed has {len(seed)} rows, exceeding selection count {count}"
        )
    seed_ids = {str(row["source_record_id"]) for row in seed}
    for row in viable:
        if str(row["source_record_id"]) in seed_ids:
            continue
        if MODULE_MAIN_SIGNAL not in importance_signal_kinds(row):
            raise CurationError(
                f"nonseed viable row {row['source_record_id']} lacks module-main signal"
            )
        queues[module_root(row)].append(row)
    for rows in queues.values():
        rows.sort(
            key=lambda row: (int(row["selection_rank"]), str(row["source_record_id"]))
        )
    if len(viable) < count:
        raise CurationError(f"only {len(viable)} viable theorem rows; need {count}")
    selected: list[Mapping[str, Any]] = list(seed)
    fill_cursor: Counter[str] = Counter()
    roots = sorted(queues)
    while len(selected) < count:
        progress = False
        for root in roots:
            if len(selected) == count:
                break
            if fill_cursor[root] >= len(queues[root]):
                continue
            selected.append(queues[root][fill_cursor[root]])
            fill_cursor[root] += 1
            progress = True
        if not progress:
            raise CurationError("branch allocator exhausted before exact selection")
    if len({str(row["source_record_id"]) for row in selected}) != count:
        raise CurationError("branch allocator selected a source row more than once")
    return selected, seed_ids


def build_candidate_rows(
    source_rows: Sequence[Mapping[str, Any]],
    parent_rows: Sequence[Mapping[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[Mapping[str, Any]],
    set[str],
    dict[str, str],
    dict[str, str],
]:
    source_links, parent_links, viable = resolve_duplicates(source_rows, parent_rows)
    selected, seed_ids = select_balanced(viable, SELECTED_ROWS)
    selected_ranks = {
        str(row["source_record_id"]): rank
        for rank, row in enumerate(selected, start=1)
    }
    source_index_by_id = {
        str(row["source_record_id"]): index for index, row in enumerate(source_rows)
    }
    rows: list[dict[str, Any]] = []
    for source in sorted(source_rows, key=lambda row: int(row["selection_rank"])):
        source_record_id = str(source["source_record_id"])
        literal_theorem = source["declaration_kind"] == "theorem"
        truth_eligible = source["formal_proof_state"] == "kernel_checked_sorry_free"
        if not literal_theorem:
            disposition = "rejected_nonliteral_lemma"
            reason_code = "literal_declaration_kind_is_lemma"
        elif not truth_eligible:
            disposition = "rejected_proof_boundary"
            reason_code = "not_kernel_checked_sorry_free"
        elif source_record_id in parent_links:
            disposition = "rejected_parent_duplicate"
            reason_code = "exact_name_or_formal_type_already_in_parent_5_2"
        elif source_record_id in source_links:
            canonical_id = source_links[source_record_id]
            canonical = next(
                row for row in source_rows if row["source_record_id"] == canonical_id
            )
            if normalize_declaration_name(str(source["declaration"])) == normalize_declaration_name(
                str(canonical["declaration"])
            ):
                disposition = "rejected_source_name_duplicate"
                reason_code = "normalized_declaration_name_duplicate"
            else:
                disposition = "rejected_source_semantic_duplicate"
                reason_code = "normalized_formal_type_duplicate"
        elif source_record_id in selected_ranks:
            disposition = "accepted_new_kernel_checked_theorem"
            reason_code = (
                "selected_docs_1000_priority_seed"
                if source_record_id in seed_ids
                else "selected_module_main_round_robin_fill"
            )
        else:
            disposition = "eligible_not_selected"
            reason_code = "viable_theorem_outside_exact_500_selection"
        accepted = disposition == "accepted_new_kernel_checked_theorem"
        selected_rank = selected_ranks.get(source_record_id) if accepted else None
        ordinal = (
            PARENT_ATV_HIGH_WATERMARK + int(selected_rank)
            if selected_rank is not None
            else None
        )
        semantic = semantic_key(source)
        canonical_source_id = source_links.get(source_record_id)
        parent_variant_id = parent_links.get(source_record_id)
        if canonical_source_id is not None:
            canonical = next(
                row for row in source_rows if row["source_record_id"] == canonical_source_id
            )
            if source["formal_type_sha256"] == canonical["formal_type_sha256"]:
                dedupe_rationale = (
                    "Exact equality of the pinned pretty-printed formal_type SHA-256; "
                    "the higher-ranked source row is the sole canonical candidate."
                )
            elif normalized_formal_type_sha256(str(source["formal_type"])) == (
                normalized_formal_type_sha256(str(canonical["formal_type"]))
            ):
                dedupe_rationale = (
                    "Equality after whitespace normalization of the pinned formal_type; "
                    "the higher-ranked source row is the sole canonical candidate."
                )
            else:
                dedupe_rationale = (
                    "Equality of the normalized full declaration name; the higher-ranked "
                    "source row is the sole canonical candidate."
                )
            dedupe_confidence = "exact"
            dedupe_reviewer = "deterministic_exact_identity_v1"
        elif parent_variant_id is not None:
            dedupe_rationale = (
                "Exact full qualified-name or exact/whitespace-normalized formal-type "
                "identity with the sealed parent Claim_Catalog."
            )
            dedupe_confidence = "exact"
            dedupe_reviewer = "deterministic_parent_identity_v1"
        else:
            dedupe_rationale = None
            dedupe_confidence = None
            dedupe_reviewer = None
        row: dict[str, Any] = {
            "candidate_key": f"mathlib:{source_record_id}",
            "source_index": source_index_by_id[source_record_id],
            "source_record_id": source_record_id,
            "source_record_sha256": sha256_bytes(canonical_json_bytes(source)),
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
            "semantic_key": semantic,
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
            "reason_code": reason_code,
            "accepted_rank": selected_rank,
            "target_variant_id": f"ATV-{ordinal:08d}" if ordinal is not None else None,
            "target_s5_id": f"S5-CLM-{ordinal:08d}" if ordinal is not None else None,
            "canonical_source_record_id": canonical_source_id,
            "duplicate_of_semantic_key": (
                semantic_key(canonical) if canonical_source_id is not None else None
            ),
            "duplicate_of_variant_id": parent_variant_id,
            "dedupe_rationale": dedupe_rationale,
            "dedupe_confidence": dedupe_confidence,
            "dedupe_reviewer": dedupe_reviewer,
            "grants_catalog_entry": accepted,
            "grants_theorem_credit": accepted,
        }
        row["row_sha256"] = hash_without(row, "row_sha256")
        if set(row) != CANDIDATE_FIELDS:
            raise CurationError("generated candidate row field closure drifted")
        rows.append(row)
    return rows, selected, seed_ids, source_links, parent_links


def validate_generated(
    document: Mapping[str, Any],
    source_rows: Sequence[Mapping[str, Any]],
    parent_rows: Sequence[Mapping[str, Any]],
    source_registry_authority: str,
    parent_receipt_authority: str,
) -> None:
    if document.get("authority_sha256") != artifact_authority(document):
        raise CurationError("curation authority seal is stale")
    required_top = {
        "schema_version",
        "source_id",
        "source_registry_authority_sha256",
        "source_asset_sha256",
        "parent_receipt_authority_sha256",
        "candidate_dispositions",
        "counts",
        "set_digests",
        "authority_sha256",
    }
    if set(document) != required_top:
        raise CurationError("curation top-level field closure drifted")
    if document.get("schema_version") != SCHEMA_VERSION:
        raise CurationError("curation schema drifted")
    if document.get("source_id") != SOURCE_ID:
        raise CurationError("curation source_id drifted")
    if document.get("source_registry_authority_sha256") != source_registry_authority:
        raise CurationError("curation source-registry binding drifted")
    if document.get("source_asset_sha256") != SOURCE_FILE_SHA256:
        raise CurationError("curation source-asset binding drifted")
    if document.get("parent_receipt_authority_sha256") != parent_receipt_authority:
        raise CurationError("curation parent-receipt binding drifted")
    rows = _require_rows(document.get("candidate_dispositions"), "candidate_dispositions")
    if len(rows) != SOURCE_ROWS:
        raise CurationError("curation does not conserve all 1500 source rows")
    expected_rows, _selected, _seed_ids, _source_links, _parent_links = (
        build_candidate_rows(source_rows, parent_rows)
    )
    if rows != expected_rows:
        raise CurationError(
            "curation dispositions differ from the deterministic two-phase selection replay"
        )
    source_by_id = {str(row["source_record_id"]): row for row in source_rows}
    source_index_by_id = {
        str(row["source_record_id"]): index for index, row in enumerate(source_rows)
    }
    observed_ids: set[str] = set()
    accepted: list[Mapping[str, Any]] = []
    for index, row in enumerate(rows):
        if set(row) != CANDIDATE_FIELDS:
            raise CurationError(f"candidate row {index} field closure drifted")
        if row.get("row_sha256") != hash_without(row, "row_sha256"):
            raise CurationError(f"candidate row {index} hash drifted")
        source_record_id = row.get("source_record_id")
        if not isinstance(source_record_id, str) or source_record_id not in source_by_id:
            raise CurationError(f"candidate row {index} is outside the source")
        if source_record_id in observed_ids:
            raise CurationError(f"candidate row {index} duplicates a source id")
        observed_ids.add(source_record_id)
        source = source_by_id[source_record_id]
        expected_values = {
            "candidate_key": f"mathlib:{source_record_id}",
            "source_index": source_index_by_id[source_record_id],
            "source_record_sha256": sha256_bytes(canonical_json_bytes(source)),
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
            "semantic_key": semantic_key(source),
            "semantic_key_method": "exact_formal_type_sha256_v1",
        }
        for field, expected in expected_values.items():
            if row.get(field) != expected:
                raise CurationError(f"candidate row {index} {field} drifted")
        expected_semantic_payload = sha256_bytes(
            canonical_json_bytes(
                {
                    "method": "exact_formal_type_sha256_v1",
                    "formal_type_sha256": row["formal_type_sha256"],
                }
            )
        )
        if row.get("semantic_key_payload_sha256") != expected_semantic_payload:
            raise CurationError(f"candidate row {index} semantic payload drifted")
        if row.get("disposition") not in DISPOSITIONS:
            raise CurationError(f"candidate row {index} disposition is invalid")
        if row["disposition"] == "accepted_new_kernel_checked_theorem":
            if source["declaration_kind"] != "theorem":
                raise CurationError("accepted row is not a literal theorem")
            validate_truth_gate(source, f"accepted source {source_record_id}")
            if row.get("grants_catalog_entry") is not True or row.get(
                "grants_theorem_credit"
            ) is not True:
                raise CurationError("accepted row lacks both credit grants")
            if any(
                row.get(field) is not None
                for field in (
                    "canonical_source_record_id",
                    "duplicate_of_semantic_key",
                    "duplicate_of_variant_id",
                )
            ):
                raise CurationError("accepted row carries duplicate linkage")
            accepted.append(row)
        else:
            if any(
                row.get(field) is not None
                for field in ("accepted_rank", "target_variant_id", "target_s5_id")
            ):
                raise CurationError("nonaccepted row has an allocation")
            if row.get("grants_catalog_entry") is not False or row.get(
                "grants_theorem_credit"
            ) is not False:
                raise CurationError("nonaccepted row grants release credit")
    if observed_ids != set(source_by_id):
        raise CurationError("curation is not an exact source-row partition")
    if len(accepted) != SELECTED_ROWS:
        raise CurationError("curation does not accept exactly 500 rows")
    ranks = {row["accepted_rank"] for row in accepted}
    if ranks != set(range(1, SELECTED_ROWS + 1)):
        raise CurationError("selected ranks are not exactly 1..500")
    accepted_semantics = [str(row["semantic_key"]) for row in accepted]
    accepted_names = [
        normalize_declaration_name(str(row["declaration"])) for row in accepted
    ]
    if len(accepted_semantics) != len(set(accepted_semantics)):
        raise CurationError("accepted semantic keys are not unique")
    if len(accepted_names) != len(set(accepted_names)):
        raise CurationError("accepted declaration names are not unique")
    parent_exact, parent_normalized, parent_names = parent_identity_indexes(parent_rows)
    for row in accepted:
        if (
            row["formal_type_sha256"] in parent_exact
            or normalized_formal_type_sha256(
                str(source_by_id[str(row["source_record_id"])]["formal_type"])
            )
            in parent_normalized
            or normalize_declaration_name(str(row["declaration"])) in parent_names
        ):
            raise CurationError("accepted row duplicates the parent")
        rank = int(row["accepted_rank"])
        ordinal = PARENT_ATV_HIGH_WATERMARK + rank
        if row.get("target_variant_id") != f"ATV-{ordinal:08d}" or row.get(
            "target_s5_id"
        ) != f"S5-CLM-{ordinal:08d}":
            raise CurationError("accepted rank/identity allocation drifted")
    if max(int(ATV_RE.fullmatch(str(row["target_variant_id"])).group(1)) for row in accepted) != LAST_NEW_ORDINAL:  # type: ignore[union-attr]
        raise CurationError("accepted ATV allocation does not end at 7084")

    counts = _require_object(document.get("counts"), "counts")
    by_disposition = Counter(str(row["disposition"]) for row in rows)
    required_counts = {
        "source_rows": SOURCE_ROWS,
        "candidate_disposition_rows": SOURCE_ROWS,
        "eligible_literal_theorems": SOURCE_LITERAL_THEOREMS,
        "pre_eligibility_excluded_lemmas": SOURCE_LITERAL_LEMMAS,
        "literal_theorems": SOURCE_LITERAL_THEOREMS,
        "literal_lemmas": SOURCE_LITERAL_LEMMAS,
        "accepted": SELECTED_ROWS,
        "nonaccepted_eligible": SOURCE_LITERAL_THEOREMS - SELECTED_ROWS,
        "nonaccepted_total": SOURCE_ROWS - SELECTED_ROWS,
        "by_disposition": dict(sorted(by_disposition.items())),
    }
    for field, expected in required_counts.items():
        if counts.get(field) != expected:
            raise CurationError(f"curation counts.{field} drifted")
    selected_by_root = Counter(
        module_root(source_by_id[str(row["source_record_id"])]) for row in accepted
    )
    if counts.get("selected_by_module_root") != dict(sorted(selected_by_root.items())):
        raise CurationError("selected branch counts drifted")
    selected_by_tier = Counter(
        importance_tier(source_by_id[str(row["source_record_id"])]) for row in accepted
    )
    if counts.get("selected_by_importance_tier") != dict(sorted(selected_by_tier.items())):
        raise CurationError("selected importance-tier counts drifted")

    digests = _require_object(document.get("set_digests"), "set_digests")
    expected_digests = {
        "candidate_source_record_id_set_sha256": set_digest(source_by_id),
        "eligible_theorem_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"])
            for row in rows
            if row["declaration_kind"] == "theorem"
        ),
        "excluded_lemma_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"])
            for row in rows
            if row["disposition"] == "rejected_nonliteral_lemma"
        ),
        "nonaccepted_eligible_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"])
            for row in rows
            if row["declaration_kind"] == "theorem"
            and row["disposition"] != "accepted_new_kernel_checked_theorem"
        ),
        "selected_source_record_id_set_sha256": set_digest(
            str(row["source_record_id"]) for row in accepted
        ),
        "selected_declaration_set_sha256": set_digest(
            str(row["declaration"]) for row in accepted
        ),
        "selected_formal_type_sha256_set_sha256": set_digest(
            str(row["formal_type_sha256"]) for row in accepted
        ),
        "selected_semantic_key_set_sha256": set_digest(accepted_semantics),
        "selected_variant_id_set_sha256": set_digest(
            str(row["target_variant_id"]) for row in accepted
        ),
        "selected_s5_id_set_sha256": set_digest(
            str(row["target_s5_id"]) for row in accepted
        ),
        "candidate_row_sha256_set_sha256": set_digest(
            str(row["row_sha256"]) for row in rows
        ),
    }
    if digests != expected_digests:
        raise CurationError("curation set digests drifted")


def build_curation(
    *,
    source_path: Path = SOURCE_PATH,
    source_registry_path: Path = SOURCE_REGISTRY_PATH,
    parent_receipt_path: Path = PARENT_RECEIPT_PATH,
    parent_manifest_path: Path = PARENT_MANIFEST_PATH,
    parent_catalog_path: Path = PARENT_CATALOG_PATH,
) -> dict[str, Any]:
    _registry, _receipt, registry_authority, receipt_authority = (
        load_versioned_bindings(source_registry_path, parent_receipt_path)
    )
    source, source_rows, source_payload = load_source(source_path)
    manifest, catalog, parent_rows, manifest_payload, catalog_payload = load_parent(
        parent_manifest_path, parent_catalog_path
    )
    candidate_rows, selected, seed_ids, source_links, parent_links = build_candidate_rows(
        source_rows, parent_rows
    )
    dispositions = Counter(str(row["disposition"]) for row in candidate_rows)
    selected_rows = [
        row
        for row in candidate_rows
        if row["disposition"] == "accepted_new_kernel_checked_theorem"
    ]
    source_by_id = {str(row["source_record_id"]): row for row in source_rows}
    selected_sources = [source_by_id[str(row["source_record_id"])] for row in selected_rows]
    selected_by_root = Counter(module_root(row) for row in selected_sources)
    selected_by_tier = Counter(importance_tier(row) for row in selected_sources)
    selected_docs = sum(
        DOCS_SIGNAL in importance_signal_kinds(row) for row in selected_sources
    )
    selected_main = sum(
        MODULE_MAIN_SIGNAL in importance_signal_kinds(row) for row in selected_sources
    )
    document: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "source_id": SOURCE_ID,
        "source_registry_authority_sha256": registry_authority,
        "source_asset_sha256": sha256_bytes(source_payload),
        "parent_receipt_authority_sha256": receipt_authority,
        "candidate_dispositions": candidate_rows,
        "counts": {
            "source_rows": len(candidate_rows),
            "candidate_disposition_rows": len(candidate_rows),
            "eligible_literal_theorems": SOURCE_LITERAL_THEOREMS,
            "pre_eligibility_excluded_lemmas": SOURCE_LITERAL_LEMMAS,
            "literal_theorems": sum(
                row["declaration_kind"] == "theorem" for row in source_rows
            ),
            "literal_lemmas": sum(
                row["declaration_kind"] == "lemma" for row in source_rows
            ),
            "kernel_checked_sorry_free": sum(
                row["formal_proof_state"] == "kernel_checked_sorry_free"
                for row in source_rows
            ),
            "accepted": len(selected),
            "nonaccepted_eligible": SOURCE_LITERAL_THEOREMS - len(selected),
            "nonaccepted_total": len(candidate_rows) - len(selected),
            "docs_1000_priority_seed": len(seed_ids),
            "module_main_balanced_fill": len(selected) - len(seed_ids),
            "source_semantic_duplicate_rows": len(source_links),
            "parent_duplicate_rows": len(parent_links),
            "selected_branches": len(selected_by_root),
            "selected_with_docs_1000_signal": selected_docs,
            "selected_with_module_main_signal": selected_main,
            "by_disposition": dict(sorted(dispositions.items())),
            "selected_by_module_root": dict(sorted(selected_by_root.items())),
            "selected_by_importance_tier": dict(sorted(selected_by_tier.items())),
        },
        "set_digests": {
            "candidate_source_record_id_set_sha256": set_digest(
                str(row["source_record_id"]) for row in candidate_rows
            ),
            "eligible_theorem_source_record_id_set_sha256": set_digest(
                str(row["source_record_id"])
                for row in candidate_rows
                if row["declaration_kind"] == "theorem"
            ),
            "excluded_lemma_source_record_id_set_sha256": set_digest(
                str(row["source_record_id"])
                for row in candidate_rows
                if row["disposition"] == "rejected_nonliteral_lemma"
            ),
            "nonaccepted_eligible_source_record_id_set_sha256": set_digest(
                str(row["source_record_id"])
                for row in candidate_rows
                if row["declaration_kind"] == "theorem"
                and row["disposition"]
                != "accepted_new_kernel_checked_theorem"
            ),
            "selected_source_record_id_set_sha256": set_digest(
                str(row["source_record_id"]) for row in selected_rows
            ),
            "selected_declaration_set_sha256": set_digest(
                str(row["declaration"]) for row in selected_rows
            ),
            "selected_formal_type_sha256_set_sha256": set_digest(
                str(row["formal_type_sha256"]) for row in selected_rows
            ),
            "selected_semantic_key_set_sha256": set_digest(
                str(row["semantic_key"]) for row in selected_rows
            ),
            "selected_variant_id_set_sha256": set_digest(
                str(row["target_variant_id"]) for row in selected_rows
            ),
            "selected_s5_id_set_sha256": set_digest(
                str(row["target_s5_id"]) for row in selected_rows
            ),
            "candidate_row_sha256_set_sha256": set_digest(
                str(row["row_sha256"]) for row in candidate_rows
            ),
        },
    }
    document["authority_sha256"] = artifact_authority(document)
    validate_generated(
        document,
        source_rows,
        parent_rows,
        registry_authority,
        receipt_authority,
    )
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
        temporary.unlink(missing_ok=True)
        raise


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE_PATH)
    parser.add_argument("--source-registry", type=Path, default=SOURCE_REGISTRY_PATH)
    parser.add_argument("--parent-receipt", type=Path, default=PARENT_RECEIPT_PATH)
    parser.add_argument("--parent-manifest", type=Path, default=PARENT_MANIFEST_PATH)
    parser.add_argument("--parent-catalog", type=Path, default=PARENT_CATALOG_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument(
        "--check", action="store_true", help="compare output bytes without writing"
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        document = build_curation(
            source_path=args.source,
            source_registry_path=args.source_registry,
            parent_receipt_path=args.parent_receipt,
            parent_manifest_path=args.parent_manifest,
            parent_catalog_path=args.parent_catalog,
        )
        payload = encoded_document(document)
        if args.check:
            try:
                observed = args.output.read_bytes()
            except OSError as error:
                raise CurationError(f"cannot read --check output: {error}") from error
            if observed != payload:
                raise CurationError("curation output bytes differ from deterministic rebuild")
            action = "checked"
        else:
            atomic_write(args.output, payload)
            action = "wrote"
        print(
            f"PASS build_mathlib_theorem_curation_v5_3 ({action}) "
            f"source_rows={document['counts']['source_rows']} "
            f"accepted={document['counts']['accepted']} "
            f"authority_sha256={document['authority_sha256']}"
        )
        return 0
    except (CurationError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"FAIL build_mathlib_theorem_curation_v5_3: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
