#!/usr/bin/env python3
"""Build the frozen THM-M-0325 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0325-OBLIGATION_TREE"
THEOREM = "THM-M-0325"
PREFIX = "M0325"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact finite real Grothendieck inequality target.", "Stage1Instances.THM_M_0325.GrothendieckInequalityTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Preserve the scalar and Hilbert matrix forms, unit-polydisc premise, arbitrary real Hilbert spaces, and one universal nonnegative constant.", "Stage1Instances.THM_M_0325.{ScalarMatrixForm,HilbertMatrixForm,ScalarUnitBoundedBy,HilbertUnitBoundedBy}", "The elaborated statement interface."),
    ("S-BOUNDARY", "terminal", "high", "Account for empty index types, zero scalar bound, zero vectors, and zero coefficients without adding nonemptiness hypotheses.", "Stage1Instances.THM_M_0325.empty_scalar_boundary", "Checked statement-boundary behavior."),
    ("S-FOUNDATION", "certificate", "critical", "Fix the classical-choice, real-analysis, TCB, computation, and no-oracle policy for every eventual proof body.", "planned exact foundation and transitive axiom report", "Accepted trust boundary."),
    ("N-FINITE-SPAN", "reduction", "critical", "Reduce each finite family of Hilbert vectors to its finite-dimensional real span while preserving inner products and norm bounds.", "planned finite-span isometric reduction", "A finite-dimensional Gram-data instance."),
    ("N-GRAM", "construction", "critical", "Encode the two vector families by compatible real Gram/correlation data and preserve the weighted bilinear objective.", "planned Gram representation theorem", "Finite correlation data with unit diagonal bounds."),
    ("K-TRANSFORM", "core_lemma", "critical", "Construct and control the real Grothendieck/Krivine transform, including the universal constant and its normalization domain.", "planned real Grothendieck transform theorem", "A universal nonnegative constant and admissible transformed correlations."),
    ("R-RANDOM", "construction", "critical", "Realize transformed correlations by a probability space of scalar sign or unit-polydisc variables with the required pairwise expectation identity.", "planned Gaussian-hyperplane rounding construction", "Bounded random scalar families with prescribed correlations."),
    ("B-MEASURABLE", "terminal", "high", "Prove measurability, integrability, and finite-sum/expectation interchange for the rounding variables.", "planned probability integration certificate", "A legitimate expectation of the finite rounded form."),
    ("B-SCALAR", "lemma", "critical", "Apply the scalar unit-polydisc hypothesis pointwise to every rounded scalar realization.", "planned pointwise ScalarUnitBoundedBy application", "A pointwise absolute bound by C."),
    ("L-EXPECTATION", "lemma", "critical", "Combine the correlation identity, finite-sum interchange, and absolute expectation bound to obtain the Hilbert estimate by the universal constant.", "planned rounded expectation estimate", "The bound for arbitrary finite Hilbert unit families."),
    ("T-PACKAGE", "terminal", "critical", "Quantify uniformly over index types, matrices, scalar bounds, Hilbert spaces, and vector families and assemble the exact proof package.", "Stage1Instances.THM_M_0325.GrothendieckProofPackage", "The exact open analytic package."),
    ("T-ASSEMBLE", "transport", "high", "Compose the proof package with the canonical target without weakening or changing binder order.", "Stage1Instances.THM_M_0325.target_of_proofPackage", "The exact canonical root, conditional on the package."),
    ("X-SOURCE", "source_boundary", "high", "Crosswalk every transform, rounding, and expectation step to a reviewed primary-source theorem passage and normalization.", "pending node-level primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, transitive declarations, axioms, TCB, and replay receipts.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    fp = ("lean-expression-sha256:b4daa662b6b3f7cc1578975aeaf9fd097ef586b209bd0d26d4262c59ac59cf82"
          if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    exclusion = None
    if machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    elif machine == "informational":
        exclusion = "release_provenance_overlay_no_proof_credit"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0325/ObligationTree.lean#target_of_proofPackage" if suffix == "T-ASSEMBLE" else None),
    })
    nodes.append({
        "node_id": f"THM-M-0325-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if suffix == "ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical experiment or oracle may close this node",
        "step_budget": 100 if suffix in {"K-TRANSFORM", "R-RANDOM", "L-EXPECTATION"} else 40,
        "semantic_step_ledger": {"premises": "Only listed proof-requires children and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only a declared typed edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0325/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0325-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0325/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-0325 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; finite-span/transform/random-rounding architecture; eligibility assigned without proof-availability credit.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": oids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no Grothendieck proof, H0 source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-PACKAGE"],
    f"{PREFIX}-T-PACKAGE": [f"{PREFIX}-N-FINITE-SPAN", f"{PREFIX}-N-GRAM", f"{PREFIX}-K-TRANSFORM", f"{PREFIX}-R-RANDOM", f"{PREFIX}-L-EXPECTATION"],
    f"{PREFIX}-R-RANDOM": [f"{PREFIX}-B-MEASURABLE"],
    f"{PREFIX}-L-EXPECTATION": [f"{PREFIX}-B-SCALAR", f"{PREFIX}-B-MEASURABLE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-TRANSFORM", f"{PREFIX}-K-TRANSFORM", "source_map", f"{PREFIX}-X-SOURCE"), edge("SRC-ROUND", f"{PREFIX}-R-RANDOM", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-K-TRANSFORM")],
    "workflow": [edge("FLOW-PACKAGE-SPAN", f"{PREFIX}-T-PACKAGE", "workflow_depends_on", f"{PREFIX}-N-FINITE-SPAN"), edge("FLOW-PACKAGE-TRANSFORM", f"{PREFIX}-T-PACKAGE", "workflow_depends_on", f"{PREFIX}-K-TRANSFORM"), edge("FLOW-PACKAGE-ROUND", f"{PREFIX}-T-PACKAGE", "workflow_depends_on", f"{PREFIX}-R-RANDOM"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "registry_id": "THM-M-0325-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-PACKAGE"], "composition_certificates": ["Stage1Instances.THM_M_0325.target_of_proofPackage"], "reason": "The final composition is conditional; the finite-span, transform, random-rounding, and expectation route has no terminal proof bodies."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid in oids:
    recipes["recipes"].append({"recipe_id": f"VAL-{oid}", "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0325/check_obligation_tree.py"], "env": {}, "timeout_seconds": 60, "network_policy": "denied", "covered_ids": [oid], "expected_exit": 0})

for filename, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / filename).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
