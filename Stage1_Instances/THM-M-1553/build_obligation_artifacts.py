#!/usr/bin/env python3
"""Generate the frozen THM-M-1553 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1553-OBLIGATION_TREE"
THEOREM = "THM-M-1553"
PREFIX = "M1553"

# id, kind, human statement, formal target, output, risk, M, H, R, budget
SPECS = [
    ("M1553-ROOT", "root", "The exact frozen Hirota-to-KdV proposition.", "Stage1Instances.THM_M_1553.HirotaKdVTarget", "The canonical proposition.", "critical", "required", "required", "required", 15),
    ("M1553-S-CONTEXT", "definition", "Preserve tau's real space-time domain, C5 regularity, strict positivity, and all-point quantifiers.", "Stage1Instances.THM_M_1553.HirotaKdVTarget", "The exact quantified context.", "critical", "required", "required", "required", 20),
    ("M1553-N-HIROTA", "normalization", "Expand D_x^4 and D_x D_t with the frozen binomial signs and mixed-derivative order.", "Stage1Instances.THM_M_1553.hirotaD", "A pointwise ordinary partial-derivative identity.", "critical", "required", "required", "required", 70),
    ("M1553-N-TRANSFORM", "normalization", "Expand u = 2 partial_x^2(log tau) and the KdV residual without changing signs.", "Stage1Instances.THM_M_1553.{tauTransform,kdvResidual}", "The explicit log-derivative KdV expression.", "critical", "required", "required", "required", 50),
    ("M1553-L-REGULARITY", "lemma", "Derive every partial derivative and log-composition regularity fact used by the algebra.", "planned exact ContDiff/deriv lemmas", "Legality of the required derivatives and product/chain rules.", "critical", "required", "required", "required", 100),
    ("M1553-L-LOG", "core_lemma", "Prove the first through fifth logarithmic derivative identities using tau > 0.", "planned exact logarithmic derivative package", "Derivatives of log tau as rational expressions in derivatives of tau.", "critical", "required", "required", "required", 100),
    ("M1553-L-MIXED", "core_lemma", "Justify the mixed x/t derivative commutations needed by D_x D_t and u_t.", "planned mixed-partial commutation lemmas", "Compatible mixed derivatives through total order five.", "critical", "required", "required", "required", 90),
    ("M1553-B-POLYNOMIAL", "bridge", "Combine the expansions into the pointwise identity relating the KdV residual to the normalized bilinear expression.", "Stage1Instances.THM_M_1553.LogDerivativeBridge (planned body)", "The central bilinear-to-KdV logarithmic derivative bridge.", "critical", "required", "required", "required", 100),
    ("M1553-T-ZERO", "terminal", "Use strict positivity to clear the nonzero tau denominator and apply the bilinear zero hypothesis.", "planned exact pointwise zero bridge", "The KdV residual vanishes at an arbitrary point.", "critical", "required", "required", "required", 45),
    ("M1553-T-ASSEMBLE", "composition", "Compose the universal logarithmic-derivative bridge into the exact public root.", "Stage1Instances.THM_M_1553.hirotaKdVTarget_of_logDerivativeBridge", "HirotaKdVTarget, conditional on the open bridge.", "high", "required", "required", "required", 10),
    ("M1553-S-BOUNDARY", "terminal", "Check constant positive tau, arbitrary points, and exclusion of zeros without adding decay or nonconstancy.", "planned exact boundary lemmas", "Boundary cases consistent with the root.", "high", "required", "required", "required", 35),
    ("M1553-X-SOURCE", "terminal", "Pinpoint a primary Hirota/KdV equation and map conventions to every mathematical node.", "human source boundary", "Reviewed source crosswalk.", "high", "not_applicable", "required", "required", 60),
    ("M1553-X-PROVENANCE", "certificate", "Classify every local and imported terminal proof body and transitive origin.", "planned provenance closure", "Content-addressed provenance.", "critical", "informational", "not_applicable", "required", 50),
    ("M1553-X-TRUST", "certificate", "Audit axioms, imports, automation, binaries, and the Lean/mathlib TCB.", "planned trust closure", "Replayable foundation and trust boundary.", "critical", "informational", "not_applicable", "required", 50),
]

def fp(oid, target):
    if oid == "M1553-ROOT":
        return "lean-expression-sha256:ef5d4bb909f3eba6d2a347e8bad055e3a4a08402beb725499259bb9bf1a9c3bc"
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

obligations = []
nodes = []
for oid, kind, statement, target, output, risk, machine, human, readable, budget in SPECS:
    closed = oid == "M1553-T-ASSEMBLE"
    body = "local:Stage1_Instances/THM-M-1553/ObligationTree.lean#hirotaKdVTarget_of_logDerivativeBridge" if closed else None
    exclusion = "provenance_or_trust_overlay_no_proof_credit" if machine == "informational" else ("human_source_boundary_only" if machine == "not_applicable" else None)
    obligations.append({"obligation_id": oid, "statement_fingerprint": fp(oid, target), "kind": kind, "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": human, "readable_eligibility": readable, "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": body})
    nodes.append({
        "node_id": f"THM-M-1553-{oid[len(PREFIX)+1:]}", "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if closed else ("M3" if oid == "M1553-ROOT" else "M4"), "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "source-pinpoint-pending" if human == "required" else "not-applicable", "provenance_id": body or "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending", "computation_record": "none; no oracle or experiment is credited",
        "step_budget": budget, "semantic_step_ledger": {"premises": "Only the frozen target context and incoming proof_requires children.", "inference": statement, "output": output, "outgoing_use": "Only declared reciprocal composition or non-proof support edges."},
        "public_readable_target": f"Stage1_Instances/THM-M-1553/obligation-tree.md#{oid.lower()}", "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Architecture or conditional interface only; no unlisted analytic premise is supplied.", "task_ids": [ITEM, "S56-M-1553-PROOF"], "owned_sources": [], "owner": "THM-M-1553 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if closed else "open"}
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable anchor audit; logarithmic-derivative normalization route selected before closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(), "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1553-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": [r["obligation_id"] for r in obligations], "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"], "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"], "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.", "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1553-T-ASSEMBLE"], "root_machine_debt": "M3"}, "status_boundary": "Scope and denominators only; the analytic bridge, source review, trust audit, and exact root remain open."
}

pairs = [("M1553-ROOT", "M1553-B-POLYNOMIAL"), ("M1553-ROOT", "M1553-T-ASSEMBLE"), ("M1553-B-POLYNOMIAL", "M1553-N-HIROTA"), ("M1553-B-POLYNOMIAL", "M1553-N-TRANSFORM"), ("M1553-B-POLYNOMIAL", "M1553-L-LOG"), ("M1553-B-POLYNOMIAL", "M1553-L-MIXED"), ("M1553-L-LOG", "M1553-L-REGULARITY"), ("M1553-L-MIXED", "M1553-L-REGULARITY"), ("M1553-T-ZERO", "M1553-B-POLYNOMIAL"), ("M1553-T-ZERO", "M1553-S-CONTEXT"), ("M1553-ROOT", "M1553-T-ZERO"), ("M1553-S-CONTEXT", "M1553-S-BOUNDARY")]
proof = []
for parent, child in pairs:
    req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof.extend([{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}])
other = {
    "refinement": [("REF-ROOT-CONTEXT", "M1553-ROOT", "logical_decomposition", "M1553-S-CONTEXT")],
    "provenance": [("SRC-HIROTA", "M1553-N-HIROTA", "source_map", "M1553-X-SOURCE"), ("SRC-BRIDGE", "M1553-B-POLYNOMIAL", "source_map", "M1553-X-SOURCE"), ("PROV-ROOT", "M1553-X-PROVENANCE", "provenance_of", "M1553-ROOT")],
    "evidence": [], "trust": [("TRUST-ROOT", "M1553-ROOT", "trusts", "M1553-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1553-X-SOURCE", "documents", "M1553-ROOT"), ("DOC-BOUNDARY", "M1553-S-BOUNDARY", "documents", "M1553-S-CONTEXT")],
    "workflow": [("FLOW-PROOF", "M1553-B-POLYNOMIAL", "workflow_depends_on", "M1553-L-REGULARITY"), ("FLOW-PROV", "M1553-X-PROVENANCE", "workflow_depends_on", "M1553-T-ASSEMBLE")]
}
def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [{"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges]
    incoming, outgoing = {}, {}
    for e in cooked:
        outgoing.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}

bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-1553-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "root_node_id": "M1553-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": {"proof": graph(proof), **{k: graph(v) for k, v in other.items()}}, "closure_boundary": {"closed_obligations": ["M1553-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1553-B-POLYNOMIAL", "M1553-T-ZERO"], "composition_certificates": ["Stage1Instances.THM_M_1553.hirotaKdVTarget_of_logDerivativeBridge"], "reason": "The conditional final interface is checked, but the logarithmic-derivative bridge and its application remain open."}}
(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
