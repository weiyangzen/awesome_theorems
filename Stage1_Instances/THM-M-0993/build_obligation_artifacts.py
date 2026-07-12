#!/usr/bin/env python3
"""Build THM-M-0993 registry version 1 and its typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0993-OBLIGATION_TREE"
PREFIX = "M0993-"

# short id, kind, risk, human statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "The exact frozen finite-family product-form Chernoff upper-tail bound.", "Stage1Instances.THM_M_0993.ObligationTree.Root", "The canonical probability inequality.", "H1", "M1", "R3", 8),
    ("S-EXACT", "definition", "high", "Preserve universes, binders, positive tilt, measurability, independence, integrability, event, and product conclusion.", "Stage1Instances.THM_M_0993.ChernoffUpperTailTarget", "The exact statement boundary.", "H1", "M3", "R3", 12),
    ("L-SUM-INT", "bridge", "high", "Derive integrability of the exponential of the finite random sum.", "iIndepFun.integrable_exp_mul_sum", "Integrability needed by exponential Markov.", "H1", "M1", "R3", 18),
    ("L-MARKOV", "core_lemma", "critical", "Apply exponential Markov to the non-strict upper-tail event at nonnegative tilt.", "measure_ge_le_exp_mul_mgf", "The unfactored MGF upper bound.", "H1", "M1", "R3", 18),
    ("L-FACTOR", "core_lemma", "critical", "Factor the MGF of the independent finite sum into individual exponential integrals.", "iIndepFun.mgf_sum", "The product of individual tilted moments.", "H1", "M1", "R3", 20),
    ("T-ASSEMBLE", "terminal", "critical", "Compose sum integrability, exponential Markov, and MGF factorization without changing the event or constants.", "Stage1Instances.THM_M_0993.ObligationTree.root_compose", "The exact canonical root conditional on three interfaces.", "H1", "M1", "R3", 10),
    ("B-EMPTY", "branch", "medium", "Retain the empty finite family and its zero sum as an included boundary case.", "Stage1Instances.THM_M_0993.empty_family_sum", "Empty-family coverage.", "H1", "M3", "R3", 8),
    ("X-PINNED", "provenance", "critical", "Pin the three terminal mathlib bodies and prevent wrapper or alias double counting.", "mathlib 8a178386: Probability.Moments.Basic", "Immutable terminal-body provenance.", "H1", "M1", "R3", 12),
    ("X-SOURCE", "source", "high", "Pinpoint and review a primary human proof, all assumptions, and errata.", "primary-source theorem/page remains open", "Human-source coverage of the mathematical leaves.", "H1", "M5", "R4", 18),
    ("X-TCB", "trust", "high", "Audit transitive kernel, mathlib, axiom, and executable trust closure.", "Lean 4.29.0; mathlib 8a178386", "Release-grade trust inventory.", "H1", "M3", "R4", 18),
]

def oid(short): return PREFIX + short

statement = json.loads((HERE / "statement.json").read_text())
expr_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
overlays = {"X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "B-EMPTY", "X-TCB"}
body_ids = {
    "L-SUM-INT": "mathlib:8a178386:ProbabilityTheory.iIndepFun.integrable_exp_mul_sum",
    "L-MARKOV": "mathlib:8a178386:ProbabilityTheory.measure_ge_le_exp_mul_mgf",
    "L-FACTOR": "mathlib:8a178386:ProbabilityTheory.iIndepFun.mgf_sum",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0993.ObligationTree.root_compose",
}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fp = "lean-expression-sha256:" + expr_hash if short in {"ROOT", "S-EXACT"} else "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest()
    rows.append({"obligation_id": oid(short), "statement_fingerprint": fp, "kind": kind,
        "root_relevant": short not in overlays,
        "machine_eligibility": "informational" if short in overlays else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": body_ids.get(short)})
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in rows]
denom = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r["obligation_id"] for r in rows]
registry = {"schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-0993", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "The elaborated product-form statement and immutable anchor audit determine the exact Markov/factorization architecture before proof closure is observed.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denom,
    "frozen_denominators": {"inventory": ids, "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"], "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"]},
    "delta_policy": "Any correction, split, merge, eligibility/exclusion/risk change requires registry version 2 and an append-only old/new ID delta.", "obligations": rows}

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({"node_id": "THM-M-0993-" + short, "obligation_id": oid(short), "kind": kind, "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [], "source_crosswalk_id": "SRC-M0993-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0993-MATHLIB-CHERNOFF" if short in {"L-SUM-INT", "L-MARKOV", "L-FACTOR", "X-PINNED"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; observed candidate axioms: propext, Classical.choice, Quot.sound", "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open", "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0993/obligation-tree.md#" + short.lower(), "validation_spec_id": "VAL-M0993-" + short,
        "status_boundary": "Architecture only; no accepted closure credit is assigned in this phase.", "task_ids": [ITEM, "S56-M-0993-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0993/obligation-registry.json", "Stage1_Instances/THM-M-0993/typed-graphs.json"], "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"}})

def graph(edges):
    out, incoming = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "L-SUM-INT"), ("T-ASSEMBLE", "L-MARKOV"), ("T-ASSEMBLE", "L-FACTOR")]
proof_edges = []
for parent, child in proof_pairs:
    f, r = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges += [{"edge_id": f, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": r}, {"edge_id": r, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": f}]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": "REFINE-ROOT-EXACT", "from": oid("ROOT"), "type": "logical_decomposition", "to": oid("S-EXACT")}, {"edge_id": "REFINE-EXACT-EMPTY", "from": oid("S-EXACT"), "type": "logical_decomposition", "to": oid("B-EMPTY")}]),
    "provenance": graph([{"edge_id": "PROV-" + s, "from": oid(s), "type": "provenance_of", "to": oid("X-PINNED")} for s in ("L-SUM-INT", "L-MARKOV", "L-FACTOR")] + [{"edge_id": "SOURCE-" + s, "from": oid(s), "type": "source_map", "to": oid("X-SOURCE")} for s in ("ROOT", "L-MARKOV", "L-FACTOR")]),
    "evidence": graph([{"edge_id": "EVID-ROOT-PINNED", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-PINNED")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}, {"edge_id": "FLOW-ASSEMBLE-PINNED", "from": oid("T-ASSEMBLE"), "type": "workflow_depends_on", "to": oid("X-PINNED")}]),
}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0993", "registry_denominator_sha256": denom, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M1", "remaining_root_cut_set": [oid("L-SUM-INT"), oid("L-MARKOV"), oid("L-FACTOR")], "composition_certificates_checked": ["Stage1Instances.THM_M_0993.ObligationTree.root_compose"], "audit_complete": False, "theorem_complete": False}}
recipes = [{"recipe_id": "VAL-M0993-" + s[0], "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0993/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid(s[0])]} for s in SPECS]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0993", "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denom}")
