#!/usr/bin/env python3
"""Build the frozen THM-M-0498 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0498-OBLIGATION_TREE"
THEOREM = "THM-M-0498"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("M0498-ROOT", "root", "critical", "The exact multiplicity-weighted Chebyshev psi explicit formula.", "Stage1Instances.THM_M_0498.RiemannVonMangoldtTarget", "The canonical proposition."),
    ("M0498-S-ZEROS", "definition", "critical", "Freeze the complete injective multiplicity-aware height ordering of nontrivial zeta zeros.", "Stage1Instances.THM_M_0498.NontrivialZeroEnumeration", "The exact zero-family and summation convention."),
    ("M0498-S-ENDPOINT", "definition", "high", "Freeze x > 1, exclusion of prime powers, and the right-continuous Chebyshev psi convention.", "Stage1Instances.THM_M_0498.IsNotPrimePower", "The exact domain and endpoint convention."),
    ("M0498-S-FOUNDATION", "certificate", "critical", "Inventory classical choice, complex powers and logarithms, meromorphic order, transitive imports, axioms, TCB, and computation policy.", "planned exact foundation and trust report", "An accepted foundation and TCB boundary."),
    ("M0498-A-DIRICHLET", "bridge", "critical", "Identify the logarithmic derivative of zeta with the von Mangoldt Dirichlet series in its convergence half-plane.", "planned wrapper around ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div", "The arithmetic-to-analytic Dirichlet-series identity."),
    ("M0498-A-PERRON", "reduction", "critical", "Derive a truncated Perron or inverse-Mellin representation for Chebyshev psi away from discontinuities.", "planned Lean inverse-Mellin/Perron theorem", "A vertical-line integral with controlled truncation error."),
    ("M0498-C-CONTOUR", "construction", "critical", "Construct admissible rectangular contours avoiding zeros and prove the horizontal and left-edge bounds needed for contour shift.", "planned contour family and analytic estimates", "A contour-shift sequence with vanishing boundary errors."),
    ("M0498-B-RESIDUES", "branch", "critical", "Compute separately the residues at s = 1, nontrivial zeros with meromorphic multiplicity, trivial zeros, and the s = 0 logarithmic contribution.", "planned residue decomposition", "The x, zero-sum, log(2*pi), and log(1-x^-2) terms with correct signs."),
    ("M0498-L-TRIVIAL", "lemma", "high", "Sum the trivial-zero residues and normalize branches of complex power and logarithm.", "planned trivial-zero series evaluation", "The correction term -(1/2) log(1-x^-2)."),
    ("M0498-L-ZERO-SUM", "core_lemma", "critical", "Prove convergence under nondecreasing absolute imaginary height and invariance for every allowed complete enumeration.", "planned symmetric nontrivial-zero sum convergence theorem", "The canonical Tendsto zero-sum convention."),
    ("M0498-T-ANALYTIC", "terminal", "critical", "Assemble Perron inversion, contour limits, residues, trivial zeros, and zero-sum convergence into the pointwise explicit formula.", "Stage1Instances.THM_M_0498.AnalyticExplicitFormulaPackage", "ExplicitFormulaAt E x for every admissible E and x."),
    ("M0498-T-ASSEMBLE", "transport", "high", "Compose the analytic package with the frozen definitions into the exact canonical root.", "Stage1Instances.THM_M_0498.root_of_analytic_package", "The exact canonical proposition, conditional on the analytic package."),
    ("M0498-X-SOURCE", "source_boundary", "high", "Map each analytic step, convention, and residue computation to reviewed primary-source theorem/page/assumption/errata passages.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M0498-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, wrappers, imports, declaration closure, axioms, TCB, licenses, and replay evidence.", "planned machine-derived provenance and trust closure", "Release provenance without mathematical proof credit."),
    ("M0498-X-PI-TRANSFER", "excluded_transport", "medium", "Transfer the weighted psi formula to an ordinary prime-counting pi formula by normalization and Mobius inversion.", "future distinct checked transport", "An explicitly excluded linked variant."),
]

checked = {"M0498-S-ZEROS", "M0498-S-ENDPOINT", "M0498-T-ASSEMBLE"}
source_na = {"M0498-S-ZEROS", "M0498-S-ENDPOINT", "M0498-S-FOUNDATION", "M0498-X-PROVENANCE", "M0498-X-PI-TRANSFER"}
machine_mode = {"M0498-X-SOURCE": "not_applicable", "M0498-X-PROVENANCE": "informational", "M0498-X-PI-TRANSFER": "excluded"}
obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    if oid == "M0498-ROOT":
        fp = "lean-expression-sha256:4de2508b7d4cc86d13c5d51e1b5d6b8c61e43dec6655035224c21e25745af526"
    else:
        fp = "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_mode.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit", "excluded": "ordinary_pi_formula_is_a_distinct_transport_not_part_of_the_frozen_root"}.get(machine)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": oid != "M0498-X-PI-TRANSFER", "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "excluded" if oid == "M0498-X-PI-TRANSFER" else "required",
        "risk_class": risk, "exclusion_reason": exclusion,
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0498/ObligationTree.lean#root_of_analytic_package" if oid == "M0498-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0498-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2" if oid in source_na else "H3",
        "machine_debt": "M0-L" if oid in checked else ("M4" if machine == "required" else "not_applicable"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M0498-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if oid in {"M0498-A-PERRON", "M0498-C-CONTOUR", "M0498-B-RESIDUES", "M0498-L-ZERO-SUM"} else 40,
        "semantic_step_ledger": {"premises": "Only declared proof_requires children and the frozen formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parents or non-proof support edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0498/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0498-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0498/ObligationTree.lean"] if oid == "M0498-T-ASSEMBLE" else [],
        "owner": "THM-M-0498 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact weighted-psi statement and bounded anchor audit; classical Perron/contour/residue architecture; eligibility fixed independently of closure observations.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0498-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": [o["obligation_id"] for o in obligations if o["readable_eligibility"] == "required"],
        "informational_overlays": ["M0498-X-PROVENANCE"], "excluded": ["M0498-X-PI-TRANSFER"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M4"},
    "status_boundary": "Scope and denominators only; no analytic explicit-formula package, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0498-ROOT": ["M0498-T-ASSEMBLE"],
    "M0498-T-ASSEMBLE": ["M0498-T-ANALYTIC"],
    "M0498-T-ANALYTIC": ["M0498-A-PERRON", "M0498-C-CONTOUR", "M0498-B-RESIDUES", "M0498-L-TRIVIAL", "M0498-L-ZERO-SUM"],
    "M0498-A-PERRON": ["M0498-A-DIRICHLET"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-ZEROS", "M0498-ROOT", "logical_decomposition", "M0498-S-ZEROS"), edge("REF-ROOT-ENDPOINT", "M0498-ROOT", "logical_decomposition", "M0498-S-ENDPOINT"), edge("REF-ROOT-FOUND", "M0498-ROOT", "logical_decomposition", "M0498-S-FOUNDATION"), edge("REF-PI-EXCLUDED", "M0498-X-PI-TRANSFER", "excluded_variant_of", "M0498-ROOT")],
    "provenance": [edge("SRC-ANALYTIC", "M0498-T-ANALYTIC", "source_map", "M0498-X-SOURCE"), edge("SRC-RESIDUES", "M0498-B-RESIDUES", "source_map", "M0498-X-SOURCE"), edge("PROV-ROOT", "M0498-X-PROVENANCE", "provenance_of", "M0498-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0498-ROOT", "trusts", "M0498-S-FOUNDATION"), edge("TRUST-PROV", "M0498-ROOT", "trusts", "M0498-X-PROVENANCE")],
    "documentation": [edge("DOC-ZEROS", "M0498-S-ZEROS", "documents", "M0498-ROOT"), edge("DOC-ENDPOINT", "M0498-S-ENDPOINT", "documents", "M0498-ROOT"), edge("DOC-SOURCE", "M0498-X-SOURCE", "documents", "M0498-T-ANALYTIC")],
    "workflow": [edge("FLOW-ASSEMBLE-ANALYTIC", "M0498-T-ASSEMBLE", "workflow_depends_on", "M0498-T-ANALYTIC"), edge("FLOW-ANALYTIC-PERRON", "M0498-T-ANALYTIC", "workflow_depends_on", "M0498-A-PERRON"), edge("FLOW-ANALYTIC-CONTOUR", "M0498-T-ANALYTIC", "workflow_depends_on", "M0498-C-CONTOUR"), edge("FLOW-ANALYTIC-RESIDUES", "M0498-T-ANALYTIC", "workflow_depends_on", "M0498-B-RESIDUES"), edge("FLOW-PROV-ASSEMBLE", "M0498-X-PROVENANCE", "workflow_depends_on", "M0498-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0498-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0498-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0498-T-ANALYTIC"], "composition_certificates": ["Stage1Instances.THM_M_0498.root_of_analytic_package"], "reason": "The final composition is conditional; the analytic explicit-formula package has no proof body."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0498/check_obligation_tree.py"], "env": {}, "timeout_seconds": 30, "network": "denied", "covered_ids": [oid], "expected_exit": 0})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
