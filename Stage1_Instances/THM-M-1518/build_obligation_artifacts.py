#!/usr/bin/env python3
"""Deterministically build the THM-M-1518 frozen obligation artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1518-OBLIGATION_TREE"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


rows = [
    ("M1518-ROOT", "root", "critical", "Exact stationary-action-to-Euler-Lagrange target.", "Stage1Instances.THM_M_1518.StationaryActionEulerLagrangeTarget"),
    ("M1518-S-DEFINITIONS", "definition", "high", "Freeze action, variations, first variation, partial derivatives, and pointwise equation.", "Stage1Instances.THM_M_1518.{Action,AdmissibleVariation,FirstVariation,EulerLagrangeEquation}"),
    ("M1518-S-BOUNDARY", "terminal", "normal", "Retain a nondegenerate interval, fixed path endpoints, zero variation, n = 0, and an interior conclusion.", "Stage1Instances.THM_M_1518.{zero_admissibleVariation,endpoints_distinct}"),
    ("M1518-S-FOUNDATION", "certificate", "critical", "Fix Lean, mathlib, axiom, TCB, and no-oracle boundaries.", "planned transitive trust report"),
    ("M1518-N-DIFFERENTIATE", "bridge", "critical", "Differentiate the parameterized interval action under the integral sign.", "Stage1Instances.THM_M_1518.ObligationTree.FirstVariationFormula"),
    ("M1518-N-WEAK", "transport", "high", "Use stationarity and the first-variation identity to obtain the weak equation.", "Stage1Instances.THM_M_1518.ObligationTree.WeakEulerLagrange"),
    ("M1518-L-IBP", "core_lemma", "critical", "Integrate the velocity-variation term by parts and discharge both endpoint terms.", "planned fixed-endpoint interval integration-by-parts package"),
    ("M1518-L-FUNDAMENTAL", "core_lemma", "critical", "Upgrade vanishing pairings against endpoint-zero tests to the pointwise interior equation.", "planned fundamental lemma plus continuity upgrade package"),
    ("M1518-L-WEAK-POINTWISE", "bridge", "critical", "Compose integration by parts and the fundamental lemma from weak to pointwise form.", "Stage1Instances.THM_M_1518.ObligationTree.WeakToPointwise"),
    ("M1518-T-ASSEMBLE", "terminal", "high", "Compose the two open analytic packages into the exact root.", "Stage1Instances.THM_M_1518.ObligationTree.exactTarget_of_packages"),
    ("M1518-X-SOURCE", "terminal", "high", "Map every analytic step to pinpoint primary mathematical sources.", "non-machine source boundary"),
    ("M1518-X-PROVENANCE", "certificate", "critical", "Track local wrappers, terminal bodies, pins, imports, axioms, and replay evidence.", "planned provenance closure"),
]

checked = {"M1518-S-DEFINITIONS", "M1518-S-BOUNDARY", "M1518-N-WEAK", "M1518-T-ASSEMBLE"}
source_na = {"M1518-S-DEFINITIONS", "M1518-S-BOUNDARY", "M1518-S-FOUNDATION", "M1518-X-PROVENANCE"}
machine_special = {"M1518-X-SOURCE": "not_applicable", "M1518-X-PROVENANCE": "informational"}
root_fp = "lean-expression-sha256:4cc15786f13f4e4ad7594012ab3e96613f5bffbf572523e8282b41139fe6979f"
obligations, nodes = [], []
for oid, kind, risk, claim, target in rows:
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": root_fp if oid == "M1518-ROOT" else "planned:v1:sha256:" + digest([oid, claim, target]),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if machine == "not_applicable" else ("release_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1518/ObligationTree.lean#exactTarget_of_packages" if oid == "M1518-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-1518-" + oid.removeprefix("M1518-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": claim,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M4" if oid != "M1518-ROOT" else "M4"), "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "anchor-audit-provisional" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M1518-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/provisional", "tcb_profile": "lean-4.29.0+mathlib-8a178386/release-audit-pending",
        "computation_record": "none; no oracle closes this node", "step_budget": 40,
        "semantic_step_ledger": {"premises": "Only declared incoming proof requirements and the exact formal context.", "inference": claim, "output": claim, "outgoing_use": "Only declared typed edges consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1518/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional composition only; no open analytic package receives proof credit.",
        "task_ids": [ITEM, "S56-M-1518-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1518/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-1518 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-1518", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact statement and pre-status variational-calculus architecture; eligibility assigned without regard to closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1518-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1518-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [], "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M4"},
    "status_boundary": "Frozen denominator and conditional architecture only; the analytic packages and root remain open.",
}

def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal: result["reciprocal_edge_id"] = reciprocal
    return result

requires = {"M1518-ROOT": ["M1518-T-ASSEMBLE"], "M1518-T-ASSEMBLE": ["M1518-N-WEAK", "M1518-L-WEAK-POINTWISE"], "M1518-N-WEAK": ["M1518-N-DIFFERENTIATE"], "M1518-L-WEAK-POINTWISE": ["M1518-L-IBP", "M1518-L-FUNDAMENTAL"]}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]
graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1518-ROOT", "logical_decomposition", "M1518-S-DEFINITIONS"), edge("REF-ROOT-BOUND", "M1518-ROOT", "logical_decomposition", "M1518-S-BOUNDARY")],
    "provenance": [edge("SRC-DIFF", "M1518-N-DIFFERENTIATE", "source_map", "M1518-X-SOURCE"), edge("SRC-IBP", "M1518-L-IBP", "source_map", "M1518-X-SOURCE"), edge("SRC-FUND", "M1518-L-FUNDAMENTAL", "source_map", "M1518-X-SOURCE"), edge("PROV-ROOT", "M1518-X-PROVENANCE", "provenance_of", "M1518-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1518-ROOT", "trusts", "M1518-S-FOUNDATION"), edge("TRUST-PROV", "M1518-ROOT", "trusts", "M1518-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M1518-S-DEFINITIONS", "documents", "M1518-ROOT"), edge("DOC-SOURCE", "M1518-X-SOURCE", "documents", "M1518-L-WEAK-POINTWISE")],
    "workflow": [edge("FLOW-PROOF-TREE", "M1518-T-ASSEMBLE", "workflow_depends_on", "M1518-N-DIFFERENTIATE"), edge("FLOW-POINTWISE-IBP", "M1518-L-WEAK-POINTWISE", "workflow_depends_on", "M1518-L-IBP"), edge("FLOW-POINTWISE-FUND", "M1518-L-WEAK-POINTWISE", "workflow_depends_on", "M1518-L-FUNDAMENTAL"), edge("FLOW-PROV-ASSEMBLE", "M1518-X-PROVENANCE", "workflow_depends_on", "M1518-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1518", "registry_id": "THM-M-1518-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "root_node_id": "M1518-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": graphs, "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1518-N-DIFFERENTIATE", "M1518-L-IBP", "M1518-L-FUNDAMENTAL"], "composition_certificates": ["Stage1Instances.THM_M_1518.ObligationTree.exactTarget_of_packages"], "reason": "The checked final composition is conditional on open analytic packages."}}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1518", "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1518/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(ids)} obligations; denominator {denominator}")
