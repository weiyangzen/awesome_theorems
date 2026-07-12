#!/usr/bin/env python3
"""Build the frozen THM-M-1241 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1241-OBLIGATION_TREE"
THEOREM = "THM-M-1241"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("M1241-ROOT", "root", "critical", "The exact Nirenberg 1959 formulas (2.2)-(2.3) target.", "Stage1Instances.THM_M_1241.GagliardoNirenbergTarget", "Canonical proposition"),
    ("M1241-S-INTERFACE", "definition", "high", "Freeze coordinate derivatives, finite suprema, ENNReal norms, regularity, and uniform constant scope.", "Stage1Instances.THM_M_1241.{coordinateDerivative,derivativeLpNorm,ParameterConclusion}", "Exact analytic interface"),
    ("M1241-S-FOUNDATION", "certificate", "critical", "Audit classical logic, choice, axioms, imports, TCB, and the no-oracle boundary.", "transitive trust report for terminal bodies", "Accepted trust boundary"),
    ("M1241-R-SMOOTH", "reduction", "critical", "Reduce the C^m finite-norm input to smooth compactly supported approximants without losing the required norms or endpoint hypotheses.", "exact density and approximation lemmas over Euclidean space", "A proof-ready dense class with limiting invariants"),
    ("M1241-L-LOCAL", "core_lemma", "critical", "Establish the local derivative estimate at scale h from Taylor expansion and averaged finite differences.", "exact local coordinate-derivative estimate", "A two-term scale-dependent derivative bound"),
    ("M1241-L-NORM", "lemma", "critical", "Integrate the local estimate and control every ordered coordinate derivative uniformly over the finite maximum.", "exact eLpNorm estimate for derivativeLpNorm", "A global two-term norm estimate"),
    ("M1241-C-OPTIMIZE", "construction", "critical", "Choose the scale and optimize the two terms to obtain powers a and 1-a with the scaling equation.", "exact real-power optimization lemma", "The interpolated product bound"),
    ("M1241-B-CRITICAL", "branch", "critical", "Handle the finite-r integer critical relation and enforce the source exclusion a < 1.", "exact critical-parameter branch", "Finite-exponent critical cases"),
    ("M1241-T-FINITE", "terminal", "critical", "Assemble all cases with q and r finite into FiniteExponentPackage.", "Stage1Instances.THM_M_1241.FiniteExponentPackage", "Uniform finite-exponent inequality"),
    ("M1241-B-INFINITY", "branch", "critical", "Prove the q=infinity and r=infinity norm estimates with the source convention 1/infinity=0.", "exact ENNReal infinity endpoint lemmas", "Infinite-exponent analytic estimates"),
    ("M1241-B-ZERO", "branch", "critical", "In the j=0, r*m<n, q=infinity case use precisely the decay-or-finite-LqTilde hypothesis.", "exact ZeroOrderExceptionalHypothesis endpoint lemma", "Exceptional zero-order estimate"),
    ("M1241-T-ENDPOINT", "terminal", "critical", "Assemble every case where q or r is infinite into InfiniteEndpointPackage.", "Stage1Instances.THM_M_1241.InfiniteEndpointPackage", "Uniform infinite-endpoint inequality"),
    ("M1241-T-ASSEMBLE", "transport", "high", "Split exhaustively between finite q,r and the infinite endpoint complement and compose into the canonical root.", "Stage1Instances.THM_M_1241.root_of_finite_and_endpoint_packages", "Exact canonical target conditional on both packages"),
    ("M1241-X-SOURCE", "source", "high", "Map every analytic lemma and endpoint branch to reviewed primary-source passages, assumptions, and errata.", "node-specific human source crosswalk", "Human-source coverage only"),
    ("M1241-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, wrappers, axioms, TCB, and replay evidence.", "machine-derived provenance ledger", "Release provenance only"),
]

checked = {"M1241-S-INTERFACE", "M1241-T-ASSEMBLE"}
source_na = {"M1241-S-INTERFACE", "M1241-S-FOUNDATION", "M1241-X-PROVENANCE"}
machine_special = {"M1241-X-SOURCE": "not_applicable", "M1241-X-PROVENANCE": "informational"}
obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = "open:v1:sha256:" + digest([oid, kind, claim, target, output])
    if oid == "M1241-ROOT":
        fingerprint = "lean-expression-sha256:bf613985e300aa3a5b5e8299a1e0e0e059369387e17c7f0d2c92dc8d8190eb82"
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1241/ObligationTree.lean#root_of_finite_and_endpoint_packages" if oid == "M1241-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-1241-" + oid.removeprefix("M1241-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1241-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M1241-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no external computation or oracle supplies proof credit",
        "step_budget": 100 if risk == "critical" else 50,
        "semantic_step_ledger": {"premises": "Only the stated context and proof_requires children.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1241/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen obligation or checked conditional interface; no unlisted premise or root closure.",
        "task_ids": [ITEM, "S56-M-1241-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1241/ObligationTree.lean"] if oid == "M1241-T-ASSEMBLE" else [],
        "owner": "THM-M-1241 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable anchor audit; eligibility assigned before proof execution.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1241-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1241-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; neither analytic package nor the theorem is proved.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M1241-ROOT": ["M1241-T-ASSEMBLE"],
    "M1241-T-ASSEMBLE": ["M1241-T-FINITE", "M1241-T-ENDPOINT"],
    "M1241-T-FINITE": ["M1241-R-SMOOTH", "M1241-L-LOCAL", "M1241-L-NORM", "M1241-C-OPTIMIZE", "M1241-B-CRITICAL"],
    "M1241-T-ENDPOINT": ["M1241-B-INFINITY", "M1241-B-ZERO"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-INTERFACE", "M1241-ROOT", "logical_decomposition", "M1241-S-INTERFACE")],
    "provenance": [edge("SRC-LOCAL", "M1241-L-LOCAL", "source_map", "M1241-X-SOURCE"), edge("SRC-ENDPOINT", "M1241-T-ENDPOINT", "source_map", "M1241-X-SOURCE"), edge("PROV-ROOT", "M1241-X-PROVENANCE", "provenance_of", "M1241-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1241-ROOT", "trusts", "M1241-S-FOUNDATION"), edge("TRUST-PROV", "M1241-ROOT", "trusts", "M1241-X-PROVENANCE")],
    "documentation": [edge("DOC-INTERFACE", "M1241-S-INTERFACE", "documents", "M1241-ROOT"), edge("DOC-SOURCE", "M1241-X-SOURCE", "documents", "M1241-L-LOCAL")],
    "workflow": [edge("FLOW-ASSEMBLE-FINITE", "M1241-T-ASSEMBLE", "workflow_depends_on", "M1241-T-FINITE"), edge("FLOW-ASSEMBLE-ENDPOINT", "M1241-T-ASSEMBLE", "workflow_depends_on", "M1241-T-ENDPOINT"), edge("FLOW-PROV-ASSEMBLE", "M1241-X-PROVENANCE", "workflow_depends_on", "M1241-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1241-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1241-ROOT", "edge_direction": "proof_requires runs parent to child; composes runs child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1241-T-FINITE", "M1241-T-ENDPOINT"], "composition_certificates": ["Stage1Instances.THM_M_1241.root_of_finite_and_endpoint_packages"], "reason": "The checked assembly is conditional and neither analytic package has a proof body."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
