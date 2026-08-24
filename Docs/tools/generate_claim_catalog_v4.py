#!/usr/bin/env python3
"""Generate the Stage4 curated supplement, numbering, migration, and lists.

This generator deliberately does *not* reinterpret the 3,338 inherited v2
variants as reviewed theorems.  It preserves that bootstrap byte-for-byte at
the identity boundary, validates a bounded curation manifest, appends one
ATO/ATS/ATV allocation for every accepted exact child, and projects the
result into Stage4 lists.

Manifest contract (``awesome-theorems/stage4-curation-manifest/4.0``)
---------------------------------------------------------------------

The root object requires ``stage``, ``review_date``, ``scope``, ``policy``,
``fragments``, and the five arrays ``sources``, ``dispositions``,
``additions``, ``overlays``, and ``collision_resolutions``.  A fragment uses
schema ``awesome-theorems/stage4-curation-fragment/4.0`` and contributes the
same five arrays plus a ``domain``.  Source IDs and curation keys are global.

``disposition.child_keys`` names exact ``addition.curation_key`` values; a
candidate name alone never allocates an ID.  An addition has the fields
documented in ``Docs/catalog/v4/README.md`` and contains an exact structured
statement, dated material status, applicable sources, lineage, and an
explicit family action.  An overlay may change metadata or append a status
event, but may not change the semantic statement.  Semantic changes require
a new addition and therefore a new ATV.  Splits have no default child and
never inherit evidence.

Every JSON output is canonical (sorted-key pretty JSON), contains hashes for
all authoritative inputs, and is sealed by a digest over canonical JSON with
``authority_sha256`` omitted.  ``--check`` performs no writes and fails when
any output byte differs.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
from copy import deepcopy
from datetime import date
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[2]
CATALOG_DIR = ROOT / "Docs" / "catalog"
V4_DIR = CATALOG_DIR / "v4"

V2_SOURCE_RECORDS_PATH = CATALOG_DIR / "Source_Records_v2.json"
V2_REGISTRY_PATH = CATALOG_DIR / "Claim_ID_Registry_v2.json"
V2_CATALOG_PATH = CATALOG_DIR / "Claim_Catalog_v2.json"
COVERAGE_PATH = CATALOG_DIR / "Coverage_Candidates_v2.json"
AUDIT_PATH = ROOT / "Docs" / "reviews" / "Stage3_v3_18_Agent_Critical_Audit_2026-08-10.md"
MANIFEST_PATH = V4_DIR / "Stage4_Curation_Manifest_v4.json"

REPAIR_PATHS = {
    "mathematics": CATALOG_DIR / "repairs" / "Mathematics_v2.json",
    "physics": CATALOG_DIR / "repairs" / "Physics_v2.json",
    "computer_science": CATALOG_DIR / "repairs" / "Computer_Science_v2.json",
}
LEGACY_SOURCE_PATHS = (
    ROOT / "Docs" / "researches" / "math_theorems.md",
    ROOT / "Docs" / "researches" / "physics_theorems.md",
    ROOT / "Docs" / "researches" / "cs_theorems.md",
)

SOURCE_RECORDS_V4_PATH = V4_DIR / "Source_Records_v4.json"
REGISTRY_V4_PATH = V4_DIR / "Claim_ID_Registry_v4.json"
STAGE_REGISTRY_V4_PATH = V4_DIR / "Stage4_Claim_ID_Registry_v4.json"
MIGRATION_V4_PATH = V4_DIR / "Claim_ID_Migration_v2_to_v4.json"
CANDIDATE_DISPOSITIONS_V4_PATH = V4_DIR / "Candidate_Dispositions_v4.json"
REPAIR_DISPOSITIONS_V4_PATH = V4_DIR / "Repair_Proposal_Dispositions_v4.json"
CATALOG_V4_PATH = V4_DIR / "Claim_Catalog_v4.json"
THEOREM_JSON_V4_PATH = V4_DIR / "Theorem_List_v4.json"
THEOREM_MD_V4_PATH = V4_DIR / "Theorem_List_v4.md"
OPEN_JSON_V4_PATH = V4_DIR / "Conjecture_Hypothesis_Open_List_v4.json"
OPEN_MD_V4_PATH = V4_DIR / "Conjecture_Hypothesis_Open_List_v4.md"
STATUS_JSON_V4_PATH = V4_DIR / "Status_Index_v4.json"
STATUS_MD_V4_PATH = V4_DIR / "Status_Index_v4.md"

OUTPUT_PATHS = (
    SOURCE_RECORDS_V4_PATH,
    REGISTRY_V4_PATH,
    STAGE_REGISTRY_V4_PATH,
    MIGRATION_V4_PATH,
    CANDIDATE_DISPOSITIONS_V4_PATH,
    REPAIR_DISPOSITIONS_V4_PATH,
    CATALOG_V4_PATH,
    THEOREM_JSON_V4_PATH,
    THEOREM_MD_V4_PATH,
    OPEN_JSON_V4_PATH,
    OPEN_MD_V4_PATH,
    STATUS_JSON_V4_PATH,
    STATUS_MD_V4_PATH,
)

JSON_OUTPUT_PATHS = tuple(path for path in OUTPUT_PATHS if path.suffix == ".json")
PREVIOUS_STATE_PATHS = (
    SOURCE_RECORDS_V4_PATH,
    REGISTRY_V4_PATH,
    MIGRATION_V4_PATH,
    CANDIDATE_DISPOSITIONS_V4_PATH,
)

BASELINE_OCCURRENCES = 3338
BASELINE_FAMILIES = 3119
BASELINE_SENSES = 3338
BASELINE_VARIANTS = 3338
BASELINE_LEGACY_ALIASES = 3262
BASELINE_FOLDED_OCCURRENCES = 76
V2_MISSING_KEYS = 62
V2_COLLISION_KEYS = 36
V3_DELTA_KEYS = 56
FROZEN_CANDIDATE_KEYS = 154
REPAIR_PROPOSALS = 623

ID_RE = re.compile(r"^(ATO|ATF|ATS|ATV)-([0-9]{8})$")
STAGE_ID_RE = re.compile(r"^S4-CLM-([0-9]{8})$")
LEGACY_ID_RE = re.compile(r"^THM-[MPC]-[0-9]{4}$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REDIRECT_ID_RE = re.compile(r"^REDIRECT-[0-9A-F]{24}$")
SPLIT_ID_RE = re.compile(r"^SPLIT-[0-9A-F]{24}$")

MANIFEST_SCHEMA = "awesome-theorems/stage4-curation-manifest/4.0"
FRAGMENT_SCHEMA = "awesome-theorems/stage4-curation-fragment/4.0"
GENERATED_BY = "Docs/tools/generate_claim_catalog_v4.py"

DOMAIN_FROM_AUDIT_PREFIX = {
    "math": "mathematics",
    "physics": "physics",
    "cs": "computer_science",
}
DISCIPLINE_TO_DOMAIN = {
    "数学": "mathematics",
    "物理": "physics",
    "计算机科学": "computer_science",
}

THEOREM_KINDS = {
    "theorem",
    "lemma",
    "result",
    "complexity_result",
    "undecidability_result",
    "no_go_theorem",
    "reconstruction_theorem",
    "representation_theorem",
    "structure_theorem",
    "sum_rule",
    "model_consequence",
    "identity",
    "inequality",
    "law",
}
THEOREM_SUBTYPES = {
    "no_go_theorem",
    "representation_theorem",
    "structure_theorem",
    "sum_rule",
    "reconstruction_theorem",
    "model_consequence",
}
OPEN_KINDS = {"conjecture", "hypothesis", "open_problem", "assumption"}
OPEN_STATUS_WORDS = {
    "open",
    "unresolved",
    "independent",
    "partial",
    "partially_resolved",
    "disputed",
    "conditional_open",
}

# These are schema enums, not projection heuristics.  Keeping them separate
# from THEOREM_KINDS/OPEN_KINDS makes manifest and artifact validation fail
# closed when a misspelled or invented value is supplied.
CURATED_CLAIM_KINDS = THEOREM_KINDS | OPEN_KINDS | {
    "dataset",
    "empirical_catalog_result",
    "empirical_comparison_result",
    "empirical_discrepancy",
    "empirical_result",
    "empirical_status_result",
    "experiment_event",
    "framework",
}
CURATED_RECORD_ROLES = {"claim", "entity", "event", "aggregate", "nonclaim"}
CURATED_ATOMICITIES = {"atomic"}
CURATED_MATERIAL_STATUSES = {
    "conditional",
    "empirically_supported",
    "not_applicable",
    "open",
    "proved",
}
CURATED_RIGHTS_STATUSES = {
    "bibliographic_metadata_only",
    "citation_only_rights_unresolved",
}
HISTORICAL_KINDS = {
    "anomaly_claim",
    "approximation",
    "assumption",
    "conjecture",
    "dataset",
    "experiment",
    "hypothesis",
    "law",
    "lemma",
    "mechanism",
    "observation",
    "open_problem",
    "scaling_law",
    "theorem",
}
MEMBERSHIP_DOMAINS = {"mathematics", "physics", "computer_science"}
CANDIDATE_DOMAINS = MEMBERSHIP_DOMAINS | {"cross_domain"}
FRAGMENT_DOMAINS = CANDIDATE_DOMAINS | {"regression_fixtures"}
LINEAGE_RELATION_TYPES = {
    "empirical_status_child_of",
    "experimental_test_of",
    "generalizes",
    "refines",
    "refines_scope_of",
    "scope_child_of",
    "scope_limited_by",
    "specializes",
    "split_child_of",
    "split_from",
    "supersedes",
}

# Independent, append-only anchors for the lifecycle rows that predate the
# final Stage4 release review.  The independent stdlib checker carries its own
# copy; this generator deliberately does not import it.  Later generations may
# append rows, but every row named here must remain byte-semantically identical
# under canonical JSON.  An adjacent artifact seal alone is insufficient,
# because a coordinated edit can recompute that unkeyed seal.
SEALED_LIFECYCLE_ROW_SHA256: Mapping[str, str] = {
    "REDIRECT-B30E3CD21DD7E2602BD3E0E5": "334d801f193c331eedabbc374878aec66af319d9e8f93a344df7a39d9226ba9e",
    "REDIRECT-4504297B39A7A25BB4C020E5": "a0e67884e808a3573c39928660ede2cad9b4454f4f225bab162ff992b6171724",
    "REDIRECT-FB27B04079086231E4E4C53F": "7a1cd1e6c1566d77d4a5855133c09b8da485b6993b676e04e5e6d19a84cc71a8",
    "REDIRECT-D438734A52F72EFBF4FB42A2": "bf9769eececdd183492ed9b33b332a320b35d2c0d2e0a477f2c3bbd65e10ddf5",
    "REDIRECT-6032E22033E288237E493FF6": "346dce6252246ec29ab90d9df72377fe493527a094d7a8609e1c6eb2710c3a7d",
    "REDIRECT-BC3F80E148AD88B187EEDD2A": "32ed4be34aeaea2011cb3fe30f4a4e13e4a7496f1e8f1ddde8928dbfec23d19e",
    "REDIRECT-167829F9FD68CED39348DC5D": "f83f58cae5a9cbc9feeb7e9df1f1466f20c05555f24ed7b9520a8c582cefc1fa",
    "REDIRECT-DCA5F275CC316F8A763348F5": "28cb48dd74106a448ab4c453f321945a00d62e14e51864af48b4a8dcf4467fd4",
    "SPLIT-B40A7EFEDCFD4C6306D5D857": "01bfcb18ffcf85814538c1a87ed0027d6e8d866c7a93704b1d2a28753b24f1a0",
    "SPLIT-825096F3118A866AA336504F": "026b21f328eea65630c81ce007afb57b79257230464174a4f71d44883365688a",
    "SPLIT-C8D4B0B44F90920D7DA33479": "bb4909fc092216c97d1213ba942173e00c75f20d129c3ef6f042250e58f2fe96",
    "SPLIT-EEC5BA3081476410928A5D99": "495aaca0cb5bdda18a5cac95261cefe9cef9ca087b795d0f75b6a1bf4bbdaf3f",
}

ARTIFACT_SCHEMAS = {
    SOURCE_RECORDS_V4_PATH.name: "awesome-theorems/source-records/4.0",
    REGISTRY_V4_PATH.name: "awesome-theorems/claim-id-registry/4.0",
    STAGE_REGISTRY_V4_PATH.name: "awesome-theorems/stage4-claim-id-registry/4.0",
    MIGRATION_V4_PATH.name: "awesome-theorems/claim-id-migration-v2-to-v4/4.0",
    CANDIDATE_DISPOSITIONS_V4_PATH.name: "awesome-theorems/candidate-dispositions/4.0",
    REPAIR_DISPOSITIONS_V4_PATH.name: "awesome-theorems/repair-proposal-dispositions/4.0",
    CATALOG_V4_PATH.name: "awesome-theorems/claim-catalog/4.0",
    THEOREM_JSON_V4_PATH.name: "awesome-theorems/theorem-list/4.0",
    OPEN_JSON_V4_PATH.name: "awesome-theorems/conjecture-hypothesis-open-list/4.0",
    STATUS_JSON_V4_PATH.name: "awesome-theorems/status-index/4.0",
}


class CatalogError(RuntimeError):
    """Fail-closed Stage4 catalog error."""


# A descriptive alias retained for callers which imported the early v4 API.
CatalogV4Error = CatalogError


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def pretty_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def stable_digest(namespace: str, payload: Any) -> str:
    return sha256_bytes(namespace.encode("utf-8") + b"\0" + canonical_json_bytes(payload))


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise CatalogError(f"required input is missing: {path.relative_to(ROOT)}") from error
    except json.JSONDecodeError as error:
        raise CatalogError(f"invalid JSON in {path.relative_to(ROOT)}: {error}") from error
    if not isinstance(value, dict):
        raise CatalogError(f"{path.relative_to(ROOT)} must contain one JSON object")
    return value


def _require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CatalogError(f"{label} must be an object")
    return value


def _require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise CatalogError(f"{label} must be an array")
    return value


def _require_string(value: Any, label: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str) or (nonempty and not value.strip()):
        raise CatalogError(f"{label} must be a non-empty string")
    return value


def _require_enum(value: Any, allowed: set[str], label: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        choices = ", ".join(sorted(allowed))
        raise CatalogError(f"{label} must be one of: {choices}")
    return value


def _require_iso_date(value: Any, label: str) -> str:
    """Require one canonical, real Gregorian calendar date."""

    if not isinstance(value, str) or DATE_RE.fullmatch(value) is None:
        raise CatalogError(f"{label} must be a strict ISO YYYY-MM-DD date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise CatalogError(f"{label} is not a real calendar date: {value!r}") from error
    if parsed.isoformat() != value:
        raise CatalogError(f"{label} must use canonical ISO YYYY-MM-DD form")
    return value


def _require_fields(row: Mapping[str, Any], required: Iterable[str], label: str) -> None:
    missing = sorted(set(required) - set(row))
    if missing:
        raise CatalogError(f"{label} is missing required fields: {', '.join(missing)}")


def _require_object_rows(value: Any, label: str) -> list[dict[str, Any]]:
    rows = _require_list(value, label)
    if not all(isinstance(row, dict) for row in rows):
        raise CatalogError(f"{label} must contain only objects")
    return rows


def _validate_sealed_lifecycle_rows(
    registry: Mapping[str, Any], label: str
) -> None:
    """Conserve every independently anchored redirect/split row exactly."""

    rows_by_id: dict[str, dict[str, Any]] = {}
    collections = (
        ("redirects", "redirect_id", REDIRECT_ID_RE),
        ("splits", "split_id", SPLIT_ID_RE),
    )
    for field, id_field, pattern in collections:
        rows = _require_object_rows(registry.get(field), f"{label}.{field}")
        for index, row in enumerate(rows):
            lifecycle_id = row.get(id_field)
            if not isinstance(lifecycle_id, str) or pattern.fullmatch(lifecycle_id) is None:
                raise CatalogError(
                    f"{label}.{field}[{index}] lacks a valid immutable {id_field}"
                )
            if lifecycle_id in rows_by_id:
                raise CatalogError(f"{label} duplicates lifecycle ID {lifecycle_id}")
            rows_by_id[lifecycle_id] = row

    missing = sorted(set(SEALED_LIFECYCLE_ROW_SHA256) - set(rows_by_id))
    if missing:
        raise CatalogError(
            f"{label} removes sealed lifecycle history: {missing[:8]!r}"
        )
    for lifecycle_id, expected in SEALED_LIFECYCLE_ROW_SHA256.items():
        observed = sha256_bytes(canonical_json_bytes(rows_by_id[lifecycle_id]))
        if observed != expected:
            raise CatalogError(
                f"{label} rebinds or mutates sealed lifecycle row {lifecycle_id}"
            )


def _parse_ordinal(identifier: str, prefix: str) -> int:
    match = re.fullmatch(rf"{re.escape(prefix)}-([0-9]{{8}})", str(identifier))
    if match is None:
        raise CatalogError(f"invalid {prefix} identifier: {identifier!r}")
    return int(match.group(1))


def _new_id(prefix: str, ordinal: int) -> str:
    if not 1 <= ordinal <= 99_999_999:
        raise CatalogError(f"{prefix} namespace exhausted")
    return f"{prefix}-{ordinal:08d}"


def _stage_id(variant_id: str) -> str:
    return f"S4-CLM-{_parse_ordinal(variant_id, 'ATV'):08d}"


def _artifact_authority(document: Mapping[str, Any]) -> str:
    body = {key: value for key, value in document.items() if key != "authority_sha256"}
    # A plain canonical-body hash is intentionally used so an independent
    # stdlib verifier need not import this generator or duplicate an artifact
    # namespace table.  The artifact filename and schema remain inside the
    # hashed body.
    return sha256_bytes(canonical_json_bytes(body))


def _seal(document: dict[str, Any]) -> dict[str, Any]:
    document["authority_sha256"] = _artifact_authority(document)
    return document


def document_authority(
    name_or_document: str | Path | Mapping[str, Any],
    document: Mapping[str, Any] | None = None,
) -> str:
    """Return the authority digest for an artifact, for independent tests."""

    if document is None:
        if not isinstance(name_or_document, Mapping):
            raise CatalogError("document_authority(document) requires an object")
        value = dict(name_or_document)
    else:
        value = deepcopy(dict(document))
        value["artifact"] = Path(str(name_or_document)).name
    return _artifact_authority(value)


def seal_document(
    name_or_document: str | Path | Mapping[str, Any],
    document: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a re-sealed copy; intended for structural mutation tests."""

    if document is None:
        if not isinstance(name_or_document, Mapping):
            raise CatalogError("seal_document(document) requires an object")
        value = deepcopy(dict(name_or_document))
    else:
        value = deepcopy(dict(document))
        value["artifact"] = Path(str(name_or_document)).name
    value.pop("authority_sha256", None)
    return _seal(value)


def _preferred_label_text(value: Any, label: str) -> str:
    """Normalize a string or language map to the Stage4 display label."""

    if isinstance(value, str) and value.strip():
        return value
    if isinstance(value, dict):
        preferred = value.get("zh-Hans", value.get("en"))
        if isinstance(preferred, str) and preferred.strip() and all(
            isinstance(language, str)
            and language
            and isinstance(text, str)
            and text.strip()
            for language, text in value.items()
        ):
            return preferred
    raise CatalogError(f"{label} must be a non-empty string or language-label object")


def _preferred_label_map(value: Any) -> dict[str, str]:
    if isinstance(value, dict):
        return deepcopy(value)
    return {"und": str(value)}


def _canonical_claim_kind(value: Any) -> str:
    """Collapse descriptive theorem subtypes into the closed list kind.

    The domain-specific subtype is retained separately in catalog records;
    projection logic therefore does not depend on an ever-growing spelling
    allowlist.
    """

    kind = str(value)
    return "theorem" if kind in THEOREM_SUBTYPES else kind


def _recomputed_document_counts(
    document: Mapping[str, Any], artifact: str
) -> dict[str, Any]:
    """Derive every public count from the artifact rows it summarizes."""

    if artifact == SOURCE_RECORDS_V4_PATH.name:
        rows = _require_object_rows(document.get("records"), f"{artifact}.records")
        baseline_ids = _require_list(
            document.get("baseline_occurrence_ids"),
            f"{artifact}.baseline_occurrence_ids",
        )
        folded_ids = _require_list(
            document.get("folded_occurrence_ids"),
            f"{artifact}.folded_occurrence_ids",
        )
        return {
            "allocated_occurrences": len(rows),
            "baseline_occurrences": len(baseline_ids),
            "stage4_additions": sum(row.get("curation_key") is not None for row in rows),
            "folded_baseline_occurrences": len(folded_ids),
        }

    if artifact == REGISTRY_V4_PATH.name:
        families = _require_object_rows(document.get("families"), f"{artifact}.families")
        senses = _require_object_rows(document.get("senses"), f"{artifact}.senses")
        variants = _require_object_rows(document.get("variants"), f"{artifact}.variants")
        aliases = _require_object_rows(
            document.get("legacy_aliases"), f"{artifact}.legacy_aliases"
        )
        redirects = _require_object_rows(document.get("redirects"), f"{artifact}.redirects")
        splits = _require_object_rows(document.get("splits"), f"{artifact}.splits")
        return {
            # The registry has one bootstrap occurrence per allocated exact
            # variant; cross-artifact validation checks the occurrence IDs.
            "occurrences_allocated": len(variants),
            "families_allocated": len(families),
            "senses_allocated": len(senses),
            "variants_allocated": len(variants),
            "legacy_aliases": len(aliases),
            "redirects": len(redirects),
            "splits": len(splits),
            "stage4_additions": sum(
                row.get("curation_key") is not None for row in variants
            ),
        }

    if artifact == STAGE_REGISTRY_V4_PATH.name:
        rows = _require_object_rows(document.get("mappings"), f"{artifact}.mappings")
        new = sum(row.get("curation_key") is not None for row in rows)
        return {"mappings": len(rows), "baseline": len(rows) - new, "new": new}

    if artifact == MIGRATION_V4_PATH.name:
        rows = _require_object_rows(document.get("migrations"), f"{artifact}.migrations")
        aliases = _require_object_rows(
            document.get("legacy_alias_migrations"),
            f"{artifact}.legacy_alias_migrations",
        )
        folded = _require_list(
            document.get("folded_occurrence_ids"),
            f"{artifact}.folded_occurrence_ids",
        )
        baseline = sum(row.get("v2_variant_id") is not None for row in rows)
        return {
            "migrations": len(rows),
            "baseline_carry": baseline,
            "new_stage4": len(rows) - baseline,
            "legacy_aliases": len(aliases),
            "folded_occurrences": len(folded),
        }

    if artifact == CANDIDATE_DISPOSITIONS_V4_PATH.name:
        rows = _require_object_rows(document.get("dispositions"), f"{artifact}.dispositions")
        origins = Counter(row.get("origin") for row in rows)
        dispositions = Counter(row.get("disposition") for row in rows)
        return {
            "total": len(rows),
            "frozen": len(rows) - origins.get("stage4_discovery", 0),
            "stage4_discovery": origins.get("stage4_discovery", 0),
            "v2_missing": origins.get("v2_missing", 0),
            "v2_collision": origins.get("v2_collision", 0),
            "v3_delta": origins.get("v3_delta", 0),
            "new_family": dispositions.get("new_family", 0),
            "existing_family": dispositions.get("existing_family", 0),
            "collision": dispositions.get("collision", 0),
            "nonclaim": dispositions.get("nonclaim", 0),
        }

    if artifact == REPAIR_DISPOSITIONS_V4_PATH.name:
        rows = _require_object_rows(document.get("dispositions"), f"{artifact}.dispositions")
        domains = Counter(row.get("domain") for row in rows)
        dispositions = Counter(row.get("disposition") for row in rows)
        return {
            "total": len(rows),
            "mathematics": domains.get("mathematics", 0),
            "physics": domains.get("physics", 0),
            "computer_science": domains.get("computer_science", 0),
            "applied_by_explicit_curation": dispositions.get(
                "applied_by_explicit_curation", 0
            ),
            "proposal_only_preserved": dispositions.get("proposal_only_preserved", 0),
        }

    if artifact == CATALOG_V4_PATH.name:
        rows = _require_object_rows(document.get("records"), f"{artifact}.records")
        states = Counter(row.get("curation_state") for row in rows)
        return {
            "records": len(rows),
            "baseline_machine_triage": states.get("inherited_v2_machine_triage", 0),
            "curated_additions": states.get("stage4_curated_addition", 0),
            "curated_overlays": states.get("stage4_curated_overlay", 0),
        }

    if artifact in {THEOREM_JSON_V4_PATH.name, OPEN_JSON_V4_PATH.name}:
        rows = _require_object_rows(document.get("records"), f"{artifact}.records")
        inherited = sum(
            row.get("curation_state") == "inherited_v2_machine_triage" for row in rows
        )
        return {
            "records": len(rows),
            "curated": len(rows) - inherited,
            "inherited_machine_triage": inherited,
        }

    if artifact == STATUS_JSON_V4_PATH.name:
        rows = _require_object_rows(document.get("records"), f"{artifact}.records")
        buckets = Counter(row.get("status_bucket") for row in rows)
        if None in buckets:
            raise CatalogError(f"{artifact}.records contains a missing status_bucket")
        return {"records": len(rows), "buckets": dict(sorted(buckets.items()))}

    raise CatalogError(f"unsupported Stage4 artifact: {artifact!r}")


def validate_document(
    name_or_document: str | Path | Mapping[str, Any],
    document: Mapping[str, Any] | None = None,
) -> None:
    """Validate the common envelope and authority seal of one v4 document.

    Both ``validate_document(document)`` and
    ``validate_document(filename, document)`` are supported for mutation
    tests and external checkers.
    """

    if document is None:
        if not isinstance(name_or_document, Mapping):
            raise CatalogError("validate_document(document) requires an object")
        value = dict(name_or_document)
        expected_name = str(value.get("artifact", ""))
    else:
        value = dict(document)
        expected_name = Path(str(name_or_document)).name
    _require_fields(
        value,
        (
            "schema_version",
            "artifact",
            "generated_by",
            "authoritative_inputs",
            "authoritative_inputs_sha256",
            "counts",
            "authority_sha256",
        ),
        expected_name or "v4 document",
    )
    if value["artifact"] != expected_name:
        raise CatalogError(
            f"artifact name mismatch: expected {expected_name!r}, got {value['artifact']!r}"
        )
    if value["generated_by"] != GENERATED_BY:
        raise CatalogError(f"{expected_name} has an unexpected generator")
    expected_schema = ARTIFACT_SCHEMAS.get(expected_name)
    if expected_schema is None or value["schema_version"] != expected_schema:
        raise CatalogError(f"{expected_name} has an unsupported schema_version")
    inputs = _require_list(value["authoritative_inputs"], f"{expected_name}.authoritative_inputs")
    if value["authoritative_inputs_sha256"] != stable_digest(
        "awesome-theorems/stage4-authoritative-inputs/v4", inputs
    ):
        raise CatalogError(f"{expected_name} authoritative input digest is stale")
    observed_counts = _require_object(value["counts"], f"{expected_name}.counts")
    expected_counts = _recomputed_document_counts(value, expected_name)
    if observed_counts != expected_counts:
        raise CatalogError(
            f"{expected_name} counts differ from its records: "
            f"expected={expected_counts!r} observed={observed_counts!r}"
        )
    observed = value.get("authority_sha256")
    expected = _artifact_authority(value)
    if not isinstance(observed, str) or observed != expected:
        raise CatalogError(f"{expected_name} authority digest is missing or stale")


def _verify_v2_authority(
    document: Mapping[str, Any], namespace: str, label: str
) -> None:
    observed = document.get("authority_sha256")
    body = {key: value for key, value in document.items() if key != "authority_sha256"}
    expected = stable_digest(namespace, body)
    if not isinstance(observed, str) or observed != expected:
        raise CatalogError(f"{label} v2 authority digest is missing or stale")


def _safe_repo_path(locator: str) -> Path:
    path = (ROOT / locator).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as error:
        raise CatalogError(f"manifest fragment escapes the repository: {locator!r}") from error
    return path


def _audit_delta_keys(text: str) -> list[str]:
    keys = re.findall(
        r"^missing\.(?:math|physics|cs)\.[a-z0-9_]+\s*$", text, flags=re.MULTILINE
    )
    keys = [key.strip() for key in keys]
    if len(keys) != V3_DELTA_KEYS or len(set(keys)) != V3_DELTA_KEYS:
        raise CatalogError(
            f"Stage3 audit must expose exactly {V3_DELTA_KEYS} unique delta keys; got {len(keys)}"
        )
    return sorted(keys)


def _repair_rows(document: Mapping[str, Any], label: str) -> list[dict[str, Any]]:
    rows = document.get("records", document.get("repairs"))
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise CatalogError(f"{label} has no repair proposal array")
    return rows


def _input_paths_from_manifest(root_manifest: Mapping[str, Any]) -> list[Path]:
    fragments = _require_list(root_manifest.get("fragments"), "manifest.fragments")
    paths: list[Path] = []
    for index, locator in enumerate(fragments):
        paths.append(_safe_repo_path(_require_string(locator, f"manifest.fragments[{index}]")))
    return paths


def _authoritative_input_paths(root_manifest: Mapping[str, Any]) -> list[Path]:
    paths = [
        V2_SOURCE_RECORDS_PATH,
        V2_REGISTRY_PATH,
        V2_CATALOG_PATH,
        COVERAGE_PATH,
        AUDIT_PATH,
        MANIFEST_PATH,
        *REPAIR_PATHS.values(),
        *LEGACY_SOURCE_PATHS,
        *_input_paths_from_manifest(root_manifest),
    ]
    return sorted({path.resolve() for path in paths}, key=str)


def _snapshot_paths(paths: Iterable[Path]) -> list[dict[str, Any]]:
    snapshot: list[dict[str, Any]] = []
    for path in sorted({Path(item).resolve() for item in paths}, key=str):
        try:
            relative = str(path.relative_to(ROOT.resolve()))
        except ValueError:
            relative = str(path)
        if not path.is_file():
            snapshot.append({"path": relative, "exists": False})
            continue
        payload = path.read_bytes()
        snapshot.append(
            {
                "path": relative,
                "exists": True,
                "size_bytes": len(payload),
                "sha256": sha256_bytes(payload),
            }
        )
    return snapshot


def capture_generation_snapshot(
    root_manifest: Mapping[str, Any] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Capture the authoritative inputs and all prior output bytes for CAS."""

    manifest = read_json(MANIFEST_PATH) if root_manifest is None else root_manifest
    return {
        "authoritative_inputs": _snapshot_paths(_authoritative_input_paths(manifest)),
        "previous_outputs": _snapshot_paths(OUTPUT_PATHS),
    }


def assert_generation_snapshot(
    expected: Mapping[str, Any],
    root_manifest: Mapping[str, Any] | None = None,
) -> None:
    """Fail when inputs or any prior artifact changed since generation began."""

    observed = capture_generation_snapshot(root_manifest)
    if observed != expected:
        expected_inputs = expected.get("authoritative_inputs")
        expected_outputs = expected.get("previous_outputs")
        changed = []
        if observed["authoritative_inputs"] != expected_inputs:
            changed.append("authoritative inputs")
        if observed["previous_outputs"] != expected_outputs:
            changed.append("prior output/allocator snapshot")
        raise CatalogError(
            "Stage4 generation snapshot CAS failed: " + ", ".join(changed)
        )


def _validate_loaded_authoritative_inventory(inputs: Mapping[str, Any]) -> None:
    """Authenticate a caller-supplied build input inventory against disk."""

    manifest = _require_object(inputs.get("manifest"), "inputs.manifest")
    observed = _require_list(
        inputs.get("authoritative_inputs"), "inputs.authoritative_inputs"
    )
    normalized: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    for index, raw in enumerate(observed):
        row = _require_object(raw, f"inputs.authoritative_inputs[{index}]")
        if set(row) != {"path", "sha256", "size_bytes"}:
            raise CatalogError(
                f"inputs.authoritative_inputs[{index}] has an invalid inventory shape"
            )
        path = _require_string(row["path"], f"inputs.authoritative_inputs[{index}].path")
        digest = row["sha256"]
        size = row["size_bytes"]
        if (
            path in seen_paths
            or Path(path).is_absolute()
            or ".." in Path(path).parts
            or not isinstance(digest, str)
            or SHA256_RE.fullmatch(digest) is None
            or not isinstance(size, int)
            or isinstance(size, bool)
            or size < 0
        ):
            raise CatalogError(
                f"inputs.authoritative_inputs[{index}] is malformed or duplicated"
            )
        seen_paths.add(path)
        normalized.append(dict(row))
    if normalized != sorted(normalized, key=lambda row: row["path"]):
        raise CatalogError("inputs.authoritative_inputs is not canonically ordered")
    expected = _input_inventory(manifest)
    if normalized != expected:
        raise CatalogError(
            "loaded authoritative input inventory differs from the current filesystem snapshot"
        )


@contextmanager
def stage4_generation_lock(*, exclusive: bool = True) -> Iterable[None]:
    """Lock the v4 directory inode for one complete generator/checker run."""

    V4_DIR.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(V4_DIR, os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _input_inventory(root_manifest: Mapping[str, Any]) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    for path in _authoritative_input_paths(root_manifest):
        relative = str(path.relative_to(ROOT.resolve()))
        if not path.is_file():
            raise CatalogError(f"authoritative input is missing: {relative}")
        inventory.append(
            {"path": relative, "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
        )
    return inventory


def load_inputs() -> dict[str, Any]:
    """Load and structurally authenticate every Stage4 authoritative input."""

    # The manifest is intentionally read twice around the first snapshot.
    # A fragment-list change during discovery must not let us combine the old
    # path set with new manifest content.
    initial_manifest = read_json(MANIFEST_PATH)
    load_start_snapshot = capture_generation_snapshot(initial_manifest)
    source_v2 = read_json(V2_SOURCE_RECORDS_PATH)
    registry_v2 = read_json(V2_REGISTRY_PATH)
    catalog_v2 = read_json(V2_CATALOG_PATH)
    coverage = read_json(COVERAGE_PATH)
    repairs = {domain: read_json(path) for domain, path in REPAIR_PATHS.items()}
    root_manifest = read_json(MANIFEST_PATH)
    audit_text = AUDIT_PATH.read_text(encoding="utf-8")

    _verify_v2_authority(
        source_v2,
        "awesome-theorems/source-records-authority/v2",
        "Source_Records_v2.json",
    )
    _verify_v2_authority(
        registry_v2,
        "awesome-theorems/claim-id-registry-authority/v2",
        "Claim_ID_Registry_v2.json",
    )
    if registry_v2.get("source_records_authority_sha256") != source_v2.get("authority_sha256"):
        raise CatalogError("v2 registry is not bound to the v2 source-record authority")

    missing = _require_list(coverage.get("missing_candidates"), "coverage.missing_candidates")
    collisions = _require_list(coverage.get("present_collisions"), "coverage.present_collisions")
    if len(missing) != V2_MISSING_KEYS or len(collisions) != V2_COLLISION_KEYS:
        raise CatalogError("Coverage_Candidates_v2.json no longer has the frozen 62+36 inventory")
    coverage_rows = missing + collisions
    coverage_by_key: dict[str, dict[str, Any]] = {}
    for row in coverage_rows:
        key = _require_string(row.get("candidate_key"), "coverage candidate_key")
        if key in coverage_by_key:
            raise CatalogError(f"duplicate v2 coverage key: {key}")
        coverage_by_key[key] = row

    audit_keys = _audit_delta_keys(audit_text)
    repair_count = sum(
        len(_repair_rows(document, str(REPAIR_PATHS[domain].relative_to(ROOT))))
        for domain, document in repairs.items()
    )
    if repair_count != REPAIR_PROPOSALS:
        raise CatalogError(f"v2 repair proposal denominator changed: expected 623, got {repair_count}")

    records = _require_list(source_v2.get("records"), "v2 source records")
    variants = _require_list(registry_v2.get("variants"), "v2 variants")
    aliases = _require_list(registry_v2.get("legacy_aliases"), "v2 legacy aliases")
    if (len(records), len(variants), len(aliases)) != (
        BASELINE_OCCURRENCES,
        BASELINE_VARIANTS,
        BASELINE_LEGACY_ALIASES,
    ):
        raise CatalogError("v2 3338/3338/3262 conservation boundary changed")
    occurrence_ids = {row.get("occurrence_id") for row in records}
    alias_occurrences = {row.get("target_occurrence_id") for row in aliases}
    if len(occurrence_ids - alias_occurrences) != BASELINE_FOLDED_OCCURRENCES:
        raise CatalogError("v2 folded-occurrence denominator is not 76")

    previous_v4: dict[str, dict[str, Any]] = {}
    previous_pair = (SOURCE_RECORDS_V4_PATH.is_file(), REGISTRY_V4_PATH.is_file())
    if previous_pair[0] != previous_pair[1]:
        raise CatalogError("partial v4 allocator state: source records and registry must coexist")
    if not any(previous_pair):
        manifest_policy = _require_object(root_manifest.get("policy"), "manifest.policy")
        release_state = str(manifest_policy.get("release_state", "draft")).casefold()
        if release_state in {"published", "released", "accepted", "sealed"}:
            raise CatalogError(
                "sealed Stage4 manifest has no allocator state; implicit reallocation forbidden"
            )
    if all(previous_pair):
        lifecycle_pair = (
            MIGRATION_V4_PATH.is_file(),
            CANDIDATE_DISPOSITIONS_V4_PATH.is_file(),
        )
        if lifecycle_pair != (True, True):
            raise CatalogError(
                "partial v4 lifecycle state: registry, migration, and candidate artifacts must coexist"
            )
        for path in (
            SOURCE_RECORDS_V4_PATH,
            REGISTRY_V4_PATH,
            MIGRATION_V4_PATH,
            CANDIDATE_DISPOSITIONS_V4_PATH,
        ):
            value = read_json(path)
            validate_document(path.name, value)
            previous_v4[path.name] = value
        if previous_v4[REGISTRY_V4_PATH.name].get(
            "source_records_authority_sha256"
        ) != previous_v4[SOURCE_RECORDS_V4_PATH.name].get("authority_sha256"):
            raise CatalogError(
                "prior v4 registry/source allocator authorities form a mixed snapshot"
            )

    inventory = _input_inventory(root_manifest)
    if previous_v4:
        _validate_previous_lifecycle_artifacts(
            previous_v4,
            current_authoritative_inputs=inventory,
            effective_manifest=_merge_manifest(root_manifest),
        )
    load_end_snapshot = capture_generation_snapshot(root_manifest)
    if load_end_snapshot != load_start_snapshot:
        raise CatalogError(
            "Stage4 inputs or prior allocator artifacts changed while load_inputs was reading"
        )
    return {
        "source_records_v2": source_v2,
        "registry_v2": registry_v2,
        "catalog_v2": catalog_v2,
        "coverage_v2": coverage,
        "coverage_by_key": coverage_by_key,
        "audit_text": audit_text,
        "audit_delta_keys": audit_keys,
        "repairs": repairs,
        "manifest": root_manifest,
        "authoritative_inputs": inventory,
        "previous_v4": previous_v4,
        "generation_snapshot": load_end_snapshot,
    }


def authorize_unreleased_bootstrap_replacement(
    inputs: Mapping[str, Any]
) -> dict[str, Any]:
    """Return inputs with draft allocator state cleared after strict guards.

    This is an explicit development recovery path for outputs generated while
    curation fragments were still being edited concurrently.  It cannot
    replace a published/released artifact and is never used by ``--check`` or
    the public ``build_artifacts()`` default.  The authoritative v2 baseline
    remains untouched.
    """

    existing = [path for path in OUTPUT_PATHS if path.is_file()]
    if not existing:
        raise CatalogError("no unreleased Stage4 draft exists to bootstrap-replace")
    release_keys = {
        "release_receipt",
        "release_receipt_sha256",
        "publication_receipt",
        "published_at",
        "released_at",
    }
    for path in existing:
        if path.suffix == ".json":
            document = read_json(path)
            if document.get("generated_by") != GENERATED_BY:
                raise CatalogError(
                    f"refusing to replace non-generator artifact {path.relative_to(ROOT)}"
                )
            if release_keys & set(document):
                raise CatalogError(
                    f"refusing to replace release-marked artifact {path.relative_to(ROOT)}"
                )
            release_state = str(document.get("release_state", "draft")).casefold()
            if release_state in {"published", "released", "accepted", "sealed"}:
                raise CatalogError(
                    f"refusing to replace {release_state} artifact {path.relative_to(ROOT)}"
                )
        else:
            text = path.read_text(encoding="utf-8")
            if "Generated from `Claim_Catalog_v4.json`; do not edit by hand." not in text:
                raise CatalogError(
                    f"refusing to replace non-generated projection {path.relative_to(ROOT)}"
                )
    policy = _require_object(inputs["manifest"].get("policy"), "manifest.policy")
    release_state = str(policy.get("release_state", "draft")).casefold()
    if release_state in {"published", "released", "accepted", "sealed"} or any(
        key in policy for key in release_keys
    ):
        raise CatalogError("manifest policy marks Stage4 as released; bootstrap replacement forbidden")
    result = deepcopy(dict(inputs))
    result["previous_v4"] = {}
    result["bootstrap_replaced_unreleased_draft"] = True
    return result


def _merge_manifest(root_manifest: Mapping[str, Any]) -> dict[str, Any]:
    _require_fields(
        root_manifest,
        (
            "schema_version",
            "stage",
            "review_date",
            "scope",
            "fragments",
            "sources",
            "dispositions",
            "additions",
            "overlays",
            "collision_resolutions",
            "policy",
        ),
        "Stage4 manifest",
    )
    if root_manifest.get("schema_version") != MANIFEST_SCHEMA:
        raise CatalogError("unsupported Stage4 manifest schema")
    effective = deepcopy(dict(root_manifest))
    for field in (
        "sources",
        "dispositions",
        "additions",
        "overlays",
        "collision_resolutions",
    ):
        effective[field] = list(_require_list(effective[field], f"manifest.{field}"))
    fragment_paths: list[str] = []
    for index, locator_value in enumerate(_require_list(root_manifest["fragments"], "manifest.fragments")):
        locator = _require_string(locator_value, f"manifest.fragments[{index}]")
        path = _safe_repo_path(locator)
        fragment = read_json(path)
        _require_fields(
            fragment,
            (
                "schema_version",
                "domain",
                "sources",
                "dispositions",
                "additions",
                "overlays",
                "collision_resolutions",
            ),
            locator,
        )
        if fragment.get("schema_version") != FRAGMENT_SCHEMA:
            raise CatalogError(f"{locator} has an unsupported fragment schema")
        _require_enum(fragment.get("domain"), FRAGMENT_DOMAINS, f"{locator}.domain")
        for field in (
            "sources",
            "dispositions",
            "additions",
            "overlays",
            "collision_resolutions",
        ):
            rows = _require_list(fragment.get(field), f"{locator}.{field}")
            for row in rows:
                if not isinstance(row, dict):
                    raise CatalogError(f"{locator}.{field} contains a non-object")
                copied = deepcopy(row)
                copied.setdefault("_manifest_fragment", locator)
                effective[field].append(copied)
        fragment_paths.append(locator)
    if len(fragment_paths) != len(set(fragment_paths)):
        raise CatalogError("manifest.fragments contains a duplicate path")
    effective["_fragment_paths"] = fragment_paths
    effective["_effective_manifest"] = True
    return effective


def _expected_candidate_universe(inputs: Mapping[str, Any]) -> dict[str, dict[str, str]]:
    expected: dict[str, dict[str, str]] = {}
    coverage = inputs["coverage_v2"]
    for row in coverage["missing_candidates"]:
        expected[row["candidate_key"]] = {
            "origin": "v2_missing",
            "domain": row["domain"],
        }
    for row in coverage["present_collisions"]:
        expected[row["candidate_key"]] = {
            "origin": "v2_collision",
            "domain": row["domain"],
        }
    for key in inputs["audit_delta_keys"]:
        prefix = key.split(".", 2)[1]
        expected[key] = {
            "origin": "v3_delta",
            "domain": DOMAIN_FROM_AUDIT_PREFIX[prefix],
        }
    if len(expected) != FROZEN_CANDIDATE_KEYS:
        raise CatalogError("internal frozen candidate union is not 154 keys")
    return expected


def validate_manifest(
    manifest: Mapping[str, Any], inputs: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate and return the root+fragment effective manifest.

    Frozen v2/v3 keys must appear exactly once.  Additional, explicitly keyed
    Stage4 discovery dispositions are permitted, but they must use origin
    ``stage4_discovery`` and satisfy the same evidence/child rules.
    """

    effective = (
        deepcopy(dict(manifest))
        if manifest.get("_effective_manifest") is True
        else _merge_manifest(manifest)
    )
    if effective.get("stage") != "Stage4":
        raise CatalogError("manifest.stage must be Stage4")
    review_date = _require_iso_date(
        effective.get("review_date"), "manifest.review_date"
    )
    _require_object(effective.get("scope"), "manifest.scope")
    _require_object(effective.get("policy"), "manifest.policy")

    # Identical source declarations may be repeated by independently owned
    # fragments.  Unequal reuse of a source ID is rejected.
    sources: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(effective["sources"]):
        row = dict(raw)
        _require_fields(row, ("source_id", "title", "locator", "source_role"), f"source[{index}]")
        source_id = _require_string(row["source_id"], f"source[{index}].source_id")
        for field in ("title", "locator", "source_role"):
            _require_string(row[field], f"source[{index}].{field}")
        comparable = {key: value for key, value in row.items() if not key.startswith("_")}
        if source_id in sources and canonical_json_bytes(sources[source_id]) != canonical_json_bytes(comparable):
            raise CatalogError(f"source_id {source_id!r} is rebound to unequal metadata")
        sources[source_id] = comparable
    effective["sources"] = [sources[key] for key in sorted(sources)]
    source_ids = set(sources)

    expected = _expected_candidate_universe(inputs)
    dispositions: dict[str, dict[str, Any]] = {}
    disposition_required = (
        "candidate_key",
        "origin",
        "domain",
        "disposition",
        "existing_atv_ids",
        "child_keys",
        "resolution_action",
        "rationale",
        "source_refs",
    )
    allowed_dispositions = {"new_family", "existing_family", "collision", "nonclaim"}
    for index, raw in enumerate(effective["dispositions"]):
        row = {key: value for key, value in raw.items() if not key.startswith("_")}
        _require_fields(row, disposition_required, f"disposition[{index}]")
        key = _require_string(row["candidate_key"], f"disposition[{index}].candidate_key")
        if key in dispositions:
            raise CatalogError(f"candidate disposition duplicated: {key}")
        origin = _require_string(row["origin"], f"disposition[{key}].origin")
        domain = _require_enum(
            row["domain"], CANDIDATE_DOMAINS, f"disposition[{key}].domain"
        )
        if key in expected:
            normalized_origin = {
                "coverage_candidates_v2": "v2_missing",
                "stage3_v3_audit_delta": "v3_delta",
            }.get(origin, origin)
            if normalized_origin != expected[key]["origin"] or domain != expected[key]["domain"]:
                raise CatalogError(f"frozen candidate {key} has the wrong origin/domain")
        elif origin != "stage4_discovery":
            raise CatalogError(f"unfrozen candidate {key} must use origin stage4_discovery")
        if row["disposition"] not in allowed_dispositions:
            raise CatalogError(f"candidate {key} has invalid disposition {row['disposition']!r}")
        existing = _require_list(row["existing_atv_ids"], f"disposition[{key}].existing_atv_ids")
        children = _require_list(row["child_keys"], f"disposition[{key}].child_keys")
        refs = _require_list(row["source_refs"], f"disposition[{key}].source_refs")
        if len(existing) != len(set(existing)) or not all(
            isinstance(item, str) and re.fullmatch(r"ATV-[0-9]{8}", item) for item in existing
        ):
            raise CatalogError(f"candidate {key} has invalid/duplicate existing ATV IDs")
        if len(children) != len(set(children)) or not all(
            isinstance(item, str) and item for item in children
        ):
            raise CatalogError(f"candidate {key} has invalid/duplicate child keys")
        if not refs or not all(isinstance(ref, str) and ref in source_ids for ref in refs):
            raise CatalogError(f"candidate {key} has an unknown or empty source_refs set")
        _require_string(row["resolution_action"], f"disposition[{key}].resolution_action")
        _require_string(row["rationale"], f"disposition[{key}].rationale")
        if row["disposition"] == "new_family" and not children:
            raise CatalogError(f"new-family candidate {key} has no exact child")
        # A nonclaim umbrella may route to one or more truth-apt exact child
        # claims.  The umbrella itself receives no allocation.  A collision
        # disposition, by contrast, only records existing targets.
        if row["disposition"] == "collision" and children:
            raise CatalogError(f"collision candidate {key} cannot allocate children")
        if row["disposition"] == "existing_family" and not existing and not children:
            raise CatalogError(f"existing-family candidate {key} resolves to nothing")
        dispositions[key] = row
    missing_frozen = sorted(set(expected) - set(dispositions))
    if missing_frozen:
        raise CatalogError(
            f"manifest omits {len(missing_frozen)} frozen candidate keys; first={missing_frozen[0]}"
        )
    effective["dispositions"] = [dispositions[key] for key in sorted(dispositions)]

    baseline_variants = {row["variant_id"] for row in inputs["registry_v2"]["variants"]}
    previous_registry = inputs.get("previous_v4", {}).get(REGISTRY_V4_PATH.name, {})
    prior_variant_by_id = {
        row["variant_id"]: row
        for row in _require_object_rows(
            previous_registry.get("variants", []), "previous Claim_ID_Registry_v4.variants"
        )
    }
    prior_variant_by_key = {
        row["curation_key"]: row
        for row in prior_variant_by_id.values()
        if row.get("curation_key") is not None
    }
    existing_redirect_by_source = {
        row.get("source_variant_id", row.get("from_variant_id")): row
        for row in _require_object_rows(
            previous_registry.get("redirects", []), "previous Claim_ID_Registry_v4.redirects"
        )
    }
    superseded_targets: dict[str, str] = {}
    additions: dict[str, dict[str, Any]] = {}
    instruction_child_keys = {
        child
        for overlay in effective["overlays"]
        if isinstance(overlay, dict)
        for child in overlay.get("child_keys", [])
        if isinstance(child, str)
    }
    addition_required = (
        "curation_key",
        "candidate_keys",
        "preferred_label",
        "aliases",
        "owner_domain",
        "membership_domains",
        "record_role",
        "claim_kind",
        "historical_kind",
        "atomicity",
        "statement",
        "material_status",
        "provenance_source_refs",
        "family_action",
        "lineage",
        "rights_status",
    )
    for index, raw in enumerate(effective["additions"]):
        row = {key: value for key, value in raw.items() if not key.startswith("_")}
        _require_fields(row, addition_required, f"addition[{index}]")
        key = _require_string(row["curation_key"], f"addition[{index}].curation_key")
        if key in additions:
            raise CatalogError(f"addition curation_key duplicated: {key}")
        candidate_keys = _require_list(row["candidate_keys"], f"addition[{key}].candidate_keys")
        if len(candidate_keys) != len(set(candidate_keys)) or (
            not candidate_keys and key not in instruction_child_keys
        ):
            raise CatalogError(
                f"addition {key} must cite unique candidate keys or be owned by a split overlay"
            )
        for candidate_key in candidate_keys:
            if candidate_key not in dispositions:
                raise CatalogError(f"addition {key} cites unknown candidate {candidate_key}")
            if key not in dispositions[candidate_key]["child_keys"]:
                raise CatalogError(
                    f"addition {key} is not named by disposition child_keys for {candidate_key}"
                )
            if dispositions[candidate_key]["disposition"] == "collision":
                raise CatalogError(f"addition {key} is owned by a collision disposition")
        _preferred_label_text(row["preferred_label"], f"addition[{key}].preferred_label")
        aliases = _require_list(row["aliases"], f"addition[{key}].aliases")
        if not all(isinstance(alias, str) and alias.strip() for alias in aliases):
            raise CatalogError(f"addition {key} has an invalid alias")
        owner = _require_enum(
            row["owner_domain"], MEMBERSHIP_DOMAINS, f"addition[{key}].owner_domain"
        )
        memberships = _require_list(row["membership_domains"], f"addition[{key}].membership_domains")
        if (
            owner not in memberships
            or len(memberships) != len(set(memberships))
            or any(domain not in MEMBERSHIP_DOMAINS for domain in memberships)
        ):
            raise CatalogError(f"addition {key} has invalid domain ownership")
        _require_enum(
            row["record_role"], CURATED_RECORD_ROLES, f"addition[{key}].record_role"
        )
        _require_enum(
            row["claim_kind"], CURATED_CLAIM_KINDS, f"addition[{key}].claim_kind"
        )
        _require_enum(
            row["historical_kind"], HISTORICAL_KINDS, f"addition[{key}].historical_kind"
        )
        _require_enum(
            row["atomicity"], CURATED_ATOMICITIES, f"addition[{key}].atomicity"
        )
        _require_enum(
            row["rights_status"],
            CURATED_RIGHTS_STATUSES,
            f"addition[{key}].rights_status",
        )
        statement = _require_object(row["statement"], f"addition[{key}].statement")
        _require_fields(statement, ("natural_language", "hypotheses", "conclusion", "scope"), f"addition[{key}].statement")
        _require_string(statement["natural_language"], f"addition[{key}].statement.natural_language")
        _require_list(statement["hypotheses"], f"addition[{key}].statement.hypotheses")
        _require_string(statement["conclusion"], f"addition[{key}].statement.conclusion")
        _require_string(statement["scope"], f"addition[{key}].statement.scope")
        status = _require_object(row["material_status"], f"addition[{key}].material_status")
        _require_fields(status, ("status", "as_of", "basis", "source_refs"), f"addition[{key}].material_status")
        _require_enum(
            status["status"],
            CURATED_MATERIAL_STATUSES,
            f"addition[{key}].material_status.status",
        )
        status_date = _require_iso_date(
            status["as_of"], f"addition[{key}].material_status.as_of"
        )
        if status_date > review_date:
            raise CatalogError(f"addition {key} material status postdates review_date")
        _require_string(status["basis"], f"addition[{key}].material_status.basis")
        status_refs = _require_list(status["source_refs"], f"addition[{key}].material_status.source_refs")
        provenance_refs = _require_list(row["provenance_source_refs"], f"addition[{key}].provenance_source_refs")
        for ref in [*status_refs, *provenance_refs]:
            if not isinstance(ref, str) or ref not in source_ids:
                raise CatalogError(f"addition {key} cites unknown source {ref!r}")
        if not status_refs or not provenance_refs:
            raise CatalogError(f"addition {key} lacks applicable status/provenance sources")
        if row["family_action"] not in {"new_family", "reuse_family"}:
            raise CatalogError(f"addition {key} has invalid family_action")
        reuse = row.get("reuse_atf_id")
        if row["family_action"] == "reuse_family":
            if not isinstance(reuse, str) or re.fullmatch(r"ATF-[0-9]{8}", reuse) is None:
                raise CatalogError(f"addition {key} must name reuse_atf_id")
            if reuse not in {item["family_id"] for item in inputs["registry_v2"]["families"]}:
                raise CatalogError(f"addition {key} reuses an unknown baseline family")
        elif reuse is not None:
            raise CatalogError(f"new-family addition {key} cannot set reuse_atf_id")
        lineage = _require_list(row["lineage"], f"addition[{key}].lineage")
        for relation_index, relation in enumerate(lineage):
            relation = _require_object(relation, f"addition[{key}].lineage[{relation_index}]")
            _require_fields(relation, ("relation_type", "target_atv_id", "evidence_inherited"), f"addition[{key}].lineage[{relation_index}]")
            _require_enum(
                relation["relation_type"],
                LINEAGE_RELATION_TYPES,
                f"addition[{key}].lineage.relation_type",
            )
            target_atv_id = relation["target_atv_id"]
            if relation["relation_type"] == "supersedes":
                if len(lineage) != 1:
                    raise CatalogError(
                        f"addition {key} supersedes lineage must be its single lineage edge"
                    )
                target = prior_variant_by_id.get(target_atv_id)
                if target is None or not isinstance(target.get("curation_key"), str):
                    raise CatalogError(
                        f"addition {key} supersedes a variant not allocated in prior Stage4"
                    )
                prior_superseding_variant = prior_variant_by_key.get(key)
                if target["curation_key"] == key:
                    raise CatalogError(
                        f"addition {key} does not mint a distinct superseding curation key"
                    )
                if prior_superseding_variant is not None and (
                    prior_superseding_variant.get("semantic_payload_sha256")
                    != _semantic_sha256(row)
                ):
                    raise CatalogError(
                        f"allocated superseding semantic payload changed for {key}"
                    )
                target_semantic = target.get("semantic_payload_sha256")
                if not isinstance(target_semantic, str) or SHA256_RE.fullmatch(target_semantic) is None:
                    raise CatalogError(
                        f"addition {key} supersedes a target without semantic authority"
                    )
                if target_semantic == _semantic_sha256(row):
                    raise CatalogError(
                        f"addition {key} supersedes an identical semantic payload"
                    )
                existing_redirect = existing_redirect_by_source.get(target_atv_id)
                if existing_redirect is not None:
                    expected_prior_target = (
                        prior_superseding_variant.get("variant_id")
                        if prior_superseding_variant is not None
                        else None
                    )
                    if (
                        existing_redirect.get("relation_type") != "supersedes"
                        or existing_redirect.get("curation_key") != key
                        or existing_redirect.get(
                            "target_variant_id", existing_redirect.get("to_variant_id")
                        )
                        != expected_prior_target
                    ):
                        raise CatalogError(
                            f"addition {key} conflicts with existing redirect for {target_atv_id}"
                        )
                if target_atv_id in superseded_targets:
                    raise CatalogError(
                        f"variant {target_atv_id} is superseded by more than one addition"
                    )
                superseded_targets[target_atv_id] = key
            elif target_atv_id not in baseline_variants:
                raise CatalogError(f"addition {key} lineage targets an unknown baseline ATV")
            if relation["evidence_inherited"] is not False:
                raise CatalogError(f"addition {key} lineage must explicitly deny evidence inheritance")
        additions[key] = row
    for candidate_key, disposition in dispositions.items():
        for child_key in disposition["child_keys"]:
            if child_key not in additions:
                raise CatalogError(f"candidate {candidate_key} names missing exact child {child_key}")
            # A regression fixture may deliberately attach a second review
            # key to an exact child owned in another domain fragment.  The
            # disposition edge is authoritative; normalize its reverse edge
            # into the generated addition instead of forcing cross-owner file
            # edits.
            if candidate_key not in additions[child_key]["candidate_keys"]:
                additions[child_key]["candidate_keys"] = sorted(
                    set(additions[child_key]["candidate_keys"]) | {candidate_key}
                )
        if disposition["disposition"] == "nonclaim" and disposition["child_keys"]:
            if not any(
                additions[child_key]["record_role"] == "claim"
                for child_key in disposition["child_keys"]
            ):
                raise CatalogError(
                    f"nonclaim umbrella {candidate_key} has no extracted truth-apt child"
                )
    effective["additions"] = [additions[key] for key in sorted(additions)]

    overlays: dict[str, dict[str, Any]] = {}
    legacy_target_by_id = {
        alias["alias_id"]: alias["target_variant_id"]
        for alias in inputs["registry_v2"]["legacy_aliases"]
    }
    overlay_required = (
        "curation_key",
        "candidate_keys",
        "target_atv_id",
        "source_refs",
        "change_class",
        "evidence_inherited",
    )
    for index, raw in enumerate(effective["overlays"]):
        row = {key: value for key, value in raw.items() if not key.startswith("_")}
        # Domain fragments may use the compact semantic-split instruction
        # form.  It is normalized here to the general overlay event form; it
        # never edits the parent statement or transfers its evidence.
        if "curation_key" not in row:
            _require_fields(
                row,
                ("target_atv_id", "legacy_id", "action", "child_keys", "rationale", "source_refs"),
                f"overlay[{index}]",
            )
            child_keys = _require_list(row["child_keys"], f"overlay[{index}].child_keys")
            inferred_candidates = sorted(
                candidate_key
                for candidate_key, disposition in dispositions.items()
                if set(disposition["child_keys"]) & set(child_keys)
                or row["target_atv_id"] in disposition["existing_atv_ids"]
            )
            row.update(
                {
                    "curation_key": "overlay."
                    + stable_digest(
                        "awesome-theorems/stage4-overlay-instruction/v4",
                        {
                            "target_atv_id": row["target_atv_id"],
                            "action": row["action"],
                            "child_keys": child_keys,
                        },
                    )[:24],
                    "candidate_keys": inferred_candidates,
                    "change_class": "split_instruction" if child_keys else "lineage_instruction",
                    "evidence_inherited": False,
                }
            )
        _require_fields(row, overlay_required, f"overlay[{index}]")
        key = _require_string(row["curation_key"], f"overlay[{index}].curation_key")
        if key in overlays or key in additions:
            raise CatalogError(f"curation_key is reused: {key}")
        if row["target_atv_id"] not in baseline_variants:
            raise CatalogError(f"overlay {key} targets an unknown baseline ATV")
        if "legacy_id" in row and legacy_target_by_id.get(row["legacy_id"]) != row["target_atv_id"]:
            raise CatalogError(f"overlay {key} legacy alias does not resolve to its target ATV")
        candidate_keys = _require_list(row["candidate_keys"], f"overlay[{key}].candidate_keys")
        if any(candidate_key not in dispositions for candidate_key in candidate_keys):
            raise CatalogError(f"overlay {key} cites an unknown candidate set")
        refs = _require_list(row["source_refs"], f"overlay[{key}].source_refs")
        if not refs or any(ref not in source_ids for ref in refs):
            raise CatalogError(f"overlay {key} cites unknown sources")
        if row["change_class"] not in {
            "metadata_only",
            "status_event",
            "split_instruction",
            "lineage_instruction",
        }:
            raise CatalogError(f"overlay {key} has invalid change_class")
        if row["evidence_inherited"] is not False:
            raise CatalogError(f"overlay {key} must explicitly deny inherited evidence")
        if "preferred_label" in row:
            _preferred_label_text(row["preferred_label"], f"overlay[{key}].preferred_label")
        if "claim_kind" in row:
            _require_enum(
                row["claim_kind"], CURATED_CLAIM_KINDS, f"overlay[{key}].claim_kind"
            )
        if "historical_kind" in row:
            _require_enum(
                row["historical_kind"],
                HISTORICAL_KINDS,
                f"overlay[{key}].historical_kind",
            )
        forbidden_domain_edits = {
            "owner_domain",
            "membership_domains",
            "membership_domains_remove",
        } & set(row)
        if forbidden_domain_edits:
            raise CatalogError(
                f"overlay {key} attempts a destructive domain edit: "
                f"{sorted(forbidden_domain_edits)!r}"
            )
        if "membership_domains_add" in row:
            membership_add = _require_list(
                row["membership_domains_add"],
                f"overlay[{key}].membership_domains_add",
            )
            if (
                not membership_add
                or len(membership_add) != len(set(membership_add))
                or any(domain not in MEMBERSHIP_DOMAINS for domain in membership_add)
            ):
                raise CatalogError(f"overlay {key} has invalid membership_domains_add")
        if "statement" in row and row["statement"] not in (None, {}):
            raise CatalogError(f"overlay {key} attempts a semantic statement mutation")
        if row["change_class"] == "status_event" and "material_status" not in row:
            raise CatalogError(f"status overlay {key} has no material_status event")
        child_keys = _require_list(row.get("child_keys", []), f"overlay[{key}].child_keys")
        for child_key in child_keys:
            child = additions.get(child_key)
            if child is None:
                raise CatalogError(f"split overlay {key} names missing child {child_key}")
            if not any(
                relation["target_atv_id"] == row["target_atv_id"]
                and relation["evidence_inherited"] is False
                for relation in child["lineage"]
            ):
                raise CatalogError(
                    f"split child {child_key} lacks non-inheriting lineage to {row['target_atv_id']}"
                )
        if "material_status" in row:
            material = _require_object(row["material_status"], f"overlay[{key}].material_status")
            _require_fields(material, ("status", "as_of", "basis", "source_refs"), f"overlay[{key}].material_status")
            _require_enum(
                material["status"],
                CURATED_MATERIAL_STATUSES,
                f"overlay[{key}].material_status.status",
            )
            material_date = _require_iso_date(
                material["as_of"], f"overlay[{key}].material_status.as_of"
            )
            if material_date > review_date:
                raise CatalogError(f"overlay {key} material status postdates review_date")
            _require_string(
                material["basis"], f"overlay[{key}].material_status.basis"
            )
            if any(ref not in source_ids for ref in _require_list(material["source_refs"], f"overlay[{key}].material_status.source_refs")):
                raise CatalogError(f"overlay {key} material status cites unknown sources")
        overlays[key] = row
    effective["overlays"] = [overlays[key] for key in sorted(overlays)]

    resolutions: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(effective["collision_resolutions"]):
        row = {key: value for key, value in raw.items() if not key.startswith("_")}
        _require_fields(
            row,
            ("candidate_key", "action", "target_atv_ids", "no_new_family", "evidence_inherited", "rationale"),
            f"collision_resolution[{index}]",
        )
        key = _require_string(row["candidate_key"], f"collision_resolution[{index}].candidate_key")
        if key in resolutions:
            raise CatalogError(f"collision resolution duplicated: {key}")
        if key not in dispositions:
            raise CatalogError(f"collision/overlap resolution {key} has no disposition")
        targets = _require_list(row["target_atv_ids"], f"collision_resolution[{key}].target_atv_ids")
        if dispositions[key]["disposition"] == "collision" and targets != dispositions[key]["existing_atv_ids"]:
            raise CatalogError(f"collision resolution {key} changes its target ATV set/order")
        if any(target not in baseline_variants for target in targets):
            raise CatalogError(f"collision resolution {key} targets an unknown ATV")
        if not isinstance(row["no_new_family"], bool) or row["evidence_inherited"] is not False:
            raise CatalogError(f"collision resolution {key} violates allocation/inheritance typing")
        if dispositions[key]["disposition"] == "collision" and row["no_new_family"] is not True:
            raise CatalogError(f"collision resolution {key} attempts a new family")
        _require_string(row["action"], f"collision_resolution[{key}].action")
        _require_string(row["rationale"], f"collision_resolution[{key}].rationale")
        resolutions[key] = row
    expected_resolutions = {
        key
        for key, row in dispositions.items()
        if row["disposition"] == "collision" and row["origin"] == "v2_collision"
    }
    if not expected_resolutions <= set(resolutions):
        missing = sorted(expected_resolutions - set(resolutions))
        raise CatalogError(f"collision resolution coverage differs: missing={missing[:1]}")
    effective["collision_resolutions"] = [resolutions[key] for key in sorted(resolutions)]
    return effective


def _semantic_payload(addition: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "record_role": addition["record_role"],
        "claim_kind": addition["claim_kind"],
        "atomicity": addition["atomicity"],
        "statement": addition["statement"],
    }


def _semantic_sha256(addition: Mapping[str, Any]) -> str:
    return stable_digest("awesome-theorems/stage4-semantic-payload/v4", _semantic_payload(addition))


def _max_id(rows: Iterable[Mapping[str, Any]], field: str, prefix: str) -> int:
    return max((_parse_ordinal(str(row[field]), prefix) for row in rows), default=0)


def _build_allocations(
    effective: Mapping[str, Any], inputs: Mapping[str, Any]
) -> tuple[dict[str, dict[str, str]], dict[str, Any], dict[str, Any]]:
    source_v2 = inputs["source_records_v2"]
    registry_v2 = inputs["registry_v2"]
    additions = {row["curation_key"]: row for row in effective["additions"]}

    baseline_sources = deepcopy(source_v2["records"])
    families = deepcopy(registry_v2["families"])
    senses = deepcopy(registry_v2["senses"])
    variants = deepcopy(registry_v2["variants"])
    legacy_aliases = deepcopy(registry_v2["legacy_aliases"])

    previous = inputs.get("previous_v4", {})
    prior_source = previous.get(SOURCE_RECORDS_V4_PATH.name)
    prior_registry = previous.get(REGISTRY_V4_PATH.name)
    redirects = deepcopy(
        (prior_registry or registry_v2).get("redirects", [])
    )
    prior_splits = deepcopy(
        (prior_registry or registry_v2).get("splits", [])
    )
    prior_by_key: dict[str, dict[str, Any]] = {}
    prior_source_by_key: dict[str, dict[str, Any]] = {}
    if prior_registry is not None:
        baseline_variant_by_id = {row["variant_id"]: row for row in registry_v2["variants"]}
        for row in prior_registry.get("variants", []):
            variant_id = row.get("variant_id")
            if variant_id in baseline_variant_by_id:
                if row != baseline_variant_by_id[variant_id]:
                    raise CatalogError(f"prior v4 allocator mutated baseline variant {variant_id}")
                continue
            key = row.get("curation_key")
            if not isinstance(key, str) or key in prior_by_key:
                raise CatalogError("prior v4 registry has an invalid new-variant curation key")
            prior_by_key[key] = row
        for row in prior_source.get("records", []):
            key = row.get("curation_key")
            if key is not None:
                if not isinstance(key, str) or key in prior_source_by_key:
                    raise CatalogError("prior v4 source authority has duplicate curation keys")
                prior_source_by_key[key] = row
        removed = sorted(set(prior_by_key) - set(additions))
        if removed:
            raise CatalogError(
                f"append-only manifest removed allocated curation key {removed[0]!r}"
            )

    next_ato = max(
        _max_id(baseline_sources, "occurrence_id", "ATO"),
        int(prior_source.get("namespace_high_watermark", 0)) if prior_source else 0,
    ) + 1
    next_atf = max(
        _max_id(families, "family_id", "ATF"),
        int((prior_registry or {}).get("namespace_high_watermarks", {}).get("ATF", 0)),
    ) + 1
    next_ats = max(
        _max_id(senses, "sense_id", "ATS"),
        int((prior_registry or {}).get("namespace_high_watermarks", {}).get("ATS", 0)),
    ) + 1
    next_atv = max(
        _max_id(variants, "variant_id", "ATV"),
        int((prior_registry or {}).get("namespace_high_watermarks", {}).get("ATV", 0)),
    ) + 1

    prior_sense_by_id = {
        row["sense_id"]: row for row in (prior_registry or {}).get("senses", [])
    }
    allocation: dict[str, dict[str, str]] = {}
    for key in sorted(additions):
        addition = additions[key]
        prior_variant = prior_by_key.get(key)
        if prior_variant is not None:
            if prior_variant.get("semantic_payload_sha256") != _semantic_sha256(addition):
                raise CatalogError(
                    f"semantic payload changed for allocated {key}; mint a new curation key/ATV"
                )
            prior_sense = prior_sense_by_id.get(prior_variant.get("sense_id"))
            prior_occurrence = prior_source_by_key.get(key)
            if prior_sense is None or prior_occurrence is None:
                raise CatalogError(f"prior v4 allocation for {key} is incomplete")
            ids = {
                "occurrence_id": prior_occurrence["occurrence_id"],
                "family_id": prior_sense["family_id"],
                "sense_id": prior_sense["sense_id"],
                "variant_id": prior_variant["variant_id"],
            }
            expected_family = (
                addition.get("reuse_atf_id")
                if addition["family_action"] == "reuse_family"
                else ids["family_id"]
            )
            if ids["family_id"] != expected_family:
                raise CatalogError(f"family binding changed for allocated {key}")
        else:
            family_id = addition.get("reuse_atf_id")
            if addition["family_action"] == "new_family":
                family_id = _new_id("ATF", next_atf)
                next_atf += 1
            ids = {
                "occurrence_id": _new_id("ATO", next_ato),
                "family_id": str(family_id),
                "sense_id": _new_id("ATS", next_ats),
                "variant_id": _new_id("ATV", next_atv),
            }
            next_ato += 1
            next_ats += 1
            next_atv += 1
        allocation[key] = ids

    family_by_id = {row["family_id"]: row for row in families}
    baseline_family_ids = set(family_by_id)
    family_membership_extensions: list[dict[str, Any]] = []
    snapshot_sha = stable_digest(
        "awesome-theorems/stage4-curation-snapshot/v4",
        {
            "manifest": {
                key: value
                for key, value in effective.items()
                if not key.startswith("_")
            },
            "authoritative_inputs": inputs["authoritative_inputs"],
        },
    )
    new_source_rows: list[dict[str, Any]] = []
    new_sense_rows: list[dict[str, Any]] = []
    new_variant_rows: list[dict[str, Any]] = []
    for key in sorted(additions, key=lambda item: allocation[item]["variant_id"]):
        addition = additions[key]
        ids = allocation[key]
        semantic_sha = _semantic_sha256(addition)
        preferred_label = _preferred_label_text(
            addition["preferred_label"], f"addition[{key}].preferred_label"
        )
        prior_occurrence = prior_source_by_key.get(key)
        if prior_occurrence is not None:
            # ATO rows are birth records.  Later label, alias, status, source,
            # or candidate metadata belongs in the catalog/event layers and
            # must never rewrite first-seen/raw authority for an allocated
            # occurrence.
            if prior_occurrence.get("semantic_payload_sha256") != semantic_sha:
                raise CatalogError(f"prior source semantic payload changed for {key}")
            new_source_rows.append(deepcopy(prior_occurrence))
        else:
            source_payload = {
                "curation_key": key,
                "candidate_keys": addition["candidate_keys"],
                "preferred_label": addition["preferred_label"],
                "statement": addition["statement"],
                "source_refs": addition["provenance_source_refs"],
            }
            locator = {
                "path": str(MANIFEST_PATH.relative_to(ROOT)),
                "parser": "structured_stage4_manifest/4.0",
                "curation_key": key,
                "source_refs": addition["provenance_source_refs"],
                "payload_sha256": stable_digest(
                    "awesome-theorems/stage4-source-payload/v4", source_payload
                ),
            }
            rendered_source_payload = pretty_json(source_payload)
            new_source_rows.append(
                {
                    "occurrence_id": ids["occurrence_id"],
                    "occurrence_key_sha256": stable_digest(
                        "awesome-theorems/stage4-occurrence-key/v4", {"curation_key": key}
                    ),
                    "idempotency_request_sha256": stable_digest(
                        "awesome-theorems/stage4-occurrence-key/v4", {"curation_key": key}
                    ),
                    "lifecycle": "current",
                    "first_seen_source_snapshot_sha256": snapshot_sha,
                    "birth_locator": locator,
                    "current_locator": locator,
                    "raw_fields": {
                        "discipline": addition["owner_domain"],
                        "name": preferred_label,
                        "statement": addition["statement"]["natural_language"],
                        "formal_status": addition["material_status"]["status"],
                        "proposer": "see provenance_source_refs",
                        "proposed_time": addition["material_status"]["as_of"],
                        "importance": "curated_gap_supplement",
                        "source_domain": addition["owner_domain"],
                    },
                    "raw_text": rendered_source_payload,
                    "raw_text_sha256": sha256_bytes(
                        rendered_source_payload.encode("utf-8")
                    ),
                    "source_status_authority": "reviewed_stage4_manifest",
                    "curation_key": key,
                    "candidate_keys": addition["candidate_keys"],
                    "source_refs": addition["provenance_source_refs"],
                    "semantic_payload_sha256": semantic_sha,
                }
            )

        if addition["family_action"] == "new_family" and ids["family_id"] not in family_by_id:
            family = {
                "family_id": ids["family_id"],
                "idempotency_request_sha256": stable_digest(
                    "awesome-theorems/stage4-family/v4", {"curation_key": key}
                ),
                "lexical_title_key": preferred_label.strip().casefold(),
                "display_titles": sorted(set([preferred_label, *addition["aliases"]])),
                "lifecycle": "current",
                "member_occurrence_ids": [],
                "historical_member_occurrence_ids": [],
                "identity_state": "stage4_curated_exact_family",
                "semantic_equivalence_asserted": True,
                "curation_key": key,
                "stage4_reviewed_member_occurrence_ids": [],
            }
            families.append(family)
            family_by_id[ids["family_id"]] = family
        family = family_by_id.get(ids["family_id"])
        if family is None:
            raise CatalogError(f"allocation for {key} has no family {ids['family_id']}")
        if ids["family_id"] in baseline_family_ids:
            # Baseline registry rows are immutable.  Reused-family membership
            # is an append-only edge, not an in-place rewrite of the v2 ATF.
            family_membership_extensions.append(
                {
                    "family_id": ids["family_id"],
                    "occurrence_id": ids["occurrence_id"],
                    "sense_id": ids["sense_id"],
                    "variant_id": ids["variant_id"],
                    "curation_key": key,
                    "evidence_inherited": False,
                }
            )
        else:
            for member_field in ("member_occurrence_ids", "historical_member_occurrence_ids"):
                family[member_field] = sorted(
                    set(family.get(member_field, [])) | {ids["occurrence_id"]}
                )
            family["stage4_reviewed_member_occurrence_ids"] = sorted(
                set(family.get("stage4_reviewed_member_occurrence_ids", []))
                | {ids["occurrence_id"]}
            )
            if preferred_label not in family.get("display_titles", []):
                family["display_titles"] = sorted(
                    set(family.get("display_titles", [])) | {preferred_label}
                )

        new_sense_rows.append(
            {
                "sense_id": ids["sense_id"],
                "idempotency_request_sha256": stable_digest(
                    "awesome-theorems/stage4-sense/v4", {"curation_key": key}
                ),
                "family_id": ids["family_id"],
                "bootstrap_occurrence_id": ids["occurrence_id"],
                "lifecycle": "current",
                "identity_state": "stage4_curated_exact_sense",
                "curation_key": key,
            }
        )
        new_variant_rows.append(
            {
                "variant_id": ids["variant_id"],
                "idempotency_request_sha256": stable_digest(
                    "awesome-theorems/stage4-variant/v4",
                    {"curation_key": key, "semantic_payload_sha256": semantic_sha},
                ),
                "sense_id": ids["sense_id"],
                "bootstrap_occurrence_id": ids["occurrence_id"],
                "lifecycle": "current",
                "identity_state": "stage4_curated_exact_variant",
                "curation_key": key,
                "semantic_payload_sha256": semantic_sha,
            }
        )

    all_sources = sorted(baseline_sources + new_source_rows, key=lambda row: row["occurrence_id"])
    senses.extend(new_sense_rows)
    variants.extend(new_variant_rows)
    families.sort(key=lambda row: row["family_id"])
    senses.sort(key=lambda row: row["sense_id"])
    variants.sort(key=lambda row: row["variant_id"])

    alias_occurrences = {row["target_occurrence_id"] for row in legacy_aliases}
    baseline_occurrence_ids = sorted(row["occurrence_id"] for row in baseline_sources)
    folded_occurrence_ids = sorted(set(baseline_occurrence_ids) - alias_occurrences)
    source_document = _base_document(
        SOURCE_RECORDS_V4_PATH,
        "awesome-theorems/source-records/4.0",
        inputs,
        {
            "allocated_occurrences": len(all_sources),
            "baseline_occurrences": len(baseline_sources),
            "stage4_additions": len(new_source_rows),
            "folded_baseline_occurrences": len(folded_occurrence_ids),
        },
        baseline_authority_sha256=source_v2["authority_sha256"],
        baseline_occurrence_ids=baseline_occurrence_ids,
        folded_occurrence_ids=folded_occurrence_ids,
        namespace_high_watermark=_max_id(all_sources, "occurrence_id", "ATO"),
        identity_policy={
            "append_only": True,
            "curation_key_is_idempotency_key_not_identifier": True,
            "semantic_change_requires_new_occurrence_and_variant": True,
        },
        records=all_sources,
    )

    # Explicit splits may arise either from lineage or an existing umbrella
    # disposition whose action is a split.  Both routes prohibit a default.
    split_children: defaultdict[str, set[str]] = defaultdict(set)
    split_candidates: defaultdict[str, set[str]] = defaultdict(set)
    current_supersedes_by_key = {
        addition["curation_key"]: relation["target_atv_id"]
        for addition in additions.values()
        for relation in addition["lineage"]
        if relation["relation_type"] == "supersedes"
    }
    if prior_registry is not None:
        for prior_redirect in redirects:
            if prior_redirect.get("relation_type") != "supersedes":
                continue
            key = prior_redirect.get("curation_key")
            prior_source_variant_id = prior_redirect.get(
                "source_variant_id", prior_redirect.get("from_variant_id")
            )
            if key not in current_supersedes_by_key:
                raise CatalogError(
                    f"prior lifecycle redirect removed from manifest: {prior_source_variant_id}"
                )
            if current_supersedes_by_key[key] != prior_source_variant_id:
                raise CatalogError(
                    f"prior lifecycle redirect rebound for {prior_source_variant_id}"
                )
            if allocation[key]["variant_id"] != prior_redirect.get(
                "target_variant_id", prior_redirect.get("to_variant_id")
            ):
                raise CatalogError(
                    f"prior lifecycle redirect target rebound for {prior_source_variant_id}"
                )

    for addition in additions.values():
        child = allocation[addition["curation_key"]]["variant_id"]
        for relation in addition["lineage"]:
            if relation["relation_type"] in {"split_child_of", "split_from"}:
                split_children[relation["target_atv_id"]].add(child)
                split_candidates[relation["target_atv_id"]].update(addition["candidate_keys"])
    disposition_by_key = {row["candidate_key"]: row for row in effective["dispositions"]}
    for candidate_key, disposition in disposition_by_key.items():
        if "split" not in disposition["resolution_action"].casefold():
            continue
        children = {
            allocation[child]["variant_id"]
            for child in disposition["child_keys"]
            if child in allocation
        }
        for parent in disposition["existing_atv_ids"]:
            split_children[parent].update(children)
            split_candidates[parent].add(candidate_key)
    for overlay in effective["overlays"]:
        if not overlay.get("child_keys"):
            continue
        parent = overlay["target_atv_id"]
        split_children[parent].update(
            allocation[child]["variant_id"] for child in overlay["child_keys"]
        )
        split_candidates[parent].update(overlay.get("candidate_keys", []))
    prior_split_by_source = {
        row.get("source_variant_id"): row for row in prior_splits
    }
    if len(prior_split_by_source) != len(prior_splits):
        raise CatalogError("prior registry has duplicate split sources")
    if prior_registry is not None:
        for source_variant_id, prior_split in prior_split_by_source.items():
            derived_children = sorted(split_children.get(source_variant_id, set()))
            if not derived_children:
                raise CatalogError(
                    f"prior lifecycle split removed from manifest: {source_variant_id}"
                )
            if derived_children != prior_split.get("child_variant_ids"):
                raise CatalogError(
                    f"prior lifecycle split rebound for {source_variant_id}"
                )
    splits = list(prior_splits)
    for parent in sorted(split_children):
        children = sorted(split_children[parent])
        # A single extracted/refined child is not a one-to-many lifecycle
        # split.  Keep that parent current and express the relationship only
        # through the child's typed lineage.
        if len(children) < 2:
            continue
        if parent in prior_split_by_source:
            if prior_split_by_source[parent].get("child_variant_ids") != children:
                raise CatalogError(f"prior lifecycle split rebound for {parent}")
            continue
        if any(
            row.get("source_variant_id", row.get("from_variant_id")) == parent
            for row in redirects
        ):
            raise CatalogError(f"lifecycle source {parent} cannot be both redirect and split")
        splits.append(
            {
                "split_id": "SPLIT-" + stable_digest(
                    "awesome-theorems/stage4-split/v4",
                    {"source_variant_id": parent, "child_variant_ids": children},
                )[:24].upper(),
                "source_variant_id": parent,
                "child_variant_ids": children,
                "default_child": None,
                "default_child_id": None,
                "evidence_inherited": False,
                "candidate_keys": sorted(split_candidates[parent]),
                "lifecycle": "active",
            }
        )

    for addition in additions.values():
        supersedes = [
            relation
            for relation in addition["lineage"]
            if relation["relation_type"] == "supersedes"
        ]
        if not supersedes:
            continue
        source_variant_id = supersedes[0]["target_atv_id"]
        target_variant_id = allocation[addition["curation_key"]]["variant_id"]
        existing_redirect = next(
            (
                row
                for row in redirects
                if row.get("source_variant_id", row.get("from_variant_id"))
                == source_variant_id
            ),
            None,
        )
        if existing_redirect is not None:
            if (
                existing_redirect.get(
                    "target_variant_id", existing_redirect.get("to_variant_id")
                )
                != target_variant_id
                or existing_redirect.get("curation_key") != addition["curation_key"]
                or existing_redirect.get("relation_type") != "supersedes"
                or existing_redirect.get("evidence_inherited") is not False
            ):
                raise CatalogError(
                    f"prior redirect for {source_variant_id} conflicts with supersedes lineage"
                )
            continue
        redirects.append(
            {
                "redirect_id": "REDIRECT-"
                + stable_digest(
                    "awesome-theorems/stage4-supersedes-redirect/v4",
                    {
                        "source_variant_id": source_variant_id,
                        "target_variant_id": target_variant_id,
                        "curation_key": addition["curation_key"],
                    },
                )[:24].upper(),
                "source_variant_id": source_variant_id,
                "target_variant_id": target_variant_id,
                "curation_key": addition["curation_key"],
                "relation_type": "supersedes",
                "default_child": None,
                "evidence_inherited": False,
                "lifecycle": "active",
            }
        )
    redirects.sort(
        key=lambda row: str(
            row.get("source_variant_id", row.get("from_variant_id", ""))
        )
    )

    registry_document = _base_document(
        REGISTRY_V4_PATH,
        "awesome-theorems/claim-id-registry/4.0",
        inputs,
        {
            "occurrences_allocated": len(all_sources),
            "families_allocated": len(families),
            "senses_allocated": len(senses),
            "variants_allocated": len(variants),
            "legacy_aliases": len(legacy_aliases),
            "redirects": len(redirects),
            "splits": len(splits),
            "stage4_additions": len(additions),
        },
        baseline_registry_authority_sha256=registry_v2["authority_sha256"],
        source_records_authority_sha256=source_document["authority_sha256"],
        allocation_policy={
            "append_only": True,
            "new_ids_use_prior_high_watermark_plus_one": True,
            "semantic_payload_change_reuses_id": False,
            "legacy_alias_rebinding_forbidden": True,
            "split_default_child": None,
            "split_evidence_inheritance": False,
        },
        namespace_high_watermarks={
            "ATO": _max_id(all_sources, "occurrence_id", "ATO"),
            "ATF": _max_id(families, "family_id", "ATF"),
            "ATS": _max_id(senses, "sense_id", "ATS"),
            "ATV": _max_id(variants, "variant_id", "ATV"),
        },
        families=families,
        family_membership_extensions=sorted(
            family_membership_extensions,
            key=lambda row: (row["family_id"], row["variant_id"]),
        ),
        senses=senses,
        variants=variants,
        legacy_aliases=legacy_aliases,
        redirects=redirects,
        splits=splits,
    )
    return allocation, source_document, registry_document


def _base_document(
    path: Path,
    schema_version: str,
    inputs: Mapping[str, Any],
    counts: Mapping[str, Any],
    **payload: Any,
) -> dict[str, Any]:
    authoritative_inputs = deepcopy(inputs["authoritative_inputs"])
    document: dict[str, Any] = {
        "schema_version": schema_version,
        "artifact": path.name,
        "generated_by": GENERATED_BY,
        "authoritative_inputs": authoritative_inputs,
        "authoritative_inputs_sha256": stable_digest(
            "awesome-theorems/stage4-authoritative-inputs/v4", authoritative_inputs
        ),
        "counts": dict(counts),
        **payload,
    }
    return _seal(document)


def _build_stage_registry(
    registry: Mapping[str, Any], inputs: Mapping[str, Any]
) -> dict[str, Any]:
    mappings = []
    for variant in registry["variants"]:
        variant_id = variant["variant_id"]
        ordinal = _parse_ordinal(variant_id, "ATV")
        mappings.append(
            {
                "variant_id": variant_id,
                "stage_claim_id": f"S4-CLM-{ordinal:08d}",
                "stage_id": f"S4-CLM-{ordinal:08d}",
                "ordinal": ordinal,
                "lifecycle": variant.get("lifecycle", "current"),
                "curation_key": variant.get("curation_key"),
            }
        )
    mappings.sort(key=lambda row: row["variant_id"])
    return _base_document(
        STAGE_REGISTRY_V4_PATH,
        "awesome-theorems/stage4-claim-id-registry/4.0",
        inputs,
        {"mappings": len(mappings), "baseline": BASELINE_VARIANTS, "new": len(mappings) - BASELINE_VARIANTS},
        numbering_policy={
            "format": "S4-CLM-########",
            "ordinal_equals_atv_ordinal": True,
            "encodes_domain_kind_or_status": False,
            "bijection": True,
        },
        mappings=mappings,
    )


def _redirect_map(registry: Mapping[str, Any]) -> dict[str, str]:
    output: dict[str, str] = {}
    for row in registry.get("redirects", []):
        source = row.get("source_variant_id", row.get("from_variant_id"))
        target = row.get("target_variant_id", row.get("to_variant_id"))
        if isinstance(source, str) and isinstance(target, str):
            output[source] = target
    return output


def _split_map(registry: Mapping[str, Any]) -> dict[str, list[str]]:
    output: dict[str, list[str]] = {}
    for row in registry.get("splits", []):
        source = row.get("source_variant_id")
        children = row.get("child_variant_ids")
        if isinstance(source, str) and isinstance(children, list):
            output[source] = list(children)
    return output


def _terminal_variant_ids(
    variant_id: str,
    redirects: Mapping[str, str],
    splits: Mapping[str, list[str]],
    trail: tuple[str, ...] = (),
) -> list[str]:
    if variant_id in trail:
        raise CatalogError(f"lifecycle resolution cycle reaches {variant_id}")
    next_trail = (*trail, variant_id)
    if variant_id in redirects:
        return _terminal_variant_ids(
            redirects[variant_id], redirects, splits, next_trail
        )
    if variant_id in splits:
        terminals: list[str] = []
        for child in splits[variant_id]:
            terminals.extend(
                _terminal_variant_ids(child, redirects, splits, next_trail)
            )
        return terminals
    return [variant_id]


def _current_variant_resolution(
    variant_id: str,
    redirects: Mapping[str, str],
    splits: Mapping[str, list[str]],
) -> dict[str, Any]:
    terminals = list(dict.fromkeys(_terminal_variant_ids(variant_id, redirects, splits)))
    kind = "redirect" if variant_id in redirects else "split" if variant_id in splits else "current"
    return {
        "kind": kind,
        "terminal_atv_ids": terminals,
        "terminal_stage_ids": [_stage_id(item) for item in terminals],
        "default_child": None,
        "evidence_inherited": False,
    }


def _validate_previous_lifecycle_artifacts(
    previous: Mapping[str, Mapping[str, Any]],
    *,
    current_authoritative_inputs: list[dict[str, Any]],
    effective_manifest: Mapping[str, Any],
) -> None:
    """Authenticate the prior four-artifact lifecycle generation as one unit."""

    required_names = {
        SOURCE_RECORDS_V4_PATH.name,
        REGISTRY_V4_PATH.name,
        MIGRATION_V4_PATH.name,
        CANDIDATE_DISPOSITIONS_V4_PATH.name,
    }
    if set(previous) != required_names:
        raise CatalogError(
            "prior v4 lifecycle authority must contain exactly source, registry, "
            "migration, and candidate artifacts"
        )

    source = previous[SOURCE_RECORDS_V4_PATH.name]
    registry = previous[REGISTRY_V4_PATH.name]
    migration = previous[MIGRATION_V4_PATH.name]
    candidates = previous[CANDIDATE_DISPOSITIONS_V4_PATH.name]
    _validate_sealed_lifecycle_rows(registry, "prior Claim_ID_Registry_v4")

    # A valid seal on each file is insufficient: all four must describe the
    # same authoritative-input generation, and a sealed Stage4 run may not
    # reinterpret an older lifecycle snapshot against newer manifest bytes.
    common_inputs = _require_list(
        source.get("authoritative_inputs"),
        "prior Source_Records_v4.authoritative_inputs",
    )
    common_inputs_sha256 = source.get("authoritative_inputs_sha256")
    for name in sorted(required_names):
        document = previous[name]
        if (
            document.get("authoritative_inputs") != common_inputs
            or document.get("authoritative_inputs_sha256") != common_inputs_sha256
        ):
            raise CatalogError(
                f"prior v4 four-artifact authoritative_inputs generation differs at {name}"
            )
    if common_inputs != current_authoritative_inputs:
        raise CatalogError(
            "prior v4 four-artifact authoritative_inputs differ from the current sealed inventory"
        )

    authority_targets = {
        "source_records_authority_sha256": source,
        "claim_id_registry_authority_sha256": registry,
        "registry_authority_sha256": registry,
        "claim_id_migration_authority_sha256": migration,
        "migration_authority_sha256": migration,
        "candidate_dispositions_authority_sha256": candidates,
    }
    for name in sorted(required_names):
        document = previous[name]
        for binding, target in authority_targets.items():
            if binding in document and document[binding] != target.get("authority_sha256"):
                raise CatalogError(
                    f"prior v4 artifact authority binding {name}.{binding} is stale"
                )

    variant_rows = _require_object_rows(
        registry.get("variants"), "prior Claim_ID_Registry_v4.variants"
    )
    variants = {row.get("variant_id"): row for row in variant_rows}
    if None in variants or len(variants) != len(variant_rows):
        raise CatalogError("prior registry has missing/duplicate variant IDs")
    variant_ids = set(variants)
    variants_by_key: dict[str, dict[str, Any]] = {}
    for row in variant_rows:
        key = row.get("curation_key")
        if key is None:
            continue
        if not isinstance(key, str) or key in variants_by_key:
            raise CatalogError("prior registry has duplicate/invalid curation keys")
        variants_by_key[key] = row

    redirect_rows = _require_object_rows(
        registry.get("redirects"), "prior Claim_ID_Registry_v4.redirects"
    )
    split_rows = _require_object_rows(
        registry.get("splits"), "prior Claim_ID_Registry_v4.splits"
    )
    redirects: dict[str, str] = {}
    for row in redirect_rows:
        source = row.get("source_variant_id", row.get("from_variant_id"))
        target = row.get("target_variant_id", row.get("to_variant_id"))
        if source in redirects or source not in variant_ids or target not in variant_ids:
            raise CatalogError("prior registry has a duplicate/unknown redirect edge")
        if row.get("default_child") is not None or row.get("evidence_inherited") is not False:
            raise CatalogError(f"prior registry redirect {source} violates lifecycle typing")
        redirects[source] = target
    splits: dict[str, list[str]] = {}
    for row in split_rows:
        source = row.get("source_variant_id")
        children = row.get("child_variant_ids")
        if (
            source in splits
            or source not in variant_ids
            or not isinstance(children, list)
            or len(children) < 2
            or len(children) != len(set(children))
            or any(child not in variant_ids for child in children)
        ):
            raise CatalogError("prior registry has a duplicate/invalid split edge")
        if row.get("default_child", row.get("default_child_id")) is not None:
            raise CatalogError(f"prior registry split {source} assigns a default child")
        if row.get("evidence_inherited") is not False:
            raise CatalogError(f"prior registry split {source} inherits evidence")
        splits[source] = list(children)
    if set(redirects) & set(splits):
        raise CatalogError("prior registry binds one source as both redirect and split")

    migration_rows = _require_object_rows(
        migration.get("migrations"), "prior Claim_ID_Migration_v2_to_v4.migrations"
    )
    migrations = {row.get("variant_id"): row for row in migration_rows}
    if None in migrations or len(migrations) != len(migration_rows):
        raise CatalogError("prior migration has missing/duplicate variant rows")
    if set(migrations) != variant_ids:
        raise CatalogError("prior migration is not total over prior registry variants")
    lifecycle_sources = set(redirects) | set(splits)
    migration_noncurrent: set[str] = set()
    for variant_id, row in migrations.items():
        resolution = _require_object(
            row.get("current_resolution"),
            f"prior migration[{variant_id}].current_resolution",
        )
        kind = resolution.get("kind")
        if kind not in {"current", "redirect", "split"}:
            raise CatalogError(f"prior migration {variant_id} has invalid lifecycle kind")
        if kind != "current":
            migration_noncurrent.add(variant_id)
        expected = _current_variant_resolution(variant_id, redirects, splits)
        if (
            resolution.get("kind") != expected["kind"]
            or resolution.get("target_stage_claim_ids")
            != expected["terminal_stage_ids"]
            or resolution.get("default_child") is not None
            or resolution.get("evidence_inherited") is not False
        ):
            raise CatalogError(
                f"prior migration lifecycle resolution drifted for {variant_id}"
            )
    if migration_noncurrent != lifecycle_sources:
        raise CatalogError(
            "prior registry lifecycle sources and migration non-current resolutions differ"
        )

    candidate_rows = _require_object_rows(
        candidates.get("dispositions"), "prior Candidate_Dispositions_v4.dispositions"
    )
    candidates_by_key: dict[str, dict[str, Any]] = {}
    for row in candidate_rows:
        key = row.get("candidate_key")
        if not isinstance(key, str) or key in candidates_by_key:
            raise CatalogError("prior candidate dispositions have missing/duplicate keys")
        candidates_by_key[key] = row

    manifest_dispositions: dict[str, dict[str, Any]] = {}
    for raw in _require_object_rows(
        effective_manifest.get("dispositions"), "effective manifest.dispositions"
    ):
        row = {key: value for key, value in raw.items() if not key.startswith("_")}
        key = _require_string(row.get("candidate_key"), "effective candidate_key")
        if key in manifest_dispositions:
            raise CatalogError(f"effective manifest duplicates candidate {key}")
        manifest_dispositions[key] = row
    if set(candidates_by_key) != set(manifest_dispositions):
        raise CatalogError(
            "prior candidate disposition key set differs from the current sealed manifest"
        )

    for key, manifest_row in manifest_dispositions.items():
        row = candidates_by_key[key]
        child_keys = _require_list(
            manifest_row.get("child_keys"), f"effective candidate[{key}].child_keys"
        )
        try:
            allocated = [variants_by_key[child]["variant_id"] for child in child_keys]
        except KeyError as error:
            raise CatalogError(
                f"prior candidate {key} names an unallocated child {error.args[0]}"
            ) from error
        existing = _require_list(
            manifest_row.get("existing_atv_ids"),
            f"effective candidate[{key}].existing_atv_ids",
        )
        targets = [*existing, *allocated]
        if any(target not in variant_ids for target in targets):
            raise CatalogError(f"prior candidate {key} targets an unknown registry variant")
        if row.get("allocated_atv_ids") != allocated:
            raise CatalogError(f"prior candidate {key} allocated ATV history drifted")
        if row.get("target_atv_ids") != targets:
            raise CatalogError(f"prior candidate {key} target ATV history drifted")
        if row.get("target_stage_ids") != [_stage_id(item) for item in targets]:
            raise CatalogError(f"prior candidate {key} target Stage4 history drifted")
        terminals = list(
            dict.fromkeys(
                terminal
                for target in targets
                for terminal in _terminal_variant_ids(target, redirects, splits)
            )
        )
        if (
            row.get("terminal_atv_ids") != terminals
            or row.get("terminal_stage_ids")
            != [_stage_id(item) for item in terminals]
        ):
            raise CatalogError(
                f"prior candidate lifecycle resolution drifted for {key}"
            )
        expected_terminal_children = [
            {
                "curation_key": variants[item].get("curation_key"),
                "variant_id": item,
                "stage_claim_id": _stage_id(item),
                "lifecycle": "active",
            }
            for item in terminals
        ]
        if row.get("terminal_children") != expected_terminal_children:
            raise CatalogError(f"prior candidate terminal child view drifted for {key}")


def _build_migration(
    source_records: Mapping[str, Any],
    registry: Mapping[str, Any],
    stage_registry: Mapping[str, Any],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    baseline_ids = {row["variant_id"] for row in inputs["registry_v2"]["variants"]}
    aliases_by_variant: defaultdict[str, list[str]] = defaultdict(list)
    for alias in registry["legacy_aliases"]:
        aliases_by_variant[alias["target_variant_id"]].append(alias["alias_id"])
    redirects = _redirect_map(registry)
    splits = _split_map(registry)
    variant_by_id = {row["variant_id"]: row for row in registry["variants"]}
    migrations = []
    for mapping in stage_registry["mappings"]:
        variant_id = mapping["variant_id"]
        if variant_id in splits:
            terminal_ids = list(
                dict.fromkeys(
                    _terminal_variant_ids(variant_id, redirects, splits)
                )
            )
            resolution = {
                "kind": "split",
                "target_stage_claim_ids": [_stage_id(item) for item in terminal_ids],
                "default_child": None,
                "evidence_inherited": False,
            }
        elif variant_id in redirects:
            terminal_ids = list(
                dict.fromkeys(
                    _terminal_variant_ids(variant_id, redirects, splits)
                )
            )
            resolution = {
                "kind": "redirect",
                "target_stage_claim_ids": [_stage_id(item) for item in terminal_ids],
                "default_child": None,
                "evidence_inherited": False,
            }
        else:
            resolution = {
                "kind": "current",
                "target_stage_claim_ids": [mapping["stage_claim_id"]],
                "default_child": None,
                "evidence_inherited": False,
            }
        migrations.append(
            {
                "v2_variant_id": variant_id if variant_id in baseline_ids else None,
                "variant_id": variant_id,
                "stage_claim_id": mapping["stage_claim_id"],
                "stage_id": mapping["stage_claim_id"],
                "action": "carry" if variant_id in baseline_ids else "new",
                "legacy_alias_ids": sorted(aliases_by_variant.get(variant_id, [])),
                "current_resolution": resolution,
            }
        )
    legacy_alias_migrations = [
        {
            "alias_id": row["alias_id"],
            "historical_target_variant_id": row["target_variant_id"],
            "historical_stage_claim_id": _stage_id(row["target_variant_id"]),
            "rebound": False,
        }
        for row in sorted(registry["legacy_aliases"], key=lambda item: item["alias_id"])
    ]
    variant_by_occurrence = {
        row["bootstrap_occurrence_id"]: row["variant_id"] for row in registry["variants"]
    }
    folded_variant_ids = sorted(
        variant_by_occurrence[occurrence]
        for occurrence in source_records["folded_occurrence_ids"]
    )
    return _base_document(
        MIGRATION_V4_PATH,
        "awesome-theorems/claim-id-migration-v2-to-v4/4.0",
        inputs,
        {
            "migrations": len(migrations),
            "baseline_carry": len(baseline_ids),
            "new_stage4": len(migrations) - len(baseline_ids),
            "legacy_aliases": len(legacy_alias_migrations),
            "folded_occurrences": len(folded_variant_ids),
        },
        policy={
            "historical_alias_target_immutable": True,
            "current_resolution_separate": True,
            "split_has_default_child": False,
            "stage_number_is_bijection_over_all_atv": True,
        },
        migrations=migrations,
        legacy_alias_migrations=legacy_alias_migrations,
        folded_occurrence_ids=list(source_records["folded_occurrence_ids"]),
        folded_variant_ids=folded_variant_ids,
    )


def _build_candidate_dispositions(
    effective: Mapping[str, Any],
    allocation: Mapping[str, Mapping[str, str]],
    registry: Mapping[str, Any],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    coverage_by_key = inputs["coverage_by_key"]
    resolution_by_key = {
        row["candidate_key"]: row for row in effective["collision_resolutions"]
    }
    redirects = _redirect_map(registry)
    splits = _split_map(registry)
    variant_by_id = {row["variant_id"]: row for row in registry["variants"]}
    rows = []
    for disposition in effective["dispositions"]:
        key = disposition["candidate_key"]
        allocated = [allocation[child]["variant_id"] for child in disposition["child_keys"]]
        targets = [*disposition["existing_atv_ids"], *allocated]
        terminal_targets = list(
            dict.fromkeys(
                terminal
                for target in targets
                for terminal in _terminal_variant_ids(target, redirects, splits)
            )
        )
        row = deepcopy(disposition)
        row.update(
            {
                "allocated_atv_ids": allocated,
                "target_atv_ids": targets,
                "target_stage_ids": [_stage_id(item) for item in targets],
                "terminal_atv_ids": terminal_targets,
                "terminal_stage_ids": [_stage_id(item) for item in terminal_targets],
                "terminal_children": [
                    {
                        "curation_key": variant_by_id[item].get("curation_key"),
                        "variant_id": item,
                        "stage_claim_id": _stage_id(item),
                        "lifecycle": "active",
                    }
                    for item in terminal_targets
                ],
                "children": [
                    {
                        "curation_key": child,
                        "variant_id": allocation[child]["variant_id"],
                        "stage_claim_id": _stage_id(allocation[child]["variant_id"]),
                        "lifecycle": (
                            "redirected"
                            if allocation[child]["variant_id"] in redirects
                            else "split"
                            if allocation[child]["variant_id"] in splits
                            else "active"
                        ),
                        "current_resolution": _current_variant_resolution(
                            allocation[child]["variant_id"], redirects, splits
                        ),
                    }
                    for child in disposition["child_keys"]
                ],
                "candidate_inventory_record": deepcopy(coverage_by_key.get(key)),
                "collision_resolution": deepcopy(resolution_by_key.get(key)),
                "disposition_sha256": stable_digest(
                    "awesome-theorems/stage4-candidate-disposition/v4", disposition
                ),
            }
        )
        rows.append(row)
    origin_counts = Counter(row["origin"] for row in rows)
    disposition_counts = Counter(row["disposition"] for row in rows)
    return _base_document(
        CANDIDATE_DISPOSITIONS_V4_PATH,
        "awesome-theorems/candidate-dispositions/4.0",
        inputs,
        {
            "total": len(rows),
            "frozen": FROZEN_CANDIDATE_KEYS,
            "stage4_discovery": origin_counts.get("stage4_discovery", 0),
            "v2_missing": origin_counts.get("v2_missing", 0),
            "v2_collision": origin_counts.get("v2_collision", 0),
            "v3_delta": origin_counts.get("v3_delta", 0),
            "new_family": disposition_counts.get("new_family", 0),
            "existing_family": disposition_counts.get("existing_family", 0),
            "collision": disposition_counts.get("collision", 0),
            "nonclaim": disposition_counts.get("nonclaim", 0),
        },
        completion_boundary={
            "frozen_candidate_keys": FROZEN_CANDIDATE_KEYS,
            "all_frozen_keys_dispositioned": True,
            "extra_discoveries_require_stable_keys": True,
            "candidate_presence_is_not_truth_credit": True,
        },
        dispositions=rows,
    )


def _proposal_id(domain: str, legacy_id: str, index: int) -> str:
    safe_domain = {"mathematics": "M", "physics": "P", "computer_science": "C"}[domain]
    return f"RPR-{safe_domain}-{index:04d}-{legacy_id}"


def _build_repair_dispositions(
    effective: Mapping[str, Any], inputs: Mapping[str, Any]
) -> dict[str, Any]:
    applied: defaultdict[str, list[str]] = defaultdict(list)
    for row in [*effective["additions"], *effective["overlays"]]:
        for proposal_id in row.get("repair_proposal_refs", []):
            applied[str(proposal_id)].append(row["curation_key"])
    records = []
    for domain in ("mathematics", "physics", "computer_science"):
        path = REPAIR_PATHS[domain]
        proposals = _repair_rows(inputs["repairs"][domain], str(path.relative_to(ROOT)))
        for index, proposal in enumerate(proposals, start=1):
            legacy_id = _require_string(proposal.get("legacy_id"), f"{path.name} proposal {index}.legacy_id")
            proposal_id = _proposal_id(domain, legacy_id, index)
            records.append(
                {
                    "proposal_id": proposal_id,
                    "domain": domain,
                    "source_path": str(path.relative_to(ROOT)),
                    "source_index": index,
                    "legacy_id": legacy_id,
                    "proposal_sha256": stable_digest(
                        "awesome-theorems/stage4-repair-proposal/v4", proposal
                    ),
                    "proposal": deepcopy(proposal),
                    "disposition": "applied_by_explicit_curation" if applied[proposal_id] else "proposal_only_preserved",
                    "applied_by_curation_keys": sorted(applied[proposal_id]),
                    "grants_truth_credit": False,
                }
            )
    unknown_refs = sorted(set(applied) - {row["proposal_id"] for row in records})
    if unknown_refs:
        raise CatalogError(f"curation cites unknown repair proposal {unknown_refs[0]}")
    return _base_document(
        REPAIR_DISPOSITIONS_V4_PATH,
        "awesome-theorems/repair-proposal-dispositions/4.0",
        inputs,
        {
            "total": len(records),
            "mathematics": sum(row["domain"] == "mathematics" for row in records),
            "physics": sum(row["domain"] == "physics" for row in records),
            "computer_science": sum(row["domain"] == "computer_science" for row in records),
            "applied_by_explicit_curation": sum(row["disposition"] == "applied_by_explicit_curation" for row in records),
            "proposal_only_preserved": sum(row["disposition"] == "proposal_only_preserved" for row in records),
        },
        policy={
            "proposal_presence_is_review_credit": False,
            "proposal_presence_is_truth_credit": False,
            "all_v2_proposals_conserved": True,
        },
        dispositions=records,
    )


def _baseline_catalog_records(
    inputs: Mapping[str, Any], registry: Mapping[str, Any]
) -> list[dict[str, Any]]:
    v2_atv = {
        row["record_id"]: row
        for row in inputs["catalog_v2"]["records"]
        if row.get("record_type") == "ATV"
    }
    senses = {row["sense_id"]: row for row in registry["senses"]}
    aliases_by_variant: defaultdict[str, list[str]] = defaultdict(list)
    for alias in registry["legacy_aliases"]:
        aliases_by_variant[alias["target_variant_id"]].append(alias["alias_id"])
    output = []
    for variant in inputs["registry_v2"]["variants"]:
        variant_id = variant["variant_id"]
        raw = v2_atv.get(variant_id)
        if raw is None:
            raise CatalogError(f"v2 catalog lacks variant record {variant_id}")
        kind = raw.get("claim_kind", {})
        identity = raw.get("identity", {})
        tags = list(identity.get("discipline_tags", []))
        human = raw.get("statuses", {}).get("human_truth", {})
        sense = senses[variant["sense_id"]]
        source_occurrence = variant["bootstrap_occurrence_id"]
        output.append(
            {
                "variant_id": variant_id,
                "stage_claim_id": _stage_id(variant_id),
                "stage_id": _stage_id(variant_id),
                "source_occurrence_id": source_occurrence,
                "family_id": sense["family_id"],
                "sense_id": variant["sense_id"],
                "preferred_label": identity.get("preferred_label", variant_id),
                "aliases": [
                    label.get("text")
                    for label in identity.get("labels", [])
                    if isinstance(label, dict) and label.get("text") != identity.get("preferred_label")
                ],
                "legacy_alias_ids": sorted(aliases_by_variant.get(variant_id, [])),
                "owner_domain": tags[0] if tags else "unreviewed",
                "membership_domains": tags,
                "record_role": "unreviewed_source_variant",
                # Machine triage is retained as evidence but is not promoted
                # into the curated theorem/open predicates.  A Stage4 overlay
                # may explicitly establish a current kind for this ATV.
                "claim_kind": "unknown",
                "current_claim_kind": "unknown",
                "machine_triage_claim_kind": deepcopy(kind),
                "historical_kind": kind.get("historical_kind", "unreviewed"),
                "atomicity": kind.get("atomicity", "unknown"),
                "truth_apt": kind.get("truth_apt", "unknown"),
                "statement": deepcopy(raw.get("exact_statement", {})),
                "material_status": {
                    "status": human.get("status", "unknown"),
                    "as_of": human.get("as_of"),
                    "basis": human.get("scope_note", "Inherited v2 machine triage."),
                    "source_refs": deepcopy(human.get("source_refs", [])),
                },
                "status_events": [],
                "provenance_source_refs": deepcopy(raw.get("provenance", {}).get("evidence_refs", [])),
                "source_refs": deepcopy(raw.get("provenance", {}).get("evidence_refs", [])),
                "rights_status": raw.get("license", {}).get("status", "unknown"),
                "lineage": deepcopy(raw.get("relations", [])),
                "lifecycle": "active" if variant.get("lifecycle", "current") == "current" else variant.get("lifecycle"),
                "registry_lifecycle": variant.get("lifecycle", "current"),
                "curation_state": "inherited_v2_machine_triage",
                "curation_key": None,
                "candidate_keys": [],
                "overlay_keys": [],
            }
        )
    return output


def _build_catalog(
    effective: Mapping[str, Any],
    allocation: Mapping[str, Mapping[str, str]],
    registry: Mapping[str, Any],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    records = _baseline_catalog_records(inputs, registry)
    by_variant = {row["variant_id"]: row for row in records}
    for addition in effective["additions"]:
        key = addition["curation_key"]
        ids = allocation[key]
        preferred_label = _preferred_label_text(
            addition["preferred_label"], f"addition[{key}].preferred_label"
        )
        canonical_kind = _canonical_claim_kind(addition["claim_kind"])
        lineage = []
        for relation in addition["lineage"]:
            lineage.append(
                {
                    **deepcopy(relation),
                    "target_stage_claim_id": _stage_id(relation["target_atv_id"]),
                }
            )
        record = {
            "variant_id": ids["variant_id"],
            "stage_claim_id": _stage_id(ids["variant_id"]),
            "stage_id": _stage_id(ids["variant_id"]),
            "source_occurrence_id": ids["occurrence_id"],
            "family_id": ids["family_id"],
            "sense_id": ids["sense_id"],
            "preferred_label": preferred_label,
            "labels": _preferred_label_map(addition["preferred_label"]),
            "aliases": deepcopy(addition["aliases"]),
            "legacy_alias_ids": [],
            "owner_domain": addition["owner_domain"],
            "membership_domains": deepcopy(addition["membership_domains"]),
            "record_role": addition["record_role"],
            "claim_kind": canonical_kind,
            "current_claim_kind": canonical_kind,
            "claim_subtype": (
                addition["claim_kind"]
                if canonical_kind != addition["claim_kind"]
                else None
            ),
            "historical_kind": addition["historical_kind"],
            "atomicity": addition["atomicity"],
            "truth_apt": addition["record_role"] == "claim",
            "statement": deepcopy(addition["statement"]),
            "material_status": deepcopy(addition["material_status"]),
            "status_events": [deepcopy(addition["material_status"])],
            "provenance_source_refs": deepcopy(addition["provenance_source_refs"]),
            "source_refs": deepcopy(addition["provenance_source_refs"]),
            "rights_status": addition["rights_status"],
            "lineage": lineage,
            "lifecycle": "active",
            "curation_state": "stage4_curated_addition",
            "curation_key": key,
            "candidate_keys": deepcopy(addition["candidate_keys"]),
            "overlay_keys": [],
            "semantic_payload_sha256": _semantic_sha256(addition),
        }
        records.append(record)
        by_variant[ids["variant_id"]] = record

    for addition in effective["additions"]:
        supersedes = [
            relation
            for relation in addition["lineage"]
            if relation["relation_type"] == "supersedes"
        ]
        if not supersedes:
            continue
        old_variant_id = supersedes[0]["target_atv_id"]
        new_variant_id = allocation[addition["curation_key"]]["variant_id"]
        old_record = by_variant[old_variant_id]
        old_record["lifecycle"] = "redirected"
        old_record["lifecycle_target_stage_ids"] = [_stage_id(new_variant_id)]
        old_record["redirected_by_curation_key"] = addition["curation_key"]

    for overlay in effective["overlays"]:
        target = by_variant[overlay["target_atv_id"]]
        if "preferred_label" in overlay:
            target["preferred_label"] = _preferred_label_text(
                overlay["preferred_label"], f"overlay[{overlay['curation_key']}].preferred_label"
            )
            target["labels"] = _preferred_label_map(overlay["preferred_label"])
        if "claim_kind" in overlay:
            canonical_kind = _canonical_claim_kind(overlay["claim_kind"])
            target["claim_kind"] = canonical_kind
            target["current_claim_kind"] = canonical_kind
            target["claim_subtype"] = (
                overlay["claim_kind"]
                if canonical_kind != overlay["claim_kind"]
                else None
            )
        if "historical_kind" in overlay:
            target["historical_kind"] = overlay["historical_kind"]
        if "material_status" in overlay:
            target["material_status"] = deepcopy(overlay["material_status"])
            target["status_events"].append(deepcopy(overlay["material_status"]))
        if "membership_domains_add" in overlay:
            target["membership_domains"] = sorted(
                set(target["membership_domains"])
                | set(overlay["membership_domains_add"])
            )
        target["source_refs"] = sorted(set(target["source_refs"]) | set(overlay["source_refs"]))
        target["provenance_source_refs"] = sorted(
            set(target["provenance_source_refs"]) | set(overlay["source_refs"])
        )
        target["candidate_keys"] = sorted(
            set(target["candidate_keys"]) | set(overlay["candidate_keys"])
        )
        target["overlay_keys"].append(overlay["curation_key"])
        if overlay.get("child_keys"):
            target["split_children"] = [
                {
                    "curation_key": child,
                    "variant_id": allocation[child]["variant_id"],
                    "stage_claim_id": _stage_id(allocation[child]["variant_id"]),
                    "evidence_inherited": False,
                }
                for child in overlay["child_keys"]
            ]
        target["curation_state"] = "stage4_curated_overlay"

    records.sort(key=lambda row: row["variant_id"])
    state_counts = Counter(row["curation_state"] for row in records)
    return _base_document(
        CATALOG_V4_PATH,
        "awesome-theorems/claim-catalog/4.0",
        inputs,
        {
            "records": len(records),
            "baseline_machine_triage": state_counts["inherited_v2_machine_triage"],
            "curated_additions": state_counts["stage4_curated_addition"],
            "curated_overlays": state_counts["stage4_curated_overlay"],
        },
        trust_boundary={
            "baseline_v2_records_remain_machine_triage": True,
            "candidate_disposition_is_not_truth_credit": True,
            "only_stage4_additions_and_overlays_are_curated": True,
            "completion_scope": "frozen_candidate_supplement_and_full_number_migration",
        },
        sources=deepcopy(effective["sources"]),
        records=records,
    )


def _status_bucket(record: Mapping[str, Any]) -> str:
    status = str(record.get("material_status", {}).get("status", "unknown")).strip().casefold()
    mapping = {
        "proved": "proved",
        "proven": "proved",
        "established": "proved",
        "true": "proved",
        "resolved_proved": "proved",
        "confirmed": "proved",
        "open": "open",
        "unresolved": "open",
        "open_problem": "open",
        "refuted": "refuted",
        "disproved": "refuted",
        "false": "refuted",
        "counterexample": "refuted",
        "independent": "independent",
        "independence": "independent",
        "partial": "partial",
        "partially_resolved": "partial",
        "disputed": "disputed",
        "contested": "disputed",
        "conditional": "conditional",
        "conditional_open": "conditional",
        "conditional_assumption": "conditional",
        "assumption": "conditional",
        "unknown": "unknown",
        "unreviewed": "unknown",
        "missing": "unknown",
        "none": "unknown",
        "": "unknown",
    }
    return mapping.get(status, status.replace(" ", "_") or "unknown")


def _is_open_record(record: Mapping[str, Any]) -> bool:
    return (
        record.get("lifecycle", "active") == "active"
        and not record.get("split_children")
        and record.get("record_role") == "claim"
        and record.get("atomicity") == "atomic"
        and record.get("truth_apt") is True
        and _status_bucket(record)
        in {"open", "partial", "independent", "conditional", "disputed"}
    )


def _is_theorem_record(record: Mapping[str, Any]) -> bool:
    return (
        record.get("lifecycle", "active") == "active"
        and not record.get("split_children")
        and record.get("record_role") == "claim"
        and record.get("atomicity") == "atomic"
        and record.get("truth_apt") is True
        and _status_bucket(record) == "proved"
    )


def _projection_row(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_claim_id": record["stage_claim_id"],
        "stage_id": record["stage_claim_id"],
        "variant_id": record["variant_id"],
        "preferred_label": record["preferred_label"],
        "owner_domain": record["owner_domain"],
        "record_role": record["record_role"],
        "current_claim_kind": record["current_claim_kind"],
        "historical_kind": record["historical_kind"],
        "material_status": deepcopy(record["material_status"]),
        "status_bucket": _status_bucket(record),
        "statement": deepcopy(record["statement"]),
        "source_refs": deepcopy(record["source_refs"]),
        "curation_state": record["curation_state"],
        "lifecycle": record.get("lifecycle", "active"),
        "lifecycle_target_stage_ids": deepcopy(
            record.get("lifecycle_target_stage_ids", [])
        ),
        "redirected_by_curation_key": record.get("redirected_by_curation_key"),
    }


def _build_projections(
    catalog: Mapping[str, Any], inputs: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    theorem_rows = [
        _projection_row(row) for row in catalog["records"] if _is_theorem_record(row)
    ]
    open_rows = [
        _projection_row(row) for row in catalog["records"] if _is_open_record(row)
    ]
    status_rows = []
    for row in catalog["records"]:
        projected = _projection_row(row)
        projected["status_event_count"] = len(row.get("status_events", []))
        status_rows.append(projected)
    theorem_rows.sort(key=lambda row: row["stage_claim_id"])
    open_rows.sort(key=lambda row: row["stage_claim_id"])
    status_rows.sort(key=lambda row: row["stage_claim_id"])
    theorem = _base_document(
        THEOREM_JSON_V4_PATH,
        "awesome-theorems/theorem-list/4.0",
        inputs,
        {
            "records": len(theorem_rows),
            "curated": sum(row["curation_state"] != "inherited_v2_machine_triage" for row in theorem_rows),
            "inherited_machine_triage": sum(row["curation_state"] == "inherited_v2_machine_triage" for row in theorem_rows),
        },
        projection_policy={
            "query": "current_claim_kind in theorem-kind set and not open-kind/status",
            "machine_triage_rows_are_labeled": True,
        },
        stage_claim_ids=[row["stage_claim_id"] for row in theorem_rows],
        records=theorem_rows,
    )
    open_document = _base_document(
        OPEN_JSON_V4_PATH,
        "awesome-theorems/conjecture-hypothesis-open-list/4.0",
        inputs,
        {
            "records": len(open_rows),
            "curated": sum(row["curation_state"] != "inherited_v2_machine_triage" for row in open_rows),
            "inherited_machine_triage": sum(row["curation_state"] == "inherited_v2_machine_triage" for row in open_rows),
        },
        projection_policy={
            "query": "current conjecture/hypothesis/open/assumption kind or material open-status",
            "historical_kind_does_not_imply_current_open_status": True,
        },
        stage_claim_ids=[row["stage_claim_id"] for row in open_rows],
        records=open_rows,
    )
    bucket_counts = Counter(row["status_bucket"] for row in status_rows)
    status = _base_document(
        STATUS_JSON_V4_PATH,
        "awesome-theorems/status-index/4.0",
        inputs,
        {"records": len(status_rows), "buckets": dict(sorted(bucket_counts.items()))},
        projection_policy={
            "exactly_one_current_bucket_per_variant": True,
            "historical_and_current_status_are_distinct": True,
            "baseline_unknown_is_not_upgraded": True,
        },
        stage_claim_ids=[row["stage_claim_id"] for row in status_rows],
        records=status_rows,
    )
    return theorem, open_document, status


def _md_escape(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ")


def _render_list_markdown(document: Mapping[str, Any], title: str, caveat: str) -> str:
    lines = [
        f"# {title}",
        "",
        "> Generated from `Claim_Catalog_v4.json`; do not edit by hand.",
        ">",
        f"> {caveat}",
        "",
        f"Authority: `{document['authority_sha256']}`",
        "",
        "| Stage4 ID | ATV | Label | Domain | Kind | Status | Curation |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in document["records"]:
        lines.append(
            "| "
            + " | ".join(
                _md_escape(value)
                for value in (
                    row["stage_claim_id"],
                    row["variant_id"],
                    row["preferred_label"],
                    row["owner_domain"],
                    row["current_claim_kind"],
                    row["material_status"].get("status"),
                    row["curation_state"],
                )
            )
            + " |"
        )
    lines.extend(["", f"Records: **{len(document['records'])}**", ""])
    return "\n".join(lines)


def _render_status_markdown(document: Mapping[str, Any]) -> str:
    lines = [
        "# Stage4 Status Index",
        "",
        "> Generated from `Claim_Catalog_v4.json`; do not edit by hand.",
        "> Inherited `unknown` values remain unknown; list membership is not proof credit.",
        "",
        f"Authority: `{document['authority_sha256']}`",
        "",
        "| Stage4 ID | ATV | Label | Kind | Bucket | As of | Curation |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in document["records"]:
        lines.append(
            "| "
            + " | ".join(
                _md_escape(value)
                for value in (
                    row["stage_claim_id"],
                    row["variant_id"],
                    row["preferred_label"],
                    row["current_claim_kind"],
                    row["status_bucket"],
                    row["material_status"].get("as_of"),
                    row["curation_state"],
                )
            )
            + " |"
        )
    lines.extend(["", f"Records: **{len(document['records'])}**", ""])
    return "\n".join(lines)


def _documents_by_name(documents: Mapping[Any, Any]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for raw_name, raw_value in documents.items():
        name = Path(str(raw_name)).name
        if not name.endswith(".json"):
            continue
        if isinstance(raw_value, str):
            try:
                value = json.loads(raw_value)
            except json.JSONDecodeError as error:
                raise CatalogError(f"generated {name} is invalid JSON") from error
        else:
            value = raw_value
        if not isinstance(value, dict):
            raise CatalogError(f"generated {name} is not an object")
        output[name] = value
    return output


def _validate_catalog_record_schema(
    row: Mapping[str, Any], label: str, review_date: str
) -> None:
    """Validate the closed Stage4 fields on one catalog projection source."""

    _require_fields(
        row,
        (
            "record_role",
            "claim_kind",
            "current_claim_kind",
            "atomicity",
            "truth_apt",
            "material_status",
            "rights_status",
            "owner_domain",
            "membership_domains",
            "curation_state",
            "status_events",
        ),
        label,
    )
    state = _require_enum(
        row["curation_state"],
        {
            "inherited_v2_machine_triage",
            "stage4_curated_addition",
            "stage4_curated_overlay",
        },
        f"{label}.curation_state",
    )
    _require_enum(
        row["record_role"],
        CURATED_RECORD_ROLES | {"unreviewed_source_variant"},
        f"{label}.record_role",
    )
    catalog_kinds = {_canonical_claim_kind(kind) for kind in CURATED_CLAIM_KINDS} | {
        "unknown"
    }
    _require_enum(row["claim_kind"], catalog_kinds, f"{label}.claim_kind")
    _require_enum(
        row["current_claim_kind"], catalog_kinds, f"{label}.current_claim_kind"
    )
    _require_enum(
        row["atomicity"], CURATED_ATOMICITIES | {"unknown"}, f"{label}.atomicity"
    )
    owner = _require_enum(row["owner_domain"], MEMBERSHIP_DOMAINS, f"{label}.owner_domain")
    memberships = _require_list(row["membership_domains"], f"{label}.membership_domains")
    if (
        owner not in memberships
        or len(memberships) != len(set(memberships))
        or any(domain not in MEMBERSHIP_DOMAINS for domain in memberships)
    ):
        raise CatalogError(f"{label}.membership_domains violates domain ownership")

    rights_allowed = set(CURATED_RIGHTS_STATUSES)
    status_allowed = set(CURATED_MATERIAL_STATUSES)
    if state != "stage4_curated_addition":
        # A metadata/status overlay does not retroactively grant rights or
        # semantic review to its inherited v2 source variant.
        rights_allowed.add("unknown")
        status_allowed.add("unknown")
    _require_enum(row["rights_status"], rights_allowed, f"{label}.rights_status")

    def validate_status(value: Any, status_label: str, *, required_date: bool) -> str:
        material = _require_object(value, status_label)
        _require_fields(material, ("status", "as_of", "basis", "source_refs"), status_label)
        status_value = _require_enum(
            material["status"], status_allowed, f"{status_label}.status"
        )
        as_of = material["as_of"]
        if as_of is None:
            if required_date or status_value != "unknown":
                raise CatalogError(f"{status_label}.as_of must be a strict ISO date")
        else:
            status_date = _require_iso_date(as_of, f"{status_label}.as_of")
            if status_date > review_date:
                raise CatalogError(f"{status_label}.as_of postdates manifest.review_date")
        _require_string(material["basis"], f"{status_label}.basis")
        _require_list(material["source_refs"], f"{status_label}.source_refs")
        return status_value

    raw_material = _require_object(
        row["material_status"], f"{label}.material_status"
    )
    raw_current_status = raw_material.get("status")
    if raw_current_status not in {"unknown", "not_applicable"} and not (
        row["record_role"] == "claim"
        and row["truth_apt"] is True
        and row["atomicity"] == "atomic"
    ):
        raise CatalogError(
            f"{label} assigns material truth status to a non-atomic/non-truth-apt row"
        )
    current_status = validate_status(
        row["material_status"],
        f"{label}.material_status",
        required_date=state == "stage4_curated_addition",
    )
    if current_status not in {"unknown", "not_applicable"} and not (
        row["record_role"] == "claim"
        and row["truth_apt"] is True
        and row["atomicity"] == "atomic"
    ):
        raise CatalogError(
            f"{label} assigns material truth status to a non-atomic/non-truth-apt row"
        )
    if (
        state == "stage4_curated_addition"
        and row["record_role"] != "claim"
        and current_status != "not_applicable"
    ):
        raise CatalogError(f"{label} assigns a nonclaim status other than not_applicable")
    events = _require_object_rows(row["status_events"], f"{label}.status_events")
    for index, event in enumerate(events):
        validate_status(event, f"{label}.status_events[{index}]", required_date=True)


def validate_artifacts(
    documents: Mapping[Any, Any],
    manifest: Mapping[str, Any],
    inputs: Mapping[str, Any],
) -> None:
    """Validate conservation, identity, candidate, and projection invariants.

    The function accepts filename/Path keys and either decoded objects or JSON
    strings, which makes it suitable for independent in-memory mutation tests.
    """

    docs = _documents_by_name(documents)
    required = {path.name for path in JSON_OUTPUT_PATHS}
    if set(docs) != required:
        raise CatalogError(
            f"artifact JSON set differs: missing={sorted(required-set(docs))} extra={sorted(set(docs)-required)}"
        )
    for name, document in docs.items():
        validate_document(name, document)
        if document["authoritative_inputs"] != inputs["authoritative_inputs"]:
            raise CatalogError(f"{name} is not bound to the complete input hash inventory")

    effective = validate_manifest(manifest, inputs)
    source = docs[SOURCE_RECORDS_V4_PATH.name]
    registry = docs[REGISTRY_V4_PATH.name]
    stage = docs[STAGE_REGISTRY_V4_PATH.name]
    migration = docs[MIGRATION_V4_PATH.name]
    candidates = docs[CANDIDATE_DISPOSITIONS_V4_PATH.name]
    repairs = docs[REPAIR_DISPOSITIONS_V4_PATH.name]
    catalog = docs[CATALOG_V4_PATH.name]
    theorem = docs[THEOREM_JSON_V4_PATH.name]
    open_document = docs[OPEN_JSON_V4_PATH.name]
    status = docs[STATUS_JSON_V4_PATH.name]
    _validate_sealed_lifecycle_rows(registry, "Claim_ID_Registry_v4")

    baseline_source_ids = {row["occurrence_id"] for row in inputs["source_records_v2"]["records"]}
    if set(source.get("baseline_occurrence_ids", [])) != baseline_source_ids:
        raise CatalogError("Source_Records_v4 baseline occurrence set drifted")
    source_rows = _require_list(source.get("records"), "Source_Records_v4.records")
    source_ids = [row.get("occurrence_id") for row in source_rows]
    if len(source_ids) != len(set(source_ids)) or not baseline_source_ids <= set(source_ids):
        raise CatalogError("Source_Records_v4 drops or duplicates occurrence IDs")
    source_by_id = {row["occurrence_id"]: row for row in source_rows}
    for baseline in inputs["source_records_v2"]["records"]:
        occurrence_id = baseline["occurrence_id"]
        if source_by_id[occurrence_id] != baseline:
            raise CatalogError(
                f"Source_Records_v4 mutated baseline occurrence {occurrence_id}"
            )
    previous_source = inputs.get("previous_v4", {}).get(SOURCE_RECORDS_V4_PATH.name)
    if previous_source is not None:
        prior_by_key = {
            row["curation_key"]: row
            for row in _require_object_rows(
                previous_source.get("records"), "previous Source_Records_v4.records"
            )
            if row.get("curation_key") is not None
        }
        current_by_key = {
            row["curation_key"]: row
            for row in source_rows
            if row.get("curation_key") is not None
        }
        if not set(prior_by_key) <= set(current_by_key):
            raise CatalogError("Source_Records_v4 removed a previously allocated occurrence")
        for key, prior_row in prior_by_key.items():
            if current_by_key[key] != prior_row:
                raise CatalogError(
                    f"Source_Records_v4 rewrote birth authority for allocated {key}"
                )
    baseline_alias_occurrences = {
        row["target_occurrence_id"] for row in inputs["registry_v2"]["legacy_aliases"]
    }
    expected_folded = baseline_source_ids - baseline_alias_occurrences
    if set(source.get("folded_occurrence_ids", [])) != expected_folded or len(expected_folded) != 76:
        raise CatalogError("folded occurrence conservation failed")

    baseline_variants = {
        row["variant_id"]: row for row in inputs["registry_v2"]["variants"]
    }
    baseline_families = {
        row["family_id"]: row for row in inputs["registry_v2"]["families"]
    }
    family_rows = _require_list(registry.get("families"), "Claim_ID_Registry_v4.families")
    families = {row.get("family_id"): row for row in family_rows}
    if len(families) != len(family_rows) or not set(baseline_families) <= set(families):
        raise CatalogError("v4 registry drops or duplicates family IDs")
    for family_id, baseline in baseline_families.items():
        # Whole-row equality includes lexical_title_key.  Baseline ATF
        # identity is immutable; Stage4 reuse is represented by a separate
        # family_membership_extensions edge.
        if families[family_id] != baseline:
            raise CatalogError(f"v4 registry mutated baseline family {family_id}")
    variant_rows = _require_list(registry.get("variants"), "Claim_ID_Registry_v4.variants")
    variants = {row.get("variant_id"): row for row in variant_rows}
    if len(variants) != len(variant_rows) or not set(baseline_variants) <= set(variants):
        raise CatalogError("v4 registry drops or duplicates variant IDs")
    for variant_id, baseline in baseline_variants.items():
        if variants[variant_id] != baseline:
            raise CatalogError(f"v4 registry mutated baseline variant {variant_id}")
    observed_aliases = registry.get("legacy_aliases")
    if canonical_json_bytes(observed_aliases) != canonical_json_bytes(inputs["registry_v2"]["legacy_aliases"]):
        raise CatalogError("legacy THM aliases were rebound, reordered, or mutated")
    if len(observed_aliases) != BASELINE_LEGACY_ALIASES:
        raise CatalogError("legacy alias denominator is not 3262")
    for split in registry.get("splits", []):
        if split.get("default_child", split.get("default_child_id")) is not None:
            raise CatalogError("a split assigns a forbidden default child")
        if split.get("evidence_inherited") not in (None, False):
            raise CatalogError("a split inherits evidence")

    allocated_by_key = {
        row["curation_key"]: row["variant_id"]
        for row in variant_rows
        if row.get("curation_key") is not None
    }
    expected_supersedes = {
        addition["curation_key"]: relation["target_atv_id"]
        for addition in effective["additions"]
        for relation in addition["lineage"]
        if relation["relation_type"] == "supersedes"
    }
    redirect_rows = _require_object_rows(
        registry.get("redirects"), "Claim_ID_Registry_v4.redirects"
    )
    redirect_sources: dict[str, dict[str, Any]] = {}
    redirect_targets: set[str] = set()
    supersedes_by_key: dict[str, dict[str, Any]] = {}
    for row in redirect_rows:
        source_variant_id = row.get("source_variant_id", row.get("from_variant_id"))
        target_variant_id = row.get("target_variant_id", row.get("to_variant_id"))
        if source_variant_id not in variants or target_variant_id not in variants:
            raise CatalogError("registry redirect has an unknown source/target variant")
        if source_variant_id in redirect_sources:
            raise CatalogError(f"registry redirect source is duplicated: {source_variant_id}")
        if target_variant_id in redirect_targets:
            raise CatalogError(f"registry redirect target is not one-to-one: {target_variant_id}")
        if row.get("default_child") is not None or row.get("evidence_inherited") is not False:
            raise CatalogError(f"registry redirect {source_variant_id} violates inheritance typing")
        redirect_sources[source_variant_id] = row
        redirect_targets.add(target_variant_id)
        if row.get("relation_type") == "supersedes":
            key = row.get("curation_key")
            if not isinstance(key, str) or key in supersedes_by_key:
                raise CatalogError("registry supersedes redirect has an invalid curation key")
            supersedes_by_key[key] = row
    previous_registry = inputs.get("previous_v4", {}).get(REGISTRY_V4_PATH.name)
    if previous_registry is not None:
        prior_redirects = _require_object_rows(
            previous_registry.get("redirects"), "previous Claim_ID_Registry_v4.redirects"
        )
        for prior_row in prior_redirects:
            if prior_row not in redirect_rows:
                raise CatalogError(
                    "prior lifecycle redirect was removed or rebound in generated registry"
                )
        prior_splits = _require_object_rows(
            previous_registry.get("splits"), "previous Claim_ID_Registry_v4.splits"
        )
        generated_splits = _require_object_rows(
            registry.get("splits"), "Claim_ID_Registry_v4.splits"
        )
        for prior_row in prior_splits:
            if prior_row not in generated_splits:
                raise CatalogError(
                    "prior lifecycle split was removed or rebound in generated registry"
                )
    if set(supersedes_by_key) != set(expected_supersedes):
        raise CatalogError("registry supersedes redirects differ from manifest lineage")
    for key, source_variant_id in expected_supersedes.items():
        row = supersedes_by_key[key]
        if (
            row.get("source_variant_id") != source_variant_id
            or row.get("target_variant_id") != allocated_by_key[key]
        ):
            raise CatalogError(f"registry supersedes redirect drifted for {key}")

    # Fail closed on redirect cycles, including any historical redirect plus
    # newly materialized supersedes edges.
    redirect_map = {
        source: row.get("target_variant_id", row.get("to_variant_id"))
        for source, row in redirect_sources.items()
    }
    for start in redirect_map:
        seen: set[str] = set()
        cursor = start
        while cursor in redirect_map:
            if cursor in seen:
                raise CatalogError(f"registry redirect cycle reaches {cursor}")
            seen.add(cursor)
            cursor = redirect_map[cursor]

    mappings = _require_list(stage.get("mappings"), "Stage4 registry mappings")
    mapping_by_variant = {row.get("variant_id"): row for row in mappings}
    if len(mapping_by_variant) != len(mappings) or set(mapping_by_variant) != set(variants):
        raise CatalogError("ATV to Stage4 mapping is not a total bijection")
    stage_ids = set()
    for variant_id, row in mapping_by_variant.items():
        expected_stage = _stage_id(variant_id)
        if row.get("stage_claim_id") != expected_stage or row.get("ordinal") != _parse_ordinal(variant_id, "ATV"):
            raise CatalogError(f"Stage4 ordinal rule failed for {variant_id}")
        stage_ids.add(expected_stage)
    if len(stage_ids) != len(mappings):
        raise CatalogError("Stage4 claim IDs are not unique")

    migrations = _require_list(migration.get("migrations"), "migration.migrations")
    migration_by_variant = {row.get("variant_id"): row for row in migrations}
    if len(migration_by_variant) != len(migrations) or set(migration_by_variant) != set(variants):
        raise CatalogError("migration is not total over all v4 variants")
    carried = {row.get("v2_variant_id") for row in migrations if row.get("v2_variant_id")}
    if carried != set(baseline_variants):
        raise CatalogError("migration does not conserve all 3338 v2 variants")
    alias_migrations = migration.get("legacy_alias_migrations", [])
    old_alias_target = {
        row["alias_id"]: row["target_variant_id"]
        for row in inputs["registry_v2"]["legacy_aliases"]
    }
    observed_alias_target = {
        row.get("alias_id"): row.get("historical_target_variant_id") for row in alias_migrations
    }
    if observed_alias_target != old_alias_target or any(row.get("rebound") is not False for row in alias_migrations):
        raise CatalogError("migration rebinds a historical THM alias")
    if set(migration.get("folded_occurrence_ids", [])) != expected_folded:
        raise CatalogError("migration loses one or more 76 folded occurrences")
    for key, source_variant_id in expected_supersedes.items():
        target_variant_id = allocated_by_key[key]
        resolution = migration_by_variant[source_variant_id].get("current_resolution")
        if resolution != {
            "kind": "redirect",
            "target_stage_claim_ids": [_stage_id(target_variant_id)],
            "default_child": None,
            "evidence_inherited": False,
        }:
            raise CatalogError(f"migration supersedes resolution drifted for {key}")

    manifest_dispositions = {
        row["candidate_key"]: row for row in effective["dispositions"]
    }
    disposition_rows = _require_list(candidates.get("dispositions"), "candidate dispositions")
    observed_dispositions = {row.get("candidate_key"): row for row in disposition_rows}
    if len(observed_dispositions) != len(disposition_rows) or set(observed_dispositions) != set(manifest_dispositions):
        raise CatalogError("candidate disposition projection drops/substitutes a key")
    frozen = _expected_candidate_universe(inputs)
    if not set(frozen) <= set(observed_dispositions) or len(frozen) != 154:
        raise CatalogError("98 v2 plus 56 v3 frozen candidate coverage failed")
    previous_candidates = inputs.get("previous_v4", {}).get(
        CANDIDATE_DISPOSITIONS_V4_PATH.name
    )
    if previous_candidates is not None:
        for prior_row in _require_object_rows(
            previous_candidates.get("dispositions"),
            "previous Candidate_Dispositions_v4.dispositions",
        ):
            key = prior_row.get("candidate_key")
            current_row = observed_dispositions.get(key)
            if current_row is None:
                raise CatalogError(f"prior candidate disposition removed: {key}")
            for field in ("allocated_atv_ids", "target_atv_ids"):
                prior_ids = _require_list(
                    prior_row.get(field), f"previous candidate[{key}].{field}"
                )
                current_ids = _require_list(
                    current_row.get(field), f"candidate[{key}].{field}"
                )
                if not set(prior_ids) <= set(current_ids):
                    raise CatalogError(
                        f"prior candidate lifecycle history removed from {key}.{field}"
                    )
    addition_allocations = {
        row.get("curation_key"): row for row in variant_rows if row.get("curation_key")
    }
    for key, manifest_row in manifest_dispositions.items():
        row = observed_dispositions[key]
        expected_allocated = [addition_allocations[child]["variant_id"] for child in manifest_row["child_keys"]]
        if row.get("allocated_atv_ids") != expected_allocated:
            raise CatalogError(f"candidate {key} child-to-ATV mapping drifted")
        if row.get("target_atv_ids") != [*manifest_row["existing_atv_ids"], *expected_allocated]:
            raise CatalogError(f"candidate {key} target ATV set drifted")
        if row.get("target_stage_ids") != [_stage_id(item) for item in row["target_atv_ids"]]:
            raise CatalogError(f"candidate {key} target Stage4 set drifted")
        split_map = _split_map(registry)
        expected_terminals = list(
            dict.fromkeys(
                terminal
                for target in row["target_atv_ids"]
                for terminal in _terminal_variant_ids(target, redirect_map, split_map)
            )
        )
        if (
            row.get("terminal_atv_ids") != expected_terminals
            or row.get("terminal_stage_ids")
            != [_stage_id(item) for item in expected_terminals]
        ):
            raise CatalogError(f"candidate {key} terminal lifecycle resolution drifted")
        expected_terminal_children = [
            {
                "curation_key": variants[item].get("curation_key"),
                "variant_id": item,
                "stage_claim_id": _stage_id(item),
                "lifecycle": "active",
            }
            for item in expected_terminals
        ]
        if row.get("terminal_children") != expected_terminal_children:
            raise CatalogError(f"candidate {key} terminal child view drifted")
        if len(expected_terminals) != len(set(expected_terminals)) or any(
            item in redirect_map or item in split_map for item in expected_terminals
        ):
            raise CatalogError(f"candidate {key} does not resolve to unique active terminals")
        expected_children = []
        for child_key in manifest_row["child_keys"]:
            child_variant_id = addition_allocations[child_key]["variant_id"]
            expected_children.append(
                {
                    "curation_key": child_key,
                    "variant_id": child_variant_id,
                    "stage_claim_id": _stage_id(child_variant_id),
                    "lifecycle": (
                        "redirected"
                        if child_variant_id in redirect_map
                        else "split"
                        if child_variant_id in split_map
                        else "active"
                    ),
                    "current_resolution": _current_variant_resolution(
                        child_variant_id, redirect_map, split_map
                    ),
                }
            )
        if row.get("children") != expected_children:
            raise CatalogError(f"candidate {key} historical child resolution drifted")
        if manifest_row["disposition"] == "collision" and expected_allocated:
            raise CatalogError(f"collision candidate {key} allocated an ATV")
        # For a nonclaim disposition these ATV IDs belong only to its explicit
        # truth-apt children, never to the umbrella candidate itself.
        if manifest_row["disposition"] == "nonclaim":
            child_by_key = {
                addition["curation_key"]: addition for addition in effective["additions"]
            }
            if manifest_row["child_keys"] and not any(
                child_by_key[child]["record_role"] == "claim"
                for child in manifest_row["child_keys"]
            ):
                raise CatalogError(f"nonclaim candidate {key} has no truth-apt child")

    repair_rows = _require_list(repairs.get("dispositions"), "repair dispositions")
    if len(repair_rows) != REPAIR_PROPOSALS or len({row.get("proposal_id") for row in repair_rows}) != REPAIR_PROPOSALS:
        raise CatalogError("repair proposal conservation is not exactly 623")

    catalog_rows = _require_list(catalog.get("records"), "Claim_Catalog_v4.records")
    catalog_by_variant = {row.get("variant_id"): row for row in catalog_rows}
    if len(catalog_by_variant) != len(catalog_rows) or set(catalog_by_variant) != set(variants):
        raise CatalogError("catalog is not exactly one record per allocated ATV")
    for variant_id, row in catalog_by_variant.items():
        _validate_catalog_record_schema(
            row, f"Claim_Catalog_v4.records[{variant_id}]", effective["review_date"]
        )
        if row.get("stage_claim_id") != _stage_id(variant_id):
            raise CatalogError(f"catalog Stage4 mapping drifted for {variant_id}")
        if row.get("source_occurrence_id") not in set(source_ids):
            raise CatalogError(f"catalog record {variant_id} has an orphan source occurrence")
    for addition in effective["additions"]:
        allocated = addition_allocations[addition["curation_key"]]["variant_id"]
        record = catalog_by_variant[allocated]
        if record.get("statement") != addition["statement"] or record.get("source_refs") != addition["provenance_source_refs"]:
            raise CatalogError(f"curated addition {addition['curation_key']} was weakened in catalog projection")
    for key, source_variant_id in expected_supersedes.items():
        target_variant_id = allocated_by_key[key]
        source_record = catalog_by_variant[source_variant_id]
        target_record = catalog_by_variant[target_variant_id]
        if (
            source_record.get("lifecycle") != "redirected"
            or source_record.get("lifecycle_target_stage_ids")
            != [_stage_id(target_variant_id)]
            or source_record.get("redirected_by_curation_key") != key
        ):
            raise CatalogError(f"catalog superseded lifecycle drifted for {key}")
        if target_record.get("lifecycle") != "active":
            raise CatalogError(f"catalog superseding target is not active for {key}")

    baseline_catalog_by_variant = {
        row["variant_id"]: row for row in _baseline_catalog_records(inputs, registry)
    }
    overlays_by_target: defaultdict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for overlay in effective["overlays"]:
        overlays_by_target[overlay["target_atv_id"]].append(overlay)
    for target_id, target_overlays in overlays_by_target.items():
        baseline_record = baseline_catalog_by_variant[target_id]
        record = catalog_by_variant[target_id]
        expected_memberships = set(baseline_record["membership_domains"])
        expected_candidates = set(baseline_record["candidate_keys"])
        expected_sources = set(baseline_record["source_refs"])
        expected_overlay_keys: list[str] = []
        for overlay in target_overlays:
            expected_memberships.update(overlay.get("membership_domains_add", []))
            expected_candidates.update(overlay["candidate_keys"])
            expected_sources.update(overlay["source_refs"])
            expected_overlay_keys.append(overlay["curation_key"])
        if record.get("owner_domain") != baseline_record["owner_domain"]:
            raise CatalogError(f"overlay changed owner_domain for {target_id}")
        if record["owner_domain"] not in record.get("membership_domains", []):
            raise CatalogError(f"overlay removed owner membership for {target_id}")
        if record.get("membership_domains") != sorted(expected_memberships):
            raise CatalogError(f"overlay membership edge is stale for {target_id}")
        if record.get("candidate_keys") != sorted(expected_candidates):
            raise CatalogError(f"overlay candidate edge is stale for {target_id}")
        if record.get("source_refs") != sorted(expected_sources):
            raise CatalogError(f"overlay source edge is stale for {target_id}")
        if record.get("provenance_source_refs") != sorted(expected_sources):
            raise CatalogError(f"overlay provenance edge is stale for {target_id}")
        if record.get("overlay_keys") != expected_overlay_keys:
            raise CatalogError(f"overlay identity edge is stale for {target_id}")

    expected_theorem = [
        _projection_row(row) for row in catalog_rows if _is_theorem_record(row)
    ]
    expected_open = [
        _projection_row(row) for row in catalog_rows if _is_open_record(row)
    ]
    expected_status = []
    for row in catalog_rows:
        projected = _projection_row(row)
        projected["status_event_count"] = len(row.get("status_events", []))
        expected_status.append(projected)
    for rows in (expected_theorem, expected_open, expected_status):
        rows.sort(key=lambda row: row["stage_claim_id"])
    for label, document, expected_rows in (
        ("theorem", theorem, expected_theorem),
        ("open", open_document, expected_open),
        ("status", status, expected_status),
    ):
        if document.get("records") != expected_rows:
            raise CatalogError(f"{label} projection is stale or content-divergent")
        if document.get("stage_claim_ids") != [row["stage_claim_id"] for row in expected_rows]:
            raise CatalogError(f"{label} projection ID set is stale")
    if set(theorem["stage_claim_ids"]) & set(open_document["stage_claim_ids"]):
        raise CatalogError("theorem and current-open projections overlap")
    if set(status["stage_claim_ids"]) != stage_ids:
        raise CatalogError("status index is not exactly one row per Stage4 claim ID")


def _build_artifacts_from_loaded(
    root_manifest: Mapping[str, Any],
    loaded: Mapping[str, Any],
) -> dict[Path, str]:
    """Internal build over an already authenticated input generation.

    Callers must use :func:`build_artifacts`.  The CLI uses this helper only
    while holding the generation lock, including the explicitly authorized
    unreleased-bootstrap recovery path.
    """

    _validate_loaded_authoritative_inventory(loaded)
    effective = validate_manifest(root_manifest, loaded)
    previous = loaded.get("previous_v4", {})
    if previous:
        previous_documents = _require_object(previous, "inputs.previous_v4")
        for name, document in previous_documents.items():
            validate_document(name, _require_object(document, f"previous_v4[{name}]"))
        _validate_previous_lifecycle_artifacts(
            previous_documents,
            current_authoritative_inputs=loaded["authoritative_inputs"],
            effective_manifest=effective,
        )
    allocation, source, registry = _build_allocations(effective, loaded)
    stage = _build_stage_registry(registry, loaded)
    migration = _build_migration(source, registry, stage, loaded)
    candidate = _build_candidate_dispositions(effective, allocation, registry, loaded)
    repair = _build_repair_dispositions(effective, loaded)
    catalog = _build_catalog(effective, allocation, registry, loaded)
    theorem, open_document, status = _build_projections(catalog, loaded)

    decoded: dict[Path, dict[str, Any]] = {
        SOURCE_RECORDS_V4_PATH: source,
        REGISTRY_V4_PATH: registry,
        STAGE_REGISTRY_V4_PATH: stage,
        MIGRATION_V4_PATH: migration,
        CANDIDATE_DISPOSITIONS_V4_PATH: candidate,
        REPAIR_DISPOSITIONS_V4_PATH: repair,
        CATALOG_V4_PATH: catalog,
        THEOREM_JSON_V4_PATH: theorem,
        OPEN_JSON_V4_PATH: open_document,
        STATUS_JSON_V4_PATH: status,
    }
    validate_artifacts(decoded, effective, loaded)

    outputs: dict[Path, str] = {path: pretty_json(value) for path, value in decoded.items()}
    outputs[THEOREM_MD_V4_PATH] = _render_list_markdown(
        theorem,
        "Stage4 Theorem List",
        "Inherited machine-triage classifications remain visibly labeled and are not human truth review.",
    )
    outputs[OPEN_MD_V4_PATH] = _render_list_markdown(
        open_document,
        "Stage4 Conjecture, Hypothesis, and Open List",
        "Current status is exact-variant scoped; historical conjecture names do not imply current openness.",
    )
    outputs[STATUS_MD_V4_PATH] = _render_status_markdown(status)
    return {path: outputs[path] for path in OUTPUT_PATHS}


def build_artifacts(
    manifest: Mapping[str, Any] | None = None,
    inputs: Mapping[str, Any] | None = None,
) -> dict[Path, str]:
    """Build all thirteen outputs from the current on-disk authority only.

    ``manifest`` and ``inputs`` remain accepted for API compatibility, but
    are assertions about the currently loaded generation, not override
    channels.  A caller-supplied effective manifest, mutated authoritative
    object, or independently re-sealed prior lifecycle view is rejected even
    when its public hashes and counts are internally self-consistent.  This
    prevents coordinated in-memory views from erasing an already allocated
    redirect/split while the outputs still claim the pristine input hashes.
    """

    trusted = load_inputs()
    if inputs is not None:
        try:
            supplied_inputs = dict(inputs)
        except (TypeError, ValueError) as error:
            raise CatalogError("public build inputs must be one ordinary mapping") from error
        if supplied_inputs != trusted:
            raise CatalogError(
                "caller-supplied loaded inputs differ from the current on-disk "
                "authoritative objects or prior lifecycle bytes"
            )
    if manifest is not None:
        try:
            supplied_manifest = dict(manifest)
        except (TypeError, ValueError) as error:
            raise CatalogError("public build manifest must be one ordinary mapping") from error
        if supplied_manifest != trusted["manifest"]:
            raise CatalogError(
                "caller-supplied manifest differs from the current on-disk root manifest; "
                "effective or mutated manifest overrides are forbidden"
            )
    outputs = _build_artifacts_from_loaded(trusted["manifest"], trusted)
    assert_generation_snapshot(trusted["generation_snapshot"], trusted["manifest"])
    return outputs


def _write_artifacts_locked(
    outputs: Mapping[Path, str],
    expected_snapshot: Mapping[str, Any],
) -> None:
    """Stage, CAS, and publish while the caller holds the directory EX lock.

    All bytes are staged and fsynced before the final CAS.  Consequently a
    CAS failure occurs before the first ``os.replace``.  The directory lock
    prevents cooperating writers from interleaving the thirteen renames.
    Authority seals and ``--check`` reject a crash-visible partial generation.
    """

    V4_DIR.mkdir(parents=True, exist_ok=True)
    staged: dict[Path, Path] = {}
    try:
        for path in OUTPUT_PATHS:
            text = outputs[path]
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
            )
            temporary = Path(temporary_name)
            try:
                with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
                    stream.write(text)
                    stream.flush()
                    os.fsync(stream.fileno())
            except BaseException:
                temporary.unlink(missing_ok=True)
                raise
            staged[path] = temporary
        # This is deliberately the last operation before the first rename.
        # It covers every authoritative input and all thirteen prior outputs.
        assert_generation_snapshot(expected_snapshot)
        for path in OUTPUT_PATHS:
            os.replace(staged[path], path)
            staged.pop(path, None)
            text = outputs[path]
            print(
                f"WROTE {path.relative_to(ROOT)} "
                f"sha256={sha256_bytes(text.encode('utf-8'))}"
            )
        directory_fd = os.open(V4_DIR, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)


def write_artifacts(
    outputs: Mapping[Path, str],
    expected_snapshot: Mapping[str, Any],
) -> None:
    """Safely publish one generated set under the Stage4 directory EX lock."""

    with stage4_generation_lock(exclusive=True):
        _write_artifacts_locked(outputs, expected_snapshot)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify output bytes without writing")
    parser.add_argument(
        "--bootstrap-replace-unreleased",
        action="store_true",
        help=(
            "explicitly replace this generator's unreleased development draft; "
            "forbidden for release-marked outputs"
        ),
    )
    args = parser.parse_args(argv)
    if args.check and args.bootstrap_replace_unreleased:
        raise CatalogError("--check and --bootstrap-replace-unreleased are mutually exclusive")
    # Both check and write runs take EX: allocator reads, high-watermark
    # selection, generation, CAS, and publication are one cross-process unit.
    with stage4_generation_lock(exclusive=True):
        loaded = load_inputs()
        if args.bootstrap_replace_unreleased:
            loaded = authorize_unreleased_bootstrap_replacement(loaded)
        outputs = _build_artifacts_from_loaded(loaded["manifest"], loaded)
        assert_generation_snapshot(loaded["generation_snapshot"])
        if args.check:
            stale = [
                path
                for path, text in outputs.items()
                if not path.is_file() or path.read_text(encoding="utf-8") != text
            ]
            if stale:
                for path in stale:
                    print(f"STALE {path.relative_to(ROOT)}", file=sys.stderr)
                return 1
            digest = stable_digest(
                "awesome-theorems/stage4-output-set/v4",
                {
                    str(path.relative_to(ROOT)): sha256_bytes(text.encode("utf-8"))
                    for path, text in outputs.items()
                },
            )
            print(f"PASS Stage4 deterministic check: {len(outputs)} outputs sha256={digest}")
            return 0
        _write_artifacts_locked(outputs, loaded["generation_snapshot"])
        catalog = json.loads(outputs[CATALOG_V4_PATH])
        candidate = json.loads(outputs[CANDIDATE_DISPOSITIONS_V4_PATH])
        print(
            "COUNTS "
            f"records={catalog['counts']['records']} "
            f"additions={catalog['counts']['curated_additions']} "
            f"overlays={catalog['counts']['curated_overlays']} "
            f"candidate_dispositions={candidate['counts']['total']} "
            f"frozen_candidates={candidate['counts']['frozen']}"
        )
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CatalogError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
