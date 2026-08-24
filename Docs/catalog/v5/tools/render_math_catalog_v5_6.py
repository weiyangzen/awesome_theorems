#!/usr/bin/env python3
"""Render authenticated, user-readable Markdown for Stage5 release 5.6.

The JSON release remains the authority.  Before rendering anything this tool
independently checks the manifest seal, the complete artifact inventory and
release root, every artifact byte/hash/row-count binding, the exact theorem and
open-claim projections, and every effective strict-conjecture credit.

Only Python's standard library is used.  The default mode atomically writes the
three Markdown projections under ``Docs/catalog/v5/readable/5.6``.  ``--check``
is read-only and compares all three files byte-for-byte.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import fcntl
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Iterable, Mapping, Sequence


RELEASE = "5.6"
PARENT_RELEASE = "5.5"
V5_REL = Path("Docs/catalog/v5")
RELEASE_REL = V5_REL / "releases/5.6"
PARENT_STRICT_REL = V5_REL / "releases/5.5/Strict_Conjecture_Ledger.json"
READABLE_REL = V5_REL / "readable/5.6"
MANIFEST_NAME = "Release_Manifest.json"
CATALOG_NAME = "Claim_Catalog.json"
THEOREM_NAME = "Theorem_List.json"
OPEN_NAME = "Open_Claim_List.json"
STRICT_NAME = "Strict_Conjecture_Ledger.json"

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
ALL_RELEASE_FILES = frozenset((*RELEASE_FILES, MANIFEST_NAME))
OUTPUT_FILES = (
    "Theorem_List.md",
    "Open_Claim_List.md",
    "Strict_Conjecture_List.md",
)

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
S5_RE = re.compile(r"^S5-CLM-([0-9]{8})$")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")

MANIFEST_FIELDS = frozenset(
    {
        "schema_version",
        "release",
        "parent_release",
        "parent_release_root_sha256",
        "authoritative_inputs",
        "accepted_set_digests",
        "release_allocation_digests",
        "quality_qualification",
        "strict_credit_binding",
        "publication",
        "artifacts",
        "counts",
        "release_root_sha256",
        "authority_sha256",
    }
)
CATALOG_FIELDS = frozenset(
    {
        "schema_version",
        "artifact",
        "release",
        "catalog_scope",
        "authoritative_inputs",
        "quality_qualification",
        "origin_5_6_closed_schema",
        "counts",
        "records",
        "authority_sha256",
    }
)
PROJECTION_FIELDS = frozenset(
    {
        "schema_version",
        "artifact",
        "release",
        "authoritative_inputs",
        "query",
        "stage_claim_ids",
        "counts",
        "records",
        "authority_sha256",
    }
)
STRICT_FIELDS = frozenset(
    {
        "schema_version",
        "release",
        "parent_release_root_sha256",
        "parent_strict_ledger_file_sha256",
        "parent_strict_ledger_authority_sha256",
        "strict_credits",
        "credit_corrections",
        "counts",
        "set_digests",
        "origin_5_6_change",
        "authority_sha256",
    }
)
LEGACY_CREDIT_FIELDS = frozenset(
    {
        "stage_claim_id",
        "variant_id",
        "origin_release",
        "credit_source_branch",
        "semantic_key",
        "grants_strict_conjecture_credit",
        "evidence_sha256",
        "row_sha256",
    }
)
ORIGIN_5_5_CREDIT_FIELDS = frozenset(
    {
        "stage_claim_id",
        "variant_id",
        "semantic_key",
        "origin_release",
        "credit_source_branch",
        "evidence_sha256",
        "catalog_record_sha256",
        "statement_sha256",
        "curation_row_sha256",
        "source_row_sha256",
        "source_authority_file_sha256",
        "allocation_request_sha256",
        "grants_strict_conjecture_credit",
        "row_sha256",
    }
)
EXPECTED_MANIFEST_COUNTS = {
    "non_manifest_artifacts": 8,
    "catalog_records": 5_525,
    "origin_theorems": 1_000,
    "origin_open_claims": 0,
    "origin_strict_conjectures": 0,
    "cumulative_theorems": 3_500,
    "cumulative_open_claims": 2_025,
    "effective_strict_conjecture_credits": 1_425,
    "net_strict_increase_after_5_0": 1_024,
    "terminal_ready_unselected": 92,
    "preserved_quarantine": 469,
    "canonical_variants": 9_009,
    "variants": 9_009,
}


class RenderError(RuntimeError):
    """An authenticated release or readable projection is invalid."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RenderError(message)


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise RenderError(f"value is not canonical JSON: {error}") from error


def _encoded(value: Any) -> bytes:
    return _canonical(value) + b"\n"


def _digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _hash_without(value: Mapping[str, Any], *fields: str) -> str:
    omitted = set(fields)
    return _digest(_canonical({key: item for key, item in value.items() if key not in omitted}))


def _set_digest(values: Iterable[str]) -> str:
    return _digest(_canonical(sorted(values)))


def _reject_constant(token: str) -> None:
    raise RenderError(f"non-finite JSON token is forbidden: {token}")


def _closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def parse_document_bytes(raw: bytes, label: str, *, canonical_file: bool = True) -> dict[str, Any]:
    """Parse one strict JSON object, rejecting duplicate keys and non-finite values."""

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_closed_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise RenderError(f"invalid JSON in {label}: {error}") from error
    _require(isinstance(value, dict), f"{label} must contain one object")
    if canonical_file:
        _require(raw == _encoded(value), f"{label} is not canonical JSON plus one LF")
    return value


def verify_seal(document: Mapping[str, Any], label: str) -> None:
    authority = document.get("authority_sha256")
    _require(
        isinstance(authority, str) and SHA_RE.fullmatch(authority) is not None,
        f"{label} authority is malformed",
    )
    _require(
        authority == _hash_without(document, "authority_sha256"),
        f"{label} authority seal is stale",
    )


def _nonnegative_int(value: Any, label: str) -> int:
    _require(
        isinstance(value, int) and not isinstance(value, bool) and value >= 0,
        f"{label} must be a non-negative integer",
    )
    return int(value)


def _string(value: Any, label: str, pattern: re.Pattern[str] | None = None) -> str:
    _require(isinstance(value, str) and bool(value.strip()), f"{label} must be a non-empty string")
    if pattern is not None:
        _require(pattern.fullmatch(value) is not None, f"{label} syntax is invalid: {value!r}")
    return value


def _rows(value: Any, label: str) -> list[dict[str, Any]]:
    _require(
        isinstance(value, list) and all(isinstance(row, dict) for row in value),
        f"{label} must be an array of objects",
    )
    return value


def _repo_root(path: Path) -> Path:
    absolute = path.absolute()
    _require(not absolute.is_symlink(), f"symlinked repository root is forbidden: {path}")
    try:
        root = absolute.resolve(strict=True)
    except OSError as error:
        raise RenderError(f"repository root does not exist: {path}") from error
    _require(root == absolute and root.is_dir(), f"repository root is aliased or not a directory: {path}")
    return root


def _safe_path(root: Path, relative: Path | str, *, file: bool = True) -> Path:
    raw = Path(relative)
    _require(not raw.is_absolute() and raw.parts and ".." not in raw.parts, f"unsafe path: {relative}")
    cursor = root
    for component in raw.parts:
        cursor = cursor / component
        _require(not cursor.is_symlink(), f"symlinked authoritative path is forbidden: {relative}")
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise RenderError(f"path escapes repository root: {relative}") from error
    _require(
        candidate.is_file() if file else candidate.is_dir(),
        f"required {'file' if file else 'directory'} is missing: {relative}",
    )
    return candidate


def _primary_rows(name: str, document: Mapping[str, Any]) -> int:
    key = {
        "Claim_Catalog.json": "records",
        "Claim_ID_Registry.json": "variants",
        "Stage5_Claim_ID_Registry.json": "mappings",
        "Migration_v4_to_v5.json": "migrations",
        "Theorem_List.json": "records",
        "Open_Claim_List.json": "records",
        "Coverage_Ledger.json": "candidate_dispositions",
        "Strict_Conjecture_Ledger.json": "strict_credits",
    }[name]
    rows = document.get(key)
    _require(isinstance(rows, list), f"{name}.{key} must be an array")
    result = len(rows)
    if name == "Coverage_Ledger.json":
        extra = document.get("msc_coverage")
        _require(isinstance(extra, list), "Coverage_Ledger.json.msc_coverage must be an array")
        result += len(extra)
    elif name == STRICT_NAME:
        extra = document.get("credit_corrections")
        _require(isinstance(extra, list), f"{STRICT_NAME}.credit_corrections must be an array")
        result += len(extra)
    return result


def _release_root(artifacts: Sequence[Mapping[str, Any]]) -> str:
    payload = sorted(
        (
            {
                "path": row["path"],
                "sha256": row["sha256"],
                "size_bytes": row["size_bytes"],
            }
            for row in artifacts
        ),
        key=lambda row: str(row["path"]),
    )
    return _digest(_canonical(payload))


def validate_manifest(manifest: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """Validate the closed 5.6 manifest and return its artifact bindings."""

    _require(set(manifest) == MANIFEST_FIELDS, "manifest top-level field set drifted")
    _require(
        manifest.get("schema_version") == "awesome-theorems/stage5-release-manifest/5.6",
        "manifest schema_version is not 5.6",
    )
    _require(
        manifest.get("release") == RELEASE and manifest.get("parent_release") == PARENT_RELEASE,
        "manifest release/parent binding is invalid",
    )
    _string(manifest.get("parent_release_root_sha256"), "manifest parent root", SHA_RE)
    declared_root = _string(manifest.get("release_root_sha256"), "manifest release root", SHA_RE)
    verify_seal(manifest, MANIFEST_NAME)

    artifacts = _rows(manifest.get("artifacts"), "manifest.artifacts")
    _require(len(artifacts) == len(RELEASE_FILES), "manifest artifact denominator drifted")
    _require(
        [row.get("path") for row in artifacts] == sorted(RELEASE_FILES),
        "manifest artifact set/order drifted",
    )
    bindings: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(artifacts):
        _require(
            set(row) == {"path", "sha256", "size_bytes", "row_count"},
            f"manifest.artifacts[{index}] field set drifted",
        )
        name = _string(row.get("path"), f"manifest.artifacts[{index}].path")
        _require(Path(name).name == name, f"unsafe manifest artifact path: {name!r}")
        _string(row.get("sha256"), f"manifest.artifacts[{index}].sha256", SHA_RE)
        _nonnegative_int(row.get("size_bytes"), f"manifest.artifacts[{index}].size_bytes")
        _nonnegative_int(row.get("row_count"), f"manifest.artifacts[{index}].row_count")
        _require(name not in bindings, f"manifest duplicates artifact path {name!r}")
        bindings[name] = dict(row)
    _require(set(bindings) == set(RELEASE_FILES), "manifest artifact denominator is not closed")
    _require(_release_root(artifacts) == declared_root, "manifest release root does not recompute")
    _require(manifest.get("counts") == EXPECTED_MANIFEST_COUNTS, "manifest count boundary drifted")

    strict_binding = manifest.get("strict_credit_binding")
    _require(isinstance(strict_binding, dict), "manifest strict-credit binding is malformed")
    _require(
        set(strict_binding)
        == {"effective_credits", "new_credits", "strict_credit_set_sha256", "strict_ledger_authority_sha256"},
        "manifest strict-credit binding field set drifted",
    )
    _require(
        strict_binding.get("effective_credits") == 1_425 and strict_binding.get("new_credits") == 0,
        "manifest strict-credit count binding drifted",
    )
    _string(strict_binding.get("strict_ledger_authority_sha256"), "strict ledger authority", SHA_RE)

    quality = manifest.get("quality_qualification")
    _require(isinstance(quality, dict), "manifest quality qualification is malformed")
    origin = quality.get("origin_5_6")
    _require(isinstance(origin, dict), "manifest origin-5.6 quality qualification is malformed")
    required_quality = {
        "accepted_kernel_checked_sorry_free_formal_identities": 1_000,
        "selected_individual_declaration_docstring": 511,
        "selected_module_main_result_description": 489,
        "source_syntax_theorem": 629,
        "source_syntax_lemma": 371,
        "human_semantic_uniqueness_claimed": False,
        "independent_universal_importance_ranking_claimed": False,
        "unsupported_formal_truth_credit": 0,
    }
    for key, value in required_quality.items():
        _require(origin.get(key) == value, f"manifest quality boundary drifted: {key}")
    return bindings


def theorem_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("record_role") == "claim"
        and row.get("lifecycle") == "active"
        and row.get("truth_apt") is True
        and row.get("current_claim_kind") == "theorem"
        and row.get("category") == "theorem"
        and row.get("material_status") == "proved"
    )


def open_predicate(row: Mapping[str, Any]) -> bool:
    return bool(
        row.get("record_role") == "claim"
        and row.get("lifecycle") == "active"
        and row.get("truth_apt") is True
        and row.get("category") == "open_claim"
        and row.get("current_claim_kind") in {"conjecture", "hypothesis", "open_problem"}
        and row.get("material_status") in {"open", "partial", "independent", "disputed"}
    )


@dataclass(frozen=True)
class StatementView:
    text: str
    language: str
    representation: str
    rights_boundary: str
    attribution: tuple[str, ...]
    source_pointer: str


def _clean_text(value: Any, label: str) -> str:
    text = _string(value, label)
    for character in text:
        if ord(character) < 32 and character not in "\n\r\t":
            raise RenderError(f"{label} contains a forbidden control character")
    # Preserve authenticated source bytes semantically, including CRLF embedded
    # in a JSON string.  Normalizing here would invalidate the pinned statement
    # digest and would make a readable projection silently cease to be exact.
    return text


def _source_pointer(record: Mapping[str, Any]) -> str:
    locator = record.get("source_locator")
    if not isinstance(locator, dict):
        locator = record.get("locator")
    _require(isinstance(locator, dict), f"{record.get('stage_claim_id')} lacks a source locator")
    if isinstance(locator.get("url"), str) and locator["url"]:
        return locator["url"]
    if isinstance(locator.get("source_url"), str) and locator["source_url"]:
        return locator["source_url"]
    path = locator.get("path") or locator.get("member_path") or locator.get("source_path")
    if isinstance(path, str) and path:
        line = locator.get("line_number") or locator.get("line_start")
        return f"{path}:{line}" if isinstance(line, int) else path
    artifact = locator.get("artifact_path") or locator.get("upstream_asset_path")
    if isinstance(artifact, str) and artifact:
        return artifact
    raise RenderError(f"{record.get('stage_claim_id')} has no displayable source pointer")


def _string_attribution(value: Any, label: str) -> tuple[str, ...]:
    if isinstance(value, str):
        return (_clean_text(value, label),)
    _require(
        isinstance(value, list) and value and all(isinstance(item, str) and item.strip() for item in value),
        f"{label} must be a non-empty string or string array",
    )
    return tuple(_clean_text(item, label) for item in value)


def statement_view(record: Mapping[str, Any]) -> StatementView:
    """Select exactly one rights-permitted mathematical/formal statement."""

    stage_id = _string(record.get("stage_claim_id"), "record.stage_claim_id", S5_RE)
    origin = _string(record.get("origin_release"), f"{stage_id}.origin_release")
    source_id = _string(record.get("source_id"), f"{stage_id}.source_id")
    rights = record.get("rights")
    _require(isinstance(rights, dict), f"{stage_id}.rights must be an object")
    pointer = _source_pointer(record)

    if origin in {"5.0", "5.1"}:
        _require(
            rights.get("redistribution_mode") == "source_terms_preserved_in_repository_inventory"
            and rights.get("formal_code_terms") == "Apache-2.0"
            and rights.get("not_independently_cleared") is True,
            f"{stage_id} legacy rights do not permit the formal-statement projection",
        )
        formal = record.get("formal_statement")
        _require(isinstance(formal, dict), f"{stage_id}.formal_statement must be an object")
        text = formal.get("declaration_type") or formal.get("formal_type")
        text = _clean_text(text, f"{stage_id} exact formal type")
        declared_sha = formal.get("declaration_type_sha256") or formal.get("formal_type_sha256")
        _require(declared_sha == _digest(text.encode("utf-8")), f"{stage_id} formal type hash is stale")
        attribution = _string_attribution(rights.get("attribution"), f"{stage_id}.rights.attribution")
        return StatementView(
            text=text,
            language="lean",
            representation="exact formal declaration type",
            rights_boundary=(
                "Apache-2.0 formal code; source terms preserved inside the repository inventory; "
                "natural-language source text is not independently cleared"
            ),
            attribution=attribution,
            source_pointer=pointer,
        )

    if origin == "5.2":
        _require(
            rights.get("publication_text_allowed") is True
            and rights.get("text_withheld") is False
            and rights.get("spdx_expression") == "CC-BY-4.0"
            and rights.get("redistribution_mode") == "verbatim_cc_by_4_0_with_per_record_attribution"
            and rights.get("catalog_relicenses_source") is False,
            f"{stage_id} OpenConjecture rights do not permit statement publication",
        )
        statement = record.get("mathematical_statement")
        _require(isinstance(statement, dict), f"{stage_id}.mathematical_statement must be an object")
        text = _clean_text(statement.get("body_tex"), f"{stage_id} source body_tex")
        _require(
            statement.get("body_tex_sha256") == _digest(text.encode("utf-8")),
            f"{stage_id} body_tex hash is stale",
        )
        authors = statement and rights.get("attribution_authors")
        attribution = _string_attribution(authors, f"{stage_id}.rights.attribution_authors")
        title = rights.get("attribution_title")
        if isinstance(title, str) and title.strip():
            attribution = (*attribution, _clean_text(title, f"{stage_id}.rights.attribution_title"))
        return StatementView(
            text=text,
            language="latex",
            representation="verbatim source conjecture block",
            rights_boundary="CC-BY-4.0 verbatim text with per-record attribution; catalog does not relicense source",
            attribution=attribution,
            source_pointer=pointer,
        )

    if origin in {"5.3", "5.4", "5.6"}:
        _require(
            rights.get("redistribution_mode") == "apache_2_0_with_attribution"
            and rights.get("formal_code_terms") == "Apache-2.0"
            and rights.get("docstring_terms") == "Apache-2.0"
            and rights.get("catalog_relicenses_source") is False,
            f"{stage_id} mathlib rights do not permit the formal-statement projection",
        )
        formal = record.get("formal_statement")
        _require(isinstance(formal, dict), f"{stage_id}.formal_statement must be an object")
        text = _clean_text(formal.get("formal_type"), f"{stage_id} exact formal type")
        _require(
            formal.get("formal_type_sha256") == _digest(text.encode("utf-8")),
            f"{stage_id} formal type hash is stale",
        )
        attribution = _string_attribution(rights.get("attribution"), f"{stage_id}.rights.attribution")
        return StatementView(
            text=text,
            language="lean",
            representation="exact runtime formal type",
            rights_boundary="Apache-2.0 formal statement with attribution; catalog does not relicense source",
            attribution=attribution,
            source_pointer=pointer,
        )

    if origin == "5.5":
        _require(
            rights.get("cleared_for_catalog_metadata_and_statement") is True
            and rights.get("source_pointer_required") is True,
            f"{stage_id} reviewed-source rights do not permit statement publication",
        )
        statement = record.get("mathematical_statement")
        _require(isinstance(statement, dict), f"{stage_id}.mathematical_statement must be an object")
        attribution = _string_attribution(rights.get("attribution"), f"{stage_id}.rights.attribution")
        if source_id == "SRC-MATH-V5-5-OPEN-PROBLEM-GARDEN":
            _require(
                rights.get("exact_source_wording_excluded_from_release") is True
                and rights.get("source_wording_redistributed") is False
                and rights.get("statement_origin") == "independently_written_reviewed_summary"
                and statement.get("representation") == "independently_written_reviewed_summary",
                f"{stage_id} Open Problem Garden source-wording boundary drifted",
            )
            text = _clean_text(statement.get("semantic_summary"), f"{stage_id} independent summary")
            _require(
                statement.get("summary_sha256") == _digest(text.encode("utf-8")),
                f"{stage_id} independent summary hash is stale",
            )
            boundary = "independently written reviewed summary only; exact source wording is excluded; source pointer retained"
            representation = "independently written reviewed summary"
        else:
            allowed = {
                "SRC-MATH-V5-5-OEIS": "CC-BY-SA-4.0",
                "SRC-MATH-V5-5-AIMPL": "CC-BY-SA-3.0",
                "SRC-MATH-V5-5-OPEN-LOGIC": "CC-BY-4.0",
            }
            _require(source_id in allowed, f"{stage_id} has an unknown 5.5 source-rights branch")
            _require(rights.get("license_spdx") == allowed[source_id], f"{stage_id} SPDX boundary drifted")
            _require(
                statement.get("representation") == "reviewed_exact_source_assertion",
                f"{stage_id} exact reviewed-statement representation drifted",
            )
            text = _clean_text(statement.get("exact_claim_text"), f"{stage_id} reviewed exact claim")
            expected_statement_sha = _digest(
                _canonical({"claim": text, "context": statement.get("exact_claim_context")})
            )
            _require(
                statement.get("statement_sha256") == expected_statement_sha,
                f"{stage_id} reviewed statement hash is stale",
            )
            boundary = f"{allowed[source_id]} reviewed statement with required attribution/source pointer"
            representation = "reviewed exact source assertion"
        return StatementView(
            text=text,
            language="text",
            representation=representation,
            rights_boundary=boundary,
            attribution=attribution,
            source_pointer=pointer,
        )

    raise RenderError(f"{stage_id} has unsupported origin/rights branch {origin!r}")


def validate_catalog(document: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, StatementView]]:
    _require(set(document) == CATALOG_FIELDS, "catalog top-level field set drifted")
    _require(
        document.get("schema_version") == "awesome-theorems/stage5-claim-catalog/5.6"
        and document.get("artifact") == CATALOG_NAME
        and document.get("release") == RELEASE,
        "catalog header drifted",
    )
    verify_seal(document, CATALOG_NAME)
    records = _rows(document.get("records"), "catalog.records")
    ids: list[str] = []
    variants: list[str] = []
    index: dict[str, dict[str, Any]] = {}
    views: dict[str, StatementView] = {}
    for number, row in enumerate(records):
        stage_id = _string(row.get("stage_claim_id"), f"catalog.records[{number}].stage_claim_id", S5_RE)
        variant_id = _string(row.get("variant_id"), f"catalog.records[{number}].variant_id", ATV_RE)
        _require(stage_id not in index, f"catalog duplicates {stage_id}")
        _require(S5_RE.fullmatch(stage_id).group(1) == ATV_RE.fullmatch(variant_id).group(1), f"{stage_id} variant ordinal differs")
        _clean_text(row.get("display_name"), f"{stage_id}.display_name")
        _string(row.get("current_claim_kind"), f"{stage_id}.current_claim_kind")
        _string(row.get("source_id"), f"{stage_id}.source_id")
        is_theorem = theorem_predicate(row)
        is_open = open_predicate(row)
        _require(is_theorem != is_open, f"{stage_id} is not in exactly one catalog predicate")
        index[stage_id] = row
        ids.append(stage_id)
        variants.append(variant_id)
        views[stage_id] = statement_view(row)
    _require(ids == sorted(ids) and len(ids) == len(set(ids)), "catalog S5 IDs are not unique sorted order")
    _require(len(variants) == len(set(variants)), "catalog variant IDs are not unique")

    theorem_count = sum(theorem_predicate(row) for row in records)
    open_count = sum(open_predicate(row) for row in records)
    origin_rows = [row for row in records if row.get("origin_release") == RELEASE]
    expected_counts = {
        "records": len(records),
        "origin_theorems": sum(theorem_predicate(row) for row in origin_rows),
        "origin_open_claims": sum(open_predicate(row) for row in origin_rows),
        "origin_strict_conjectures": sum(
            open_predicate(row) and row.get("current_claim_kind") == "conjecture" for row in origin_rows
        ),
        "cumulative_theorems": theorem_count,
        "cumulative_open_claims": open_count,
        "effective_strict_conjectures": 1_425,
    }
    _require(document.get("counts") == expected_counts, "catalog counts do not match its records")
    _require(len(records) == 5_525 and theorem_count == 3_500 and open_count == 2_025, "catalog 5.6 quantity boundary drifted")
    return records, index, views


def validate_projection(
    name: str,
    document: Mapping[str, Any],
    catalog_records: Sequence[Mapping[str, Any]],
    *,
    bucket: str,
) -> list[str]:
    """Validate a projection as an exact ordered copy of the catalog predicate."""

    _require(name in {THEOREM_NAME, OPEN_NAME}, f"unknown projection: {name}")
    _require(set(document) == PROJECTION_FIELDS, f"{name} top-level field set drifted")
    _require(
        document.get("schema_version") == "awesome-theorems/stage5-query-projection/5.6"
        and document.get("artifact") == name
        and document.get("release") == RELEASE
        and document.get("query") == "pure predicate over Claim_Catalog.json; records copied byte-semantically",
        f"{name} header drifted",
    )
    verify_seal(document, name)
    rows = _rows(document.get("records"), f"{name}.records")
    ids = document.get("stage_claim_ids")
    _require(isinstance(ids, list) and all(isinstance(value, str) for value in ids), f"{name}.stage_claim_ids is malformed")
    actual_ids = [row.get("stage_claim_id") for row in rows]
    _require(ids == actual_ids, f"{name} IDs do not exactly match its copied records")
    _require(ids == sorted(set(ids)), f"{name} IDs are not unique sorted order")
    predicate = theorem_predicate if bucket == "theorem" else open_predicate
    expected_rows = [row for row in catalog_records if predicate(row)]
    _require(rows == expected_rows, f"{name} is not the exact ordered catalog predicate")
    _require(document.get("counts") == {"records": len(rows)}, f"{name} record count is stale")
    return list(ids)


def _legacy_evidence(record: Mapping[str, Any]) -> str:
    if record.get("origin_release") in {"5.0", "5.1"}:
        content_hash = _digest(
            _canonical(
                {
                    "formal_statement": record.get("formal_statement"),
                    "mathematical_statement": record.get("mathematical_statement"),
                }
            )
        )
        source_hash = _digest(
            _canonical(
                {
                    "source_id": record.get("source_id"),
                    "locator": record.get("locator"),
                    "formal_statement": record.get("formal_statement"),
                    "provenance": record.get("provenance"),
                }
            )
        )
        rights_hash = _digest(_canonical(record.get("rights")))
    else:
        content_hash = _string(record.get("content_payload_sha256"), "strict record content hash", SHA_RE)
        source_hash = _string(record.get("source_payload_sha256"), "strict record source hash", SHA_RE)
        rights = record.get("rights")
        _require(isinstance(rights, dict), "strict record rights are malformed")
        rights_hash = _string(rights.get("rights_payload_sha256"), "strict record rights hash", SHA_RE)
    allocation = record.get("allocation")
    _require(isinstance(allocation, dict), "strict record allocation is malformed")
    return _digest(
        _canonical(
            {
                "record_sha256": _digest(_canonical(record)),
                "content_payload_sha256": content_hash,
                "source_payload_sha256": source_hash,
                "rights_payload_sha256": rights_hash,
                "allocation_request_sha256": _string(
                    allocation.get("allocation_request_sha256"), "strict allocation request", SHA_RE
                ),
            }
        )
    )


def validate_strict_credit(
    credit: Mapping[str, Any],
    record: Mapping[str, Any],
    *,
    index: int = 0,
) -> None:
    """Validate one strict credit against its exact catalog record."""

    label = f"strict_credits[{index}]"
    origin = credit.get("origin_release")
    expected_fields = ORIGIN_5_5_CREDIT_FIELDS if origin == "5.5" else LEGACY_CREDIT_FIELDS
    _require(set(credit) == expected_fields, f"{label} field set drifted")
    _require(credit.get("row_sha256") == _hash_without(credit, "row_sha256"), f"{label} row seal is stale")
    stage_id = _string(credit.get("stage_claim_id"), f"{label}.stage_claim_id", S5_RE)
    variant_id = _string(credit.get("variant_id"), f"{label}.variant_id", ATV_RE)
    _require(
        record.get("stage_claim_id") == stage_id
        and record.get("variant_id") == variant_id
        and record.get("origin_release") == origin,
        f"{label} identity differs from the catalog",
    )
    _require(
        credit.get("grants_strict_conjecture_credit") is True
        and record.get("record_role") == "claim"
        and record.get("lifecycle") == "active"
        and record.get("truth_apt") is True
        and record.get("category") == "open_claim"
        and record.get("current_claim_kind") == "conjecture"
        and record.get("material_status") == "open",
        f"{label} does not join to an active open conjecture",
    )
    expected_semantic = record.get("semantic_key")
    if not isinstance(expected_semantic, str):
        expected_semantic = "formal-conjectures-semantic/" + _string(
            record.get("semantic_payload_sha256"), f"{stage_id}.semantic_payload_sha256", SHA_RE
        )
    _require(credit.get("semantic_key") == expected_semantic, f"{label} semantic identity differs")

    if origin == "5.0":
        _require(
            credit.get("credit_source_branch") == "effective_parent_5_1_direct_prop"
            and record.get("formal_shape") == "direct_prop",
            f"{label} legacy strict-credit branch is invalid",
        )
        _require(credit.get("evidence_sha256") == _legacy_evidence(record), f"{label} evidence hash is stale")
    elif origin == "5.2":
        _require(
            credit.get("credit_source_branch") == "origin_5_2_curated_latex_environment",
            f"{label} 5.2 strict-credit branch is invalid",
        )
        _require(credit.get("evidence_sha256") == _legacy_evidence(record), f"{label} evidence hash is stale")
    elif origin == "5.5":
        provenance = record.get("provenance")
        disposition = record.get("curator_disposition")
        locator = record.get("source_locator")
        allocation = record.get("allocation")
        statement = record.get("mathematical_statement")
        _require(all(isinstance(value, dict) for value in (provenance, disposition, locator, allocation, statement)), f"{label} joined record bindings are malformed")
        branch = f"origin_5_5_{provenance['source_kind']}_reviewed_assertion"
        wanted = {
            "credit_source_branch": branch,
            "evidence_sha256": record.get("content_payload_sha256"),
            "catalog_record_sha256": record.get("catalog_record_sha256"),
            "statement_sha256": statement.get("statement_sha256"),
            "curation_row_sha256": disposition.get("ledger_row_sha256"),
            "source_row_sha256": locator.get("source_row_sha256"),
            "source_authority_file_sha256": locator.get("authority_receipt", {}).get("file_sha256"),
            "allocation_request_sha256": allocation.get("allocation_request_sha256"),
        }
        for key, value in wanted.items():
            _require(credit.get(key) == value, f"{label} {key} differs from its catalog record")
        _require(
            record.get("catalog_record_sha256") == _hash_without(record, "catalog_record_sha256"),
            f"{label} catalog record seal is stale",
        )
    else:
        raise RenderError(f"{label} has unsupported origin {origin!r}")


def validate_strict_ledger(
    document: Mapping[str, Any],
    catalog_index: Mapping[str, Mapping[str, Any]],
    manifest: Mapping[str, Any],
    parent_document: Mapping[str, Any],
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    _require(set(document) == STRICT_FIELDS, f"{STRICT_NAME} top-level field set drifted")
    _require(
        document.get("schema_version") == "awesome-theorems/stage5-strict-conjecture-ledger/5.6"
        and document.get("release") == RELEASE,
        f"{STRICT_NAME} header drifted",
    )
    verify_seal(document, STRICT_NAME)
    _require(
        document.get("parent_release_root_sha256") == manifest.get("parent_release_root_sha256"),
        f"{STRICT_NAME} parent root differs from the manifest",
    )
    verify_seal(parent_document, "5.5 strict ledger")
    _require(parent_document.get("release") == PARENT_RELEASE, "parent strict ledger release drifted")
    _require(
        document.get("parent_strict_ledger_authority_sha256") == parent_document.get("authority_sha256"),
        "parent strict-ledger authority binding drifted",
    )

    credits = _rows(document.get("strict_credits"), f"{STRICT_NAME}.strict_credits")
    corrections = _rows(document.get("credit_corrections"), f"{STRICT_NAME}.credit_corrections")
    _require(
        credits == parent_document.get("strict_credits")
        and corrections == parent_document.get("credit_corrections")
        and document.get("origin_5_6_change")
        == {"strict_credits_added": 0, "strict_credits_removed": 0, "credit_corrections_added": 0},
        "5.6 strict ledger is not an unchanged parent-credit carry-forward",
    )
    ids: list[str] = []
    variants: list[str] = []
    semantics: list[str] = []
    credit_by_id: dict[str, dict[str, Any]] = {}
    origins: Counter[str] = Counter()
    for index, credit in enumerate(credits):
        stage_id = credit.get("stage_claim_id")
        _require(isinstance(stage_id, str) and stage_id in catalog_index, f"strict_credits[{index}] references a missing catalog ID")
        validate_strict_credit(credit, catalog_index[stage_id], index=index)
        ids.append(stage_id)
        variants.append(str(credit["variant_id"]))
        semantics.append(str(credit["semantic_key"]))
        origins[str(credit["origin_release"])] += 1
        credit_by_id[stage_id] = dict(credit)
    _require(ids == sorted(set(ids)), "strict-credit S5 IDs are not unique sorted order")
    _require(variants == sorted(set(variants)), "strict-credit variant IDs are not unique sorted order")
    _require(len(semantics) == len(set(semantics)), "strict-credit semantic identities are not unique")
    _require(origins == Counter({"5.0": 400, "5.2": 600, "5.5": 425}), "strict-credit origin partition drifted")

    _require(len(corrections) == 1, "strict-credit correction denominator drifted")
    correction = corrections[0]
    corrected_id = correction.get("stage_claim_id")
    _require(
        corrected_id == "S5-CLM-00005311"
        and correction.get("variant_id") == "ATV-00005311"
        and correction.get("disposition") == "strict_credit_revoked"
        and correction.get("effective_release") == "5.2"
        and correction.get("grants_strict_conjecture_credit") is False
        and corrected_id not in credit_by_id,
        "strict-credit correction is invalid",
    )
    corrected_record = catalog_index.get(str(corrected_id))
    _require(isinstance(corrected_record, dict), "strict-credit correction references a missing record")
    _require(
        correction.get("parent_record_sha256") == _digest(_canonical(corrected_record)),
        "strict-credit correction record hash is stale",
    )

    syntactic_conjectures = {
        stage_id
        for stage_id, row in catalog_index.items()
        if open_predicate(row) and row.get("current_claim_kind") == "conjecture"
    }
    _require(
        set(ids) == syntactic_conjectures - {str(corrected_id)},
        "strict credits are not the exact conjecture set after explicit corrections",
    )
    _require(
        all(catalog_index[stage_id].get("current_claim_kind") != "open_problem" for stage_id in ids),
        "an open_problem was counted as a strict conjecture",
    )

    expected_counts = {
        "credit_corrections": 1,
        "effective_parent_credits": 1_000,
        "origin_5_2_credits": 600,
        "origin_5_5_credits": 425,
        "effective_strict_credits": 1_425,
        "stage5_5_0_baseline_strict_credits": 401,
        "net_strict_increase_after_5_0": 1_024,
    }
    _require(document.get("counts") == expected_counts, "strict-ledger count reconciliation drifted")
    origin_5_5 = [credit for credit in credits if credit.get("origin_release") == "5.5"]
    expected_digests = {
        "effective_s5_id_set_sha256": _set_digest(ids),
        "effective_variant_id_set_sha256": _set_digest(variants),
        "origin_5_5_s5_id_set_sha256": _set_digest(str(row["stage_claim_id"]) for row in origin_5_5),
        "origin_5_5_semantic_key_set_sha256": _set_digest(str(row["semantic_key"]) for row in origin_5_5),
    }
    _require(document.get("set_digests") == expected_digests, "strict-ledger set digests are stale")
    binding = manifest.get("strict_credit_binding")
    _require(isinstance(binding, dict), "manifest strict-credit binding is malformed")
    _require(
        binding.get("strict_ledger_authority_sha256") == document.get("authority_sha256")
        and binding.get("effective_credits") == len(ids)
        and binding.get("new_credits") == 0
        and binding.get("strict_credit_set_sha256") == expected_digests,
        "manifest strict-credit binding differs from the validated ledger",
    )
    return ids, credit_by_id


@dataclass
class ReleaseBundle:
    root: Path
    manifest: dict[str, Any]
    manifest_file_sha256: str
    artifact_file_sha256: dict[str, str]
    catalog_records: list[dict[str, Any]]
    catalog_index: dict[str, dict[str, Any]]
    statement_views: dict[str, StatementView]
    theorem_ids: list[str]
    open_ids: list[str]
    strict_ids: list[str]
    strict_credit_by_id: dict[str, dict[str, Any]]


def _load_release(root: Path, manifest_bytes: bytes) -> ReleaseBundle:
    release_dir = _safe_path(root, RELEASE_REL, file=False)
    entries = list(release_dir.iterdir())
    _require(
        all(path.is_file() and not path.is_symlink() for path in entries),
        "release 5.6 contains a non-regular or symlinked entry",
    )
    observed_names = {path.name for path in entries}
    _require(observed_names == ALL_RELEASE_FILES, f"release 5.6 file set drifted: {sorted(observed_names)}")

    manifest = parse_document_bytes(manifest_bytes, MANIFEST_NAME)
    bindings = validate_manifest(manifest)
    artifact_hashes: dict[str, str] = {}
    catalog_records: list[dict[str, Any]] | None = None
    catalog_index: dict[str, dict[str, Any]] | None = None
    statement_views: dict[str, StatementView] | None = None
    theorem_ids: list[str] | None = None
    open_ids: list[str] | None = None
    strict_ids: list[str] | None = None
    strict_credit_by_id: dict[str, dict[str, Any]] | None = None
    catalog_inputs: Any = None

    parent_path = _safe_path(root, PARENT_STRICT_REL)
    parent_bytes = parent_path.read_bytes()
    parent_strict = parse_document_bytes(parent_bytes, PARENT_STRICT_REL.as_posix())

    for name in sorted(RELEASE_FILES):
        path = _safe_path(root, RELEASE_REL / name)
        raw = path.read_bytes()
        binding = bindings[name]
        actual_sha = _digest(raw)
        _require(actual_sha == binding["sha256"], f"manifest artifact hash differs: {name}")
        _require(len(raw) == binding["size_bytes"], f"manifest artifact size differs: {name}")
        document = parse_document_bytes(raw, name)
        verify_seal(document, name)
        _require(document.get("release") == RELEASE, f"{name} release marker drifted")
        _require(_primary_rows(name, document) == binding["row_count"], f"manifest row count differs: {name}")
        artifact_hashes[name] = actual_sha

        if name == CATALOG_NAME:
            catalog_records, catalog_index, statement_views = validate_catalog(document)
            catalog_inputs = document.get("authoritative_inputs")
        elif name in {THEOREM_NAME, OPEN_NAME}:
            _require(catalog_records is not None, f"{name} loaded before catalog")
            _require(document.get("authoritative_inputs") == catalog_inputs, f"{name} authority inputs differ from catalog")
            ids = validate_projection(
                name,
                document,
                catalog_records,
                bucket="theorem" if name == THEOREM_NAME else "open",
            )
            if name == THEOREM_NAME:
                theorem_ids = ids
            else:
                open_ids = ids
        elif name == STRICT_NAME:
            _require(catalog_index is not None, f"{STRICT_NAME} loaded before catalog")
            _require(
                _digest(parent_bytes) == document.get("parent_strict_ledger_file_sha256"),
                "parent strict-ledger file hash binding drifted",
            )
            strict_ids, strict_credit_by_id = validate_strict_ledger(
                document, catalog_index, manifest, parent_strict
            )

    _require(
        all(
            value is not None
            for value in (
                catalog_records,
                catalog_index,
                statement_views,
                theorem_ids,
                open_ids,
                strict_ids,
                strict_credit_by_id,
            )
        ),
        "release did not yield all readable authorities",
    )
    _require(len(theorem_ids) == 3_500 and len(open_ids) == 2_025 and len(strict_ids) == 1_425, "readable member denominator drifted")
    return ReleaseBundle(
        root=root,
        manifest=dict(manifest),
        manifest_file_sha256=_digest(manifest_bytes),
        artifact_file_sha256=artifact_hashes,
        catalog_records=catalog_records,
        catalog_index=catalog_index,
        statement_views=statement_views,
        theorem_ids=theorem_ids,
        open_ids=open_ids,
        strict_ids=strict_ids,
        strict_credit_by_id=strict_credit_by_id,
    )


def load_release(repo_root: Path | None = None) -> ReleaseBundle:
    root = _repo_root(repo_root or Path(__file__).resolve().parents[4])
    manifest_path = _safe_path(root, RELEASE_REL / MANIFEST_NAME)
    with manifest_path.open("rb") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_SH)
        return _load_release(root, stream.read())


def _inline(value: Any) -> str:
    text = " ".join(str(value).split())
    text = html.escape(text, quote=False)
    escaped: list[str] = []
    for character in text:
        if character in "\\`*_{}[]()#+-.!|":
            escaped.append("\\" + character)
        else:
            escaped.append(character)
    return "".join(escaped)


def _fenced(text: str, language: str) -> str:
    runs = [len(match.group(0)) for match in re.finditer(r"`+", text)]
    fence = "`" * max(3, (max(runs) + 1) if runs else 3)
    payload = text if text.endswith("\n") else text + "\n"
    return f"{fence}{language}\n{payload}{fence}\n"


def _record_markdown(
    record: Mapping[str, Any],
    view: StatementView,
    credit: Mapping[str, Any] | None = None,
) -> str:
    stage_id = str(record["stage_claim_id"])
    name = _inline(record["display_name"])
    parts = [
        f"## {stage_id} — {name}\n\n",
        f"- ID：`{stage_id}`\n",
        f"- 名称 / Name：{name}\n",
        f"- 类型 / Kind：`{record['current_claim_kind']}`\n",
        f"- 来源 / Source：`{record['source_id']}`\n",
        f"- 来源定位 / Source pointer：{_inline(view.source_pointer)}\n",
        f"- 来源版本 / Origin release：`{record['origin_release']}`\n",
        f"- 陈述形式 / Representation：{_inline(view.representation)}\n",
        f"- 权利边界 / Rights boundary：{_inline(view.rights_boundary)}\n",
        "- 归属 / Attribution：" + "; ".join(_inline(value) for value in view.attribution) + "\n",
    ]
    if credit is not None:
        parts.append(f"- 严格猜想额度 / Strict credit：`{credit['credit_source_branch']}`\n")
    parts.extend(
        [
            "\n### 数学或形式化陈述 / Mathematical or formal statement\n\n",
            _fenced(view.text, view.language),
            "\n",
        ]
    )
    return "".join(parts)


def _counts_table(manifest: Mapping[str, Any]) -> str:
    keys = (
        "catalog_records",
        "cumulative_theorems",
        "cumulative_open_claims",
        "effective_strict_conjecture_credits",
        "origin_theorems",
        "origin_open_claims",
        "origin_strict_conjectures",
    )
    lines = ["| Metric | Count |\n", "|---|---:|\n"]
    counts = manifest["counts"]
    for key in keys:
        lines.append(f"| `{key}` | {counts[key]} |\n")
    return "".join(lines)


def _header(bundle: ReleaseBundle, kind: str, count: int) -> str:
    titles = {
        "theorem": "Stage5 数学定理清单 / Stage5 Mathematics Theorem List",
        "open": "Stage5 数学开放命题清单 / Stage5 Mathematics Open-Claim List",
        "strict": "Stage5 数学严格猜想清单 / Stage5 Mathematics Strict Conjecture List",
    }
    authorities = {
        "theorem": THEOREM_NAME,
        "open": OPEN_NAME,
        "strict": STRICT_NAME,
    }
    return (
        f"# {titles[kind]}\n\n"
        "> 由 `render_math_catalog_v5_6.py` 从已封印 JSON release 生成；请勿手工编辑。  \n"
        "> Generated from the sealed JSON release by `render_math_catalog_v5_6.py`; do not edit by hand.\n\n"
        f"- 发布 / Release：`{RELEASE}`\n"
        f"- 发布根 / Release root：`sha256:{bundle.manifest['release_root_sha256']}`\n"
        f"- 成员权威 / Membership authority：`{authorities[kind]}`\n"
        f"- 精确成员数 / Exact members：**{count}**\n\n"
        "## 封印计数 / Sealed counts\n\n"
        + _counts_table(bundle.manifest)
        + "\n"
    )


def _render_theorem(bundle: ReleaseBundle) -> bytes:
    quality = bundle.manifest["quality_qualification"]["origin_5_6"]
    parts = [
        _header(bundle, "theorem", len(bundle.theorem_ids)),
        "## 定理质量边界 / Theorem-quality boundary\n\n",
        "- 5.6 新增 1,000 个经固定 mathlib 环境内核检查且不使用 `sorry` 的形式命题身份。\n",
        f"- 源语法：`theorem`={quality['source_syntax_theorem']}，`lemma`={quality['source_syntax_lemma']}；每条均按定理记录计数。\n",
        f"- 文档信号：单声明 docstring={quality['selected_individual_declaration_docstring']}，module Main-result={quality['selected_module_main_result_description']}。\n",
        "- 不声称这 1,000 条已经完成人工语义唯一性审查，也不声称它们是独立的全局重要性排名。\n",
        "- 继承记录保留各自原始证据层级；源标记不等于本仓库逐条独立重放证明。\n\n",
        "## 精确成员 / Exact members\n\n",
    ]
    for stage_id in bundle.theorem_ids:
        parts.append(_record_markdown(bundle.catalog_index[stage_id], bundle.statement_views[stage_id]))
    return "".join(parts).encode("utf-8")


def _render_open(bundle: ReleaseBundle) -> bytes:
    kinds = Counter(bundle.catalog_index[stage_id]["current_claim_kind"] for stage_id in bundle.open_ids)
    parts = [
        _header(bundle, "open", len(bundle.open_ids)),
        "## 开放命题口径 / Open-claim boundary\n\n",
        f"- 语法 `conjecture`：{kinds['conjecture']}。\n",
        f"- `open_problem`：{kinds['open_problem']}；它们不计入严格猜想。\n",
        "- 严格猜想成员由 `Strict_Conjecture_Ledger.json` 的有效 credit 唯一决定，不由名称或宽口径类别猜测。\n",
        "- 开放状态和截止日保留各固定来源/审核证据的边界；不冒充全部逐条完成当前文献调查。\n\n",
        "## 精确成员 / Exact members\n\n",
    ]
    for stage_id in bundle.open_ids:
        parts.append(_record_markdown(bundle.catalog_index[stage_id], bundle.statement_views[stage_id]))
    return "".join(parts).encode("utf-8")


def _render_strict(bundle: ReleaseBundle) -> bytes:
    open_problem_count = sum(
        bundle.catalog_index[stage_id]["current_claim_kind"] == "open_problem"
        for stage_id in bundle.open_ids
    )
    parts = [
        _header(bundle, "strict", len(bundle.strict_ids)),
        "## 严格额度对账 / Strict-credit reconciliation\n\n",
        "- Stage5 5.0 语法猜想基线：401；显式撤销旧 credit：1。\n",
        "- 5.2 新增有效 strict credits：600；5.5 新增：425；最终有效成员：1,425。\n",
        f"- `open_problem` records：{open_problem_count}；全部明确排除在 strict-credit 成员集外。\n",
        "- `S5-CLM-00005311` 的旧 strict credit 继续按显式 correction 撤销；记录本身未被改写。\n\n",
        "## 精确成员 / Exact members\n\n",
    ]
    for stage_id in bundle.strict_ids:
        parts.append(
            _record_markdown(
                bundle.catalog_index[stage_id],
                bundle.statement_views[stage_id],
                bundle.strict_credit_by_id[stage_id],
            )
        )
    return "".join(parts).encode("utf-8")


def render_documents(bundle: ReleaseBundle) -> dict[str, bytes]:
    result = {
        "Theorem_List.md": _render_theorem(bundle),
        "Open_Claim_List.md": _render_open(bundle),
        "Strict_Conjecture_List.md": _render_strict(bundle),
    }
    _require(tuple(result) == OUTPUT_FILES, "readable output denominator/order drifted")
    for name, payload in result.items():
        _require(payload and payload.endswith(b"\n"), f"{name} is empty or lacks its final LF")
        try:
            payload.decode("utf-8")
        except UnicodeError as error:
            raise RenderError(f"{name} is not valid UTF-8") from error
    return result


def _release_unchanged(bundle: ReleaseBundle) -> None:
    manifest_path = _safe_path(bundle.root, RELEASE_REL / MANIFEST_NAME)
    _require(_digest(manifest_path.read_bytes()) == bundle.manifest_file_sha256, "release manifest changed during rendering")
    for name, expected_sha in bundle.artifact_file_sha256.items():
        path = _safe_path(bundle.root, RELEASE_REL / name)
        _require(_digest(path.read_bytes()) == expected_sha, f"release artifact changed during rendering: {name}")


def _output_directory(root: Path, *, create: bool) -> Path:
    path = root / READABLE_REL
    if path.exists() or path.is_symlink():
        _require(not path.is_symlink() and path.is_dir(), f"readable path is not a real directory: {READABLE_REL}")
        resolved = path.resolve()
        _require(resolved == path.absolute(), f"readable directory is aliased: {READABLE_REL}")
        return resolved
    _require(create, f"readable directory is missing: {READABLE_REL}")
    parent = root / READABLE_REL.parent
    _require(parent.is_dir() and not parent.is_symlink(), f"readable parent is unsafe: {READABLE_REL.parent}")
    path.mkdir(mode=0o755)
    return path.resolve()


def check_readable(bundle: ReleaseBundle, documents: Mapping[str, bytes] | None = None) -> bool:
    expected = dict(documents) if documents is not None else render_documents(bundle)
    try:
        directory = _output_directory(bundle.root, create=False)
    except RenderError as error:
        print(f"STALE {error}", file=sys.stderr)
        return False
    entries = list(directory.iterdir())
    if not all(path.is_file() and not path.is_symlink() for path in entries):
        print("STALE readable/5.6 contains a non-regular or symlinked entry", file=sys.stderr)
        return False
    names = {path.name for path in entries}
    if names != set(OUTPUT_FILES):
        print(f"STALE readable/5.6 file set differs: {sorted(names)}", file=sys.stderr)
        return False
    current = True
    for name in OUTPUT_FILES:
        path = directory / name
        observed = path.read_bytes()
        if observed != expected[name]:
            current = False
            mismatch = next(
                (index for index, pair in enumerate(zip(observed, expected[name])) if pair[0] != pair[1]),
                min(len(observed), len(expected[name])),
            )
            print(f"STALE {READABLE_REL / name}: first mismatch at byte {mismatch}", file=sys.stderr)
    _release_unchanged(bundle)
    return current


def _atomic_write(path: Path, payload: bytes) -> bool:
    if path.exists():
        _require(path.is_file() and not path.is_symlink(), f"refusing unsafe output target: {path}")
        if path.read_bytes() == payload:
            return False
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()
    return True


def write_readable(bundle: ReleaseBundle, documents: Mapping[str, bytes] | None = None) -> list[Path]:
    rendered = dict(documents) if documents is not None else render_documents(bundle)
    _require(set(rendered) == set(OUTPUT_FILES), "write output denominator drifted")
    directory = _output_directory(bundle.root, create=True)
    _release_unchanged(bundle)
    written: list[Path] = []
    for name in OUTPUT_FILES:
        _release_unchanged(bundle)
        path = directory / name
        if _atomic_write(path, rendered[name]):
            written.append(path)
    _release_unchanged(bundle)
    _require(check_readable(bundle, rendered), "written readable projections failed byte verification")
    return written


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--check", action="store_true", help="validate and compare without writing")
    parser.add_argument("--quiet", action="store_true", help="suppress PASS/CURRENT output")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        root = _repo_root(args.repo_root)
        manifest_path = _safe_path(root, RELEASE_REL / MANIFEST_NAME)
        with manifest_path.open("rb") as stream:
            fcntl.flock(stream.fileno(), fcntl.LOCK_SH if args.check else fcntl.LOCK_EX)
            bundle = _load_release(root, stream.read())
            rendered = render_documents(bundle)
            if args.check:
                if not check_readable(bundle, rendered):
                    return 1
                if not args.quiet:
                    print(
                        "PASS Stage5 readable projections 5.6 "
                        f"theorem={len(bundle.theorem_ids)} open={len(bundle.open_ids)} "
                        f"strict={len(bundle.strict_ids)} root={bundle.manifest['release_root_sha256']}"
                    )
                return 0
            written = write_readable(bundle, rendered)
            if not args.quiet:
                if written:
                    for path in written:
                        print(f"WROTE {path.relative_to(root)}")
                else:
                    print(f"CURRENT Stage5 readable projections 5.6 root={bundle.manifest['release_root_sha256']}")
            return 0
    except (RenderError, OSError, KeyError, TypeError, ValueError, IndexError) as error:
        print(f"ERROR render_math_catalog_v5_6: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
