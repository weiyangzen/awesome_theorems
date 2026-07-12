#!/usr/bin/env python3
"""Build the deterministic THM-M-1061 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1061-OBLIGATION_TREE"
THEOREM = "THM-M-1061"
PREFIX = "M1061-"

# Eligibility is architectural, not inferred from the observed absence of proofs.
ROWS = [
    ("ROOT", "root", "The exact frozen bounded-continuous Varadhan integral lemma.", "Stage1Instances.THM_M_1061.VaradhanIntegralLemmaTarget", "The canonical proposition.", "critical", "required"),
    ("S-DEFINITIONS", "definition", "Freeze the full LDP, good rate function, logarithmic integral, EReal coercions, and Polish/Borel context.", "Stage1Instances.THM_M_1061.{SatisfiesLDP,IsGoodRateFunction,LogExpIntegral}", "The exact elaborated vocabulary and context.", "high", "not_applicable"),
    ("S-BOUNDARIES", "normalization", "Preserve nonempty X, positive speed tending to zero, bounded F, infinite rate values, and zero/infinite integral semantics.", "planned exact boundary package", "All frozen degenerate-case conventions.", "high", "required"),
    ("S-FOUNDATION", "certificate", "Audit imports, classical choice, noncomputability, transitive axioms, and the EReal/ENNReal trust boundary.", "planned axiom/import/TCB certificate", "Accepted foundation profile.", "critical", "not_applicable"),
    ("N-VARIATIONAL", "normalization", "Normalize the target value sup_x (F x - I x), including finite approximants and EReal order/coercion facts.", "planned EReal variational-value normalization", "A stable variational target usable by both bounds.", "high", "required"),
    ("L-LOWER-LOCAL", "core_lemma", "For each x and tolerance, use continuity of F and the open-set LDP lower bound on a neighborhood of x.", "planned local exponential-integral lower estimate", "A pointwise lower bound F x - I x.", "critical", "required"),
    ("T-LOWER", "terminal", "Pass the local estimates through liminf and supremum to obtain the global lower bound.", "planned global liminf lower bound", "variational value <= liminf logarithmic integrals.", "critical", "required"),
    ("C-COMPACT-COVER", "construction", "For a finite rate sublevel, construct a finite cover on which F is controlled and retain all compactness invariants.", "planned compact-sublevel finite-cover package", "A finite exponential-sum upper estimate on the compact core.", "critical", "required"),
    ("L-CORE-UPPER", "core_lemma", "Apply the closed-set LDP upper bound to the finite compact-core cover and take the finite maximum.", "planned compact-core LDP upper estimate", "The correct variational upper bound on a finite sublevel.", "critical", "required"),
    ("L-TAIL-UPPER", "core_lemma", "Use boundedness of F, probability mass, and goodness of I to control the complement of a large sublevel.", "planned bounded-tail exponential estimate", "A tail contribution negligible at the selected level.", "critical", "required"),
    ("T-UPPER", "terminal", "Combine compact-core and tail estimates, then pass through limsup and remove the truncation level.", "planned global limsup upper bound", "limsup logarithmic integrals <= variational value.", "critical", "required"),
    ("T-LIMIT-MERGE", "terminal", "Merge the matching EReal liminf and limsup bounds into Tendsto atTop to the variational value.", "planned EReal liminf/limsup convergence theorem", "The exact terminal integral-lemma proposition.", "critical", "required"),
    ("T-ROOT-TRANSPORT", "transport", "Transport the exact terminal result to the public canonical target without changing any binder or hypothesis.", "Stage1Instances.THM_M_1061.ObligationTree.root_of_integralLemmaTerminal", "The exact public root, conditional on the open terminal package.", "high", "required"),
    ("X-SOURCE", "terminal", "Map every material lower, upper, compactness, tail, and limit step to reviewed primary-source passages and conventions.", "planned primary-source node crosswalk", "Human-source coverage only.", "high", "required"),
    ("X-PROVENANCE", "certificate", "Inventory terminal bodies, imports, wrappers, axioms, TCB, and replay evidence without duplicating proof credit.", "planned provenance and trust packet", "Release provenance overlay only.", "critical", "not_applicable"),
]

PROOF_CHILDREN = {
    "ROOT": ["T-ROOT-TRANSPORT"],
    "T-ROOT-TRANSPORT": ["T-LIMIT-MERGE"],
    "T-LIMIT-MERGE": ["T-LOWER", "T-UPPER", "N-VARIATIONAL"],
    "T-LOWER": ["L-LOWER-LOCAL", "N-VARIATIONAL", "S-BOUNDARIES"],
    "T-UPPER": ["C-COMPACT-COVER", "L-CORE-UPPER", "L-TAIL-UPPER", "N-VARIATIONAL", "S-BOUNDARIES"],
    "L-LOWER-LOCAL": ["S-DEFINITIONS"],
    "C-COMPACT-COVER": ["S-DEFINITIONS"],
    "L-CORE-UPPER": ["C-COMPACT-COVER"],
    "L-TAIL-UPPER": ["S-DEFINITIONS", "S-BOUNDARIES"],
}

def oid(short): return PREFIX + short
def sha(value): return hashlib.sha256(value).hexdigest()
def graph(edges):
    out, incoming = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e["edge_id"])
        incoming.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}
def edge(eid, source, target, typ, reciprocal=None):
    result = {"edge_id": eid, "from": oid(source), "to": oid(target), "type": typ}
    if reciprocal: result["reciprocal_edge_id"] = reciprocal
    return result

def main():
    statement_hash = sha((HERE / "Statement.lean").read_bytes())
    anchor_hash = sha((HERE / "anchor-audit.json").read_bytes())
    obligations, nodes = [], []
    for short, kind, human, formal, output, risk, source_eligibility in ROWS:
        machine = "informational" if short in {"X-SOURCE", "X-PROVENANCE"} else "required"
        fingerprint = ("lean-file-sha256:" + statement_hash) if short in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + sha(f"{oid(short)}\n{human}\n{formal}".encode())
        obligations.append({
            "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
            "root_relevant": True, "machine_eligibility": machine,
            "human_source_eligibility": source_eligibility, "readable_eligibility": "required",
            "risk_class": risk, "exclusion_reason": "source_or_provenance_overlay_no_machine_credit" if machine == "informational" else None,
            "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1061/ObligationTree.lean#root_of_integralLemmaTerminal" if short == "T-ROOT-TRANSPORT" else None,
        })
        children = PROOF_CHILDREN.get(short, [])
        checked = short in {"S-DEFINITIONS", "T-ROOT-TRANSPORT"}
        nodes.append({
            "node_id": f"{THEOREM}-{short}", "obligation_id": oid(short), "kind": kind,
            "human_statement": human, "formal_target": formal, "output": output,
            "human_debt": "H1", "machine_debt": "M0-L" if checked else ("M3" if short == "ROOT" else "M4"), "readability_debt": "R3",
            "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if source_eligibility == "required" else "not-applicable",
            "provenance_id": "local-conditional-composition" if short == "T-ROOT-TRANSPORT" else "none",
            "foundation_profile": "lean4-mathlib-classical/noncomputable-policy-audit-pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
            "computation_record": "none; no oracle or external computation supplies proof credit",
            "step_budget": "split-required" if children else 40,
            "semantic_step_ledger": {"premises": ", ".join(oid(c) for c in children) if children else "Exact frozen context", "inference": human, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
            "public_readable_target": f"Stage1_Instances/THM-M-1061/obligation-tree.md#{oid(short).lower()}",
            "validation_spec_id": f"VAL-{oid(short)}", "status_boundary": "Frozen architecture or checked conditional interface only; no open proof is claimed.",
            "task_ids": [ITEM, "S56-M-1061-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1061/ObligationTree.lean"] if short == "T-ROOT-TRANSPORT" else [],
            "owner": "THM-M-1061 proof lane", "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-12" if checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if checked else "open"},
        })
    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    digest = sha(json.dumps([{k: o[k] for k in fields} for o in obligations], sort_keys=True, separators=(",", ":")).encode())
    ids = [o["obligation_id"] for o in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
        "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact elaborated statement and bounded immutable anchor audit; eligibility frozen before proof-phase status inspection.",
        "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"), "denominator_sha256": digest,
        "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [oid("X-SOURCE"), oid("X-PROVENANCE")]},
        "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version with append-only old/new ID delta.",
        "obligations": obligations, "append_only_delta": [],
        "status_observed_after_freeze": {"closed_obligations": [oid("S-DEFINITIONS"), oid("T-ROOT-TRANSPORT")], "root_machine_debt": "M3"},
        "status_boundary": "Architecture only; no Varadhan proof, H0, M0 root, validation, release, or theorem completion.",
    }
    proof, n = [], 1
    for parent, children in PROOF_CHILDREN.items():
        for child in children:
            req, comp = f"M1061-PROOF-{n:02d}R", f"M1061-PROOF-{n:02d}C"
            proof += [edge(req, parent, child, "proof_requires", comp), edge(comp, child, parent, "composes", req)]
            n += 1
    graphs = {
        "proof": graph(proof),
        "refinement": graph([edge("M1061-REF-01", "ROOT", "S-DEFINITIONS", "logical_decomposition"), edge("M1061-REF-02", "ROOT", "S-BOUNDARIES", "logical_decomposition"), edge("M1061-REF-03", "ROOT", "S-FOUNDATION", "logical_decomposition")]),
        "provenance": graph([edge("M1061-PROV-01", "X-PROVENANCE", "ROOT", "provenance_of"), edge("M1061-PROV-02", "L-LOWER-LOCAL", "X-SOURCE", "source_map"), edge("M1061-PROV-03", "T-UPPER", "X-SOURCE", "source_map")]),
        "evidence": graph([]),
        "trust": graph([edge("M1061-TRUST-01", "ROOT", "S-FOUNDATION", "trusts"), edge("M1061-TRUST-02", "ROOT", "X-PROVENANCE", "trusts")]),
        "documentation": graph([edge("M1061-DOC-01", "X-SOURCE", "T-LOWER", "documents"), edge("M1061-DOC-02", "X-SOURCE", "T-UPPER", "documents")]),
        "workflow": graph([edge("M1061-FLOW-01", "T-LIMIT-MERGE", "T-LOWER", "workflow_depends_on"), edge("M1061-FLOW-02", "T-LIMIT-MERGE", "T-UPPER", "workflow_depends_on"), edge("M1061-FLOW-03", "X-PROVENANCE", "T-ROOT-TRANSPORT", "workflow_depends_on")]),
    }
    bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-1061-OBLIGATIONS-v1", "registry_denominator_sha256": digest, "root_node_id": oid("ROOT"), "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent.", "nodes": nodes, "graphs": graphs, "closure_boundary": {"closed_obligations": [oid("S-DEFINITIONS"), oid("T-ROOT-TRANSPORT")], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [oid("T-LIMIT-MERGE")], "composition_certificates": ["Stage1Instances.THM_M_1061.ObligationTree.root_of_integralLemmaTerminal"], "root_machine_debt": "M3"}}
    recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid(short)}", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1061/check_obligation_tree.py"], "network_policy": "denied", "expected_exit": 0, "covered_obligation_ids": [oid(short)]} for short, *_ in ROWS], "status_boundary": "Structural validation and conditional composition only."}
    for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    print(digest)

if __name__ == "__main__": main()
