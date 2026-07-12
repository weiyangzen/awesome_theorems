#!/usr/bin/env python3
"""Deterministically build the THM-M-1010 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1010-OBLIGATION_TREE"


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


rows = [
    ("M1010-ROOT", "root", "critical", "Exact Polish-space Skorokhod representation target.", "Stage1Instances.THM_M_1010.Target"),
    ("M1010-S-DEFINITIONS", "definition", "high", "Freeze weak convergence, probability laws, the common probability space, and almost-sure convergence.", "Stage1Instances.THM_M_1010.{WeakConvergence,Representation}"),
    ("M1010-S-DOMAIN", "definition", "critical", "Preserve the universe, topology, Borel measurable structure, Polish instance, and all probability-measure binders.", "Stage1Instances.THM_M_1010.Target"),
    ("M1010-S-BOUNDARY", "branch", "high", "Cover atomic laws, countable spaces, constant sequences, and empty exceptional sets without strengthening the hypotheses.", "planned exact boundary lemmas for Target"),
    ("M1010-S-FOUNDATION", "certificate", "critical", "Audit classical choice, measure-theoretic quotients, imports, axioms, and the Lean/mathlib TCB.", "planned transitive trust report"),
    ("M1010-N-PARTITIONS", "construction", "critical", "Construct refining countable Borel partitions with shrinking mesh and limit-law-null boundaries.", "planned Polish partition package for mu"),
    ("M1010-C-INTERVAL", "construction", "high", "Fix one atomless standard probability space and its measurable interval coding interface.", "planned atomless interval probability-space package"),
    ("M1010-C-COUPLING", "construction", "critical", "Use partition masses and weak convergence to construct all representatives on the common space.", "Stage1Instances.THM_M_1010.ObligationTree.CouplingPackage"),
    ("M1010-L-MEASURABLE", "core_lemma", "critical", "Prove every constructed representative is a.e. measurable.", "planned AEMeasurable fields for the coupling"),
    ("M1010-L-LAWS", "core_lemma", "critical", "Prove the pushforward of each representative is exactly its prescribed probability measure.", "planned HasLaw fields for muSeq and mu"),
    ("M1010-L-AE-STABILIZE", "core_lemma", "critical", "Outside one null set, show the finite partition codes eventually agree at every fixed refinement level.", "planned almost-everywhere code stabilization theorem"),
    ("M1010-L-METRIC-CONVERGENCE", "bridge", "critical", "Turn stabilization in shrinking partition cells into convergence in the original Polish topology.", "planned Tendsto theorem for the constructed representatives"),
    ("M1010-T-ASSEMBLE", "terminal", "high", "Convert the complete coupling data into the exact canonical Representation and Target.", "Stage1Instances.THM_M_1010.ObligationTree.target_of_couplingPackage"),
    ("M1010-X-SOURCE", "terminal", "high", "Map the partition and coupling argument to pinpoint primary mathematical sources and assumptions.", "non-machine source boundary"),
    ("M1010-X-PROVENANCE", "certificate", "critical", "Track terminal bodies, imports, pins, axioms, validation receipts, and replay inputs.", "planned provenance closure"),
]

checked = {"M1010-S-DEFINITIONS", "M1010-S-DOMAIN", "M1010-T-ASSEMBLE"}
source_na = {"M1010-S-DEFINITIONS", "M1010-S-FOUNDATION", "M1010-X-PROVENANCE"}
machine_special = {"M1010-X-SOURCE": "not_applicable", "M1010-X-PROVENANCE": "informational"}
root_fp = "lean-expression-sha256:f5f12340fa49d0be0eed038c99c47c921017284447b4a73f4b096e085e800d18"
obligations = []
nodes = []
for oid, kind, risk, claim, target in rows:
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": root_fp if oid == "M1010-ROOT" else "planned:v1:sha256:" + digest([oid, claim, target]),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if machine == "not_applicable" else ("release_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1010/ObligationTree.lean#target_of_couplingPackage" if oid == "M1010-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-1010-" + oid.removeprefix("M1010-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": claim,
        "formal_target": target,
        "output": claim,
        "human_debt": "H1",
        "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1010-ROOT" else "M4"),
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit-provisional" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M1010-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or experiment is credited",
        "step_budget": 40,
        "semantic_step_ledger": {
            "premises": "Only the exact formal context and incoming proof requirements recorded in the proof graph.",
            "inference": claim,
            "output": claim,
            "outgoing_use": "Only the declared typed edges consume this output.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-1010/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional composition only; no open coupling or analytic obligation receives proof credit.",
        "task_ids": [ITEM, "S56-M-1010-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1010/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-1010 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-12" if oid in checked else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["Statement.lean", "anchor_audit.json", "toolchain", "registry"],
            "revocation_state": "provisional" if oid in checked else "open",
        },
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": "THM-M-1010",
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus the pre-closure partition-coupling architecture; eligibility is independent of observed proof status.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor_audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1010-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M1010-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new version with an append-only old/new ID delta.",
    "obligations": obligations,
    "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "The denominator and a conditional final conversion are frozen; the coupling construction and root remain open.",
}


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M1010-ROOT": ["M1010-T-ASSEMBLE"],
    "M1010-T-ASSEMBLE": ["M1010-C-COUPLING"],
    "M1010-C-COUPLING": ["M1010-N-PARTITIONS", "M1010-C-INTERVAL", "M1010-L-MEASURABLE", "M1010-L-LAWS", "M1010-L-METRIC-CONVERGENCE"],
    "M1010-L-METRIC-CONVERGENCE": ["M1010-L-AE-STABILIZE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [
        edge("REF-ROOT-DEFS", "M1010-ROOT", "logical_decomposition", "M1010-S-DEFINITIONS"),
        edge("REF-ROOT-DOMAIN", "M1010-ROOT", "logical_decomposition", "M1010-S-DOMAIN"),
        edge("REF-ROOT-BOUNDARY", "M1010-ROOT", "logical_decomposition", "M1010-S-BOUNDARY"),
    ],
    "provenance": [
        edge("SRC-PARTITIONS", "M1010-N-PARTITIONS", "source_map", "M1010-X-SOURCE"),
        edge("SRC-COUPLING", "M1010-C-COUPLING", "source_map", "M1010-X-SOURCE"),
        edge("PROV-ROOT", "M1010-X-PROVENANCE", "provenance_of", "M1010-ROOT"),
    ],
    "evidence": [],
    "trust": [
        edge("TRUST-FOUNDATION", "M1010-ROOT", "trusts", "M1010-S-FOUNDATION"),
        edge("TRUST-PROVENANCE", "M1010-ROOT", "trusts", "M1010-X-PROVENANCE"),
    ],
    "documentation": [
        edge("DOC-DEFS", "M1010-S-DEFINITIONS", "documents", "M1010-ROOT"),
        edge("DOC-SOURCE", "M1010-X-SOURCE", "documents", "M1010-C-COUPLING"),
    ],
    "workflow": [
        edge("FLOW-COUPLING-PARTITIONS", "M1010-C-COUPLING", "workflow_depends_on", "M1010-N-PARTITIONS"),
        edge("FLOW-COUPLING-INTERVAL", "M1010-C-COUPLING", "workflow_depends_on", "M1010-C-INTERVAL"),
        edge("FLOW-CONVERGENCE-STABILIZE", "M1010-L-METRIC-CONVERGENCE", "workflow_depends_on", "M1010-L-AE-STABILIZE"),
        edge("FLOW-ASSEMBLY-COUPLING", "M1010-T-ASSEMBLE", "workflow_depends_on", "M1010-C-COUPLING"),
        edge("FLOW-PROVENANCE-ASSEMBLY", "M1010-X-PROVENANCE", "workflow_depends_on", "M1010-T-ASSEMBLE"),
    ],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": "THM-M-1010",
    "registry_id": "THM-M-1010-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": "M1010-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": sorted(checked),
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1010-N-PARTITIONS", "M1010-C-INTERVAL", "M1010-L-MEASURABLE", "M1010-L-LAWS", "M1010-L-AE-STABILIZE"],
        "composition_certificates": ["Stage1Instances.THM_M_1010.ObligationTree.target_of_couplingPackage"],
        "reason": "The checked final conversion is conditional on the open coupling package.",
    },
}

recipes = []
for oid in ids:
    recipes.append({
        "recipe_id": "VAL-" + oid,
        "cwd": ".",
        "argv": ["python3", "Stage1_Instances/THM-M-1010/check_obligation_tree.py"],
        "env_allowlist": {},
        "timeout_seconds": 120,
        "network_policy": "denied",
        "expected_exit": 0,
        "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1010 obligation tree"}],
        "covered_obligation_ids": [oid],
        "covered_declarations": ["Stage1Instances.THM_M_1010.ObligationTree.target_of_couplingPackage"] if oid == "M1010-T-ASSEMBLE" else [],
    })
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1010", "recipes": recipes}

tasks = {
    "schema_version": "stage1-task-dag/1.0",
    "item_id": ITEM,
    "theorem_id": "THM-M-1010",
    "tasks": [
        {"task_id": ITEM + "-FREEZE", "kind": "freeze_registry", "depends_on": [], "covered_obligation_ids": ids, "state": "provisional_self_tested"},
        {"task_id": ITEM + "-LEAN-COMPOSE", "kind": "check_composition", "depends_on": [ITEM + "-FREEZE"], "covered_obligation_ids": ["M1010-ROOT", "M1010-T-ASSEMBLE"], "state": "provisional_self_tested"},
        {"task_id": "S56-M-1010-PROOF", "kind": "implement_open_obligations", "depends_on": [ITEM + "-LEAN-COMPOSE"], "covered_obligation_ids": bundle["closure_boundary"]["remaining_root_cut_set"], "state": "open"},
    ],
}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs), ("task-dag.json", tasks)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(ids)} obligations; denominator {denominator}")
