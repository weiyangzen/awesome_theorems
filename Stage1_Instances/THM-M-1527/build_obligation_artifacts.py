#!/usr/bin/env python3
"""Build the frozen THM-M-1527 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1527-OBLIGATION_TREE"
THEOREM = "THM-M-1527"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M1527-ROOT", "root", "critical", "The exact conditional Maxwell coordinate equivalence.", "Stage1Instances.THM_M_1527.MaxwellCoordinateEquivalence", "The canonical proposition."),
    ("M1527-S-DEFINITIONS", "definition", "high", "Freeze the four component predicates, covariant predicates, and conjunction association.", "Stage1Instances.THM_M_1527.{ClassicalMaxwellSystem,CovariantMaxwellSystem}", "The exact elaborated statement interface."),
    ("M1527-S-CONVENTIONS", "boundary", "critical", "Preserve dimension, signature, orientation, and positive-SI-constant premises without using them as hidden proof shortcuts.", "the six non-decomposition premises of MaxwellCoordinateEquivalence", "The exact model boundary carried to the root wrapper."),
    ("M1527-L-HOMOGENEOUS", "bridge", "critical", "Relate dF = 0 to Gauss-magnetic and Faraday under the supplied coordinate decomposition.", "CoordinateDecomposition.homogeneous_iff", "Homogeneous iff the two homogeneous component equations."),
    ("M1527-L-INHOMOGENEOUS", "bridge", "critical", "Relate d(star F) = J to Gauss-electric and Ampere-Maxwell under the supplied coordinate decomposition.", "CoordinateDecomposition.inhomogeneous_iff", "Inhomogeneous iff the two sourced component equations."),
    ("M1527-L-CONJUNCTION", "logic", "medium", "Reassociate and reorder the four classical conjuncts into homogeneous and inhomogeneous pairs.", "propositional conjunction normalization in assemble_from_component_equivalences", "The paired component propositions."),
    ("M1527-T-ASSEMBLE", "transport", "high", "Compose the two component equivalences and conjunction normalization.", "Stage1Instances.THM_M_1527.assemble_from_component_equivalences", "The exact equivalence for fixed fields, conditional on both bridges."),
    ("M1527-X-SOURCE", "source", "high", "Map both coordinate bridges and convention choices to reviewed primary-source passages.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M1527-X-FOUNDATION", "certificate", "critical", "Record imports, axioms, TCB, classical policy, and no-oracle status.", "planned transitive trust report", "Accepted trust boundary."),
    ("M1527-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, projections, wrappers, hashes, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without proof credit."),
]

checked = {"M1527-S-DEFINITIONS", "M1527-L-CONJUNCTION", "M1527-T-ASSEMBLE"}
source_na = {"M1527-S-DEFINITIONS", "M1527-S-CONVENTIONS", "M1527-L-CONJUNCTION", "M1527-X-FOUNDATION", "M1527-X-PROVENANCE"}
machine_special = {"M1527-X-SOURCE": "not_applicable", "M1527-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    machine = machine_special.get(oid, "required")
    fp = "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1527/ObligationTree.lean#assemble_from_component_equivalences" if oid == "M1527-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-1527-" + oid.removeprefix("M1527-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1527-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "local-conditional-composition" if oid == "M1527-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 40,
        "semantic_step_ledger": {"premises": "Only the declared proof children and formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parents may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1527/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or conditional interface only; no unlisted premise or root closure.",
        "task_ids": [ITEM, "S56-M-1527-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1527/ObligationTree.lean"] if oid == "M1527-T-ASSEMBLE" else [],
        "owner": "THM-M-1527 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and bounded anchor audit; two coordinate bridges plus checked propositional assembly; eligibility assigned before proof execution.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M1527-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M1527-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; the canonical root wrapper, source acceptance, trust closure, and theorem completion remain open.",
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M1527-ROOT": ["M1527-T-ASSEMBLE", "M1527-S-CONVENTIONS"],
    "M1527-T-ASSEMBLE": ["M1527-L-HOMOGENEOUS", "M1527-L-INHOMOGENEOUS", "M1527-L-CONJUNCTION"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1527-ROOT", "logical_decomposition", "M1527-S-DEFINITIONS")],
    "provenance": [edge("SRC-HOM", "M1527-L-HOMOGENEOUS", "source_map", "M1527-X-SOURCE"), edge("SRC-INHOM", "M1527-L-INHOMOGENEOUS", "source_map", "M1527-X-SOURCE"), edge("PROV-ROOT", "M1527-X-PROVENANCE", "provenance_of", "M1527-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1527-ROOT", "trusts", "M1527-X-FOUNDATION"), edge("TRUST-PROV", "M1527-ROOT", "trusts", "M1527-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", "M1527-S-DEFINITIONS", "documents", "M1527-ROOT"), edge("DOC-SOURCE", "M1527-X-SOURCE", "documents", "M1527-L-HOMOGENEOUS")],
    "workflow": [edge("FLOW-ASSEMBLE-HOM", "M1527-T-ASSEMBLE", "workflow_depends_on", "M1527-L-HOMOGENEOUS"), edge("FLOW-ASSEMBLE-INHOM", "M1527-T-ASSEMBLE", "workflow_depends_on", "M1527-L-INHOMOGENEOUS"), edge("FLOW-PROV-ASSEMBLE", "M1527-X-PROVENANCE", "workflow_depends_on", "M1527-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming = {oid: [] for oid in ids}
    outgoing = {oid: [] for oid in ids}
    for item in edges:
        outgoing[item["from"]].append(item["edge_id"])
        incoming[item["to"]].append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1527-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1527-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "minimal_open_root_cut": ["M1527-L-HOMOGENEOUS", "M1527-L-INHOMOGENEOUS", "M1527-S-CONVENTIONS"],
    "closure_boundary": {"root_closed": False, "theorem_complete": False, "reason": "Only conditional propositional assembly is checked; canonical wrapper, trust, source, and release gates remain open."},
}
specs = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1527/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids],
}

for filename, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / filename).write_text(json.dumps(value, indent=2) + "\n")
print(denominator)
