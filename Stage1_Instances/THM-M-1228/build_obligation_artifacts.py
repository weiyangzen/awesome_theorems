#!/usr/bin/env python3
"""Build the frozen THM-M-1228 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1228-OBLIGATION_TREE"
PREFIX = "M1228-"

# short id, kind, risk, statement, formal target, output, H/M/R, step budget
SPECS = [
    ("ROOT", "root", "critical", "Every source-suitable weak three-dimensional Navier-Stokes solution has a singular set of zero one-dimensional parabolic Hausdorff measure.", "Stage1Instances.THMM1228.CaffarelliKohnNirenbergTarget", "The exact frozen CKN proposition.", "H1", "M4", "R4", 8),
    ("S-CONCRETE", "definition", "critical", "Replace the semantic suitability, regularity, and parabolic-measure parameters by source-faithful analytic definitions.", "planned: concrete CKNSourceSemantics instantiation and checked transport", "Concrete PDE and parabolic-geometry semantics.", "H1", "M5", "R4", 70),
    ("S-SUITABLE", "definition", "critical", "Define suitable weak solutions, including distributional equations, incompressibility, integrability, and the local energy inequality.", "planned: IsSuitableWeakSolutionConcrete", "A source-faithful suitability predicate.", "H1", "M5", "R4", 90),
    ("S-REGULAR", "definition", "high", "Define regular points with the source's local boundedness or Holder regularity convention.", "planned: RegularAtConcrete", "A source-faithful regular-point predicate.", "H1", "M5", "R4", 55),
    ("G-PARABOLIC", "construction", "critical", "Construct backward parabolic cylinders, scaling, coverings, and one-dimensional parabolic Hausdorff measure.", "planned: ParabolicHausdorffOneMeasureZeroConcrete", "The anisotropic measure notion used by CKN.", "H1", "M5", "R4", 95),
    ("E-EPSILON", "core_lemma", "critical", "Prove the scale-invariant epsilon-regularity criterion for suitable weak solutions.", "planned: ckn_epsilon_regularity", "Small scale-invariant energy implies local regularity.", "H1", "M5", "R4", 95),
    ("D-DECAY", "core_lemma", "critical", "Establish the compactness and decay estimate driving epsilon regularity.", "planned: ckn_decay", "Quantitative decay below a universal threshold.", "H1", "M5", "R4", 95),
    ("C-COVER", "core_lemma", "critical", "Cover the singular set by bad parabolic cylinders and control their one-dimensional content.", "planned: singular_covering", "Arbitrarily small parabolic one-content covers.", "H1", "M5", "R4", 85),
    ("L-MEASURE", "core_lemma", "critical", "Convert the covering estimate into zero one-dimensional parabolic Hausdorff measure of the singular set.", "planned: singularSet_parabolicHausdorffOneMeasureZero", "The per-solution terminal measure conclusion.", "H1", "M5", "R4", 65),
    ("T-PERSOLUTION", "terminal", "critical", "Generalize the terminal measure conclusion over every suitable solution.", "Stage1Instances.THMM1228.ObligationTree.SingularMeasureConclusion", "The per-solution family consumed by root composition.", "H1", "M5", "R4", 20),
    ("T-ASSEMBLE", "terminal", "high", "Check the per-solution binder composition against a structural mirror of the exact canonical target.", "Stage1Instances.THMM1228.ObligationTree.root_compose", "The root-shaped harness, conditional on the open analytic family.", "H1", "M1", "R3", 10),
    ("X-SOURCE", "source_boundary", "high", "Pinpoint and independently review primary-source definitions, lemmas, theorem, assumptions, and errata.", "primary CKN source crosswalk remains open", "Node-specific human-source mappings.", "H1", "M5", "R4", 30),
    ("X-PROVENANCE", "provenance_boundary", "high", "Record immutable terminal proof-body provenance for every integrated formal candidate.", "anchor-audit.json: no exact terminal candidate", "Transitive formal provenance closure.", "H1", "M4", "R4", 25),
    ("X-TCB", "trust_boundary", "high", "Audit Lean, mathlib, axioms, imported artifacts, and executable trust closure.", "Lean 4.29.0; mathlib 8a178386; release closure open", "Release-grade trust inventory.", "H1", "M3", "R4", 25),
    ("X-DOC", "documentation_boundary", "normal", "Produce a readable node-by-node reconstruction distinguishing analytic work from logical assembly.", "obligation-tree.md and later readable proof", "Public proof reconstruction.", "H1", "M5", "R4", 30),
]


def oid(short):
    return PREFIX + short


def sha(value):
    return hashlib.sha256(value).hexdigest()


statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
overlays = {"X-SOURCE", "X-PROVENANCE", "X-TCB", "X-DOC"}
no_human = {"T-ASSEMBLE", "X-PROVENANCE", "X-TCB", "X-DOC"}
body_ids = {
    "T-ASSEMBLE": "repo:Stage1Instances.THMM1228.ObligationTree.root_compose",
}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fingerprint = ("lean-expression-sha256:" + expression_hash) if short == "ROOT" else \
        "planned:v1:sha256:" + sha((human + "\n" + formal).encode())
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fingerprint,
        "kind": kind, "root_relevant": short not in overlays,
        "machine_eligibility": "informational" if short in overlays else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None, "terminal_proof_body_id": body_ids.get(short),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode())
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": "THM-M-1228", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated semantic-interface target and bounded immutable anchor audit fix the source-definition, epsilon-regularity, decay, covering, measure, composition, and boundary obligations before proof closure is observed.",
    "frozen_against_statement_sha256": sha((HERE / "statement.json").read_bytes()),
    "frozen_against_anchor_audit_sha256": sha((HERE / "anchor-audit.json").read_bytes()),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, eligibility, exclusion, or risk change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": rows,
}

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-1228-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd,
        "evidence_ids": [],
        "source_crosswalk_id": "SRC-M1228-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M1228-ANCHOR-AUDIT" if short in {"ROOT", "X-PROVENANCE"} else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib; concrete analytic definitions and axiom inventory remain open",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none credited", "step_budget": budget,
        "semantic_step_ledger": {"premises": ["typed proof/refinement children"], "inference": formal, "output": output, "outgoing_use": "typed parent edge or root result"},
        "public_readable_target": "Stage1_Instances/THM-M-1228/obligation-tree.md#" + short.lower(),
        "validation_spec_id": "VAL-M1228-" + short,
        "status_boundary": "Architecture only; no analytic obligation is credited closed by this phase.",
        "task_ids": [ITEM, "S56-M-1228-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1228/obligation-registry.json", "Stage1_Instances/THM-M-1228/typed-graphs.json"],
        "owner": "Stage1 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "toolchain", "mathlib revision", "anchor provenance", "source interpretation"], "revocation_state": "not-accepted"},
    })


def graph(edges):
    out, incoming = {}, {}
    for edge in edges:
        out.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": out, "in": incoming}


proof_pairs = [("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "T-PERSOLUTION"), ("T-PERSOLUTION", "L-MEASURE"), ("L-MEASURE", "C-COVER"), ("C-COVER", "E-EPSILON"), ("E-EPSILON", "D-DECAY"), ("E-EPSILON", "S-SUITABLE"), ("L-MEASURE", "G-PARABOLIC"), ("T-PERSOLUTION", "S-REGULAR")]
proof_edges = []
for parent, child in proof_pairs:
    fwd, rev = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges += [{"edge_id": fwd, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": rev}, {"edge_id": rev, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": fwd}]
refine_pairs = [("ROOT", "S-CONCRETE"), ("S-CONCRETE", "S-SUITABLE"), ("S-CONCRETE", "S-REGULAR"), ("S-CONCRETE", "G-PARABOLIC"), ("E-EPSILON", "D-DECAY"), ("L-MEASURE", "C-COVER")]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refine_pairs]),
    "provenance": graph([{"edge_id": "PROV-ROOT", "from": oid("ROOT"), "type": "provenance_of", "to": oid("X-PROVENANCE")}, {"edge_id": "SOURCE-ROOT", "from": oid("ROOT"), "type": "source_map", "to": oid("X-SOURCE")}]),
    "evidence": graph([{"edge_id": "EVID-ASSEMBLE", "from": oid("T-ASSEMBLE"), "type": "evidence_for", "to": oid("ROOT")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": "DOC-ROOT", "from": oid("ROOT"), "type": "documents", "to": oid("X-DOC")}]),
    "workflow": graph([{"edge_id": "FLOW-ROOT-ASSEMBLE", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")}, {"edge_id": "FLOW-PROOF-SOURCE", "from": oid("T-PERSOLUTION"), "type": "workflow_depends_on", "to": oid("X-SOURCE")}]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1228",
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "root_machine_debt": "M4", "remaining_root_cut_set": [oid("S-CONCRETE"), oid("E-EPSILON"), oid("C-COVER"), oid("L-MEASURE")], "composition_certificates_checked": ["Stage1Instances.THMM1228.ObligationTree.root_compose", "Stage1Instances.THMM1228.ObligationTree.per_solution_expands"], "audit_complete": False, "theorem_complete": False},
}
recipes = [{"recipe_id": "VAL-M1228-" + spec[0], "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-1228/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid(spec[0])]} for spec in SPECS]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1228", "recipes": recipes}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(rows)} obligations, {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
