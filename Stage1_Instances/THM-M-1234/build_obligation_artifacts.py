#!/usr/bin/env python3
"""Generate the frozen THM-M-1234 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1234-OBLIGATION_TREE"
THEOREM = "THM-M-1234"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M1234-ROOT", "root", "critical", "Exact whole-plane unforced finite-energy Yudovich existence target.", "Stage1Rev56.THMM1234.Statement", "Canonical proposition", 40),
    ("M1234-S-DEFINITIONS", "definition", "high", "Freeze weak divergence, curl, momentum, trace, and solution interfaces.", "Stage1Rev56.THMM1234.{InitialData,GlobalWeakSolution}", "Exact statement interface", 40),
    ("M1234-S-FOUNDATION", "certificate", "critical", "Audit classical logic, choice, axioms, TCB, and the no-oracle policy.", "planned foundation and transitive axiom report", "Accepted trust boundary", 40),
    ("M1234-A-APPROX", "construction", "critical", "Construct smooth divergence-free approximations preserving energy and uniform vorticity bounds.", "planned regularized initial-data and Euler approximation theorem", "Globally defined approximate solutions with uniform bounds", 100),
    ("M1234-A-ENERGY", "estimate", "critical", "Prove uniform kinetic-energy and essential-vorticity estimates for the approximants.", "planned energy and L-infinity vorticity estimates", "Time-uniform compactness bounds", 100),
    ("M1234-A-COMPACT", "compactness", "critical", "Extract a subsequence with convergence strong enough for the nonlinear momentum term.", "planned weak/strong compactness extraction", "Limit velocity and vorticity with nonlinear convergence", 100),
    ("M1234-A-STRUCTURE", "transport", "critical", "Pass measurability, L2/L-infinity, divergence, and weak-curl structure to the limit.", "Stage1Rev56.THMM1234.CandidateConstructionPackage", "CandidateFields for every admissible datum", 100),
    ("M1234-E-LINEAR", "limit_passage", "high", "Pass the time-derivative and initial linear terms in the weak momentum identity.", "planned linear weak-limit theorem", "Linear weak-equation limits", 80),
    ("M1234-E-NONLINEAR", "limit_passage", "critical", "Pass the quadratic velocity tensor against compact divergence-free tests.", "planned nonlinear compactness theorem", "Quadratic weak-limit identity", 100),
    ("M1234-E-TRACE", "trace", "critical", "Establish the one-sided weak initial vorticity trace for every compact smooth test.", "planned initial-trace theorem", "Canonical initial-vorticity trace", 100),
    ("M1234-E-CLOSURE", "assembly", "critical", "Combine limit identities into momentum and trace closure for each candidate.", "Stage1Rev56.THMM1234.EquationAndTraceClosurePackage", "Equation and trace closure", 80),
    ("M1234-T-ASSEMBLE", "transport", "high", "Construct GlobalWeakSolution from candidate fields and closure witnesses.", "Stage1Rev56.THMM1234.root_of_construction_and_closure", "Exact canonical root conditional on two packages", 40),
    ("M1234-X-SOURCE", "source_boundary", "high", "Map every analytic step to reviewed primary-source theorem passages and hypotheses.", "node-specific primary-source crosswalk", "Human-source coverage only", 60),
    ("M1234-X-PROVENANCE", "certificate", "critical", "Inventory proof bodies, imports, axioms, TCB, and replay evidence.", "planned provenance report", "Release provenance overlay", 40),
]

checked = {"M1234-S-DEFINITIONS", "M1234-T-ASSEMBLE"}
source_na = {"M1234-S-DEFINITIONS", "M1234-S-FOUNDATION", "M1234-X-PROVENANCE"}
machine_special = {"M1234-X-SOURCE": "not_applicable", "M1234-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output, budget in rows:
    machine = machine_special.get(oid, "required")
    fingerprint = ("lean-file-sha256:" + statement_hash if oid in {"M1234-ROOT", "M1234-S-DEFINITIONS"}
                   else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_only", "informational": "provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1234/ObligationTree.lean#root_of_construction_and_closure" if oid == "M1234-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-1234-" + oid.removeprefix("M1234-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1234-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M1234-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical solver or oracle closes this node",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only typed proof children and the exact formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1234/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen architecture or conditional interface only; no open analytic premise is supplied.",
        "task_ids": [ITEM, "S56-M-1234-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1234/ObligationTree.lean"] if oid == "M1234-T-ASSEMBLE" else [],
        "owner": "THM-M-1234 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M1234-ROOT": ["M1234-T-ASSEMBLE"],
    "M1234-T-ASSEMBLE": ["M1234-A-STRUCTURE", "M1234-E-CLOSURE"],
    "M1234-A-STRUCTURE": ["M1234-A-APPROX", "M1234-A-ENERGY", "M1234-A-COMPACT"],
    "M1234-E-CLOSURE": ["M1234-E-LINEAR", "M1234-E-NONLINEAR", "M1234-E-TRACE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1234-ROOT", "logical_decomposition", "M1234-S-DEFINITIONS")],
    "provenance": [edge("SRC-ANALYSIS", "M1234-A-APPROX", "source_map", "M1234-X-SOURCE"), edge("PROV-ROOT", "M1234-X-PROVENANCE", "provenance_of", "M1234-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1234-ROOT", "trusts", "M1234-S-FOUNDATION"), edge("TRUST-PROV", "M1234-ROOT", "trusts", "M1234-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M1234-S-DEFINITIONS", "documents", "M1234-ROOT"), edge("DOC-SOURCE", "M1234-X-SOURCE", "documents", "M1234-A-APPROX")],
    "workflow": [edge("FLOW-ASSEMBLE-CONSTRUCT", "M1234-T-ASSEMBLE", "workflow_depends_on", "M1234-A-STRUCTURE"), edge("FLOW-ASSEMBLE-CLOSE", "M1234-T-ASSEMBLE", "workflow_depends_on", "M1234-E-CLOSURE"), edge("FLOW-PROV-ASSEMBLE", "M1234-X-PROVENANCE", "workflow_depends_on", "M1234-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and completed bounded anchor audit; approximation/compactness route selected before proof-status observation.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1234-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [x["obligation_id"] for x in obligations if x["machine_eligibility"] == "required"], "required_human_source": [x["obligation_id"] for x in obligations if x["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1234-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Architecture only; no analytic package, root proof, source acceptance, or theorem completion.",
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1234-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1234-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composition runs child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1234-A-STRUCTURE", "M1234-E-CLOSURE"], "composition_certificates": ["Stage1Rev56.THMM1234.root_of_construction_and_closure"], "reason": "The checked assembly is conditional; both substantive packages remain unproved."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
