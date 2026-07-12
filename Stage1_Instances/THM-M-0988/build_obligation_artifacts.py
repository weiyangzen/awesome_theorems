#!/usr/bin/env python3
"""Build the frozen THM-M-0988 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0988-OBLIGATION_TREE"
PREFIX = "M0988-"

# short id, kind, risk, human statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "The exact frozen iid real central limit theorem, including variance zero.", "Stage1Instances.THM_M_0988.StatementShape", "The frozen TendstoInDistribution conclusion.", "H2", "M1", "R4", 8),
    ("S-EXACT", "definition", "high", "Preserve every universe, measure, probability instance, random-variable binder, hypothesis, and conclusion.", "Stage1Instances.THM_M_0988.StatementShape", "The exact binder and hypothesis boundary.", "H2", "M3", "R3", 14),
    ("S-BOUNDARY", "branch", "high", "Include variance zero and Lean's totalized inverse at n = 0.", "variance (X 0) P = 0 or != 0; n : Nat includes 0", "An exhaustive boundary policy.", "H2", "M3", "R3", 12),
    ("S-FOUNDATION", "certificate", "high", "Fix classical choice, quotient, propositional extensionality, kernel, and pinned dependency policy.", "#print axioms root_compose and imported CLT", "The foundation and trust boundary.", "H2", "M3", "R4", 12),
    ("N-CENTER", "normalization", "high", "Rewrite the centered sum as the sum of X k minus the common expectation.", "Finset.sum_sub_distrib plus IdentDistrib.integral_eq", "A centered iid family.", "H2", "M1", "R4", 24),
    ("N-SCALE", "normalization", "critical", "For nonzero variance, divide the centered family by sqrt variance and later scale the limit back.", "tendstoInDistribution_inv_sqrt_mul_var_mul_sum_sub", "A unit-variance normalized CLT and inverse transport.", "H2", "M1", "R4", 32),
    ("B-ZERO", "branch", "critical", "When variance is zero, show every coordinate is almost surely its common expectation and the normalized sum is zero.", "eq_or_ne Var[X 0; P] 0, zero branch", "Convergence to the degenerate Gaussian.", "H2", "M1", "R4", 42),
    ("B-NONZERO", "branch", "critical", "When variance is nonzero, invoke the standardized CLT and transport by multiplication with sqrt variance.", "eq_or_ne Var[X 0; P] 0, nonzero branch", "Convergence to the requested nondegenerate Gaussian.", "H2", "M1", "R4", 38),
    ("C-DEGENERATE", "construction", "high", "Construct the identically-zero limiting route and its Gaussian law in the variance-zero branch.", "tendstoInDistribution_of_identDistrib 0", "The zero-variance distributional limit.", "H2", "M1", "R4", 34),
    ("C-STANDARD", "construction", "critical", "Construct centered, variance-normalized summands and the correspondingly normalized target variable.", "fun x => (x - P[X 0]) / sqrt Var[X 0; P]", "Centered unit-variance inputs and a standard Gaussian target.", "H2", "M1", "R4", 46),
    ("L-MOMENTS", "core_lemma", "critical", "Establish integrability, zero mean, and unit second moment for the standardized reference summand.", "memLp_two_of_variance_ne_zero; variance_eq_integral", "The standardized moment premises.", "H2", "M1", "R4", 48),
    ("L-IID", "core_lemma", "high", "Transport independence and identical distribution through centering and scaling.", "iIndepFun.comp; IdentDistrib.comp", "The standardized iid premises.", "H2", "M1", "R4", 26),
    ("L-CHARFUN", "core_lemma", "critical", "Prove the standard CLT by characteristic functions and Levy convergence.", "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum", "The unit-variance distributional convergence theorem.", "H2", "M1", "R4", 58),
    ("L-TRANSPORT", "transport", "high", "Transport standardized convergence through continuous multiplication by sqrt variance.", "TendstoInDistribution.continuous_comp", "The nonzero-variance target conclusion.", "H2", "M1", "R4", 28),
    ("X-PINNED", "bridge", "critical", "Audit and consume the exact pinned mathlib terminal theorem without wrapper duplication.", "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub", "The exact frozen root proposition.", "H2", "M1", "R4", 18),
    ("T-ASSEMBLE", "terminal", "critical", "Consume the exact pinned bridge conclusion and yield the canonical root.", "Stage1Instances.THM_M_0988.ObligationTree.root_compose", "The exact canonical root, conditional on the bridge.", "H2", "M1", "R3", 6),
    ("X-SOURCE", "terminal", "high", "Pinpoint and review a primary human proof, assumptions, normalization, and errata.", "primary-source crosswalk remains open", "Human-source coverage of the material proof nodes.", "H2", "M5", "R4", 20),
    ("X-TCB", "terminal", "high", "Audit transitive Lean, mathlib, foundation, axiom, and executable trust closure.", "Lean 4.29.0; mathlib 8a178386; release audit open", "Release-grade trust inventory.", "H2", "M3", "R4", 20),
]

def oid(short): return PREFIX + short

statement = json.loads((HERE / "statement.json").read_text())
expr_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
informational = {"X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "S-BOUNDARY", "S-FOUNDATION", "X-TCB"}
body_ids = {
    "L-CHARFUN": "mathlib:8a178386:ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum",
    "X-PINNED": "mathlib:8a178386:ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0988.ObligationTree.root_compose",
}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fp = "lean-expression-sha256:" + expr_hash if short in {"ROOT", "S-EXACT", "X-PINNED"} else "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest()
    rows.append({"obligation_id": oid(short), "statement_fingerprint": fp, "kind": kind,
        "root_relevant": short not in informational,
        "machine_eligibility": "informational" if short in informational else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": body_ids.get(short)})

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r["obligation_id"] for r in rows]
registry = {"schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-0988", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated statement and immutable anchor audit determine the S/N/B/C/L/X/T architecture before proof-phase closure credit.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"]},
    "delta_policy": "Any correction, split, merge, eligibility/exclusion/risk change requires registry version 2 and an append-only old/new ID delta.", "obligations": rows}

recipe_ids = {oid(s[0]): "VAL-M0988-" + s[0] for s in SPECS}
nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({"node_id": "THM-M-0988-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output, "human_debt": hd,
        "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0988-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0988-MATHLIB-CLT" if short in {"N-CENTER", "N-SCALE", "B-ZERO", "B-NONZERO", "C-DEGENERATE", "C-STANDARD", "L-MOMENTS", "L-IID", "L-CHARFUN", "L-TRANSPORT", "X-PINNED"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; observed candidate axioms: propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0988/obligation-tree.md#" + short.lower(),
        "validation_spec_id": recipe_ids[oid(short)], "status_boundary": "Architecture only; this obligation receives no accepted closure credit in this phase.",
        "task_ids": [ITEM, "S56-M-0988-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0988/obligation-registry.json", "Stage1_Instances/THM-M-0988/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"}})

def graph(edges):
    out, incoming = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e["edge_id"]); incoming.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "X-PINNED")]
proof_edges = []
for parent, child in proof_pairs:
    f, r = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges += [{"edge_id": f, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": r}, {"edge_id": r, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": f}]
refine_pairs = [("ROOT", "S-EXACT"), ("S-EXACT", "S-BOUNDARY"), ("S-EXACT", "S-FOUNDATION"), ("X-PINNED", "B-ZERO"), ("X-PINNED", "B-NONZERO"), ("B-ZERO", "C-DEGENERATE"), ("B-NONZERO", "N-CENTER"), ("B-NONZERO", "N-SCALE"), ("B-NONZERO", "C-STANDARD"), ("C-STANDARD", "L-MOMENTS"), ("C-STANDARD", "L-IID"), ("C-STANDARD", "L-CHARFUN"), ("B-NONZERO", "L-TRANSPORT")]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a,b in refine_pairs]),
    "provenance": graph([{"edge_id": f"PROV-{s}", "from": oid(s), "type": "provenance_of", "to": oid("X-PINNED")} for s in ("B-ZERO", "B-NONZERO", "L-CHARFUN", "L-TRANSPORT")] + [{"edge_id": f"SOURCE-{s}", "from": oid(s), "type": "source_map", "to": oid("X-SOURCE")} for s in ("ROOT", "B-ZERO", "B-NONZERO", "L-CHARFUN")]),
    "evidence": graph([{"edge_id": "EVID-ROOT-PINNED", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-PINNED")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}])}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0988", "registry_denominator_sha256": denominator,
    "nodes": nodes, "graphs": graphs, "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M1",
    "remaining_root_cut_set": [oid("X-PINNED")], "composition_certificates_checked": ["Stage1Instances.THM_M_0988.ObligationTree.root_compose"], "audit_complete": False, "theorem_complete": False}}
recipes = [{"recipe_id": rid, "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0988/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [ob]} for ob, rid in recipe_ids.items()]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0988", "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
