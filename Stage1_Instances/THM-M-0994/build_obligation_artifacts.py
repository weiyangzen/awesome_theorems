#!/usr/bin/env python3
"""Build the THM-M-0994 v1 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0994-OBLIGATION_TREE"
THEOREM = "THM-M-0994"
PREFIX = "M0994-"

# short id, kind, risk, statement, formal target, output, H/M/R, step budget
SPECS = [
    ("ROOT", "root", "critical", "The exact frozen finite-family one-sided Hoeffding inequality.", "Stage1Instances.THM_M_0994.ObligationTree.Root", "The canonical sharp upper-tail inequality.", "H2", "M1", "R3", 8),
    ("S-EXACT", "definition", "high", "Preserve universes, binders, measurability, independence, almost-sure interval bounds, centered event, and denominator.", "Stage1Instances.THM_M_0994.HoeffdingTarget", "The exact statement boundary.", "H2", "M3", "R3", 12),
    ("L-CENTER", "bridge", "high", "Transport independence through coordinatewise centering by each expectation.", "iIndepFun.comp", "Independence of the centered family.", "H2", "M1", "R3", 16),
    ("L-INTERVAL-MGF", "core_lemma", "critical", "Apply Hoeffding's lemma to each measurable almost-sure interval-bounded coordinate.", "ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc", "A subgaussian MGF certificate for every centered coordinate.", "H2", "M1", "R3", 20),
    ("L-SUM-TAIL", "core_lemma", "critical", "Compose centered independence and coordinate MGF certificates into mathlib's finite-sum upper-tail bound.", "ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun", "The tail bound using the NNReal variance proxy.", "H2", "M1", "R3", 20),
    ("L-ENDPOINTS", "bridge", "high", "Derive a_i <= b_i from the almost-sure nonempty interval under a probability measure.", "Stage1Instances.THM_M_0994.ObligationTree.root_compose", "Ordered endpoints for every coordinate.", "H2", "M0-L", "R3", 10),
    ("L-PROXY-ALG", "bridge", "critical", "Normalize nnnorm, division by two, coercions, squares, and the exponent constant.", "Stage1Instances.THM_M_0994.ObligationTree.ProxyTransportInterface", "Proxy-to-exact exponent inequality when total width is positive.", "H2", "M2", "R3", 28),
    ("B-ZERO-WIDTH", "branch", "critical", "Handle empty families and zero total squared width without adding a positivity hypothesis.", "Stage1Instances.THM_M_0994.ObligationTree.ProxyTransportInterface", "Exact denominator-zero boundary, whose right side is exp 0.", "H2", "M2", "R3", 18),
    ("T-PROXY", "terminal", "critical", "Package the three pinned mathlib steps as the proxy-bound interface without wrapper double counting.", "Stage1Instances.THM_M_0994.ObligationTree.ProxyBoundInterface", "The checked candidate's NNReal-proxy inequality.", "H2", "M1", "R3", 12),
    ("T-ASSEMBLE", "terminal", "critical", "Compose proxy closure, endpoint order, algebra, and the zero-width branch into the exact root.", "Stage1Instances.THM_M_0994.ObligationTree.root_compose", "The exact root conditional on the proxy and transport interfaces.", "H2", "M1", "R3", 10),
    ("X-PINNED", "provenance", "critical", "Pin terminal mathlib bodies, the local wrapper, revisions, imports, and alias deduplication.", "mathlib 8a178386: Mathlib.Probability.Moments.SubGaussian", "Immutable proof-body provenance.", "H2", "M1", "R3", 14),
    ("X-SOURCE", "source", "high", "Pinpoint and review Hoeffding 1963 Theorem 2, assumptions, proof steps, and errata.", "primary source stable scan remains open", "Human-source coverage of all mathematical leaves.", "H2", "M5", "R4", 20),
    ("X-TCB", "trust", "high", "Audit transitive imports, axioms, toolchain, licenses, and replay environment.", "Lean 4.29.0; mathlib 8a178386", "Release-grade trust inventory.", "H2", "M3", "R4", 18),
]

def oid(short): return PREFIX + short
def sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

statement = json.loads((HERE / "statement.json").read_text())
expr_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
overlays = {"X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "L-ENDPOINTS", "X-TCB"}
bodies = {
    "L-INTERVAL-MGF": "mathlib:8a178386:ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc",
    "L-SUM-TAIL": "mathlib:8a178386:ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun",
    "T-PROXY": "repo:Stage1Instances.THM_M_0994.mathlibCandidateProxy",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0994.ObligationTree.root_compose",
}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fp = "lean-expression-sha256:" + expr_hash if short in {"ROOT", "S-EXACT"} else "planned:v1:sha256:" + sha([human, formal, output])
    rows.append({"obligation_id": oid(short), "statement_fingerprint": fp, "kind": kind,
        "root_relevant": short not in overlays, "machine_eligibility": "informational" if short in overlays else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required", "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": None, "terminal_proof_body_id": bodies.get(short)})
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denom = sha([{k: row[k] for k in fields} for row in rows])
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated exact statement and immutable mathlib anchor audit determine the centered-subgaussian/proxy-transport route before proof closure is observed.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denom,
    "frozen_denominators": {"inventory": ids, "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [oid(s) for s in sorted(overlays)]},
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows, "append_only_delta": [],
    "status_observed_after_freeze": {"root_machine_debt": "M1", "root_closed": False},
    "status_boundary": "Architecture only; no exact-root proof, source acceptance, audit completion, or theorem completion."
}

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({"node_id": THEOREM + "-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output, "human_debt": hd, "machine_debt": md,
        "readability_debt": rd, "evidence_ids": [], "source_crosswalk_id": "SRC-M0994-HOEFFDING-1963-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0994-MATHLIB-HOEFFDING" if short in {"L-INTERVAL-MGF", "L-SUM-TAIL", "T-PROXY", "X-PINNED"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; observed anchor axioms: propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open", "computation_record": "none",
        "step_budget": budget, "semantic_step_ledger": {"premises": ["only typed children in the proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "only its declared typed parent or support edge"},
        "public_readable_target": "Stage1_Instances/THM-M-0994/obligation-tree.md#" + short.lower(), "validation_spec_id": "VAL-M0994-" + short,
        "status_boundary": "Frozen architecture or conditional interface only; no accepted root closure credit.", "task_ids": [ITEM, "S56-M-0994-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0994/obligation-registry.json", "Stage1_Instances/THM-M-0994/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"}})

def edge(eid, source, typ, target, reciprocal=None):
    e = {"edge_id": eid, "from": oid(source), "type": typ, "to": oid(target)}
    if reciprocal: e["reciprocal_edge_id"] = reciprocal
    return e
def graph(edges):
    out, incoming = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

requires = {"ROOT": ["T-ASSEMBLE"], "T-ASSEMBLE": ["T-PROXY", "L-ENDPOINTS", "L-PROXY-ALG", "B-ZERO-WIDTH"], "T-PROXY": ["L-CENTER", "L-INTERVAL-MGF", "L-SUM-TAIL"]}
proof = []
for parent, children in requires.items():
    for child in children:
        f, r = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
        proof += [edge(f, parent, "proof_requires", child, r), edge(r, child, "composes", parent, f)]
graphs = {
    "proof": graph(proof),
    "refinement": graph([edge("REF-ROOT-EXACT", "ROOT", "logical_decomposition", "S-EXACT"), edge("REF-ALG-ZERO", "L-PROXY-ALG", "case_refinement", "B-ZERO-WIDTH")]),
    "provenance": graph([edge("PROV-MGF", "L-INTERVAL-MGF", "provenance_of", "X-PINNED"), edge("PROV-TAIL", "L-SUM-TAIL", "provenance_of", "X-PINNED"), edge("SRC-ROOT", "ROOT", "source_map", "X-SOURCE")]),
    "evidence": graph([edge("EVID-PROXY", "T-PROXY", "evidence_for", "X-PINNED")]),
    "trust": graph([edge("TRUST-ROOT", "ROOT", "trusts", "X-TCB")]),
    "documentation": graph([edge("DOC-ROOT", "X-SOURCE", "documents", "ROOT")]),
    "workflow": graph([edge("FLOW-ROOT-ASSEMBLE", "ROOT", "workflow_depends_on", "T-ASSEMBLE"), edge("FLOW-ASSEMBLE-PIN", "T-ASSEMBLE", "workflow_depends_on", "X-PINNED")]),
}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_denominator_sha256": denom,
    "root_node_id": oid("ROOT"), "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M1", "remaining_root_cut_set": [oid("T-PROXY"), oid("L-PROXY-ALG"), oid("B-ZERO-WIDTH")], "composition_certificates_checked": ["Stage1Instances.THM_M_0994.ObligationTree.root_compose"], "audit_complete": False, "theorem_complete": False}}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [
    {"recipe_id": "VAL-M0994-" + s[0], "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0994/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid(s[0])]} for s in SPECS]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denom}")
