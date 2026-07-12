#!/usr/bin/env python3
"""Build the frozen THM-M-0990 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0990-OBLIGATION_TREE"
PREFIX = "M0990-"

# short id, kind, risk, human statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "The exact frozen Lyapunov triangular-array CLT.", "Stage1Instances.THM_M_0990.StatementShape", "Convergence in distribution of normalized centered row sums to N(0,1).", "H2", "M3", "R4", 8),
    ("S-EXACT", "definition", "critical", "Preserve all universes, measures, binders, moments, independence, positivity, Lyapunov limit, and conclusion.", "Stage1Instances.THM_M_0990.StatementShape", "The exact statement boundary.", "H2", "M3", "R3", 18),
    ("S-BOUNDARY", "branch", "high", "Respect n = 0 totalized inverses and use eventual positive row variance only on an atTop tail.", "eventually 0 < rowVarianceSum; Nat includes zero", "A valid asymptotic tail policy.", "H2", "M3", "R3", 18),
    ("S-FOUNDATION", "certificate", "high", "Freeze kernel, classical/noncomputable, imported theorem, and dependency trust boundaries.", "#print axioms root_compose", "The foundation and TCB boundary.", "H2", "M3", "R4", 12),
    ("N-CENTER", "normalization", "high", "Center each array entry and establish zero expectation.", "centered P X n k", "Centered row variables.", "H2", "M3", "R4", 30),
    ("N-VARIANCE", "normalization", "critical", "Identify the centered row variance sum and normalize it to one on the positive tail.", "rowScale P X n = sqrt (rowVarianceSum P X n)", "Unit total variance after scaling.", "H2", "M3", "R4", 42),
    ("L-MOMENT-TRANSPORT", "core_lemma", "critical", "Derive the required centered second moments and 2+delta bounds from the frozen hypotheses.", "MemLp and Integrable rpow hypotheses", "Finite moments for normalized entries.", "H2", "M3", "R4", 48),
    ("L-INDEPENDENCE", "core_lemma", "critical", "Restrict joint independence of each infinite row to range n and transport it through centering and scaling.", "iIndepFun (X n) P", "Independent normalized finite rows.", "H2", "M3", "R4", 36),
    ("L-LYAPUNOV-INF", "core_lemma", "critical", "Use the Lyapunov ratio limit to prove the normalized triangular array is infinitesimal and controls Taylor remainders.", "Tendsto (lyapunovRatio P X delta) atTop (nhds 0)", "Uniformly negligible row summands and remainder sum.", "H2", "M3", "R4", 68),
    ("L-CHARFUN-ENTRY", "core_lemma", "critical", "Expand each centered normalized entry characteristic function to second order with a Lyapunov remainder.", "MeasureTheory.taylor_charFun_two plus a 2+delta remainder estimate", "One-entry characteristic-function expansion.", "H2", "M3", "R4", 76),
    ("L-CHARFUN-PRODUCT", "core_lemma", "critical", "Factor each row-sum characteristic function using finite-row independence.", "iIndepFun.charFun_map_fun_finset_sum_eq_prod", "Product formula for the normalized row sum.", "H2", "M3", "R4", 42),
    ("L-PRODUCT-LIMIT", "core_lemma", "critical", "Combine unit total variance and remainder control to show the product tends to exp(-t^2/2).", "finite product/logarithm asymptotics", "Pointwise convergence to the standard Gaussian characteristic function.", "H2", "M3", "R4", 88),
    ("L-LEVY", "bridge", "critical", "Convert pointwise characteristic-function convergence into convergence in distribution.", "ProbabilityMeasure.tendsto_iff_tendsto_charFun", "Distributional convergence to a law with the Gaussian characteristic function.", "H2", "M3", "R4", 44),
    ("L-GAUSSIAN", "transport", "high", "Use HasLaw Y (gaussianReal 0 1) P' to identify the selected target variable and measure.", "HasLaw Y (gaussianReal 0 1) P'", "The exact TendstoInDistribution target.", "H2", "M3", "R4", 28),
    ("T-TRIANGULAR-BRIDGE", "terminal", "critical", "Assemble the normalized triangular-array characteristic-function proof.", "planned repository proof body; no exact pinned terminal exists", "The exact frozen root proposition.", "H2", "M3", "R4", 54),
    ("T-ASSEMBLE", "terminal", "critical", "Consume the exact triangular-array bridge and return the canonical root.", "Stage1Instances.THM_M_0990.ObligationTree.root_compose", "The exact root, conditional on the open bridge.", "H2", "M3", "R3", 6),
    ("X-SOURCE", "terminal", "high", "Pinpoint and independently review a primary proof, conventions, assumptions, and errata.", "primary-source crosswalk remains open", "Human-source coverage of all material proof nodes.", "H2", "M5", "R4", 24),
    ("X-TCB", "terminal", "high", "Audit transitive Lean, mathlib, axiom, executable, and replay trust closure.", "Lean 4.29.0; mathlib 8a178386; release audit open", "Release-grade trust inventory.", "H2", "M3", "R4", 20),
]

def oid(short):
    return PREFIX + short

informational = {"X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "S-BOUNDARY", "S-FOUNDATION", "X-TCB"}
body_ids = {"T-ASSEMBLE": "repo:Stage1Instances.THM_M_0990.ObligationTree.root_compose"}
root_fp = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fp = "source-file-sha256:" + root_fp if short in {"ROOT", "S-EXACT"} else "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest()
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fp, "kind": kind,
        "root_relevant": short not in informational,
        "machine_eligibility": "informational" if short in informational else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": body_ids.get(short),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-0990",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated statement and immutable anchor audit determine the S/N/L/T/X architecture before proof closure is observed.",
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
    "delta_policy": "Any correction, split, merge, eligibility/exclusion/risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows,
}

recipe_ids = {oid(spec[0]): "VAL-M0990-" + spec[0] for spec in SPECS}
nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-0990-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0990-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0990-MATHLIB-SUPPORT" if short.startswith("L-") else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; exact axiom inventory remains a validation-phase obligation",
        "tcb_profile": "Lean 4.29.0; mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0990/obligation-tree.md#" + short.lower(),
        "validation_spec_id": recipe_ids[oid(short)],
        "status_boundary": "Architecture only; no accepted closure credit is assigned in this phase.",
        "task_ids": [ITEM, "S56-M-0990-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0990/obligation-registry.json", "Stage1_Instances/THM-M-0990/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })

def graph(edges):
    outgoing, incoming = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "T-TRIANGULAR-BRIDGE"),
    ("T-TRIANGULAR-BRIDGE", "L-LEVY"), ("T-TRIANGULAR-BRIDGE", "L-GAUSSIAN")]
proof_edges = []
for parent, child in proof_pairs:
    forward, reverse = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges.extend([
        {"edge_id": forward, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": reverse},
        {"edge_id": reverse, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": forward},
    ])
refine_pairs = [("ROOT", "S-EXACT"), ("S-EXACT", "S-BOUNDARY"), ("S-EXACT", "S-FOUNDATION"),
    ("T-TRIANGULAR-BRIDGE", "N-CENTER"), ("T-TRIANGULAR-BRIDGE", "N-VARIANCE"),
    ("T-TRIANGULAR-BRIDGE", "L-MOMENT-TRANSPORT"), ("T-TRIANGULAR-BRIDGE", "L-INDEPENDENCE"),
    ("T-TRIANGULAR-BRIDGE", "L-LYAPUNOV-INF"), ("T-TRIANGULAR-BRIDGE", "L-CHARFUN-ENTRY"),
    ("T-TRIANGULAR-BRIDGE", "L-CHARFUN-PRODUCT"), ("T-TRIANGULAR-BRIDGE", "L-PRODUCT-LIMIT")]
material = ("N-CENTER", "N-VARIANCE", "L-MOMENT-TRANSPORT", "L-INDEPENDENCE", "L-LYAPUNOV-INF", "L-CHARFUN-ENTRY", "L-CHARFUN-PRODUCT", "L-PRODUCT-LIMIT", "L-LEVY", "L-GAUSSIAN")
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refine_pairs]),
    "provenance": graph([{"edge_id": f"PROV-{s}", "from": oid(s), "type": "provenance_of", "to": oid("T-TRIANGULAR-BRIDGE")} for s in material] + [{"edge_id": f"SOURCE-{s}", "from": oid(s), "type": "source_map", "to": oid("X-SOURCE")} for s in material]),
    "evidence": graph([{"edge_id": "EVID-ROOT-BRIDGE", "from": oid("ROOT"), "type": "evidence_for", "to": oid("T-TRIANGULAR-BRIDGE")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0990",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M3",
        "remaining_root_cut_set": [oid("T-TRIANGULAR-BRIDGE")],
        "composition_certificates_checked": ["Stage1Instances.THM_M_0990.ObligationTree.root_compose"],
        "audit_complete": False, "theorem_complete": False},
}
recipes = [{"recipe_id": rid, "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0990/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [ob]} for ob, rid in recipe_ids.items()]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0990", "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
