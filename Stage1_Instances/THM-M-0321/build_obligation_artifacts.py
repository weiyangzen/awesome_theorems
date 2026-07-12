#!/usr/bin/env python3
"""Build the frozen THM-M-0321 obligation registry and typed graphs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0321-OBLIGATION_TREE"
THEOREM = "THM-M-0321"
PREFIX = "M0321-"
STATEMENT_HASH = "7a9628fca04eb72d787efad1f852517f4385377b3ad16f3eba662ccea4bb86a5"


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


specs = [
    ("ROOT", "root", "The exact Markov-Kakutani common-fixed-point theorem for an arbitrary commuting family.", "Stage1Instances.THM_M_0321.MarkovKakutaniTarget", "The canonical theorem.", "critical", "split-required"),
    ("S-EXACT", "definition", "Freeze the exact ambient-map statement and every hypothesis.", "Stage1Instances.THM_M_0321.MarkovKakutaniTarget", "The exact root interface.", "critical", 8),
    ("S-DEFS", "definition", "Fix affinity on K, invariance, and common fixed point definitions.", "IsAffineOn; MapsTo; HasCommonFixedPoint", "Definitions with no hidden subtype affine structure.", "high", 8),
    ("S-CONTEXT", "definition", "Fix universes and the Hausdorff locally convex real topological-module context.", "Statement.lean ordered binders", "The context inherited by every mathematical child.", "high", 7),
    ("S-BOUNDARY", "branch", "Retain empty index types and all nonempty compact convex K, including singleton K.", "emptyFamily_boundary", "Boundary-complete scope.", "high", 6),
    ("S-TRANSPORT", "transport", "Transport only through the checked EqOn commutation equivalence.", "markovKakutaniTarget_iff_eqOnCommutationTarget", "A bidirectional exact statement transport.", "normal", 4),
    ("S-FOUNDATION", "certificate", "Audit classical choice, compactness, topology, and the complete kernel/dependency trust boundary.", "#print axioms of terminal declarations", "A versioned foundation and TCB report.", "critical", 10),
    ("N-FINITE", "reduction", "Reduce the mathematical core to common fixed points for every finite subfamily.", "FiniteFamilyStep", "Finite-subfamily nonemptiness.", "critical", "split-required"),
    ("N-INFINITE", "reduction", "Upgrade finite-subfamily fixed points to the full arbitrary family by compactness.", "CompactnessUpgrade", "A common fixed point for all indices.", "critical", "split-required"),
    ("B-FINITE-EMPTY", "branch", "Establish the finite-family base case from K.Nonempty.", "planned: Finset.empty fixed-point base", "The empty finite subfamily has a common fixed point.", "normal", 8),
    ("B-FINITE-INSERT", "branch", "For insert i s, restrict f i to the common fixed set of s and obtain a fixed point there.", "planned: Finset.induction insert branch", "A point fixed by every member of insert i s.", "critical", "split-required"),
    ("B-RECOMPOSE", "certificate", "Prove the empty and insert branches exhaust all finite subfamilies.", "planned: Finset.induction recomposition", "FiniteFamilyStep.", "high", 8),
    ("C-FIXSET", "construction", "Construct K intersected with the equalizer f i x = x for a selected map.", "planned: fixedSetWithin K (f i)", "The restricted fixed-point carrier.", "critical", "split-required"),
    ("C-RESTRICT", "construction", "Restrict every commuting map to each earlier common fixed set.", "planned: restricted ambient self-map", "A well-defined continuous affine self-map on the invariant carrier.", "critical", "split-required"),
    ("C-AVERAGE", "construction", "Construct Cesaro averages for one affine self-map and keep them inside K.", "planned: (n+1)^-1 • ∑ k in range (n+1), f^[k] x", "A net/sequence of approximate fixed points in K.", "critical", "split-required"),
    ("C-FIP", "construction", "Construct the closed fixed subsets of K and their finite intersections.", "planned: {x ∈ K | f i x = x}", "A closed family with the finite-intersection property.", "critical", "split-required"),
    ("L-SINGLE", "core_lemma", "A continuous affine self-map of nonempty compact convex K has a fixed point.", "planned: singleMap_fixedPoint", "One-map fixed-point existence.", "critical", "split-required"),
    ("L-AVERAGE-IN-K", "core_lemma", "Every Cesaro average lies in K by convexity and invariance.", "planned: cesaroAverage_mem", "Membership of all averages in K.", "high", 20),
    ("L-AVERAGE-DEFECT", "core_lemma", "The displacement of Cesaro averages tends to zero by telescoping and boundedness.", "planned: tendsto_cesaro_displacement_zero", "Approximate fixed-point convergence.", "critical", "split-required"),
    ("L-CLUSTER", "core_lemma", "Compactness supplies a cluster point and continuity makes it a genuine fixed point.", "planned: clusterPoint_isFixedPt", "A fixed point of the selected map in K.", "critical", "split-required"),
    ("L-FIXSET-COMPACT", "core_lemma", "The fixed-point subset inside K is compact.", "planned: isCompact_fixedSetWithin", "Compactness of the induction carrier.", "high", 15),
    ("L-FIXSET-CONVEX", "core_lemma", "Affinity makes the fixed-point subset inside K convex.", "planned: convex_fixedSetWithin", "Convexity of the induction carrier.", "high", 15),
    ("L-COMMUTE-INVARIANT", "core_lemma", "Pairwise commutation makes each remaining map preserve prior common fixed points.", "planned: MapsTo on common fixed set", "Invariance required for restriction.", "critical", 18),
    ("L-FIP-COMPACT", "core_lemma", "A compact space's closed subsets with the finite-intersection property have nonempty total intersection.", "planned: IsCompact nonempty_iInter_of_directed", "A point in every fixed subset.", "critical", "split-required"),
    ("X-SOURCE", "terminal", "Pinpoint each proof package to primary Markov/Kakutani theorem text and errata.", "source-statement-crosswalk.md; primary pages pending", "Human-source boundary.", "critical", 20),
    ("X-LEAN", "terminal", "Resolve every imported Lean theorem and terminal proof body used by proof execution.", "anchor-audit.json; exact candidate absent", "Formal provenance boundary.", "critical", 15),
    ("X-TCB", "terminal", "Record transitive declarations, axioms, toolchain, dependencies, and replay boundary.", "Lean 4.29.0; mathlib 8a178386; closure pending", "Trusted-computing-base boundary.", "critical", 15),
    ("T-FINITE", "terminal", "Assemble the finite induction into FiniteFamilyStep.", "FiniteFamilyStep", "The first premise of root_compose.", "critical", 12),
    ("T-UPGRADE", "terminal", "Assemble closed fixed sets and compact FIP into CompactnessUpgrade.", "CompactnessUpgrade", "The second premise of root_compose.", "critical", 12),
    ("T-ASSEMBLE", "terminal", "Consume both exact child propositions and return the canonical target.", "Stage1Instances.THM_M_0321.ObligationTree.root_compose", "MarkovKakutaniTarget.", "critical", 6),
]

ids = [PREFIX + row[0] for row in specs]
math_ids = [oid for oid in ids if not oid.startswith(PREFIX + "X-")]
source_required = [oid for oid in ids if oid not in {PREFIX + "S-DEFS", PREFIX + "S-CONTEXT", PREFIX + "S-BOUNDARY", PREFIX + "S-TRANSPORT", PREFIX + "S-FOUNDATION", PREFIX + "X-LEAN", PREFIX + "X-TCB"}]

obligations = []
nodes = []
for suffix, kind, claim, formal, output, risk, budget in specs:
    oid = PREFIX + suffix
    planned = "lean-expression-sha256:" + STATEMENT_HASH if suffix in {"ROOT", "S-EXACT"} else "planned:v1:sha256:" + digest({"id": oid, "claim": claim, "formal": formal, "output": output})
    overlay = suffix.startswith("X-")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": planned, "kind": kind,
        "root_relevant": not overlay, "machine_eligibility": "informational" if overlay else "required",
        "human_source_eligibility": "required" if oid in source_required else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "typed_source_provenance_or_trust_overlay" if overlay else None,
        "terminal_proof_body_id": "repo:Stage1Instances.THM_M_0321.ObligationTree.root_compose" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": THEOREM + "-" + suffix, "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": formal, "output": output,
        "human_debt": "H2", "machine_debt": "M3", "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "source-statement-crosswalk.md" if oid in source_required else "not-applicable",
        "provenance_id": "repo:root_compose" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-dependent-type-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children listed in proof/refinement graph"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": f"Stage1_Instances/THM-M-0321/obligation-tree.md#{suffix.lower()}",
        "validation_spec_id": "VAL-" + oid + "-PENDING",
        "status_boundary": "Architecture only; no proof, H0/R0 credit, accepted state, or theorem completion is claimed.",
        "task_ids": [ITEM, "S56-M-0321-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0321/obligation-registry.json", "Stage1_Instances/THM-M-0321/typed-graphs.json"],
        "owner": "THM-M-0321 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "typed edges", "source map", "toolchain", "mathlib revision"], "revocation_state": "not-accepted"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact statement and negative immutable-anchor audit freeze a two-stage finite-family/compact-FIP proof architecture before proof closure is observed.",
    "frozen_against_statement_sha256": STATEMENT_HASH,
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": PREFIX + "ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids, "required_machine": math_ids, "required_human_source": source_required,
        "required_readable": ids, "informational_overlays": [PREFIX + x for x in ("X-SOURCE", "X-LEAN", "X-TCB")],
    },
    "delta_policy": "Any split, merge, target, eligibility, exclusion, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations,
}

proof_pairs = [
    ("ROOT", "T-ASSEMBLE", "composes"), ("T-ASSEMBLE", "T-FINITE", "proof_requires"), ("T-ASSEMBLE", "T-UPGRADE", "proof_requires"),
    ("T-FINITE", "N-FINITE", "composes"), ("N-FINITE", "B-RECOMPOSE", "proof_requires"),
    ("B-RECOMPOSE", "B-FINITE-EMPTY", "proof_requires"), ("B-RECOMPOSE", "B-FINITE-INSERT", "proof_requires"),
    ("B-FINITE-INSERT", "C-RESTRICT", "proof_requires"), ("B-FINITE-INSERT", "L-SINGLE", "proof_requires"),
    ("C-RESTRICT", "C-FIXSET", "proof_requires"), ("C-RESTRICT", "L-FIXSET-COMPACT", "proof_requires"),
    ("C-RESTRICT", "L-FIXSET-CONVEX", "proof_requires"), ("C-RESTRICT", "L-COMMUTE-INVARIANT", "proof_requires"),
    ("L-SINGLE", "C-AVERAGE", "proof_requires"), ("L-SINGLE", "L-AVERAGE-IN-K", "proof_requires"),
    ("L-SINGLE", "L-AVERAGE-DEFECT", "proof_requires"), ("L-SINGLE", "L-CLUSTER", "proof_requires"),
    ("T-UPGRADE", "N-INFINITE", "composes"), ("N-INFINITE", "C-FIP", "proof_requires"),
    ("C-FIP", "L-FIP-COMPACT", "proof_requires"),
]
refine_pairs = [("ROOT", x, "logical_decomposition") for x in ("S-EXACT", "S-DEFS", "S-CONTEXT", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION")]

def make_graph(name: str, pairs: list[tuple[str, str, str]]) -> dict:
    edges, out, incoming = [], {}, {}
    for index, (source, target, kind) in enumerate(pairs, 1):
        edge_id = f"{name.upper()}-{index:03d}"
        edge = {"edge_id": edge_id, "from": PREFIX + source, "type": kind, "to": PREFIX + target}
        edges.append(edge); out.setdefault(edge["from"], []).append(edge_id); incoming.setdefault(edge["to"], []).append(edge_id)
    return {"edges": edges, "out": out, "in": incoming}

graph_pairs = {
    "proof": proof_pairs, "refinement": refine_pairs,
    "provenance": [("ROOT", "X-LEAN", "provenance_of")],
    "evidence": [("T-ASSEMBLE", "X-LEAN", "evidence_for")],
    "trust": [("ROOT", "X-TCB", "trusts"), ("S-FOUNDATION", "X-TCB", "trusts")],
    "documentation": [("ROOT", "X-SOURCE", "documents")],
    "workflow": [("X-SOURCE", "T-FINITE", "workflow_depends_on"), ("X-LEAN", "T-ASSEMBLE", "workflow_depends_on")],
}
graphs = {name: make_graph(name, pairs) for name, pairs in graph_pairs.items()}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_machine_debt": "M3",
        "remaining_root_cut_set": [PREFIX + "L-SINGLE", PREFIX + "L-FIP-COMPACT"],
        "composition_certificates_checked": [PREFIX + "T-ASSEMBLE"], "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n")

lines = ["# Frozen obligation architecture", "", "This is an architecture freeze, not a proof or closure report. Every node remains open.", "", "## Proof flow", "", "The checked root composition consumes `FiniteFamilyStep` and `CompactnessUpgrade`. The former is expanded through finite induction and the one-map fixed-point engine; the latter is expanded through closed fixed sets and compact finite-intersection reasoning.", ""]
for suffix, _, claim, formal, output, _, budget in specs:
    lines += [f"## {suffix}", "", f"**Claim:** {claim}", "", f"**Formal target:** `{formal}`", "", f"**Output:** {output}", "", f"**Step budget:** `{budget}`. **Status:** `[H2, M3, R4]`; architecture only, with proof/source/readability acceptance open.", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"wrote {len(obligations)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
