#!/usr/bin/env python3
"""Generate the frozen THM-M-1285 registry and typed graph projections."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

NODES = [
    ("M1285-ROOT", "root", "The exact frozen Schwarz rearrangement target.", "Stage1Instances.THM_M_1285.SchwarzRearrangementTarget", "M3", "critical", True, True),
    ("M1285-S-INTERFACE", "definition", "Freeze the Euclidean, strict-superlevel, radiality, and equimeasurability interfaces.", "Stage1Instances.THM_M_1285.{Euclidean,IsRadial,IsRadiallyNonincreasing,Equimeasurable}", "M0-L", "high", True, False),
    ("M1285-S-FOUNDATION", "certificate", "Fix classical choice, measure-theory, TCB, and no-oracle policy for terminal bodies.", "planned exact axiom and transitive trust report", "M4", "critical", True, False),
    ("M1285-D-DISTRIBUTION", "construction", "Define the strict-superlevel distribution function and prove its finiteness at every positive threshold.", "planned Lean distribution-function definition and finiteness theorem", "M4", "critical", True, True),
    ("M1285-L-DISTRIBUTION", "lemma", "Prove the distribution function has the monotonicity and limit properties required by generalized inversion.", "planned Lean antitonicity and continuity package", "M4", "critical", True, True),
    ("M1285-C-INVERSE", "construction", "Construct a generalized inverse of the distribution profile with exact strict-level conventions.", "planned Lean generalized-inverse construction", "M4", "critical", True, True),
    ("M1285-C-RADIUS", "construction", "Convert finite distribution values to centered-ball radii with the required volume.", "planned Lean radius/ball-volume selection theorem", "M4", "critical", True, True),
    ("M1285-C-WITNESS", "construction", "Define fstar from radius or inverse-distribution data on Euclidean space.", "planned Lean Schwarz witness definition", "M4", "critical", True, True),
    ("M1285-L-MEASURABLE", "lemma", "Prove the constructed witness is measurable.", "planned Lean witness measurability theorem", "M4", "critical", True, True),
    ("M1285-L-RADIAL", "lemma", "Prove the constructed witness is constant on equal-norm spheres.", "planned Lean witness radiality theorem", "M4", "high", True, True),
    ("M1285-L-ANTITONE", "lemma", "Prove the witness is nonincreasing as radius increases.", "planned Lean radial antitonicity theorem", "M4", "critical", True, True),
    ("M1285-L-EQUIMEASURABLE", "lemma", "Identify every positive strict superlevel of the witness with a centered ball of the original distribution volume.", "planned Lean exact strict-superlevel volume theorem", "M4", "critical", True, True),
    ("M1285-T-PACKAGE", "transport", "Assemble the witness and its four properties into SchwarzConstructionPackage.", "Stage1Instances.THM_M_1285.SchwarzConstructionPackage", "M4", "critical", True, True),
    ("M1285-T-ASSEMBLE", "transport", "Compose SchwarzConstructionPackage into the exact canonical root.", "Stage1Instances.THM_M_1285.schwarzRearrangementTarget_of_construction", "M0-L", "high", True, True),
    ("M1285-X-SOURCE", "terminal", "Map each substantive construction and lemma to primary theorem/page/assumption/errata evidence.", "planned node-level human-source crosswalk", "M4", "high", False, True),
    ("M1285-X-PROVENANCE", "certificate", "Record terminal bodies, imports, axioms, TCB, licenses, and replay receipts.", "planned proof-provenance inventory", "M4", "critical", False, False),
]

PROOF = [
    ("M1285-ROOT", "M1285-T-ASSEMBLE"),
    ("M1285-T-ASSEMBLE", "M1285-T-PACKAGE"),
    ("M1285-T-PACKAGE", "M1285-C-WITNESS"),
    ("M1285-T-PACKAGE", "M1285-L-MEASURABLE"),
    ("M1285-T-PACKAGE", "M1285-L-RADIAL"),
    ("M1285-T-PACKAGE", "M1285-L-ANTITONE"),
    ("M1285-T-PACKAGE", "M1285-L-EQUIMEASURABLE"),
    ("M1285-C-WITNESS", "M1285-C-INVERSE"),
    ("M1285-C-WITNESS", "M1285-C-RADIUS"),
    ("M1285-C-INVERSE", "M1285-D-DISTRIBUTION"),
    ("M1285-C-INVERSE", "M1285-L-DISTRIBUTION"),
    ("M1285-C-RADIUS", "M1285-D-DISTRIBUTION"),
    ("M1285-L-MEASURABLE", "M1285-C-WITNESS"),
    ("M1285-L-RADIAL", "M1285-C-WITNESS"),
    ("M1285-L-ANTITONE", "M1285-C-WITNESS"),
    ("M1285-L-ANTITONE", "M1285-L-DISTRIBUTION"),
    ("M1285-L-EQUIMEASURABLE", "M1285-C-INVERSE"),
    ("M1285-L-EQUIMEASURABLE", "M1285-C-RADIUS"),
]

def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()

rows = []
for oid, kind, human, formal, debt, risk, machine, human_source in NODES:
    fp = ("lean-expression-sha256:ffce741885f8c5eeb87a6dd893e7c5bf6ccc7a7f88fcc37e9fdd8750ab2d41ac"
          if oid == "M1285-ROOT" else "planned:v1:sha256:" + hashlib.sha256((oid + "|" + human + "|" + formal).encode()).hexdigest())
    rows.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": "required" if machine else "informational",
        "human_source_eligibility": "required" if human_source else "not_applicable",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None if machine else ("human_source_boundary_only" if oid.endswith("SOURCE") else "release_provenance_overlay_no_proof_credit"),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1285/ObligationTree.lean#schwarzRearrangementTarget_of_construction" if oid == "M1285-T-ASSEMBLE" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: r[k] for k in fields} for r in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [r["obligation_id"] for r in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-1285-OBLIGATION_TREE", "theorem_id": "THM-M-1285",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and bounded anchor audit; distribution/generalized-inverse/centered-ball construction selected before proof execution.",
    "frozen_against_statement_sha256": sha("Statement.lean"), "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
    "root_obligation_id": "M1285-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M1285-X-SOURCE", "M1285-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": rows, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1285-S-INTERFACE", "M1285-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; the construction premise is open and no theorem completion is claimed.",
}

node_map = {x[0]: x for x in NODES}
nodes = []
for oid, kind, human, formal, debt, risk, machine, human_source in NODES:
    nodes.append({
        "node_id": "THM-M-1285-" + oid.removeprefix("M1285-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human, "human_debt": "H2", "machine_debt": debt,
        "readability_debt": "R3", "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if human_source else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending", "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only declared proof_requires children and the frozen formal context.", "inference": human, "output": human, "outgoing_use": "Only declared typed parents may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1285/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise or root closure is supplied.",
        "task_ids": ["S56-M-1285-OBLIGATION_TREE", "S56-M-1285-PROOF"], "owned_sources": [], "owner": "THM-M-1285 proof lane",
        "reviewer": "independent Stage1 integration lane", "validity": {"validated_at": "2026-07-12" if debt == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if debt == "M0-L" else "open"},
    })

def graph(edges):
    out = {i: [] for i in ids}; inn = {i: [] for i in ids}
    for e in edges:
        out[e["from"]].append(e["edge_id"]); inn[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": out, "in": inn}

proof_edges = []
for i, (parent, child) in enumerate(PROOF, 1):
    a, b = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": a, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": b}, {"edge_id": b, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": a}]

def simple(prefix, typ, pairs):
    return graph([{"edge_id": f"{prefix}{i:02d}", "type": typ, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)])

substantive = [x for x in ids if x not in ("M1285-S-INTERFACE", "M1285-S-FOUNDATION", "M1285-X-SOURCE", "M1285-X-PROVENANCE")]
graphs = {
    "proof": graph(proof_edges),
    "refinement": simple("R", "logical_decomposition", [("M1285-ROOT", "M1285-S-INTERFACE"), ("M1285-D-DISTRIBUTION", "M1285-L-DISTRIBUTION")]),
    "provenance": simple("V", "provenance_of", [("M1285-X-PROVENANCE", x) for x in substantive]),
    "evidence": simple("E", "provenance_of", [("M1285-X-PROVENANCE", "M1285-T-ASSEMBLE")]),
    "trust": simple("T", "trusts", [(x, "M1285-S-FOUNDATION") for x in substantive]),
    "documentation": simple("D", "documents", [("M1285-X-SOURCE", x) for x in substantive]),
    "workflow": simple("W", "workflow_depends_on", [("M1285-T-PACKAGE", x) for x in ("M1285-D-DISTRIBUTION", "M1285-C-INVERSE", "M1285-C-RADIUS", "M1285-C-WITNESS", "M1285-L-MEASURABLE", "M1285-L-RADIAL", "M1285-L-ANTITONE", "M1285-L-EQUIMEASURABLE")]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-1285-OBLIGATION_TREE", "theorem_id": "THM-M-1285",
    "registry_id": "THM-M-1285-OBLIGATIONS-v1", "registry_denominator_sha256": digest, "root_node_id": "M1285-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"minimal_open_root_cut": ["M1285-T-PACKAGE"], "root_closed": False, "root_machine_debt": "M3", "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n")
print(digest)
