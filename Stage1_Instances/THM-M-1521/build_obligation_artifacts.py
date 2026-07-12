#!/usr/bin/env python3
"""Generate the frozen THM-M-1521 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1521-OBLIGATION_TREE"
THEOREM = "THM-M-1521"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("M1521-ROOT", "root", "critical", "The exact finite-measure preserving Poincare recurrence target.", "Stage1Instances.THM_M_1521.PoincareRecurrenceTarget", "The canonical proposition."),
    ("M1521-S-DEFINITIONS", "definition", "high", "Freeze iterates, almost-everywhere implication, frequently-atTop recurrence, and null-measurability.", "Stage1Instances.THM_M_1521.{SetRecurrenceConclusion,PoincareRecurrenceTarget}", "The exact statement interface."),
    ("M1521-S-BOUNDARY", "terminal", "normal", "Retain null sets, including the empty set, without a positive-measure side condition.", "Stage1Instances.THM_M_1521.emptySetBoundary", "The checked empty-set boundary and unchanged quantified target."),
    ("M1521-S-FOUNDATION", "certificate", "critical", "Fix the Lean, mathlib, classical-choice, quotient, extensionality, TCB, and no-oracle boundary.", "planned transitive axiom and trust report", "Accepted foundation and trust boundary."),
    ("M1521-N-FINITE", "transport", "high", "Install the explicit IsFiniteMeasure proposition as the local instance required by the pinned bridge.", "letI : MeasureTheory.IsFiniteMeasure mu := hFinite", "A context in which MeasurePreserving.conservative is applicable."),
    ("M1521-L-CONSERVATIVE", "bridge", "critical", "A measure-preserving self-map on a finite measure space is conservative.", "Stage1Instances.THM_M_1521.ObligationTree.PreservingToConservative", "MeasureTheory.Conservative f mu."),
    ("M1521-L-RECURRENCE", "bridge", "critical", "For a conservative map, almost every member of each null-measurable set returns to it frequently along Nat iterates.", "Stage1Instances.THM_M_1521.ObligationTree.ConservativeToSetRecurrence", "Stage1Instances.THM_M_1521.SetRecurrenceConclusion f mu."),
    ("M1521-T-ASSEMBLE", "terminal", "critical", "Compose the preservation bridge and conservative recurrence engine into the exact canonical root.", "Stage1Instances.THM_M_1521.ObligationTree.exactTarget_of_packages", "The exact canonical proposition, conditional on both bridge packages."),
    ("M1521-X-SOURCE", "terminal", "high", "Map the recurrence formulation and each material bridge to independently reviewed primary mathematical sources.", "non-machine node-specific source crosswalk", "Human-source coverage without proof credit."),
    ("M1521-X-PROVENANCE", "certificate", "critical", "Inventory wrapper, terminal mathlib bodies, imports, revisions, axioms, trust, and replay receipts.", "planned machine-derived provenance closure", "Unique terminal-body provenance without duplicate wrapper credit."),
]

checked = {"M1521-S-DEFINITIONS", "M1521-S-BOUNDARY", "M1521-T-ASSEMBLE"}
source_na = {"M1521-S-DEFINITIONS", "M1521-S-BOUNDARY", "M1521-S-FOUNDATION", "M1521-N-FINITE", "M1521-X-PROVENANCE"}
machine_special = {"M1521-X-SOURCE": "not_applicable", "M1521-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
root_fp = "lean-expression-sha256:3d7c202adf1f52ae3dbcdb46e7726395600cb0d89d93220d70d42b9b837f6c06"

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fp = root_fp if oid in {"M1521-ROOT", "M1521-S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1521/ObligationTree.lean#exactTarget_of_packages" if oid == "M1521-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-1521-" + oid.removeprefix("M1521-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1521-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit-map-provisional" if oid not in source_na else "not-applicable",
        "provenance_id": "pinned-mathlib-conservative-chain" if oid in {"M1521-L-CONSERVATIVE", "M1521-L-RECURRENCE"} else ("local-conditional-composition" if oid == "M1521-T-ASSEMBLE" else "none"),
        "foundation_profile": "lean4-mathlib-classical/provisional",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-release-audit-pending",
        "computation_record": "none; no oracle or external computation closes this node",
        "step_budget": 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires children and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge consumes this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1521/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; this node receives no proof acceptance in the obligation-tree phase.",
        "task_ids": [ITEM, "S56-M-1521-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1521/ObligationTree.lean"] if oid == "M1521-T-ASSEMBLE" else [],
        "owner": "THM-M-1521 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and audited conservative-system architecture; eligibility assigned from semantics, independently of candidate proof availability.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1521-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1521-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen denominator and architecture only; no bridge proof credit, source acceptance, audit completion, or theorem completion."
}


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M1521-ROOT": ["M1521-T-ASSEMBLE"],
    "M1521-T-ASSEMBLE": ["M1521-L-CONSERVATIVE", "M1521-L-RECURRENCE"],
    "M1521-L-CONSERVATIVE": ["M1521-N-FINITE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1521-ROOT", "logical_decomposition", "M1521-S-DEFINITIONS"), edge("REF-ROOT-BOUND", "M1521-ROOT", "logical_decomposition", "M1521-S-BOUNDARY"), edge("REF-CONS-FINITE", "M1521-L-CONSERVATIVE", "transports", "M1521-N-FINITE")],
    "provenance": [edge("SRC-CONS", "M1521-L-CONSERVATIVE", "source_map", "M1521-X-SOURCE"), edge("SRC-REC", "M1521-L-RECURRENCE", "source_map", "M1521-X-SOURCE"), edge("PROV-ROOT", "M1521-X-PROVENANCE", "provenance_of", "M1521-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1521-ROOT", "trusts", "M1521-S-FOUNDATION"), edge("TRUST-PROV", "M1521-ROOT", "trusts", "M1521-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M1521-S-DEFINITIONS", "documents", "M1521-ROOT"), edge("DOC-SOURCE", "M1521-X-SOURCE", "documents", "M1521-L-RECURRENCE")],
    "workflow": [edge("FLOW-ASSEMBLE-CONS", "M1521-T-ASSEMBLE", "workflow_depends_on", "M1521-L-CONSERVATIVE"), edge("FLOW-ASSEMBLE-REC", "M1521-T-ASSEMBLE", "workflow_depends_on", "M1521-L-RECURRENCE"), edge("FLOW-PROV-ASSEMBLE", "M1521-X-PROVENANCE", "workflow_depends_on", "M1521-T-ASSEMBLE")],
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
    "registry_id": "THM-M-1521-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1521-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1521-L-CONSERVATIVE", "M1521-L-RECURRENCE"], "composition_certificates": ["Stage1Instances.THM_M_1521.ObligationTree.exactTarget_of_packages"], "reason": "The final composition is conditional; imported candidate bodies are not accepted during this phase."}
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1521/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
