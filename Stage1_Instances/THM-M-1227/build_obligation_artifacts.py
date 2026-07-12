#!/usr/bin/env python3
"""Build the frozen THM-M-1227 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1227-OBLIGATION_TREE"
PREFIX = "M1227-"

# short id, kind, risk, statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "Every positive viscosity and finite-energy distributionally divergence-free datum on R^3 admits a global unforced Leray-Hopf solution in the frozen formulation.", "Stage1.THM_M_1227.lerayHopfExistenceTarget", "The exact canonical existence proposition.", "H2", "M4", "R4", 8),
    ("S-EXACT", "definition", "critical", "Preserve the exact binders, hypotheses, witnesses, and six conjuncts in Statement.lean.", "Stage1.THM_M_1227.lerayHopfExistenceTarget", "The fixed statement boundary.", "H2", "M4", "R3", 18),
    ("S-BOUNDARY", "branch", "high", "Cover zero datum, exclude zero viscosity, retain dimension three, all nonnegative times, and the whole-space domain.", "planned: boundary cases for lerayHopfExistenceTarget", "No degenerate case silently changes the target.", "H2", "M4", "R3", 20),
    ("S-FOUNDATION", "certificate", "high", "Audit classical choice, extensionality, integration, derivatives, and the transitive Lean trust boundary.", "#print axioms terminal proof declarations", "A versioned foundation and TCB decision.", "H2", "M4", "R4", 18),
    ("N-DATA", "normalization", "high", "Approximate arbitrary finite-energy solenoidal data by smooth finite-dimensional data without changing viscosity or domain.", "planned: solenoidal smooth approximation of u0", "A convergent admissible datum sequence.", "H2", "M4", "R4", 55),
    ("N-GLOBAL", "normalization", "critical", "Pass from finite-dimensional and finite-time approximants to one solution on every nonnegative time.", "planned: diagonal local-to-global normalization", "A globally defined witness pair u,g.", "H2", "M4", "R4", 70),
    ("B-ZERO", "branch", "normal", "Construct and verify the zero solution when the datum vanishes.", "planned: u0 = 0 branch", "The degenerate datum branch.", "H2", "M4", "R3", 22),
    ("B-GENERAL", "branch", "critical", "Handle nonzero admissible data and prove the zero/general branches exhaust all inputs.", "planned: u0 != 0 branch and recomposition", "The general-data branch and exhaustive merge.", "H2", "M4", "R4", 24),
    ("C-GALERKIN", "construction", "critical", "Construct divergence-free Galerkin approximants satisfying the projected Navier-Stokes system.", "planned: Galerkin approximant construction", "Finite-dimensional approximate velocities.", "H2", "M4", "R4", 85),
    ("C-BOUNDS", "construction", "critical", "Derive viscosity-uniform-in-dimension energy and gradient bounds for the approximants.", "planned: Galerkin energy estimate", "Uniform L2 and dissipation control.", "H2", "M4", "R4", 72),
    ("C-COMPACT", "construction", "critical", "Extract a subsequence with enough strong/weak convergence to pass the quadratic term and gradients.", "planned: weak compactness plus nonlinear compactness", "Limit witnesses u,g and convergence certificates.", "H2", "M4", "R4", 96),
    ("L-GRADIENT", "core_lemma", "high", "Identify g as the distributional spatial gradient of the limiting velocity.", "Stage1.THM_M_1227.IsWeakGradient u g", "The weak-gradient conjunct.", "H2", "M4", "R4", 48),
    ("L-CLASS", "core_lemma", "high", "Prove almost-everywhere spatial integrability of the limiting velocity and gradient energies.", "planned: energyClass premise of isLerayHopfSolution_compose", "The energy-class conjunct.", "H2", "M4", "R4", 42),
    ("L-DIVERGENCE", "core_lemma", "high", "Pass solenoidality to the limit and identify the almost-everywhere trace-free gradient.", "planned: incompressible premise of isLerayHopfSolution_compose", "The incompressibility conjunct.", "H2", "M4", "R4", 45),
    ("L-MOMENTUM", "core_lemma", "critical", "Pass the Galerkin identity, including the quadratic convection term, to every frozen solenoidal test velocity.", "planned: weakMomentum premise of isLerayHopfSolution_compose", "The weak momentum identity and integrability conjunct.", "H2", "M4", "R4", 92),
    ("L-TRACE", "core_lemma", "critical", "Prove strong L2 attainment of the datum as time tends to zero from the right.", "planned: initialTrace premise of isLerayHopfSolution_compose", "The initial-trace conjunct.", "H2", "M4", "R4", 68),
    ("L-ENERGY", "core_lemma", "critical", "Pass the approximate energy estimates to the limit for every nonnegative time in the frozen representative.", "planned: energyInequality premise of isLerayHopfSolution_compose", "The global energy-inequality conjunct.", "H2", "M4", "R4", 78),
    ("T-ASSEMBLE", "terminal", "critical", "Consume all six exact solution components and assemble IsLerayHopfSolution, then introduce the witnesses.", "Stage1.THM_M_1227.isLerayHopfSolution_compose", "The exact root conditional on the open construction and lemma obligations.", "H2", "M3", "R3", 16),
    ("X-SOURCE", "terminal", "high", "Pinpoint and independently review the primary theorem, assumptions, proof route, translation, and errata.", "primary-source theorem/page crosswalk open", "Human-source provenance for every material node.", "H2", "M5", "R4", 24),
    ("X-TCB", "terminal", "high", "Audit the transitive Lean, mathlib, imported artifact, axiom, and reproducibility boundary.", "Lean 4 and mathlib pinned environment; release audit open", "Release-grade trust inventory.", "H2", "M4", "R4", 24),
    ("X-AUTOMATION", "terminal", "normal", "Record every future tactic, simplifier, compactness library theorem, and terminal proof-body provenance.", "planned: proof-body provenance ledger", "No automation or imported theorem is hidden.", "H2", "M4", "R4", 20),
]


def oid(short):
    return PREFIX + short


statement_bytes = (HERE / "Statement.lean").read_bytes()
anchor_bytes = (HERE / "anchor-audit.json").read_bytes()
statement_hash = hashlib.sha256(statement_bytes).hexdigest()
informational = {"X-SOURCE", "X-TCB", "X-AUTOMATION"}
no_human = {"S-EXACT", "S-BOUNDARY", "S-FOUNDATION", "X-TCB", "X-AUTOMATION"}
body_ids = {"T-ASSEMBLE": "repo:Stage1.THM_M_1227.isLerayHopfSolution_compose"}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fingerprint = ("lean-source-sha256:" + statement_hash if short in {"ROOT", "S-EXACT"} else
                   "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest())
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
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": "THM-M-1227", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact elaborated target and immutable zero-terminal-candidate anchor audit determine this S/N/B/C/L/X/T architecture before proof-phase closure credit.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": hashlib.sha256(anchor_bytes).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, target, eligibility, exclusion, weight, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows,
}

recipes = {oid(s[0]): "VAL-M1227-" + s[0] for s in SPECS}
nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-1227-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd, "evidence_ids": [],
        "source_crosswalk_id": "SRC-M1227-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M1227-LOCAL-COMPOSITION" if short == "T-ASSEMBLE" else "none",
        "foundation_profile": "Lean 4 dependent type theory; classical/noncomputable analysis boundary remains to be audited",
        "tcb_profile": "repository-pinned Lean toolchain and mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed children in proof/refinement graphs"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-1227/obligation-tree.md#" + short.lower(),
        "validation_spec_id": recipes[oid(short)],
        "status_boundary": "Architecture only; this obligation is not credited closed or accepted by this phase.",
        "task_ids": [ITEM, "S56-M-1227-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1227/obligation-registry.json", "Stage1_Instances/THM-M-1227/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["Statement.lean", "registry", "toolchain", "mathlib revision", "anchor audit", "source crosswalk"], "revocation_state": "not-accepted"},
    })


def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}


proof_pairs = [
    ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "L-GRADIENT"), ("T-ASSEMBLE", "L-CLASS"),
    ("T-ASSEMBLE", "L-DIVERGENCE"), ("T-ASSEMBLE", "L-MOMENTUM"),
    ("T-ASSEMBLE", "L-TRACE"), ("T-ASSEMBLE", "L-ENERGY"),
    ("L-GRADIENT", "C-COMPACT"), ("L-CLASS", "C-BOUNDS"), ("L-CLASS", "C-COMPACT"),
    ("L-DIVERGENCE", "C-GALERKIN"), ("L-DIVERGENCE", "C-COMPACT"),
    ("L-MOMENTUM", "C-GALERKIN"), ("L-MOMENTUM", "C-COMPACT"),
    ("L-TRACE", "N-DATA"), ("L-TRACE", "C-COMPACT"),
    ("L-ENERGY", "C-BOUNDS"), ("L-ENERGY", "C-COMPACT"),
    ("C-GALERKIN", "N-DATA"), ("C-COMPACT", "C-BOUNDS"), ("C-COMPACT", "N-GLOBAL"),
]
proof_edges = []
for parent, child in proof_pairs:
    forward, reverse = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges.extend([
        {"edge_id": forward, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": reverse},
        {"edge_id": reverse, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": forward},
    ])
refinement_pairs = [("ROOT", "S-EXACT"), ("S-EXACT", "S-BOUNDARY"), ("S-EXACT", "S-FOUNDATION"), ("ROOT", "N-DATA"), ("ROOT", "N-GLOBAL"), ("ROOT", "B-ZERO"), ("ROOT", "B-GENERAL")]
refinement = [{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refinement_pairs]
material = ("ROOT", "N-DATA", "N-GLOBAL", "C-GALERKIN", "C-BOUNDS", "C-COMPACT", "L-MOMENTUM", "L-TRACE", "L-ENERGY")
graphs = {
    "proof": graph(proof_edges), "refinement": graph(refinement),
    "provenance": graph([{"edge_id": f"SOURCE-{s}", "from": oid(s), "type": "source_map", "to": oid("X-SOURCE")} for s in material] + [{"edge_id": "PROV-T-ASSEMBLE", "from": oid("T-ASSEMBLE"), "type": "provenance_of", "to": oid("X-AUTOMATION")}]),
    "evidence": graph([{"edge_id": "EVID-ROOT-AUTOMATION", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X-AUTOMATION")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT-SOURCE", "from": oid("ROOT"), "type": "documents", "to": oid("X-SOURCE")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}]),
}
cut_set = [oid(s) for s in ("N-DATA", "N-GLOBAL", "C-GALERKIN", "C-BOUNDS", "C-COMPACT")]
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1227",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M4", "remaining_root_cut_set": cut_set, "composition_certificates_checked": ["Stage1.THM_M_1227.isLerayHopfSolution_compose"], "audit_complete": False, "theorem_complete": False},
}
recipe_rows = [{"recipe_id": rid, "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-1227/Statement.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [ob]} for ob, rid in recipes.items()]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1227", "recipes": recipe_rows}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
