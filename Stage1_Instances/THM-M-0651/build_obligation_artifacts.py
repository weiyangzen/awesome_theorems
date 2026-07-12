#!/usr/bin/env python3
"""Build the frozen THM-M-0651 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0651-OBLIGATION_TREE"
THEOREM = "THM-M-0651"
PREFIX = "M0651-"

# short id, kind, risk, human statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "The exact frozen simultaneous countable omitting-types target.", "Stage1Instances.THM_M_0651.ObligationTree.Root", "A countable model of T omitting every indexed partial type.", "H1", "M4", "R3", 10),
    ("S-EXACT", "definition", "critical", "Preserve the universes, countable language, satisfiability, varying finite arities, partiality, nonprincipality, and universal omission conclusion.", "Stage1Instances.THM_M_0651.OmittingTypesTarget", "The exact statement boundary.", "H1", "M3", "R3", 14),
    ("L-ENUM", "bridge", "high", "Enumerate the language syntax, the Nat-indexed types, and every finite tuple requirement without losing varying arities.", "countable syntax and requirement enumeration interface", "A fair countable schedule of Henkin and omission requirements.", "H1", "M4", "R3", 24),
    ("L-DENSE", "core_lemma", "critical", "Use nonprincipality to extend each finite consistent stage while forcing a formula from the scheduled type to fail at the scheduled tuple.", "nonprincipality avoidance extension interface", "One-step preservation of consistency and a fresh omission witness.", "H1", "M4", "R4", 32),
    ("L-HENKIN", "core_lemma", "critical", "Build a complete Henkin theory meeting the witness and avoidance schedules while preserving consistency.", "Stage1Instances.THM_M_0651.ObligationTree.ConstructionInterface", "A countable candidate model produced from the completed construction.", "H1", "M4", "R4", 40),
    ("L-OMIT", "bridge", "critical", "Decode the avoidance schedule in the term model so every tuple falsifies a member of each indexed type.", "Stage1Instances.THM_M_0651.ObligationTree.AvoidanceInterface", "The candidate omits every p i.", "H1", "M4", "R4", 28),
    ("T-ASSEMBLE", "terminal", "critical", "Compose the countable construction and omission invariant into the exact canonical root.", "Stage1Instances.THM_M_0651.ObligationTree.root_compose", "The exact root conditional on the two substantive interfaces.", "H1", "M1", "R3", 12),
    ("B-ARITY0", "branch", "medium", "Retain zero-arity types and repeated family entries inside the enumeration and omission arguments.", "Fin (arity i), including arity i = 0", "Boundary-case coverage without changing the index domain.", "H1", "M4", "R3", 12),
    ("X-ANCHOR", "provenance", "critical", "Keep the external infinitary theorem architecture-only and prohibit proof credit or an unchecked semantic transport.", "anchor-audit candidate A-INFINITARY-LOGIC", "Deduplicated and correctly bounded formal provenance.", "H1", "M4", "R3", 12),
    ("X-SOURCE", "source", "high", "Pinpoint and review a primary human proof, its exact variant assumptions, and errata.", "primary-source theorem/page remains open", "Human-source coverage of every substantive leaf.", "H1", "M5", "R4", 20),
    ("X-TCB", "trust", "high", "Audit the transitive kernel, dependency, axiom, and executable trust boundary.", "Lean 4.29.0; mathlib 8a178386", "Release-grade trust inventory.", "H1", "M3", "R4", 18),
]

def oid(short):
    return PREFIX + short

statement = json.loads((HERE / "statement.json").read_text())
expr_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
overlays = {"X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "B-ARITY0", "X-TCB"}
body_ids = {"T-ASSEMBLE": "repo:Stage1Instances.THM_M_0651.ObligationTree.root_compose"}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fingerprint = ("lean-expression-sha256:" + expr_hash if short in {"ROOT", "S-EXACT"}
                   else "architecture:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest())
    rows.append({"obligation_id": oid(short), "statement_fingerprint": fingerprint,
        "kind": kind, "root_relevant": short not in overlays,
        "machine_eligibility": "informational" if short in overlays else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None, "terminal_proof_body_id": body_ids.get(short)})

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact elaborated statement and immutable anchor audit determine a countable Henkin construction with explicit dense-avoidance and term-model decoding leaves before any proof closure is observed.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"]},
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows}

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({"node_id": THEOREM + "-" + short, "obligation_id": oid(short),
        "kind": kind, "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd,
        "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0651-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0651-ANCHOR-AUDIT" if short in {"X-ANCHOR", "L-HENKIN", "L-OMIT"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; classical choice is expected but the final axiom inventory is open",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof and refinement graphs"],
            "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0651/obligation-tree.md#" + short.lower(),
        "validation_spec_id": "VAL-M0651-" + short,
        "status_boundary": "Architecture only; no accepted closure credit is assigned in this phase.",
        "task_ids": [ITEM, "S56-M-0651-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0651/obligation-registry.json", "Stage1_Instances/THM-M-0651/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance",
            "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"],
            "revocation_state": "not-accepted"}})

def graph(edges):
    outgoing, incoming = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "L-HENKIN"),
               ("T-ASSEMBLE", "L-OMIT"), ("L-HENKIN", "L-ENUM"),
               ("L-HENKIN", "L-DENSE")]
proof_edges = []
for parent, child in proof_pairs:
    forward, reverse = "PROOF-" + parent + "-" + child, "COMPOSE-" + child + "-" + parent
    proof_edges.extend([
        {"edge_id": forward, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": reverse},
        {"edge_id": reverse, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": forward}])
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([
        {"edge_id": "REFINE-ROOT-EXACT", "from": oid("ROOT"), "type": "logical_decomposition", "to": oid("S-EXACT")},
        {"edge_id": "REFINE-ENUM-ARITY0", "from": oid("L-ENUM"), "type": "logical_decomposition", "to": oid("B-ARITY0")}]),
    "provenance": graph([
        {"edge_id": "PROV-HENKIN-ANCHOR", "from": oid("L-HENKIN"), "type": "provenance_of", "to": oid("X-ANCHOR")},
        {"edge_id": "PROV-OMIT-ANCHOR", "from": oid("L-OMIT"), "type": "provenance_of", "to": oid("X-ANCHOR")},
        {"edge_id": "SOURCE-ROOT", "from": oid("ROOT"), "type": "source_map", "to": oid("X-SOURCE")},
        {"edge_id": "SOURCE-DENSE", "from": oid("L-DENSE"), "type": "source_map", "to": oid("X-SOURCE")}]),
    "evidence": graph([{"edge_id": "EVID-ROOT-ANCHOR", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-ANCHOR")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([
        {"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")},
        {"edge_id": "FLOW-ASSEMBLE-ANCHOR", "from": oid("T-ASSEMBLE"), "type": "workflow_depends_on", "to": oid("X-ANCHOR")}])}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "registry_denominator_sha256": denominator,
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False,
        "root_machine_debt": "M4",
        "remaining_root_cut_set": [oid("L-ENUM"), oid("L-DENSE"), oid("L-HENKIN"), oid("L-OMIT")],
        "composition_certificates_checked": ["Stage1Instances.THM_M_0651.ObligationTree.root_compose"],
        "audit_complete": False, "theorem_complete": False}}
recipes = [{"recipe_id": "VAL-M0651-" + spec[0], "cwd": "Formalizations/Lean",
    "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0651/ObligationTree.lean"],
    "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid(spec[0])]}
    for spec in SPECS]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle),
                    ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
