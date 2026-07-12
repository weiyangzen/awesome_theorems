#!/usr/bin/env python3
"""Build the frozen THM-M-1016 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM, THEOREM, PREFIX = "S56-M-1016-OBLIGATION_TREE", "THM-M-1016", "M1016"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen finite-dimensional delta-method proposition.", "Stage1Instances.THM_M_1016.StatementShape", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze weak convergence, finite-dimensional Borel spaces, positive divergent scaling, and the Frechet derivative.", "Stage1Instances.THM_M_1016.StatementShape binders", "The exact elaborated vocabulary and scope."),
    ("S-BOUNDARIES", "normalization", "high", "Preserve zero derivative, constant transformations, degenerate limits, and one-dimensional specializations without weakening hypotheses.", "checked statement mutations and boundary ledger", "The frozen boundary policy."),
    ("S-FOUNDATION", "certificate", "critical", "Audit imports, classical principles, transitive axioms, TCB, and the noncomputable boundary.", "planned axiom/import/TCB certificate", "Accepted foundation profile."),
    ("N-TIGHTNESS", "bridge", "critical", "Derive boundedness in probability of the normalized input from convergence in distribution.", "planned finite-dimensional tightness theorem", "The normalized input is bounded in probability."),
    ("N-CONCENTRATION", "bridge", "critical", "Use positive scaling tending to infinity and normalized-input tightness to show X_n tends to theta in probability.", "planned scaling/concentration theorem", "X_n converges to theta in measure."),
    ("C-REMAINDER", "construction", "critical", "Define the Frechet remainder and prove its measurability and exact algebraic decomposition.", "planned measurable Frechet-remainder package", "A measurable quotient-free remainder identity."),
    ("L-LITTLE-O", "core_lemma", "critical", "Evaluate the Frechet little-o estimate along X_n to obtain an o-in-probability remainder factor.", "planned HasFDerivAt probabilistic little-o bridge", "The local remainder factor tends to zero in probability."),
    ("L-PRODUCT", "core_lemma", "critical", "Prove that an o-in-probability factor times a bounded-in-probability vector sequence tends to zero in probability.", "planned finite-dimensional product lemma", "The scaled Frechet remainder tends to zero in measure."),
    ("L-LINEAR-MAP", "bridge", "high", "Apply the continuous mapping theorem to the continuous linear derivative.", "TendstoInDistribution.continuous_comp g'.continuous", "The linearized statistic converges to g'(Z)."),
    ("T-REMAINDER", "terminal", "critical", "Combine concentration, little-o, boundedness, product, and measurability into the exact scaled remainder premise.", "planned TendstoInMeasure scaled-remainder theorem", "The nonlinear statistic minus its linearization tends to zero in measure."),
    ("T-ASSEMBLE", "transport", "high", "Compose linearized convergence and the negligible remainder with mathlib's Slutsky bridge.", "Stage1Instances.THM_M_1016.deltaMethod_of_remainder", "The exact conclusion conditional on the remainder leaf."),
    ("X-SOURCE", "terminal", "high", "Map every analytic and probabilistic bridge to a reviewed theorem/page, assumptions, conventions, and errata record.", "non-machine primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, wrappers, axioms, trust edges, and replay receipts.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARIES", f"{PREFIX}-L-LINEAR-MAP", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-expression-sha256:9cdb0281811565d62d5b8a7cc2933f27facd49e39aff10c29fe1d7702797dbee"
obligations, nodes = [], []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fingerprint = statement_fp if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind, "root_relevant": True,
        "machine_eligibility": machine, "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1016/ObligationTree.lean#deltaMethod_of_remainder" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind, "human_statement": claim,
        "formal_target": target, "output": output, "human_debt": "H2",
        "machine_debt": "M0-L" if oid in checked else ("M3" if suffix == "ROOT" else "M4"), "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-probability-analysis/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node", "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact declared proof children and the frozen formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parent edges may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-1016/obligation-tree.md#{oid.lower()}", "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1016-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1016/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1016 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact statement and immutable anchor audit; finite-dimensional Frechet remainder architecture frozen independently of closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": oids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [], "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no delta-method proof, H0 source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal: row["reciprocal_edge_id"] = reciprocal
    return row


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"], f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-L-LINEAR-MAP", f"{PREFIX}-T-REMAINDER"],
    f"{PREFIX}-T-REMAINDER": [f"{PREFIX}-C-REMAINDER", f"{PREFIX}-L-LITTLE-O", f"{PREFIX}-L-PRODUCT"],
    f"{PREFIX}-L-LITTLE-O": [f"{PREFIX}-N-CONCENTRATION", f"{PREFIX}-C-REMAINDER"],
    f"{PREFIX}-L-PRODUCT": [f"{PREFIX}-N-TIGHTNESS", f"{PREFIX}-L-LITTLE-O"], f"{PREFIX}-N-CONCENTRATION": [f"{PREFIX}-N-TIGHTNESS"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]
graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARIES")],
    "provenance": [edge("SRC-REMAINDER", f"{PREFIX}-T-REMAINDER", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [], "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-BOUND", f"{PREFIX}-S-BOUNDARIES", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-T-REMAINDER")],
    "workflow": [edge("FLOW-ASSEMBLE-REM", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-REMAINDER"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"]); incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": f"{THEOREM}-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator, "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs, "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": [f"{PREFIX}-T-REMAINDER"], "composition_certificates": ["Stage1Instances.THM_M_1016.deltaMethod_of_remainder"],
        "reason": "Final composition is conditional; the scaled Frechet remainder has no proof body."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1016/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in oids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
