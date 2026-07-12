#!/usr/bin/env python3
"""Build the frozen rev-5.6 obligation architecture for THM-M-0527."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0527-OBLIGATION_TREE"
THEOREM = "THM-M-0527"
ROOT = "M0527-ROOT"


def canonical_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# (id, kind, human statement, formal target, output, children, step budget)
SPECS = [
    (ROOT, "root", "The frozen pointed connected-cover assignment is surjective and has pointed-isomorphism fibers.", "Stage1Instances.THM_M_0527.CoveringSpaceClassificationTarget", "The exact conjunction in the frozen target.", ["M0527-EX", "M0527-FIB"], None),
    ("M0527-EX", "construction", "Every subgroup is induced by a pointed connected covering.", "Function.Surjective (PointedConnectedCover.inducedSubgroup (x₀ := x₀))", "A cover P with inducedSubgroup P = H.", ["M0527-EX-PATH", "M0527-EX-REL", "M0527-EX-TOTAL", "M0527-EX-TOPO", "M0527-EX-COVER", "M0527-EX-CONN", "M0527-EX-BASE", "M0527-EX-RANGE", "M0527-EX-PACK"], None),
    ("M0527-EX-PATH", "construction", "Form based paths from x0 with arbitrary endpoints and concatenate them coherently.", "Planned Lean signature: based path total space over X", "Raw based-path representatives and endpoint projection.", [], 18),
    ("M0527-EX-REL", "quotient", "Identify two based paths precisely when their endpoint agrees and their loop difference represents H.", "Planned Lean signature: Setoid on based-path representatives parameterized by H", "An equivalence relation compatible with endpoints.", ["M0527-EX-REL-REFL", "M0527-EX-REL-SYM", "M0527-EX-REL-TRANS", "M0527-EX-REL-END"], None),
    ("M0527-EX-REL-REFL", "lemma", "The H-path relation is reflexive.", "Planned Lean proposition: Reflexive (pathRel H)", "Reflexivity certificate.", [], 12),
    ("M0527-EX-REL-SYM", "lemma", "The H-path relation is symmetric using subgroup inversion.", "Planned Lean proposition: Symmetric (pathRel H)", "Symmetry certificate.", [], 16),
    ("M0527-EX-REL-TRANS", "lemma", "The H-path relation is transitive using subgroup multiplication.", "Planned Lean proposition: Transitive (pathRel H)", "Transitivity certificate.", [], 22),
    ("M0527-EX-REL-END", "invariant", "Equivalent paths have the same endpoint.", "Planned Lean proposition: pathRel H a b -> endpoint a = endpoint b", "Well-defined endpoint invariant.", [], 10),
    ("M0527-EX-TOTAL", "quotient", "Take the quotient by the H-path relation and descend endpoint projection.", "Planned Lean signature: E_H and p_H : E_H -> X", "Candidate total space and projection.", [], 20),
    ("M0527-EX-TOPO", "topology", "Give E_H the evenly-covered neighborhood topology induced by local path lifting.", "Planned Lean signature: TopologicalSpace E_H", "Topology with sheet neighborhoods.", ["M0527-EX-TOPO-NEIGH", "M0527-EX-TOPO-WELL", "M0527-EX-TOPO-BASIS"], None),
    ("M0527-EX-TOPO-NEIGH", "topology", "Choose sufficiently small path-connected neighborhoods whose ambient loop maps are trivial.", "SemilocallySimplyConnected X and LocPathConnectedSpace X yield admissible neighborhoods", "Admissible local neighborhoods at every endpoint.", [], 35),
    ("M0527-EX-TOPO-WELL", "invariant", "Changing a path representative does not change its local sheet chart.", "Planned Lean proposition: localChart respects pathRel H", "Representative independence of charts.", [], 40),
    ("M0527-EX-TOPO-BASIS", "topology", "The local sheet sets form a topology basis and endpoint projection is continuous.", "Planned Lean signature: TopologicalSpace E_H and Continuous p_H", "A topology and continuous projection.", [], 42),
    ("M0527-EX-COVER", "covering", "Each admissible neighborhood is evenly covered by disjoint local sheets.", "IsCoveringMap p_H", "Covering-map certificate.", ["M0527-EX-COVER-FIB", "M0527-EX-COVER-SHEET", "M0527-EX-COVER-HOME", "M0527-EX-COVER-DISJ"], None),
    ("M0527-EX-COVER-FIB", "covering", "Index the fiber and sheets over an admissible neighborhood.", "Planned Lean signature: fiber index for p_H over U", "Sheet index family.", [], 25),
    ("M0527-EX-COVER-SHEET", "covering", "Prove the preimage is the union of the indexed sheets.", "Planned Lean proposition: p_H ⁻¹' U = union sheets", "Preimage decomposition.", [], 34),
    ("M0527-EX-COVER-HOME", "covering", "Restriction of p_H to every sheet is a homeomorphism onto U.", "Planned Lean signature: sheet i ≃ₜ U", "Local homeomorphisms.", [], 48),
    ("M0527-EX-COVER-DISJ", "covering", "Distinct indexed sheets are disjoint.", "Planned Lean proposition: Pairwise (Disjoint on sheets)", "Sheet disjointness.", [], 32),
    ("M0527-EX-CONN", "connectivity", "Every quotient path class is joined to the constant-path class.", "PathConnectedSpace E_H", "Path-connected total-space instance.", [], 38),
    ("M0527-EX-BASE", "construction", "Choose the constant path class over x0 as the covering basepoint.", "Planned Lean terms: e₀_H : E_H and p_H e₀_H = x₀", "Pointed-cover basepoint equation.", [], 12),
    ("M0527-EX-RANGE", "fundamental_group", "The induced fundamental-group range of the constructed cover is exactly H.", "PointedConnectedCover.inducedSubgroup P_H = H", "Exact subgroup equality.", ["M0527-EX-RANGE-LE", "M0527-EX-RANGE-GE"], None),
    ("M0527-EX-RANGE-LE", "fundamental_group", "A lifted loop at e0 has ambient class in H.", "PointedConnectedCover.inducedSubgroup P_H ≤ H", "Forward subgroup inclusion.", [], 45),
    ("M0527-EX-RANGE-GE", "fundamental_group", "Every class in H lifts to a loop at e0.", "H ≤ PointedConnectedCover.inducedSubgroup P_H", "Reverse subgroup inclusion.", [], 45),
    ("M0527-EX-PACK", "composition", "Bundle the constructed topology, cover, connectivity, and basepoint and return its range equality.", "Planned Lean witness for Function.Surjective inducedSubgroup", "Surjectivity witness consuming all construction invariants.", [], 20),
    ("M0527-FIB", "classification", "Two pointed connected covers have equal induced subgroups iff they are pointed-isomorphic.", "∀ P Q, inducedSubgroup P = inducedSubgroup Q ↔ PointedConnectedCover.Isomorphic P Q", "The exact fiber criterion.", ["M0527-FIB-FWD", "M0527-FIB-REV"], None),
    ("M0527-FIB-FWD", "classification", "Equal induced subgroups produce a pointed covering isomorphism.", "inducedSubgroup P = inducedSubgroup Q -> PointedConnectedCover.Isomorphic P Q", "Forward implication.", ["M0527-FIB-LIFT-PQ", "M0527-FIB-LIFT-QP", "M0527-FIB-INVERSE", "M0527-FIB-HOME", "M0527-FIB-OVER"], None),
    ("M0527-FIB-LIFT-PQ", "lifting", "Lift P.p through Q from the selected basepoint using the subgroup-range criterion.", "∃! f : C(P.E, Q.E), f P.e₀ = Q.e₀ ∧ Q.p ∘ f = P.p", "Unique pointed comparison map P to Q.", [], 45),
    ("M0527-FIB-LIFT-QP", "lifting", "Lift Q.p through P from the selected basepoint using the reverse range inclusion.", "∃! g : C(Q.E, P.E), g Q.e₀ = P.e₀ ∧ P.p ∘ g = Q.p", "Unique pointed comparison map Q to P.", [], 45),
    ("M0527-FIB-INVERSE", "uniqueness", "Uniqueness of pointed lifts makes the two comparison maps mutual inverses.", "g ∘ f = id ∧ f ∘ g = id", "Mutual-inverse equations.", [], 30),
    ("M0527-FIB-HOME", "topology", "Continuous mutual inverses assemble to a homeomorphism of total spaces.", "P.E ≃ₜ Q.E", "Total-space homeomorphism.", [], 18),
    ("M0527-FIB-OVER", "composition", "The homeomorphism preserves basepoints and commutes with projections.", "PointedConnectedCover.Isomorphic P Q", "Pointed covering isomorphism witness.", [], 16),
    ("M0527-FIB-REV", "naturality", "A pointed covering isomorphism induces equality of the two fundamental-group ranges.", "PointedConnectedCover.Isomorphic P Q -> inducedSubgroup P = inducedSubgroup Q", "Reverse implication.", ["M0527-FIB-REV-MAP", "M0527-FIB-REV-RANGE"], None),
    ("M0527-FIB-REV-MAP", "naturality", "Projection commutation identifies the two induced homomorphisms after the basepoint-preserving homeomorphism.", "Planned Lean equality of FundamentalGroup.mapOfEq composites", "Induced-map compatibility.", [], 38),
    ("M0527-FIB-REV-RANGE", "group_theory", "Precomposition by the fundamental-group isomorphism preserves the homomorphism range.", "inducedSubgroup P = inducedSubgroup Q", "Equality of subgroup ranges.", [], 24),
]


def edge(graph, source, relation, target):
    return {"edge_id": f"{graph.upper()}-{source}-{target}", "from": source, "type": relation, "to": target}


ids = [row[0] for row in SPECS]
assert len(ids) == len(set(ids))
spec_by_id = {row[0]: row for row in SPECS}
assert all(child in spec_by_id for row in SPECS for child in row[5])

obligations = []
nodes = []
for oid, kind, human, formal, output, children, budget in SPECS:
    fingerprint = ("lean-expression-sha256:4c7a7d4c54edb4a2d46091dda31f20a26664f005b20495012be1425dd625f55d" if oid == ROOT else "planned:v1:sha256:" + canonical_hash({"id": oid, "human": human, "formal": formal, "output": output}))
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": "required",
        "human_source_eligibility": "required", "readable_eligibility": "required",
        "risk_class": "critical" if oid in {ROOT, "M0527-EX-COVER", "M0527-EX-RANGE", "M0527-FIB"} else ("high" if children else "normal"),
        "exclusion_reason": None, "terminal_proof_body_id": None,
    })
    ledger = (f"Inputs: the frozen hypotheses and outputs of {', '.join(children)}. " if children else "Inputs: the frozen hypotheses and definitions named in this leaf. ") + f"Deliver exactly: {output} No stronger or alternate theorem is credited."
    nodes.append({
        "node_id": f"THM-M-0527-{oid.removeprefix('M0527-')}", "obligation_id": oid,
        "kind": kind, "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H1", "machine_debt": "M3" if oid == ROOT else "M4", "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "source_statement_crosswalk.md",
        "provenance_id": "none", "foundation_profile": "lean4-dependent-type-theory/classical-and-quotient-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-transitive-closure-pending", "computation_record": "none",
        "step_budget": "split-required" if children else budget, "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-0527/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}-PENDING", "status_boundary": "Architecture only; no proof body or closure is credited.",
        "task_ids": [ITEM, "S56-M-0527-PROOF"], "owned_sources": [],
        "owner": "THM-M-0527 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; invalidate_on=statement,registry,toolchain,source-map-change; revocation=none",
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "freeze_basis": "Exact elaborated statement plus the audited mathlib lifting anchors; no candidate proof status was imported.",
    "root_obligation_id": ROOT,
    "frozen_denominators": {"inventory": ids, "required_machine": ids, "required_human_source": ids, "required_readable": ids, "informational_overlays": []},
    "denominator_sha256": canonical_hash(projection),
    "delta_policy": "Any split, merge, eligibility change, or exclusion requires registry_version 2 and an append-only old/new ID delta.",
    "obligations": obligations,
}

proof_edges = [edge("proof", row[0], "proof_requires", child) for row in SPECS for child in row[5]]
graph_edges = {
    "proof": proof_edges,
    "refinement": [edge("refinement", ROOT, "statement_refines", "M0527-EX"), edge("refinement", ROOT, "statement_refines", "M0527-FIB")],
    "provenance": [edge("provenance", "M0527-FIB-LIFT-PQ", "candidate_anchor", "M0527-FIB-LIFT-QP")],
    "evidence": [edge("evidence", ROOT, "evidence_pending_on", "M0527-EX-COVER")],
    "trust": [edge("trust", ROOT, "trust_audit_requires", "M0527-EX-TOPO")],
    "documentation": [edge("documentation", ROOT, "documented_with", "M0527-FIB")],
    "workflow": [edge("workflow", "M0527-EX", "workflow_precedes", "M0527-FIB")],
}
graphs = {}
for name, edges in graph_edges.items():
    outgoing, incoming = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_machine_debt": "M3", "remaining_root_cut_set": ["M0527-EX-COVER", "M0527-EX-RANGE", "M0527-FIB"], "composition_certificates_checked": [], "theorem_complete": False},
}

registry_path = HERE / "obligation-registry.json"
graphs_path = HERE / "typed-graphs.json"
registry_path.write_text(json.dumps(registry, indent=2) + "\n")
graphs_path.write_text(json.dumps(bundle, indent=2) + "\n")
receipt = {
    "schema_version": "stage1-node-receipt/1.0", "receipt_id": "S56-M-0527-OBLIGATION_TREE-selftest-v1",
    "item_id": ITEM, "theorem_id": THEOREM, "state": "self_tested_pending_master_acceptance",
    "inputs": {"statement_sha256": file_hash(HERE / "Statement.lean"), "anchor_audit_sha256": file_hash(HERE / "anchor-audit.json")},
    "outputs": {"obligation_registry_sha256": file_hash(registry_path), "typed_graphs_sha256": file_hash(graphs_path), "denominator_sha256": registry["denominator_sha256"]},
    "counts": {"obligations": len(ids), "typed_edges": sum(len(rows) for rows in graph_edges.values())},
    "theorem_complete": False, "master_acceptance_required": True,
}
(HERE / "obligation-tree-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(f"wrote {len(ids)} obligations and {receipt['counts']['typed_edges']} typed edges")
