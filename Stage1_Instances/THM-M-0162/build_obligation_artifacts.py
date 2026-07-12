#!/usr/bin/env python3
"""Generate the frozen THM-M-0162 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0162-OBLIGATION_TREE"
THEOREM = "THM-M-0162"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("M0162-ROOT", "root", "critical", "The exact elaborated Frenet-Serret target.", "Stage1Instances.THM_M_0162.FrenetSerretTarget"),
    ("M0162-S-PREMISES", "definition", "high", "Freeze the open domain, derivative witnesses, unit speed, positive curvature, frame definitions, and torsion sign.", "Stage1Instances.THM_M_0162.FrenetPremises"),
    ("M0162-S-FOUNDATION", "certificate", "critical", "Audit classical logic, analysis imports, axioms, TCB, and the no-oracle policy.", "planned trust certificate"),
    ("M0162-F-ORTHONORMAL", "lemma", "critical", "Derive that T, N, and B form the positively oriented orthonormal frame on U.", "planned exact Lean frame-orthonormality target"),
    ("M0162-D-INNER", "lemma", "critical", "Differentiate all root-relevant frame inner products using the supplied derivative witnesses.", "planned exact Lean differentiated-inner-product identities"),
    ("M0162-A-DECOMPOSE", "lemma", "critical", "Decompose vector derivatives in the orthonormal basis and identify coefficients by dot products.", "planned exact Lean orthonormal-basis decomposition target"),
    ("M0162-E-TANGENT", "terminal", "high", "Use N = kappa^-1 T' and positive kappa to prove T' = kappa N.", "Stage1Instances.THM_M_0162.TangentEquationPackage"),
    ("M0162-C-NORMAL-T", "lemma", "critical", "Differentiate dot(T,N)=0 and use T'=kappa N to obtain the T coefficient of N'.", "planned exact Lean normal tangent-coefficient target"),
    ("M0162-C-NORMAL-N", "lemma", "high", "Differentiate dot(N,N)=1 to show the N coefficient of N' vanishes.", "planned exact Lean normal self-coefficient target"),
    ("M0162-C-NORMAL-B", "lemma", "critical", "Use differentiated B=T cross N identities and the torsion convention to identify dot(N',B)=tau.", "planned exact Lean normal binormal-coefficient target"),
    ("M0162-E-NORMAL", "terminal", "critical", "Assemble the three normal coefficients into N'=-kappa T+tau B.", "Stage1Instances.THM_M_0162.NormalEquationPackage"),
    ("M0162-D-CROSS", "lemma", "critical", "Differentiate B=T cross N and establish the cross-product product rule in Vec3.", "planned exact Lean derivative-of-cross-product target"),
    ("M0162-C-BINORMAL", "lemma", "critical", "Show the T and B coefficients of B' vanish and its N coefficient is -tau.", "planned exact Lean binormal coefficient target"),
    ("M0162-E-BINORMAL", "terminal", "critical", "Assemble the binormal coefficients into B'=-tau N.", "Stage1Instances.THM_M_0162.BinormalEquationPackage"),
    ("M0162-T-ASSEMBLE", "composition", "high", "Compose the three exact equation packages into the canonical conjunction and quantifier structure.", "Stage1Instances.THM_M_0162.root_of_equation_packages"),
    ("M0162-X-SOURCE", "source_boundary", "high", "Crosswalk every material identity and convention to pinpoint primary sources and errata.", "non-machine source crosswalk"),
    ("M0162-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, axioms, wrapper boundaries, and replay evidence.", "planned provenance certificate"),
]

source_na = {"M0162-S-PREMISES", "M0162-S-FOUNDATION", "M0162-X-PROVENANCE"}
machine_special = {"M0162-X-SOURCE": "not_applicable", "M0162-X-PROVENANCE": "informational"}
checked = {"M0162-S-PREMISES", "M0162-T-ASSEMBLE"}
obligations = []
nodes = []
for oid, kind, risk, statement, formal in rows:
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "planned:v1:sha256:" + digest([oid, kind, statement, formal]),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_only", "informational": "provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0162/ObligationTree.lean#root_of_equation_packages" if oid == "M0162-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0162-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": statement,
        "formal_target": formal,
        "output": statement,
        "human_debt": "H1",
        "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0162-ROOT" else "M4"),
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M0162-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or numerical certificate is credited",
        "step_budget": 60,
        "semantic_step_ledger": {"premises": "Only typed proof-requires children and the frozen formal context.", "inference": statement, "output": statement, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0162/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no open child is treated as proved.",
        "task_ids": [ITEM, "S56-M-0162-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0162/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-0162 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and completed bounded anchor audit; standard moving-frame derivation; eligibility frozen independently of proof status.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0162-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0162-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Architecture only; all three equation packages remain open and no root proof or theorem completion is claimed.",
}


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0162-ROOT": ["M0162-T-ASSEMBLE"],
    "M0162-T-ASSEMBLE": ["M0162-E-TANGENT", "M0162-E-NORMAL", "M0162-E-BINORMAL"],
    "M0162-E-TANGENT": ["M0162-S-PREMISES"],
    "M0162-E-NORMAL": ["M0162-F-ORTHONORMAL", "M0162-D-INNER", "M0162-A-DECOMPOSE", "M0162-C-NORMAL-T", "M0162-C-NORMAL-N", "M0162-C-NORMAL-B"],
    "M0162-C-NORMAL-T": ["M0162-E-TANGENT"],
    "M0162-C-NORMAL-N": ["M0162-D-INNER"],
    "M0162-C-NORMAL-B": ["M0162-D-CROSS"],
    "M0162-E-BINORMAL": ["M0162-F-ORTHONORMAL", "M0162-A-DECOMPOSE", "M0162-D-CROSS", "M0162-C-BINORMAL"],
    "M0162-C-BINORMAL": ["M0162-D-INNER", "M0162-D-CROSS"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-PREMISES", "M0162-ROOT", "logical_decomposition", "M0162-S-PREMISES")],
    "provenance": [edge("PROV-ROOT", "M0162-X-PROVENANCE", "provenance_of", "M0162-ROOT"), edge("SRC-FRAME", "M0162-F-ORTHONORMAL", "source_map", "M0162-X-SOURCE")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M0162-ROOT", "trusts", "M0162-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M0162-ROOT", "trusts", "M0162-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE", "M0162-X-SOURCE", "documents", "M0162-ROOT"), edge("DOC-PREMISES", "M0162-S-PREMISES", "documents", "M0162-ROOT")],
    "workflow": [edge("FLOW-PROOF-AUDIT", "M0162-E-TANGENT", "workflow_depends_on", "M0162-X-SOURCE"), edge("FLOW-VALIDATE-ASSEMBLE", "M0162-X-PROVENANCE", "workflow_depends_on", "M0162-T-ASSEMBLE")],
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
    "registry_id": "THM-M-0162-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0162-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composition runs child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0162-E-TANGENT", "M0162-E-NORMAL", "M0162-E-BINORMAL"], "composition_certificates": ["Stage1Instances.THM_M_0162.root_of_equation_packages"], "reason": "The checked final composition is conditional and all three equation packages lack proof bodies."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0162/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid, *_ in rows]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
