#!/usr/bin/env python3
"""Build the Stage5 theorem-quality curation used by release 5.5.

This curation does not create theorem identities and does not change proof
status.  It binds 1,000 existing 5.4 theorem rows to two deliberately distinct
quality cohorts:

* 500 source-signalled important results: a maximum one-to-one join from the
  pinned 1000+ Theorems source, followed by a diversified fill from mathlib
  module-main-result documentation; and
* 500 source-signalled research-frontier resolutions, with at most one credit
  from each Formal Conjectures source file.

Neither cohort claims a universal ranking or an independent replay of every
human proof.  Those boundaries are part of the emitted authority rather than
being left to prose.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import copy
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping, Sequence
import unicodedata


REPO_ROOT = Path(__file__).resolve().parents[4]
V5_ROOT = REPO_ROOT / "Docs/catalog/v5"
CATALOG_PATH = V5_ROOT / "releases/5.4/Claim_Catalog.json"
MANIFEST_PATH = V5_ROOT / "releases/5.4/Release_Manifest.json"
THOUSAND_PLUS_PATH = V5_ROOT / "sources/1000-plus-theorems-8e04b97d.json"
OUTPUT_PATH = V5_ROOT / "curation/Theorem_Quality_Curation_v5_5.json"

PARENT_RELEASE = "5.4"
PARENT_RELEASE_ROOT = "c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813"
PARENT_CATALOG_SHA256 = "384c1e34a57443dafe2e2ce70e36d6a6e23c6d03e006171b94aa2defa92e9709"
PARENT_MANIFEST_SHA256 = "8cc6a2b5d4f94861eedbf31c76026e08191595c2927ba253cdae3b26d9a8edc9"
REVIEW_DATE = "2026-08-10"

IMPORTANT_TARGET = 500
FRONTIER_TARGET = 500
EXPECTED_LANDMARK_MATCHES = 150
EXPECTED_MODULE_MAIN_FILL = 350

S5_RE = re.compile(r"^S5-CLM-[0-9]{8}$")
ATV_RE = re.compile(r"^ATV-[0-9]{8}$")
RESOLUTION_RE = re.compile(
    r"\b(proved|proof|resolved|solved|disproved|refuted|counterexample)\b",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://", re.IGNORECASE)
YEAR_RE = re.compile(r"\b(?:18|19|20)[0-9]{2}\b")


class CurationError(RuntimeError):
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
        raise CurationError(f"cannot canonicalize JSON: {error}") from error


def encoded_document(value: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_without(value: Mapping[str, Any], *fields: str) -> str:
    ignored = set(fields)
    return sha256_bytes(
        canonical_json_bytes({key: item for key, item in value.items() if key not in ignored})
    )


def set_digest(values: Iterable[str]) -> str:
    return sha256_bytes(canonical_json_bytes(sorted(values)))


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CurationError(f"cannot load {path}: {error}") from error
    if not isinstance(value, dict):
        raise CurationError(f"{path} must contain one JSON object")
    return value


def normalized_title(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).casefold()
    value = "".join(character for character in value if not unicodedata.combining(character))
    value = value.replace("–", "-").replace("—", "-").replace("−", "-")
    return " ".join(re.findall(r"[a-z0-9]+", value))


def signal_rows(row: Mapping[str, Any], kind: str) -> list[Mapping[str, Any]]:
    signals = row.get("theorem_selection", {}).get("importance_signals", [])
    if not isinstance(signals, list):
        return []
    return [
        signal
        for signal in signals
        if isinstance(signal, dict) and signal.get("kind") == kind
    ]


def stable_semantic_key(row: Mapping[str, Any]) -> str:
    """Return the strongest stable semantic key exposed by a release row.

    Native 5.3/5.4 mathlib rows carry a top-level ``semantic_key``.  The
    inherited Formal Conjectures rows predate that field and instead bind their
    normalized statement digest under ``dedupe``.  Falling back to the
    curation key keeps legacy rows addressable without silently using a display
    name or allocation ID as mathematical identity.
    """
    semantic_key = row.get("semantic_key")
    if isinstance(semantic_key, str) and semantic_key:
        return semantic_key
    normalized_statement = row.get("dedupe", {}).get("normalized_statement_sha256")
    if isinstance(normalized_statement, str) and normalized_statement:
        return f"normalized-statement-sha256/{normalized_statement}"
    curation_key = row.get("curation_key")
    if isinstance(curation_key, str) and curation_key:
        return f"legacy-curation-key/{curation_key}"
    raise CurationError(f"row lacks a stable semantic key: {row.get('stage_claim_id')}")


def stable_formal_type_sha256(row: Mapping[str, Any]) -> str:
    """Read the formal-type digest across native and legacy row schemas."""
    formal = row.get("formal_statement", {})
    candidates = (
        formal.get("formal_type_sha256"),
        formal.get("declaration_type_sha256"),
        row.get("formal_type_sha256"),
        row.get("dedupe", {}).get("formal_type_sha256"),
    )
    for candidate in candidates:
        if isinstance(candidate, str) and re.fullmatch(r"[0-9a-f]{64}", candidate):
            return candidate
    raise CurationError(f"row lacks a formal-type digest: {row.get('stage_claim_id')}")


def catalog_by_declaration(records: Sequence[Mapping[str, Any]]) -> dict[str, list[Mapping[str, Any]]]:
    result: defaultdict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in records:
        if row.get("current_claim_kind") != "theorem":
            continue
        declaration = row.get("formal_statement", {}).get("declaration")
        if isinstance(declaration, str) and declaration:
            result[declaration].append(row)
    for values in result.values():
        values.sort(key=lambda row: str(row["stage_claim_id"]))
    return dict(result)


def validate_mathlib_row(row: Mapping[str, Any]) -> None:
    if row.get("origin_release") not in {"5.3", "5.4"}:
        raise CurationError(f"non-native mathlib row in importance cohort: {row.get('stage_claim_id')}")
    if row.get("current_claim_kind") != "theorem" or row.get("material_status") != "proved":
        raise CurationError(f"invalid theorem status for {row.get('stage_claim_id')}")
    formal = row.get("formal_statement", {})
    proof = row.get("proof_evidence", {})
    rights = row.get("rights", {})
    if formal.get("declaration_kind") != "theorem":
        raise CurationError(f"non-literal theorem in importance cohort: {row.get('stage_claim_id')}")
    if proof.get("formal_proof_state") != "kernel_checked_sorry_free" or proof.get("uses_sorry") is not False:
        raise CurationError(f"non-kernel/sorry-free importance row: {row.get('stage_claim_id')}")
    if rights.get("status") != "cleared_with_attribution":
        raise CurationError(f"uncleared importance row: {row.get('stage_claim_id')}")


def maximum_landmark_matching(
    source_records: Sequence[Mapping[str, Any]],
    catalog_records: Sequence[Mapping[str, Any]],
) -> dict[str, Mapping[str, Any]]:
    """Return a deterministic maximum source-identity to catalog-row matching."""
    by_declaration = catalog_by_declaration(catalog_records)
    mathlib_catalog = [
        row
        for row in catalog_records
        if row.get("current_claim_kind") == "theorem"
        and row.get("origin_release") in {"5.3", "5.4"}
    ]
    adjacency: dict[str, list[Mapping[str, Any]]] = {}
    source_by_key: dict[str, Mapping[str, Any]] = {}
    for source in source_records:
        source_key = str(source.get("source_record_id", ""))
        if not source_key:
            raise CurationError("1000+ row lacks source_record_id")
        candidates: dict[str, Mapping[str, Any]] = {}
        mappings = source.get("proof_assistant_mappings", [])
        if not isinstance(mappings, list):
            raise CurationError(f"malformed mappings in {source_key}")
        identifiers = sorted(
            {
                identifier
                for mapping in mappings
                if isinstance(mapping, dict)
                and mapping.get("assistant") == "lean"
                and mapping.get("status") == "formalized"
                for identifier in mapping.get("identifiers", [])
                if isinstance(identifier, str) and identifier
            }
        )
        for identifier in identifiers:
            for row in by_declaration.get(identifier, []):
                if row.get("origin_release") not in {"5.3", "5.4"}:
                    continue
                exact_signals = [
                    signal
                    for signal in signal_rows(row, "mathlib_1000_theorems")
                    if signal.get("external_id") == source.get("external_id")
                    and normalized_title(str(signal.get("upstream_title", "")))
                    == normalized_title(str(source.get("title", "")))
                    and str(signal.get("msc2020", "")) == str(source.get("msc2020", ""))
                ]
                if not exact_signals:
                    continue
                validate_mathlib_row(row)
                candidates[str(row["stage_claim_id"])] = row
        # The pinned mathlib asset also carries an exact source-key/title/MSC
        # signal.  One upstream mapping has identifier drift but still has this
        # exact identity binding, so identifier equality is corroborating rather
        # than the sole admissible edge.
        for row in mathlib_catalog:
            exact_signals = [
                signal
                for signal in signal_rows(row, "mathlib_1000_theorems")
                if signal.get("external_id") == source.get("external_id")
                and normalized_title(str(signal.get("upstream_title", "")))
                == normalized_title(str(source.get("title", "")))
                and str(signal.get("msc2020", "")) == str(source.get("msc2020", ""))
            ]
            if exact_signals:
                validate_mathlib_row(row)
                candidates[str(row["stage_claim_id"])] = row
        if candidates:
            adjacency[source_key] = [candidates[key] for key in sorted(candidates)]
            source_by_key[source_key] = source

    # Deterministic Kuhn augmenting paths are sufficient for this small graph.
    matched_row_to_source: dict[str, str] = {}

    def augment(source_key: str, seen: set[str]) -> bool:
        for row in adjacency[source_key]:
            row_key = str(row["stage_claim_id"])
            if row_key in seen:
                continue
            seen.add(row_key)
            previous = matched_row_to_source.get(row_key)
            if previous is None or augment(previous, seen):
                matched_row_to_source[row_key] = source_key
                return True
        return False

    for source_key in sorted(adjacency):
        augment(source_key, set())

    result = {
        source_key: next(
            row
            for row_key, owner in matched_row_to_source.items()
            if owner == source_key
            for row in adjacency[source_key]
            if row["stage_claim_id"] == row_key
        )
        for source_key in sorted(set(matched_row_to_source.values()))
    }
    if len(result) != EXPECTED_LANDMARK_MATCHES:
        raise CurationError(
            f"1000+ maximum matching is {len(result)}, expected {EXPECTED_LANDMARK_MATCHES}"
        )
    return result


def round_robin(
    rows: Sequence[Mapping[str, Any]],
    count: int,
    *,
    bucket_key,
    order_key,
) -> list[Mapping[str, Any]]:
    buckets: defaultdict[Any, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[bucket_key(row)].append(row)
    for values in buckets.values():
        values.sort(key=order_key)
    keys = sorted(buckets, key=lambda value: canonical_json_bytes(value))
    offsets = {key: 0 for key in keys}
    selected: list[Mapping[str, Any]] = []
    while len(selected) < count:
        advanced = False
        for key in keys:
            index = offsets[key]
            if index >= len(buckets[key]):
                continue
            selected.append(buckets[key][index])
            offsets[key] += 1
            advanced = True
            if len(selected) == count:
                break
        if not advanced:
            break
    if len(selected) != count:
        raise CurationError(f"round-robin pool supplied {len(selected)} of {count} rows")
    return selected


def important_rows(
    source_records: Sequence[Mapping[str, Any]],
    catalog_records: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    source_by_key = {str(row["source_record_id"]): row for row in source_records}
    landmark_matching = maximum_landmark_matching(source_records, catalog_records)
    used_s5 = {str(row["stage_claim_id"]) for row in landmark_matching.values()}

    module_candidates = [
        row
        for row in catalog_records
        if row.get("origin_release") == "5.4"
        and row.get("stage_claim_id") not in used_s5
        and signal_rows(row, "mathlib_module_main_result")
    ]
    for row in module_candidates:
        validate_mathlib_row(row)
    module_fill = round_robin(
        module_candidates,
        EXPECTED_MODULE_MAIN_FILL,
        bucket_key=lambda row: str(row.get("theorem_selection", {}).get("module_root", "")),
        order_key=lambda row: (
            int(row.get("theorem_selection", {}).get("selection_rank", 10**12)),
            str(row.get("stage_claim_id", "")),
        ),
    )

    output: list[dict[str, Any]] = []
    for source_key, row in sorted(landmark_matching.items()):
        source = source_by_key[source_key]
        source_signals = signal_rows(row, "mathlib_1000_theorems")
        item = {
            "cohort": "important",
            "quality_tier": "encyclopedic_named_landmark_with_exact_formal_join",
            "stage_claim_id": row["stage_claim_id"],
            "variant_id": row["variant_id"],
            "semantic_key": row["semantic_key"],
            "origin_release": row["origin_release"],
            "display_name": row["display_name"],
            "formal_type_sha256": stable_formal_type_sha256(row),
            "statement_sha256": row["mathematical_statement"]["statement_sha256"],
            "proof_payload_sha256": row["proof_payload_sha256"],
            "source_record_id": row["provenance"]["source_record_id"],
            "source_locator": row["source_locator"],
            "quality_evidence": {
                "thousand_plus_source_record_id": source_key,
                "thousand_plus_row_sha256": source["row_sha256"],
                "thousand_plus_external_id": source["external_id"],
                "thousand_plus_title": source["title"],
                "thousand_plus_msc2020": source["msc2020"],
                "mathlib_signal": source_signals,
                "exact_lean_identifier": row["formal_statement"]["declaration"],
                "proof_evidence_level": "kernel_checked_sorry_free_at_pinned_commit",
                "importance_evidence_level": "source_signalled_encyclopedic_named_theorem",
                "independent_universal_ranking_claimed": False,
            },
        }
        item["row_sha256"] = hash_without(item, "row_sha256")
        output.append(item)

    for row in module_fill:
        item = {
            "cohort": "important",
            "quality_tier": "source_documented_mathlib_module_main_result",
            "stage_claim_id": row["stage_claim_id"],
            "variant_id": row["variant_id"],
            "semantic_key": row["semantic_key"],
            "origin_release": row["origin_release"],
            "display_name": row["display_name"],
            "formal_type_sha256": stable_formal_type_sha256(row),
            "statement_sha256": row["mathematical_statement"]["statement_sha256"],
            "proof_payload_sha256": row["proof_payload_sha256"],
            "source_record_id": row["provenance"]["source_record_id"],
            "source_locator": row["source_locator"],
            "quality_evidence": {
                "module_root": row["theorem_selection"]["module_root"],
                "module_main_signals": signal_rows(row, "mathlib_module_main_result"),
                "proof_evidence_level": "kernel_checked_sorry_free_at_pinned_commit",
                "importance_evidence_level": "source_documented_main_result_within_module",
                "independent_universal_ranking_claimed": False,
            },
        }
        item["row_sha256"] = hash_without(item, "row_sha256")
        output.append(item)

    output.sort(key=lambda row: str(row["stage_claim_id"]))
    if len(output) != IMPORTANT_TARGET or len({row["stage_claim_id"] for row in output}) != IMPORTANT_TARGET:
        raise CurationError("important cohort cardinality/uniqueness drifted")
    return output


def frontier_score(row: Mapping[str, Any]) -> tuple[int, int, int, int, int]:
    text = "\n".join(
        [
            str(row.get("formal_docstring", "")),
            str(row.get("mathematical_statement", {}).get("natural_language", "")),
        ]
    )
    return (
        int(bool(RESOLUTION_RE.search(text))),
        int(bool(URL_RE.search(text))),
        int(bool(YEAR_RE.search(text))),
        int(row.get("formal_statement", {}).get("sorry_free") is True),
        len(text),
    )


def validate_frontier_row(row: Mapping[str, Any]) -> None:
    if row.get("current_claim_kind") != "theorem" or row.get("material_status") != "proved":
        raise CurationError(f"frontier row is not a proved theorem: {row.get('stage_claim_id')}")
    if row.get("raw_category") != "research solved":
        raise CurationError(f"frontier row lacks research-solved source status: {row.get('stage_claim_id')}")
    if row.get("frontier", {}).get("class") != "source_asserted_solved":
        raise CurationError(f"frontier source class drifted: {row.get('stage_claim_id')}")
    if row.get("formal_statement", {}).get("declaration_kind") != "theorem":
        raise CurationError(f"frontier row is not literal theorem syntax: {row.get('stage_claim_id')}")
    statement = row.get("mathematical_statement", {})
    if not statement.get("formal_type") or not statement.get("natural_language"):
        raise CurationError(f"frontier row lacks complete source statements: {row.get('stage_claim_id')}")
    member_path = row.get("locator", {}).get("member_path")
    if not isinstance(member_path, str) or not member_path:
        raise CurationError(f"frontier row lacks source member path: {row.get('stage_claim_id')}")


def frontier_rows(catalog_records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    candidates = [
        row
        for row in catalog_records
        if row.get("current_claim_kind") == "theorem"
        and row.get("raw_category") == "research solved"
    ]
    by_file: defaultdict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in candidates:
        validate_frontier_row(row)
        by_file[str(row["locator"]["member_path"])].append(row)
    representatives: list[Mapping[str, Any]] = []
    for member_path, rows in sorted(by_file.items()):
        rows.sort(
            key=lambda row: (
                tuple(-item for item in frontier_score(row)),
                stable_semantic_key(row),
                str(row["stage_claim_id"]),
            )
        )
        representatives.append(rows[0])
    if len(representatives) < FRONTIER_TARGET:
        raise CurationError(f"only {len(representatives)} distinct research-solved source files")

    selected = round_robin(
        representatives,
        FRONTIER_TARGET,
        bucket_key=lambda row: (
            str(row.get("primary_ams_class", "")),
            str(row["locator"]["member_path"]).split("/")[1],
        ),
        order_key=lambda row: (
            tuple(-item for item in frontier_score(row)),
            str(row["locator"]["member_path"]),
            str(row["stage_claim_id"]),
        ),
    )

    output: list[dict[str, Any]] = []
    for row in selected:
        member_path = str(row["locator"]["member_path"])
        collection = member_path.split("/")[1]
        text = "\n".join(
            [
                str(row.get("formal_docstring", "")),
                str(row.get("mathematical_statement", {}).get("natural_language", "")),
            ]
        )
        item = {
            "cohort": "frontier",
            "quality_tier": "source_curated_research_problem_resolution",
            "stage_claim_id": row["stage_claim_id"],
            "variant_id": row["variant_id"],
            "semantic_key": stable_semantic_key(row),
            "origin_release": row["origin_release"],
            "display_name": row["display_name"],
            "formal_type_sha256": stable_formal_type_sha256(row),
            "statement_sha256": row["mathematical_statement"]["statement_sha256"],
            "source_record_id": row["curation_key"],
            "source_locator": row["locator"],
            "quality_evidence": {
                "source_collection": collection,
                "source_member_path": member_path,
                "source_category": row["raw_category"],
                "source_frontier_class": row["frontier"]["class"],
                "source_frontier_evidence_level": row["frontier"]["evidence_level"],
                "primary_ams_class": row["primary_ams_class"],
                "explicit_resolution_language_present": bool(RESOLUTION_RE.search(text)),
                "explicit_url_present": bool(URL_RE.search(text)),
                "explicit_year_present": bool(YEAR_RE.search(text)),
                "source_inferred_sorry_free": row["formal_statement"].get("sorry_free") is True,
                "frontier_meaning": "resolution_of_a_source_curated_research_problem",
                "recent_publication_window_claimed": False,
                "independent_human_proof_replay_claimed": False,
                "independent_universal_ranking_claimed": False,
            },
        }
        item["row_sha256"] = hash_without(item, "row_sha256")
        output.append(item)
    output.sort(key=lambda row: str(row["stage_claim_id"]))
    if len(output) != FRONTIER_TARGET:
        raise CurationError("frontier cohort cardinality drifted")
    if len({row["source_locator"]["member_path"] for row in output}) != FRONTIER_TARGET:
        raise CurationError("frontier cohort reuses a Formal Conjectures source file")
    if len({row["stage_claim_id"] for row in output}) != FRONTIER_TARGET:
        raise CurationError("frontier cohort stage identity collision")
    return output


def build() -> dict[str, Any]:
    if sha256_file(CATALOG_PATH) != PARENT_CATALOG_SHA256:
        raise CurationError("parent 5.4 catalog hash drifted")
    if sha256_file(MANIFEST_PATH) != PARENT_MANIFEST_SHA256:
        raise CurationError("parent 5.4 manifest hash drifted")
    catalog = load_json(CATALOG_PATH)
    manifest = load_json(MANIFEST_PATH)
    thousand_plus = load_json(THOUSAND_PLUS_PATH)
    if manifest.get("release_root_sha256") != PARENT_RELEASE_ROOT:
        raise CurationError("parent 5.4 release root drifted")
    catalog_records = catalog.get("records")
    source_records = thousand_plus.get("records")
    if not isinstance(catalog_records, list) or not isinstance(source_records, list):
        raise CurationError("input records are malformed")
    if len(catalog_records) != 4_100 or len(source_records) != 1_200:
        raise CurationError("input cardinality drifted")

    important = important_rows(source_records, catalog_records)
    frontier = frontier_rows(catalog_records)
    overlap = {row["stage_claim_id"] for row in important} & {
        row["stage_claim_id"] for row in frontier
    }
    if overlap:
        raise CurationError(f"important/frontier quota cohorts overlap: {sorted(overlap)[:5]}")

    important_tiers = Counter(str(row["quality_tier"]) for row in important)
    frontier_collections = Counter(
        str(row["quality_evidence"]["source_collection"]) for row in frontier
    )
    result: dict[str, Any] = {
        "schema_version": "awesome-theorems/stage5-theorem-quality-curation/5.5",
        "release_basis": PARENT_RELEASE,
        "review_date": REVIEW_DATE,
        "scope": "quality evidence for existing theorem identities; grants no new theorem identity or proof credit",
        "quality_boundary": {
            "important_definition": "pinned 1000+ named-theorem identity with an exact formal join, or a human-authored mathlib module-main-result signal",
            "frontier_definition": "a proved-status statement sourced from Formal Conjectures category research solved, with one quota credit per source file",
            "independent_universal_importance_ranking_claimed": False,
            "independent_human_proof_replay_for_formal_conjectures_claimed": False,
            "recent_publication_window_for_frontier_claimed": False,
            "frontier_is_historical_research_problem_resolution": True,
            "source_signal_is_not_universal_consensus": True,
        },
        "inputs": {
            "parent_release_root_sha256": PARENT_RELEASE_ROOT,
            "parent_catalog": {
                "path": CATALOG_PATH.relative_to(REPO_ROOT).as_posix(),
                "sha256": sha256_file(CATALOG_PATH),
                "authority_sha256": catalog.get("authority_sha256"),
            },
            "parent_manifest": {
                "path": MANIFEST_PATH.relative_to(REPO_ROOT).as_posix(),
                "sha256": sha256_file(MANIFEST_PATH),
                "authority_sha256": manifest.get("authority_sha256"),
            },
            "thousand_plus_source": {
                "path": THOUSAND_PLUS_PATH.relative_to(REPO_ROOT).as_posix(),
                "sha256": sha256_file(THOUSAND_PLUS_PATH),
                "content_digest_before_self_field": thousand_plus.get(
                    "content_digest_before_self_field"
                ),
                "commit": thousand_plus.get("source_snapshot", {}).get("commit"),
            },
        },
        "selection_policy": {
            "important_target": IMPORTANT_TARGET,
            "landmark_maximum_one_to_one_join": EXPECTED_LANDMARK_MATCHES,
            "module_main_diversified_fill": EXPECTED_MODULE_MAIN_FILL,
            "module_main_fill_origin_release": "5.4",
            "frontier_target": FRONTIER_TARGET,
            "frontier_source_file_cap": 1,
            "frontier_representative_priority": [
                "explicit resolution language",
                "explicit URL",
                "explicit year",
                "source-inferred sorry-free formal proof",
                "longer source explanation",
                "semantic key",
            ],
            "frontier_diversification": "round-robin by primary AMS class and source collection",
            "cohort_overlap_for_quota_forbidden": True,
        },
        "counts": {
            "quality_credits": len(important) + len(frontier),
            "important_credits": len(important),
            "frontier_resolution_credits": len(frontier),
            "new_theorem_identity_credits": 0,
            "new_proof_credits": 0,
            "important_by_tier": dict(sorted(important_tiers.items())),
            "frontier_by_source_collection": dict(sorted(frontier_collections.items())),
            "frontier_distinct_source_files": len(
                {row["source_locator"]["member_path"] for row in frontier}
            ),
        },
        "set_digests": {
            "important_s5_id_set_sha256": set_digest(
                str(row["stage_claim_id"]) for row in important
            ),
            "frontier_s5_id_set_sha256": set_digest(
                str(row["stage_claim_id"]) for row in frontier
            ),
            "quality_s5_id_set_sha256": set_digest(
                str(row["stage_claim_id"]) for row in important + frontier
            ),
            "quality_semantic_key_set_sha256": set_digest(
                str(row["semantic_key"]) for row in important + frontier
            ),
            "row_sha256_set_sha256": set_digest(
                str(row["row_sha256"]) for row in important + frontier
            ),
        },
        "important_credits": important,
        "frontier_credits": frontier,
    }
    result["authority_sha256"] = hash_without(result, "authority_sha256")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check the committed output bytes")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    document = build()
    encoded = encoded_document(document)
    if args.check:
        if not args.output.is_file():
            raise CurationError(f"missing curation output: {args.output}")
        if args.output.read_bytes() != encoded:
            raise CurationError(f"stale curation output: {args.output}")
        print(
            "PASS theorem quality curation 5.5 "
            f"important={document['counts']['important_credits']} "
            f"frontier={document['counts']['frontier_resolution_credits']} "
            f"authority={document['authority_sha256']}"
        )
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encoded)
    print(
        f"wrote {args.output} quality={document['counts']['quality_credits']} "
        f"authority={document['authority_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
