#!/usr/bin/env python3
"""Build the frozen THM-M-0646 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0646-OBLIGATION_TREE"
PREFIX = "M0646-"

# short id, kind, risk, statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "The exact frozen upward Loewenheim-Skolem target.", "Stage1Instances.THM_M_0646.ObligationTree.Root", "An elementarily equivalent model of cardinality kappa.", "H2", "M4", "R4", 8),
    ("S-EXACT", "definition", "high", "Preserve universes, ordered binders, infinitude and all three cardinal hypotheses.", "Stage1Instances.THM_M_0646.LoewenheimSkolemTarget", "The exact statement boundary.", "H2", "M3", "R4", 12),
    ("T-ASSEMBLE", "terminal", "critical", "Apply the pinned equivalence interface and deliberately discard only the stronger source-cardinality premise.", "Stage1Instances.THM_M_0646.ObligationTree.root_compose", "The exact root conditional on the pinned interface.", "H2", "M1", "R3", 8),
    ("B-EQUIV", "bridge", "critical", "Produce exact-cardinality elementary equivalence from the directional embedding theorem.", "FirstOrder.Language.exists_elementarilyEquivalent_card_eq", "The pinned interface used by assembly.", "H2", "M1", "R3", 12),
    ("C-CARD", "case_split", "high", "Split according to whether kappa is at most or greater than the source cardinal.", "FirstOrder.Language.exists_elementaryEmbedding_card_eq", "An elementary embedding in the appropriate direction.", "H2", "M1", "R3", 14),
    ("B-DOWN", "bridge", "high", "In the small-cardinal branch construct an elementary embedding into M.", "FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_le", "N elementarily embeds into M and has cardinality kappa.", "H2", "M1", "R3", 20),
    ("B-UP", "bridge", "critical", "In the large-cardinal branch construct an elementary extension of M.", "FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge", "M elementarily embeds into N and N has cardinality kappa.", "H2", "M1", "R3", 24),
    ("L-SKOLEM", "import_boundary", "high", "Construct the downward elementary substructure containing the requested parameters.", "FirstOrder.Language.exists_elementarySubstructure_card_eq", "A small elementary substructure of exact cardinality.", "H2", "M1", "R3", 30),
    ("L-LARGE", "import_boundary", "critical", "Obtain a sufficiently large model of the elementary diagram.", "FirstOrder.Language.Theory.exists_large_model_of_infinite_model", "A large model of the elementary diagram.", "H2", "M1", "R3", 28),
    ("L-DIAGRAM", "construction", "critical", "Reduce the large elementary-diagram model and recover the elementary embedding of M.", "FirstOrder.Language.ElementaryEmbedding.ofModelsElementaryDiagram", "The upward elementary embedding.", "H2", "M1", "R3", 28),
    ("X-PINNED", "provenance", "critical", "Pin and deduplicate the terminal mathlib bodies at revision 8a178386.", "Mathlib.ModelTheory.Satisfiability and Skolem", "Immutable terminal-body provenance.", "H2", "M1", "R3", 16),
    ("X-SOURCE", "source", "high", "Pinpoint and independently review a primary human theorem, assumptions and errata.", "primary source theorem/page remains open", "Human-source coverage.", "H2", "M5", "R4", 20),
    ("X-TCB", "trust", "high", "Audit the transitive kernel, dependency, axiom and executable trust closure.", "Lean 4.29.0; mathlib 8a178386", "Release-grade trust inventory.", "H2", "M3", "R4", 20),
]

def oid(short):
    return PREFIX + short

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
overlays = {"X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "X-TCB"}
body_ids = {
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0646.ObligationTree.root_compose",
    "B-EQUIV": "mathlib:8a178386:FirstOrder.Language.exists_elementarilyEquivalent_card_eq",
    "C-CARD": "mathlib:8a178386:FirstOrder.Language.exists_elementaryEmbedding_card_eq",
    "B-DOWN": "mathlib:8a178386:FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_le",
    "B-UP": "mathlib:8a178386:FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge",
    "L-SKOLEM": "mathlib:8a178386:FirstOrder.Language.exists_elementarySubstructure_card_eq",
    "L-LARGE": "mathlib:8a178386:FirstOrder.Language.Theory.exists_large_model_of_infinite_model",
    "L-DIAGRAM": "mathlib:8a178386:FirstOrder.Language.ElementaryEmbedding.ofModelsElementaryDiagram",
}

rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fp = "lean-file-sha256:" + statement_hash if short in {"ROOT", "S-EXACT"} else "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest()
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fp, "kind": kind,
        "root_relevant": short not in overlays,
        "machine_eligibility": "informational" if short in overlays else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None, "terminal_proof_body_id": body_ids.get(short),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
denom = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": "THM-M-0646", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated upward statement and immutable anchor audit fix the pinned mathlib direction split and construction boundaries before proof closure is credited.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denom,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in rows if row["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [row["obligation_id"] for row in rows if row["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, eligibility, exclusion or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows,
}

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-0646-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd,
        "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0646-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0646-MATHLIB-LS" if short in body_ids and short != "T-ASSEMBLE" else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; observed candidate axioms: propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0646/obligation-tree.md#" + short.lower(),
        "validation_spec_id": "VAL-M0646-" + short,
        "status_boundary": "Architecture only; no accepted closure credit is assigned in this phase.",
        "task_ids": [ITEM, "S56-M-0646-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0646/obligation-registry.json", "Stage1_Instances/THM-M-0646/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })

def graph(edges):
    outgoing, incoming = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "B-EQUIV"), ("B-EQUIV", "C-CARD"), ("C-CARD", "B-DOWN"), ("C-CARD", "B-UP"), ("B-DOWN", "L-SKOLEM"), ("B-UP", "L-LARGE"), ("B-UP", "B-DOWN"), ("B-UP", "L-DIAGRAM")]
proof_edges = []
for parent, child in proof_pairs:
    forward, reverse = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges.extend([
        {"edge_id": forward, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": reverse},
        {"edge_id": reverse, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": forward},
    ])

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": "REFINE-ROOT-EXACT", "from": oid("ROOT"), "type": "logical_decomposition", "to": oid("S-EXACT")}]),
    "provenance": graph([{"edge_id": "PROV-" + short, "from": oid(short), "type": "provenance_of", "to": oid("X-PINNED")} for short in body_ids if short != "T-ASSEMBLE"] + [{"edge_id": "SOURCE-" + short, "from": oid(short), "type": "source_map", "to": oid("X-SOURCE")} for short in ("ROOT", "B-EQUIV", "C-CARD", "B-DOWN", "B-UP")]),
    "evidence": graph([{"edge_id": "EVID-ROOT-PINNED", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-PINNED")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}, {"edge_id": "FLOW-ASSEMBLE-PINNED", "from": oid("T-ASSEMBLE"), "type": "workflow_depends_on", "to": oid("X-PINNED")}]),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0646",
    "registry_denominator_sha256": denom, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M4", "remaining_root_cut_set": [oid("B-EQUIV")], "composition_certificates_checked": ["Stage1Instances.THM_M_0646.ObligationTree.root_compose"], "audit_complete": False, "theorem_complete": False},
}
recipes = [{"recipe_id": "VAL-M0646-" + spec[0], "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0646/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid(spec[0])]} for spec in SPECS]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0646", "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(item['edges']) for item in graphs.values())} typed edges")
print(f"registry denominator sha256: {denom}")
