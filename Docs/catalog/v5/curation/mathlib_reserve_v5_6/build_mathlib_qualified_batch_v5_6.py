#!/usr/bin/env python3
"""Build the candidate-only, globally deduped mathlib theorem batch for v5.6.

The v5.6 policy treats both Lean ``theorem`` and ``lemma`` source commands as
theorem records when Lean reports ``ConstantInfo.thmInfo`` and the proof is
sorry-free.  This builder selects one canonical row for each exact/normalized
formal proposition identity, removes the 1,000 mathlib identities already in
release 5.5, and routes possible human-level aliases or formal variants to a
semantic-review quarantine.  It never allocates IDs or changes a release.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Iterable, Mapping, Sequence

import build_mathlib_reserve_inventory_v5_6 as base


SCHEMA = "awesome-theorems/mathlib-qualified-theorem-candidate/5.6"
INVENTORY_SCHEMA = "awesome-theorems/mathlib-qualified-batch-inventory/5.6"
THEOREM_LIST_SHA256 = "f57b885995f4edf8204e96b57b7489c3dfa9d6ac96785031d0498b9ed80f46ab"

HERE = Path(__file__).resolve().parent
REPO = base.REPO
THEOREM_LIST = REPO / "Docs/catalog/v5/releases/5.5/Theorem_List.json"
QUALIFIED_LEDGER = HERE / "Mathlib_Qualified_Theorem_Candidates_v5_6.jsonl"
QUALIFIED_INVENTORY = HERE / "Mathlib_Qualified_Batch_Inventory_v5_6.json"

EXPECTED_COUNTS: dict[str, Any] = {
    "parent_theorem_records": 2_500,
    "parent_mathlib_theorem_records": 1_000,
    "full_mathlib_verified_rows": 2_566,
    "full_mathlib_canonical_formal_identities": 2_561,
    "exact_identity_duplicate_losers_noncredit": 5,
    "unadmitted_canonical_theorem_candidates": 1_561,
    "candidate_source_syntax_kinds": {"lemma": 489, "theorem": 1_072},
    "candidate_theorem_record_kind": {"theorem": 1_561},
    "exact_or_normalized_parent_identity_conflicts": 0,
    "generator_lanes": {
        "provisional_generator_admission": 1_092,
        "semantic_variant_review_quarantine": 469,
    },
    "generator_admission_qualified": 1_092,
    "semantic_variant_review_quarantine": 469,
    "ready_by_source_syntax_kind": {"lemma": 385, "theorem": 707},
    "quarantine_by_source_syntax_kind": {"lemma": 104, "theorem": 365},
    "semantic_evidence_rows_by_type": {
        "same_explicit_parent_declaration_docstring": 3,
        "same_explicit_parent_label_or_alias": 5,
        "same_normalized_declaration_docstring": 15,
        "same_normalized_display_label": 9,
        "same_normalized_mathlib_declaration_leaf": 164,
        "same_normalized_module_main_result_description": 298,
        "same_wikidata_id": 9,
        "same_embedded_named_result_label": 26,
        "same_embedded_named_result_label_with_parent": 12,
    },
    "semantic_evidence_objects_by_type": {
        "same_explicit_parent_declaration_docstring": 3,
        "same_explicit_parent_label_or_alias": 5,
        "same_normalized_declaration_docstring": 15,
        "same_normalized_display_label": 9,
        "same_normalized_mathlib_declaration_leaf": 164,
        "same_normalized_module_main_result_description": 300,
        "same_wikidata_id": 9,
        "same_embedded_named_result_label": 28,
        "same_embedded_named_result_label_with_parent": 12,
    },
    "reliable_mathlib_formal_identity_inventory_if_all_candidates_admitted": 2_561,
    "catalog_entries_granted_here": 0,
    "theorem_credits_granted_here": 0,
}
EXPECTED_ALL_ROOTS: dict[str, int] = {
    "Algebra": 103,
    "AlgebraicGeometry": 51,
    "AlgebraicTopology": 1,
    "Analysis": 344,
    "CategoryTheory": 15,
    "Combinatorics": 27,
    "Computability": 8,
    "Data": 38,
    "Dynamics": 5,
    "FieldTheory": 33,
    "Geometry": 35,
    "GroupTheory": 33,
    "LinearAlgebra": 73,
    "Logic": 2,
    "MeasureTheory": 97,
    "ModelTheory": 11,
    "NumberTheory": 51,
    "Order": 46,
    "Probability": 44,
    "RingTheory": 367,
    "SetTheory": 7,
    "Topology": 170,
}
EXPECTED_READY_ROOTS: dict[str, int] = {
    "Algebra": 73,
    "AlgebraicGeometry": 39,
    "AlgebraicTopology": 1,
    "Analysis": 207,
    "CategoryTheory": 13,
    "Combinatorics": 21,
    "Computability": 8,
    "Data": 25,
    "Dynamics": 5,
    "FieldTheory": 21,
    "Geometry": 24,
    "GroupTheory": 28,
    "LinearAlgebra": 61,
    "Logic": 2,
    "MeasureTheory": 48,
    "ModelTheory": 9,
    "NumberTheory": 42,
    "Order": 22,
    "Probability": 37,
    "RingTheory": 278,
    "SetTheory": 5,
    "Topology": 123,
}


class QualificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise QualificationError(message)


def normalized_text(value: str) -> str:
    return " ".join(base.normalize_name(value).split())


def value_sha(value: str) -> str:
    return base.sha(value.encode("utf-8"))


NAMED_RESULT_TERM_RE = re.compile(
    r"(?:theorem|inequalit(?:y|ies)|equation|principle|lemma|law|formula|"
    r"criterion|identity|duality|decomposition|classification|reciprocity|h[öo]hensatz)",
    re.IGNORECASE,
)
BOLD_SPAN_RE = re.compile(r"\*\*([^*\n]+?)\*\*")


def embedded_named_result_labels(values: Iterable[Any]) -> set[str]:
    labels: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        for raw in BOLD_SPAN_RE.findall(value):
            if NAMED_RESULT_TERM_RE.search(raw):
                label = normalized_text(raw).strip(" .,:;")
                if label:
                    labels.add(label)
    return labels


def source_features(row: Mapping[str, Any]) -> dict[str, set[str]]:
    declaration = str(row["declaration"])
    output: dict[str, set[str]] = {
        "declaration_leaf": {normalized_text(declaration.rsplit(".", 1)[-1])},
        "display_label": {normalized_text(str(row["display_label"]))},
        "declaration_docstring": set(),
        "module_main_result_description": set(),
        "wikidata_id": set(),
        "embedded_named_result_label": set(),
    }
    docstring = row.get("declaration_docstring")
    if isinstance(docstring, str) and docstring.strip():
        output["declaration_docstring"].add(normalized_text(docstring))
    signals = row.get("importance_signals")
    require(isinstance(signals, list), "source importance_signals missing")
    named_label_values: list[Any] = [
        row.get("declaration_docstring"),
        row.get("formal_docstring"),
        row.get("exact_curated_summary"),
    ]
    for signal in signals:
        require(isinstance(signal, dict), "source importance signal is not an object")
        if signal.get("kind") == "mathlib_module_main_result":
            description = signal.get("description")
            require(isinstance(description, str) and bool(description.strip()), "module-main description missing")
            output["module_main_result_description"].add(normalized_text(description))
            named_label_values.append(description)
        elif signal.get("kind") == "mathlib_1000_theorems":
            external = signal.get("external_id")
            require(isinstance(external, str) and bool(external.strip()), "1000+ external id missing")
            output["wikidata_id"].add(normalized_text(external))
            named_label_values.extend((signal.get("title"), signal.get("upstream_title")))
    output["embedded_named_result_label"] = embedded_named_result_labels(named_label_values)
    return output


FEATURE_POLICY = {
    "declaration_leaf": {
        "evidence_type": "same_normalized_mathlib_declaration_leaf",
        "candidate_relation": "declaration_alias_or_parallel_formalization_candidate",
        "strength": "mechanical_name_alias_candidate",
    },
    "display_label": {
        "evidence_type": "same_normalized_display_label",
        "candidate_relation": "same_named_theorem_candidate",
        "strength": "exact_human_label_candidate",
    },
    "declaration_docstring": {
        "evidence_type": "same_normalized_declaration_docstring",
        "candidate_relation": "same_theorem_or_formal_variant_candidate",
        "strength": "exact_individual_prose_candidate",
    },
    "module_main_result_description": {
        "evidence_type": "same_normalized_module_main_result_description",
        "candidate_relation": "same_theorem_family_or_formal_variant_candidate",
        "strength": "source_curated_family_candidate",
    },
    "wikidata_id": {
        "evidence_type": "same_wikidata_id",
        "candidate_relation": "same_named_theorem_candidate",
        "strength": "authoritative_external_identifier_candidate",
    },
    "embedded_named_result_label": {
        "evidence_type": "same_embedded_named_result_label",
        "candidate_relation": "same_named_theorem_or_formal_variant_candidate",
        "strength": "exact_source_embedded_named_result_candidate",
    },
}


def parent_explicit_indexes(
    rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, set[str]]]:
    labels: dict[str, set[str]] = defaultdict(set)
    docstrings: dict[str, set[str]] = defaultdict(set)
    named_results: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        variant = row.get("variant_id")
        require(isinstance(variant, str) and bool(variant), "parent theorem lacks variant_id")
        formal = row.get("formal_statement")
        formal = formal if isinstance(formal, dict) else {}
        label_values: list[Any] = [
            row.get("display_name"),
            row.get("qualified_name"),
            formal.get("declaration"),
            formal.get("qualified_declaration"),
            formal.get("declaration_name"),
        ]
        aliases = row.get("aliases")
        if isinstance(aliases, list):
            label_values.extend(aliases)
        for value in label_values:
            if isinstance(value, str) and value.strip():
                labels[normalized_text(value)].add(variant)
        statement = row.get("statement")
        statement = statement if isinstance(statement, dict) else {}
        doc_values = [
            row.get("formal_docstring"),
            formal.get("formal_docstring"),
            formal.get("docstring"),
            statement.get("natural_language"),
        ]
        for value in doc_values:
            if isinstance(value, str) and value.strip():
                docstrings[normalized_text(value)].add(variant)
        for value in embedded_named_result_labels([*label_values, *doc_values]):
            named_results[value].add(variant)
    return labels, docstrings, named_results


def source_binding(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "asset_path": base.FULL_SOURCE.relative_to(REPO).as_posix(),
        "asset_sha256": base.FULL_SOURCE_SHA256,
        "source_index_zero_based": int(row["selection_rank"]) - 1,
        "source_record_id": row["source_record_id"],
        "source_record_sha256": base.sha(base.canonical(row)),
    }


def load_inputs() -> tuple[
    dict[str, Any],
    bytes,
    list[dict[str, Any]],
    dict[str, Any],
    bytes,
    list[dict[str, Any]],
    bytes,
]:
    full, full_payload = base.load_json(base.FULL_SOURCE, base.FULL_SOURCE_SHA256)
    full_rows = base.validate_source_document(full, base.FULL_ROWS, "qualified full source")
    theorem, theorem_payload = base.load_json(THEOREM_LIST, THEOREM_LIST_SHA256)
    theorem_rows = theorem.get("records")
    require(
        isinstance(theorem_rows, list)
        and len(theorem_rows) == 2_500
        and all(isinstance(row, dict) for row in theorem_rows),
        "release 5.5 theorem denominator drifted",
    )
    manifest, manifest_payload = base.load_json(base.PARENT_MANIFEST, base.PARENT_MANIFEST_SHA256)
    require(manifest.get("release") == "5.5", "parent manifest is not release 5.5")
    return full, full_payload, full_rows, theorem, theorem_payload, theorem_rows, manifest_payload


def canonicalize_source(
    rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_type: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        by_type[base.normalized_type_sha(str(row["formal_type"]))].append(row)
    canonical_rows: list[dict[str, Any]] = []
    duplicate_losers: list[dict[str, Any]] = []
    for normalized_digest, component in sorted(by_type.items()):
        ordered = sorted(component, key=base.duplicate_winner_rank)
        winner = ordered[0]
        canonical_rows.append(dict(winner))
        for loser in ordered[1:]:
            exact = loser["formal_type_sha256"] == winner["formal_type_sha256"]
            duplicate_losers.append(
                {
                    "source_record_id": loser["source_record_id"],
                    "selection_rank": loser["selection_rank"],
                    "declaration": loser["declaration"],
                    "source_syntax_kind": loser["source_syntax_kind"],
                    "formal_type_sha256": loser["formal_type_sha256"],
                    "normalized_formal_type_sha256": normalized_digest,
                    "canonical_source_record_id": winner["source_record_id"],
                    "canonical_selection_rank": winner["selection_rank"],
                    "method": (
                        "exact_formal_type_sha256"
                        if exact
                        else "unicode_whitespace_normalized_formal_type"
                    ),
                    "candidate_only": True,
                    "grants_catalog_entry": False,
                    "grants_theorem_credit": False,
                }
            )
    canonical_rows.sort(key=lambda row: int(row["selection_rank"]))
    duplicate_losers.sort(key=lambda row: int(row["selection_rank"]))
    return canonical_rows, duplicate_losers


def build() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    (
        full,
        full_payload,
        full_rows,
        theorem,
        theorem_payload,
        theorem_rows,
        manifest_payload,
    ) = load_inputs()
    canonical_rows, duplicate_losers = canonicalize_source(full_rows)
    require(len(canonical_rows) == 2_561, "canonical mathlib formal identity count drifted")
    require(
        [int(row["selection_rank"]) for row in duplicate_losers]
        == [38, 378, 618, 619, 2_517],
        "the five exact-identity duplicate losers drifted",
    )
    require(all(row["method"] == "exact_formal_type_sha256" for row in duplicate_losers), "a normalized-only duplicate appeared")

    current_mathlib: dict[str, str] = {}
    for row in theorem_rows:
        if row.get("source_id") != "SRC-MATH-V5-MATHLIB-8A178386":
            continue
        provenance = row.get("provenance")
        require(isinstance(provenance, dict), "current mathlib theorem provenance missing")
        source_id = provenance.get("source_record_id")
        variant_id = row.get("variant_id")
        require(
            isinstance(source_id, str)
            and isinstance(variant_id, str)
            and source_id not in current_mathlib,
            "current mathlib source binding is invalid or duplicated",
        )
        current_mathlib[source_id] = variant_id
    require(len(current_mathlib) == 1_000, "release 5.5 does not contain exactly 1,000 mathlib theorems")

    canonical_by_id = {str(row["source_record_id"]): row for row in canonical_rows}
    require(set(current_mathlib) <= set(canonical_by_id), "an admitted mathlib theorem is not the canonical source winner")
    candidate_rows = [row for row in canonical_rows if row["source_record_id"] not in current_mathlib]
    require(len(candidate_rows) == 1_561, "unadmitted canonical identity count drifted")

    parent_exact, parent_types, parent_names = base.parent_indexes(theorem_rows)
    exact_conflicts: dict[str, dict[str, list[str]]] = {}
    for row in candidate_rows:
        exact, normalized_type, normalized_name = base.source_identity(row)
        conflicts = {
            "exact_formal_type_variant_ids": sorted(parent_exact.get(exact, [])),
            "normalized_formal_type_variant_ids": sorted(parent_types.get(normalized_type, [])),
            "normalized_declaration_name_variant_ids": sorted(parent_names.get(normalized_name, [])),
        }
        if any(conflicts.values()):
            exact_conflicts[str(row["source_record_id"])] = conflicts
    require(not exact_conflicts, "an unadmitted canonical mathlib identity conflicts with the existing 2,500-theorem surface")

    # Candidate alias/family signals are computed against the 1,000 admitted
    # mathlib canonical rows and all 1,561 candidate canonical rows.  The
    # 1,500 non-mathlib parent rows also contribute explicit labels, aliases,
    # and declaration docstrings below.
    canonical_universe = [canonical_by_id[source_id] for source_id in sorted(set(current_mathlib) | {str(row["source_record_id"]) for row in candidate_rows})]
    feature_indexes: dict[str, dict[str, set[str]]] = {
        feature: defaultdict(set) for feature in FEATURE_POLICY
    }
    for row in canonical_universe:
        for feature, values in source_features(row).items():
            for value in values:
                feature_indexes[feature][value].add(str(row["source_record_id"]))

    candidate_ids = {str(row["source_record_id"]) for row in candidate_rows}
    parent_labels, parent_docstrings, parent_named_results = parent_explicit_indexes(theorem_rows)
    ledger: list[dict[str, Any]] = []
    qualified_rank = 0
    quarantine_rank = 0
    for candidate_index, row in enumerate(candidate_rows, 1):
        source_id = str(row["source_record_id"])
        evidence: list[dict[str, Any]] = []
        for feature, values in source_features(row).items():
            policy = FEATURE_POLICY[feature]
            for value in sorted(values):
                targets = feature_indexes[feature][value] - {source_id}
                if not targets:
                    continue
                evidence.append(
                    {
                        **policy,
                        "normalized_value_sha256": value_sha(value),
                        "candidate_source_record_ids": sorted(targets & candidate_ids),
                        "existing_parent_variant_ids": sorted(
                            current_mathlib[target]
                            for target in targets
                            if target in current_mathlib
                        ),
                        "blocks_automatic_theorem_credit": True,
                        "relation_adjudicated": False,
                        "relation_credit_granted": False,
                    }
                )

        candidate_labels = {
            normalized_text(str(row["declaration"])),
            normalized_text(str(row["display_label"])),
        }
        explicit_parent_targets = sorted(
            set().union(*(parent_labels.get(value, set()) for value in candidate_labels))
        )
        if explicit_parent_targets:
            evidence.append(
                {
                    "evidence_type": "same_explicit_parent_label_or_alias",
                    "candidate_relation": "same_named_theorem_candidate",
                    "strength": "exact_parent_label_or_alias_candidate",
                    "normalized_value_sha256": base.set_digest(candidate_labels),
                    "candidate_source_record_ids": [],
                    "existing_parent_variant_ids": explicit_parent_targets,
                    "blocks_automatic_theorem_credit": True,
                    "relation_adjudicated": False,
                    "relation_credit_granted": False,
                }
            )
        declaration_docstring = row.get("declaration_docstring")
        if isinstance(declaration_docstring, str) and declaration_docstring.strip():
            normalized_docstring = normalized_text(declaration_docstring)
            parent_doc_targets = sorted(parent_docstrings.get(normalized_docstring, set()))
            if parent_doc_targets:
                evidence.append(
                    {
                        "evidence_type": "same_explicit_parent_declaration_docstring",
                        "candidate_relation": "same_theorem_or_formal_variant_candidate",
                        "strength": "exact_parent_individual_prose_candidate",
                        "normalized_value_sha256": value_sha(normalized_docstring),
                        "candidate_source_record_ids": [],
                        "existing_parent_variant_ids": parent_doc_targets,
                        "blocks_automatic_theorem_credit": True,
                        "relation_adjudicated": False,
                        "relation_credit_granted": False,
                    }
                )
        for named_label in sorted(source_features(row)["embedded_named_result_label"]):
            parent_named_targets = sorted(parent_named_results.get(named_label, set()))
            if parent_named_targets:
                evidence.append(
                    {
                        "evidence_type": "same_embedded_named_result_label_with_parent",
                        "candidate_relation": "same_named_theorem_or_formal_variant_candidate",
                        "strength": "exact_parent_embedded_named_result_candidate",
                        "normalized_value_sha256": value_sha(named_label),
                        "candidate_source_record_ids": [],
                        "existing_parent_variant_ids": parent_named_targets,
                        "blocks_automatic_theorem_credit": True,
                        "relation_adjudicated": False,
                        "relation_credit_granted": False,
                    }
                )

        evidence.sort(
            key=lambda item: (
                str(item["evidence_type"]),
                str(item["normalized_value_sha256"]),
                tuple(item["candidate_source_record_ids"]),
                tuple(item["existing_parent_variant_ids"]),
            )
        )
        semantic_review = bool(evidence)
        if semantic_review:
            quarantine_rank += 1
            lane = "semantic_variant_review_quarantine"
            lane_rank = quarantine_rank
            semantic_status = "candidate_alias_or_family_signal_requires_review"
            generator_qualified = False
        else:
            qualified_rank += 1
            lane = "provisional_generator_admission"
            lane_rank = qualified_rank
            semantic_status = "no_exact_alias_or_family_signal_found"
            generator_qualified = True

        record: dict[str, Any] = {
            "schema_version": SCHEMA,
            "candidate_index": candidate_index,
            "candidate_key": f"mathlib-qualified-v5.6:{source_id}",
            "source_binding": source_binding(row),
            "declaration": row["declaration"],
            "source_syntax_kind": row["source_syntax_kind"],
            "theorem_record_kind": "theorem",
            "formal_proof_state": row["formal_proof_state"],
            "formal_type_sha256": row["formal_type_sha256"],
            "normalized_formal_type_sha256": base.normalized_type_sha(str(row["formal_type"])),
            "normalized_declaration_name_sha256": base.normalized_name_sha(str(row["declaration"])),
            "module": row["source"]["module"],
            "module_root": base.module_root(row),
            "runtime_truth_status": "kernel_checked_thmInfo_sorry_free_at_pinned_commit",
            "documentation_status": (
                "individual_declaration_docstring"
                if row.get("declaration_docstring") is not None
                else "module_main_result_description"
            ),
            "credit_policy_status": "v5.6_theorem_record_regardless_of_theorem_or_lemma_source_keyword",
            "formal_identity_status": "unique_against_existing_2500_and_qualified_batch",
            "semantic_canonical_status": semantic_status,
            "semantic_alias_evidence": evidence,
            "generator_lane": lane,
            "generator_lane_rank": lane_rank,
            "generator_admission_qualified": generator_qualified,
            "target_variant_id": None,
            "target_stage_claim_id": None,
            "candidate_only": True,
            "grants_catalog_entry": False,
            "grants_theorem_credit": False,
            "row_sha256": None,
        }
        record["row_sha256"] = base.hash_without(record, "row_sha256")
        ledger.append(record)

    counts_by_lane = Counter(str(row["generator_lane"]) for row in ledger)
    counts_by_syntax = Counter(str(row["source_syntax_kind"]) for row in ledger)
    ready_by_syntax = Counter(
        str(row["source_syntax_kind"])
        for row in ledger
        if row["generator_admission_qualified"] is True
    )
    quarantine_by_syntax = Counter(
        str(row["source_syntax_kind"])
        for row in ledger
        if row["generator_admission_qualified"] is False
    )
    evidence_rows = Counter()
    evidence_objects = Counter()
    for row in ledger:
        row_types = {str(item["evidence_type"]) for item in row["semantic_alias_evidence"]}
        evidence_rows.update(row_types)
        evidence_objects.update(str(item["evidence_type"]) for item in row["semantic_alias_evidence"])
    roots_all = Counter(str(row["module_root"]) for row in ledger)
    roots_ready = Counter(
        str(row["module_root"])
        for row in ledger
        if row["generator_admission_qualified"] is True
    )
    counts: dict[str, Any] = {
        "parent_theorem_records": 2_500,
        "parent_mathlib_theorem_records": 1_000,
        "full_mathlib_verified_rows": 2_566,
        "full_mathlib_canonical_formal_identities": 2_561,
        "exact_identity_duplicate_losers_noncredit": len(duplicate_losers),
        "unadmitted_canonical_theorem_candidates": len(ledger),
        "candidate_source_syntax_kinds": dict(sorted(counts_by_syntax.items())),
        "candidate_theorem_record_kind": {"theorem": len(ledger)},
        "exact_or_normalized_parent_identity_conflicts": len(exact_conflicts),
        "generator_lanes": dict(sorted(counts_by_lane.items())),
        "generator_admission_qualified": qualified_rank,
        "semantic_variant_review_quarantine": quarantine_rank,
        "ready_by_source_syntax_kind": dict(sorted(ready_by_syntax.items())),
        "quarantine_by_source_syntax_kind": dict(sorted(quarantine_by_syntax.items())),
        "semantic_evidence_rows_by_type": dict(sorted(evidence_rows.items())),
        "semantic_evidence_objects_by_type": dict(sorted(evidence_objects.items())),
        "reliable_mathlib_formal_identity_inventory_if_all_candidates_admitted": 2_561,
        "catalog_entries_granted_here": 0,
        "theorem_credits_granted_here": 0,
    }
    for key, expected in EXPECTED_COUNTS.items():
        require(counts.get(key) == expected, f"hard count {key}={counts.get(key)!r}, expected {expected!r}")
    if EXPECTED_ALL_ROOTS:
        require(dict(sorted(roots_all.items())) == EXPECTED_ALL_ROOTS, "all-candidate root counts drifted")
    if EXPECTED_READY_ROOTS:
        require(
            dict(sorted(roots_ready.items())) == EXPECTED_READY_ROOTS,
            f"ready-candidate root counts drifted: {dict(sorted(roots_ready.items()))!r}",
        )

    ledger_payload = b"".join(base.canonical(row) + b"\n" for row in ledger)
    inventory: dict[str, Any] = {
        "schema_version": INVENTORY_SCHEMA,
        "artifact": QUALIFIED_INVENTORY.name,
        "as_of": "2026-08-10",
        "candidate_only": True,
        "release_mutation_authorized_or_performed": False,
        "counts": counts,
        "module_root_counts": {
            "all_candidates": dict(sorted(roots_all.items())),
            "generator_admission_qualified": dict(sorted(roots_ready.items())),
        },
        "exact_identity_duplicate_losers": duplicate_losers,
        "inputs": {
            "full_mathlib_source": base.binding(base.FULL_SOURCE, full_payload),
            "parent_5_5_theorem_list": base.binding(THEOREM_LIST, theorem_payload),
            "parent_5_5_manifest": base.binding(base.PARENT_MANIFEST, manifest_payload),
            "mathlib_extractor": base.binding(base.EXTRACTOR, base.EXTRACTOR.read_bytes()),
            "qualification_builder": base.binding(
                Path(__file__).resolve(), Path(__file__).resolve().read_bytes()
            ),
        },
        "output": {
            "path": QUALIFIED_LEDGER.relative_to(REPO).as_posix(),
            "sha256": base.sha(ledger_payload),
            "size_bytes": len(ledger_payload),
            "rows": len(ledger),
            "row_sha256_set_sha256": base.set_digest(str(row["row_sha256"]) for row in ledger),
            "source_record_id_set_sha256": base.set_digest(str(row["source_binding"]["source_record_id"]) for row in ledger),
            "formal_type_sha256_set_sha256": base.set_digest(str(row["formal_type_sha256"]) for row in ledger),
        },
        "v5_6_policy": {
            "theorem_record_rule": (
                "Lean source commands `theorem` and `lemma` both become theorem records when runtime kind is "
                "ConstantInfo.thmInfo and the pinned collectAxioms batch union excludes sorryAx."
            ),
            "formal_identity_rule": (
                "One canonical source row per exact or Unicode-whitespace-normalized formal type; all five "
                "losers remain noncredit and are listed in this inventory."
            ),
            "semantic_variant_rule": (
                "A shared Wikidata ID, exact display label, exact embedded Markdown-bold named-result label, "
                "exact declaration docstring, normalized mathlib declaration leaf, or exact module Main-result "
                "description is a review signal, not a proved equivalence. Any such signal blocks automatic "
                "theorem credit and routes the row to quarantine."
            ),
            "absence_boundary": (
                "No mechanical alias/family signal is not proof that two statements represent different human-level "
                "mathematical theorems. The provisional lane remains candidate-only until release acceptance."
            ),
        },
        "generator_contract": {
            "input_rows": 1_561,
            "record_kind": "theorem for every row, independent of source_syntax_kind",
            "provisional_admission_filter": (
                "generator_lane == 'provisional_generator_admission' and "
                "generator_admission_qualified == true"
            ),
            "mandatory_quarantine_filter": (
                "generator_lane == 'semantic_variant_review_quarantine' or "
                "generator_admission_qualified == false"
            ),
            "source_join": "join source_binding.source_record_id and verify source_record_sha256 against full_mathlib_source",
            "id_allocation": "must remain null until a later append-only release transaction",
            "credit": "this ledger grants zero catalog entries and zero theorem credits",
        },
        "putnam_closure_join_boundary": {
            "status": "pending independently sealed Putnam target-declaration ledger",
            "closure_node_requires_any_of": [
                "exact direct mathlib declaration reference in elaborated Putnam theorem type",
                "exact direct mathlib declaration reference in an elaborated Putnam solution/proof body",
                "authoritative named-theorem label corroborated by exact Wikidata or declaration identity and semantic review",
            ],
            "forbidden_inferences": [
                "direction inferred from theorem naming",
                "edge inferred from import or transitive dependency alone",
                "edge inferred from broad topic tag",
                "edge inferred from label or embedding similarity alone",
            ],
            "edge_credit": "no closure edge is granted by this qualification artifact",
        },
        "authority_sha256": None,
    }
    inventory["authority_sha256"] = base.hash_without(inventory, "authority_sha256")
    return ledger, inventory


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="wb", prefix=path.name + ".", suffix=".tmp", dir=path.parent, delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def compare(path: Path, expected: bytes) -> None:
    try:
        observed = path.read_bytes()
    except OSError as error:
        raise QualificationError(f"cannot read {path}: {error}") from error
    require(
        observed == expected,
        f"generated output drift: {path} sha256={base.sha(observed)}, expected {base.sha(expected)}",
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="atomically write qualified outputs")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        ledger, inventory = build()
        ledger_payload = b"".join(base.canonical(row) + b"\n" for row in ledger)
        inventory_payload = base.pretty(inventory)
        if args.write:
            atomic_write(QUALIFIED_LEDGER, ledger_payload)
            atomic_write(QUALIFIED_INVENTORY, inventory_payload)
            action = "wrote"
        else:
            compare(QUALIFIED_LEDGER, ledger_payload)
            compare(QUALIFIED_INVENTORY, inventory_payload)
            action = "checked"
        counts = inventory["counts"]
        print(
            f"PASS {action} mathlib qualified batch v5.6 "
            f"candidates={counts['unadmitted_canonical_theorem_candidates']} "
            f"ready={counts['generator_admission_qualified']} "
            f"quarantine={counts['semantic_variant_review_quarantine']} "
            f"authority={inventory['authority_sha256']}"
        )
        return 0
    except (QualificationError, base.InventoryError) as error:
        print(f"FAIL mathlib qualified batch v5.6: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
