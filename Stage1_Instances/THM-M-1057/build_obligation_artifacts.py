#!/usr/bin/env python3
"""Generate the frozen THM-M-1057 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

ITEM = "S56-M-1057-OBLIGATION_TREE"
THEOREM = "THM-M-1057"
PREFIX = "M1057"

ROWS = [
    ("ROOT", "root", "The exact frozen ergodic Kingman target.", "Stage1Instances.THM_M_1057.KingmanTarget", "The canonical proposition.", 40, "H1", "M3", "critical", "required", "required"),
    ("S-DEFINITIONS", "definition", "Freeze the process, normalization, expected average, and positive-index infimum.", "Stage1Instances.THM_M_1057.{KingmanData,normalizedProcess,expectedAverage,kingmanValue}", "The exact elaborated vocabulary.", 40, "H1", "M0-L", "high", "not_applicable", "required"),
    ("S-BOUNDARY", "terminal", "Preserve the expanded statement and the distinct zero and positive-index boundaries.", "Stage1Instances.THM_M_1057.{kingmanTarget_iff_expandedSourceShape,zeroIndexNormalizationBoundary,positiveIndexMembershipBoundary}", "Checked statement and boundary behavior.", 40, "H1", "M0-L", "high", "not_applicable", "required"),
    ("S-FOUNDATION", "certificate", "Audit imports, axioms, classical choice, TCB, and the no-oracle boundary.", "planned transitive axiom and import certificate", "Accepted foundation and trust profile.", 40, "H1", "M4", "critical", "not_applicable", "required"),
    ("N-EXPECTATION-SUBADDITIVE", "normalization", "Integrate the cocycle inequality using iterate preservation and derive subadditivity of expected values.", "planned exact integral/subadditivity lemma", "A subadditive real sequence n |-> integral X_n.", 100, "H1", "M4", "critical", "required", "required"),
    ("L-FEKETE", "bridge", "Apply the audited deterministic Fekete anchor with the required bounded-below proof.", "Subadditive.tendsto_lim via a checked target-specific bridge", "Convergence and infimum identification for normalized expectations.", 60, "H1", "M3", "high", "required", "required"),
    ("C-BLOCK-DECOMPOSITION", "construction", "Decompose long cocycle values into fixed-size blocks plus controlled remainders.", "planned measurable block decomposition and remainder bounds", "Block-average estimates usable by the maximal branch.", 100, "H1", "M4", "critical", "required", "required"),
    ("L-MAXIMAL-INEQUALITY", "core_lemma", "Prove the subadditive maximal/ergodic estimate needed to control limsup and liminf.", "planned Kingman maximal inequality", "Almost-everywhere bounds for normalized process oscillation.", 100, "H1", "M4", "critical", "required", "required"),
    ("L-AE-CONVERGENCE", "core_lemma", "Derive almost-everywhere convergence of the normalized process to a measurable finite limit.", "planned a.e. pointwise convergence theorem", "A measurable real-valued pointwise limit g.", 100, "H1", "M4", "critical", "required", "required"),
    ("L-INVARIANCE", "core_lemma", "Show the pointwise limit is invariant almost everywhere under the transformation.", "planned limit invariance theorem", "g composed with T equals g almost everywhere.", 80, "H1", "M4", "critical", "required", "required"),
    ("L-ERGODIC-IDENTIFICATION", "bridge", "Use ergodic constancy and expectation asymptotics to identify the limit with kingmanValue.", "Ergodic.ae_eq_const_of_ae_eq_comp_ae plus planned constant identification", "g equals the positive-index expectation infimum almost everywhere.", 100, "H1", "M4", "critical", "required", "required"),
    ("T-LIMIT-PACKAGE", "terminal", "Combine convergence, invariance, and value identification into the explicit package consumed by assembly.", "Stage1Instances.THM_M_1057.PointwiseLimitPackage", "The complete conditional pointwise-limit package.", 40, "H1", "M4", "critical", "required", "required"),
    ("T-ASSEMBLE", "transport", "Compose the explicit pointwise-limit package into the exact canonical target.", "Stage1Instances.THM_M_1057.root_of_pointwiseLimitPackage", "KingmanTarget, conditional on PointwiseLimitPackage.", 40, "H1", "M0-L", "high", "required", "required"),
    ("X-SOURCE", "terminal", "Map every analytic branch to primary theorem pages, hypotheses, conventions, and errata.", "human source boundary only", "Accepted node-specific human-source crosswalk.", 100, "H1", "M4", "high", "required", "required"),
    ("X-PROVENANCE", "certificate", "Inventory terminal bodies, wrappers, imports, axioms, TCB, replay inputs, and licenses.", "release provenance overlay", "Accepted provenance and replay inventory.", 60, "H1", "M4", "critical", "not_applicable", "required"),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def planned(text):
    return "planned:v1:sha256:" + sha(text.encode())

obligations = []
nodes = []
for suffix, kind, human, formal, output, budget, hdebt, mdebt, risk, helig, relig in ROWS:
    oid = f"{PREFIX}-{suffix}"
    terminal = None
    if suffix == "T-ASSEMBLE":
        terminal = "local:Stage1_Instances/THM-M-1057/ObligationTree.lean#root_of_pointwiseLimitPackage"
    fingerprint = ("lean-expression-sha256:" + json.loads((HERE / "statement.json").read_text())["canonical_formal_target"]["elaborated_expression_sha256"]) if suffix == "ROOT" else planned(human + "|" + formal)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": "informational" if suffix == "X-PROVENANCE" else ("not_applicable" if suffix == "X-SOURCE" else "required"),
        "human_source_eligibility": helig, "readable_eligibility": relig,
        "risk_class": risk, "exclusion_reason": "human_source_boundary_only" if suffix == "X-SOURCE" else ("release_provenance_overlay_no_proof_credit" if suffix == "X-PROVENANCE" else None),
        "terminal_proof_body_id": terminal,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hdebt, "machine_debt": mdebt, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if helig == "required" else "not-applicable",
        "provenance_id": "none", "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only declared proof children and the exact formal context.", "inference": human, "output": output, "outgoing_use": "Only declared typed parents may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1057/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1057-PROOF"], "owned_sources": [], "owner": "THM-M-1057 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if mdebt == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if mdebt == "M0-L" else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode())
ids = [row["obligation_id"] for row in obligations]

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and bounded anchor audit; Kingman block/maximal/convergence/invariance architecture; eligibility frozen independently of closure.",
    "frozen_against_statement_sha256": sha((HERE / "Statement.lean").read_bytes()),
    "frozen_against_anchor_audit_sha256": sha((HERE / "anchor-audit.json").read_bytes()),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [f"{PREFIX}-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": [f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no Kingman proof, source acceptance, audit completion, or theorem completion.",
}

proof_pairs = [
    ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "T-LIMIT-PACKAGE"),
    ("T-LIMIT-PACKAGE", "L-AE-CONVERGENCE"), ("T-LIMIT-PACKAGE", "L-INVARIANCE"), ("T-LIMIT-PACKAGE", "L-ERGODIC-IDENTIFICATION"),
    ("L-AE-CONVERGENCE", "C-BLOCK-DECOMPOSITION"), ("L-AE-CONVERGENCE", "L-MAXIMAL-INEQUALITY"),
    ("L-MAXIMAL-INEQUALITY", "C-BLOCK-DECOMPOSITION"),
    ("L-ERGODIC-IDENTIFICATION", "L-INVARIANCE"), ("L-ERGODIC-IDENTIFICATION", "L-FEKETE"),
    ("L-FEKETE", "N-EXPECTATION-SUBADDITIVE"),
]

def graph(name, raw_edges):
    edges, incoming, outgoing = [], {i: [] for i in ids}, {i: [] for i in ids}
    for index, (src, dst, typ, reciprocal) in enumerate(raw_edges, 1):
        eid = f"{name.upper()}-{index:03d}"
        edge = {"edge_id": eid, "from": src, "to": dst, "type": typ}
        if reciprocal is not None: edge["reciprocal_edge_id"] = reciprocal
        edges.append(edge); outgoing[src].append(eid); incoming[dst].append(eid)
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_raw = []
for index, (p, c) in enumerate(proof_pairs):
    req, comp = f"PROOF-{2*index+1:03d}", f"PROOF-{2*index+2:03d}"
    proof_raw.extend([(f"{PREFIX}-{p}", f"{PREFIX}-{c}", "proof_requires", comp), (f"{PREFIX}-{c}", f"{PREFIX}-{p}", "composes", req)])

refinement = [(f"{PREFIX}-ROOT", f"{PREFIX}-{x}", "logical_decomposition", None) for x in ("S-DEFINITIONS", "S-BOUNDARY", "S-FOUNDATION")]
provenance = [(f"{PREFIX}-{x}", f"{PREFIX}-X-PROVENANCE", "provenance_of", None) for x in ("ROOT", "T-ASSEMBLE", "L-FEKETE", "L-ERGODIC-IDENTIFICATION")]
evidence = [(f"{PREFIX}-{x}", f"{PREFIX}-X-PROVENANCE", "provenance_of", None) for x in ("S-BOUNDARY", "S-DEFINITIONS")]
trust = [(f"{PREFIX}-{x}", f"{PREFIX}-S-FOUNDATION", "trusts", None) for x in ("ROOT", "T-ASSEMBLE", "L-FEKETE")]
documentation = [(f"{PREFIX}-{x}", f"{PREFIX}-X-SOURCE", "documents", None) for x in ("ROOT", "N-EXPECTATION-SUBADDITIVE", "L-MAXIMAL-INEQUALITY", "L-AE-CONVERGENCE", "L-INVARIANCE", "L-ERGODIC-IDENTIFICATION")]
workflow = [(f"{PREFIX}-{a}", f"{PREFIX}-{b}", "workflow_depends_on", None) for a, b in (("T-LIMIT-PACKAGE", "L-AE-CONVERGENCE"), ("T-LIMIT-PACKAGE", "L-INVARIANCE"), ("T-LIMIT-PACKAGE", "L-ERGODIC-IDENTIFICATION"), ("L-FEKETE", "N-EXPECTATION-SUBADDITIVE"), ("L-ERGODIC-IDENTIFICATION", "L-FEKETE"), ("ROOT", "T-ASSEMBLE"))]

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1057-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": {"proof": graph("proof", proof_raw), "refinement": graph("refinement", refinement), "provenance": graph("provenance", provenance), "evidence": graph("evidence", evidence), "trust": graph("trust", trust), "documentation": graph("documentation", documentation), "workflow": graph("workflow", workflow)},
    "closure_boundary": {"root_closed": False, "root_machine_debt": "M3", "minimal_open_cut": [f"{PREFIX}-T-LIMIT-PACKAGE"], "audit_complete": False, "theorem_complete": False, "reason": "Only conditional child-to-root composition is checked; every analytic branch remains open."},
}

recipes = [{"recipe_id": n["validation_spec_id"], "obligation_id": n["obligation_id"], "kind": "lean_exact_type" if n["machine_debt"] == "M0-L" else "planned_node_validation", "acceptance": "Exact node-specific evidence and independent review; unknown state fails closed."} for n in nodes]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes, "status_boundary": "Recipes define future node gates; their presence is not evidence that open obligations passed."}

for filename, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / filename).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
