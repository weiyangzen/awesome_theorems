#!/usr/bin/env python3
"""Build the frozen THM-M-1270 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1270-OBLIGATION_TREE"
PREFIX = "M1270-"

# short id, kind, risk, human statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "The exact real-valued two-parameter Ekeland variational principle.", "Stage1Instances.THM_M_1270.EkelandVariationalPrincipleTarget", "The frozen canonical proposition.", "H1", "M3", "R4", 8),
    ("S-EXACT", "definition", "high", "Fix the complete metric, lower-semicontinuous, bounded-below, positive-parameter, approximate-minimizer context.", "Stage1Instances.THM_M_1270.EkelandVariationalPrincipleTarget", "The exact ordered binder and hypothesis boundary.", "H1", "M3", "R3", 14),
    ("S-BOUNDARY", "branch", "high", "Exclude epsilon or lambda equal to zero and retain the strict conclusion only for y distinct from v.", "0 < epsilon; 0 < lambda; y != v", "A denominator-safe and nonreflexive strictness boundary.", "H1", "M3", "R3", 10),
    ("S-TRANSPORT", "transport", "normal", "Transport between pointwise and infimum approximate-minimizer premises under boundedness below.", "Stage1Instances.THM_M_1270.target_iff_infimum_target", "A checked bidirectional premise-encoding transport.", "H1", "M0-L", "R3", 16),
    ("S-FOUNDATION", "certificate", "high", "Freeze the classical choice, real infimum, completeness, kernel, and dependency trust boundary.", "#print axioms root_compose and later proof declarations", "A versioned foundation and TCB boundary.", "H1", "M3", "R4", 12),
    ("N-SLOPE", "normalization", "high", "Normalize the positive penalty slope as epsilon / lambda and record its positivity.", "slope = epsilon / lambda; 0 < slope", "A positive descent coefficient used throughout the construction.", "H1", "M3", "R3", 12),
    ("C-SEQUENCE", "construction", "critical", "Recursively choose a descent sequence whose next value nearly infimizes the current descent set.", "planned: c : Nat -> X with c 0 = x0 and quantitative descent selection", "A started quantitative descent sequence.", "H1", "M3", "R4", 48),
    ("C-INVARIANTS", "construction", "critical", "Prove nested descent sets, value monotonicity, and the penalized-distance drop inequality at every step.", "planned: descent invariants for c", "The invariants needed for telescoping and maximality.", "H1", "M3", "R4", 44),
    ("L-CAUCHY", "core_lemma", "critical", "Use the lower bound and telescoping penalized drops to prove the descent sequence is Cauchy.", "planned: CauchySeq c", "Cauchy convergence eligibility in the complete metric space.", "H1", "M3", "R4", 52),
    ("L-LIMIT", "core_lemma", "critical", "Obtain the complete-space limit v and pass value and descent inequalities to it using lower semicontinuity.", "planned: exists v, Tendsto c atTop (nhds v) with limit invariants", "A limit point carrying value and descent bounds.", "H1", "M3", "R4", 58),
    ("L-LOCALIZE", "core_lemma", "critical", "Combine approximate minimality with the positive slope descent estimate to bound dist v x0 by lambda and show f v <= f x0.", "Stage1Instances.THM_M_1270.ObligationTree.ValueImprovement and Localization", "Value improvement and localization for v.", "H1", "M3", "R4", 32),
    ("L-MAXIMAL", "core_lemma", "critical", "Show every distinct y fails the terminal descent relation, giving strict penalized minimality at v.", "Stage1Instances.THM_M_1270.ObligationTree.StrictPenalizedMinimality", "The strict inequality against every y != v.", "H1", "M3", "R4", 46),
    ("T-WITNESS", "terminal", "critical", "Package the limit point with value improvement, localization, and strict penalized minimality.", "Stage1Instances.THM_M_1270.ObligationTree.WitnessPackage", "The exact existential witness package.", "H1", "M3", "R3", 10),
    ("T-ASSEMBLE", "terminal", "critical", "Consume the hard-core witness package and return the exact canonical root.", "Stage1Instances.THM_M_1270.ObligationTree.root_compose", "The exact root, conditional on the open hard core.", "H1", "M0-L", "R3", 12),
    ("X-ANCHORS", "terminal", "high", "Record immutable mathlib lower-semicontinuity, Cauchy, completeness, and infimum infrastructure without treating it as a terminal proof.", "anchor-audit.json at mathlib 8a178386", "Formal provenance boundaries for partial infrastructure.", "H1", "M3", "R4", 18),
    ("X-SOURCE", "terminal", "high", "Pinpoint and independently review Ekeland's primary proof, assumptions, constants, and errata.", "primary source crosswalk remains open", "Human-source mapping for every material proof node.", "H1", "M5", "R4", 20),
    ("X-TCB", "terminal", "high", "Audit the transitive Lean, mathlib, foundation, automation, and executable trust closure.", "Lean 4.29.0; mathlib 8a178386; transitive closure pending", "Release-grade trust inventory and axiom decision.", "H1", "M3", "R4", 20),
]

def oid(short): return PREFIX + short
def digest_text(text): return hashlib.sha256(text.encode()).hexdigest()

statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaboration_output_sha256"]
informational = {"X-ANCHORS", "X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION", "X-ANCHORS", "X-TCB"}
body_ids = {
    "S-TRANSPORT": "repo:Stage1Instances.THM_M_1270.target_iff_infimum_target",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_1270.ObligationTree.root_compose",
}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fingerprint = "lean-expression-sha256:" + expression_hash if short in {"ROOT", "S-EXACT"} else "planned:v1:sha256:" + digest_text(human + "\n" + formal)
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": short not in informational,
        "machine_eligibility": "informational" if short in informational else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": body_ids.get(short),
    })

projection_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in projection_fields} for row in rows]
denominator = digest_text(json.dumps(projection, sort_keys=True, separators=(",", ":")))
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-1270",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated target and immutable anchor audit determine the S/N/B/C/L/X/T architecture; eligibility was assigned by mathematical role without granting proof-phase closure credit.",
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

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-1270-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M1270-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M1270-PARTIAL-ANCHORS" if short in {"S-TRANSPORT", "L-CAUCHY", "L-LIMIT", "X-ANCHORS"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib foundations; classical choice permitted but transitive axiom audit open",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-1270/obligation-tree.md#" + short.lower(),
        "validation_spec_id": "VAL-M1270-" + short,
        "status_boundary": "Architecture only; this node is not credited closed or accepted by this phase.",
        "task_ids": [ITEM, "S56-M-1270-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1270/obligation-registry.json", "Stage1_Instances/THM-M-1270/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })

def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "T-WITNESS"), ("T-WITNESS", "L-LOCALIZE"), ("T-WITNESS", "L-MAXIMAL"), ("L-LOCALIZE", "L-LIMIT"), ("L-MAXIMAL", "L-LIMIT"), ("L-LIMIT", "L-CAUCHY"), ("L-LIMIT", "C-INVARIANTS"), ("L-CAUCHY", "C-INVARIANTS"), ("C-INVARIANTS", "C-SEQUENCE"), ("C-SEQUENCE", "N-SLOPE")]
proof_edges = []
for parent, child in proof_pairs:
    forward, reverse = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges += [
        {"edge_id": forward, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": reverse},
        {"edge_id": reverse, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": forward},
    ]
refinement_pairs = [("ROOT", "S-EXACT"), ("S-EXACT", "S-BOUNDARY"), ("S-EXACT", "S-TRANSPORT"), ("S-EXACT", "S-FOUNDATION"), ("ROOT", "N-SLOPE"), ("T-WITNESS", "L-LOCALIZE"), ("T-WITNESS", "L-MAXIMAL")]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refinement_pairs]),
    "provenance": graph([{"edge_id": f"PROV-{s}", "from": oid(s), "type": "provenance_of", "to": oid("X-ANCHORS")} for s in ("S-TRANSPORT", "L-CAUCHY", "L-LIMIT")] + [{"edge_id": f"SOURCE-{s}", "from": oid(s), "type": "source_map", "to": oid("X-SOURCE")} for s in ("ROOT", "C-SEQUENCE", "L-CAUCHY", "L-LIMIT", "L-MAXIMAL")]),
    "evidence": graph([{"edge_id": "EVID-ROOT-ANCHORS", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-ANCHORS")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1270",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M3", "remaining_root_cut_set": [oid("C-SEQUENCE"), oid("C-INVARIANTS"), oid("L-CAUCHY"), oid("L-LIMIT"), oid("L-LOCALIZE"), oid("L-MAXIMAL")], "composition_certificates_checked": ["Stage1Instances.THM_M_1270.ObligationTree.root_compose"], "audit_complete": False, "theorem_complete": False},
}
recipes = [{"recipe_id": "VAL-M1270-" + s[0], "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-1270/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid(s[0])]} for s in SPECS]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1270", "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
