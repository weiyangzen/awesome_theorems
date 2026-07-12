#!/usr/bin/env python3
"""Build the deterministic THM-M-1515 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def planned(text):
    return "planned:v1:sha256:" + sha(text.encode())


rows = [
    ("M1515-ROOT", "root", "Exact finite-dimensional Noether target", "critical", "required", "required", "required", "M3"),
    ("M1515-S-DEFINITIONS", "definition", "Freeze derivatives, Euler-Lagrange equation, symmetry, regularity, and charge", "high", "required", "not_applicable", "required", "M0-L"),
    ("M1515-S-FOUNDATION", "certificate", "Audit classical logic, choice, fderiv fallback, imports, and TCB", "critical", "required", "not_applicable", "required", "M4"),
    ("M1515-N-CHARGE", "normalization", "Rewrite the charge as momentum pairing minus boundary along the curve", "normal", "required", "required", "required", "M0-L"),
    ("M1515-C-MOMENTUM", "construction", "Construct the time-dependent momentum covector and its pairing with the generator", "high", "required", "required", "required", "M4"),
    ("M1515-L-MOMENTUM-DERIV", "core_lemma", "Differentiate the momentum-generator pairing and use Euler-Lagrange", "critical", "required", "required", "required", "M4"),
    ("M1515-L-BOUNDARY-DERIV", "core_lemma", "Differentiate the boundary term along the trajectory", "high", "required", "required", "required", "M4"),
    ("M1515-L-SYMMETRY", "lemma", "Identify both derivative values by infinitesimal quasi-invariance", "critical", "required", "required", "required", "M0-L"),
    ("M1515-T-SUBTRACT", "terminal", "Subtract the equal derivatives to obtain derivative zero for the charge", "high", "required", "required", "required", "M0-L"),
    ("M1515-X-CALCULUS", "bridge", "Audit every imported derivative, chain, application, and subtraction rule", "high", "required", "not_applicable", "required", "M4"),
    ("M1515-X-SOURCE", "terminal", "Map every root-relevant analytic step to an accepted human source", "high", "not_applicable", "required", "required", "M4"),
    ("M1515-X-PROVENANCE", "certificate", "Inventory terminal bodies, declarations, axioms, imports, and replay provenance", "critical", "informational", "not_applicable", "required", "M4"),
]

statement_hash = sha((HERE / "Statement.lean").read_bytes())
anchor_hash = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, desc, risk, machine, human, readable, debt in rows:
    fingerprint = (
        "lean-expression-sha256:91f6f9b51af1889d9f92f9647f41b0c3e23574783ee97517fd0498b67d8e537e"
        if oid == "M1515-ROOT" else planned(oid + "|" + desc)
    )
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint,
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": human,
        "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "not_in_this_axis", "informational": "release_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1515/ObligationTree.lean#root_of_derivative_packages" if oid == "M1515-T-SUBTRACT" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode())
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": "S56-M-1515-OBLIGATION_TREE",
    "theorem_id": "THM-M-1515",
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; direct variational-calculus architecture; eligibility assigned before proof execution.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1515-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": [o["obligation_id"] for o in obligations if o["readable_eligibility"] == "required"],
        "informational_overlays": ["M1515-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
    "append_only_delta": [],
    "status_observed_after_freeze": {
        "closed_obligations": ["M1515-S-DEFINITIONS", "M1515-N-CHARGE", "M1515-L-SYMMETRY", "M1515-T-SUBTRACT"],
        "root_machine_debt": "M3",
    },
    "status_boundary": "Architecture and denominator freeze only; both analytic derivative packages and the root remain open.",
}

nodes = []
for oid, kind, desc, risk, machine, human, readable, debt in rows:
    nodes.append({
        "node_id": "THM-M-1515-" + oid.removeprefix("M1515-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": desc + ".",
        "formal_target": {
            "M1515-ROOT": "Stage1Instances.THM_M_1515.NoetherFirstTheoremTarget",
            "M1515-L-MOMENTUM-DERIV": "Stage1Instances.THM_M_1515.MomentumPairingDerivative",
            "M1515-L-BOUNDARY-DERIV": "Stage1Instances.THM_M_1515.BoundaryAlongCurveDerivative",
            "M1515-T-SUBTRACT": "Stage1Instances.THM_M_1515.root_of_derivative_packages",
        }.get(oid, "planned exact signature: " + desc),
        "output": desc + ".",
        "human_debt": "H1",
        "machine_debt": debt,
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk/open-node-map" if human == "required" else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M1515-T-SUBTRACT" else "none",
        "foundation_profile": "lean4-mathlib/noncomputable-classical-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation is eligible",
        "step_budget": 60 if risk == "critical" else 35,
        "semantic_step_ledger": {
            "premises": "Only the exact incoming proof_requires children and the frozen formal context.",
            "inference": desc + ".",
            "output": desc + ".",
            "outgoing_use": "Only the declared typed parent may consume this conclusion for proof closure.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-1515/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "This node supplies only its stated interface; open children and the exact root are not silently closed.",
        "task_ids": ["S56-M-1515-OBLIGATION_TREE", "S56-M-1515-PROOF"],
        "owned_sources": (["Stage1_Instances/THM-M-1515/ObligationTree.lean#root_of_derivative_packages"] if oid == "M1515-T-SUBTRACT" else []),
        "owner": "THM-M-1515 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if debt == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if debt == "M0-L" else "open"},
    })

graphs = {name: {"edges": [], "out": {oid: [] for oid in ids}, "in": {oid: [] for oid in ids}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}


def edge(graph, eid, typ, source, target, reciprocal=None):
    item = {"edge_id": eid, "type": typ, "from": source, "to": target}
    if reciprocal:
        item["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(item)
    graphs[graph]["out"][source].append(eid)
    graphs[graph]["in"][target].append(eid)


proof_pairs = [
    ("M1515-ROOT", "M1515-T-SUBTRACT"),
    ("M1515-T-SUBTRACT", "M1515-N-CHARGE"),
    ("M1515-T-SUBTRACT", "M1515-L-MOMENTUM-DERIV"),
    ("M1515-T-SUBTRACT", "M1515-L-BOUNDARY-DERIV"),
    ("M1515-T-SUBTRACT", "M1515-L-SYMMETRY"),
    ("M1515-L-MOMENTUM-DERIV", "M1515-C-MOMENTUM"),
    ("M1515-L-MOMENTUM-DERIV", "M1515-X-CALCULUS"),
    ("M1515-L-BOUNDARY-DERIV", "M1515-X-CALCULUS"),
]
for i, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    edge("proof", req, "proof_requires", parent, child, comp)
    edge("proof", comp, "composes", child, parent, req)

for i, child in enumerate(("M1515-S-DEFINITIONS", "M1515-S-FOUNDATION"), 1):
    edge("refinement", f"R{i:02d}", "logical_decomposition", "M1515-ROOT", child)
edge("provenance", "PR01", "provenance_of", "M1515-X-PROVENANCE", "M1515-ROOT")
edge("evidence", "EV01", "evidence_for", "M1515-X-PROVENANCE", "M1515-T-SUBTRACT")
edge("trust", "TR01", "trusts", "M1515-ROOT", "M1515-S-FOUNDATION")
for i, oid in enumerate(ids, 1):
    edge("documentation", f"D{i:02d}", "documents", "M1515-X-SOURCE" if oid != "M1515-X-SOURCE" else "M1515-X-PROVENANCE", oid)
for i, child in enumerate(("M1515-S-DEFINITIONS", "M1515-N-CHARGE", "M1515-C-MOMENTUM", "M1515-L-MOMENTUM-DERIV", "M1515-L-BOUNDARY-DERIV", "M1515-L-SYMMETRY", "M1515-T-SUBTRACT", "M1515-X-PROVENANCE"), 1):
    edge("workflow", f"W{i:02d}", "workflow_depends_on", child, "M1515-ROOT")

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": "S56-M-1515-OBLIGATION_TREE",
    "theorem_id": "THM-M-1515",
    "registry_id": "THM-M-1515-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": "M1515-ROOT",
    "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_debt": "M3", "minimal_open_root_cut": ["M1515-L-MOMENTUM-DERIV", "M1515-L-BOUNDARY-DERIV"], "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(denominator)
