#!/usr/bin/env python3
"""Build the frozen THM-M-1537 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1537-OBLIGATION_TREE"
THEOREM = "THM-M-1537"

rows = [
    ("M1537-ROOT", "root", "critical", "Prove the exact dimensionful Bekenstein-Hawking area law for every frozen model.", "Stage1Instances.THM_M_1537.BekensteinHawkingAreaLaw", "The canonical proposition.", "required", "required", 30),
    ("M1537-S-DEFINITIONS", "definition", "high", "Freeze the black-hole record, entropyFromArea expression, and exact root binders.", "Stage1Instances.THM_M_1537.{SemiclassicalBlackHole,entropyFromArea}", "The elaborated statement interface.", "required", "not_applicable", 20),
    ("M1537-S-REGIME", "boundary", "critical", "Preserve stationarity, Einstein-gravity, semiclassical, area, and positivity premises.", "the nine premises of BekensteinHawkingAreaLaw", "The exact applicability boundary.", "required", "required", 30),
    ("M1537-B-PHYSICS", "bridge", "critical", "Derive entropy equals k_B*c^3*A/(4*G*hbar) from a formal black-hole model rather than assuming the law.", "Stage1Instances.THM_M_1537.AreaLawBridge", "The pointwise area-law equality under every frozen premise.", "required", "required", 100),
    ("M1537-L-COUNTERMODEL", "countermodel", "critical", "Show the current record admits all regime premises while entropy is independent of area.", "Stage1Instances.THM_M_1537.not_bekensteinHawkingAreaLaw", "A proof of not BekensteinHawkingAreaLaw for the frozen model.", "required", "not_applicable", 40),
    ("M1537-T-ASSEMBLE", "transport", "high", "Transport the exact area-law bridge to the public root without changing binders.", "Stage1Instances.THM_M_1537.areaLaw_of_bridge", "The root conditional on AreaLawBridge.", "required", "not_applicable", 10),
    ("M1537-X-SOURCE", "source", "high", "Map the area law, physical regime, constants, and approximation boundary to primary-source passages.", "human source boundary; no Lean proposition", "Reviewed human-source coverage without machine proof credit.", "not_applicable", "required", 60),
    ("M1537-X-FOUNDATION", "certificate", "critical", "Audit imports, axioms, TCB, classical policy, and computation boundaries.", "planned transitive trust report", "Accepted foundation and TCB profile.", "required", "not_applicable", 50),
    ("M1537-X-PROVENANCE", "certificate", "critical", "Inventory local and imported terminal bodies, wrappers, hashes, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without proof credit.", "informational", "not_applicable", 50),
]

checked = {"M1537-S-DEFINITIONS", "M1537-L-COUNTERMODEL", "M1537-T-ASSEMBLE"}
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

obligations, nodes = [], []
for oid, kind, risk, claim, target, output, machine, human, budget in rows:
    body = None
    if oid == "M1537-L-COUNTERMODEL": body = "local:Stage1_Instances/THM-M-1537/ObligationTree.lean#not_bekensteinHawkingAreaLaw"
    if oid == "M1537-T-ASSEMBLE": body = "local:Stage1_Instances/THM-M-1537/ObligationTree.lean#areaLaw_of_bridge"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": "planned:v1:sha256:" + digest([oid, kind, claim, target, output]),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if machine == "not_applicable" else ("release_provenance_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": body,
    })
    debt = "M0-L" if oid in checked else ("M5" if oid == "M1537-ROOT" else "M4")
    nodes.append({
        "node_id": "THM-M-1537-" + oid.removeprefix("M1537-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": debt, "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if human == "required" else "not-applicable",
        "provenance_id": body or "none", "foundation_profile": "lean4-mathlib/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or experiment receives proof credit", "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the frozen formal context and declared proof children.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parents may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1537/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture, countermodel, or conditional interface only; no canonical root proof.",
        "task_ids": [ITEM, "S56-M-1537-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1537/ObligationTree.lean"] if body else [],
        "owner": "THM-M-1537 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable anchor audit; a physics bridge, exact transport, and model counterexample were selected before closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1537-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M1537-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M5"},
    "status_boundary": "The exact root is kernel-refuted for the frozen unconstrained model; theorem proof and completion are blocked pending an authorized statement/model repair.",
}

def edge(eid, source, typ, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal: row["reciprocal_edge_id"] = reciprocal
    return row

proof = []
for parent, child in [("M1537-ROOT", "M1537-B-PHYSICS"), ("M1537-ROOT", "M1537-T-ASSEMBLE"), ("M1537-B-PHYSICS", "M1537-S-REGIME")]:
    req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
    proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1537-ROOT", "logical_decomposition", "M1537-S-DEFINITIONS")],
    "provenance": [edge("SRC-PHYSICS", "M1537-B-PHYSICS", "source_map", "M1537-X-SOURCE"), edge("PROV-ROOT", "M1537-X-PROVENANCE", "provenance_of", "M1537-ROOT")],
    "evidence": [edge("EVID-COUNTERMODEL", "M1537-L-COUNTERMODEL", "evidence_for", "M1537-ROOT")],
    "trust": [edge("TRUST-FOUND", "M1537-ROOT", "trusts", "M1537-X-FOUNDATION"), edge("TRUST-PROV", "M1537-ROOT", "trusts", "M1537-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE", "M1537-X-SOURCE", "documents", "M1537-B-PHYSICS"), edge("DOC-COUNTERMODEL", "M1537-L-COUNTERMODEL", "documents", "M1537-ROOT")],
    "workflow": [edge("FLOW-ASSEMBLE-PHYSICS", "M1537-T-ASSEMBLE", "workflow_depends_on", "M1537-B-PHYSICS"), edge("FLOW-REPAIR-COUNTERMODEL", "M1537-B-PHYSICS", "workflow_depends_on", "M1537-L-COUNTERMODEL")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {oid: [] for oid in ids}, {oid: [] for oid in ids}
    for e in edges:
        outgoing[e["from"]].append(e["edge_id"]); incoming[e["to"]].append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1537-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1537-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs, "minimal_open_root_cut": ["M1537-B-PHYSICS"],
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_refuted_in_current_model": True, "audit_complete": False, "theorem_complete": False, "reason": "The checked countermodel refutes the canonical universal proposition because entropy is an unconstrained record field."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(f"generated {len(ids)} obligations; denominator {denominator}")
