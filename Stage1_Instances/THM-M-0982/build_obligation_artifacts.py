#!/usr/bin/env python3
"""Build the frozen THM-M-0982 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0982-OBLIGATION_TREE"
THEOREM = "THM-M-0982"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


rows = [
    ("M0982-ROOT", "root", "critical", "The exact conjunction of continuity from below and continuity from above for a probability measure.", "Stage1Instances.THM_M_0982.ProbabilityContinuityTarget", "The canonical proposition."),
    ("M0982-B-BELOW", "branch", "critical", "Increasing measurable events have probabilities tending to the probability of their indexed union.", "Stage1Instances.THM_M_0982.ObligationTree.Below", "The below conjunct."),
    ("M0982-B-ABOVE", "branch", "critical", "Decreasing measurable events have probabilities tending to the probability of their indexed intersection.", "Stage1Instances.THM_M_0982.ObligationTree.Above", "The above conjunct."),
    ("M0982-L-BELOW-ANCHOR", "terminal", "high", "The pinned mathlib continuity-from-below theorem supplies the increasing-event limit (with a stronger premise set).", "MeasureTheory.tendsto_measure_iUnion_atTop", "The below limit for a monotone event sequence."),
    ("M0982-L-ABOVE-ANCHOR", "terminal", "high", "The pinned mathlib continuity-from-above theorem supplies the decreasing-event limit from null measurability and one finite member.", "MeasureTheory.tendsto_measure_iInter_atTop", "The above limit under the anchor premises."),
    ("M0982-T-NULL", "transport", "high", "Measurable events are null-measurable for the same measure.", "Stage1Instances.THM_M_0982.ObligationTree.measurable_to_nullMeasurable", "NullMeasurableSet for every event."),
    ("M0982-L-FINITE", "lemma", "high", "A probability measure assigns every event measure different from infinity.", "Stage1Instances.THM_M_0982.ObligationTree.probability_member_ne_top", "The finite-member premise at index zero."),
    ("M0982-S-BOUNDARY", "terminal", "normal", "Constant, empty, and universal event sequences remain within the frozen weak monotonicity statement.", "Stage1Instances.THM_M_0982.{constant_sequence_boundary,empty_union_boundary,universal_intersection_boundary}", "Checked encoding boundaries."),
    ("M0982-S-FOUNDATION", "certificate", "critical", "Record the transitive axiom, TCB, and no-oracle boundary for terminal bodies.", "planned exact proof-phase axiom and dependency report", "Accepted trust boundary."),
    ("M0982-X-SOURCE", "terminal", "high", "Map both continuity laws and every premise to pinpoint primary-source passages and errata review.", "non-machine primary-source crosswalk", "Human-source coverage without proof credit."),
    ("M0982-X-PROVENANCE", "certificate", "critical", "Distinguish the local wrappers from their two terminal mathlib proof bodies and bind immutable revisions.", "Stage1_Instances/THM-M-0982/anchor-audit.json", "Body-origin coverage without duplicate proof credit."),
]

machine_special = {"M0982-X-SOURCE": "not_applicable", "M0982-X-PROVENANCE": "informational"}
source_na = {"M0982-S-BOUNDARY", "M0982-S-FOUNDATION", "M0982-X-PROVENANCE"}
checked_local = {"M0982-T-NULL", "M0982-L-FINITE", "M0982-S-BOUNDARY"}
anchor_candidates = {"M0982-B-BELOW", "M0982-B-ABOVE", "M0982-L-BELOW-ANCHOR", "M0982-L-ABOVE-ANCHOR"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fp = "lean-expression-sha256:7ff4b7b4d50897c445c48b9d307a22590726bbbef6b6f8b064a8179d5d6cd088" if oid == "M0982-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    body = None
    if oid == "M0982-L-BELOW-ANCHOR": body = "mathlib@8a178386:MeasureTheory.tendsto_measure_iUnion_atTop"
    if oid == "M0982-L-ABOVE-ANCHOR": body = "mathlib@8a178386:MeasureTheory.tendsto_measure_iInter_atTop"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if machine == "not_applicable" else ("provenance_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": body,
    })
    debt = "M0-L" if oid in checked_local else ("M1" if oid in anchor_candidates else ("M3" if oid == "M0982-ROOT" else "M4"))
    nodes.append({
        "node_id": "THM-M-0982-" + oid.removeprefix("M0982-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": debt, "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "anchor-audit:M0982" if oid in anchor_candidates else "none",
        "foundation_profile": "lean4-mathlib/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no computation or oracle closes this node", "step_budget": 30,
        "semantic_step_ledger": {"premises": "Only typed proof children and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0982/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture and provisional node classification only; no proof-phase or theorem-completion acceptance.",
        "task_ids": [ITEM, "S56-M-0982-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0982/ObligationTree.lean"] if oid in checked_local else [],
        "owner": "THM-M-0982 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked_local else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked_local else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable anchor audit; branch, bridge, finiteness, boundary, source, trust, and provenance eligibility assigned before reading closure status.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0982-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0982-X-PROVENANCE"],
    },
    "delta_policy": "Any split, merge, exclusion, eligibility, or target correction creates a new registry version with append-only old/new ID mapping.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"locally_checked_support": sorted(checked_local), "anchor_candidates": sorted(anchor_candidates), "root_machine_debt": "M3"},
    "status_boundary": "The denominator and architecture are frozen; proof integration, H0, R0, release evidence, and theorem completion remain open.",
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal: value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0982-ROOT": ["M0982-B-BELOW", "M0982-B-ABOVE"],
    "M0982-B-BELOW": ["M0982-L-BELOW-ANCHOR"],
    "M0982-B-ABOVE": ["M0982-L-ABOVE-ANCHOR", "M0982-T-NULL", "M0982-L-FINITE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-BOUNDARY", "M0982-ROOT", "logical_decomposition", "M0982-S-BOUNDARY")],
    "provenance": [edge("PROV-BELOW", "M0982-L-BELOW-ANCHOR", "provenance_of", "M0982-X-PROVENANCE"), edge("PROV-ABOVE", "M0982-L-ABOVE-ANCHOR", "provenance_of", "M0982-X-PROVENANCE"), edge("SOURCE-BELOW", "M0982-B-BELOW", "source_map", "M0982-X-SOURCE"), edge("SOURCE-ABOVE", "M0982-B-ABOVE", "source_map", "M0982-X-SOURCE")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M0982-ROOT", "trusts", "M0982-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M0982-ROOT", "trusts", "M0982-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE-ROOT", "M0982-X-SOURCE", "documents", "M0982-ROOT"), edge("DOC-BOUNDARY-ROOT", "M0982-S-BOUNDARY", "documents", "M0982-ROOT")],
    "workflow": [edge("FLOW-PROOF-TREE", "M0982-ROOT", "workflow_depends_on", "M0982-X-PROVENANCE"), edge("FLOW-SOURCE", "M0982-ROOT", "workflow_depends_on", "M0982-X-SOURCE")],
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
    "registry_id": "THM-M-0982-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0982-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composition runs child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"locally_checked_support": sorted(checked_local), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0982-B-BELOW", "M0982-B-ABOVE"], "composition_certificates": ["Stage1Instances.THM_M_0982.ObligationTree.target_of_branches"], "reason": "The exact composition is conditional and proof-phase integration of both branch wrappers has not been accepted."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0982/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
