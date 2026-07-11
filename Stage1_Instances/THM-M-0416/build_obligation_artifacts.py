#!/usr/bin/env python3
"""Build the frozen THM-M-0416 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0416-OBLIGATION_TREE"
THEOREM = "THM-M-0416"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M0416-ROOT", "root", "critical", "The exact frozen Dirichlet unit theorem proposition.", "Stage1Instances.THM_M_0416.DirichletUnitTheoremTarget", "M3"),
    ("M0416-C-COMPOSE", "composition", "high", "Compose the four mathematical packages into the exact conjunction.", "Stage1Instances.THM_M_0416.ObligationTree.root_of_packages", "M0-L"),
    ("M0416-I-FREE", "instance", "critical", "The additive units-mod-torsion quotient is a free Z-module.", "Module.Free ℤ (UnitsModTorsion K)", "M0-W"),
    ("M0416-I-FINITE", "instance", "critical", "The additive units-mod-torsion quotient is a finite Z-module.", "Module.Finite ℤ (UnitsModTorsion K)", "M0-W"),
    ("M0416-T-RANK", "terminal", "critical", "Its finrank equals NumberField.Units.rank K.", "NumberField.Units.rank_modTorsion", "M0-W"),
    ("M0416-T-COORDINATES", "terminal", "critical", "Every unit has unique torsion and fundamental-unit coordinates.", "NumberField.Units.exist_unique_eq_mul_prod", "M0-W"),
    ("M0416-X-SOURCE", "source_boundary", "high", "Map all mathematical packages to pinpoint primary-source passages and conventions.", "non-machine primary-source crosswalk", "M4"),
    ("M0416-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, typeclass providers, imports, and transitive body provenance.", "planned provenance closure", "M4"),
    ("M0416-X-TRUST", "certificate", "critical", "Validate the accepted foundation, axiom, TCB, and no-oracle boundary.", "planned trust closure", "M4"),
]

source_na = {"M0416-C-COMPOSE", "M0416-X-PROVENANCE", "M0416-X-TRUST"}
machine_special = {"M0416-X-SOURCE": "not_applicable", "M0416-X-PROVENANCE": "informational", "M0416-X-TRUST": "informational"}
obligations = []
nodes = []
for oid, kind, risk, claim, target, debt in rows:
    machine = machine_special.get(oid, "required")
    terminal = {
        "M0416-C-COMPOSE": "local:Stage1_Instances/THM-M-0416/ObligationTree.lean#root_of_packages",
        "M0416-T-RANK": "mathlib:NumberField.Units.rank_modTorsion",
        "M0416-T-COORDINATES": "mathlib:NumberField.Units.exist_unique_eq_mul_prod",
    }.get(oid)
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": "planned:v1:sha256:" + digest([oid, claim, target]),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_only", "informational": "release_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": terminal,
    })
    nodes.append({
        "node_id": "THM-M-0416-" + oid.removeprefix("M0416-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": claim,
        "human_debt": "H1", "machine_debt": debt, "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "anchor:S56-M-0416-C01" if oid in {"M0416-I-FREE", "M0416-I-FINITE", "M0416-T-RANK", "M0416-T-COORDINATES"} else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no computation or oracle is credited",
        "step_budget": 30, "semantic_step_ledger": {"premises": "Only incoming typed proof edges and the frozen formal context.", "inference": claim, "output": claim, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0416/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen architecture or candidate route only; proof integration and acceptance remain later gates.",
        "task_ids": [ITEM, "S56-M-0416-PROOF"], "owner": "THM-M-0416 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid == "M0416-C-COMPOSE" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid == "M0416-C-COMPOSE" else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus pinned anchor audit; four conjunct packages frozen before proof integration metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0416-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0416-X-PROVENANCE", "M0416-X-TRUST"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M0416-C-COMPOSE"], "candidate_obligations": ["M0416-I-FREE", "M0416-I-FINITE", "M0416-T-RANK", "M0416-T-COORDINATES"], "root_machine_debt": "M3"},
    "status_boundary": "Denominators and interfaces only; candidate availability is not proof integration, provenance acceptance, or theorem completion.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


proof = []
for parent, children in {"M0416-ROOT": ["M0416-C-COMPOSE"], "M0416-C-COMPOSE": ["M0416-I-FREE", "M0416-I-FINITE", "M0416-T-RANK", "M0416-T-COORDINATES"]}.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

edge_sets = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-SOURCE", "M0416-ROOT", "refined_by", "M0416-X-SOURCE")],
    "provenance": [edge("PROV-RANK", "M0416-T-RANK", "provenance_requires", "M0416-X-PROVENANCE"), edge("PROV-COORD", "M0416-T-COORDINATES", "provenance_requires", "M0416-X-PROVENANCE")],
    "evidence": [],
    "trust": [edge("TRUST-ROOT", "M0416-ROOT", "trusts", "M0416-X-TRUST"), edge("TRUST-PROV", "M0416-X-PROVENANCE", "trusts", "M0416-X-TRUST")],
    "documentation": [edge("DOC-SOURCE-ROOT", "M0416-X-SOURCE", "documents", "M0416-ROOT")],
    "workflow": [edge("FLOW-PROOF-OBL", "S56-M-0416-PROOF", "workflow_depends_on", ITEM), edge("FLOW-VALID-PROOF", "S56-M-0416-VALIDATION", "workflow_depends_on", "S56-M-0416-PROOF"), edge("FLOW-RELEASE-VALID", "S56-M-0416-RELEASE", "workflow_depends_on", "S56-M-0416-VALIDATION")],
}
graphs = {}
for name, edges in edge_sets.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0416-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0416-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M0416-C-COMPOSE"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0416-I-FREE", "M0416-I-FINITE", "M0416-T-RANK", "M0416-T-COORDINATES"], "composition_certificates": ["Stage1Instances.THM_M_0416.ObligationTree.root_of_packages"], "reason": "The four exact mathlib-backed candidates have not received proof-integration, transitive provenance/trust, and acceptance receipts."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0416/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
