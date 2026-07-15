#!/usr/bin/env python3
"""Build or verify the frozen THM-M-0812 obligation architecture."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM_ID = "S56-M-0812-OBLIGATION_TREE"
THEOREM_ID = "THM-M-0812"
PREFIX = "M0812"
FROZEN_AT = "2026-07-16T00:00:00+08:00"
ROOT_EXPRESSION = "b20dc7426179377f6838e3ca384aaa80431d00713953494a5ea789d84ec1d7b4"
STATEMENT_BUNDLE = "8b8107e613a53247d69c71d1a838fd4719b3c0330e4a707b54060bd9247dc0f1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
CONTEXT_DIGEST = "bc99f9e70a837e425f01f88835dda207b07138301527ae3715e6640b0998be7d"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def spec(
    suffix: str,
    kind: str,
    risk: str,
    claim: str,
    formal: str,
    output: str,
    source: str,
    method: str,
    budget: int,
    *,
    machine_eligibility: str = "required",
    human_source_eligibility: str = "required",
    terminal_body: str | None = None,
) -> dict:
    registry_kind = {
        "normalization": "reduction",
        "core_lemma": "lemma",
        "certificate": "terminal",
    }.get(kind, kind)
    return {
        "id": f"{PREFIX}-{suffix}",
        "kind": registry_kind,
        "node_kind": kind,
        "risk": risk,
        "claim": claim,
        "formal": formal,
        "output": output,
        "source": source,
        "method": method,
        "budget": budget,
        "machine_eligibility": machine_eligibility,
        "human_source_eligibility": human_source_eligibility,
        "terminal_body": terminal_body,
    }


SPECS = [
    spec("ROOT", "root", "critical", "For every finite two-sorted bipartite incidence graph, one natural number is both its attained maximum matching size and attained minimum vertex-cover size.", "Stage1Instances.THM_M_0812.KonigMatchingCoverTarget", "The exact canonical proposition at universes uL, uR, and uE.", "Statement.lean#KonigMatchingCoverTarget", "Compose finite matching attainment, the maximum-matching cover construction, and weak duality without changing the frozen binders or extrema.", 8),
    spec("S-TARGET", "definition", "critical", "Freeze the exact finite incidence target and its expression and bundle fingerprints.", "Stage1Instances.THM_M_0812.KonigMatchingCoverTarget", "The canonical target interface, counted once at the root.", "Statement.lean; statement.json canonical_formal_target", "Preserve the exact ordered types, instances, endpoint maps, existential k, and both extremal predicates.", 8, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("S-REPRESENTATION", "definition", "high", "Use typed sides L and R, an independent edge-identity type E, and endpoint maps so isolated vertices and parallel edges remain representable.", "Stage1Instances.THM_M_0812.IsEdgeMatching; Stage1Instances.THM_M_0812.IsBipartiteVertexCover", "A source-faithful finite bipartite incidence representation.", "Statement.lean:17-31", "Propagate the typed-side incidence model to every construction and avoid silently switching to a one-sorted simple graph.", 14, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("S-EXTREMA", "definition", "critical", "Maximum and minimum mean attained witnesses plus universal natural-cardinality bounds, not maximality or minimality by inclusion.", "Stage1Instances.THM_M_0812.HasMatchingNumber; Stage1Instances.THM_M_0812.HasVertexCoverNumber", "The exact matching-number and vertex-cover-number interfaces.", "Statement.lean:33-53", "Retain both witness and universal-bound conjuncts and count matching edges versus tagged side vertices.", 14, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("S-BOUNDARY", "branch", "high", "Retain edgeless graphs, isolated vertices, empty sides when E is empty, singleton graphs, and parallel-edge identities.", "Stage1Instances.THM_M_0812.edgelessBoundary; Stage1Instances.THM_M_0812.singleEdgeBoundary", "No hidden nonempty or simplicity premise.", "Statement.lean#edgelessBoundary; Statement.lean#singleEdgeBoundary", "Carry every admitted degenerate case through the proof architecture; do not discharge it by strengthening the target.", 16, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("S-TRANSPORT", "transport", "critical", "Bind the named target to its direct expansion and to simple-relation erasure in both checked directions.", "Stage1Instances.THM_M_0812.konigMatchingCoverTarget_iff_expanded; Stage1Instances.THM_M_0812.konigMatchingCoverTarget_iff_simpleRelationKonigTarget", "Checked representation relationships without duplicate root credit.", "Statement.lean#konigMatchingCoverTarget_iff_expanded; Statement.lean#konigMatchingCoverTarget_iff_simpleRelationKonigTarget", "Use the local Iffs only in their declared directions and deduplicate them from semantic proof coverage.", 16, machine_eligibility="informational", human_source_eligibility="not_applicable", terminal_body="repo:Statement.lean#konigMatchingCoverTarget_iff_simpleRelationKonigTarget"),
    spec("S-FOUNDATION", "certificate", "critical", "Account for propositional extensionality, classical choice, quotient soundness, Lean, mathlib, and a no-oracle computation policy.", "stage1-foundation-profile/1.0", "A reviewed foundation decision, not a theorem premise.", "anchor-audit.json immutable_environment", "Compare machine-derived terminal dependencies with the accepted profile and reject unknown or placeholder trust paths.", 40, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("N-FINITE-SETS", "normalization", "high", "Expose finite matching candidates and finite cardinalities without adding decidability or nonemptiness assumptions.", "planned finite Set E and Set.ncard interfaces", "A finite search space on which maximum cardinality is attained.", "Statement.lean finite binders; Mathlib.Data.Finite.Card", "Obtain local finite interfaces from [Finite E] and keep the empty matching as the nonempty candidate witness.", 24),
    spec("N-SIMPLE-RELATION", "normalization", "high", "Erase parallel edge identities only after the checked statement transport proves that both extrema are preserved.", "Stage1Instances.THM_M_0812.konigMatchingCoverTarget_iff_simpleRelationKonigTarget", "A simple endpoint-pair relation route equivalent to the canonical target.", "Statement.lean:367-406", "Use endpoint representatives and cardinality-preserving image lemmas; retain the canonical incidence target as the root.", 20, machine_eligibility="informational", human_source_eligibility="not_applicable", terminal_body="repo:Statement.lean#konigMatchingCoverTarget_iff_simpleRelationKonigTarget"),
    spec("N-ALTERNATING-REACH", "normalization", "critical", "Normalize the translated path process to alternating reachability from unmatched left vertices relative to a chosen maximum matching.", "planned alternating reachability predicate", "Stable reachable-left and reachable-right vertex sets.", "translated Konig 1931 pp.1-2", "Define reachability with explicit parity and matching/nonmatching edge roles before selecting the cover.", 34),
    spec("T-MATCHING-ATTAIN", "terminal", "critical", "Every finite incidence graph has an attained maximum matching cardinality.", "Stage1Instances.THM_M_0812_Obligations.MatchingAttainmentTarget", "Exists k, HasMatchingNumber left right k for every finite E.", "ObligationTree.lean#MatchingAttainmentTarget", "Select a matching of greatest ncard from the finite candidate set and prove the universal bound.", 24),
    spec("C-MAX-MATCHING", "construction", "high", "Choose a maximum matching witness M and retain both injectivity conditions and M.ncard = k.", "planned extraction from HasMatchingNumber", "A fixed matching driving the alternating construction.", "Statement.lean#HasMatchingNumber", "Eliminate only the attained-witness conjunct and keep the universal bound available for the no-augmentation contradiction.", 10),
    spec("T-COVER-FROM-MAX", "terminal", "critical", "Every attained maximum matching of size k yields a vertex cover of cardinality k.", "Stage1Instances.THM_M_0812_Obligations.MaximumMatchingCoverTarget", "Exists CLeft CRight, cover and CLeft.ncard + CRight.ncard = k.", "ObligationTree.lean#MaximumMatchingCoverTarget; translated Konig 1931 pp.1-2", "Build alternating reachability, select the unreached left and reached right endpoints, prove coverage, and count exactly one selected endpoint per matching edge.", 18),
    spec("C-ALT-PATH", "construction", "critical", "Construct alternating paths whose first edge is outside M and whose edge membership alternates thereafter.", "planned finite path object with parity invariant", "A path/reachability witness with explicit endpoints and alternation.", "translated Konig 1931 pp.1-2", "Define the finite path object, endpoint side, simplicity, and parity-indexed membership in M.", 42),
    spec("L-ALT-PATH-NORMALIZE", "core_lemma", "high", "Any alternating walk witness can be shortened to a simple alternating path without changing endpoints.", "planned walk-to-path normalization", "A simple path suitable for augmentation and counting.", "translated proof route; formal normalization obligation", "Erase loops while proving the alternating invariant survives every splice.", 35),
    spec("C-REACHABLE-SIDES", "construction", "critical", "Define ZLeft and ZRight as vertices reached from unmatched left vertices by alternating paths of the appropriate parity.", "planned Set L and Set R definitions", "The two reachability sets used by the cover formula.", "translated Konig 1931 pp.1-2", "Project normalized path endpoints to typed sides and retain an origin unmatched-left witness.", 28),
    spec("C-AUGMENT", "construction", "critical", "Toggle matching membership along an alternating path from an unmatched left vertex to an unmatched right vertex.", "planned Set E symmetric-difference construction", "A new matching with one additional edge.", "translated Konig 1931 no-augmenting-path argument", "Define the toggled edge set and separate endpoint, internal-vertex, and off-path injectivity cases.", 38),
    spec("L-AUGMENT-MATCHING", "core_lemma", "critical", "The toggled edge set is still injective under both endpoint maps.", "planned IsEdgeMatching proof for augmentation", "IsEdgeMatching left right augmentedM.", "translated proof route; formal invariant obligation", "Use path simplicity and alternation to show each internal vertex loses and gains exactly one incident chosen edge.", 48),
    spec("L-AUGMENT-CARD", "core_lemma", "critical", "An odd alternating augmenting path adds exactly one chosen edge.", "planned ncard augmentedM = M.ncard + 1", "Strictly larger matching cardinality.", "translated proof route; finite cardinality obligation", "Pair removed path edges with all but one added path edge and preserve off-path membership.", 36),
    spec("L-NO-AUGMENTING", "core_lemma", "critical", "A maximum matching admits no alternating path from an unmatched left vertex to an unmatched right vertex.", "planned contradiction from HasMatchingNumber universal bound", "Every reached right vertex is matched by M.", "translated Konig 1931 pp.1-2", "Assume such a path, invoke the matching and cardinality augmentation lemmas, and contradict maximal cardinality.", 22),
    spec("L-REACHED-R-MATCHED", "core_lemma", "high", "Each reached right vertex is incident to a unique matching edge.", "planned endpoint existence and uniqueness", "A matching-edge predecessor for every member of ZRight.", "translated Konig 1931 pp.1-2", "Use no-augmentation for existence and right-endpoint injectivity for uniqueness.", 24),
    spec("L-MATCHED-REACH-IFF", "core_lemma", "critical", "For each matching edge, its left endpoint is reached exactly when its right endpoint is reached.", "planned iff on endpoints of e in M", "Matched edges pair ZLeft and ZRight membership.", "translated Konig 1931 pp.1-2", "Extend or truncate an alternating path by the matching edge in the two directions.", 28),
    spec("C-SELECTED-COVER", "construction", "critical", "Select CLeft = left endpoints not in ZLeft and CRight = ZRight.", "planned Set L and Set R cover", "The canonical cover extracted from the maximum matching.", "translated Konig 1931 endpoint selection", "Define the two sets extensionally and retain their disjoint typed-side cardinalities.", 12),
    spec("B-EDGE-MEMBER-SPLIT", "branch", "critical", "Split every graph edge according to membership in the fixed maximum matching.", "planned by_cases e in M", "Exhaustive matching-edge versus nonmatching-edge cases.", "translated Konig 1931 four-case coverage proof", "Run classical excluded middle on e membership and preserve the exact endpoint goal in both branches.", 8),
    spec("B-FOUR-ENDPOINT-CASES", "branch", "critical", "For a nonmatching edge, split reachability of its left and right endpoints and rule out the uncovered configuration by extending an alternating path.", "planned four endpoint-membership cases", "Every nonmatching edge meets CLeft or CRight.", "translated Konig 1931 pp.1-2", "Enumerate the four membership pairs; the only potentially uncovered pair would make the right endpoint reachable.", 26),
    spec("L-COVER-EVERY-EDGE", "core_lemma", "critical", "The selected left and right sets cover every edge.", "Stage1Instances.THM_M_0812.IsBipartiteVertexCover left right CLeft CRight", "The cover predicate for the constructed sets.", "translated Konig 1931 four cases", "Combine the matching-edge reachability iff with the exhaustive nonmatching endpoint cases.", 24),
    spec("C-COVER-BIJECTION", "construction", "critical", "Associate each matched edge with exactly one selected endpoint: right when reached, left otherwise.", "planned equivalence between M and Sum CLeft CRight", "A cardinality-preserving selection map.", "translated Konig 1931 endpoint selection", "Use left/right endpoint injectivity for injectivity and reached-right matching plus matched reachability iff for surjectivity.", 38),
    spec("L-COVER-CARD", "core_lemma", "critical", "The constructed cover has CLeft.ncard + CRight.ncard = M.ncard = k.", "planned Set.ncard equality", "Exact cover cardinality k.", "translated Konig 1931 pp.1-2", "Convert the cover bijection to cardinal equality and rewrite by the maximum-matching witness equation.", 26),
    spec("B-COVER-MERGE", "branch", "high", "Recompose coverage and cardinality into the exact cover-from-maximum existential.", "planned conjunction/existential assembly", "Exists CLeft CRight, cover and exact cardinality.", "ObligationTree.lean#MaximumMatchingCoverTarget", "Package the selected sets, coverage lemma, and cardinality lemma without introducing a minimum-cover premise.", 10),
    spec("T-WEAK-DUALITY", "terminal", "critical", "Every vertex cover has size at least every matching.", "Stage1Instances.THM_M_0812_Obligations.WeakDualityTarget", "M.ncard <= CLeft.ncard + CRight.ncard.", "ObligationTree.lean#WeakDualityTarget; translated Konig 1931 reverse inequality", "Map each matching edge to a covering endpoint and prove injectivity using matching endpoint injectivity and tagged sides.", 18),
    spec("C-DUALITY-INJECTION", "construction", "critical", "Choose for each matching edge a tagged covering endpoint in CLeft or CRight.", "planned injection M -> Sum CLeft CRight", "A finite injection from matching edges to cover vertices.", "translated Konig 1931 p.2 reverse bound", "Use the cover disjunction to choose a tagged endpoint and prove equal images force equal edges on the corresponding side.", 34),
    spec("L-WEAK-DUALITY-INJECTION", "core_lemma", "high", "The tagged endpoint choice is injective and yields the natural-cardinality inequality.", "planned Fintype.card_le_of_injective / Set.ncard bound", "The exact weak-duality inequality.", "translated Konig 1931 p.2", "Apply finite cardinal monotonicity and normalize the cardinal of a disjoint sum to the sum of set ncard values.", 22),
    spec("T-ASSEMBLE", "terminal", "critical", "Bundle attainment, equal-size cover construction, and weak duality into the exact extremal predicates.", "Stage1Instances.THM_M_0812_Obligations.AssemblyTarget", "All three child packages required by the exact root.", "ObligationTree.lean#AssemblyTarget", "Use the attained matching witness, construct an equal-size cover, and derive its universal minimum bound from weak duality.", 12, terminal_body="repo:ObligationTree.lean#root_of_assembly"),
    spec("X-IMPORTS", "terminal", "high", "Audit direct and transitive Lean imports, declaration bodies, licenses, and exact compatibility before any external theorem is credited.", "stage1-import-boundary-record/1.0", "A content-bound import decision with no hidden proof premise.", "anchor-audit.json; dependency-reuse-ledger.json", "Reject ATLAS sorryAx and the unintegrated PR; retain mathlib APIs only as substrate until exact use is implemented.", 55, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("X-COMPUTATION", "computation", "normal", "Record that this symbolic architecture uses no solver, oracle, experiment, native decision, or unchecked certificate.", "stage1-computation-record/1.0", "An explicit no-computation boundary pending independent approval.", "instance.json computation_profile", "Reopen this obligation if future finite search or reflected computation becomes proof-relevant.", 12, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("X-SOURCE", "terminal", "high", "Map every material mathematical obligation to an admitted primary edition, exact locator, assumptions, translations, corrections, and independent review.", "stage1-source-crosswalk-record/1.0", "An independently reviewed H0 source crosswalk.", "source-statement-crosswalk.md; translated Konig 1931 pp.1-3", "Inspect the Hungarian original, translation fidelity, and errata, then approve the node-specific mapping; the current translation remains H1 evidence only.", 90, machine_eligibility="not_applicable"),
    spec("X-PROVENANCE", "certificate", "critical", "Bind wrapper, conclusion, future terminal bodies, origins, hashes, licenses, aliases, and revocations without duplicate credit.", "stage1-provenance-closure-record/1.0", "Release-grade proof-body provenance.", "anchor-audit.json; dependency-reuse-ledger.json", "Traverse actual terminal declarations and keep statement transports and conditional composition separate from proof bodies.", 70, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("X-TRUST", "certificate", "critical", "Close transitive declarations, axioms, compiled artifacts, unsafe/oracle boundaries, TCB, and independent replay.", "stage1-trust-closure-record/1.0", "Accepted trust closure under the selected foundation policy.", "anchor-audit.json immutable_environment", "Derive trust from terminal objects, not names; reject placeholders, unknown bodies, and moving dependencies.", 70, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("X-READABLE", "terminal", "high", "Produce and independently review a complete node-specific proof reconstruction linked to exact fingerprints.", "stage1-readable-crosswalk-record/1.0", "Readable R0 coverage without machine proof credit.", "obligation-tree.md", "Expand the accepted alternating-path proof route while distinguishing architecture plans from checked proof bodies.", 90, machine_eligibility="informational", human_source_eligibility="not_applicable"),
    spec("X-WORKFLOW", "terminal", "critical", "Bind dependency inspection, proof, composition, validation, source, readability, freshness, revocation, independent verification, and release tasks.", "stage1-workflow-state-record/1.0", "Only dependency-legal provisional or accepted execution states.", "Docs/Stage1_Execution_DAG_rev-5.6.json; dependency-reuse-ledger.json", "Reject acceptance before predecessor and node-specific receipt gates pass, and refresh the dependency context on invalidation.", 30, machine_eligibility="informational", human_source_eligibility="not_applicable"),
]


REQUIRES = {
    "M0812-ROOT": ["M0812-T-ASSEMBLE"],
    "M0812-T-ASSEMBLE": ["M0812-T-MATCHING-ATTAIN", "M0812-T-COVER-FROM-MAX", "M0812-T-WEAK-DUALITY"],
    "M0812-T-MATCHING-ATTAIN": ["M0812-N-FINITE-SETS", "M0812-C-MAX-MATCHING"],
    "M0812-T-COVER-FROM-MAX": ["M0812-C-MAX-MATCHING", "M0812-N-ALTERNATING-REACH", "M0812-C-ALT-PATH", "M0812-C-REACHABLE-SIDES", "M0812-L-NO-AUGMENTING", "M0812-C-SELECTED-COVER", "M0812-L-COVER-EVERY-EDGE", "M0812-L-COVER-CARD", "M0812-B-COVER-MERGE"],
    "M0812-N-ALTERNATING-REACH": ["M0812-C-ALT-PATH", "M0812-L-ALT-PATH-NORMALIZE"],
    "M0812-C-REACHABLE-SIDES": ["M0812-C-ALT-PATH", "M0812-L-ALT-PATH-NORMALIZE"],
    "M0812-L-NO-AUGMENTING": ["M0812-C-AUGMENT", "M0812-L-AUGMENT-MATCHING", "M0812-L-AUGMENT-CARD"],
    "M0812-L-REACHED-R-MATCHED": ["M0812-L-NO-AUGMENTING"],
    "M0812-L-MATCHED-REACH-IFF": ["M0812-C-ALT-PATH", "M0812-C-REACHABLE-SIDES"],
    "M0812-L-COVER-EVERY-EDGE": ["M0812-B-EDGE-MEMBER-SPLIT", "M0812-B-FOUR-ENDPOINT-CASES", "M0812-L-MATCHED-REACH-IFF"],
    "M0812-C-COVER-BIJECTION": ["M0812-L-REACHED-R-MATCHED", "M0812-L-MATCHED-REACH-IFF", "M0812-C-SELECTED-COVER"],
    "M0812-L-COVER-CARD": ["M0812-C-COVER-BIJECTION"],
    "M0812-B-COVER-MERGE": ["M0812-C-SELECTED-COVER", "M0812-L-COVER-EVERY-EDGE", "M0812-L-COVER-CARD"],
    "M0812-T-WEAK-DUALITY": ["M0812-C-DUALITY-INJECTION", "M0812-L-WEAK-DUALITY-INJECTION"],
    "M0812-L-WEAK-DUALITY-INJECTION": ["M0812-C-DUALITY-INJECTION"],
}


REGISTRY_FIELDS = (
    "obligation_id",
    "statement_fingerprint",
    "kind",
    "root_relevant",
    "machine_eligibility",
    "human_source_eligibility",
    "readable_eligibility",
    "risk_class",
    "exclusion_reason",
    "terminal_proof_body_id",
)


def fingerprint(row: dict) -> str:
    if row["id"] in {"M0812-ROOT", "M0812-S-TARGET"}:
        return "lean-expression-sha256:" + ROOT_EXPRESSION
    payload = {
        "obligation_id": row["id"],
        "claim": row["claim"],
        "formal_target": row["formal"],
        "output": row["output"],
        "statement_bundle": STATEMENT_BUNDLE,
    }
    return "architecture:v1:sha256:" + canonical_digest(payload)


def make_graph(edges: list[dict], endpoints: list[str]) -> dict:
    outgoing = {node: [] for node in endpoints}
    incoming = {node: [] for node in endpoints}
    for edge in edges:
        outgoing[edge["from"]].append(edge["edge_id"])
        incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


def proof_edges() -> tuple[list[dict], list[dict]]:
    edges = []
    plans = []
    index = 1
    for parent, children in REQUIRES.items():
        for child in children:
            req = f"PROOF-{index:03d}-REQ"
            back = f"PROOF-{index:03d}-BACK"
            checked = parent in {"M0812-ROOT", "M0812-T-ASSEMBLE"}
            back_type = "composes" if checked else "logical_decomposition"
            edges.extend(
                [
                    {"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": back},
                    {"edge_id": back, "from": child, "type": back_type, "to": parent, "reciprocal_edge_id": req},
                ]
            )
            if not checked:
                plans.append(
                    {
                        "parent_obligation_id": parent,
                        "child_obligation_id": child,
                        "status": "frozen source-shaped decomposition; exact child-to-parent Lean composition remains open",
                    }
                )
            index += 1
    return edges, plans


def build() -> tuple[dict, dict, dict, str]:
    obligations = []
    nodes = []
    for row in SPECS:
        excluded = None
        if row["machine_eligibility"] != "required":
            excluded = (
                "human_source_boundary_no_machine_proof_credit_pending_independent_approval"
                if row["machine_eligibility"] == "not_applicable"
                else "typed_overlay_or_assurance_boundary_no_duplicate_machine_proof_credit_pending_independent_approval"
            )
        obligation = {
            "obligation_id": row["id"],
            "statement_fingerprint": fingerprint(row),
            "kind": row["kind"],
            "root_relevant": True,
            "machine_eligibility": row["machine_eligibility"],
            "human_source_eligibility": row["human_source_eligibility"],
            "readable_eligibility": "required",
            "risk_class": row["risk"],
            "exclusion_reason": excluded,
            "terminal_proof_body_id": row["terminal_body"],
        }
        obligations.append(obligation)
        children = REQUIRES.get(row["id"], [])
        step = {
            "step_id": row["id"] + "-STEP-01",
            "premise_ids": children or ["frozen-formal-context"],
            "inference": row["method"],
            "source_locator": row["source"],
            "output": row["output"],
            "outgoing_use": [
                parent for parent, child_ids in REQUIRES.items() if row["id"] in child_ids
            ] or ["typed-non-proof-edge-or-canonical-root-boundary"],
        }
        nodes.append(
            {
                "node_id": f"{THEOREM_ID}-{row['id'].removeprefix(PREFIX + '-')}",
                "obligation_id": row["id"],
                "kind": row["node_kind"],
                "human_statement": row["claim"],
                "formal_target": row["formal"],
                "output": row["output"],
                "human_debt": "H1" if row["human_source_eligibility"] == "required" else "H2",
                "machine_debt": "M3",
                "readability_debt": "R2",
                "evidence_ids": [],
                "source_crosswalk_id": "source-statement-crosswalk.md; node pinpoint and independent review pending" if row["human_source_eligibility"] == "required" else "not-applicable-pending-independent-approval",
                "provenance_id": "anchor-audit.json; terminal-body acceptance pending" if row["terminal_body"] else "none",
                "foundation_profile": "Lean4 dependent type theory; propext, Classical.choice, and Quot.sound observed on checked interfaces; accepted terminal policy pending",
                "tcb_profile": f"Lean-4.29.0 plus mathlib-{MATHLIB_REVISION[:8]}; terminal proof and independent replay closure pending",
                "computation_record": "none; no solver, oracle, native shortcut, experiment, or unchecked certificate is credited",
                "step_budget": row["budget"],
                "semantic_step_ledger": [step],
                "public_readable_target": f"Stage1_Instances/{THEOREM_ID}/obligation-tree.md#{row['id'].lower()}",
                "validation_spec_id": f"VAL-{row['id']}",
                "status_boundary": "Frozen architecture or conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.",
                "task_ids": [ITEM_ID, "S56-M-0812-PROOF", "S56-M-0812-VALIDATION"],
                "owned_sources": ["Stage1_Instances/THM-M-0812/ObligationTree.lean"] if row["id"] in {"M0812-T-MATCHING-ATTAIN", "M0812-T-COVER-FROM-MAX", "M0812-T-WEAK-DUALITY", "M0812-T-ASSEMBLE", "M0812-ROOT"} else [],
                "owner": "THM-M-0812 proof lane",
                "reviewer": "unassigned independent Stage1 integration reviewer",
                "validity": {
                    "validated_at": None,
                    "review_due": "before proof acceptance",
                    "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "dependency-reuse-ledger.json", "obligation-registry.json", "typed-graphs.json", "source crosswalk", "toolchain", "dependency pins"],
                    "revocation_state": "open",
                },
            }
        )

    denominator = canonical_digest(
        [{field: row[field] for field in REGISTRY_FIELDS} for row in obligations]
    )
    ids = [row["obligation_id"] for row in obligations]
    layer_map = {
        "S_statement_foundation": [x for x in ids if "-S-" in x],
        "N_normalization": [x for x in ids if "-N-" in x],
        "B_branch": [x for x in ids if "-B-" in x],
        "C_construction": [x for x in ids if "-C-" in x],
        "L_core_lemma": [x for x in ids if "-L-" in x],
        "X_external_computation": [x for x in ids if "-X-" in x],
        "T_terminal": [x for x in ids if "-T-" in x] + ["M0812-ROOT"],
    }
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "registry_id": "THM-M-0812-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": FROZEN_AT,
        "freeze_basis": "The exact statement, translated-primary alternating-path route, immutable anchor audit, and v2 reuse context fix the semantic obligation universe before any proof-phase closure observation.",
        "frozen_against_statement_sha256": sha256(HERE / "Statement.lean"),
        "frozen_against_anchor_audit_sha256": sha256(HERE / "anchor-audit.json"),
        "frozen_against_dependency_context_sha256": CONTEXT_DIGEST,
        "root_obligation_id": "M0812-ROOT",
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [x["obligation_id"] for x in obligations if x["machine_eligibility"] == "required"],
            "required_human_source": [x["obligation_id"] for x in obligations if x["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [x["obligation_id"] for x in obligations if x["machine_eligibility"] != "required"],
        },
        "mandatory_layer_analysis": {
            key: {"state": "required", "obligation_ids": values} for key, values in layer_map.items()
        },
        "deduplication_policy": "The root, direct expansion, simple-relation transport, conditional assembly, aliases, wrappers, and any future shared terminal body are deduplicated. Only distinct semantic obligations and terminal bodies receive coverage credit.",
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility, risk, or terminal-body identity change requires registry v2 with an append-only old/new delta; v1 denominators remain reportable.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "checked_conditional_composition": ["M0812-T-ASSEMBLE", "M0812-ROOT"],
            "accepted_closed_obligations": [],
            "authoritative_root_machine_debt": "M3",
            "authoritative_root_vector": {"H": "H1", "M": "M3", "R": "R2"},
        },
        "status_boundary": "Registry scope and frozen denominators only. No proof child or terminal body is accepted, and H0, M0, R0, AUDIT-Z, theorem completion, and release remain open.",
    }

    proof, plans = proof_edges()
    refinement_edges = [
        {"edge_id": "REF-001", "from": "M0812-S-TRANSPORT", "type": "equivalent_to", "to": "M0812-S-TARGET"},
        {"edge_id": "REF-002", "from": "M0812-N-SIMPLE-RELATION", "type": "transports", "to": "M0812-S-TARGET"},
        {"edge_id": "REF-003", "from": "M0812-S-BOUNDARY", "type": "expository_decomposition", "to": "M0812-S-TARGET"},
    ]
    provenance_edges = [
        {"edge_id": f"PROV-{i:03d}", "from": "M0812-X-PROVENANCE", "type": "provenance_of", "to": node}
        for i, node in enumerate(ids, 1) if node != "M0812-X-PROVENANCE"
    ] + [
        {"edge_id": "PROV-SOURCE", "from": "M0812-X-SOURCE", "type": "source_map", "to": "M0812-T-COVER-FROM-MAX"},
        {"edge_id": "PROV-DUALITY", "from": "M0812-X-SOURCE", "type": "source_map", "to": "M0812-T-WEAK-DUALITY"},
    ]
    trust_edges = [
        {"edge_id": f"TRUST-{i:03d}", "from": node, "type": "trusts", "to": "M0812-X-TRUST"}
        for i, node in enumerate(ids, 1) if node != "M0812-X-TRUST"
    ]
    documentation_edges = [
        {"edge_id": f"DOC-{i:03d}", "from": "M0812-X-READABLE", "type": "documents", "to": node}
        for i, node in enumerate(ids, 1) if node != "M0812-X-READABLE"
    ]
    tasks = [
        "S56-M-0812-INTAKE",
        "S56-M-0812-STATEMENT",
        "S56-M-0812-ANCHOR_AUDIT",
        "S56-M-0812-OBLIGATION_TREE",
        "S56-M-0812-PROOF",
        "S56-M-0812-VALIDATION",
        "S56-M-0812-RELEASE",
    ]
    workflow_edges = [
        {"edge_id": f"FLOW-{i:03d}", "from": tasks[i], "type": "workflow_depends_on", "to": tasks[i - 1]}
        for i in range(1, len(tasks))
    ]
    graphs = {
        "proof": make_graph(proof, ids),
        "refinement": make_graph(refinement_edges, ids),
        "provenance": make_graph(provenance_edges, ids),
        "evidence": make_graph([], ids),
        "trust": make_graph(trust_edges, ids),
        "documentation": make_graph(documentation_edges, ids),
        "workflow": make_graph(workflow_edges, tasks),
    }
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": "M0812-ROOT",
        "edge_direction": "from consumer or dependent node to required/supporting node unless the edge type states composition or documentation",
        "nodes": nodes,
        "graphs": graphs,
        "workflow_task_nodes": tasks,
        "composition_certificates": [
            {
                "certificate_id": "COMP-M0812-T-ASSEMBLE",
                "parent_obligation_id": "M0812-T-ASSEMBLE",
                "parent_statement_fingerprint": next(x["statement_fingerprint"] for x in obligations if x["obligation_id"] == "M0812-T-ASSEMBLE"),
                "child_obligation_ids": ["M0812-T-MATCHING-ATTAIN", "M0812-T-COVER-FROM-MAX", "M0812-T-WEAK-DUALITY"],
                "declaration": "Stage1Instances.THM_M_0812_Obligations.assembly_of_construction_and_duality",
                "kind": "Lean abstract-child harness",
                "status": "provisional kernel-checked conditional composition; all three children remain open",
            },
            {
                "certificate_id": "COMP-M0812-ROOT",
                "parent_obligation_id": "M0812-ROOT",
                "parent_statement_fingerprint": "lean-expression-sha256:" + ROOT_EXPRESSION,
                "child_obligation_ids": ["M0812-T-ASSEMBLE"],
                "declaration": "Stage1Instances.THM_M_0812_Obligations.root_of_assembly",
                "kind": "Lean abstract-child harness",
                "status": "provisional kernel-checked exact-root composition; assembly remains open",
            },
        ],
        "unverified_decomposition_plans": plans,
        "closure_boundary": {
            "accepted_closed_obligations": [],
            "checked_conditional_interfaces": ["M0812-T-MATCHING-ATTAIN", "M0812-T-COVER-FROM-MAX", "M0812-T-WEAK-DUALITY", "M0812-T-ASSEMBLE", "M0812-ROOT"],
            "root_closed": False,
            "authoritative_root_vector": {"H": "H1", "M": "M3", "R": "R2"},
            "audit_complete": False,
            "theorem_complete": False,
            "minimal_open_proof_cut_set": ["M0812-T-MATCHING-ATTAIN", "M0812-T-COVER-FROM-MAX", "M0812-T-WEAK-DUALITY"],
            "remaining_release_cut_set": ["M0812-T-MATCHING-ATTAIN", "M0812-T-COVER-FROM-MAX", "M0812-T-WEAK-DUALITY", "M0812-X-SOURCE", "M0812-X-PROVENANCE", "M0812-X-TRUST", "M0812-X-READABLE", "M0812-X-WORKFLOW"],
            "reason": "This phase freezes and checks architecture only. No proof child or exact external terminal body is accepted.",
        },
    }
    recipes = [
        {
            "recipe_id": f"VAL-{row['id']}",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0812/check_obligation_tree.py"],
            "env_allowlist": ["PATH", "HOME", "TMPDIR", "PYTHONDONTWRITEBYTECODE"],
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS and exact frozen counts"}],
            "covered_obligation_ids": [row["id"]],
            "covered_declarations": [row["formal"]] if row["formal"].startswith("Stage1Instances.") else [],
        }
        for row in SPECS
    ]
    validation = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "registry_denominator_sha256": denominator,
        "recipes": recipes,
    }
    readable = build_readable(registry, bundle)
    return registry, bundle, validation, readable


def build_readable(registry: dict, bundle: dict) -> str:
    node_by_id = {row["obligation_id"]: row for row in bundle["nodes"]}
    lines = [
        "# THM-M-0812 frozen obligation tree",
        "",
        "This version-1 registry describes the finite bipartite matching-cover proof architecture. It is not a proof receipt. All proof children remain open, no provider result is reused, and the authoritative root remains `H1/M3/R2`.",
        "",
        "The proof route fixes a maximum matching, follows alternating paths from unmatched left vertices, selects every unreached left vertex and every reached right vertex, proves this is a cover with exactly one selected endpoint per matching edge, and combines that construction with the injection from any matching into any cover.",
        "",
        "## Frozen boundary",
        "",
        f"- Registry: `{registry['registry_id']}`",
        f"- Denominator: `{registry['denominator_sha256']}`",
        f"- Obligations: `{len(registry['obligations'])}`",
        "- Accepted closed obligations: none",
        "- Minimal open proof cut: matching attainment, cover from a maximum matching, and weak duality",
        "- External candidates: ATLAS is placeholder-blocked; closed PR 33032 is unintegrated and incompatible with the pin",
        "",
        "## Nodes",
        "",
    ]
    for obligation in registry["obligations"]:
        oid = obligation["obligation_id"]
        node = node_by_id[oid]
        lines.extend(
            [
                f'<a id="{oid.lower()}"></a>',
                f"### {oid}",
                "",
                node["human_statement"],
                "",
                f"Formal target: `{node['formal_target']}`",
                "",
                f"Output: {node['output']}",
                "",
                f"Budget: `{node['step_budget']}` substantive steps. Status: `{node['human_debt']}/{node['machine_debt']}/{node['readability_debt']}`.",
                "",
                f"Method ledger: {node['semantic_step_ledger'][0]['inference']}",
                "",
                f"Source anchor: `{node['semantic_step_ledger'][0]['source_locator']}`",
                "",
                f"Boundary: {node['status_boundary']}",
                "",
            ]
        )
    return "\n".join(lines)


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry, bundle, validation, readable = build()
    outputs: dict[str, object] = {
        "obligation-registry.json": registry,
        "typed-graphs.json": bundle,
        "validation-specs.json": validation,
        "obligation-tree.md": readable,
    }
    if args.check:
        for name, expected in outputs.items():
            path = HERE / name
            actual = path.read_text(encoding="utf-8") if isinstance(expected, str) else json.loads(path.read_text(encoding="utf-8"))
            if actual != expected:
                raise SystemExit(f"stale generated artifact: {name}")
        print("build_obligation_artifacts: generated artifacts match")
        return
    for name, value in outputs.items():
        path = HERE / name
        if isinstance(value, str):
            path.write_text(value, encoding="utf-8")
        else:
            write_json(path, value)
    print("build_obligation_artifacts: wrote obligation registry, graphs, validation specs, and readable tree")


if __name__ == "__main__":
    main()
