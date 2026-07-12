#!/usr/bin/env python3
"""Build the deterministic THM-M-1246 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM, THEOREM, PREFIX = "S56-M-1246-OBLIGATION_TREE", "THM-M-1246", "M1246-"

# short id, kind, claim, formal target, output, risk, human-source eligibility
ROWS = [
    ("ROOT", "root", "Prove the exact frozen Euclidean differential L2 Hardy inequality.", "Stage1Instances.THM_M_1246.HardyInequalityTarget", "The canonical proposition.", "critical", "required"),
    ("S-DEFINITIONS", "definition", "Freeze Euclidean space, volume measure, compact support, smoothness, fderiv norm, singular weight, and sharp constant.", "Stage1Instances.THM_M_1246.HardyInequalityTarget", "The exact elaborated vocabulary and binder context.", "high", "not_applicable"),
    ("S-BOUNDARY", "normalization", "Account for n >= 3, u = 0, totalized division at the origin, and integrability of both displayed integrands.", "planned exact boundary and integrability package", "Legal finite integral manipulations including the null singular point.", "critical", "required"),
    ("S-FOUNDATION", "certificate", "Audit classical logic, choice, Haar volume, Bochner integration, imports, axioms, and TCB.", "planned transitive axiom/import certificate", "Accepted trust boundary for terminal bodies.", "high", "not_applicable"),
    ("N-CUTOFF", "construction", "Construct radial cutoffs excluding a ball about zero and prove support, smoothness, and convergence properties.", "planned punctured-domain cutoff family", "A regularized domain on which divergence and integration by parts are nonsingular.", "critical", "required"),
    ("L-DIVERGENCE", "core_lemma", "Compute div(x / ||x||^2) = (n-2) / ||x||^2 away from zero in Euclidean dimension n.", "planned Frechet divergence identity on Space n minus {0}", "The sharp dimension coefficient in the weighted integral.", "critical", "required"),
    ("L-INTEGRATION-BY-PARTS", "core_lemma", "Apply compact-support integration by parts to u^2 times the regularized radial vector field.", "planned Bochner/Lebesgue integration-by-parts identity", "The weighted L2 integral bounded through u and its derivative.", "critical", "required"),
    ("L-DERIVATIVE", "lemma", "Identify the derivative of u^2 and its pairing with the radial vector field, with all real and norm coercions.", "planned fderiv product/inner-product estimate", "The cross-term with coefficient two.", "high", "required"),
    ("L-CAUCHY-SCHWARZ", "core_lemma", "Bound the cross-term by the square roots of the weighted L2 and derivative-energy integrals.", "planned integral Cauchy-Schwarz estimate", "(n-2) A <= 2 sqrt(A) sqrt(E).", "critical", "required"),
    ("L-LIMIT", "bridge", "Remove the puncture cutoff by dominated or monotone convergence and retain the exact weighted integrals.", "planned cutoff-limit theorem", "The global inequality before scalar rearrangement.", "critical", "required"),
    ("L-REARRANGE", "lemma", "Use n >= 3 and nonnegativity to derive A <= (2/(n-2))^2 E, including A = 0.", "planned ordered-field square-root rearrangement", "The exact sharp scalar coefficient and inequality direction.", "high", "required"),
    ("T-ANALYTIC", "terminal", "Assemble cutoff, divergence, integration by parts, Cauchy-Schwarz, limit, and scalar steps for every frozen binder.", "Stage1Instances.THM_M_1246.ObligationTree.HardyTerminal", "The complete exact Hardy proposition, still open.", "critical", "required"),
    ("T-ROOT-TRANSPORT", "transport", "Transport the exact analytic terminal proposition to the canonical declaration.", "Stage1Instances.THM_M_1246.ObligationTree.root_of_hardyTerminal", "The exact public root from the exact terminal package.", "high", "required"),
    ("X-SOURCE", "terminal", "Pinpoint-map each material analytic transition to primary sources, assumptions, and errata.", "planned primary-source node crosswalk", "Human-source coverage for the selected proof route.", "high", "required"),
    ("X-PROVENANCE", "certificate", "Record terminal bodies, imports, wrappers, axioms, TCB, and replay provenance.", "planned provenance and trust closure packet", "A support-only provenance overlay.", "critical", "not_applicable"),
]

CHILDREN = {
    "ROOT": ["T-ROOT-TRANSPORT"], "T-ROOT-TRANSPORT": ["T-ANALYTIC"],
    "T-ANALYTIC": ["S-BOUNDARY", "N-CUTOFF", "L-DIVERGENCE", "L-INTEGRATION-BY-PARTS", "L-DERIVATIVE", "L-CAUCHY-SCHWARZ", "L-LIMIT", "L-REARRANGE"],
    "N-CUTOFF": ["S-DEFINITIONS", "S-BOUNDARY"],
    "L-DIVERGENCE": ["S-DEFINITIONS", "S-BOUNDARY"],
    "L-INTEGRATION-BY-PARTS": ["N-CUTOFF", "L-DIVERGENCE", "L-DERIVATIVE"],
    "L-DERIVATIVE": ["S-DEFINITIONS"],
    "L-CAUCHY-SCHWARZ": ["S-BOUNDARY", "L-INTEGRATION-BY-PARTS"],
    "L-LIMIT": ["S-BOUNDARY", "N-CUTOFF", "L-CAUCHY-SCHWARZ"],
    "L-REARRANGE": ["S-BOUNDARY", "L-LIMIT"],
}

def oid(short): return PREFIX + short
def planned(short, claim, formal):
    return "planned:v1:sha256:" + hashlib.sha256(f"v1\n{oid(short)}\n{claim}\n{formal}".encode()).hexdigest()
def graph(edges):
    out, incoming = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e["edge_id"])
        incoming.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}
def edge(group, number, source, target, kind, reciprocal=None):
    e = {"edge_id": f"M1246-{group.upper()}-{number:02d}", "from": oid(source), "to": oid(target), "type": kind}
    if reciprocal: e["reciprocal_edge_id"] = reciprocal
    return e

def main():
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations, nodes = [], []
    for short, kind, claim, formal, output, risk, human_eligibility in ROWS:
        machine = "informational" if short.startswith("X-") else "required"
        fingerprint = "lean-expression-sha256:07f1c030325dfe8d02e99a0af1a00c5241a312e6195aa4a9e2967822960048f1" if short in {"ROOT", "S-DEFINITIONS", "T-ANALYTIC"} else planned(short, claim, formal)
        obligations.append({"obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind, "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": human_eligibility, "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": "source_or_provenance_overlay_no_machine_proof_credit" if machine == "informational" else None, "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1246/ObligationTree.lean#root_of_hardyTerminal" if short == "T-ROOT-TRANSPORT" else None})
        children = CHILDREN.get(short, [])
        closed = short in {"S-DEFINITIONS", "T-ROOT-TRANSPORT"}
        nodes.append({
            "node_id": f"{THEOREM}-{short}", "obligation_id": oid(short), "kind": kind,
            "human_statement": claim, "formal_target": formal, "output": output,
            "human_debt": "H2", "machine_debt": "M0-L" if closed else ("M3" if short == "ROOT" else "M4"), "readability_debt": "R4", "evidence_ids": [],
            "source_crosswalk_id": "primary-source-node-map-pending" if human_eligibility == "required" else "not-applicable",
            "provenance_id": "local-obligation-tree-composition" if short == "T-ROOT-TRANSPORT" else "none",
            "foundation_profile": "lean4-mathlib-classical-analysis/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
            "computation_record": "none; no oracle or external computation supplies proof credit", "step_budget": 100 if children else 40,
            "semantic_step_ledger": {"premises": ", ".join(oid(c) for c in children) if children else "Exact frozen context only.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
            "public_readable_target": f"Stage1_Instances/THM-M-1246/obligation-tree.md#{oid(short).lower()}", "validation_spec_id": f"VAL-{oid(short)}",
            "status_boundary": "Architecture or checked conditional interface only; no undeclared premise and no root proof closure.", "task_ids": [ITEM, "S56-M-1246-PROOF"],
            "owned_sources": ["Stage1_Instances/THM-M-1246/ObligationTree.lean"] if short == "T-ROOT-TRANSPORT" else [], "owner": "THM-M-1246 proof lane", "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-12" if closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if closed else "open"},
        })
    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    digest = hashlib.sha256(json.dumps([{k: r[k] for k in fields} for r in obligations], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    ids = [r["obligation_id"] for r in obligations]
    registry = {"schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact elaborated statement and immutable bounded anchor audit; classical divergence/cutoff architecture; eligibility assigned before proof-phase closure.", "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash, "root_obligation_id": oid("ROOT"), "denominator_sha256": digest, "frozen_denominators": {"inventory": ids, "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"]}, "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.", "obligations": obligations, "append_only_delta": [], "status_observed_after_freeze": {"closed_obligations": [oid("S-DEFINITIONS"), oid("T-ROOT-TRANSPORT")], "root_machine_debt": "M3"}, "status_boundary": "Frozen scope and architecture only; no Hardy proof, H0/R0 promotion, or theorem completion."}
    proof, number = [], 1
    for parent, children in CHILDREN.items():
        for child in children:
            rid, cid = f"M1246-PROOF-{number:02d}R", f"M1246-PROOF-{number:02d}C"
            a, b = edge("proof", number, parent, child, "proof_requires", cid), edge("proof", number, child, parent, "composes", rid)
            a["edge_id"], b["edge_id"] = rid, cid; proof += [a, b]; number += 1
    graphs = {
        "proof": graph(proof),
        "refinement": graph([edge("refine", 1, "ROOT", "S-DEFINITIONS", "logical_decomposition"), edge("refine", 2, "ROOT", "S-BOUNDARY", "logical_decomposition"), edge("refine", 3, "ROOT", "S-FOUNDATION", "logical_decomposition")]),
        "provenance": graph([edge("prov", 1, "T-ROOT-TRANSPORT", "X-PROVENANCE", "provenance_of")]),
        "evidence": graph([edge("evidence", 1, "T-ROOT-TRANSPORT", "S-FOUNDATION", "evidence_for")]),
        "trust": graph([edge("trust", 1, "ROOT", "S-FOUNDATION", "trusts"), edge("trust", 2, "T-ANALYTIC", "X-PROVENANCE", "trusts")]),
        "documentation": graph([edge("docs", 1, "ROOT", "X-SOURCE", "documents"), edge("docs", 2, "ROOT", "X-PROVENANCE", "documents")]),
        "workflow": graph([edge("workflow", 1, "T-ANALYTIC", "X-SOURCE", "workflow_depends_on"), edge("workflow", 2, "ROOT", "T-ROOT-TRANSPORT", "workflow_depends_on")]),
    }
    bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-1246-OBLIGATIONS-v1", "registry_denominator_sha256": digest, "root_node_id": oid("ROOT"), "edge_direction": "proof_requires is parent to child; reciprocal composes is child to parent.", "nodes": nodes, "graphs": graphs, "closure_boundary": {"closed_obligations": [oid("S-DEFINITIONS"), oid("T-ROOT-TRANSPORT")], "root_closed": False, "theorem_complete": False, "remaining_root_cut_set": [oid("T-ANALYTIC")], "root_machine_debt": "M3"}}
    recipes = [{"recipe_id": f"VAL-{oid(s)}", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1246/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 60, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1246 obligation tree"}], "covered_obligation_ids": [oid(s)], "covered_declarations": [formal] if formal.startswith("Stage1Instances.") else []} for s, _, _, formal, _, _, _ in ROWS]
    specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes, "status_boundary": "Structural recipes validate the freeze and exact conditional composition, not open analytic proofs."}
    for name, obj in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
        (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=True) + "\n")

if __name__ == "__main__": main()
