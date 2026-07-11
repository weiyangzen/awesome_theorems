#!/usr/bin/env python3
"""Generate the frozen THM-M-0396 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0396-OBLIGATION_TREE"
THEOREM = "THM-M-0396"
STATEMENT_SHA = "adc9e134e2e2164064f33d35c056fd66aac052127dff858fa5b4b3de4ad9d094"
ANCHOR_SHA = "22655612476feb1a835e5e3524a81e8eed92744d46825b659c21c8f273e1beef"


def fingerprint(target: str) -> str:
    return "sha256:" + hashlib.sha256(target.encode()).hexdigest()


# This architecture is frozen independently of proof availability.  Planned
# signatures describe obligations; they are not Lean declarations or evidence.
RAW = [
    ("M0396-ROOT", "root", "The exact frozen real multiplicative Matveev lower bound holds for every admitted parameter tuple.", "Stage1Rev56.THMM0396.Statement", "The unchanged canonical proposition.", "split-required", "H1", "M3", "critical"),
    ("M0396-S1", "definition", "The algebraic product, nonzero linear-form value, explicit exponent bound, and normalized logarithmic height have the meanings fixed in Statement.lean.", "Stage1Rev56.THMM0396.algebraicProduct + linearFormValue + exponentBound", "The exact terms occurring in the root.", 6, "H1", "M3", "high"),
    ("M0396-S2", "transport", "The parameterwise CoreEstimate is logically equivalent to the fully quantified canonical Statement.", "Stage1Rev56.THMM0396.ObligationTree.core_iff_statement", "A checked binder-preserving transport to the root.", 2, "H1", "M0-L", "normal"),
    ("M0396-S3", "branch", "The nonvanishing hypothesis excludes the all-zero coefficient boundary case.", "Stage1Rev56.THMM0396.linearFormValue_eq_zero_of_coeff_zero", "At least one coefficient is nonzero whenever the root hypotheses hold.", 3, "H1", "M0-L", "normal"),
    ("M0396-N1", "normalization", "Replace each positive embedded algebraic number by its unambiguous real logarithm and relate the exponential of the additive form to the algebraic product.", "planned: exp_sum_coeff_log_eq_algebraicProduct", "An additive logarithmic form L with exp L = algebraicProduct.", 12, "H1", "M4", "critical"),
    ("M0396-N2", "reduction", "Normalize degree, coefficient, height, and positivity parameters to the hypotheses required by the determinant estimate without strengthening the root assumptions.", "planned: matveev_parameter_normalization", "Admissible normalized data with the same Lambda and no larger claimed bound.", 16, "H1", "M4", "critical"),
    ("M0396-C1", "construction", "Construct the auxiliary interpolation determinant and its integer index sets from the normalized parameters.", "planned: matveev_auxiliary_determinant", "A square auxiliary determinant with controlled dimension and multiplicities.", "split-required", "H1", "M4", "critical"),
    ("M0396-C2", "construction", "Prove the auxiliary determinant is nonzero using the required zero estimate and rank argument.", "planned: matveev_auxiliary_determinant_ne_zero", "Nonvanishing of the determinant used by both estimates.", "split-required", "H1", "M4", "critical"),
    ("M0396-L1", "core_lemma", "Bound the logarithmic heights of every algebraic entry and determinant conjugate in terms of D, B, and the product of the A_i.", "planned: auxiliary_determinant_height_bound", "A global arithmetic height bound for the determinant.", 30, "H1", "M4", "critical"),
    ("M0396-L2", "core_lemma", "Apply an algebraic lower-bound principle to the nonzero determinant using its degree and height controls.", "planned: auxiliary_determinant_arithmetic_lower_bound", "A quantitative lower bound for the determinant absolute value.", 24, "H1", "M4", "critical"),
    ("M0396-L3", "core_lemma", "Use interpolation and analytic estimates to upper-bound the same determinant under a hypothetical excessively small nonzero Lambda.", "planned: auxiliary_determinant_analytic_upper_bound", "An upper bound contradicting M0396-L2 below the explicit threshold.", "split-required", "H1", "M4", "critical"),
    ("M0396-L4", "core_lemma", "Choose and round all auxiliary integer parameters and verify the numerical inequalities producing the frozen constant 1.4 * 30^(n+3) * n^(9/2).", "planned: matveev_explicit_constant_optimization", "The exact exponentBound constant and strict inequality, with rounding errors discharged.", "split-required", "H1", "M4", "critical"),
    ("M0396-T", "terminal", "Combine normalization, determinant nonvanishing, arithmetic and analytic estimates, and constant optimization to prove CoreEstimate for every parameter tuple.", "planned: matveev_terminal_estimate", "The exact parameterwise CoreEstimate consumed by root_compose.", "split-required", "H1", "M4", "critical"),
    ("M0396-X1", "terminal", "Identify and audit the exact primary theorem, page, conventions, assumptions, and errata corresponding to every mathematical proof node.", "policy: pinpoint primary-source crosswalk", "Accepted node-specific human-source mapping; no machine-proof premise.", 12, "H1", "not_applicable", "critical"),
    ("M0396-X2", "terminal", "Audit the future terminal declaration's body provenance, transitive dependencies, axioms, TCB, computation policy, and reproducible validation closure.", "policy: terminal trust and provenance certificate", "A release trust receipt; no mathematical proof premise.", 12, "H1", "M4", "critical"),
]

obligations = []
nodes = []
for oid, kind, human, formal, output, budget, hdebt, mdebt, risk in RAW:
    machine_eligibility = "not_applicable" if mdebt == "not_applicable" else "required"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(formal), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine_eligibility,
        "human_source_eligibility": "required", "readable_eligibility": "required",
        "risk_class": risk, "exclusion_reason": "human-source policy obligation has no Lean proof target" if oid == "M0396-X1" else None,
        "terminal_proof_body_id": "local:ObligationTree.lean:core_iff_statement" if oid == "M0396-S2" else
                                  "local:Statement.lean:linearFormValue_eq_zero_of_coeff_zero" if oid == "M0396-S3" else None,
    })
    validation = "VAL-M0396-COMPOSITION-LEAN" if oid in ("M0396-S1", "M0396-S2", "M0396-S3") else "VAL-M0396-ARCH-STRUCTURE"
    nodes.append({
        "node_id": "THM-M-0396-" + oid.removeprefix("M0396-"), "obligation_id": oid,
        "kind": kind, "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hdebt, "machine_debt": mdebt, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "anchor-audit:H1-primary-pinpoint-open",
        "provenance_id": "local:Statement.lean" if oid.startswith("M0396-S") else "none",
        "foundation_profile": "lean4-mathlib/rev-5.6; classical/choice use pending terminal body",
        "tcb_profile": "lean-4.29.0/mathlib-8a178386; terminal transitive closure pending",
        "computation_record": "none; no oracle or certificate is credited",
        "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "exact incoming typed proof/refinement edges for " + oid,
            "inference": formal,
            "output": output,
            "outgoing_use": "only the recorded typed outgoing edges"
        },
        "public_readable_target": "Stage1_Instances/THM-M-0396/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": validation,
        "status_boundary": "Frozen architecture/current debt only; no proof is claimed unless machine_debt is M0-L.",
        "task_ids": [ITEM, "S56-M-0396-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0396/Statement.lean"] if oid.startswith("M0396-S") else [],
        "owner": "THM-M-0396 execution lane", "reviewer": "independent master integration lane",
        "validity": {"frozen_on": "2026-07-12", "review_due": "before proof acceptance",
                     "invalidate_on": ["canonical statement", "registry", "source map", "toolchain", "dependency revisions"],
                     "revocation_state": "none"}
    })

projection_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
                     "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                     "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in projection_fields} for row in obligations]
denominator_sha = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
all_ids = [row[0] for row in RAW]
machine_ids = [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_against_statement_sha256": STATEMENT_SHA,
    "frozen_against_anchor_audit_sha256": ANCHOR_SHA,
    "freeze_basis": "The elaborated statement and completed anchor audit; eligibility is architectural and does not depend on closure.",
    "root_obligation_id": "M0396-ROOT", "denominator_sha256": denominator_sha,
    "frozen_denominators": {"inventory": all_ids, "required_machine": machine_ids,
                            "required_human_source": all_ids, "required_readable": all_ids},
    "append_only_deltas": [], "obligations": obligations,
    "status_boundary": "Fifteen semantic obligations are frozen. Planned signatures and eligibility do not imply proof closure."
}

proof_pairs = [
    ("M0396-ROOT", "M0396-T"),
    ("M0396-T", "M0396-N1"), ("M0396-T", "M0396-N2"),
    ("M0396-T", "M0396-C1"), ("M0396-T", "M0396-C2"),
    ("M0396-T", "M0396-L1"), ("M0396-T", "M0396-L2"),
    ("M0396-T", "M0396-L3"), ("M0396-T", "M0396-L4"),
]
refinement_pairs = [("M0396-ROOT", "M0396-S1"), ("M0396-ROOT", "M0396-S2"),
                    ("M0396-ROOT", "M0396-S3")]


def indexed(edges):
    incoming, outgoing = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


proof_edges = []
for index, (parent, child) in enumerate(proof_pairs, 1):
    proof_edges.extend([
        {"edge_id": f"P{index:02d}R", "type": "proof_requires", "from": parent, "to": child,
         "reciprocal_edge_id": f"P{index:02d}C"},
        {"edge_id": f"P{index:02d}C", "type": "composes", "from": child, "to": parent,
         "reciprocal_edge_id": f"P{index:02d}R"},
    ])
refinement_edges = [{"edge_id": f"R{i:02d}", "type": "logical_decomposition", "from": a, "to": b}
                    for i, (a, b) in enumerate(refinement_pairs, 1)]
graphs = {
    "proof": indexed(proof_edges),
    "refinement": indexed(refinement_edges),
    "provenance": indexed([
        {"edge_id": "PR01", "type": "provenance_of", "from": "M0396-S1", "to": "M0396-ROOT"},
        {"edge_id": "PR02", "type": "source_map", "from": "M0396-X1", "to": "M0396-T"},
    ]),
    "evidence": indexed([]),
    "trust": indexed([{"edge_id": "TR01", "type": "trusts", "from": "M0396-ROOT", "to": "M0396-X2"}]),
    "documentation": indexed([{"edge_id": f"D{i:02d}", "type": "documents", "from": "M0396-S1", "to": oid}
                               for i, oid in enumerate(all_ids, 1) if oid != "M0396-S1"]),
    "workflow": indexed([
        {"edge_id": "W01", "type": "workflow_depends_on", "from": "task:S56-M-0396-OBLIGATION_TREE", "to": "task:S56-M-0396-ANCHOR_AUDIT"},
        {"edge_id": "W02", "type": "workflow_depends_on", "from": "task:S56-M-0396-PROOF", "to": "task:S56-M-0396-OBLIGATION_TREE"},
        {"edge_id": "W03", "type": "workflow_depends_on", "from": "task:S56-M-0396-VALIDATION", "to": "task:S56-M-0396-PROOF"},
        {"edge_id": "W04", "type": "workflow_depends_on", "from": "task:S56-M-0396-RELEASE", "to": "task:S56-M-0396-VALIDATION"},
    ]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "root_obligation_id": "M0396-ROOT", "registry_denominator_sha256": denominator_sha,
    "nodes": nodes, "graphs": graphs,
    "composition_certificates": [{
        "parent": "M0396-ROOT", "required_child": "M0396-T",
        "declaration": "Stage1Rev56.THMM0396.ObligationTree.root_compose",
        "state": "conditional_kernel_checked", "boundary": "Consumes CoreEstimate as a premise; does not close M0396-T."
    }],
    "closure_boundary": {"closed_obligations": ["M0396-S2", "M0396-S3"], "root_closed": False,
                         "audit_complete": False, "theorem_complete": False,
                         "remaining_root_cut_set": ["M0396-T"],
                         "reason": "No terminal Baker-Matveev proof body was located or implemented."}
}

specs = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [
        {"recipe_id": "VAL-M0396-ARCH-STRUCTURE", "cwd": ".",
         "argv": ["python3", "Stage1_Instances/THM-M-0396/check_obligation_tree.py"],
         "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0,
         "covered_obligation_ids": [oid for oid in all_ids if oid not in ("M0396-S1", "M0396-S2", "M0396-S3")],
         "covered_declarations": [], "claim_boundary": "schema and graph structure only"},
        {"recipe_id": "VAL-M0396-COMPOSITION-LEAN", "cwd": "Formalizations/Lean",
         "argv": ["bash", "-c", "tmp=$(mktemp -d ./.m0396-obligation.XXXXXX); trap 'rm -rf \"$tmp\"' EXIT; cp ../../Stage1_Instances/THM-M-0396/Statement.lean ../../Stage1_Instances/THM-M-0396/ObligationTree.lean \"$tmp/\"; lake env lean -o \"$tmp/Statement.olean\" \"$tmp/Statement.lean\" && LEAN_PATH=\"$tmp:$(lake env printenv LEAN_PATH)\" lake env lean \"$tmp/ObligationTree.lean\""],
         "env_allowlist": {}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0,
         "covered_obligation_ids": ["M0396-S1", "M0396-S2", "M0396-S3"],
         "covered_declarations": ["Stage1Rev56.THMM0396.ObligationTree.root_compose", "Stage1Rev56.THMM0396.ObligationTree.core_iff_statement"],
         "claim_boundary": "conditional binder composition and statement-layer checks only"},
    ],
    "status_boundary": "Neither recipe proves the terminal estimate or canonical root."
}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle),
                    ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
