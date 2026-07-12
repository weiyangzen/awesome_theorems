#!/usr/bin/env python3
"""Build the frozen THM-M-0665 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFIX = "M0665-"
ITEM = "S56-M-0665-OBLIGATION_TREE"

# short id, kind, risk, human statement, planned formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "The first-version Pila-Wilkie bound holds for every definable set in every o-minimal expansion of the real field.", "Stage1Instances.THM_M_0665.PilaWilkie", "The exact frozen quantitative counting proposition.", "H1", "M3", "R4", 8),
    ("S-EXACT", "definition", "critical", "Fix the exact language, structure, definability, exponent, constant, height threshold, finiteness, and cardinality binders.", "Stage1Instances.THM_M_0665.PilaWilkie", "The exact statement boundary and binder scope.", "H1", "M3", "R3", 18),
    ("S-DEFS", "definition", "critical", "Relate affine rational height, rational embedding, definability, o-minimality, and the algebraic part to the source definitions.", "rationalHeight; pointHeight; IsOMinimalExpansion; algebraicPart", "Source-faithful definitions for the counting target.", "H1", "M3", "R4", 30),
    ("S-BOUNDARY", "branch", "high", "Retain n=0 and empty or zero-dimensional sets, while excluding epsilon <= 0 and T=0 exactly as frozen.", "threshold_boundary; zero_dimensional_height; planned remaining cases", "Complete handling of all admitted and excluded boundary cases.", "H1", "M3", "R3", 20),
    ("S-TRANSPORT", "transport", "normal", "Expand the named root without changing binder order or quantitative conventions.", "Stage1Instances.THM_M_0665.pilaWilkie_iff", "A checked bidirectional transport to the expanded target.", "H1", "M3", "R3", 8),
    ("S-FOUNDATION", "certificate", "high", "Fix classical logic, choice, real analysis, finite-cardinality, kernel, and dependency trust policy.", "planned: transitive #print axioms and dependency report", "A versioned foundation and TCB boundary.", "H1", "M3", "R4", 16),
    ("N-ALGEBRAIC", "normalization", "critical", "Separate X into its algebraic part and the transcendental complement used by the source theorem.", "planned: algebraicPart decomposition and membership lemmas", "A normalized transcendental locus with no omitted positive-dimensional semialgebraic piece.", "H1", "M4", "R4", 34),
    ("N-HEIGHT", "normalization", "high", "Normalize affine rational points and coordinatewise height into the finite counting interface.", "planned: rational-height finiteness and coercion lemmas", "A finite bounded-height ambient rational grid and compatible real embedding.", "H1", "M4", "R4", 28),
    ("B-DIMENSION", "branch", "critical", "Induct on the dimension of the definable set and discharge the zero-dimensional branch.", "planned: o-minimal dimension induction", "All dimension branches, including strict dimension drops.", "H1", "M4", "R4", 54),
    ("B-CHARTS", "branch", "critical", "Split a definable set into finitely many controlled smooth parameterized charts.", "planned: definable parametrization branch family", "An exhaustive finite chart cover with uniform derivative control.", "H1", "M4", "R4", 60),
    ("C-PARAM", "construction", "critical", "Construct the controlled C^r parametrizations required for an exponent chosen from epsilon and ambient dimension.", "planned: Pila-Wilkie parametrization theorem", "Finitely many derivative-controlled maps covering the normalized set.", "H1", "M4", "R4", 72),
    ("C-HYPERSURFACE", "construction", "critical", "For rational points in a sufficiently small parameter box, construct a bounded-degree algebraic hypersurface containing them.", "planned: determinant-method hypersurface construction", "A low-degree hypersurface certificate for every local rational-point cluster.", "H1", "M4", "R4", 78),
    ("L-DERIVATIVE", "core_lemma", "critical", "Bound Taylor remainders and determinants using the controlled derivatives of each chart.", "planned: analytic determinant estimate", "The small-determinant inequality needed for integrality to force vanishing.", "H1", "M4", "R4", 70),
    ("L-ARITHMETIC", "core_lemma", "critical", "Use rational denominators and affine height to turn a sufficiently small determinant into an exactly zero determinant.", "planned: denominator lower bound and determinant vanishing", "Algebraic dependence of each local bounded-height point cluster.", "H1", "M4", "R4", 62),
    ("L-DROP", "core_lemma", "critical", "Intersect the definable chart image with each auxiliary hypersurface and prove either algebraic-part containment or strict dimension drop.", "planned: hypersurface intersection dimension lemma", "Subproblems eligible for the dimension induction without losing transcendental points.", "H1", "M4", "R4", 74),
    ("L-COUNT", "core_lemma", "critical", "Choose degree, differentiability order, and box scale so the number of auxiliary hypersurfaces and all lower-dimensional contributions are O(T^epsilon).", "planned: exponent bookkeeping and finite-sum estimate", "A positive constant uniform in every natural T >= 1 and the required cardinality bound.", "H1", "M4", "R4", 82),
    ("T-ASSEMBLE", "terminal", "critical", "Compose normalization, parametrization, determinant vanishing, dimension descent, and exponent bookkeeping into the exact root.", "planned: Stage1Instances.THM_M_0665.ObligationTree.root_compose", "Stage1Instances.THM_M_0665.PilaWilkie with no extra premise.", "H1", "M4", "R4", 36),
    ("X-SOURCE", "terminal", "high", "Pinpoint and independently review Theorem 1.8 and Definitions 1.3 and 1.5, including errata and every material proof lemma.", "primary-source crosswalk remains open", "Human-source mappings for the root and every material proof node.", "H1", "M5", "R4", 30),
    ("X-UPSTREAM", "terminal", "high", "Record immutable formal candidates and distinguish statement ingredients from terminal proof bodies.", "Stage1_Instances/THM-M-0665/anchor-audit.json", "Body-level provenance showing that no candidate currently closes a proof node.", "H1", "M3", "R4", 20),
    ("X-TCB", "terminal", "high", "Audit Lean, mathlib, all future proof bodies, foundation axioms, generated artifacts, and replay executables transitively.", "Lean 4.29.0; mathlib 8a178386; proof closure absent", "Release-grade trust inventory and axiom decision.", "H1", "M3", "R4", 24),
]


def oid(short):
    return PREFIX + short


statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
informational = {"X-SOURCE", "X-UPSTREAM", "X-TCB"}
no_human = {"S-EXACT", "S-BOUNDARY", "S-TRANSPORT", "S-FOUNDATION", "X-UPSTREAM", "X-TCB"}
body_ids = {"S-TRANSPORT": "repo:Stage1Instances.THM_M_0665.pilaWilkie_iff"}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fingerprint = ("lean-expression-sha256:" + expression_hash) if short in {"ROOT", "S-EXACT"} else \
        "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest()
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
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
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": "THM-M-0665",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact elaborated first-version target, source pinpoint, and immutable no-closure anchor audit determine this S/N/B/C/L/X/T architecture. Eligibility was assigned from mathematical role without granting closure credit.",
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

recipe_ids = {oid(spec[0]): "VAL-M0665-" + spec[0] for spec in SPECS}
nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-0665-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M0665-PW2006-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0665-ANCHOR-NO-CLOSURE" if short == "X-UPSTREAM" else "none",
        "foundation_profile": "Lean 4 dependent type theory with classical real-analysis dependencies to be audited; no custom axiom accepted",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive proof and release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-0665/obligation-tree.md#" + short.lower(),
        "validation_spec_id": recipe_ids[oid(short)],
        "status_boundary": "Architecture only; this phase grants no machine closure or accepted proof state.",
        "task_ids": [ITEM, "S56-M-0665-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0665/obligation-registry.json", "Stage1_Instances/THM-M-0665/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "source pinpoint", "registry", "toolchain", "mathlib revision", "anchor provenance"], "revocation_state": "not-accepted"},
    })


def graph(edges):
    outgoing, incoming = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


proof_pairs = [
    ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "N-ALGEBRAIC"), ("T-ASSEMBLE", "N-HEIGHT"),
    ("T-ASSEMBLE", "B-DIMENSION"), ("T-ASSEMBLE", "L-COUNT"),
    ("B-DIMENSION", "L-DROP"), ("B-CHARTS", "C-PARAM"),
    ("C-HYPERSURFACE", "L-DERIVATIVE"), ("C-HYPERSURFACE", "L-ARITHMETIC"),
    ("L-DROP", "C-HYPERSURFACE"), ("L-DROP", "B-CHARTS"),
    ("L-COUNT", "C-PARAM"), ("L-COUNT", "C-HYPERSURFACE"), ("L-COUNT", "L-DROP"),
]
proof_edges = []
for parent, child in proof_pairs:
    forward, reverse = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges.extend([
        {"edge_id": forward, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": reverse},
        {"edge_id": reverse, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": forward},
    ])
refinement_pairs = [("ROOT", "S-EXACT"), ("S-EXACT", "S-DEFS"), ("S-EXACT", "S-BOUNDARY"), ("S-EXACT", "S-TRANSPORT"), ("S-EXACT", "S-FOUNDATION"), ("ROOT", "N-ALGEBRAIC"), ("ROOT", "N-HEIGHT"), ("B-DIMENSION", "B-CHARTS")]
source_nodes = ("ROOT", "S-DEFS", "C-PARAM", "L-DERIVATIVE", "L-ARITHMETIC", "L-DROP", "L-COUNT")
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refinement_pairs]),
    "provenance": graph([{"edge_id": f"SOURCE-{s}", "from": oid(s), "type": "source_map", "to": oid("X-SOURCE")} for s in source_nodes] + [{"edge_id": "PROV-ROOT-UPSTREAM", "from": oid("ROOT"), "type": "provenance_of", "to": oid("X-UPSTREAM")}]),
    "evidence": graph([{"edge_id": "EVID-ROOT-UPSTREAM", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-UPSTREAM")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0665",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [], "root_closed": False, "root_machine_debt": "M3",
        "remaining_root_cut_set": [oid("C-PARAM"), oid("L-DERIVATIVE"), oid("L-ARITHMETIC"), oid("L-DROP"), oid("L-COUNT")],
        "composition_certificates_checked": [],
        "composition_blocker": "No exact Lean signatures or proofs exist for the parametrization, determinant, dimension-drop, and counting children, so manufacturing a conditional composition certificate would not bind exact child fingerprints.",
        "audit_complete": False, "theorem_complete": False,
    },
}
recipes = [{"recipe_id": rid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0665/check_obligation_tree.py"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [ob]} for ob, rid in recipe_ids.items()]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-0665", "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
