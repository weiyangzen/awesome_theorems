#!/usr/bin/env python3
"""Deterministically build THM-M-0995 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0995-OBLIGATION_TREE"
PREFIX = "M0995-"

# short id, kind, risk, description, formal target, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "Prove the exact frozen bounded-summand upper-tail Bernstein inequality.", "Stage1Instances.THM_M_0995.ObligationTree.Root", "H2", "M3", "R4", 8),
    ("S-EXACT", "definition", "high", "Preserve all frozen binders, assumptions, event convention, constants, and totalized division boundaries.", "Stage1Instances.THM_M_0995.StatementShape", "H2", "M3", "R3", 12),
    ("L-IND-MGF", "core_lemma", "critical", "Derive the variance-sensitive Bernstein MGF bound for each centered almost-surely bounded summand.", "Stage1Instances.THM_M_0995.ObligationTree.IndividualMGFPackage", "H2", "M3", "R4", 70),
    ("L-SUM-MGF", "bridge", "critical", "Factor the independent sum MGF, sum exponent bounds, and use the variance budget.", "Stage1Instances.THM_M_0995.ObligationTree.SumMGFPackage", "H2", "M3", "R4", 45),
    ("L-CHERNOFF", "bridge", "high", "Apply exponential Markov to the exact non-strict upper-tail event.", "Stage1Instances.THM_M_0995.ObligationTree.ChernoffPackage", "H2", "M2", "R3", 30),
    ("L-OPTIMIZE", "core_lemma", "critical", "Choose the admissible tilt and verify the exact Bernstein exponent algebra.", "Stage1Instances.THM_M_0995.ObligationTree.OptimizeExponentPackage", "H2", "M3", "R4", 55),
    ("B-ZERO-DENOM", "branch", "critical", "Prove the zero-denominator case without using the unavailable positive-denominator tilt.", "Stage1Instances.THM_M_0995.ObligationTree.ZeroDenominatorPackage", "H2", "M3", "R4", 50),
    ("B-EMPTY", "branch", "medium", "Retain the empty-family case and its zero partial sum inside the root.", "Stage1Instances.THM_M_0995.emptyPartialSum", "H2", "M3", "R3", 20),
    ("T-ASSEMBLE", "terminal", "critical", "Split on the denominator and compose MGF, Chernoff, optimization, and boundary packages into the exact root.", "Stage1Instances.THM_M_0995.ObligationTree.AssemblyPackage", "H2", "M3", "R4", 35),
    ("X-MATHLIB", "provenance", "high", "Pin and audit the mathlib Chernoff, independence, variance, and Hoeffding-support bodies without counting them as an exact Bernstein proof.", "mathlib 8a178386: Probability.Moments.SubGaussian and Variance", "H2", "M2", "R3", 20),
    ("X-EXTERNAL", "provenance", "high", "Keep the mismatched HighDimProb Bernstein result isolated until an exact checked transport exists.", "HighDimProb 8d4eec8: Concentration.Bernstein", "H2", "M5", "R4", 20),
    ("X-SOURCE", "source", "high", "Pinpoint a primary human theorem, assumptions, constants, proof crosswalk, and errata.", "primary source theorem/page open", "H2", "M5", "R4", 30),
    ("X-TCB", "trust", "high", "Audit the transitive kernel, dependency, axiom, executable, and computation boundary.", "Lean 4.29.0; mathlib 8a178386", "H2", "M3", "R4", 25),
]

def oid(short):
    return PREFIX + short

statement = json.loads((HERE / "statement.json").read_text())
expr_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
overlays = {"X-MATHLIB", "X-EXTERNAL", "X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "B-EMPTY", "X-TCB"}
body_ids = {
    "L-CHERNOFF": "mathlib:8a178386:ProbabilityTheory.measure_ge_le_exp_mul_mgf",
    "B-EMPTY": "repo:Stage1Instances.THM_M_0995.emptyPartialSum",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0995.ObligationTree.root_compose",
}
rows = []
for short, kind, risk, desc, formal, hd, md, rd, budget in SPECS:
    fingerprint = ("lean-expression-sha256:" + expr_hash) if short in {"ROOT", "S-EXACT"} else (
        "planned:v1:sha256:" + hashlib.sha256((desc + "\n" + formal).encode()).hexdigest())
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": short not in overlays,
        "machine_eligibility": "informational" if short in overlays else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": body_ids.get(short),
    })
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": "THM-M-0995", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact elaborated statement and immutable anchor inventory determine this Bernstein MGF/Chernoff/optimization architecture before proof closure is observed.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, or risk change requires registry version 2 and an append-only ID delta.",
    "obligations": rows,
}

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, desc, formal, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-0995-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": desc, "formal_target": formal, "output": desc,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd,
        "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0995-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0995-MATHLIB" if short in {"L-CHERNOFF", "L-SUM-MGF", "X-MATHLIB"} else ("PROV-M0995-HIGHDIMPROB-NONEXACT" if short == "X-EXTERNAL" else "none"),
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; observed candidate axioms: propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; release-grade transitive audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": desc, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0995/obligation-tree.md#" + short.lower(),
        "validation_spec_id": "VAL-M0995-" + short,
        "status_boundary": "Frozen architecture only; no proof closure is credited by this phase.",
        "task_ids": [ITEM, "S56-M-0995-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0995/obligation-registry.json", "Stage1_Instances/THM-M-0995/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })

def graph(edges):
    outgoing, incoming = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "L-IND-MGF"), ("T-ASSEMBLE", "L-SUM-MGF"), ("T-ASSEMBLE", "L-CHERNOFF"), ("T-ASSEMBLE", "L-OPTIMIZE"), ("T-ASSEMBLE", "B-ZERO-DENOM")]
proof_edges = []
for parent, child in proof_pairs:
    forward, reverse = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges.extend([
        {"edge_id": forward, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": reverse},
        {"edge_id": reverse, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": forward},
    ])
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([
        {"edge_id": "REFINE-ROOT-EXACT", "from": oid("ROOT"), "type": "logical_decomposition", "to": oid("S-EXACT")},
        {"edge_id": "REFINE-EXACT-EMPTY", "from": oid("S-EXACT"), "type": "logical_decomposition", "to": oid("B-EMPTY")},
    ]),
    "provenance": graph([
        {"edge_id": "PROV-CHERNOFF-MATHLIB", "from": oid("L-CHERNOFF"), "type": "provenance_of", "to": oid("X-MATHLIB")},
        {"edge_id": "PROV-SUM-MATHLIB", "from": oid("L-SUM-MGF"), "type": "provenance_of", "to": oid("X-MATHLIB")},
        {"edge_id": "PROV-ROOT-EXTERNAL", "from": oid("ROOT"), "type": "provenance_of", "to": oid("X-EXTERNAL")},
        {"edge_id": "SOURCE-ROOT", "from": oid("ROOT"), "type": "source_map", "to": oid("X-SOURCE")},
        {"edge_id": "SOURCE-IND-MGF", "from": oid("L-IND-MGF"), "type": "source_map", "to": oid("X-SOURCE")},
    ]),
    "evidence": graph([{"edge_id": "EVID-ROOT-MATHLIB", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-MATHLIB")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([
        {"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")},
        {"edge_id": "FLOW-ASSEMBLE-MATHLIB", "from": oid("T-ASSEMBLE"), "type": "workflow_depends_on", "to": oid("X-MATHLIB")},
    ]),
}
cut_set = [oid(short) for short in ("L-IND-MGF", "L-SUM-MGF", "L-CHERNOFF", "L-OPTIMIZE", "B-ZERO-DENOM")]
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0995",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M3", "remaining_root_cut_set": cut_set, "composition_certificates_checked": ["Stage1Instances.THM_M_0995.ObligationTree.root_compose"], "audit_complete": False, "theorem_complete": False},
}
lean_recipe = "LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) -o Statement.olean Statement.lean && LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) ObligationTree.lean; rc=$?; rm -f Statement.olean Statement.ilean; exit $rc"
recipes = [{"recipe_id": "VAL-M0995-" + spec[0], "cwd": "Stage1_Instances/THM-M-0995", "argv": ["bash", "-lc", lean_recipe], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid(spec[0])]} for spec in SPECS]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0995", "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
