#!/usr/bin/env python3
"""Build the frozen THM-M-0339 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0339-OBLIGATION_TREE"
PREFIX = "M0339-"

# short id, kind, risk, human statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "Every finite complex tight frame with squared norms bounded by delta has the frozen r-part MSS partition bound.", "Stage1.THM_M_0339.MSSPartitionStatement", "The exact Corollary 1.5 proposition.", "H1", "M4", "R4", 8),
    ("S-EXACT", "definition", "high", "Fix d, m, positive r, nonnegative delta, the complex Euclidean frame, identity rank-one sum, and pointwise norm bound.", "Stage1.THM_M_0339.MSSPartitionStatement", "The exact binder and hypothesis interface.", "H1", "M3", "R3", 14),
    ("S-PARTITION", "definition", "high", "Represent the labeled partition by color : Fin m -> Fin r, permitting empty fibers.", "planned: color : Fin m -> Fin r", "The source-faithful finite partition encoding.", "H1", "M3", "R3", 12),
    ("S-BOUNDARY", "branch", "high", "Account for r positive and retain d=0, m=0, delta=0, and empty-part boundary behavior.", "planned: boundary cases of the frozen quantifiers", "An exhaustive boundary policy without added assumptions.", "H1", "M3", "R3", 18),
    ("S-FOUNDATION", "certificate", "high", "Fix the classical-choice, quotient, kernel, and pinned-mathlib trust boundary.", "#print axioms Stage1.THM_M_0339.ObligationTree.root_compose", "A versioned foundation and TCB boundary.", "H1", "M3", "R4", 12),
    ("N-OPERATORS", "normalization", "high", "Normalize source matrices u_i u_i* to positive rank-one continuous linear maps with operator norm.", "InnerProductSpace.rankOne; isPositive_rankOne_self; norm_rankOne", "A checked operator-language interface for the source proof.", "H1", "M3", "R4", 28),
    ("B-RONE", "branch", "normal", "Handle r=1 consistently with the identity-sum hypothesis and frozen numerical bound.", "planned: r = 1 branch", "The one-part boundary branch.", "H1", "M4", "R4", 24),
    ("B-RMANY", "branch", "critical", "Handle the general positive-r branch through the MSS random-vector estimate.", "planned: 1 < r branch", "The nontrivial partition branch.", "H1", "M4", "R4", 20),
    ("C-RANDOM", "construction", "critical", "Construct independent random labels and scaled vectors whose expectations sum to identity.", "planned: finite probability-space labeling construction", "A finite-support random-vector family satisfying Theorem 1.4 hypotheses.", "H1", "M4", "R4", 60),
    ("C-MCP", "construction", "critical", "Define the mixed characteristic polynomial for independent rank-one positive operators and prove its structural invariants.", "planned: mixed characteristic polynomial", "A real-rooted polynomial controlling a sampled operator norm.", "H1", "M4", "R4", 80),
    ("L-REALROOTED", "core_lemma", "critical", "Prove real-rootedness and positive-root control for the mixed characteristic polynomial.", "planned: MSS real-rootedness theorem", "Real roots with the required largest-root interpretation.", "H1", "M4", "R4", 90),
    ("L-INTERLACING", "core_lemma", "critical", "Build the interlacing family and select an outcome whose largest root is bounded by the expectation polynomial.", "planned: interlacing-family selection theorem", "A positive-probability/sample selection bridge.", "H1", "M4", "R4", 90),
    ("L-BARRIER", "core_lemma", "critical", "Establish the barrier-function estimate giving (1 + sqrt epsilon)^2 for the largest root.", "planned: MSS barrier estimate", "The quantitative spectral bound.", "H1", "M4", "R4", 90),
    ("L-THEOREM14", "bridge", "critical", "Combine random-vector hypotheses, mixed characteristic polynomials, interlacing, and the barrier estimate into MSS Theorem 1.4.", "planned: formal MSS Theorem 1.4", "A sample with the source spectral norm bound.", "H1", "M4", "R4", 45),
    ("T-COR15", "terminal", "critical", "Apply Theorem 1.4 to random labels and read a successful outcome as r partition fibers.", "planned: formal derivation of MSS Corollary 1.5", "The exact partition conclusion for arbitrary frozen inputs.", "H1", "M4", "R4", 55),
    ("T-ASSEMBLE", "terminal", "critical", "Consume the partition engine and return the exact frozen root without changing binders or constants.", "Stage1.THM_M_0339.ObligationTree.root_compose", "The exact root conditionally on the open engine.", "H1", "M3", "R3", 4),
    ("X-UPSTREAM", "terminal", "high", "Record pinned rank-one support APIs and the absence of a target-relevant terminal Lean body.", "anchor-audit.json candidates C02 and C03", "Formal provenance and integration boundary.", "H1", "M3", "R4", 20),
    ("X-SOURCE", "terminal", "high", "Map every material node to MSS arXiv:1306.3969v4 and independently check assumptions and errata.", "primary source node crosswalk remains open", "Human-source fidelity for the architecture.", "H1", "M5", "R4", 30),
    ("X-TCB", "terminal", "high", "Audit the transitive Lean, mathlib, foundation, and executable trust closure.", "Lean 4.29.0; mathlib 8a178386; release audit open", "Release-grade trust inventory.", "H1", "M3", "R4", 20),
]

def oid(short): return PREFIX + short
def planned_fp(human, formal):
    return "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest()

expression_hash = "65f33abcebfa3d3c007b923852d0f89d71c3250f72b95b8645546178813503dc"
informational = {"X-UPSTREAM", "X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "S-PARTITION", "S-BOUNDARY", "S-FOUNDATION", "X-UPSTREAM", "X-TCB"}
body_ids = {"T-ASSEMBLE": "repo:Stage1.THM_M_0339.ObligationTree.root_compose"}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    rows.append({
        "obligation_id": oid(short),
        "statement_fingerprint": "lean-expression-sha256:" + expression_hash if short in {"ROOT", "S-EXACT"} else planned_fp(human, formal),
        "kind": kind, "root_relevant": short not in informational,
        "machine_eligibility": "informational" if short in informational else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": body_ids.get(short),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-0339",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated Corollary 1.5 target and immutable anchor audit fix the statement, boundary, operator normalization, Theorem 1.4, mixed-characteristic-polynomial, interlacing, barrier, source, provenance, and trust obligations before proof-phase closure credit.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
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

recipe_ids = {oid(s[0]): "VAL-M0339-" + s[0] for s in SPECS}
nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-0339-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0339-MSS-V4-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0339-PINNED-SUPPORT" if short in {"N-OPERATORS", "X-UPSTREAM"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; classical/choice acceptance and transitive axiom audit remain open",
        "tcb_profile": "Lean 4.29.0; mathlib 8a178386; transitive release audit open",
        "computation_record": "none; no numerical root approximation or oracle is credited",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0339/obligation-tree.md#" + short.lower(),
        "validation_spec_id": recipe_ids[oid(short)],
        "status_boundary": "Architecture only; this obligation is not credited closed or accepted by this phase.",
        "task_ids": [ITEM, "S56-M-0339-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0339/obligation-registry.json", "Stage1_Instances/THM-M-0339/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })

def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "T-COR15"), ("T-COR15", "B-RONE"), ("T-COR15", "B-RMANY"), ("B-RMANY", "C-RANDOM"), ("B-RMANY", "L-THEOREM14"), ("L-THEOREM14", "C-MCP"), ("L-THEOREM14", "L-REALROOTED"), ("L-THEOREM14", "L-INTERLACING"), ("L-THEOREM14", "L-BARRIER")]
proof_edges = []
for parent, child in proof_pairs:
    fwd, rev = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges += [{"edge_id": fwd, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": rev}, {"edge_id": rev, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": fwd}]
refinement_pairs = [("ROOT", "S-EXACT"), ("S-EXACT", "S-PARTITION"), ("S-EXACT", "S-BOUNDARY"), ("S-EXACT", "S-FOUNDATION"), ("ROOT", "N-OPERATORS"), ("T-COR15", "B-RONE"), ("T-COR15", "B-RMANY")]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refinement_pairs]),
    "provenance": graph([{"edge_id": "PROV-N-OPERATORS", "from": oid("N-OPERATORS"), "type": "provenance_of", "to": oid("X-UPSTREAM")}, {"edge_id": "SOURCE-ROOT", "from": oid("ROOT"), "type": "source_map", "to": oid("X-SOURCE")}, {"edge_id": "SOURCE-T14", "from": oid("L-THEOREM14"), "type": "source_map", "to": oid("X-SOURCE")}]),
    "evidence": graph([{"edge_id": "EVID-ROOT-UPSTREAM", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-UPSTREAM")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}, {"edge_id": "FLOW-ASSEMBLE-COR15", "from": oid("T-ASSEMBLE"), "type": "workflow_depends_on", "to": oid("T-COR15")}]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0339",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M4", "remaining_root_cut_set": [oid("L-THEOREM14")], "composition_certificates_checked": ["Stage1.THM_M_0339.ObligationTree.root_compose"], "audit_complete": False, "theorem_complete": False},
}
recipes = [{"recipe_id": rid, "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0339/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [ob]} for ob, rid in recipe_ids.items()]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0339", "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
