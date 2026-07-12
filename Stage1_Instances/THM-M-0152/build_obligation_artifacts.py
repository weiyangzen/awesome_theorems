#!/usr/bin/env python3
"""Build the frozen THM-M-0152 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def planned(text):
    return "planned:v1:sha256:" + sha(text)


items = [
    ("M0152-ROOT", "root", "Exact TheoremaEgregiumTarget", "Stage1Instances.THM_M_0152.TheoremaEgregiumTarget", "critical", "H1", "M4"),
    ("M0152-S-DEFINITIONS", "definition", "Definitions of regularity, metric coefficients, normal, and Gaussian curvature agree with the frozen target", "Statement.lean definitions and theoremaEgregiumTarget_iff_expandedTarget", "high", "H1", "M0-L"),
    ("M0152-S-REGULAR", "lemma", "Regularity makes the two tangent vectors independent and EG-F^2 nonzero", "forall X p, Regular X -> metricDeterminant X p != 0", "critical", "H1", "M4"),
    ("M0152-S-LOCAL-INVERSE", "lemma", "The eventual inverse identities give inverse differentials after shrinking the neighborhood", "IsLocalCoordinateEquivAt phi psi p -> local differential inverse identities", "high", "H1", "M4"),
    ("M0152-N-LOCAL", "normalization", "Shrink to one neighborhood where inverse, smoothness, metric preservation, and derivative identities all hold", "exists s in nhds p, forall q in s, all local hypotheses hold", "high", "H1", "M4"),
    ("M0152-B-ORIENTATION", "branch", "Both choices of unit normal give the same value of LN-M^2", "gaussian numerator is invariant under normal -> -normal", "normal", "H1", "M4"),
    ("M0152-C-CHRISTOFFEL", "construction", "Construct the tangential coefficients of second derivatives from the metric and its first derivatives", "Christoffel coefficients determined by firstFundamentalForm and its first derivatives", "critical", "H1", "M4"),
    ("M0152-L-CHAIN", "core_lemma", "First and second Frechet derivative chain rules transport the two-jets through phi", "two-jet chain rule for Y o phi at p", "critical", "H1", "M4"),
    ("M0152-L-METRIC-JET", "core_lemma", "Neighborhood metric equality implies equality of the required metric two-jets at p", "IsLocalIsometryAt X Y phi p -> equality of metric coefficient derivatives through order two", "critical", "H1", "M4"),
    ("M0152-L-GAUSS-CANCEL", "core_lemma", "Eliminate normal second-derivative terms to express LN-M^2 intrinsically", "Gauss equation in the frozen coordinate encoding", "critical", "H1", "M4"),
    ("M0152-L-INTRINSIC-FORMULA", "bridge", "Express the frozen Gaussian-curvature quotient solely from metric coefficients and their derivatives", "gaussianCurvature X p = intrinsicMetricFormula X p", "critical", "H1", "M4"),
    ("M0152-T-INVARIANCE", "terminal", "The intrinsic metric formula is invariant under the local coordinate equivalence", "intrinsicMetricFormula Y (phi p) = intrinsicMetricFormula X p", "critical", "H1", "M4"),
    ("M0152-T-ASSEMBLE", "transport", "Compose the two intrinsic-formula equalities with coordinate invariance to obtain the exact root", "required children imply TheoremaEgregiumTarget", "critical", "H1", "M4"),
    ("M0152-S-FOUNDATION", "certificate", "Audit classical choice, quotient, extensionality, denominator, and TCB policy", "axiom and trust report for terminal declarations", "critical", "H1", "M4"),
    ("M0152-X-EXTERNAL", "bridge", "Classify the external intrinsic pullback-naturality candidate without proof credit", "candidate C03 provenance boundary", "high", "H1", "M3"),
    ("M0152-X-SOURCE", "terminal", "Map every mathematical node to Gauss Articles 11-12 and a modern proof source with assumptions and errata", "human source crosswalk", "high", "H1", "M4"),
    ("M0152-X-PROVENANCE", "certificate", "Record terminal bodies, transitive imports, axioms, placeholders, TCB, and replay evidence", "formal provenance and evidence closure", "critical", "H1", "M4"),
]

required_machine = {x[0] for x in items if not x[0].startswith("M0152-X-")}
required_machine.add("M0152-X-EXTERNAL")
source_na = {"M0152-S-DEFINITIONS", "M0152-S-FOUNDATION", "M0152-X-PROVENANCE"}
obligations = []
for oid, kind, human, formal, risk, hdebt, mdebt in items:
    exact = oid in {"M0152-ROOT", "M0152-S-DEFINITIONS"}
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-expression-sha256:898c24a88007838d739dc3ec63103e92ba06df082fa6d0b91557ba3863de2f02" if exact else planned(formal),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "required" if oid in required_machine else ("informational" if oid == "M0152-X-PROVENANCE" else "not_applicable"),
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": ({"M0152-X-SOURCE": "human_source_boundary_only", "M0152-X-PROVENANCE": "release_overlay_no_proof_credit"}.get(oid)),
        "terminal_proof_body_id": None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")))
ids = [x[0] for x in items]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": "S56-M-0152-OBLIGATION_TREE",
    "theorem_id": "THM-M-0152",
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated parametrized-surface target and bounded anchor audit; classical coordinate proof architecture; eligibility fixed without using closure status.",
    "frozen_against_statement_sha256": sha((HERE / "Statement.lean").read_bytes()),
    "frozen_against_anchor_audit_sha256": sha((HERE / "anchor-audit.json").read_bytes()),
    "root_obligation_id": "M0152-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0152-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
    "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M0152-S-DEFINITIONS"], "root_machine_debt": "M4"},
    "status_boundary": "This freezes scope and execution architecture only. No curvature proof, H0 source closure, audit completion, or theorem completion is claimed.",
}

proof_pairs = [
    ("M0152-ROOT", "M0152-T-ASSEMBLE"),
    ("M0152-T-ASSEMBLE", "M0152-L-INTRINSIC-FORMULA"),
    ("M0152-T-ASSEMBLE", "M0152-T-INVARIANCE"),
    ("M0152-L-INTRINSIC-FORMULA", "M0152-S-REGULAR"),
    ("M0152-L-INTRINSIC-FORMULA", "M0152-C-CHRISTOFFEL"),
    ("M0152-L-INTRINSIC-FORMULA", "M0152-L-GAUSS-CANCEL"),
    ("M0152-L-INTRINSIC-FORMULA", "M0152-B-ORIENTATION"),
    ("M0152-C-CHRISTOFFEL", "M0152-L-CHAIN"),
    ("M0152-L-GAUSS-CANCEL", "M0152-C-CHRISTOFFEL"),
    ("M0152-T-INVARIANCE", "M0152-S-LOCAL-INVERSE"),
    ("M0152-T-INVARIANCE", "M0152-N-LOCAL"),
    ("M0152-T-INVARIANCE", "M0152-L-METRIC-JET"),
    ("M0152-L-METRIC-JET", "M0152-L-CHAIN"),
    ("M0152-N-LOCAL", "M0152-S-LOCAL-INVERSE"),
]

def graph(edges):
    out = {i: [] for i in ids}
    inc = {i: [] for i in ids}
    for e in edges:
        out[e["from"]].append(e["edge_id"])
        inc[e["to"]].append(e["edge_id"])
    return {"edges": edges, "out": out, "in": inc}

proof_edges = []
for n, (parent, child) in enumerate(proof_pairs, 1):
    a, b = f"P{n:02d}R", f"P{n:02d}C"
    proof_edges += [
        {"edge_id": a, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": b},
        {"edge_id": b, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": a},
    ]

def simple(prefix, typ, pairs):
    return graph([{"edge_id": f"{prefix}{i:02d}", "type": typ, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)])

node_lookup = {x[0]: x for x in items}
nodes = []
for oid in ids:
    _, kind, human, formal, _, hdebt, mdebt = node_lookup[oid]
    premises = [b for a, b in proof_pairs if a == oid]
    nodes.append({
        "node_id": "THM-M-0152-" + oid.removeprefix("M0152-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": hdebt, "machine_debt": mdebt, "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "pending:M0152-X-SOURCE" if oid not in source_na else "not-applicable",
        "provenance_id": "pending:M0152-X-PROVENANCE", "foundation_profile": "lean4-classical-v1",
        "tcb_profile": "lean4-pinned-kernel-v1", "computation_record": "none",
        "step_budget": 24 if premises else 48,
        "semantic_step_ledger": {"premises": premises, "inference": "planned exact Lean composition" if premises else "planned direct proof ledger", "output": human, "outgoing_use": [a for a, b in proof_pairs if b == oid]},
        "public_readable_target": f"Stage1_Instances/THM-M-0152/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture entry only; debt labels are not proof evidence.",
        "task_ids": ["S56-M-0152-PROOF", "S56-M-0152-VALIDATION"],
        "owned_sources": ["Stage1_Instances/THM-M-0152/Statement.lean", "Stage1_Instances/THM-M-0152/obligation-registry.json"],
        "owner": "Stage1 rev-5.6 execution lane", "reviewer": "independent integration-lane reviewer required",
        "validity": {"validated_at": "2026-07-12", "review_due": "before proof or release acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry version"], "revocation_state": "active provisional"},
    })

graphs = {
    "proof": graph(proof_edges),
    "refinement": simple("R", "logical_decomposition", [("M0152-ROOT", x) for x in ["M0152-S-DEFINITIONS", "M0152-S-REGULAR", "M0152-S-LOCAL-INVERSE", "M0152-S-FOUNDATION"]]),
    "provenance": simple("V", "provenance_of", [("M0152-X-PROVENANCE", "M0152-ROOT"), ("M0152-X-EXTERNAL", "M0152-L-INTRINSIC-FORMULA")]),
    "evidence": simple("E", "evidence_for", [("M0152-X-PROVENANCE", "M0152-S-DEFINITIONS")]),
    "trust": simple("T", "trusts", [("M0152-ROOT", "M0152-S-FOUNDATION")]),
    "documentation": simple("D", "documents", [("M0152-X-SOURCE", x) for x in ["M0152-ROOT", "M0152-L-GAUSS-CANCEL", "M0152-L-INTRINSIC-FORMULA"]]),
    "workflow": simple("W", "workflow_depends_on", [("M0152-ROOT", "M0152-X-PROVENANCE"), ("M0152-X-PROVENANCE", "M0152-X-SOURCE")]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": registry["item_id"], "theorem_id": registry["theorem_id"],
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "minimal_open_root_cut": ["M0152-L-INTRINSIC-FORMULA", "M0152-T-INVARIANCE"], "audit_complete": False, "theorem_complete": False},
}
recipes = [{"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0152/check_obligation_tree.py"], "env": {}, "timeout_seconds": 30, "network": "disabled", "covered_ids": [oid]} for oid in ids]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": registry["item_id"], "theorem_id": registry["theorem_id"], "recipes": recipes}
for name, value in [("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)]:
    (HERE / name).write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n")
print(denominator)
