#!/usr/bin/env python3
"""Build the frozen THM-M-0161 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0161-OBLIGATION_TREE"
THEOREM = "THM-M-0161"
PREFIX = "M0161"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


# ID, kind, risk, statement, planned/exact formal target, output, source eligibility.
ROWS = [
    ("M0161-ROOT", "root", "critical", "The exact open-interval fundamental theorem of space curves.", "Stage1Instances.THM_M_0161.FundamentalTheoremOfSpaceCurvesTarget", "The canonical proposition.", True),
    ("M0161-S-DEFINITIONS", "definition", "high", "Freeze E3, Euclidean dot and length, within derivatives, curvature, signed torsion, unit speed, realization, and proper rigid motion.", "Stage1Instances.THM_M_0161.{E3,dot,length,dWithin,d2Within,d3Within,curvature,torsion,IsUnitSpeed,RealizesInvariants,RelatedByProperRigidMotion}", "The exact elaborated statement interface.", False),
    ("M0161-S-BOUNDARY", "terminal", "high", "Preserve a < b, pointwise positive curvature, allowed zero torsion, open-interval derivatives, fixed parameter orientation, and determinant-one congruence.", "Statement.lean mutation suite and planned boundary lemmas", "Checked proposition boundaries and later endpoint side conditions.", False),
    ("M0161-S-FOUNDATION", "certificate", "critical", "Fix classical choice, noncomputable analysis, quotient/extensionality, axiom, TCB, and no-oracle policy.", "planned transitive axiom and TCB report", "Accepted foundation boundary.", False),
    ("M0161-N-BASEPOINT", "normalization", "high", "Choose a base point s0 in (a,b), an initial position, and a positively oriented orthonormal frame without shrinking the interval.", "planned Lean basepoint and initial-frame normalization", "Initial data for the Frenet system.", True),
    ("M0161-C-FRENET-LOCAL", "construction", "critical", "Encode the Frenet-Serret frame equations as a time-dependent ODE and discharge local Picard-Lindelof hypotheses from differentiability of kappa and tau.", "planned Lean Frenet ODE local-existence theorem", "A local frame solution through the initial data.", True),
    ("M0161-L-FRAME-INVARIANTS", "core_lemma", "critical", "Prove along every frame solution that pairwise dot products and determinant remain those of the initial proper orthonormal frame.", "planned Lean Gram-matrix and determinant preservation theorem", "A proper orthonormal moving frame.", True),
    ("M0161-C-FRENET-GLOBAL", "construction", "critical", "Continue the bounded orthonormal frame solution over the entire arbitrary open interval, with compatible local solutions.", "planned Lean open-interval continuation theorem for the Frenet ODE", "A global frame T,N,B on (a,b).", True),
    ("M0161-C-CURVE", "construction", "critical", "Integrate the tangent component of the global frame from the base point and prove its within derivative equals T.", "planned Lean curve integral construction", "A candidate curve with derivative T.", True),
    ("M0161-L-REGULARITY", "lemma", "high", "Bootstrap coefficient and frame regularity to the C3 regularity required by RealizesInvariants.", "planned Lean regularity bridge to ContDiffOn Real 3", "C3 regularity of the constructed curve.", True),
    ("M0161-L-CURVATURE", "lemma", "critical", "From T' = kappa N, unit N, and kappa > 0 derive unit speed and curvature exactly kappa under the frozen within-derivative definitions.", "planned Lean unit-speed and curvature identity theorem", "Unit speed and prescribed curvature.", True),
    ("M0161-L-TORSION", "lemma", "critical", "Using the proper frame orientation and Frenet equations derive the frozen signed triple-product torsion formula exactly tau.", "planned Lean signed-torsion identity theorem", "Prescribed signed torsion.", True),
    ("M0161-T-EXISTENCE", "terminal", "critical", "Assemble global frame, curve, regularity, and invariant identities into the exact ExistencePackage.", "Stage1Instances.THM_M_0161.ExistencePackage", "The existence half of the root.", True),
    ("M0161-N-ALIGN", "normalization", "critical", "For two realizing curves at one base point, construct the unique determinant-one orthogonal linear equivalence aligning their Frenet frames and record the translation aligning positions.", "planned Lean proper-frame alignment theorem", "One proper rigid motion matching initial data.", True),
    ("M0161-L-ODE-UNIQUENESS", "core_lemma", "critical", "Show the aligned Frenet frames solve the same Lipschitz ODE and use open-interval ODE uniqueness to identify them everywhere.", "planned Lean frame uniqueness theorem using ODE_solution_unique_of_mem_Ioo", "Equality of aligned moving frames on (a,b).", True),
    ("M0161-L-CURVE-UNIQUENESS", "lemma", "critical", "From equality of aligned tangents and equality at the base point prove equality of the translated curves throughout the interval.", "planned Lean zero-derivative/connected-interval uniqueness theorem", "The rigid-motion equation for both curves.", True),
    ("M0161-T-UNIQUENESS", "terminal", "critical", "Package frame alignment and curve equality into the exact UniquenessPackage, including dot preservation and determinant one.", "Stage1Instances.THM_M_0161.UniquenessPackage", "The uniqueness half of the root.", True),
    ("M0161-T-ASSEMBLE", "transport", "high", "Conjoin exact existence and uniqueness packages without adding premises.", "Stage1Instances.THM_M_0161.root_of_existence_and_uniqueness", "The exact canonical root conditional on both packages.", True),
    ("M0161-X-ODE", "bridge", "critical", "Audit and instantiate pinned mathlib ODE existence and uniqueness declarations; expose all Lipschitz, interval, and continuation gaps.", "IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt; ODE_solution_unique_of_mem_Ioo", "Checked external bridge interfaces, not root closure.", False),
    ("M0161-X-SOURCE", "terminal", "high", "Map every material construction and uniqueness step to reviewed primary-source theorem passages, assumptions, conventions, and errata.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit.", True),
    ("M0161-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, wrappers, imports, transitive declarations, axioms, TCB, and replay evidence without duplicate body credit.", "planned machine-derived provenance and trust closure", "Release provenance coverage without mathematical proof credit.", False),
]

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
checked = {"M0161-S-DEFINITIONS", "M0161-S-BOUNDARY", "M0161-T-ASSEMBLE", "M0161-X-ODE"}
source_na = {"M0161-S-DEFINITIONS", "M0161-S-BOUNDARY", "M0161-S-FOUNDATION", "M0161-X-ODE", "M0161-X-PROVENANCE"}
machine_special = {"M0161-X-SOURCE": "not_applicable", "M0161-X-PROVENANCE": "informational"}

obligations = []
nodes = []
for oid, kind, risk, claim, target, output, _source_material in ROWS:
    fp = ("lean-expression-sha256:c140d1d15da39c41b3cc430e5119c4ec5194856f15481e2040cc0ea710c47f82"
          if oid in {"M0161-ROOT", "M0161-S-DEFINITIONS"}
          else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
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
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0161/ObligationTree.lean#root_of_existence_and_uniqueness" if oid == "M0161-T-ASSEMBLE" else None),
    })
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX + "-"),
        "obligation_id": oid, "kind": kind, "human_statement": claim,
        "formal_target": target, "output": output,
        "human_debt": "H3", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0161-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M0161-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 60,
        "semantic_step_ledger": {
            "premises": "Only exact incoming proof_requires children and the stated formal context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output.",
        },
        "public_readable_target": f"Stage1_Instances/THM-M-0161/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.",
        "task_ids": [ITEM, "S56-M-0161-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0161/ObligationTree.lean"] if oid == "M0161-T-ASSEMBLE" else [],
        "owner": "THM-M-0161 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None,
                     "review_due": "before proof acceptance",
                     "invalidation_inputs": ["statement", "registry", "source map", "toolchain"],
                     "revocation_state": "provisional" if oid in checked else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact open-interval statement and bounded anchor audit; Frenet-ODE existence and frame-alignment uniqueness architecture selected before proof-status inspection.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0161-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0161-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no existence package, uniqueness package, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, edge_type, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": edge_type, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0161-ROOT": ["M0161-T-ASSEMBLE"],
    "M0161-T-ASSEMBLE": ["M0161-T-EXISTENCE", "M0161-T-UNIQUENESS"],
    "M0161-T-EXISTENCE": ["M0161-N-BASEPOINT", "M0161-C-FRENET-GLOBAL", "M0161-C-CURVE", "M0161-L-REGULARITY", "M0161-L-CURVATURE", "M0161-L-TORSION"],
    "M0161-C-FRENET-GLOBAL": ["M0161-C-FRENET-LOCAL", "M0161-L-FRAME-INVARIANTS"],
    "M0161-C-FRENET-LOCAL": ["M0161-X-ODE"],
    "M0161-T-UNIQUENESS": ["M0161-N-ALIGN", "M0161-L-ODE-UNIQUENESS", "M0161-L-CURVE-UNIQUENESS"],
    "M0161-L-ODE-UNIQUENESS": ["M0161-X-ODE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0161-ROOT", "logical_decomposition", "M0161-S-DEFINITIONS"), edge("REF-ROOT-BOUND", "M0161-ROOT", "logical_decomposition", "M0161-S-BOUNDARY")],
    "provenance": [edge("SRC-ROOT", "M0161-ROOT", "source_map", "M0161-X-SOURCE"), edge("SRC-ODE", "M0161-X-ODE", "source_map", "M0161-X-SOURCE"), edge("PROV-ROOT", "M0161-X-PROVENANCE", "provenance_of", "M0161-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0161-ROOT", "trusts", "M0161-S-FOUNDATION"), edge("TRUST-PROV", "M0161-ROOT", "trusts", "M0161-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M0161-S-DEFINITIONS", "documents", "M0161-ROOT"), edge("DOC-SOURCE", "M0161-X-SOURCE", "documents", "M0161-T-EXISTENCE")],
    "workflow": [edge("FLOW-ASSEMBLE-EX", "M0161-T-ASSEMBLE", "workflow_depends_on", "M0161-T-EXISTENCE"), edge("FLOW-ASSEMBLE-UNIQ", "M0161-T-ASSEMBLE", "workflow_depends_on", "M0161-T-UNIQUENESS"), edge("FLOW-PROV-ASSEMBLE", "M0161-X-PROVENANCE", "workflow_depends_on", "M0161-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for relation in edges:
        outgoing.setdefault(relation["from"], []).append(relation["edge_id"])
        incoming.setdefault(relation["to"], []).append(relation["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0161-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0161-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False,
                         "audit_complete": False, "theorem_complete": False,
                         "remaining_root_cut_set": ["M0161-T-EXISTENCE", "M0161-T-UNIQUENESS"],
                         "composition_certificates": ["Stage1Instances.THM_M_0161.root_of_existence_and_uniqueness"],
                         "reason": "Final composition is conditional; neither exact package has a proof body."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in ROWS:
    recipes["recipes"].append({
        "recipe_id": "VAL-" + oid, "obligation_id": oid,
        "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0161/check_obligation_tree.py"],
        "env": {}, "timeout_seconds": 60, "network_policy": "denied",
        "covered_ids": [oid], "expected_exit": 0,
    })

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
