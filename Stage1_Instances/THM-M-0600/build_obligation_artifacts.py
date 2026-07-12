#!/usr/bin/env python3
"""Build the frozen THM-M-0600 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0600-OBLIGATION_TREE"
THEOREM = "THM-M-0600"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


rows = [
    ("M0600-ROOT", "root", "critical", "The exact finite-dimensional real-manifold Morse lemma target.", "Stage1Instances.THM_M_0600.MorseLemmaTarget", "The canonical proposition."),
    ("M0600-S-DEFINITIONS", "definition", "high", "Freeze centered smooth local coordinates, coordinate representative, coordinate Hessian, and the sign convention for the diagonal form.", "Stage1Instances.THM_M_0600.{SmoothLocalCoordinates,inCoordinates,coordinateHessian,morseQuadratic}", "The exact elaborated statement interface."),
    ("M0600-S-DIMZERO", "branch", "normal", "Handle dimension zero and prove that the empty quadratic sums and unique index satisfy the local identity.", "planned exact n = 0 branch", "The zero-dimensional normal form."),
    ("M0600-S-FOUNDATION", "certificate", "critical", "Fix logic, choice, extensionality, axiom, TCB, and no-oracle policy for all terminal bodies.", "planned transitive axiom and trust report", "Accepted foundation boundary."),
    ("M0600-N-CHART", "reduction", "critical", "Reduce the manifold statement through the given centered base coordinates to a smooth function on an open neighborhood of zero in Euclidean space.", "planned checked chart reduction preserving derivative and Hessian hypotheses", "A Euclidean local Morse problem at zero."),
    ("M0600-N-DERIVATIVES", "normalization", "high", "Reconcile ContDiffOn, first derivative zero, and the iterated-fderiv Hessian with the derivative conventions needed by the analytic construction.", "planned derivative-convention transports", "A compatible smooth critical nondegenerate Euclidean germ."),
    ("M0600-C-TAYLOR", "construction", "critical", "Factor the function difference by a smooth family of quadratic coefficients near zero, with its value at zero controlled by the Hessian.", "planned smooth second-order Hadamard/Taylor factorization", "A smooth symmetric quadratic-coefficient family representing g(x)-g(0)."),
    ("M0600-L-SYLVESTER", "bridge", "critical", "Diagonalize the nondegenerate Hessian over the reals and identify positive and negative dimensions.", "QuadraticForm.equivalent_one_neg_one_weighted_sum_squared plus checked convention bridges", "A linear basis with diagonal signs and an index not exceeding n."),
    ("M0600-B-INDEX", "branch", "high", "Split and account for negative and positive directions, including minimum and maximum endpoints, without reversing the frozen sign convention.", "planned signature/index accounting", "A complete ordered coordinate partition at the critical point."),
    ("M0600-L-SPLITTING", "core_lemma", "critical", "Prove the parameterized splitting lemma that removes mixed and higher-order terms while retaining smooth dependence and a local inverse.", "planned finite-dimensional smooth splitting lemma", "A local smooth change of variables giving a nondegenerate quadratic block."),
    ("M0600-C-INDUCTION", "construction", "critical", "Iterate the splitting lemma over all nondegenerate directions and prove termination, compatibility, and preservation of the remaining hypotheses.", "planned finite-dimensional induction with construction invariants", "A full local diagonalizing map."),
    ("M0600-L-INVERSE", "bridge", "critical", "Use the smooth inverse function theorem to restrict the constructed map to mutually inverse open neighborhoods containing zero.", "ContDiffAt.to_localInverse plus exact derivative-invertibility bridge", "A centered smooth Euclidean local equivalence."),
    ("M0600-C-NORMALCOORDS", "construction", "critical", "Compose the Euclidean local equivalence with the base chart and prove every SmoothLocalCoordinates field.", "planned Stage1Instances.THM_M_0600.SmoothLocalCoordinates constructor", "Centered smooth local coordinates on M."),
    ("M0600-T-IDENTITY", "terminal", "critical", "Transport the Euclidean quadratic identity through the constructed coordinates for every point of the restricted target.", "planned local normal-form identity", "The exact pointwise equality on normal.target."),
    ("M0600-T-ENGINE", "terminal", "critical", "Assemble chart reduction, analytic construction, index accounting, coordinates, and identity into the expanded engine interface.", "Stage1Instances.THM_M_0600.MorseNormalFormEngine", "The full premise consumed by the root composition."),
    ("M0600-T-ASSEMBLE", "transport", "high", "Consume the expanded engine interface and yield the exact frozen MorseLemmaTarget.", "Stage1Instances.THM_M_0600.root_of_morseNormalFormEngine", "The exact canonical root conditional on the engine."),
    ("M0600-X-SOURCE", "terminal", "high", "Map every material analytic and geometric node to a reviewed primary-source passage and convention.", "node-specific primary-source crosswalk pending", "Human-source coverage without machine proof credit."),
    ("M0600-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, axioms, TCB, placeholders, immutable pins, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

checked = {"M0600-S-DEFINITIONS", "M0600-T-ASSEMBLE"}
source_na = {"M0600-S-DEFINITIONS", "M0600-S-FOUNDATION", "M0600-T-ASSEMBLE", "M0600-X-PROVENANCE"}
machine_special = {"M0600-X-SOURCE": "not_applicable", "M0600-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
expression_hash = json.loads((HERE / "statement.json").read_text())["canonical_formal_target"]["elaborated_expression_sha256"]

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fingerprint = ("lean-expression-sha256:" + expression_hash if oid == "M0600-ROOT"
                   else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    body = ("local:Stage1_Instances/THM-M-0600/ObligationTree.lean#root_of_morseNormalFormEngine"
            if oid == "M0600-T-ASSEMBLE" else None)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": exclusion, "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": "THM-M-0600-" + oid.removeprefix("M0600-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0600-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if body else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical experiment or oracle may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {
            "premises": "Only exact incoming proof_requires conclusions and the stated formal context.",
            "inference": claim, "output": output,
            "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."
        },
        "public_readable_target": "Stage1_Instances/THM-M-0600/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise and no Morse engine proof is supplied.",
        "task_ids": [ITEM, "S56-M-0600-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0600/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0600 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None,
                     "review_due": "before proof acceptance",
                     "invalidation_inputs": ["statement", "registry", "source map", "toolchain"],
                     "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and bounded anchor audit; classical Taylor/Sylvester/splitting architecture expanded before observing closure.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0600-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0600-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no Morse normal-form engine, H0/R0, audit completion, or theorem completion.",
}


def edge(eid, source, edge_type, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": edge_type, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0600-ROOT": ["M0600-T-ASSEMBLE"],
    "M0600-T-ASSEMBLE": ["M0600-T-ENGINE"],
    "M0600-T-ENGINE": ["M0600-S-DIMZERO", "M0600-N-CHART", "M0600-N-DERIVATIVES", "M0600-T-IDENTITY", "M0600-C-NORMALCOORDS", "M0600-B-INDEX"],
    "M0600-T-IDENTITY": ["M0600-C-INDUCTION"],
    "M0600-C-INDUCTION": ["M0600-C-TAYLOR", "M0600-L-SPLITTING", "M0600-L-SYLVESTER"],
    "M0600-C-NORMALCOORDS": ["M0600-L-INVERSE", "M0600-N-CHART"],
    "M0600-B-INDEX": ["M0600-L-SYLVESTER"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0600-ROOT", "logical_decomposition", "M0600-S-DEFINITIONS"), edge("REF-ROOT-FOUND", "M0600-ROOT", "logical_decomposition", "M0600-S-FOUNDATION")],
    "provenance": [edge("SRC-TAYLOR", "M0600-C-TAYLOR", "source_map", "M0600-X-SOURCE"), edge("SRC-SPLIT", "M0600-L-SPLITTING", "source_map", "M0600-X-SOURCE"), edge("SRC-SYLVESTER", "M0600-L-SYLVESTER", "source_map", "M0600-X-SOURCE"), edge("PROV-ROOT", "M0600-X-PROVENANCE", "provenance_of", "M0600-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0600-ROOT", "trusts", "M0600-S-FOUNDATION"), edge("TRUST-PROV", "M0600-ROOT", "trusts", "M0600-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M0600-S-DEFINITIONS", "documents", "M0600-ROOT"), edge("DOC-ENGINE", "M0600-X-SOURCE", "documents", "M0600-T-ENGINE")],
    "workflow": [edge("FLOW-ASSEMBLE-ENGINE", "M0600-T-ASSEMBLE", "workflow_depends_on", "M0600-T-ENGINE"), edge("FLOW-ENGINE-IDENTITY", "M0600-T-ENGINE", "workflow_depends_on", "M0600-T-IDENTITY"), edge("FLOW-IDENTITY-INDUCT", "M0600-T-IDENTITY", "workflow_depends_on", "M0600-C-INDUCTION"), edge("FLOW-PROV-ASSEMBLE", "M0600-X-PROVENANCE", "workflow_depends_on", "M0600-T-ASSEMBLE")],
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
    "registry_id": "THM-M-0600-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0600-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False,
                         "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False,
                         "remaining_root_cut_set": ["M0600-T-ENGINE"],
                         "composition_certificates": ["Stage1Instances.THM_M_0600.root_of_morseNormalFormEngine"],
                         "reason": "The final composition is conditional; MorseNormalFormEngine has no proof body."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-0600/check_obligation_tree.py"],
        "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0600 obligation tree"}],
        "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
