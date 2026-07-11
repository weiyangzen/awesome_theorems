#!/usr/bin/env python3
"""Build the frozen THM-M-0106 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

specs = [
    # id, kind, risk, human statement, formal target, output, H, M, R, budget
    ("ROOT", "root", "critical", "The exact algebraic-plus-affine Noether-normalization target.", "Stage1Instances.THM_M_0106.NoetherNormalizationTarget", "The frozen root proposition.", "H4", "M2", "R4", 8),
    ("S-EXACT", "definition", "high", "Fix universes, typeclasses, polynomial indexing, and the affine target.", "Stage1Instances.THM_M_0106.NoetherNormalizationTarget", "An exact statement boundary definitionally equal to ROOT.", "H4", "M1", "R3", 8),
    ("S-BOUNDARY", "branch", "normal", "Include s = 0 while excluding the zero ring and no other geometric hypotheses.", "planned: boundary cases of NoetherNormalizationTarget", "Exhaustive degenerate-case policy.", "H4", "M4", "R3", 10),
    ("S-TRANSPORT", "transport", "high", "Transport the affine-Spec formulation to the explicit affine-space morphism.", "Stage1Instances.THM_M_0106.target_iff_pinnedAffineSpecCandidateShape", "Checked equivalence of the two target encodings.", "H4", "M1", "R3", 12),
    ("S-FOUNDATION", "certificate", "high", "Fix classical, quotient, extensionality, kernel, and dependency trust boundaries.", "#print axioms root_compose", "A named foundation and axiom-policy boundary.", "H4", "M3", "R4", 12),
    ("N-PRESENT", "normalization", "high", "Present a finite-type algebra as a quotient of a finite-variable polynomial algebra.", "Algebra.FiniteType.iff_quotient_mvPolynomial''", "A surjective polynomial presentation and quotient-kernel equivalence.", "H4", "M2", "R4", 24),
    ("B-QUOTIENT", "reduction", "critical", "Prove integral injective normalization for every proper polynomial ideal by induction on variables.", "exists_integral_inj_algHom_of_quotient", "An integral injective polynomial map into the quotient.", "H4", "M2", "R4", 16),
    ("B-ZERO", "branch", "high", "Handle the zero-variable quotient using constants and properness of the ideal.", "exists_integral_inj_algHom_of_quotient: induction zero branch", "The quotient normalization package for n = 0.", "H4", "M2", "R4", 38),
    ("B-SUCC", "branch", "critical", "Split the successor-variable case into I = bottom and I != bottom and recompose.", "exists_integral_inj_algHom_of_quotient: induction succ branch", "The quotient normalization package for n + 1.", "H4", "M2", "R4", 30),
    ("C-NAGATA", "construction", "critical", "Choose a triangular coordinate change making a nonzero ideal element monic in one variable.", "NoetherNormalization.T_leadingcoeff_isUnit", "A transformed polynomial with unit leading coefficient.", "H4", "M2", "R4", 84),
    ("C-HOM2", "construction", "critical", "Construct the lower-variable map through quotient equivalences and prove it integral.", "NoetherNormalization.hom2; NoetherNormalization.hom2_isIntegral", "An integral map used by the induction step.", "H4", "M2", "R4", 58),
    ("L-INTEGRAL-FG", "core_lemma", "critical", "Transfer quotient normalization along a finite-type polynomial presentation.", "exists_integral_inj_algHom_of_fg", "An injective integral polynomial-algebra map into R.", "H4", "M2", "R4", 28),
    ("L-FINITE", "core_lemma", "critical", "Upgrade integrality to module finiteness using finite type and scalar-tower compatibility.", "exists_finite_inj_algHom_of_fg", "The exact algebraic child required by root composition.", "H4", "M2", "R4", 20),
    ("L-SPEC", "bridge", "high", "Translate AlgHom.Finite to finiteness of Spec.map and postcompose with SpecIso.inv.", "AlgebraicGeometry.IsFinite.SpecMap_iff; MorphismProperty.RespectsIso.postcomp", "The finite affine-space morphism and commuting equation.", "H4", "M1", "R3", 18),
    ("T-ASSEMBLE", "terminal", "critical", "Consume the algebraic core and affine bridge to return the exact root.", "Stage1Instances.THM_M_0106.ObligationTree.root_compose", "ROOT with no undeclared mathematical premise beyond L-FINITE.", "H4", "M1", "R3", 14),
    ("X-UPSTREAM", "terminal", "high", "Record the pinned mathlib body chain and distinguish private bodies from wrappers.", "Mathlib/RingTheory/NoetherNormalization.lean at 8a178386", "Body-level provenance for B, C, and L nodes.", "H4", "M3", "R4", 18),
    ("X-SOURCE", "terminal", "high", "Pinpoint and review a primary mathematical proof and assumptions.", "Stacks Project tag 00OW (lead only; review open)", "Human-source crosswalk for every mathematical node.", "H4", "M5", "R4", 20),
    ("X-TCB", "terminal", "high", "Audit the transitive Lean, mathlib, foundation, and computation boundary.", "Lean 4.29.0; mathlib 8a178386; transitive closure pending", "Release trust inventory and axiom report.", "H5", "M3", "R4", 20),
]

def oid(short):
    return "M0106-" + short

statement_hash = json.loads((HERE / "statement.json").read_text())["canonical_formal_target"]["elaborated_expression_sha256"]
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in specs:
    fingerprint = ("lean-expression-sha256:" + statement_hash) if short in {"ROOT", "S-EXACT"} else \
        "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest()
    informational = short.startswith("X-")
    body_ids = {
        "B-QUOTIENT": "mathlib:8a178386:exists_integral_inj_algHom_of_quotient",
        "C-NAGATA": "mathlib:8a178386:NoetherNormalization.T_leadingcoeff_isUnit",
        "C-HOM2": "mathlib:8a178386:NoetherNormalization.hom2_isIntegral",
        "L-INTEGRAL-FG": "mathlib:8a178386:exists_integral_inj_algHom_of_fg",
        "L-FINITE": "mathlib:8a178386:exists_finite_inj_algHom_of_fg",
        "S-TRANSPORT": "repo:Stage1Instances.THM_M_0106.target_iff_pinnedAffineSpecCandidateShape",
        "T-ASSEMBLE": "repo:Stage1Instances.THM_M_0106.ObligationTree.root_compose",
    }
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": not informational,
        "machine_eligibility": "informational" if informational else "required",
        "human_source_eligibility": "required" if short not in {"S-EXACT", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION", "X-UPSTREAM", "X-TCB"} else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": body_ids.get(short),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: r[k] for k in fields} for r in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r["obligation_id"] for r in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0106-OBLIGATION_TREE",
    "theorem_id": "THM-M-0106", "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact statement and immutable anchor inventory determine the S/N/B/C/L/X/T architecture; eligibility is assigned by mathematical role, never by observed closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.md").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any target correction, split, merge, eligibility change, exclusion, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows,
}

recipe_ids = {oid(s[0]): "VAL-M0106-" + s[0] for s in specs}
nodes = []
for (short, kind, risk, human, formal, output, hd, md, rd, budget), row in zip(specs, rows):
    nodes.append({
        "node_id": "THM-M-0106-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0106-MATHLIB" if short in {"N-PRESENT", "B-QUOTIENT", "B-ZERO", "B-SUCC", "C-NAGATA", "C-HOM2", "L-INTEGRAL-FG", "L-FINITE"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib default foundations; audit reports propext, Classical.choice, Quot.sound",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; release trust audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof graph"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0106/obligation-tree.md#" + short.lower(),
        "validation_spec_id": recipe_ids[oid(short)], "status_boundary": "Architecture only; this node is not accepted or credited closed by the obligation-tree phase.",
        "task_ids": ["S56-M-0106-OBLIGATION_TREE", "S56-M-0106-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0106/obligation-registry.json", "Stage1_Instances/THM-M-0106/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })

proof_pairs = [
    ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "S-EXACT"), ("T-ASSEMBLE", "L-FINITE"), ("T-ASSEMBLE", "L-SPEC"),
    ("L-FINITE", "L-INTEGRAL-FG"), ("L-INTEGRAL-FG", "N-PRESENT"), ("L-INTEGRAL-FG", "B-QUOTIENT"),
    ("B-QUOTIENT", "B-ZERO"), ("B-QUOTIENT", "B-SUCC"), ("B-SUCC", "C-NAGATA"), ("B-SUCC", "C-HOM2"),
]
refine_pairs = [("S-EXACT", x) for x in ("S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION")]

def graph(edges):
    out, inn = {}, {}
    for e in edges:
        out.setdefault(e["from"], []).append(e["edge_id"])
        inn.setdefault(e["to"], []).append(e["edge_id"])
    return {"edges": edges, "out": out, "in": inn}

proof_edges = []
for parent, child in proof_pairs:
    a = f"PROOF-{parent}-{child}"
    b = f"COMPOSE-{child}-{parent}"
    proof_edges += [
        {"edge_id": a, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": b},
        {"edge_id": b, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": a},
    ]
refinement_edges = [{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refine_pairs]
prov_edges = [{"edge_id": f"PROV-{x}", "from": oid(x), "type": "provenance_of", "to": oid("X-UPSTREAM")} for x in ("B-QUOTIENT", "C-NAGATA", "C-HOM2", "L-INTEGRAL-FG", "L-FINITE")]
source_edges = [{"edge_id": f"SOURCE-{x}", "from": oid(x), "type": "source_map", "to": oid("X-SOURCE")} for x in ("ROOT", "B-QUOTIENT", "C-NAGATA", "L-INTEGRAL-FG", "L-FINITE")]
graphs = {
    "proof": graph(proof_edges), "refinement": graph(refinement_edges),
    "provenance": graph(prov_edges + source_edges),
    "evidence": graph([{"edge_id": "EVID-ROOT-UPSTREAM", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-UPSTREAM")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-0106-OBLIGATION_TREE", "theorem_id": "THM-M-0106",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M2", "remaining_root_cut_set": [oid("L-FINITE")], "composition_certificates_checked": ["Stage1Instances.THM_M_0106.ObligationTree.root_compose"], "theorem_complete": False},
}
recipes = [{"recipe_id": rid, "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0106/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [ob]} for ob, rid in recipe_ids.items()]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": "S56-M-0106-OBLIGATION_TREE", "theorem_id": "THM-M-0106", "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
