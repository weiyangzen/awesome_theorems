#!/usr/bin/env python3
"""Deterministically build the THM-M-0394 frozen architecture artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0394-OBLIGATION_TREE"
THEOREM = "THM-M-0394"
STATEMENT_SHA = "7db337b7285aa5908d1504574e09bb3ba02d13bdada499da93f3d79035a27cc8"
ANCHOR_SHA = "df9a793baac554282ef893604e3b51378b8845ce2cf94dc645ecfc880ae9e55a"


def fingerprint(formal_target):
    return "sha256:" + hashlib.sha256(formal_target.encode()).hexdigest()


# Planned signatures identify semantic units; they are not declarations or proof claims.
raw_nodes = [
    ("M0394-ROOT", "root", "Siegel's theorem for the frozen number-field affine-curve model.",
     "Stage1Rev56.THMM0394.Statement", "The exact canonical proposition.", "split-required", "critical", "M3"),
    ("M0394-S", "definition", "Freeze the curve, completion, boundary, coordinate, and S-integrality interfaces.",
     "Stage1Rev56.THMM0394.CurveModel / IsSiegelCurve / IsSIntegral", "The target's exact object-model boundary.", "split-required", "high", "M3"),
    ("M0394-S1", "transport", "Expand the ordered binders and exact root conclusion.",
     "Stage1Rev56.THMM0394.statement_iff_expanded", "A checked exact-statement transport.", 3, "low", "M0-L"),
    ("M0394-S2", "transport", "Expand integral-point membership into coordinatewise S-integrality.",
     "Stage1Rev56.THMM0394.mem_integralPointSet_iff", "A checked integrality-definition transport.", 4, "normal", "M0-L"),
    ("M0394-S3", "definition", "The geometric hypothesis splits into positive genus or genus zero with at least three boundary points.",
     "Stage1Rev56.THMM0394.IsSiegelCurve", "The exhaustive canonical branch predicate.", 6, "high", "M3"),
    ("M0394-N", "normalization", "Relate the explicit compatibility predicates to genuine curve genus, geometric complement, and affine embedding semantics.",
     "planned: curveModel_semantic_realization", "A model whose explicit fields carry their intended mathematical meaning.", "split-required", "critical", "M4"),
    ("M0394-N1", "bridge", "Integral-point finiteness is invariant under admissible changes of affine coordinates and integral model.",
     "planned: integralPointSet_finite_model_independent", "Transfer finiteness from a proof-compatible model to the frozen model.", 18, "critical", "M4"),
    ("M0394-B", "branch", "Exhaust the positive-genus and genus-zero alternatives and recombine their conclusions.",
     "Stage1Rev56.THMM0394.ObligationTree.branch_composition", "Finiteness after consuming both exact branch theorems.", 8, "critical", "M0-L"),
    ("M0394-B1", "branch", "Positive-genus Siegel branch for the frozen integral-point set.",
     "Stage1Rev56.THMM0394.ObligationTree.PositiveGenusBranch", "Finiteness when the completion has positive genus.", "split-required", "critical", "M4"),
    ("M0394-B2", "branch", "Genus-zero Siegel branch with at least three geometric boundary points.",
     "Stage1Rev56.THMM0394.ObligationTree.GenusZeroBranch", "Finiteness in the three-boundary-point case.", "split-required", "critical", "M4"),
    ("M0394-C1", "construction", "Construct the divisor, height, and approximation data needed by the positive-genus proof.",
     "planned: positive_genus_height_package", "A height/approximation package compatible with S-integrality.", "split-required", "critical", "M4"),
    ("M0394-L1", "core_lemma", "The positive-genus Diophantine approximation argument bounds the relevant integral points.",
     "planned: positive_genus_integral_points_finite", "Closure of PositiveGenusBranch.", "split-required", "critical", "M4"),
    ("M0394-C2", "construction", "Choose a rational parameter on the genus-zero completion and track the boundary to 0, 1, and infinity after finite extension.",
     "planned: genus_zero_three_boundary_parameter", "A reduction of integral points to an S-unit equation.", "split-required", "critical", "M4"),
    ("M0394-L2", "core_lemma", "The parameter reduction maps frozen integral points into finitely many solutions of an S-unit equation with finite fibers.",
     "planned: integral_points_reduce_to_sunit_equation", "A finite-fiber reduction for the genus-zero branch.", "split-required", "critical", "M4"),
    ("M0394-X1", "bridge", "The S-unit equation u + v = 1 has finitely many solutions over a number field with fixed S.",
     "planned: sunit_equation_finite", "The external arithmetic finiteness engine.", "split-required", "critical", "M4"),
    ("M0394-T", "terminal", "Compose semantic realization, model invariance, the two branch closures, and checked branch recomposition.",
     "planned: siegel_terminal : Stage1Rev56.THMM0394.Statement", "The exact canonical root without extra premises.", "split-required", "critical", "M4"),
    ("M0394-X2", "terminal", "Audit terminal declarations, proof bodies, axioms, provenance, imports, and reproducibility.",
     "planned: terminal trust/provenance certificate", "A release-gate report, not a mathematical premise.", 12, "critical", "M4"),
]

obligations = []
nodes = []
for oid, kind, human, formal, output, budget, risk, machine in raw_nodes:
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(formal), "kind": kind,
        "root_relevant": True, "machine_eligibility": "required",
        "human_source_eligibility": "required", "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": None,
        "terminal_proof_body_id": "local:ObligationTree.lean:branch_composition" if oid == "M0394-B" else None,
    })
    local = oid in {"M0394-S", "M0394-S1", "M0394-S2", "M0394-S3", "M0394-B"}
    nodes.append({
        "node_id": "THM-M-0394-" + oid.removeprefix("M0394-"), "obligation_id": oid,
        "kind": kind, "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H3", "machine_debt": machine, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-pinpoint-pending",
        "provenance_id": "local:Statement.lean" if local else "none",
        "foundation_profile": "lean4-mathlib/rev-5.6-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": (
            f"Premises are the incoming proof/refinement edges for {oid}. The planned inference is `{formal}`. "
            f"Output: {output} The output is consumed only through the recorded typed edges."),
        "public_readable_target": f"Stage1_Instances/THM-M-0394/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-M0394-COMPOSITION-LEAN" if oid == "M0394-B" else "VAL-M0394-ARCH-STRUCTURE",
        "status_boundary": "This record freezes architecture and current debt; planned signatures and M3/M4 nodes have no proof body.",
        "task_ids": [ITEM, "S56-M-0394-PROOF"],
        "owned_sources": (["Stage1_Instances/THM-M-0394/Statement.lean"] if local else []) +
                         (["Stage1_Instances/THM-M-0394/ObligationTree.lean"] if oid == "M0394-B" else []),
        "owner": "THM-M-0394 execution lane", "reviewer": "independent master integration lane",
        "validity": {"frozen_on": "2026-07-12", "review_due": "before proof acceptance",
                     "invalidate_on": ["canonical statement", "registry", "anchor audit", "source map", "toolchain"],
                     "revocation_state": "none"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
          "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator_sha = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row[0] for row in raw_nodes]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_against_statement_sha256": STATEMENT_SHA,
    "frozen_against_anchor_audit_sha256": ANCHOR_SHA,
    "freeze_basis": "The exact elaborated statement and completed immutable anchor audit; eligibility does not depend on closure status.",
    "root_obligation_id": "M0394-ROOT", "denominator_sha256": denominator_sha,
    "frozen_denominators": {key: ids for key in ("inventory", "required_machine", "required_human_source", "required_readable")},
    "append_only_deltas": [], "obligations": obligations,
    "status_boundary": "Seventeen semantic obligations are frozen. This denominator and its planned signatures grant no proof credit."
}


def indexed(edges):
    incoming, outgoing = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


proof_pairs = [
    ("M0394-ROOT", "M0394-T"), ("M0394-T", "M0394-N"), ("M0394-T", "M0394-N1"),
    ("M0394-T", "M0394-B"), ("M0394-T", "M0394-B1"), ("M0394-T", "M0394-B2"),
    ("M0394-B1", "M0394-C1"), ("M0394-B1", "M0394-L1"),
    ("M0394-B2", "M0394-C2"), ("M0394-B2", "M0394-L2"), ("M0394-B2", "M0394-X1"),
]
proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    proof_edges += [
        {"edge_id": f"P{i:02d}R", "type": "proof_requires", "from": parent, "to": child,
         "reciprocal_edge_id": f"P{i:02d}C"},
        {"edge_id": f"P{i:02d}C", "type": "composes", "from": child, "to": parent,
         "reciprocal_edge_id": f"P{i:02d}R"},
    ]
refinement_pairs = [("M0394-ROOT", "M0394-S"), ("M0394-S", "M0394-S1"),
                    ("M0394-S", "M0394-S2"), ("M0394-S", "M0394-S3")]
refinement = [{"edge_id": f"R{i:02d}", "type": "logical_decomposition", "from": a, "to": b}
              for i, (a, b) in enumerate(refinement_pairs, 1)]
provenance = [
    {"edge_id": "PR01", "type": "provenance_of", "from": "M0394-B", "to": "M0394-T"},
    {"edge_id": "PR02", "type": "provenance_of", "from": "M0394-X1", "to": "M0394-B2"},
]
trust = [{"edge_id": "TR01", "type": "trusts", "from": "M0394-ROOT", "to": "M0394-X2"}]
docs = [{"edge_id": f"D{i:02d}", "type": "documents", "from": "M0394-S", "to": oid}
        for i, oid in enumerate(ids, 1) if oid != "M0394-S"]
workflow = [
    {"edge_id": "W01", "type": "workflow_depends_on", "from": "M0394-T", "to": "M0394-ROOT"},
    {"edge_id": "W02", "type": "workflow_depends_on", "from": "M0394-X2", "to": "M0394-T"},
]
graphs = {"proof": indexed(proof_edges), "refinement": indexed(refinement),
          "provenance": indexed(provenance), "evidence": indexed([]), "trust": indexed(trust),
          "documentation": indexed(docs), "workflow": indexed(workflow)}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "root_obligation_id": "M0394-ROOT", "registry_denominator_sha256": denominator_sha,
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M0394-S1", "M0394-S2", "M0394-B"],
                         "root_closed": False, "theorem_complete": False,
                         "remaining_root_cut_set": ["M0394-T"],
                         "reason": "Definition transports and conditional branch composition do not prove either Siegel branch."}
}
specs = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [
        {"recipe_id": "VAL-M0394-ARCH-STRUCTURE", "cwd": ".",
         "argv": ["python3", "Stage1_Instances/THM-M-0394/check_obligation_tree.py"],
         "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0,
         "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0394 obligation tree"}],
         "covered_obligation_ids": [oid for oid in ids if oid != "M0394-B"], "covered_declarations": []},
        {"recipe_id": "VAL-M0394-COMPOSITION-LEAN", "cwd": "Formalizations/Lean",
         "argv": ["bash", "../../Stage1_Instances/THM-M-0394/check_composition.sh"],
         "env_allowlist": {}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0,
         "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains branch_composition"}],
         "covered_obligation_ids": ["M0394-B"],
         "covered_declarations": ["Stage1Rev56.THMM0394.ObligationTree.branch_composition"]},
    ],
    "status_boundary": "The Lean recipe checks only a conditional child-to-parent composition theorem; no branch premise is asserted."
}

for name, data in (("obligation-registry.json", registry), ("typed-graphs.json", bundle),
                   ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(data, indent=2) + "\n")
