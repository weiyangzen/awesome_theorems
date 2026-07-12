#!/usr/bin/env python3
"""Build the frozen THM-M-0319 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0319-OBLIGATION_TREE"
THEOREM = "THM-M-0319"
ROOT_FP = "lean-expression-sha256:2e4dc02230de7a1c08fdf4a19ef0ec1da107297972dee0e85d893bdb33d6a514"


def planned(text):
    return "planned:v1:sha256:" + hashlib.sha256(text.encode()).hexdigest()


rows = [
    ("M0319-ROOT", "root", "The exact frozen ambient-map Brouwer fixed-point proposition.", "critical", "required", "required", "required", ROOT_FP),
    ("M0319-S-DEFINITIONS", "definition", "Freeze EuclideanSpace, ContinuousOn, MapsTo, compactness, convexity, and literal equality conventions.", "high", "required", "not_applicable", "required", ROOT_FP),
    ("M0319-S-BOUNDARY", "terminal", "Close dimension zero and preserve nonempty lower-dimensional and singleton cases.", "high", "required", "required", "required", None),
    ("M0319-S-FOUNDATION", "certificate", "Audit classical choice, transitive imports, axioms, TCB, and the no-oracle boundary.", "critical", "required", "not_applicable", "required", None),
    ("M0319-T-SUBTYPE", "transport", "Convert ContinuousOn plus MapsTo into a continuous subtype self-map and transport its fixed point to ambient equality.", "critical", "required", "required", "required", None),
    ("M0319-N-FINITE-DIM", "normalization", "Instantiate the general finite-dimensional real normed-space theorem at EuclideanSpace Real (Fin n).", "high", "required", "required", "required", None),
    ("M0319-R-CONVEX-CUBE", "reduction", "Construct and verify the compact-convex-set reduction used by the audited external body via its cube homeomorphism route.", "critical", "required", "required", "required", None),
    ("M0319-L-UNIT-CUBE", "core_lemma", "Prove the fixed-point theorem on the finite-dimensional unit cube, including all face and dimension boundaries.", "critical", "required", "required", "required", None),
    ("M0319-T-EXTERNAL", "terminal", "Assemble the cube reduction and unit-cube theorem into the exact audited ExternalBrouwerBody interface.", "critical", "required", "required", "required", None),
    ("M0319-X-INTEGRATION", "certificate", "Pin or vendor the audited Lean 4 body and produce an exact local elaboration and kernel receipt.", "critical", "required", "not_applicable", "required", None),
    ("M0319-X-SOURCE", "terminal", "Pin primary human sources and map every mathematical leaf and boundary to exact theorem pages and assumptions.", "high", "not_applicable", "required", "required", None),
    ("M0319-X-PROVENANCE", "certificate", "Record terminal bodies, revisions, imports, declaration dependencies, axioms, and replay provenance.", "critical", "informational", "not_applicable", "required", None),
]

closed = {"M0319-S-DEFINITIONS", "M0319-S-BOUNDARY", "M0319-T-SUBTYPE", "M0319-N-FINITE-DIM"}
obligations = []
for oid, kind, statement, risk, machine, human, readable, fingerprint in rows:
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint or planned(statement),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": {"M0319-X-SOURCE": "human_source_boundary_only", "M0319-X-PROVENANCE": "release_provenance_overlay_no_proof_credit"}.get(oid),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0319/ObligationTree.lean#root_of_external_body" if oid == "M0319-T-SUBTYPE" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated target and completed immutable anchor audit; the audited candidate's compact-convex-to-cube route was decomposed before observing downstream closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0319-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": ["M0319-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(closed), "root_machine_debt": "M3"},
    "status_boundary": "Architecture and checked conditional transport only; the external terminal body is not in the pinned closure, so no Brouwer proof or theorem completion is claimed.",
}

nodes = []
for oid, kind, statement, _risk, _machine, human, _readable, _fp in rows:
    is_closed = oid in closed
    formal = {
        "M0319-ROOT": "Stage1Instances.THM_M_0319.BrouwerFixedPointTarget",
        "M0319-S-DEFINITIONS": "Stage1Instances.THM_M_0319.{RealEuclideanSpace,BrouwerFixedPointTarget}",
        "M0319-S-BOUNDARY": "Stage1Instances.THM_M_0319.ObligationTree.zero_dimensional_boundary",
        "M0319-T-SUBTYPE": "Stage1Instances.THM_M_0319.ObligationTree.root_of_external_body",
        "M0319-N-FINITE-DIM": "typeclass synthesis for EuclideanSpace Real (Fin n)",
        "M0319-T-EXTERNAL": "FixedPointTheorems.brouwer.brouwer_fixed_point at audited immutable revision",
    }.get(oid, "planned exact Lean signature: " + statement)
    nodes.append({
        "node_id": "THM-M-0319-" + oid.removeprefix("M0319-"), "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": formal,
        "output": "The exact claim described by this obligation, usable only along declared typed edges.",
        "human_debt": "H1" if human == "required" else "H3",
        "machine_debt": "M0-L" if is_closed else ("M3" if oid in {"M0319-ROOT", "M0319-T-EXTERNAL", "M0319-X-INTEGRATION"} else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if human == "required" else "not-applicable",
        "provenance_id": "M0319-C02" if oid == "M0319-T-EXTERNAL" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386; external-4.21-rc3 closure absent",
        "computation_record": "none; no oracle or external computation may close this node", "step_budget": 40,
        "semantic_step_ledger": {"premises": "Only exact proof_requires children and the frozen formal context.", "inference": statement, "output": "The stated node output.", "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0319/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no undeclared premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0319-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0319/ObligationTree.lean"] if oid in {"M0319-S-BOUNDARY", "M0319-T-SUBTYPE"} else [],
        "owner": "THM-M-0319 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if is_closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if is_closed else "open"},
    })

graphs = {name: {"edges": [], "out": {oid: [] for oid in ids}, "in": {oid: [] for oid in ids}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}


def edge(graph, eid, typ, src, dst, reciprocal=None):
    value = {"edge_id": eid, "type": typ, "from": src, "to": dst}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(value)
    graphs[graph]["out"][src].append(eid)
    graphs[graph]["in"][dst].append(eid)


proof_pairs = [
    ("ROOT", "M0319-ROOT", "M0319-T-SUBTYPE"),
    ("SUBTYPE-EXT", "M0319-T-SUBTYPE", "M0319-T-EXTERNAL"),
    ("SUBTYPE-FD", "M0319-T-SUBTYPE", "M0319-N-FINITE-DIM"),
    ("EXT-REDUCE", "M0319-T-EXTERNAL", "M0319-R-CONVEX-CUBE"),
    ("EXT-CUBE", "M0319-T-EXTERNAL", "M0319-L-UNIT-CUBE"),
]
for label, parent, child in proof_pairs:
    req, comp = "P-" + label + "-REQ", "P-" + label + "-COMP"
    edge("proof", req, "proof_requires", parent, child, comp)
    edge("proof", comp, "composes", child, parent, req)
for oid in ("M0319-S-DEFINITIONS", "M0319-S-BOUNDARY"):
    edge("refinement", "R-" + oid, "logical_decomposition", "M0319-ROOT", oid)
edge("provenance", "PV-EXTERNAL", "provenance_of", "M0319-X-PROVENANCE", "M0319-T-EXTERNAL")
edge("evidence", "EV-INTEGRATION", "evidence_for", "M0319-X-INTEGRATION", "M0319-T-EXTERNAL")
edge("trust", "TR-ROOT", "trusts", "M0319-ROOT", "M0319-S-FOUNDATION")
for oid in ids:
    if oid != "M0319-X-SOURCE":
        edge("documentation", "D-" + oid, "documents", "M0319-X-SOURCE", oid)
workflow = ["M0319-S-DEFINITIONS", "M0319-R-CONVEX-CUBE", "M0319-L-UNIT-CUBE", "M0319-T-EXTERNAL", "M0319-T-SUBTYPE", "M0319-ROOT"]
for index, (before, after) in enumerate(zip(workflow, workflow[1:]), 1):
    edge("workflow", f"W-{index:02d}", "workflow_depends_on", after, before)

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0319-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M0319-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "minimal_open_root_cut": ["M0319-T-EXTERNAL"], "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(digest)
