#!/usr/bin/env python3
"""Generate the frozen THM-M-0395 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0395-OBLIGATION_TREE"
THEOREM = "THM-M-0395"
STATEMENT_SHA = "de1bfb399ccec48a224e867c55f6eab12589e458949d6d409260be65f0920ba6"


def fp(formal_target: str) -> str:
    return "sha256:" + hashlib.sha256(formal_target.encode()).hexdigest()


# These are semantic units, not claims that the indicated mathematics has been formalized.
raw_nodes = [
    ("M0395-ROOT", "root", "Every selected Faltings curve over every number field has finitely many rational sections.",
     "Stage1Rev56.THMM0395.Statement", "The exact canonical proposition.", "split-required", "H1", "M4", "critical"),
    ("M0395-S", "definition", "Freeze the curve, rational-point, finiteness, universe, and foundation interfaces.",
     "Statement boundary package for Stage1Rev56.THMM0395.Statement", "An unambiguous target interface.", "split-required", "H1", "M3", "high"),
    ("M0395-S1", "definition", "A rational point is a section of the curve structure morphism over Spec K.",
     "Stage1Rev56.THMM0395.RationalPoint", "The rational-section type used by the root.", 4, "H1", "M3", "normal"),
    ("M0395-S2", "definition", "The selected curve carries smoothness, properness, geometric connectedness, dimension one, and genus at least two.",
     "Stage1Rev56.THMM0395.IsFaltingsCurve", "The exact conjunction of root hypotheses.", 6, "H1", "M3", "high"),
    ("M0395-S3", "transport", "Finiteness of rational points is equivalent to finiteness of their universal set.",
     "Stage1Rev56.THMM0395.finite_points_iff_finite_univ", "Checked finiteness encoding transport.", 3, "H1", "M0-L", "low"),
    ("M0395-N", "normalization", "Normalize the problem after a finite extension carrying a geometric point, while retaining an injection from C(K).",
     "planned: finite extension L/K, C(L) nonempty, and C(K) -> C(L) injective", "A pointed curve over a finite number-field extension.", "split-required", "H1", "M4", "critical"),
    ("M0395-N1", "bridge", "There is a finite extension L/K over which the geometrically connected curve has a rational point.",
     "planned: exists_finite_extension_with_curve_point", "A finite number-field extension L and a point P in C(L).", 9, "H1", "M4", "high"),
    ("M0395-N2", "transport", "Base extension sends K-rational points injectively to L-rational points and preserves the curve hypotheses.",
     "planned: rationalPoint_baseChange_injective_and_preserves_faltings", "An injection C(K) -> C_L(L) plus transported hypotheses.", 10, "H1", "M4", "high"),
    ("M0395-C", "construction", "A chosen L-point defines the Abel-Jacobi map from C_L to its Jacobian.",
     "planned: abelJacobi C_L P : C_L -> Jac(C_L)", "The Abel-Jacobi morphism based at P.", "split-required", "H1", "M4", "critical"),
    ("M0395-C1", "construction", "Construct the Jacobian of the smooth proper geometrically connected curve and its L-rational group.",
     "planned: jacobian_construction C_L", "An abelian variety J/L with group J(L).", 15, "H1", "M4", "critical"),
    ("M0395-C2", "bridge", "For genus at least two, the Abel-Jacobi map based at P is a closed immersion and injective on L-points.",
     "planned: abelJacobi_isClosedImmersion_and_point_injective", "An injection C_L(L) -> J(L) identifying points with the curve image.", 12, "H1", "M4", "critical"),
    ("M0395-L1", "core_lemma", "The Mordell-Weil theorem makes J(L) a finitely generated abelian group.",
     "planned: jacobian_rational_points_finitelyGenerated", "Finite generation of J(L).", 8, "H1", "M4", "critical"),
    ("M0395-X1", "bridge", "Mordell-Lang/Faltings for subvarieties of abelian varieties describes intersection with a finitely generated subgroup by finitely many cosets.",
     "planned: mordellLang_finite_coset_decomposition", "A finite coset decomposition of the Abel-Jacobi curve image intersected with J(L).", "split-required", "H1", "M4", "critical"),
    ("M0395-L2", "core_lemma", "A genus-at-least-two curve image in its Jacobian contains no translate of a positive-dimensional abelian subvariety.",
     "planned: abelJacobi_image_contains_no_positive_dimensional_coset", "Every coset occurring in the curve intersection is zero-dimensional.", 18, "H1", "M4", "critical"),
    ("M0395-L3", "core_lemma", "A finite union of zero-dimensional cosets contributes only finitely many L-rational points.",
     "planned: finite_of_finite_zeroDimensional_cosets", "Finiteness of the Abel-Jacobi image intersection with J(L).", 8, "H1", "M4", "normal"),
    ("M0395-T", "terminal", "Compose finite extension, Abel-Jacobi, Mordell-Weil, Mordell-Lang, and the no-coset lemma to prove C(K) finite.",
     "planned: faltings_terminal_composition : Stage1Rev56.THMM0395.Statement", "The exact root statement with no additional premise.", "split-required", "H1", "M4", "critical"),
    ("M0395-X2", "terminal", "Audit the terminal declaration's axioms, proof-body provenance, dependencies, and reproducibility boundary.",
     "planned: terminal trust and provenance certificate", "A release-gate trust report; it supplies no mathematical premise.", 10, "H1", "M4", "critical"),
]

obligations = []
nodes = []
for oid, kind, human, formal, output, budget, h, m, risk in raw_nodes:
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp(formal), "kind": kind,
        "root_relevant": True, "machine_eligibility": "required",
        "human_source_eligibility": "required", "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": None, "terminal_proof_body_id": None,
    })
    ledger = (f"Premises are exactly the incoming proof/refinement edges recorded for {oid}. "
              f"The planned inference is identified by `{formal}`. Output: {output} "
              "The output is used only by the recorded outgoing composition/refinement edges.")
    nodes.append({
        "node_id": f"THM-M-0395-{oid.removeprefix('M0395-')}", "obligation_id": oid,
        "kind": kind, "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": h, "machine_debt": m, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "source-crosswalk-audit-pending",
        "provenance_id": "local:Statement.lean" if oid.startswith("M0395-S") else "none",
        "foundation_profile": "lean4-mathlib/rev-5.6-audit-pending",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-0395/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-M0395-S3-LEAN" if oid == "M0395-S3" else "VAL-M0395-ARCH-STRUCTURE",
        "status_boundary": "Architecture and current debt only; this node has no admitted proof body unless its machine debt explicitly says M0-L.",
        "task_ids": [ITEM, "S56-M-0395-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0395/Statement.lean"] if oid.startswith("M0395-S") else [],
        "owner": "THM-M-0395 execution lane", "reviewer": "independent master integration lane",
        "validity": {"frozen_on": "2026-07-12", "review_due": "before proof acceptance",
                     "invalidate_on": ["canonical statement", "registry", "source map", "toolchain"],
                     "revocation_state": "none"},
    })

projection_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
                     "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                     "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in projection_fields} for row in obligations]
denominator_sha = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_against_statement_sha256": STATEMENT_SHA,
    "freeze_basis": "Exact statement and immutable anchor audit; eligibility was assigned without reading proof closure.",
    "root_obligation_id": "M0395-ROOT", "denominator_sha256": denominator_sha,
    "frozen_denominators": {"inventory": [x[0] for x in raw_nodes],
        "required_machine": [x[0] for x in raw_nodes], "required_human_source": [x[0] for x in raw_nodes],
        "required_readable": [x[0] for x in raw_nodes]},
    "append_only_deltas": [], "obligations": obligations,
    "status_boundary": "Seventeen obligations are frozen; eligibility and planned signatures do not imply closure."
}

proof_pairs = [
    ("M0395-ROOT", "M0395-T"),
    ("M0395-T", "M0395-N"), ("M0395-T", "M0395-C"), ("M0395-T", "M0395-L1"),
    ("M0395-T", "M0395-X1"), ("M0395-T", "M0395-L2"), ("M0395-T", "M0395-L3"),
    ("M0395-N", "M0395-N1"), ("M0395-N", "M0395-N2"),
    ("M0395-C", "M0395-C1"), ("M0395-C", "M0395-C2"),
]
refine_pairs = [("M0395-ROOT", "M0395-S"), ("M0395-S", "M0395-S1"),
                ("M0395-S", "M0395-S2"), ("M0395-S", "M0395-S3")]

def indexed(edges):
    incoming, outgoing = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    proof_edges.extend([
        {"edge_id": f"P{i:02d}R", "type": "proof_requires", "from": parent, "to": child,
         "reciprocal_edge_id": f"P{i:02d}C"},
        {"edge_id": f"P{i:02d}C", "type": "composes", "from": child, "to": parent,
         "reciprocal_edge_id": f"P{i:02d}R"},
    ])
refinement_edges = [{"edge_id": f"R{i:02d}", "type": "logical_decomposition", "from": a, "to": b}
                    for i, (a, b) in enumerate(refine_pairs, 1)]
provenance_edges = [{"edge_id": "PR01", "type": "provenance_of", "from": "M0395-X1", "to": "M0395-T"}]
trust_edges = [{"edge_id": "TR01", "type": "trusts", "from": "M0395-ROOT", "to": "M0395-X2"}]
documentation_edges = [{"edge_id": f"D{i:02d}", "type": "documents", "from": "M0395-S", "to": oid}
                       for i, (oid, *_) in enumerate(raw_nodes, 1) if oid != "M0395-S"]
workflow_edges = [
    {"edge_id": "W01", "type": "workflow_depends_on", "from": "M0395-T", "to": "M0395-ROOT"},
    {"edge_id": "W02", "type": "workflow_depends_on", "from": "M0395-X2", "to": "M0395-T"},
]
graphs = {
    "proof": indexed(proof_edges), "refinement": indexed(refinement_edges),
    "provenance": indexed(provenance_edges), "evidence": indexed([]), "trust": indexed(trust_edges),
    "documentation": indexed(documentation_edges), "workflow": indexed(workflow_edges),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "root_obligation_id": "M0395-ROOT", "registry_denominator_sha256": denominator_sha,
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M0395-S3"], "root_closed": False,
                         "theorem_complete": False, "remaining_root_cut_set": ["M0395-T"],
                         "reason": "The checked statement transport does not close any Faltings proof obligation."}
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")

specs = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [
        {"recipe_id": "VAL-M0395-ARCH-STRUCTURE", "cwd": ".",
         "argv": ["python3", "Stage1_Instances/THM-M-0395/check_obligation_tree.py"],
         "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0,
         "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0395 obligation tree"}],
         "covered_obligation_ids": [x[0] for x in raw_nodes if x[0] != "M0395-S3"],
         "covered_declarations": []},
        {"recipe_id": "VAL-M0395-S3-LEAN", "cwd": "Formalizations/Lean",
         "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0395/Statement.lean"],
         "env_allowlist": {}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0,
         "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains Stage1Rev56.THMM0395.Statement"}],
         "covered_obligation_ids": ["M0395-S3"],
         "covered_declarations": ["Stage1Rev56.THMM0395.finite_points_iff_finite_univ"]},
    ],
    "status_boundary": "The architecture recipe validates structure only. The Lean recipe checks the statement transport, not Faltings's theorem."
}
(HERE / "validation-specs.json").write_text(json.dumps(specs, indent=2) + "\n")
