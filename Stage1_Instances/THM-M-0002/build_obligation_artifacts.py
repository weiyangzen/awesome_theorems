#!/usr/bin/env python3
"""Build the frozen THM-M-0002 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFIX = "M0002-"
ITEM = "S56-M-0002-OBLIGATION_TREE"

# short id, kind, risk, human statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "The middle vertical component of the frozen exact five-object diagram is an isomorphism.", "Stage1Instances.THM_M_0002.FiveLemmaTarget", "The exact frozen five-lemma proposition.", "H2", "M1", "R4", 8),
    ("S-EXACT", "definition", "high", "Fix two exact composable rows of length four and their natural transformation.", "ComposableArrows.Exact; app'", "The exact binder and row-exactness boundary.", "H2", "M3", "R3", 12),
    ("S-HYPOTHESES", "definition", "high", "Retain epi at component 0, isomorphisms at 1 and 3, and mono at 4 without strengthening them.", "Epi(app' phi 0); IsIso(app' phi 1); IsIso(app' phi 3); Mono(app' phi 4)", "The four asymmetric vertical hypotheses.", "H2", "M3", "R3", 12),
    ("S-TRANSPORT", "transport", "normal", "Identify the frozen target with the pinned candidate source shape.", "fiveLemmaTarget_iff_pinnedCandidateSourceShape", "A checked bidirectional statement transport.", "H2", "M1", "R3", 8),
    ("B-MONO", "branch", "critical", "Derive that the middle component is monic from the left four-object truncation.", "MiddleMono", "Mono (app' phi 2).", "H2", "M1", "R4", 30),
    ("B-EPI", "branch", "critical", "Derive that the middle component is epic from the right four-object truncation.", "MiddleEpi", "Epi (app' phi 2).", "H2", "M1", "R4", 30),
    ("C-LEFT-TRUNC", "construction", "high", "Apply delta-last truncation and transport exactness of both five-object rows.", "deltaLastFunctor; ComposableArrows.exact_iff_deltaLast", "Exact left four-object rows and their induced morphism.", "H2", "M1", "R4", 22),
    ("C-RIGHT-TRUNC", "construction", "high", "Apply delta-zero truncation and transport exactness of both five-object rows.", "deltaZeroFunctor; ComposableArrows.exact_iff_deltaZero", "Exact right four-object rows and their induced morphism.", "H2", "M1", "R4", 22),
    ("L-FOUR-MONO", "core_lemma", "critical", "Use the mono four lemma on the left truncation, discharging mono interfaces from isomorphisms.", "CategoryTheory.Abelian.mono_of_epi_of_mono_of_mono", "Mono (app' phi 2).", "H2", "M1", "R4", 44),
    ("L-FOUR-EPI", "core_lemma", "critical", "Use the epi four lemma on the right truncation, discharging epi interfaces from isomorphisms.", "CategoryTheory.Abelian.epi_of_epi_of_epi_of_mono", "Epi (app' phi 2).", "H2", "M1", "R4", 44),
    ("T-ASSEMBLE", "terminal", "critical", "Combine the middle Mono and Epi instances into IsIso.", "Stage1Instances.THM_M_0002.ObligationTree.root_compose", "The exact root conditional on the two branch obligations.", "H2", "M1", "R3", 12),
    ("X-UPSTREAM", "terminal", "high", "Record the pinned mathlib theorem bodies, imports, revision, and wrapper/body distinction.", "Mathlib.CategoryTheory.Abelian.DiagramLemmas.Four at 8a178386", "Body-level formal provenance for both four lemmas and isIso assembly.", "H2", "M3", "R4", 24),
    ("X-SOURCE", "terminal", "high", "Pinpoint and independently review a primary mathematical proof, assumptions, and errata.", "primary source crosswalk remains open", "Human-source mapping for each mathematical branch.", "H2", "M5", "R4", 20),
    ("X-TCB", "terminal", "high", "Audit transitive Lean, mathlib, foundation, imported artifact, and executable trust closure.", "Lean 4.29.0; mathlib 8a178386; transitive closure pending", "Release-grade trust inventory and axiom decision.", "H2", "M3", "R4", 20),
]

def oid(short): return PREFIX + short

statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
informational = {"X-UPSTREAM", "X-SOURCE", "X-TCB"}
no_human = {"S-EXACT", "S-HYPOTHESES", "S-TRANSPORT", "X-UPSTREAM", "X-TCB"}
body_ids = {
    "S-TRANSPORT": "repo:Stage1Instances.THM_M_0002.fiveLemmaTarget_iff_pinnedCandidateSourceShape",
    "L-FOUR-MONO": "mathlib:8a178386:CategoryTheory.Abelian.mono_of_epi_of_mono_of_mono",
    "L-FOUR-EPI": "mathlib:8a178386:CategoryTheory.Abelian.epi_of_epi_of_epi_of_mono",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0002.ObligationTree.root_compose",
}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fp = "lean-expression-sha256:" + expression_hash if short == "ROOT" else "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest()
    rows.append({"obligation_id": oid(short), "statement_fingerprint": fp, "kind": kind,
        "root_relevant": short not in informational,
        "machine_eligibility": "informational" if short in informational else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": body_ids.get(short)})

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: r[k] for k in fields} for r in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r["obligation_id"] for r in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-0002",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated five-lemma target and immutable anchor audit determine the two four-lemma branches and separate statement, provenance, source, and trust obligations; eligibility was fixed before proof-phase closure credit.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"]},
    "delta_policy": "Any correction, split, merge, eligibility/exclusion/risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows}

recipe_ids = {oid(s[0]): "VAL-M0002-" + s[0] for s in SPECS}
nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({"node_id": "THM-M-0002-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0002-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0002-MATHLIB" if short in {"C-LEFT-TRUNC", "C-RIGHT-TRUNC", "L-FOUR-MONO", "L-FOUR-EPI"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib foundations; observed candidate axioms: propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0002/obligation-tree.md#" + short.lower(),
        "validation_spec_id": recipe_ids[oid(short)],
        "status_boundary": "Architecture only; this obligation is not credited closed or accepted by this phase.",
        "task_ids": [ITEM, "S56-M-0002-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0002/obligation-registry.json", "Stage1_Instances/THM-M-0002/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"}})

def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"]); incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}

proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "B-MONO"), ("T-ASSEMBLE", "B-EPI"), ("B-MONO", "L-FOUR-MONO"), ("B-MONO", "C-LEFT-TRUNC"), ("B-EPI", "L-FOUR-EPI"), ("B-EPI", "C-RIGHT-TRUNC")]
proof_edges = []
for parent, child in proof_pairs:
    f, r = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges += [{"edge_id": f, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": r}, {"edge_id": r, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": f}]
refinement = [("ROOT", "S-EXACT"), ("ROOT", "S-HYPOTHESES"), ("ROOT", "S-TRANSPORT"), ("ROOT", "B-MONO"), ("ROOT", "B-EPI")]
prov_nodes = ("C-LEFT-TRUNC", "C-RIGHT-TRUNC", "L-FOUR-MONO", "L-FOUR-EPI", "T-ASSEMBLE")
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a,b in refinement]),
    "provenance": graph([{"edge_id": f"PROV-{s}", "from": oid(s), "type": "provenance_of", "to": oid("X-UPSTREAM")} for s in prov_nodes] + [{"edge_id": f"SOURCE-{s}", "from": oid(s), "type": "source_map", "to": oid("X-SOURCE")} for s in ("ROOT", "B-MONO", "B-EPI")]),
    "evidence": graph([{"edge_id": "EVID-ROOT-UPSTREAM", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-UPSTREAM")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}])}
bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0002",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M1",
        "remaining_root_cut_set": [oid("B-MONO"), oid("B-EPI")],
        "composition_certificates_checked": ["Stage1Instances.THM_M_0002.ObligationTree.root_compose"],
        "audit_complete": False, "theorem_complete": False}}
recipes = [{"recipe_id": rid, "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0002/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [ob]} for ob, rid in recipe_ids.items()]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0002", "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
