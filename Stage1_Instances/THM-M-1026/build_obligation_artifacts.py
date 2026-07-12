#!/usr/bin/env python3
"""Build the deterministic THM-M-1026 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1026-OBLIGATION_TREE"
THEOREM = "THM-M-1026"
PREFIX = "M1026-"

ROWS = [
    ("ROOT", "root", "The exact frozen law-level generalized central limit theorem.",
     "Stage1Instances.THM_M_1026.Statement", "The canonical stable-law/domain-of-attraction biconditional.", "critical", "required", "required"),
    ("S-DEFINITIONS", "definition", "Freeze convolution powers, affine normalization, weak convergence, probability, nondegeneracy, stability, and attraction.",
     "Stage1Instances.THM_M_1026.{convPow,normalizedLaw,WeaklyConverges,IsProbabilityLaw,IsNondegenerate,IsStableLaw,InDomainOfAttraction}", "The exact elaborated vocabulary.", "high", "not_applicable", "required"),
    ("S-BOUNDARIES", "branch", "Preserve positive scaling, all n at least two, nondegenerate limits, and the zeroth/first convolution conventions.",
     "planned exact boundary lemmas for n = 0, n = 1, 2 <= n, and 0 < a n", "All exceptional indices and excluded degeneracies are discharged.", "critical", "required", "required"),
    ("S-FOUNDATION", "certificate", "Audit imports, classical measure theory, choice, transitive axioms, and the noncomputable boundary.",
     "planned foundation/import/TCB certificate", "Accepted foundation and trust profile.", "high", "not_applicable", "required"),
    ("N-WEAK-CHARFUN", "transport", "Relate the frozen bounded-continuous-test weak convergence to mathlib's probability-measure and characteristic-function convergence interfaces.",
     "planned checked transport to ProbabilityMeasure.tendsto_iff_tendsto_charFun", "A checked weak-convergence representation usable by the analytic argument.", "critical", "required", "required"),
    ("B-NECESSITY", "branch", "Assume an attracting probability law and prove that the nondegenerate limit is stable.",
     "Stage1Instances.THM_M_1026.ObligationTree.NecessityTerminal", "The reverse implication of the frozen iff.", "critical", "required", "required"),
    ("C-BLOCK-DECOMPOSITION", "construction", "For each block size m at least two, decompose mn summands into m independent n-blocks and track both affine normalizations.",
     "planned convolution-power block and affine-map identities", "A comparison sequence for the n and mn normalized sums.", "critical", "required", "required"),
    ("L-LIMIT-COMPARISON", "core_lemma", "Use convergence of normalized sums and their fixed block convolutions to identify the limit with a positive affine normalization of its m-fold convolution.",
     "planned characteristic-function/tightness convergence-of-types theorem", "For every m >= 2, positive c and d satisfy normalizedLaw (convPow nu m) c d = nu.", "critical", "required", "required"),
    ("T-NECESSITY", "terminal", "Assemble block decomposition and limit comparison for every m at least two.",
     "Stage1Instances.THM_M_1026.ObligationTree.NecessityTerminal", "Every admitted nondegenerate normalized-sum limit is stable.", "critical", "required", "required"),
    ("B-CONVERSE", "branch", "From stability, construct an attracting probability law and normalizers.",
     "Stage1Instances.THM_M_1026.ObligationTree.ConverseTerminal", "The forward implication of the frozen iff.", "critical", "required", "required"),
    ("C-STABLE-WITNESS", "construction", "Choose the stable law itself as the summand law and choose normalizers at every convolution index, including zero and one.",
     "planned choice function from IsStableLaw plus explicit n = 0,1 values", "A probability witness and total positive scale/centering sequences.", "high", "required", "required"),
    ("L-CONSTANT-WEAK-LIMIT", "core_lemma", "Rewrite every normalized convolution power to nu and prove weak convergence of the resulting constant sequence.",
     "planned WeaklyConverges congruence and tendsto_const_nhds", "The chosen law lies in the frozen domain of attraction.", "high", "required", "required"),
    ("T-CONVERSE", "terminal", "Assemble the stable witness and its constant weak limit.",
     "Stage1Instances.THM_M_1026.ObligationTree.ConverseTerminal", "Every frozen stable law has a nonempty domain of attraction.", "critical", "required", "required"),
    ("T-BRANCH-MERGE", "transport", "Merge the exact necessity and converse propositions into the frozen biconditional without changing binders.",
     "Stage1Instances.THM_M_1026.ObligationTree.root_of_directions", "The exact public root, conditional on both complete directions.", "high", "required", "required"),
    ("X-CHARFUN-PROVENANCE", "certificate", "Record immutable provenance and trust for convolution characteristic functions and Levy convergence infrastructure.",
     "mathlib 8a178386 charFun_conv and ProbabilityMeasure.tendsto_iff_tendsto_charFun provenance", "A support-only imported boundary, not a generalized-CLT proof.", "high", "not_applicable", "required"),
    ("X-SOURCE", "terminal", "Pinpoint-map every material transition to a primary human source with assumptions and errata.",
     "planned primary-source node crosswalk", "Human-source coverage for the selected biconditional.", "high", "required", "required"),
]

PROOF_CHILDREN = {
    "ROOT": ["T-BRANCH-MERGE"],
    "T-BRANCH-MERGE": ["T-NECESSITY", "T-CONVERSE"],
    "T-NECESSITY": ["B-NECESSITY"],
    "B-NECESSITY": ["C-BLOCK-DECOMPOSITION", "L-LIMIT-COMPARISON"],
    "C-BLOCK-DECOMPOSITION": ["S-DEFINITIONS", "S-BOUNDARIES"],
    "L-LIMIT-COMPARISON": ["C-BLOCK-DECOMPOSITION", "N-WEAK-CHARFUN"],
    "N-WEAK-CHARFUN": ["S-DEFINITIONS"],
    "T-CONVERSE": ["B-CONVERSE"],
    "B-CONVERSE": ["C-STABLE-WITNESS", "L-CONSTANT-WEAK-LIMIT"],
    "C-STABLE-WITNESS": ["S-DEFINITIONS", "S-BOUNDARIES"],
    "L-CONSTANT-WEAK-LIMIT": ["C-STABLE-WITNESS"],
}

def oid(short): return PREFIX + short

def planned_hash(short, statement, formal):
    return "planned:v1:sha256:" + hashlib.sha256(f"v1\n{oid(short)}\n{statement}\n{formal}".encode()).hexdigest()

def graph(edges):
    out, incoming = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e["edge_id"])
        incoming.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

def edge(group, number, source, target, kind, reciprocal=None):
    e = {"edge_id": f"M1026-{group.upper()}-{number:02d}", "from": oid(source), "to": oid(target), "type": kind}
    if reciprocal: e["reciprocal_edge_id"] = reciprocal
    return e

def main():
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations, nodes = [], []
    for short, kind, human, formal, output, risk, human_elig, readable in ROWS:
        fingerprint = "lean-file-sha256:" + statement_hash if short in {"ROOT", "S-DEFINITIONS"} else planned_hash(short, human, formal)
        machine = "informational" if short.startswith("X-") else "required"
        obligations.append({
            "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
            "root_relevant": True, "machine_eligibility": machine,
            "human_source_eligibility": human_elig, "readable_eligibility": readable,
            "risk_class": risk, "exclusion_reason": "provenance_or_human_source_boundary_only" if machine == "informational" else None,
            "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1026/ObligationTree.lean#root_of_directions" if short == "T-BRANCH-MERGE" else None,
        })
        children = PROOF_CHILDREN.get(short, [])
        checked = short in {"S-DEFINITIONS", "T-BRANCH-MERGE"}
        nodes.append({
            "node_id": f"{THEOREM}-{short}", "obligation_id": oid(short), "kind": kind,
            "human_statement": human, "formal_target": formal, "output": output,
            "human_debt": "H2", "machine_debt": "M0-L" if checked else ("M3" if short == "ROOT" else "M4"),
            "readability_debt": "R4", "evidence_ids": [],
            "source_crosswalk_id": "anchor-audit-charfun-levy" if short in {"N-WEAK-CHARFUN", "X-CHARFUN-PROVENANCE"} else ("primary-source-node-map-pending" if human_elig == "required" else "not-applicable"),
            "provenance_id": "S56-M-1026-C02+C03" if short in {"N-WEAK-CHARFUN", "X-CHARFUN-PROVENANCE"} else ("local-obligation-tree-composition" if short == "T-BRANCH-MERGE" else "none"),
            "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
            "computation_record": "none; no oracle or external computation supplies proof credit",
            "step_budget": "split-required" if children else 40,
            "semantic_step_ledger": {"premises": ", ".join(map(oid, children)) if children else "Exact frozen context", "inference": human, "output": output, "outgoing_use": "Only declared proof/composition edges may consume this output."},
            "public_readable_target": f"Stage1_Instances/THM-M-1026/obligation-tree.md#{oid(short).lower()}",
            "validation_spec_id": f"VAL-{oid(short)}",
            "status_boundary": "Architecture or checked conditional interface only; no open mathematical proof is credited.",
            "task_ids": [ITEM, "S56-M-1026-PROOF"],
            "owned_sources": ["Stage1_Instances/THM-M-1026/ObligationTree.lean"] if short == "T-BRANCH-MERGE" else [],
            "owner": "THM-M-1026 proof lane", "reviewer": "independent Stage1 integration lane",
            "validity": {"validated_at": "2026-07-12" if checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if checked else "open"},
        })
    fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
    projection = [{k: r[k] for k in fields} for r in obligations]
    digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    ids = [r["obligation_id"] for r in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
        "freeze_basis": "Exact elaborated statement and bounded immutable anchor audit; eligibility frozen before proof-phase closure inspection.",
        "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"), "denominator_sha256": digest,
        "frozen_denominators": {"inventory": ids, "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"], "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"], "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"]},
        "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version with an append-only old/new ID delta.",
        "obligations": obligations,
    }
    proof, number = [], 1
    for parent, children in PROOF_CHILDREN.items():
        for child in children:
            rid, cid = f"M1026-PROOF-{number:02d}R", f"M1026-PROOF-{number:02d}C"
            a, b = edge("proof", number, parent, child, "proof_requires", cid), edge("proof", number, child, parent, "composes", rid)
            a["edge_id"], b["edge_id"] = rid, cid
            proof.extend([a, b]); number += 1
    refinement = [edge("refine", 1, "ROOT", "S-DEFINITIONS", "logical_decomposition"), edge("refine", 2, "ROOT", "S-BOUNDARIES", "logical_decomposition"), edge("refine", 3, "ROOT", "S-FOUNDATION", "logical_decomposition")]
    provenance = [edge("prov", 1, "N-WEAK-CHARFUN", "X-CHARFUN-PROVENANCE", "provenance_of")]
    evidence = [edge("evidence", 1, "T-BRANCH-MERGE", "S-FOUNDATION", "evidence_for")]
    trust = [edge("trust", 1, "ROOT", "S-FOUNDATION", "trusts"), edge("trust", 2, "N-WEAK-CHARFUN", "X-CHARFUN-PROVENANCE", "trusts")]
    documentation = [edge("docs", 1, "ROOT", "X-SOURCE", "documents"), edge("docs", 2, "ROOT", "X-CHARFUN-PROVENANCE", "documents")]
    workflow = [edge("workflow", 1, "T-NECESSITY", "X-SOURCE", "workflow_depends_on"), edge("workflow", 2, "N-WEAK-CHARFUN", "X-CHARFUN-PROVENANCE", "workflow_depends_on"), edge("workflow", 3, "ROOT", "T-BRANCH-MERGE", "workflow_depends_on")]
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_id": "THM-M-1026-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
        "root_node_id": oid("ROOT"), "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent.",
        "nodes": nodes,
        "graphs": {"proof": graph(proof), "refinement": graph(refinement), "provenance": graph(provenance), "evidence": graph(evidence), "trust": graph(trust), "documentation": graph(documentation), "workflow": graph(workflow)},
        "closure_boundary": {"closed_obligations": [oid("S-DEFINITIONS"), oid("T-BRANCH-MERGE")], "root_closed": False, "theorem_complete": False, "remaining_root_cut_set": [oid("T-NECESSITY"), oid("T-CONVERSE")], "root_machine_debt": "M3"},
    }
    recipes = [{"recipe_id": f"VAL-{oid(short)}", "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1026/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1026 obligation tree"}], "covered_obligation_ids": [oid(short)], "covered_declarations": [formal] if formal.startswith("Stage1Instances.") else []} for short, _, _, formal, _, _, _, _ in ROWS]
    specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes, "status_boundary": "Structural recipes validate the frozen architecture and conditional branch merge, not either open generalized-CLT direction."}
    for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
        (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

if __name__ == "__main__": main()
