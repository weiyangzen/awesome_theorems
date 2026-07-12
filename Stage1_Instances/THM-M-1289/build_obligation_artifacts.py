#!/usr/bin/env python3
"""Generate the frozen THM-M-1289 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1289-OBLIGATION_TREE"
THEOREM = "THM-M-1289"
ROOT = "M1289-ROOT"

# Frozen before consulting any proof-closure metric. Each tuple is
# id, kind, statement, formal target, output, risk, machine, human, readable, budget.
SPECS = [
    (ROOT, "root", "The exact canonical AubinTalentiTarget.", "Stage1Instances.THM_M_1289.AubinTalentiTarget", "The complete canonical proposition.", "critical", "required", "required", "required", 20),
    ("M1289-S-DEFS", "definition", "Fix Euclidean space, critical exponent, bubble, gradient seminorm, and sharp-constant predicate exactly as in Statement.lean.", "Stage1Instances.THM_M_1289.{Euclidean,criticalExponent,bubble,gradientNorm,IsSharpSobolevConstant}", "The definitions shared by every analytic child.", "critical", "required", "not_applicable", "required", 40),
    ("M1289-S-DOMAIN", "definition", "Preserve n >= 3, arbitrary center, and strictly positive real scale with the original binder order.", "binder context of Stage1Instances.THM_M_1289.AubinTalentiTarget", "The exact quantified context.", "critical", "required", "required", "required", 20),
    ("M1289-S-BOUNDARY", "terminal", "Discharge denominator positivity, nonzero scale, and the behavior at x = a without weakening strict positivity.", "planned exact boundary lemmas for n, lambda, and x = a", "All boundary side conditions used downstream.", "high", "required", "required", "required", 60),
    ("M1289-S-FOUNDATION", "certificate", "Audit classical logic, real powers, measure theory, differentiation, imports, and transitive axioms.", "planned transitive foundation and axiom report", "Accepted foundation and TCB profile.", "critical", "required", "not_applicable", "required", 50),
    ("M1289-N-RADIAL", "normalization", "Normalize translation and positive dilation to the radial profile while tracking constants and measure scaling.", "planned translation/dilation identities for bubble", "A checked reduction to the centered unit-scale radial calculation.", "critical", "required", "required", "required", 90),
    ("M1289-C-BUBBLE", "construction", "Construct the real-power bubble and prove its base is strictly positive everywhere.", "planned positivity and well-definedness package for bubble", "A well-defined positive radial function.", "critical", "required", "required", "required", 70),
    ("M1289-L-POS", "core_lemma", "Prove pointwise strict positivity of every admissible bubble.", "Stage1Instances.THM_M_1289.PositivityComponent", "The first root conjunct.", "high", "required", "required", "required", 40),
    ("M1289-L-SMOOTH", "core_lemma", "Prove infinite Frechet differentiability despite fractional real powers.", "Stage1Instances.THM_M_1289.SmoothnessComponent", "The smoothness root conjunct.", "critical", "required", "required", "required", 100),
    ("M1289-L-RADIAL-DERIV", "core_lemma", "Compute first and second Frechet derivatives of the translated radial profile with exact coefficients.", "planned exact fderiv/iteratedFDeriv identities", "Derivative identities consumed by PDE and gradient calculations.", "critical", "required", "required", "required", 100),
    ("M1289-L-PDE", "core_lemma", "Compute the pointwise Laplacian and prove the normalized critical PDE.", "Stage1Instances.THM_M_1289.PDEComponent", "The PDE root conjunct.", "critical", "required", "required", "required", 100),
    ("M1289-L-FUN-NORM", "core_lemma", "Prove finiteness of the critical eLpNorm of the bubble.", "Stage1Instances.THM_M_1289.FunctionNormComponent", "The function-norm finiteness conjunct.", "critical", "required", "required", "required", 100),
    ("M1289-L-GRAD-NORM", "core_lemma", "Prove finiteness of the L2 Frechet-gradient eLpNorm.", "Stage1Instances.THM_M_1289.GradientNormComponent", "The gradient-norm finiteness conjunct.", "critical", "required", "required", "required", 100),
    ("M1289-L-SHARP", "bridge", "Prove the critical homogeneous Sobolev inequality and leastness of its constant over the stated test class.", "planned proof of IsSharpSobolevConstant n C", "A witness C with the exact least-constant property.", "critical", "required", "required", "required", 100),
    ("M1289-L-NORM-EVAL", "computation", "Evaluate the two bubble seminorms, including radial integration and scaling, and establish equality at the same C.", "planned exact radial integral and norm identities", "The sharp equality identity for the explicit bubble.", "critical", "required", "required", "required", 100),
    ("M1289-T-EXTREMAL", "terminal", "Package sharpness and the explicit equality with one shared constant witness.", "Stage1Instances.THM_M_1289.ExtremalComponent", "The existential final root conjunct.", "critical", "required", "required", "required", 40),
    ("M1289-T-ASSEMBLE", "transport", "Consume all six exact component propositions and assemble the unchanged public target.", "Stage1Instances.THM_M_1289.aubinTalentiTarget_of_components", "AubinTalentiTarget conditional on all analytic components.", "high", "required", "required", "required", 20),
    ("M1289-X-SOURCE", "terminal", "Pinpoint primary sources and map every analytic transition, normalization, and equality convention.", "human source boundary; no Lean proposition", "Reviewed premise-level human-source crosswalk.", "high", "not_applicable", "required", "required", 80),
    ("M1289-X-PROVENANCE", "certificate", "Classify every imported and local terminal proof body and transitive origin.", "planned proof-body provenance closure", "Content-addressed provenance records.", "critical", "informational", "not_applicable", "required", 50),
    ("M1289-X-TRUST", "certificate", "Record kernel, automation, executable, compiled artifact, dependency, and computation trust boundaries.", "planned release trust record", "Replayable trust and computation boundary.", "critical", "informational", "not_applicable", "required", 50),
]

def fp(oid, target):
    if oid == ROOT:
        return "lean-expression-sha256:f61848575711c421710615fb16d1febe13fb89e9e57266124c83cebff6ba0a68"
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

obligations, nodes = [], []
for oid, kind, statement, target, output, risk, machine, human, readable, budget in SPECS:
    body = "local:Stage1_Instances/THM-M-1289/ObligationTree.lean#aubinTalentiTarget_of_components" if oid == "M1289-T-ASSEMBLE" else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp(oid, target), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": "non_proof_overlay" if machine == "informational" else ("human_source_only" if machine == "not_applicable" else None),
        "terminal_proof_body_id": body,
    })
    closed = oid == "M1289-T-ASSEMBLE"
    nodes.append({
        "node_id": "THM-M-1289-" + oid[6:], "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if closed else ("M3" if oid == ROOT else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-pinpoint-pending" if human == "required" else "not-applicable",
        "provenance_id": body or "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none credited; radial integral computation remains a proof obligation",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Exact stated context plus declared proof_requires children.", "inference": statement, "output": output, "outgoing_use": "Only the reciprocal composition edge or a typed non-proof support edge."},
        "public_readable_target": f"Stage1_Instances/THM-M-1289/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture or conditional interface only; no unlisted analytic fact is supplied.",
        "task_ids": [ITEM, "S56-M-1289-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1289/ObligationTree.lean"] if closed else [],
        "owner": "THM-M-1289 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if closed else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in FIELDS} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable anchor audit; radial differentiation, integration, sharp-inequality, and equality route selected before closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": ROOT, "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new version with append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1289-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; all substantive analytic leaves and the exact root remain open.",
}

pairs = [
    (ROOT, "M1289-L-POS"), (ROOT, "M1289-L-SMOOTH"), (ROOT, "M1289-L-PDE"),
    (ROOT, "M1289-L-FUN-NORM"), (ROOT, "M1289-L-GRAD-NORM"), (ROOT, "M1289-T-EXTREMAL"),
    (ROOT, "M1289-T-ASSEMBLE"), ("M1289-L-POS", "M1289-C-BUBBLE"),
    ("M1289-L-SMOOTH", "M1289-C-BUBBLE"), ("M1289-L-SMOOTH", "M1289-L-RADIAL-DERIV"),
    ("M1289-L-PDE", "M1289-L-RADIAL-DERIV"), ("M1289-L-PDE", "M1289-N-RADIAL"),
    ("M1289-L-FUN-NORM", "M1289-N-RADIAL"), ("M1289-L-GRAD-NORM", "M1289-L-RADIAL-DERIV"),
    ("M1289-L-GRAD-NORM", "M1289-N-RADIAL"), ("M1289-T-EXTREMAL", "M1289-L-SHARP"),
    ("M1289-T-EXTREMAL", "M1289-L-NORM-EVAL"), ("M1289-N-RADIAL", "M1289-S-DOMAIN"),
    ("M1289-C-BUBBLE", "M1289-S-DEFS"), ("M1289-C-BUBBLE", "M1289-S-BOUNDARY"),
]
proof = []
for parent, child in pairs:
    req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof += [{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}]

other = {
    "refinement": [("REF-ROOT-DOMAIN", ROOT, "logical_decomposition", "M1289-S-DOMAIN")],
    "provenance": [("SRC-PDE", "M1289-L-PDE", "source_map", "M1289-X-SOURCE"), ("SRC-SHARP", "M1289-L-SHARP", "source_map", "M1289-X-SOURCE"), ("PROV-ROOT", "M1289-X-PROVENANCE", "provenance_of", ROOT)],
    "evidence": [],
    "trust": [("TRUST-FOUNDATION", ROOT, "trusts", "M1289-S-FOUNDATION"), ("TRUST-RELEASE", ROOT, "trusts", "M1289-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1289-X-SOURCE", "documents", ROOT), ("DOC-BOUNDARY", "M1289-S-BOUNDARY", "documents", "M1289-C-BUBBLE")],
    "workflow": [("FLOW-PROOF", "M1289-T-EXTREMAL", "workflow_depends_on", "M1289-L-SHARP"), ("FLOW-PROV", "M1289-X-PROVENANCE", "workflow_depends_on", "M1289-T-ASSEMBLE")],
}

def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [{"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges]
    incoming, outgoing = {}, {}
    for edge in cooked:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}

graphs = {"proof": graph(proof), **{name: graph(edges) for name, edges in other.items()}}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1289-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": ROOT, "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M1289-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1289-L-POS", "M1289-L-SMOOTH", "M1289-L-PDE", "M1289-L-FUN-NORM", "M1289-L-GRAD-NORM", "M1289-T-EXTREMAL"], "composition_certificates": ["Stage1Instances.THM_M_1289.aubinTalentiTarget_of_components"], "reason": "The exact conditional assembly is checked; all six analytic component premises remain open."},
}
(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
