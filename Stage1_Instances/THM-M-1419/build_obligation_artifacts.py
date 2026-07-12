#!/usr/bin/env python3
"""Generate the frozen THM-M-1419 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1419-OBLIGATION_TREE"
TASKS = [ITEM, "S56-M-1419-PROOF"]

specs = [
    ("M1419-ROOT", "root", "The exact selected Oseledets splitting target.", "Stage1Instances.THM_M_1419.OseledetsMultiplicativeErgodicTarget", "The canonical proposition.", "critical", "required", "required", 30),
    ("M1419-S-INTERFACE", "definition", "Freeze cocycle order, norms, AE scopes, measurable fibers, and all boundary choices.", "Stage1Instances.THM_M_1419.{cocycleProduct,MeasurableSubspaceField,OseledetsConclusion}", "The exact elaborated input and output interface.", "high", "not_applicable", "required", 24),
    ("M1419-A-INTEGRABILITY", "transport", "Convert both log-plus moment hypotheses into the scalar subadditive and exterior-power integrability facts used downstream.", "planned exact Lean integrability transport package", "Integrable forward and inverse exterior-power log-norm processes.", "critical", "required", "required", 80),
    ("M1419-E-KINGMAN", "bridge", "Apply a pinned kernel-checked subadditive ergodic theorem to every exterior power and identify almost-sure constant growth rates.", "planned exact Lean Kingman/exterior-power package", "Almost-sure deterministic sums of the largest Lyapunov exponents.", "critical", "required", "required", 100),
    ("M1419-F-FORWARD", "construction", "Construct the forward filtration from exterior-power growth, with dimensions and vector growth characterized on one conull set.", "planned exact Lean forward filtration package", "A measurable invariant forward Lyapunov filtration.", "critical", "required", "required", 100),
    ("M1419-B-BACKWARD", "construction", "Repeat the filtration construction for the inverse cocycle over T inverse and relate backward rates to the forward spectrum.", "planned exact Lean inverse-cocycle filtration package", "A measurable backward filtration with matched exponents.", "critical", "required", "required", 100),
    ("M1419-S-SPLITTING", "construction", "Intersect complementary forward and backward flags and prove nonzero internal direct-sum fibers spanning the whole space.", "planned exact Lean two-sided splitting package", "Finite nonzero Oseledets subspaces and strictly decreasing exponents.", "critical", "required", "required", 100),
    ("M1419-M-MEASURABLE", "bridge", "Prove distance-to-fiber measurability for every subspace produced by the flag-intersection construction.", "planned exact Lean measurable-subspace bridge", "MeasurableSubspaceField E.", "critical", "required", "required", 90),
    ("M1419-I-EQUIVARIANT", "lemma", "Upgrade filtration invariance and almost-everywhere invertibility to one-step equality of mapped splitting fibers.", "planned exact Lean equivariance lemma", "Submodule.map (Matrix.mulVecLin (A ω)) (E ω i) = E (T ω) i almost everywhere.", "critical", "required", "required", 80),
    ("M1419-G-GROWTH", "lemma", "Derive the exact forward logarithmic norm limit for every nonzero vector in each splitting fiber on the same conull set.", "planned exact Lean vector-growth lemma", "The target Tendsto statement for all indices and nonzero fiber vectors.", "critical", "required", "required", 100),
    ("M1419-T-ASSEMBLE", "transport", "Package exponents, measurable fibers, direct-sum, positivity, equivariance, and growth into the exact target.", "Stage1Instances.THM_M_1419.target_of_construction_package", "The exact canonical proposition, conditional on the construction package.", "high", "required", "required", 18),
    ("M1419-S-FOUNDATION", "certificate", "Audit classical choice, axioms, transitive imports, TCB, and the no-oracle boundary for every terminal body.", "planned exact axiom and dependency certificate", "Accepted trust boundary for all proof bodies.", "critical", "not_applicable", "required", 30),
    ("M1419-X-SOURCE", "source_boundary", "Map every substantive reduction and construction to exact primary-source premises and transitions.", "human-source crosswalk; no kernel proof credit", "Reviewed H0 source boundary.", "high", "required", "required", 100),
    ("M1419-X-PROVENANCE", "certificate", "Trace every terminal body, bridge, import, and wrapper to an immutable local or external origin.", "planned transitive declaration provenance report", "Complete formal provenance boundary.", "critical", "not_applicable", "required", 40),
]

def fp(oid, statement):
    if oid == "M1419-ROOT":
        raw = (HERE / "OseledetsStatement.lean").read_bytes()
    else:
        raw = ("THM-M-1419:v1:" + oid + ":" + statement).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()

obligations = []
nodes = []
for oid, kind, statement, formal, output, risk, human, readable, budget in specs:
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp(oid, statement), "kind": kind,
        "root_relevant": True, "machine_eligibility": "not_applicable" if kind == "source_boundary" else "required",
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk, "exclusion_reason": "human_source_boundary_only" if kind == "source_boundary" else None,
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1419/ObligationTree.lean#target_of_construction_package" if oid == "M1419-T-ASSEMBLE" else None,
    })
    closed = oid in {"M1419-S-INTERFACE", "M1419-T-ASSEMBLE"}
    nodes.append({
        "node_id": "THM-M-1419-" + oid.removeprefix("M1419-"), "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": formal, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if closed else ("M3" if oid == "M1419-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md" if oid in {"M1419-ROOT", "M1419-X-SOURCE"} else "primary-source-node-map-pending",
        "provenance_id": "local:Stage1_Instances/THM-M-1419/ObligationTree.lean" if closed else "pending",
        "foundation_profile": "lean4-dependent-type-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; computation and numerical experiments receive no proof credit",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the typed proof children and the exact canonical context.", "inference": statement, "output": output, "outgoing_use": "Consumed only through the declared composition or support edges."},
        "public_readable_target": "Stage1_Instances/THM-M-1419/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture or conditional-interface record only; no open mathematical premise is discharged.",
        "task_ids": TASKS, "owned_sources": [], "owner": "THM-M-1419 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if closed else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-1419",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated splitting statement and immutable candidate audit; standard two-sided exterior-power/forward-backward filtration architecture; eligibility fixed without proof-status discovery.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "OseledetsStatement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1419-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
}

proof_requirements = {
    "M1419-ROOT": ["M1419-T-ASSEMBLE"],
    "M1419-T-ASSEMBLE": ["M1419-S-SPLITTING", "M1419-M-MEASURABLE", "M1419-I-EQUIVARIANT", "M1419-G-GROWTH"],
    "M1419-S-SPLITTING": ["M1419-F-FORWARD", "M1419-B-BACKWARD"],
    "M1419-F-FORWARD": ["M1419-E-KINGMAN"], "M1419-B-BACKWARD": ["M1419-E-KINGMAN"],
    "M1419-E-KINGMAN": ["M1419-A-INTEGRABILITY"],
    "M1419-M-MEASURABLE": ["M1419-S-SPLITTING"], "M1419-I-EQUIVARIANT": ["M1419-S-SPLITTING"],
    "M1419-G-GROWTH": ["M1419-F-FORWARD", "M1419-B-BACKWARD", "M1419-S-SPLITTING"],
}

def make_graph(edges):
    out, inn = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        inn.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": inn}

proof_edges = []
for parent, children in proof_requirements.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof_edges += [{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}]

def edges(kind, triples):
    return make_graph([{"edge_id": eid, "from": src, "type": kind, "to": dst} for eid, src, dst in triples])

graphs = {
    "proof": make_graph(proof_edges),
    "refinement": edges("logical_decomposition", [("REF-INTERFACE", "M1419-ROOT", "M1419-S-INTERFACE")]),
    "provenance": edges("provenance_of", [("PROV-ROOT", "M1419-X-PROVENANCE", "M1419-ROOT"), ("SRC-KINGMAN", "M1419-X-SOURCE", "M1419-E-KINGMAN"), ("SRC-SPLIT", "M1419-X-SOURCE", "M1419-S-SPLITTING")]),
    "evidence": make_graph([]),
    "trust": edges("trusts", [("TRUST-FOUND", "M1419-ROOT", "M1419-S-FOUNDATION"), ("TRUST-PROV", "M1419-ROOT", "M1419-X-PROVENANCE")]),
    "documentation": edges("documents", [("DOC-INTERFACE", "M1419-S-INTERFACE", "M1419-ROOT"), ("DOC-SOURCE", "M1419-X-SOURCE", "M1419-E-KINGMAN")]),
    "workflow": edges("workflow_depends_on", [("FLOW-PROOF-AUDIT", "M1419-T-ASSEMBLE", "M1419-X-SOURCE"), ("FLOW-PROOF-FOUND", "M1419-T-ASSEMBLE", "M1419-S-FOUNDATION"), ("FLOW-PROV-ASSEMBLE", "M1419-X-PROVENANCE", "M1419-T-ASSEMBLE")]),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1419",
    "registry_id": "THM-M-1419-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M1419-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M1419-S-INTERFACE", "M1419-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M1419-S-SPLITTING", "M1419-M-MEASURABLE", "M1419-I-EQUIVARIANT", "M1419-G-GROWTH"],
        "composition_certificates": ["Stage1Instances.THM_M_1419.target_of_construction_package"],
        "reason": "The exact final composition is conditional; all substantive construction, measurability, equivariance, and growth packages remain open."},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated 14 obligations; denominator sha256: {digest}")
