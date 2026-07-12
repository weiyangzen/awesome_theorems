#!/usr/bin/env python3
"""Build the frozen THM-M-0320 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0320-OBLIGATION_TREE"
THEOREM = "THM-M-0320"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("M0320-ROOT", "root", "critical", "The exact frozen Euclidean Kakutani target.", "Stage1Instances.THM_M_0320.KakutaniFixedPointTarget", "A fixed point x in K with x in F x."),
    ("M0320-S-STATEMENT", "definition", "high", "Preserve all nine hypotheses, binder scopes, and the fixed-point conclusion.", "Stage1Instances.THM_M_0320.KakutaniFixedPointTarget", "The exact elaborated root interface."),
    ("M0320-S-FOUNDATION", "certificate", "critical", "Freeze classical logic, choice, imports, TCB, and the no-oracle policy.", "planned transitive axiom and TCB report", "An accepted foundation boundary."),
    ("M0320-T-COMPACT", "transport", "high", "Derive compactness of K from closedness and bornological boundedness in Euclidean space.", "Stage1Instances.THM_M_0320.compact_of_closed_bounded", "IsCompact K."),
    ("M0320-T-GRAPH", "transport", "critical", "Derive the selected closed correspondence graph from upper hemicontinuity and closed values on closed K.", "Stage1Instances.THM_M_0320.UpperHemicontinuityClosedGraphBridge", "IsClosed (CorrespondenceGraph K F)."),
    ("M0320-C-CORE", "external_core", "critical", "Supply a locally licensed, pinned, kernel-checked closed-graph Kakutani theorem at the frozen finite-dimensional type.", "Stage1Instances.THM_M_0320.ClosedGraphKakutaniCore", "A fixed point under compact-convex closed-graph premises."),
    ("M0320-T-SUBTYPE", "integration", "critical", "Check ambient/subtype correspondence conversion required by the audited external candidate.", "planned wrapper around harfe/fixed-point-theorems-lean4.kakutani_fixed_point", "The exact local ClosedGraphKakutaniCore interface."),
    ("M0320-T-ASSEMBLE", "composition", "high", "Compose compactness, the closed-graph bridge, and the core without weakening the root.", "Stage1Instances.THM_M_0320.root_of_closedGraph_packages", "The exact canonical root, conditional on the two open packages."),
    ("M0320-X-SOURCE", "source_boundary", "high", "Map every material premise and proof transition to reviewed primary-source passages and errata.", "node-specific primary-source crosswalk pending", "Human-source coverage without machine proof credit."),
    ("M0320-X-PROVENANCE", "certificate", "critical", "Inventory wrapper, terminal proof bodies, license, imports, axioms, TCB, and replay evidence.", "planned transitive provenance packet", "Release provenance without mathematical proof credit."),
]

checked = {"M0320-S-STATEMENT", "M0320-T-COMPACT", "M0320-T-ASSEMBLE"}
source_na = {"M0320-S-STATEMENT", "M0320-S-FOUNDATION", "M0320-X-PROVENANCE"}
machine_special = {"M0320-X-SOURCE": "not_applicable", "M0320-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fp = ("source-expression-sha256:" + statement_hash if oid in {"M0320-ROOT", "M0320-S-STATEMENT"}
          else "planned:v1:sha256:" + digest([oid, kind, claim, target, output]))
    machine = machine_special.get(oid, "required")
    source = "not_applicable" if oid in source_na else "required"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": source, "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0320/ObligationTree.lean#compact_of_closed_bounded" if oid == "M0320-T-COMPACT" else
                                   "local:Stage1_Instances/THM-M-0320/ObligationTree.lean#root_of_closedGraph_packages" if oid == "M0320-T-ASSEMBLE" else None),
    })
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0320-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1" if oid == "M0320-ROOT" else "H3",
        "machine_debt": "M0-L" if oid in checked else ("M1" if oid in {"M0320-ROOT", "M0320-C-CORE", "M0320-T-SUBTYPE"} else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if source == "not_applicable" else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M0320-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical or external oracle output may close this node",
        "step_budget": 80 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only declared proof-requirement children and the frozen formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parent or non-proof support edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0320/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen interface or conditional composition only; no unlisted premise and no root closure.",
        "task_ids": [ITEM, "S56-M-0320-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0320/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-0320 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{k: row[k] for k in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus bounded anchor audit; eligibility assigned before closure status; external closed-graph architecture expanded into compactness, graph, subtype, core, composition, source, and provenance obligations.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0320-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids, "informational_overlays": ["M0320-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M1"},
    "status_boundary": "Scope and denominators only; the core, graph bridge, subtype integration, source review, and theorem completion remain open.",
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0320-ROOT": ["M0320-T-ASSEMBLE"],
    "M0320-T-ASSEMBLE": ["M0320-T-COMPACT", "M0320-T-GRAPH", "M0320-C-CORE"],
    "M0320-C-CORE": ["M0320-T-SUBTYPE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-STMT", "M0320-ROOT", "logical_decomposition", "M0320-S-STATEMENT"), edge("REF-ROOT-FOUND", "M0320-ROOT", "logical_decomposition", "M0320-S-FOUNDATION")],
    "provenance": [edge("SRC-CORE", "M0320-C-CORE", "source_map", "M0320-X-SOURCE"), edge("PROV-ROOT", "M0320-X-PROVENANCE", "provenance_of", "M0320-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M0320-ROOT", "trusts", "M0320-S-FOUNDATION"), edge("TRUST-PROV", "M0320-ROOT", "trusts", "M0320-X-PROVENANCE")],
    "documentation": [edge("DOC-STMT", "M0320-S-STATEMENT", "documents", "M0320-ROOT"), edge("DOC-SOURCE", "M0320-X-SOURCE", "documents", "M0320-C-CORE")],
    "workflow": [edge("FLOW-ASSEMBLE-GRAPH", "M0320-T-ASSEMBLE", "workflow_depends_on", "M0320-T-GRAPH"), edge("FLOW-ASSEMBLE-CORE", "M0320-T-ASSEMBLE", "workflow_depends_on", "M0320-C-CORE"), edge("FLOW-CORE-SUBTYPE", "M0320-C-CORE", "workflow_depends_on", "M0320-T-SUBTYPE"), edge("FLOW-PROV-CORE", "M0320-X-PROVENANCE", "workflow_depends_on", "M0320-C-CORE")],
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
    "registry_id": "THM-M-0320-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0320-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0320-T-GRAPH", "M0320-C-CORE"], "composition_certificates": ["Stage1Instances.THM_M_0320.root_of_closedGraph_packages"], "reason": "The composition theorem is conditional; the graph bridge and locally integrated closed-graph core have no accepted proof bodies."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0320/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid, *_ in rows]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
