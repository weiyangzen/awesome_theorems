#!/usr/bin/env python3
"""Build the frozen THM-M-0001 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFIX = "M0001-"
ITEM = "S56-M-0001-OBLIGATION_TREE"

# short id, kind, risk, human statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "Every short exact sequence of homological complexes induces exact homology at all three repeating positions in every degree.", "Stage1Instances.THM_M_0001.LongExactHomologySequenceTarget", "The exact frozen continuing long-sequence proposition.", "H1", "M1", "R4", 8),
    ("S-EXACT", "definition", "high", "Fix arbitrary universes, an abelian category, a complex shape, a short complex, and its ShortExact witness.", "Stage1Instances.THM_M_0001.LongExactHomologySequenceTarget", "The exact binder and hypothesis boundary.", "H1", "M3", "R3", 12),
    ("S-BOUNDARY", "branch", "high", "Retain same-degree exactness at endpoints even when no outgoing Rel edge exists.", "planned: endpoint policy for every i : ι", "An endpoint-complete quantifier policy.", "H1", "M3", "R3", 10),
    ("S-TRANSPORT", "transport", "normal", "Regroup the nested pair into three universally quantified exactness families.", "Stage1Instances.THM_M_0001.longExactHomologySequenceTarget_iff_grouped", "A checked bidirectional statement transport.", "H1", "M1", "R3", 14),
    ("S-FOUNDATION", "certificate", "high", "Fix the classical, quotient, extensionality, kernel, and dependency trust boundary.", "#print axioms root_compose and terminal exactness declarations", "A versioned foundation and TCB boundary.", "H1", "M3", "R4", 12),
    ("N-REPEAT", "normalization", "high", "Normalize the continuing sequence into one same-degree family and two Rel-indexed connecting families.", "SameDegree; RightOfG; LeftOfF", "Three non-overlapping exactness interfaces.", "H1", "M3", "R3", 18),
    ("B-DEGREE", "branch", "high", "For every degree, handle the f-to-g exactness position, including terminal degrees.", "SameDegree", "Exactness of H(f) followed by H(g) for every degree.", "H1", "M1", "R3", 16),
    ("B-RELATED", "branch", "high", "For every c.Rel i j, handle both exactness positions adjacent to the connecting morphism.", "RightOfG ∧ LeftOfF", "The two Rel-indexed exactness families.", "H1", "M1", "R3", 16),
    ("C-DELTA", "construction", "critical", "Construct the connecting morphism delta for a ShortExact sequence and each related degree pair.", "CategoryTheory.ShortComplex.ShortExact.δ", "The connecting morphism H(S.g,i) to H(S.f,j).", "H1", "M1", "R4", 44),
    ("C-ZERO", "construction", "high", "Establish the two zero composites on either side of delta.", "ShortExact.comp_δ; ShortExact.δ_comp", "Well-formed ShortComplex inputs around delta.", "H1", "M1", "R4", 28),
    ("L-EXACT2", "core_lemma", "critical", "Prove same-degree exactness of the induced homology maps for every degree.", "CategoryTheory.ShortComplex.ShortExact.homology_exact₂", "SameDegree for every short exact input.", "H1", "M1", "R4", 36),
    ("L-EXACT3", "core_lemma", "critical", "Prove exactness of H(g) followed by delta for every related degree pair.", "CategoryTheory.ShortComplex.ShortExact.homology_exact₃", "RightOfG for every short exact input.", "H1", "M1", "R4", 32),
    ("L-EXACT1", "core_lemma", "critical", "Prove exactness of delta followed by H(f) for every related degree pair.", "CategoryTheory.ShortComplex.ShortExact.homology_exact₁", "LeftOfF for every short exact input.", "H1", "M1", "R4", 32),
    ("T-ASSEMBLE", "terminal", "critical", "Consume exactly the three exactness families and assemble the nested canonical root.", "Stage1Instances.THM_M_0001.ObligationTree.root_compose", "The exact root, conditionally on all three family obligations.", "H1", "M1", "R3", 12),
    ("X-UPSTREAM", "terminal", "high", "Record the immutable mathlib terminal bodies, source file, declarations, and wrapper/body distinction.", "Mathlib.Algebra.Homology.HomologySequence at 8a178386", "Body-level formal provenance for delta and exactness families.", "H1", "M3", "R4", 20),
    ("X-SOURCE", "terminal", "high", "Pinpoint and independently review a primary mathematical proof, its assumptions, and errata.", "primary source crosswalk remains open", "Human-source mapping for every material node.", "H1", "M5", "R4", 20),
    ("X-TCB", "terminal", "high", "Audit the transitive Lean, mathlib, foundation, imported artifacts, and executable trust closure.", "Lean 4.29.0; mathlib 8a178386; transitive closure pending", "Release-grade trust inventory and axiom decision.", "H1", "M3", "R4", 20),
]


def oid(short):
    return PREFIX + short


statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
informational = {"X-UPSTREAM", "X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION", "X-UPSTREAM", "X-TCB"}
body_ids = {
    "S-TRANSPORT": "repo:Stage1Instances.THM_M_0001.longExactHomologySequenceTarget_iff_grouped",
    "C-DELTA": "mathlib:8a178386:CategoryTheory.ShortComplex.ShortExact.δ",
    "C-ZERO": "mathlib:8a178386:ShortExact.comp_δ+δ_comp",
    "L-EXACT1": "mathlib:8a178386:ShortExact.homology_exact₁",
    "L-EXACT2": "mathlib:8a178386:ShortExact.homology_exact₂",
    "L-EXACT3": "mathlib:8a178386:ShortExact.homology_exact₃",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0001.ObligationTree.root_compose",
}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fp = "lean-expression-sha256:" + expression_hash if short in {"ROOT", "S-EXACT"} else \
        "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest()
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fp, "kind": kind,
        "root_relevant": short not in informational,
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
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": "THM-M-0001", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated target and immutable anchor audit determine the S/N/B/C/L/X/T architecture; eligibility is assigned by mathematical role before proof-phase closure credit.",
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

recipe_ids = {oid(spec[0]): "VAL-M0001-" + spec[0] for spec in SPECS}
nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-0001-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0001-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0001-MATHLIB" if short in {"C-DELTA", "C-ZERO", "L-EXACT1", "L-EXACT2", "L-EXACT3"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib foundations; observed candidate axioms: propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0001/obligation-tree.md#" + short.lower(),
        "validation_spec_id": recipe_ids[oid(short)],
        "status_boundary": "Architecture only; this obligation is not credited closed or accepted by this phase.",
        "task_ids": [ITEM, "S56-M-0001-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0001/obligation-registry.json", "Stage1_Instances/THM-M-0001/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })


def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}


proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "L-EXACT2"), ("T-ASSEMBLE", "L-EXACT3"), ("T-ASSEMBLE", "L-EXACT1"), ("L-EXACT2", "B-DEGREE"), ("L-EXACT3", "B-RELATED"), ("L-EXACT3", "C-DELTA"), ("L-EXACT3", "C-ZERO"), ("L-EXACT1", "B-RELATED"), ("L-EXACT1", "C-DELTA"), ("L-EXACT1", "C-ZERO")]
proof_edges = []
for parent, child in proof_pairs:
    forward, reverse = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges.extend([
        {"edge_id": forward, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": reverse},
        {"edge_id": reverse, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": forward},
    ])
refinement_pairs = [("ROOT", "S-EXACT"), ("S-EXACT", "S-BOUNDARY"), ("S-EXACT", "S-TRANSPORT"), ("S-EXACT", "S-FOUNDATION"), ("ROOT", "N-REPEAT"), ("N-REPEAT", "B-DEGREE"), ("N-REPEAT", "B-RELATED")]
refinement_edges = [{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refinement_pairs]
provenance_edges = [{"edge_id": f"PROV-{short}", "from": oid(short), "type": "provenance_of", "to": oid("X-UPSTREAM")} for short in ("C-DELTA", "C-ZERO", "L-EXACT1", "L-EXACT2", "L-EXACT3")]
provenance_edges += [{"edge_id": f"SOURCE-{short}", "from": oid(short), "type": "source_map", "to": oid("X-SOURCE")} for short in ("ROOT", "C-DELTA", "L-EXACT1", "L-EXACT2", "L-EXACT3")]
graphs = {
    "proof": graph(proof_edges), "refinement": graph(refinement_edges), "provenance": graph(provenance_edges),
    "evidence": graph([{"edge_id": "EVID-ROOT-UPSTREAM", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-UPSTREAM")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0001",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M1", "remaining_root_cut_set": [oid("L-EXACT1"), oid("L-EXACT2"), oid("L-EXACT3")], "composition_certificates_checked": ["Stage1Instances.THM_M_0001.ObligationTree.root_compose"], "audit_complete": False, "theorem_complete": False},
}
recipes = [{"recipe_id": rid, "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0001/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [ob]} for ob, rid in recipe_ids.items()]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0001", "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
