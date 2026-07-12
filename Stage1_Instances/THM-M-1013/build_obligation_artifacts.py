#!/usr/bin/env python3
"""Build the frozen THM-M-1013 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "240ce7cf9937f5d92636d86bdc3c05b9224b27b0"
ITEM = "S56-M-1013-OBLIGATION_TREE"
PREFIX = "M1013"

specs = [
    ("ROOT", "root", "Stage1Instances.THM_M_1013.StatementShape", "critical", None, 20),
    ("S", "statement-foundation", "exact finite-dimensional probability-measure target", "high", "local:Statement.lean", 35),
    ("S-BOUNDARY", "boundary", "dimension zero is retained by the universal dimension binder", "high", "local:ObligationTree.lean:zero_dimension_boundary", 20),
    ("T-COMPOSE", "composition", "Stage1Instances.THM_M_1013.ObligationTree.compose_directions", "critical", "local:ObligationTree.lean:compose_directions", 20),
    ("F", "forward-branch", "weak convergence implies every projected weak convergence", "high", None, 30),
    ("F-MAP", "bridge", "continuous mapping theorem for ProbabilityMeasure.map", "high", "mathlib:ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous", 35),
    ("R", "reverse-branch", "all projected weak limits imply vector weak convergence", "critical", None, 45),
    ("R-VECTOR-CHAR", "bridge", "vector weak convergence from pointwise characteristic functions", "critical", "mathlib:ProbabilityMeasure.tendsto_iff_tendsto_charFun", 40),
    ("R-SCALAR-CHAR", "bridge", "projected weak convergence gives scalar characteristic convergence at frequency one", "high", "mathlib:ProbabilityMeasure.tendsto_iff_tendsto_charFun", 35),
    ("R-PROJ-ID", "core-lemma", "charFun (map (projection t) mu) 1 = charFun mu t", "critical", "local:AnchorAudit.lean:projection_charFun_one_measure", 40),
    ("C-PROJECTION", "construction", "continuous measurable scalar projection x |-> inner x t", "high", "local:Statement.lean:continuous_projection", 25),
    ("X-SOURCE", "source-boundary", "primary proof source, assumptions, and errata crosswalk", "critical", None, 100),
    ("X-PROVENANCE", "provenance-boundary", "terminal bodies, imports, revisions, and licenses", "critical", None, 70),
    ("X-TRUST", "trust-boundary", "axiom closure, replay, freshness, and independent verification", "critical", None, 70),
]

def oid(suffix):
    return f"{PREFIX}-{suffix}"

obligations = []
for suffix, kind, target, risk, body, budget in specs:
    machine = "not_applicable" if suffix == "X-SOURCE" else "required"
    human = "required" if suffix in {"ROOT", "F", "R", "R-PROJ-ID", "X-SOURCE"} else "not_applicable"
    exclusion = None
    if machine == "not_applicable":
        exclusion = "Human source review is evidence and is not a Lean proposition."
    elif human == "not_applicable":
        exclusion = "Formal composition, representation, provenance, or trust duty; source mathematics is assigned to branch/source nodes."
    obligations.append({
        "obligation_id": oid(suffix),
        "statement_fingerprint": "sha256:" + hashlib.sha256(target.encode()).hexdigest(),
        "kind": kind,
        "formal_target": target,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": human,
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": body,
        "step_budget": budget,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in obligations]

registry = {
    "schema_version": "stage1-obligation-registry/5.6.0",
    "item_id": ITEM,
    "theorem_id": "THM-M-1013",
    "registry_version": 1,
    "base_revision": BASE,
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.md").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"),
    "freeze_basis": "Exact elaborated target and immutable anchor inventory; the characteristic-function route is frozen without claiming proof-phase closure.",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
    },
    "append_only_deltas": [],
    "obligations": obligations,
    "status_boundary": "Fourteen root-relevant obligations are frozen. Composition and boundary probes are checked, but proof-phase credit, source review, trust closure, master acceptance, and theorem completion remain open.",
}

edge_specs = {
    "proof": [("P01", "proof_requires", "ROOT", "T-COMPOSE"), ("P02", "proof_requires", "T-COMPOSE", "F"), ("P03", "proof_requires", "T-COMPOSE", "R"), ("P04", "proof_requires", "F", "F-MAP"), ("P05", "proof_requires", "F", "C-PROJECTION"), ("P06", "proof_requires", "R", "R-VECTOR-CHAR"), ("P07", "proof_requires", "R", "R-SCALAR-CHAR"), ("P08", "proof_requires", "R", "R-PROJ-ID"), ("P09", "proof_requires", "R-PROJ-ID", "C-PROJECTION")],
    "refinement": [("R01", "refines", "S", "ROOT"), ("R02", "refines", "S-BOUNDARY", "S"), ("R03", "refines", "F-MAP", "F"), ("R04", "refines", "R-VECTOR-CHAR", "R"), ("R05", "refines", "R-SCALAR-CHAR", "R"), ("R06", "refines", "R-PROJ-ID", "R")],
    "provenance": [("V01", "provenance_of", "X-PROVENANCE", "S"), ("V02", "provenance_of", "X-PROVENANCE", "F-MAP"), ("V03", "provenance_of", "X-PROVENANCE", "R-VECTOR-CHAR"), ("V04", "provenance_of", "X-PROVENANCE", "R-PROJ-ID")],
    "evidence": [("E01", "evidence_for", "X-TRUST", "T-COMPOSE"), ("E02", "evidence_for", "X-TRUST", "ROOT")],
    "trust": [("T01", "trusts", "ROOT", "X-TRUST"), ("T02", "trusts", "T-COMPOSE", "X-TRUST"), ("T03", "trusts", "F-MAP", "X-TRUST"), ("T04", "trusts", "R-VECTOR-CHAR", "X-TRUST")],
    "documentation": [("D01", "documents", "X-SOURCE", "ROOT"), ("D02", "source_map", "X-SOURCE", "F"), ("D03", "source_map", "X-SOURCE", "R"), ("D04", "documents", "S", "ROOT")],
    "workflow": [("W01", "workflow_depends_on", "T-COMPOSE", "S"), ("W02", "workflow_depends_on", "F", "F-MAP"), ("W03", "workflow_depends_on", "R", "R-VECTOR-CHAR"), ("W04", "workflow_depends_on", "R", "R-SCALAR-CHAR"), ("W05", "workflow_depends_on", "R", "R-PROJ-ID"), ("W06", "workflow_depends_on", "ROOT", "T-COMPOSE"), ("W07", "workflow_depends_on", "X-TRUST", "X-PROVENANCE")],
}

graphs = {}
for name, raw_edges in edge_specs.items():
    edges, out, incoming = [], {}, {}
    for eid, typ, source, target in raw_edges:
        edge = {"edge_id": eid, "type": typ, "from": oid(source), "to": oid(target)}
        edges.append(edge)
        out.setdefault(edge["from"], []).append(eid)
        incoming.setdefault(edge["to"], []).append(eid)
    graphs[name] = {"edges": edges, "out": out, "in": incoming}

known = {"S", "S-BOUNDARY", "T-COMPOSE", "F-MAP", "R-VECTOR-CHAR", "R-SCALAR-CHAR", "R-PROJ-ID", "C-PROJECTION"}
nodes = []
for row in obligations:
    suffix = row["obligation_id"][len(PREFIX) + 1:]
    nodes.append({
        "obligation_id": row["obligation_id"],
        "debt": "H1/" + ("NA" if suffix == "X-SOURCE" else "M3") + "/R3",
        "status": "architecture_checked" if suffix in known else "open",
        "meaning": row["formal_target"],
    })

bundle = {
    "schema_version": "stage1-typed-graphs/5.6.0",
    "item_id": ITEM,
    "theorem_id": "THM-M-1013",
    "root_obligation_id": oid("ROOT"),
    "registry_denominator_sha256": denominator,
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "root_closed": False,
        "theorem_complete": False,
        "immediate_open_root_cut_set": [oid("F"), oid("R")],
        "note": "Anchor candidates are inventoried, but proof execution and acceptance are downstream phases."
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(denominator)
