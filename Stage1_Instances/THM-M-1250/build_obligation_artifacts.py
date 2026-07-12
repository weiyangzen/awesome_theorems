#!/usr/bin/env python3
"""Build the frozen THM-M-1250 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1250-OBLIGATION_TREE"
THEOREM = "THM-M-1250"

# id, kind, statement, formal target, output, risk, machine, human, budget, debt
SPECS = [
    ("M1250-ROOT", "root", "The exact SchwartzSpaceCharacterization.", "Stage1Instances.THM_M_1250.SchwartzSpaceCharacterization", "Canonical proposition", "critical", "required", "required", 10, "M3"),
    ("M1250-T-ASSEMBLE", "transport", "Compose both directions without changing the frozen binders.", "Stage1Instances.THM_M_1250.characterization_of_packages", "Exact root conditional on both packages", "high", "required", "required", 20, "M0-L"),
    ("M1250-F-PACKAGE", "branch", "Extract smoothness and every weighted derivative bound from a bundled SchwartzMap and transport along toFun equality.", "Stage1Instances.THM_M_1250.ForwardPackage", "Forward implication", "critical", "required", "required", 70, "M4"),
    ("M1250-F-SMOOTH", "bridge", "Project ContDiff Real top from SchwartzMap.smooth'.", "SchwartzMap.smooth'", "Smoothness before equality transport", "high", "required", "required", 20, "M1"),
    ("M1250-F-DECAY", "bridge", "Project the exact non-strict decay bound for every k and r.", "SchwartzMap.decay'", "Weighted derivative bounds before equality transport", "high", "required", "required", 20, "M1"),
    ("M1250-R-PACKAGE", "branch", "Construct a bundled SchwartzMap from the two classical conditions.", "Stage1Instances.THM_M_1250.ReversePackage", "Reverse implication", "critical", "required", "required", 70, "M4"),
    ("M1250-R-SMOOTH", "bridge", "Supply the smooth' structure field from the first conjunct.", "SchwartzMap.mk smooth' field", "Constructor smoothness field", "high", "required", "required", 20, "M1"),
    ("M1250-R-DECAY", "bridge", "Supply the decay' structure field with unchanged quantifier order.", "SchwartzMap.mk decay' field", "Constructor decay field", "high", "required", "required", 20, "M1"),
    ("M1250-R-CONSTRUCT", "construction", "Assemble SchwartzMap.mk and prove its coerced function is f.", "SchwartzMap.mk", "Existential bundled representative", "critical", "required", "required", 40, "M1"),
    ("M1250-S-EQUALITY", "transport", "Rewrite smoothness and iterated derivatives along bundled toFun equality.", "Eq substitution over ContDiff and iteratedFDeriv", "Both directions retain the exact f", "critical", "required", "required", 50, "M4"),
    ("M1250-S-BOUNDARY", "terminal", "Retain n = 0 and the zero function without extra premises.", "SchwartzSpaceCharacterization at n = 0", "Boundary-compatible general proof", "high", "required", "required", 30, "M4"),
    ("M1250-S-FOUNDATION", "certificate", "Audit axioms, imports, TCB, and absence of oracle computation.", "planned transitive trust report", "Accepted foundation profile", "critical", "required", "not_applicable", 40, "M4"),
    ("M1250-X-SOURCE", "terminal", "Map a primary definition/proof source to both directions and boundary cases.", "human source boundary", "Reviewed source crosswalk", "high", "not_applicable", "required", 50, "M4"),
    ("M1250-X-PROVENANCE", "certificate", "Classify every terminal proof body and imported bridge.", "planned provenance closure", "Content-addressed provenance", "critical", "informational", "not_applicable", 50, "M4"),
    ("M1250-X-TRUST", "certificate", "Record replay, executable, compiled-artifact, and dependency trust boundaries.", "planned release trust record", "Replayable trust boundary", "critical", "informational", "not_applicable", 50, "M4"),
]

def fp(oid, target):
    if oid == "M1250-ROOT":
        return "lean-expression-sha256:367a6b23168c88dcc5023a4d82bff17b496187a25303b4f81871a321750205f0"
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

obligations, nodes = [], []
for oid, kind, statement, target, output, risk, machine, human, budget, debt in SPECS:
    body = "local:Stage1_Instances/THM-M-1250/ObligationTree.lean#characterization_of_packages" if oid == "M1250-T-ASSEMBLE" else None
    exclusion = "human_source_boundary_only" if machine == "not_applicable" else ("release_overlay_no_proof_credit" if machine == "informational" else None)
    obligations.append({"obligation_id": oid, "statement_fingerprint": fp(oid, target), "kind": kind, "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": human, "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": body})
    nodes.append({
        "node_id": "THM-M-1250-" + oid[6:], "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": debt, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "source-pinpoint-pending" if human == "required" else "not-applicable",
        "provenance_id": body or "none", "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or experiment is credited", "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the frozen formal context and declared proof children.", "inference": statement, "output": output, "outgoing_use": "Only declared reciprocal composition or non-proof support edges."},
        "public_readable_target": "Stage1_Instances/THM-M-1250/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture or conditional interface only; no unlisted proof premise is supplied.",
        "task_ids": [ITEM, "S56-M-1250-PROOF"], "owned_sources": [], "owner": "THM-M-1250 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid == "M1250-T-ASSEMBLE" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid == "M1250-T-ASSEMBLE" else "open"}
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in FIELDS} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact statement and immutable anchor audit; direct structure-constructor/projection route selected before proof closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1250-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [], "status_observed_after_freeze": {"closed_obligations": ["M1250-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; both direction packages, source review, trust closure, and exact root remain open."
}

pairs = [("M1250-ROOT", "M1250-T-ASSEMBLE"), ("M1250-T-ASSEMBLE", "M1250-F-PACKAGE"), ("M1250-T-ASSEMBLE", "M1250-R-PACKAGE"), ("M1250-F-PACKAGE", "M1250-F-SMOOTH"), ("M1250-F-PACKAGE", "M1250-F-DECAY"), ("M1250-F-PACKAGE", "M1250-S-EQUALITY"), ("M1250-R-PACKAGE", "M1250-R-SMOOTH"), ("M1250-R-PACKAGE", "M1250-R-DECAY"), ("M1250-R-PACKAGE", "M1250-R-CONSTRUCT"), ("M1250-R-PACKAGE", "M1250-S-BOUNDARY")]
proof = []
for parent, child in pairs:
    req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
    proof.extend([{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}])
support = {
    "refinement": [("REF-ROOT-BOUNDARY", "M1250-ROOT", "logical_decomposition", "M1250-S-BOUNDARY")],
    "provenance": [("PROV-F", "M1250-X-PROVENANCE", "provenance_of", "M1250-F-PACKAGE"), ("SRC-F", "M1250-F-PACKAGE", "source_map", "M1250-X-SOURCE"), ("SRC-R", "M1250-R-PACKAGE", "source_map", "M1250-X-SOURCE")],
    "evidence": [], "trust": [("TRUST-FOUND", "M1250-ROOT", "trusts", "M1250-S-FOUNDATION"), ("TRUST-REPLAY", "M1250-ROOT", "trusts", "M1250-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1250-X-SOURCE", "documents", "M1250-ROOT"), ("DOC-BOUND", "M1250-S-BOUNDARY", "documents", "M1250-ROOT")],
    "workflow": [("FLOW-PROOF", "M1250-T-ASSEMBLE", "workflow_depends_on", "M1250-F-PACKAGE"), ("FLOW-PROV", "M1250-X-PROVENANCE", "workflow_depends_on", "M1250-T-ASSEMBLE")]
}
def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [{"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges]
    incoming, outgoing = {}, {}
    for edge in cooked:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"]); incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}
graphs = {"proof": graph(proof), **{name: graph(edges) for name, edges in support.items()}}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-1250-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "root_node_id": "M1250-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": graphs, "closure_boundary": {"closed_obligations": ["M1250-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1250-F-PACKAGE", "M1250-R-PACKAGE"], "composition_certificates": ["Stage1Instances.THM_M_1250.characterization_of_packages"], "reason": "Final composition is checked, but both mathematical directions remain explicit premises."}}
(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
