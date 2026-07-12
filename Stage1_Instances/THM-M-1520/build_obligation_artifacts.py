#!/usr/bin/env python3
"""Build the frozen THM-M-1520 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1520-OBLIGATION_TREE"
THEOREM = "THM-M-1520"

specs = [
    ("M1520-ROOT", "root", "The exact canonical LiouvilleStatement.", "Stage1.THM_M_1520.LiouvilleStatement", "The canonical proposition.", "critical", "required", "required", "required", 20),
    ("M1520-S-DEFS", "definition", "Fix canonical phase space, symplectic rotation, Hamiltonian vector field, and volume.", "Stage1.THM_M_1520.{PhaseSpace,symplecticRotation,hamiltonianVectorField}", "The exact objects used by every analytic child.", "high", "required", "not_applicable", "required", 20),
    ("M1520-S-DOMAIN", "definition", "Preserve all binders, regularity hypotheses, the global flow law, and all real times.", "Stage1.THM_M_1520.LiouvilleStatement", "The exact quantified context.", "critical", "required", "required", "required", 20),
    ("M1520-S-BOUNDARY", "terminal", "Cover n = 0, t = 0, and complete global flows without adding positivity assumptions.", "planned exact boundary lemmas for LiouvilleStatement", "Boundary cases compatible with the general proof.", "high", "required", "required", "required", 30),
    ("M1520-S-FOUNDATION", "certificate", "Audit axioms, classical principles, imports, and the Lean/mathlib TCB.", "planned transitive axiom and trust report", "An accepted foundation and TCB profile.", "critical", "required", "not_applicable", "required", 40),
    ("M1520-N-FLOW", "normalization", "Derive the spatial regularity, invertibility, and inverse-time facts needed for change of variables from the stated complete flow.", "planned Lean signature over H and Phi from LiouvilleStatement", "A C1 family of diffeomorphic time maps with inverse Phi (-t).", "critical", "required", "required", "required", 80),
    ("M1520-B-DIVERGENCE", "core_lemma", "Show the canonical Hamiltonian vector field has zero divergence by cancellation of mixed second derivatives.", "planned Lean divergence-free theorem for hamiltonianVectorField H", "div X_H = 0 at every phase point.", "critical", "required", "required", "required", 80),
    ("M1520-C-VARIATION", "construction", "Differentiate the flow in its initial condition and establish the variational equation.", "planned Lean spatial derivative and variational-equation package", "A derivative cocycle solving D_t D Phi_t = DX_H o Phi_t * D Phi_t.", "critical", "required", "required", "required", 100),
    ("M1520-L-JACOBIAN", "core_lemma", "Apply the determinant evolution formula and zero divergence to prove Jacobian determinant one.", "planned Lean Liouville/Jacobi determinant formula", "det D(Phi t) z = 1 for every t and z.", "critical", "required", "required", "required", 100),
    ("M1520-L-MEASURABLE", "lemma", "Prove each time map and its inverse are measurable with the regularity needed by measure transport.", "planned Lean measurability theorem for Phi t", "Measurability and inverse data for every time map.", "high", "required", "required", "required", 50),
    ("M1520-L-CHANGE", "bridge", "Convert the global diffeomorphism and unit Jacobian facts into preservation of Euclidean volume.", "planned exact change-of-variables bridge to MeasurePreserving", "MeasurePreserving (Phi t) volume volume for a fixed t.", "critical", "required", "required", "required", 100),
    ("M1520-T-ALL-TIMES", "terminal", "Discharge the arbitrary-time analytic package from the fixed-time change-of-variables result.", "Stage1.THM_M_1520.LiouvilleAnalyticPackage (planned body)", "LiouvilleAnalyticPackage.", "critical", "required", "required", "required", 30),
    ("M1520-T-ASSEMBLE", "transport", "Unfold the analytic package to the exact public root without changing a binder or hypothesis.", "Stage1.THM_M_1520.liouvilleStatement_of_analyticPackage", "LiouvilleStatement conditional on LiouvilleAnalyticPackage.", "high", "required", "required", "required", 10),
    ("M1520-X-SOURCE", "terminal", "Pinpoint a primary proof and map its assumptions and transitions to the analytic nodes.", "human source boundary; no Lean proposition", "Reviewed source crosswalk for all material transitions.", "high", "not_applicable", "required", "required", 60),
    ("M1520-X-PROVENANCE", "certificate", "Classify every imported or local terminal proof body and its transitive origin.", "planned provenance closure", "Content-addressed proof-body provenance.", "critical", "informational", "not_applicable", "required", 50),
    ("M1520-X-TRUST", "certificate", "Record computation, automation, executable, compiled-artifact, and dependency trust boundaries.", "planned release trust record", "Replayable trust and computation boundary.", "critical", "informational", "not_applicable", "required", 50),
]

def fingerprint(oid, target):
    if oid == "M1520-ROOT":
        return "lean-expression-sha256:547fe7d61d57e7ea242aaff7a97763a769275f0c6f1c64d03ca5db45e82a012b"
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

obligations = []
nodes = []
for oid, kind, statement, target, output, risk, machine, human, readable, budget in specs:
    body = "local:Stage1_Instances/THM-M-1520/ObligationTree.lean#liouvilleStatement_of_analyticPackage" if oid == "M1520-T-ASSEMBLE" else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(oid, target), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk, "exclusion_reason": (
            "provenance_or_trust_overlay_no_proof_credit" if machine == "informational" else
            "human_source_boundary_only" if machine == "not_applicable" else None),
        "terminal_proof_body_id": body,
    })
    closed = oid == "M1520-T-ASSEMBLE"
    nodes.append({
        "node_id": f"THM-M-1520-{oid[6:]}", "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if closed else ("M3" if oid == "M1520-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-pinpoint-pending" if human == "required" else "not-applicable",
        "provenance_id": body or "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or experiment is credited",
        "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "Only the stated formal context and incoming proof_requires children.",
            "inference": statement,
            "output": output,
            "outgoing_use": "Consumed only through the declared reciprocal composition edge or a non-proof support edge.",
        },
        "public_readable_target": f"Stage1_Instances/THM-M-1520/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Architecture or conditional interface only; no unlisted premise and no analytic closure is supplied.",
        "task_ids": [ITEM, "S56-M-1520-PROOF"], "owned_sources": [],
        "owner": "THM-M-1520 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if closed else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus immutable anchor audit; coordinate divergence/Jacobian/change-of-variables route selected before proof closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor_audit.md").read_bytes()).hexdigest(),
    "root_obligation_id": "M1520-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1520-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; the analytic package, source review, trust audit, and exact root remain open.",
}

proof_pairs = [
    ("M1520-ROOT", "M1520-T-ALL-TIMES"), ("M1520-ROOT", "M1520-T-ASSEMBLE"),
    ("M1520-T-ALL-TIMES", "M1520-L-CHANGE"),
    ("M1520-L-CHANGE", "M1520-L-JACOBIAN"), ("M1520-L-CHANGE", "M1520-L-MEASURABLE"),
    ("M1520-L-JACOBIAN", "M1520-C-VARIATION"), ("M1520-L-JACOBIAN", "M1520-B-DIVERGENCE"),
    ("M1520-C-VARIATION", "M1520-N-FLOW"), ("M1520-B-DIVERGENCE", "M1520-S-DEFS"),
    ("M1520-N-FLOW", "M1520-S-DOMAIN"), ("M1520-N-FLOW", "M1520-S-BOUNDARY"),
]
proof_edges = []
for parent, child in proof_pairs:
    req, cmp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof_edges += [
        {"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": cmp},
        {"edge_id": cmp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req},
    ]

other = {
    "refinement": [("REF-ROOT-DOMAIN", "M1520-ROOT", "logical_decomposition", "M1520-S-DOMAIN")],
    "provenance": [("SRC-DIV", "M1520-B-DIVERGENCE", "source_map", "M1520-X-SOURCE"), ("SRC-JAC", "M1520-L-JACOBIAN", "source_map", "M1520-X-SOURCE"), ("PROV-ROOT", "M1520-X-PROVENANCE", "provenance_of", "M1520-ROOT")],
    "evidence": [],
    "trust": [("TRUST-FOUNDATION", "M1520-ROOT", "trusts", "M1520-S-FOUNDATION"), ("TRUST-RELEASE", "M1520-ROOT", "trusts", "M1520-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1520-X-SOURCE", "documents", "M1520-ROOT"), ("DOC-BOUNDARY", "M1520-S-BOUNDARY", "documents", "M1520-N-FLOW")],
    "workflow": [("FLOW-PROOF", "M1520-T-ALL-TIMES", "workflow_depends_on", "M1520-L-CHANGE"), ("FLOW-PROV", "M1520-X-PROVENANCE", "workflow_depends_on", "M1520-T-ASSEMBLE")],
}

def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [{"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges]
    incoming, outgoing = {}, {}
    for e in cooked:
        outgoing.setdefault(e["from"], []).append(e["edge_id"])
        incoming.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}

graphs = {"proof": graph(proof_edges), **{name: graph(edges) for name, edges in other.items()}}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1520-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1520-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M1520-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1520-T-ALL-TIMES"], "composition_certificates": ["Stage1.THM_M_1520.liouvilleStatement_of_analyticPackage"], "reason": "The exact final interface is checked, but the complete analytic package remains open."},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
