#!/usr/bin/env python3
"""Build the immutable Stage4 predecessor-import receipt used by Stage5.

The receipt is a read-only bridge.  It authenticates the sealed Stage4
manifest, all thirteen materialized Stage4 release outputs, the common source
inventory embedded in the JSON authorities, and the independent Stage4
checker result.  It then emits a directly consumable ATV -> S4-CLM crosswalk,
the historical THM alias crosswalk, and the complete redirect/split rows.

This module intentionally uses only the Python standard library and does not
import ``generate_claim_catalog_v4.py``.  ``--check`` performs no writes and
compares the expected canonical JSON bytes with the committed receipt.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Iterable, Iterator, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
V4_DIR_RELATIVE = Path("Docs/catalog/v4")
MANIFEST_RELATIVE = V4_DIR_RELATIVE / "Stage4_Curation_Manifest_v4.json"
CHECKER_RELATIVE = Path("scripts/check_claim_catalog_v4.py")
OUTPUT_RELATIVE = Path("Docs/catalog/v5/V4_Import_Receipt_v5.json")

# These are the thirteen materialized release outputs, not the curation
# manifest, README, or input fragments.  The JSON artifacts identify
# themselves by the same basename and share one authoritative-input snapshot.
OFFICIAL_OUTPUTS: tuple[tuple[str, Path, str], ...] = (
    ("source_records", V4_DIR_RELATIVE / "Source_Records_v4.json", "json"),
    ("claim_id_registry", V4_DIR_RELATIVE / "Claim_ID_Registry_v4.json", "json"),
    (
        "stage4_claim_id_registry",
        V4_DIR_RELATIVE / "Stage4_Claim_ID_Registry_v4.json",
        "json",
    ),
    (
        "claim_id_migration",
        V4_DIR_RELATIVE / "Claim_ID_Migration_v2_to_v4.json",
        "json",
    ),
    (
        "candidate_dispositions",
        V4_DIR_RELATIVE / "Candidate_Dispositions_v4.json",
        "json",
    ),
    (
        "repair_proposal_dispositions",
        V4_DIR_RELATIVE / "Repair_Proposal_Dispositions_v4.json",
        "json",
    ),
    ("claim_catalog", V4_DIR_RELATIVE / "Claim_Catalog_v4.json", "json"),
    ("theorem_list_json", V4_DIR_RELATIVE / "Theorem_List_v4.json", "json"),
    ("theorem_list_md", V4_DIR_RELATIVE / "Theorem_List_v4.md", "markdown"),
    (
        "open_list_json",
        V4_DIR_RELATIVE / "Conjecture_Hypothesis_Open_List_v4.json",
        "json",
    ),
    (
        "open_list_md",
        V4_DIR_RELATIVE / "Conjecture_Hypothesis_Open_List_v4.md",
        "markdown",
    ),
    ("status_index_json", V4_DIR_RELATIVE / "Status_Index_v4.json", "json"),
    ("status_index_md", V4_DIR_RELATIVE / "Status_Index_v4.md", "markdown"),
)

JSON_ROLES = tuple(role for role, _path, kind in OFFICIAL_OUTPUTS if kind == "json")
ATV_RE = re.compile(r"^ATV-([0-9]{8})$")
ATO_RE = re.compile(r"^ATO-([0-9]{8})$")
ATS_RE = re.compile(r"^ATS-([0-9]{8})$")
ATF_RE = re.compile(r"^ATF-([0-9]{8})$")
S4_RE = re.compile(r"^S4-CLM-([0-9]{8})$")
THM_RE = re.compile(r"^THM-[MPC]-[0-9]{4}$")
REDIRECT_RE = re.compile(r"^REDIRECT-[0-9A-F]{24}$")
SPLIT_RE = re.compile(r"^SPLIT-[0-9A-F]{24}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ImportReceiptError(RuntimeError):
    """Fail-closed error while authenticating or importing Stage4."""


def canonical_json_bytes(value: Any) -> bytes:
    """Return the canonical JSON representation used by the receipt seal."""

    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ImportReceiptError(f"value is not canonical-JSON serializable: {exc}") from exc


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def stable_digest(namespace: str, value: Any) -> str:
    return sha256_bytes(namespace.encode("utf-8") + b"\0" + canonical_json_bytes(value))


def _reject_constant(value: str) -> None:
    raise ImportReceiptError(f"non-finite JSON number is forbidden: {value}")


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ImportReceiptError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def strict_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    try:
        text = payload.decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ImportReceiptError(f"invalid JSON in {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ImportReceiptError(f"{label} must contain one JSON object")
    return value


def _safe_repo_file(root: Path, relative: Path | str) -> Path:
    pure = Path(relative)
    if pure.is_absolute() or not pure.parts or ".." in pure.parts:
        raise ImportReceiptError(f"unsafe repository-relative path: {str(relative)!r}")
    resolved_root = root.resolve()
    resolved = (resolved_root / pure).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ImportReceiptError(f"path escapes repository root: {str(relative)!r}") from exc
    if not resolved.is_file():
        raise ImportReceiptError(f"required file is missing: {pure.as_posix()}")
    return resolved


def _read_binding(root: Path, relative: Path | str) -> tuple[dict[str, Any], bytes]:
    pure = Path(relative)
    path = _safe_repo_file(root, pure)
    payload = path.read_bytes()
    return (
        {
            "path": pure.as_posix(),
            "sha256": sha256_bytes(payload),
            "size_bytes": len(payload),
        },
        payload,
    )


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ImportReceiptError(f"{label} must be an object")
    return value


def _require_rows(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise ImportReceiptError(f"{label} must be an array of objects")
    return value


def _require_string(value: Any, label: str, pattern: re.Pattern[str] | None = None) -> str:
    if not isinstance(value, str) or not value:
        raise ImportReceiptError(f"{label} must be a non-empty string")
    if pattern is not None and pattern.fullmatch(value) is None:
        raise ImportReceiptError(f"{label} has invalid syntax: {value!r}")
    return value


def _require_nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ImportReceiptError(f"{label} must be a non-negative integer")
    return value


def _unique_index(
    rows: Iterable[dict[str, Any]],
    key: str,
    label: str,
    pattern: re.Pattern[str] | None = None,
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(rows):
        identifier = _require_string(row.get(key), f"{label}[{index}].{key}", pattern)
        if identifier in result:
            raise ImportReceiptError(f"{label} duplicates {key}={identifier}")
        result[identifier] = row
    return result


def _artifact_authority(document: Mapping[str, Any]) -> str:
    body = {key: value for key, value in document.items() if key != "authority_sha256"}
    return sha256_bytes(canonical_json_bytes(body))


def _validate_json_authority(
    role: str,
    relative: Path,
    document: dict[str, Any],
) -> dict[str, Any]:
    artifact = _require_string(document.get("artifact"), f"{role}.artifact")
    if artifact != relative.name:
        raise ImportReceiptError(
            f"{relative.as_posix()} artifact field {artifact!r} does not match its filename"
        )
    schema = _require_string(document.get("schema_version"), f"{role}.schema_version")
    declared = _require_string(
        document.get("authority_sha256"), f"{role}.authority_sha256", SHA256_RE
    )
    computed = _artifact_authority(document)
    if declared != computed:
        raise ImportReceiptError(f"{relative.as_posix()} has a stale authority_sha256")
    counts = _require_object(document.get("counts"), f"{role}.counts")
    return {
        "schema_version": schema,
        "declared_authority_sha256": declared,
        "counts": counts,
    }


def _validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    schema = _require_string(manifest.get("schema_version"), "manifest.schema_version")
    if schema != "awesome-theorems/stage4-curation-manifest/4.0":
        raise ImportReceiptError(f"unsupported Stage4 manifest schema: {schema!r}")
    if manifest.get("stage") != "Stage4":
        raise ImportReceiptError("manifest.stage must be 'Stage4'")
    scope = _require_object(manifest.get("scope"), "manifest.scope")
    policy = _require_object(manifest.get("policy"), "manifest.policy")
    if policy.get("release_state") != "sealed":
        raise ImportReceiptError("Stage4 predecessor manifest is not sealed")
    fragments = manifest.get("fragments")
    if not isinstance(fragments, list) or not fragments:
        raise ImportReceiptError("manifest.fragments must be a non-empty array")
    normalized_fragments: list[str] = []
    for index, value in enumerate(fragments):
        item = _require_string(value, f"manifest.fragments[{index}]")
        pure = Path(item)
        if pure.is_absolute() or ".." in pure.parts:
            raise ImportReceiptError(f"unsafe manifest fragment path: {item!r}")
        normalized_fragments.append(pure.as_posix())
    if len(normalized_fragments) != len(set(normalized_fragments)):
        raise ImportReceiptError("manifest.fragments contains duplicates")
    return {
        "schema_version": schema,
        "stage": "Stage4",
        "review_date": _require_string(manifest.get("review_date"), "manifest.review_date"),
        "completion_boundary": _require_string(
            scope.get("completion_boundary"), "manifest.scope.completion_boundary"
        ),
        "baseline_catalog_semantics": _require_string(
            scope.get("baseline_catalog_semantics"),
            "manifest.scope.baseline_catalog_semantics",
        ),
        "release_scope": _require_string(
            policy.get("release_scope"), "manifest.policy.release_scope"
        ),
        "stage_number_format": _require_string(
            policy.get("stage_number_format"), "manifest.policy.stage_number_format"
        ),
        "fragments": normalized_fragments,
    }


def _validate_common_source_inventory(
    root: Path,
    json_documents: Mapping[str, dict[str, Any]],
    manifest_fragments: Sequence[str],
) -> tuple[list[dict[str, Any]], str]:
    inventories: list[list[dict[str, Any]]] = []
    digests: list[str] = []
    for role in JSON_ROLES:
        document = json_documents[role]
        rows = _require_rows(document.get("authoritative_inputs"), f"{role}.authoritative_inputs")
        normalized: list[dict[str, Any]] = []
        seen: set[str] = set()
        for index, row in enumerate(rows):
            if set(row) != {"path", "sha256", "size_bytes"}:
                raise ImportReceiptError(
                    f"{role}.authoritative_inputs[{index}] has an unexpected shape"
                )
            path = _require_string(row.get("path"), f"{role}.authoritative_inputs[{index}].path")
            if path in seen:
                raise ImportReceiptError(f"{role}.authoritative_inputs duplicates {path}")
            seen.add(path)
            digest = _require_string(
                row.get("sha256"), f"{role}.authoritative_inputs[{index}].sha256", SHA256_RE
            )
            size = _require_nonnegative_int(
                row.get("size_bytes"), f"{role}.authoritative_inputs[{index}].size_bytes"
            )
            observed, _payload = _read_binding(root, path)
            expected = {"path": path, "sha256": digest, "size_bytes": size}
            if observed != expected:
                raise ImportReceiptError(
                    f"authoritative input bytes drifted for {path}: "
                    f"declared={expected!r}, observed={observed!r}"
                )
            normalized.append(expected)
        declared_digest = _require_string(
            document.get("authoritative_inputs_sha256"),
            f"{role}.authoritative_inputs_sha256",
            SHA256_RE,
        )
        computed_digest = stable_digest(
            "awesome-theorems/stage4-authoritative-inputs/v4", normalized
        )
        if declared_digest != computed_digest:
            raise ImportReceiptError(f"{role} has a stale authoritative_inputs_sha256")
        inventories.append(normalized)
        digests.append(declared_digest)

    first = inventories[0]
    if any(inventory != first for inventory in inventories[1:]):
        raise ImportReceiptError("Stage4 JSON outputs do not share one source inventory")
    if len(set(digests)) != 1:
        raise ImportReceiptError("Stage4 JSON outputs disagree on source-inventory authority")

    paths = {row["path"] for row in first}
    required = {MANIFEST_RELATIVE.as_posix(), *manifest_fragments}
    missing = sorted(required - paths)
    if missing:
        raise ImportReceiptError(
            f"Stage4 source inventory omits manifest/fragment paths: {missing!r}"
        )
    return first, digests[0]


def _count_matches(document: Mapping[str, Any], key: str, observed: int, label: str) -> None:
    counts = _require_object(document.get("counts"), f"{label}.counts")
    expected = _require_nonnegative_int(counts.get(key), f"{label}.counts.{key}")
    if expected != observed:
        raise ImportReceiptError(
            f"{label}.counts.{key}={expected} but direct row count is {observed}"
        )


def _build_identity_import(
    manifest: dict[str, Any],
    documents: Mapping[str, dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, int]]:
    source_document = documents["source_records"]
    registry = documents["claim_id_registry"]
    numbering = documents["stage4_claim_id_registry"]
    migration = documents["claim_id_migration"]
    catalog = documents["claim_catalog"]

    source_rows = _require_rows(source_document.get("records"), "Source_Records_v4.records")
    source_by_id = _unique_index(source_rows, "occurrence_id", "source records", ATO_RE)
    variants = _require_rows(registry.get("variants"), "Claim_ID_Registry_v4.variants")
    variant_by_id = _unique_index(variants, "variant_id", "registry variants", ATV_RE)
    senses = _require_rows(registry.get("senses"), "Claim_ID_Registry_v4.senses")
    _unique_index(senses, "sense_id", "registry senses", ATS_RE)
    families = _require_rows(registry.get("families"), "Claim_ID_Registry_v4.families")
    _unique_index(families, "family_id", "registry families", ATF_RE)

    variant_occurrences: set[str] = set()
    for variant_id, row in variant_by_id.items():
        occurrence_id = _require_string(
            row.get("bootstrap_occurrence_id"),
            f"registry variant {variant_id}.bootstrap_occurrence_id",
            ATO_RE,
        )
        if occurrence_id in variant_occurrences:
            raise ImportReceiptError(
                f"multiple Stage4 variants claim source occurrence {occurrence_id}"
            )
        variant_occurrences.add(occurrence_id)
    if variant_occurrences != set(source_by_id):
        raise ImportReceiptError("Stage4 variant/source-occurrence sets are not bijective")

    mapping_rows = _require_rows(numbering.get("mappings"), "Stage4 numbering mappings")
    mapping_by_variant = _unique_index(
        mapping_rows, "variant_id", "Stage4 numbering mappings", ATV_RE
    )
    stage_ids: set[str] = set()
    for variant_id, row in mapping_by_variant.items():
        stage_id = _require_string(
            row.get("stage_claim_id"), f"numbering {variant_id}.stage_claim_id", S4_RE
        )
        duplicate_stage_id = row.get("stage_id")
        if duplicate_stage_id != stage_id:
            raise ImportReceiptError(f"numbering {variant_id} has inconsistent stage_id fields")
        if stage_id in stage_ids:
            raise ImportReceiptError(f"Stage4 numbering duplicates {stage_id}")
        stage_ids.add(stage_id)
        ordinal = _require_nonnegative_int(row.get("ordinal"), f"numbering {variant_id}.ordinal")
        atv_match = ATV_RE.fullmatch(variant_id)
        stage_match = S4_RE.fullmatch(stage_id)
        assert atv_match is not None and stage_match is not None
        if ordinal < 1 or ordinal != int(atv_match.group(1)) or ordinal != int(stage_match.group(1)):
            raise ImportReceiptError(
                f"Stage4 ordinal rule fails for {variant_id} -> {stage_id}"
            )
        registry_lifecycle = variant_by_id[variant_id].get("lifecycle")
        if row.get("lifecycle") != registry_lifecycle:
            raise ImportReceiptError(f"numbering lifecycle drift for {variant_id}")
    if set(mapping_by_variant) != set(variant_by_id):
        raise ImportReceiptError("Stage4 numbering is not a bijection over all registry ATV IDs")

    migration_rows = _require_rows(migration.get("migrations"), "Stage4 migration rows")
    migration_by_variant = _unique_index(
        migration_rows, "variant_id", "Stage4 migration rows", ATV_RE
    )
    if set(migration_by_variant) != set(variant_by_id):
        raise ImportReceiptError("Stage4 migration rows do not cover every ATV exactly once")

    catalog_rows = _require_rows(catalog.get("records"), "Claim_Catalog_v4.records")
    catalog_by_variant = _unique_index(catalog_rows, "variant_id", "catalog records", ATV_RE)
    if set(catalog_by_variant) != set(variant_by_id):
        raise ImportReceiptError("Stage4 catalog records do not cover every registry ATV")

    crosswalk: list[dict[str, Any]] = []
    carry = 0
    additions = 0
    for variant_id in sorted(variant_by_id, key=lambda value: int(value[-8:])):
        mapping = mapping_by_variant[variant_id]
        migration_row = migration_by_variant[variant_id]
        catalog_row = catalog_by_variant[variant_id]
        stage_id = mapping["stage_claim_id"]
        if migration_row.get("stage_claim_id") != stage_id or migration_row.get("stage_id") != stage_id:
            raise ImportReceiptError(f"migration numbering drift for {variant_id}")
        if catalog_row.get("stage_claim_id") != stage_id or catalog_row.get("stage_id") != stage_id:
            raise ImportReceiptError(f"catalog numbering drift for {variant_id}")
        action = migration_row.get("action")
        if action == "carry":
            carry += 1
            if migration_row.get("v2_variant_id") != variant_id:
                raise ImportReceiptError(f"carry row {variant_id} lacks its exact v2 identity")
        elif action == "new":
            additions += 1
            if migration_row.get("v2_variant_id") is not None:
                raise ImportReceiptError(f"new row {variant_id} falsely names a v2 identity")
        else:
            raise ImportReceiptError(f"migration row {variant_id} has invalid action {action!r}")
        resolution = _require_object(
            migration_row.get("current_resolution"),
            f"migration {variant_id}.current_resolution",
        )
        targets = resolution.get("target_stage_claim_ids")
        if not isinstance(targets, list) or not targets:
            raise ImportReceiptError(
                f"migration {variant_id}.current_resolution lacks terminal targets"
            )
        for index, target in enumerate(targets):
            _require_string(target, f"migration {variant_id}.terminal[{index}]", S4_RE)
            if target not in stage_ids:
                raise ImportReceiptError(
                    f"migration {variant_id} resolves outside Stage4 numbering: {target}"
                )
        crosswalk.append(
            {
                "atv_id": variant_id,
                "s4_claim_id": stage_id,
                "ordinal": mapping["ordinal"],
                "lifecycle": mapping.get("lifecycle"),
                "curation_key": mapping.get("curation_key"),
                "migration_action": action,
                "v2_variant_id": migration_row.get("v2_variant_id"),
                "current_resolution": resolution,
            }
        )

    alias_rows = _require_rows(registry.get("legacy_aliases"), "registry legacy aliases")
    registry_aliases = _unique_index(alias_rows, "alias_id", "registry legacy aliases", THM_RE)
    migration_alias_rows = _require_rows(
        migration.get("legacy_alias_migrations"), "migration legacy aliases"
    )
    migration_aliases = _unique_index(
        migration_alias_rows, "alias_id", "migration legacy aliases", THM_RE
    )
    if set(registry_aliases) != set(migration_aliases):
        raise ImportReceiptError("registry and migration historical THM alias sets differ")
    alias_crosswalk: list[dict[str, Any]] = []
    for alias_id in sorted(registry_aliases):
        registry_row = registry_aliases[alias_id]
        migration_row = migration_aliases[alias_id]
        target = _require_string(
            registry_row.get("target_variant_id"),
            f"legacy alias {alias_id}.target_variant_id",
            ATV_RE,
        )
        if target not in mapping_by_variant:
            raise ImportReceiptError(f"legacy alias {alias_id} targets unknown {target}")
        stage_id = mapping_by_variant[target]["stage_claim_id"]
        if (
            migration_row.get("historical_target_variant_id") != target
            or migration_row.get("historical_stage_claim_id") != stage_id
            or migration_row.get("rebound") is not False
        ):
            raise ImportReceiptError(f"historical alias migration drift for {alias_id}")
        alias_crosswalk.append(
            {
                "thm_alias_id": alias_id,
                "historical_atv_id": target,
                "historical_s4_claim_id": stage_id,
                "rebound": False,
            }
        )

    redirects = _require_rows(registry.get("redirects"), "registry redirects")
    redirect_by_id = _unique_index(redirects, "redirect_id", "registry redirects", REDIRECT_RE)
    for redirect_id, row in redirect_by_id.items():
        source = _require_string(
            row.get("source_variant_id"), f"redirect {redirect_id}.source", ATV_RE
        )
        target = _require_string(
            row.get("target_variant_id"), f"redirect {redirect_id}.target", ATV_RE
        )
        if source not in variant_by_id or target not in variant_by_id:
            raise ImportReceiptError(f"redirect {redirect_id} has an unknown endpoint")
        if row.get("default_child") is not None or row.get("evidence_inherited") is not False:
            raise ImportReceiptError(f"redirect {redirect_id} violates no-inheritance policy")

    splits = _require_rows(registry.get("splits"), "registry splits")
    split_by_id = _unique_index(splits, "split_id", "registry splits", SPLIT_RE)
    split_child_edges = 0
    for split_id, row in split_by_id.items():
        source = _require_string(
            row.get("source_variant_id"), f"split {split_id}.source", ATV_RE
        )
        if source not in variant_by_id:
            raise ImportReceiptError(f"split {split_id} has an unknown source")
        children = row.get("child_variant_ids")
        if not isinstance(children, list) or not children:
            raise ImportReceiptError(f"split {split_id} has no children")
        if len(children) != len(set(children)):
            raise ImportReceiptError(f"split {split_id} repeats a child")
        for index, child in enumerate(children):
            child_id = _require_string(child, f"split {split_id}.child[{index}]", ATV_RE)
            if child_id not in variant_by_id:
                raise ImportReceiptError(f"split {split_id} has unknown child {child_id}")
        split_child_edges += len(children)
        if (
            row.get("default_child") is not None
            or row.get("default_child_id") is not None
            or row.get("evidence_inherited") is not False
        ):
            raise ImportReceiptError(f"split {split_id} violates no-default/no-inheritance policy")

    baseline = _require_object(
        _require_object(manifest.get("scope"), "manifest.scope").get("baseline_universe"),
        "manifest.scope.baseline_universe",
    )
    expected_aliases = _require_nonnegative_int(
        baseline.get("legacy_aliases"), "manifest baseline legacy_aliases"
    )
    expected_variants = _require_nonnegative_int(
        baseline.get("canonical_variants"), "manifest baseline canonical_variants"
    )
    expected_occurrences = _require_nonnegative_int(
        baseline.get("source_occurrences"), "manifest baseline source_occurrences"
    )
    expected_folded = _require_nonnegative_int(
        baseline.get("folded_occurrences"), "manifest baseline folded_occurrences"
    )
    if len(alias_crosswalk) != expected_aliases:
        raise ImportReceiptError("historical THM alias count disagrees with the sealed manifest")
    if carry != expected_variants or expected_variants != expected_occurrences:
        raise ImportReceiptError("baseline carry count disagrees with the sealed manifest")

    folded_occurrences = migration.get("folded_occurrence_ids")
    if not isinstance(folded_occurrences, list) or len(folded_occurrences) != expected_folded:
        raise ImportReceiptError("folded occurrence inventory disagrees with the sealed manifest")
    for index, value in enumerate(folded_occurrences):
        _require_string(value, f"folded_occurrence_ids[{index}]", ATO_RE)
    if len(folded_occurrences) != len(set(folded_occurrences)):
        raise ImportReceiptError("folded occurrence inventory contains duplicates")

    _count_matches(source_document, "allocated_occurrences", len(source_rows), "source records")
    _count_matches(registry, "variants_allocated", len(variants), "claim ID registry")
    _count_matches(registry, "senses_allocated", len(senses), "claim ID registry")
    _count_matches(registry, "families_allocated", len(families), "claim ID registry")
    _count_matches(registry, "legacy_aliases", len(alias_rows), "claim ID registry")
    _count_matches(registry, "redirects", len(redirects), "claim ID registry")
    _count_matches(registry, "splits", len(splits), "claim ID registry")
    _count_matches(numbering, "mappings", len(mapping_rows), "Stage4 numbering")
    _count_matches(migration, "migrations", len(migration_rows), "Stage4 migration")
    _count_matches(migration, "legacy_aliases", len(migration_alias_rows), "Stage4 migration")
    _count_matches(catalog, "records", len(catalog_rows), "claim catalog")

    theorem_rows = _require_rows(documents["theorem_list_json"].get("records"), "theorem list")
    open_rows = _require_rows(documents["open_list_json"].get("records"), "open list")
    status_rows = _require_rows(documents["status_index_json"].get("records"), "status index")
    candidate_rows = _require_rows(
        documents["candidate_dispositions"].get("dispositions"), "candidate dispositions"
    )
    proposal_rows = _require_rows(
        documents["repair_proposal_dispositions"].get("dispositions"),
        "repair proposal dispositions",
    )
    _count_matches(documents["theorem_list_json"], "records", len(theorem_rows), "theorem list")
    _count_matches(documents["open_list_json"], "records", len(open_rows), "open list")
    _count_matches(documents["status_index_json"], "records", len(status_rows), "status index")
    _count_matches(
        documents["candidate_dispositions"], "total", len(candidate_rows), "candidate dispositions"
    )
    _count_matches(
        documents["repair_proposal_dispositions"],
        "total",
        len(proposal_rows),
        "repair proposal dispositions",
    )

    counts = {
        "source_occurrences": len(source_rows),
        "atv_variants": len(variants),
        "ats_senses": len(senses),
        "atf_families": len(families),
        "stage_claim_mappings": len(crosswalk),
        "baseline_carry": carry,
        "stage4_additions": additions,
        "historical_thm_aliases": len(alias_crosswalk),
        "folded_occurrences": len(folded_occurrences),
        "redirects": len(redirects),
        "splits": len(splits),
        "split_child_edges": split_child_edges,
        "candidate_dispositions": len(candidate_rows),
        "repair_proposal_dispositions": len(proposal_rows),
        "theorem_projection_records": len(theorem_rows),
        "open_projection_records": len(open_rows),
        "status_projection_records": len(status_rows),
    }
    identity_import = {
        "policy": {
            "predecessor_bytes_mutated": False,
            "historical_aliases_rebound": False,
            "stage4_number_reassigned": False,
            "semantic_or_truth_upgrade_implied": False,
            "split_default_child": None,
            "split_evidence_inherited": False,
        },
        "variant_stage_crosswalk": crosswalk,
        "historical_thm_alias_crosswalk": alias_crosswalk,
        "redirects": [redirect_by_id[key] for key in sorted(redirect_by_id)],
        "splits": [split_by_id[key] for key in sorted(split_by_id)],
        "folded_occurrence_ids": sorted(folded_occurrences),
    }
    identity_import["set_digests"] = {
        "variant_stage_crosswalk_sha256": sha256_bytes(canonical_json_bytes(crosswalk)),
        "historical_thm_alias_crosswalk_sha256": sha256_bytes(
            canonical_json_bytes(alias_crosswalk)
        ),
        "redirect_rows_sha256": sha256_bytes(
            canonical_json_bytes(identity_import["redirects"])
        ),
        "split_rows_sha256": sha256_bytes(canonical_json_bytes(identity_import["splits"])),
        "folded_occurrence_ids_sha256": sha256_bytes(
            canonical_json_bytes(identity_import["folded_occurrence_ids"])
        ),
    }
    return identity_import, counts


def _stream_binding(payload: bytes) -> dict[str, Any]:
    return {
        "sha256": sha256_bytes(payload),
        "size_bytes": len(payload),
        "text_utf8": payload.decode("utf-8"),
    }


def _run_checker(root: Path) -> dict[str, Any]:
    checker_binding, checker_bytes = _read_binding(root, CHECKER_RELATIVE)
    argv = ["python3", CHECKER_RELATIVE.as_posix(), "--require-complete"]
    completed = subprocess.run(
        [sys.executable, CHECKER_RELATIVE.as_posix(), "--require-complete"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        stdout = completed.stdout.decode("utf-8", errors="replace")
        stderr = completed.stderr.decode("utf-8", errors="replace")
        raise ImportReceiptError(
            "independent Stage4 checker failed "
            f"(exit={completed.returncode}, stdout={stdout!r}, stderr={stderr!r})"
        )
    # The receipt is canonical UTF-8; fail rather than silently replacing a
    # checker byte that cannot be represented exactly.
    try:
        completed.stdout.decode("utf-8")
        completed.stderr.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ImportReceiptError("Stage4 checker emitted non-UTF-8 output") from exc
    checker_after, checker_after_bytes = _read_binding(root, CHECKER_RELATIVE)
    if checker_after != checker_binding or checker_after_bytes != checker_bytes:
        raise ImportReceiptError("Stage4 checker bytes changed while verification ran")
    return {
        "status": "passed",
        "argv": argv,
        "cwd": ".",
        "exit_code": completed.returncode,
        "checker_artifact": checker_binding,
        "stdout": _stream_binding(completed.stdout),
        "stderr": _stream_binding(completed.stderr),
    }


@contextmanager
def _shared_v4_lock(root: Path) -> Iterator[None]:
    directory = (root / V4_DIR_RELATIVE).resolve()
    if not directory.is_dir():
        raise ImportReceiptError(f"required Stage4 directory is missing: {V4_DIR_RELATIVE}")
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_SH)
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def build_receipt(root: Path = ROOT) -> dict[str, Any]:
    """Authenticate current Stage4 bytes and return the sealed Stage5 receipt."""

    root = root.resolve()
    with _shared_v4_lock(root):
        manifest_binding, manifest_bytes = _read_binding(root, MANIFEST_RELATIVE)
        manifest = strict_json_bytes(manifest_bytes, MANIFEST_RELATIVE.as_posix())
        manifest_summary = _validate_manifest(manifest)

        documents: dict[str, dict[str, Any]] = {}
        output_bindings: list[dict[str, Any]] = []
        initial_output_files: dict[str, dict[str, Any]] = {}
        for role, relative, kind in OFFICIAL_OUTPUTS:
            binding, payload = _read_binding(root, relative)
            initial_output_files[role] = binding
            entry: dict[str, Any] = {
                **binding,
                "role": role,
                "media_type": "application/json" if kind == "json" else "text/markdown",
            }
            if kind == "json":
                document = strict_json_bytes(payload, relative.as_posix())
                documents[role] = document
                entry.update(_validate_json_authority(role, relative, document))
            else:
                try:
                    payload.decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise ImportReceiptError(
                        f"Stage4 Markdown output is not UTF-8: {relative.as_posix()}"
                    ) from exc
            output_bindings.append(entry)

        if len(output_bindings) != 13 or len(documents) != 10:
            raise ImportReceiptError("Stage4 release surface is not exactly 13 outputs (10 JSON + 3 Markdown)")
        source_inventory, source_inventory_digest = _validate_common_source_inventory(
            root, documents, manifest_summary["fragments"]
        )
        manifest_source_row = next(
            (row for row in source_inventory if row["path"] == MANIFEST_RELATIVE.as_posix()),
            None,
        )
        if manifest_source_row != manifest_binding:
            raise ImportReceiptError("manifest binding differs from the common Stage4 source inventory")

        identity_import, direct_counts = _build_identity_import(manifest, documents)
        checker_result = _run_checker(root)

        # Re-read all bound predecessor bytes after the independent checker.
        # The v4 directory lock protects normal publishers; these comparisons
        # also catch writers that ignored the lock.
        for role, relative, _kind in OFFICIAL_OUTPUTS:
            observed, _payload = _read_binding(root, relative)
            if observed != initial_output_files[role]:
                raise ImportReceiptError(f"Stage4 output changed during import: {relative.as_posix()}")
        for expected in source_inventory:
            observed, _payload = _read_binding(root, expected["path"])
            if observed != expected:
                raise ImportReceiptError(
                    f"Stage4 authoritative input changed during import: {expected['path']}"
                )

        json_count = sum(entry[2] == "json" for entry in OFFICIAL_OUTPUTS)
        markdown_count = len(OFFICIAL_OUTPUTS) - json_count
        counts = {
            "official_outputs": len(OFFICIAL_OUTPUTS),
            "official_json_outputs": json_count,
            "official_markdown_outputs": markdown_count,
            "authoritative_source_artifacts": len(source_inventory),
            **direct_counts,
        }
        receipt: dict[str, Any] = {
            "schema_version": "awesome-theorems/v4-import-receipt-v5/5.0",
            "artifact": OUTPUT_RELATIVE.name,
            "generated_by": "Docs/tools/build_v4_import_receipt_v5.py",
            "import_from_stage": "Stage4",
            "import_into_stage": "Stage5",
            "predecessor_manifest": {
                **manifest_binding,
                **manifest_summary,
            },
            "counts": counts,
            "official_outputs": output_bindings,
            "official_outputs_sha256": sha256_bytes(canonical_json_bytes(output_bindings)),
            "authoritative_sources": source_inventory,
            "authoritative_sources_sha256": source_inventory_digest,
            "identity_import": identity_import,
            "independent_checker": checker_result,
            "completion_boundary": {
                "import_receipt_complete": True,
                "stage4_gap_supplement_imported": True,
                "stage4_number_migration_imported": True,
                "inherited_baseline_semantic_review_complete": False,
                "note": (
                    "This receipt proves exact predecessor-byte and identity migration, not a semantic, "
                    "truth, proof, rights, or benchmark upgrade for inherited machine-triage rows."
                ),
            },
        }
        receipt["authority_sha256"] = _artifact_authority(receipt)
        return receipt


def receipt_bytes(receipt: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(receipt) + b"\n"


def _atomic_write(path: Path, payload: bytes) -> None:
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
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except BaseException:
        try:
            temporary.unlink(missing_ok=True)
        finally:
            raise


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="repository root (default: inferred from this script)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="perform no writes; require the committed receipt to equal a fresh rebuild",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = args.root.resolve()
    try:
        expected_receipt = build_receipt(root)
        expected_bytes = receipt_bytes(expected_receipt)
        output_path = root / OUTPUT_RELATIVE
        if args.check:
            if not output_path.is_file():
                raise ImportReceiptError(f"missing receipt: {OUTPUT_RELATIVE.as_posix()}")
            observed = output_path.read_bytes()
            if observed != expected_bytes:
                raise ImportReceiptError(
                    f"stale receipt: {OUTPUT_RELATIVE.as_posix()} does not match current Stage4 bytes"
                )
            action = "checked"
        else:
            _atomic_write(output_path, expected_bytes)
            action = "wrote"
        counts = expected_receipt["counts"]
        print(
            f"PASS build_v4_import_receipt_v5 ({action}) "
            f"ATV/S4={counts['atv_variants']}/{counts['stage_claim_mappings']} "
            f"THM={counts['historical_thm_aliases']} "
            f"redirects/splits={counts['redirects']}/{counts['splits']} "
            f"outputs={counts['official_outputs']}"
        )
        return 0
    except (ImportReceiptError, OSError) as exc:
        print(f"FAIL build_v4_import_receipt_v5: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
