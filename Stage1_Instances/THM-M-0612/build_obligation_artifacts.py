#!/usr/bin/env python3
"""Build the frozen THM-M-0612 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0612-OBLIGATION_TREE"
THEOREM = "THM-M-0612"


def canonical_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M0612-ROOT", "root", "critical", "The exact local-domain Gromov nonsqueezing target frozen in Statement.lean.", "Stage1.THM_M_0612.StatementShape", "The sharp inequality r <= R."),
    ("M0612-S-DEFINITIONS", "definition", "high", "Freeze phase space, Euclidean ball, one-coordinate cylinder, standard form, and local embedding conventions.", "Stage1.THM_M_0612.{PhaseSpace,normSq,ball,cylinder,standardForm,IsSymplecticEmbeddingOnBall}", "The exact canonical interface."),
    ("M0612-S-DIMENSION", "normalization", "high", "Relate a finite inhabited coordinate type Q to real dimension 2*|Q| and identify the selected conjugate pair.", "planned finite-coordinate/dimension equivalence", "A dimension-positive standard symplectic coordinate model."),
    ("M0612-S-BOUNDARY", "branch", "high", "Account for positive radii, strict-open domains, the two-dimensional case, and exclusion of dimension zero.", "planned exact boundary lemmas for StatementShape", "All admitted boundary cases match the canonical quantifiers."),
    ("M0612-S-FOUNDATION", "certificate", "critical", "Fix the classical-choice, quotient, analytic, TCB, and no-oracle policy for every terminal body.", "planned transitive axiom and trust report", "An accepted foundation and trust boundary."),
    ("M0612-N-LOCAL", "transport", "critical", "Transport the total-function local predicates to a genuine smooth symplectic embedding between the open ball and ambient phase space.", "planned checked local-embedding equivalence", "A geometric local embedding with no hypotheses outside the ball."),
    ("M0612-N-SCALE", "normalization", "high", "Normalize translations, coordinate-pair permutations, symplectic scalings, and form sign without changing the radius claim.", "planned symplectic coordinate normalization", "A standard centered ball-to-standard-cylinder instance."),
    ("M0612-B-DIM2", "branch", "critical", "Prove the dimension-two branch using symplectic area preservation and injectivity.", "planned n=1 area obstruction", "The squared-radius obstruction when |Q|=1."),
    ("M0612-B-HIGHER", "branch", "critical", "Prove the dimension-at-least-four branch by the capacity or pseudoholomorphic-curve construction.", "planned n>=2 nonsqueezing obstruction", "The squared-radius obstruction when 2<=|Q|."),
    ("M0612-B-MERGE", "terminal", "high", "Split on |Q|=1 versus |Q|>=2 and recompose the exhaustive positive-dimensional branches.", "planned Nat-cardinality branch recomposition", "RadiusSquaredObstruction for every inhabited finite Q."),
    ("M0612-C-CAPACITY", "construction", "critical", "Construct a symplectic capacity on the required class of open subsets with fixed normalization.", "planned capacity construction on standard finite-dimensional domains", "A well-defined capacity value for balls, cylinders, and embedding images."),
    ("M0612-C-INVARIANCE", "core_lemma", "critical", "Prove capacity invariance under symplectomorphisms and independence of coordinate presentations.", "planned symplectic-invariance theorem", "Equal capacities for equivalent domain presentations."),
    ("M0612-L-MONOTONE", "core_lemma", "critical", "Prove monotonicity of capacity under local symplectic embeddings, not merely set inclusion.", "planned symplectic-embedding monotonicity theorem", "c(ball r) <= c(cylinder R)."),
    ("M0612-L-CONFORMAL", "core_lemma", "high", "Prove the quadratic conformality law for symplectic dilation and positive radii.", "planned capacity conformality theorem", "Radius scaling contributes the factor r^2."),
    ("M0612-L-BALL", "computation", "critical", "Compute the normalized capacity of the open standard ball as pi*r^2.", "planned ball-capacity computation", "c(ball r) = pi*r^2."),
    ("M0612-L-CYLINDER", "computation", "critical", "Compute or sharply bound the capacity of the open standard cylinder by pi*R^2.", "planned cylinder-capacity computation", "c(cylinder i R) <= pi*R^2."),
    ("M0612-C-J", "construction", "critical", "Choose a compatible almost-complex structure adapted to the embedding and standard near the relevant boundary.", "planned compatible almost-complex extension", "A controlled tame almost-complex structure."),
    ("M0612-L-CURVE", "core_lemma", "critical", "Establish existence of a pseudoholomorphic sphere/plane through the required point in the compactified target.", "planned pseudoholomorphic-curve existence theorem", "A curve intersecting the embedded ball with controlled homology class."),
    ("M0612-L-COMPACT", "core_lemma", "critical", "Supply compactness, bubbling control, and limiting-curve survival for the chosen moduli problem.", "planned Gromov compactness package", "A nonconstant limiting curve retaining the incidence constraint."),
    ("M0612-L-ENERGY", "core_lemma", "critical", "Relate symplectic area, analytic energy, and the cylinder class upper bound.", "planned energy-area identity and upper estimate", "Curve area at most pi*R^2."),
    ("M0612-L-MONOTONICITY", "core_lemma", "critical", "Apply the local monotonicity/minimal-area estimate to the portion of the curve crossing the embedded ball.", "planned pseudoholomorphic monotonicity lemma", "Curve area at least pi*r^2."),
    ("M0612-T-SQUARED", "terminal", "critical", "Combine capacity monotonicity or curve area bounds and cancel the positive normalization constant.", "Stage1.THM_M_0612.RadiusSquaredObstruction", "The inequality r^2 <= R^2."),
    ("M0612-T-ORDER", "terminal", "normal", "Use positivity to transport r^2 <= R^2 to r <= R.", "Stage1.THM_M_0612.radius_le_of_sq_le", "The sharp radius inequality."),
    ("M0612-T-ASSEMBLE", "transport", "high", "Consume the squared obstruction and yield the exact canonical StatementShape.", "Stage1.THM_M_0612.root_of_radiusSquaredObstruction", "The exact canonical root conditional on the geometric package."),
    ("M0612-X-SOURCE", "terminal", "high", "Map every material geometric lemma to a reviewed primary-source passage and convention.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M0612-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, axioms, TCB, placeholders, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

checked = {"M0612-S-DEFINITIONS", "M0612-T-ORDER", "M0612-T-ASSEMBLE"}
source_na = {"M0612-S-DEFINITIONS", "M0612-S-DIMENSION", "M0612-S-BOUNDARY", "M0612-S-FOUNDATION", "M0612-T-ORDER", "M0612-X-PROVENANCE"}
machine_special = {"M0612-X-SOURCE": "not_applicable", "M0612-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit-receipt.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    if oid in {"M0612-ROOT", "M0612-S-DEFINITIONS"}:
        fingerprint = "lean-source:v1:sha256:" + statement_hash
    else:
        fingerprint = "planned:v1:sha256:" + canonical_hash([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    body = None
    if oid == "M0612-T-ORDER":
        body = "local:Stage1_Instances/THM-M-0612/ObligationTree.lean#radius_le_of_sq_le"
    elif oid == "M0612-T-ASSEMBLE":
        body = "local:Stage1_Instances/THM-M-0612/ObligationTree.lean#root_of_radiusSquaredObstruction"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion, "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-0612-" + oid.removeprefix("M0612-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0612-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if body else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical experiment or oracle may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires conclusions and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0612/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise and no nonsqueezing closure is supplied.",
        "task_ids": [ITEM, "S56-M-0612-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0612/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0612 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = canonical_hash([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact local-domain statement plus bounded anchor audit; capacity and pseudoholomorphic-curve routes expanded before observing proof closure.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0612-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0612-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no nonlinear nonsqueezing proof, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0612-ROOT": ["M0612-T-ASSEMBLE"],
    "M0612-T-ASSEMBLE": ["M0612-T-SQUARED", "M0612-T-ORDER"],
    "M0612-T-SQUARED": ["M0612-N-LOCAL", "M0612-N-SCALE", "M0612-B-MERGE"],
    "M0612-B-MERGE": ["M0612-B-DIM2", "M0612-B-HIGHER"],
    "M0612-B-DIM2": ["M0612-L-MONOTONE", "M0612-L-BALL", "M0612-L-CYLINDER"],
    "M0612-B-HIGHER": ["M0612-C-CAPACITY", "M0612-C-INVARIANCE", "M0612-L-MONOTONE", "M0612-L-CONFORMAL", "M0612-L-BALL", "M0612-L-CYLINDER"],
    "M0612-C-CAPACITY": ["M0612-C-J", "M0612-L-CURVE", "M0612-L-COMPACT", "M0612-L-ENERGY", "M0612-L-MONOTONICITY"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0612-ROOT", "logical_decomposition", "M0612-S-DEFINITIONS"), edge("REF-ROOT-DIM", "M0612-ROOT", "logical_decomposition", "M0612-S-DIMENSION"), edge("REF-ROOT-BOUND", "M0612-ROOT", "logical_decomposition", "M0612-S-BOUNDARY"), edge("REF-ROOT-FOUND", "M0612-ROOT", "logical_decomposition", "M0612-S-FOUNDATION")],
    "provenance": [edge("SRC-CURVE", "M0612-L-CURVE", "source_map", "M0612-X-SOURCE"), edge("SRC-COMPACT", "M0612-L-COMPACT", "source_map", "M0612-X-SOURCE"), edge("PROV-ROOT", "M0612-X-PROVENANCE", "provenance_of", "M0612-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0612-ROOT", "trusts", "M0612-S-FOUNDATION"), edge("TRUST-PROV", "M0612-ROOT", "trusts", "M0612-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", "M0612-S-DEFINITIONS", "documents", "M0612-ROOT"), edge("DOC-GEOMETRY", "M0612-X-SOURCE", "documents", "M0612-B-HIGHER")],
    "workflow": [edge("FLOW-ASSEMBLE-SQ", "M0612-T-ASSEMBLE", "workflow_depends_on", "M0612-T-SQUARED"), edge("FLOW-SQ-BRANCH", "M0612-T-SQUARED", "workflow_depends_on", "M0612-B-MERGE"), edge("FLOW-PROV-ASSEMBLE", "M0612-X-PROVENANCE", "workflow_depends_on", "M0612-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0612-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0612-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0612-T-SQUARED"], "composition_certificates": ["Stage1.THM_M_0612.root_of_radiusSquaredObstruction"], "reason": "The final composition is conditional; RadiusSquaredObstruction has no proof body."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0612/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0612 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
