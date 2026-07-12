#!/usr/bin/env python3
"""Build the frozen THM-M-0346 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0346-OBLIGATION_TREE"
THEOREM = "THM-M-0346"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


rows = [
    ("M0346-ROOT", "root", "critical", "The exact unit-circle L2 almost-everywhere Fourier convergence target.", "Stage1.THM_M_0346.CarlesonTarget", 40),
    ("M0346-S-ENCODING", "definition", "high", "Freeze the unit AddCircle, probability Haar measure, Lp coercion, Fourier coefficient, and inclusive symmetric cutoff.", "Stage1.THM_M_0346.{symmetricPartialSum,CarlesonTarget}", 40),
    ("M0346-S-FOUNDATION", "certificate", "critical", "Audit classical choice, imports, transitive axioms, TCB, and the no-oracle boundary.", "planned foundation and trust report", 40),
    ("M0346-C-REPRESENTATIVE", "construction", "critical", "Choose the canonical measurable representative of each Lp class and obtain its MemLp 2 certificate.", "planned Lp representative/MemLp adapter", 60),
    ("M0346-N-NORMALIZATION", "normalization", "critical", "Match period one, normalized Haar measure, character sign, and Fourier coefficient normalization with the integrated theorem.", "planned AddCircle normalization transport", 80),
    ("M0346-N-CUTOFF", "normalization", "critical", "Prove the upstream partialFourierSum' equals the inclusive integer interval sum used by symmetricPartialSum.", "planned partial-sum equality", 80),
    ("M0346-L-CARLESON-HUNT", "core_lemma", "critical", "Integrate and kernel-check Carleson-Hunt at p = 2 for the representative.", "fpvandoorn/carleson carleson_hunt at pinned compatible revision", 100),
    ("M0346-T-AE-REP", "transport", "critical", "Transport the a.e. upstream limit from the selected representative to the Lp coercion appearing in the frozen target.", "planned a.e. representative equality transport", 60),
    ("M0346-T-ASSEMBLE", "transport", "high", "Compose the analytic theorem and all checked transports into the canonical target.", "Stage1.THM_M_0346.root_of_transported_carleson_hunt", 40),
    ("M0346-X-SOURCE", "terminal", "high", "Map every analytic and transport obligation to reviewed primary-source passages and conventions.", "node-specific primary-source crosswalk", 40),
    ("M0346-X-PROVENANCE", "certificate", "critical", "Inventory upstream and local terminal bodies, wrappers, imports, licenses, axioms, and replay evidence.", "planned provenance closure", 40),
]

checked = {"M0346-S-ENCODING", "M0346-T-ASSEMBLE"}
source_na = {"M0346-S-ENCODING", "M0346-S-FOUNDATION", "M0346-X-PROVENANCE"}
machine_special = {"M0346-X-SOURCE": "not_applicable", "M0346-X-PROVENANCE": "informational"}
obligations = []
nodes = []
for oid, kind, risk, claim, target, budget in rows:
    machine = machine_special.get(oid, "required")
    fp = ("lean-source-sha256:" + hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
          if oid in {"M0346-ROOT", "M0346-S-ENCODING"}
          else "planned:v1:sha256:" + digest([oid, kind, claim, target]))
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0346/ObligationTree.lean#root_of_transported_carleson_hunt" if oid == "M0346-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-0346-" + oid.removeprefix("M0346-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target,
        "output": "The stated node output, consumable only through declared typed edges.",
        "human_debt": "H3", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0346-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M0346-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/external-closure-pending",
        "computation_record": "none; no oracle or numerical experiment may close this node",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only declared proof_requires children and the frozen formal context.", "inference": claim, "output": "The stated node output.", "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0346/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-0346-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0346/ObligationTree.lean"] if oid == "M0346-T-ASSEMBLE" else [],
        "owner": "THM-M-0346 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus immutable anchor audit; integration-first Carleson-Hunt architecture selected before closure status.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.md").read_bytes()).hexdigest(),
    "root_obligation_id": "M0346-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0346-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; the external theorem and transports are open, so no root proof or theorem completion is claimed.",
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M0346-ROOT": ["M0346-T-ASSEMBLE"],
    "M0346-T-ASSEMBLE": ["M0346-C-REPRESENTATIVE", "M0346-N-NORMALIZATION", "M0346-N-CUTOFF", "M0346-L-CARLESON-HUNT", "M0346-T-AE-REP"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ENCODING", "M0346-ROOT", "logical_decomposition", "M0346-S-ENCODING"), edge("REF-FOUNDATION", "M0346-ROOT", "logical_decomposition", "M0346-S-FOUNDATION")],
    "provenance": [edge("SRC-CARLESON", "M0346-L-CARLESON-HUNT", "source_map", "M0346-X-SOURCE"), edge("PROV-ROOT", "M0346-X-PROVENANCE", "provenance_of", "M0346-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M0346-ROOT", "trusts", "M0346-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M0346-ROOT", "trusts", "M0346-X-PROVENANCE")],
    "documentation": [edge("DOC-ENCODING", "M0346-S-ENCODING", "documents", "M0346-ROOT"), edge("DOC-SOURCE", "M0346-X-SOURCE", "documents", "M0346-L-CARLESON-HUNT")],
    "workflow": [edge("FLOW-ASSEMBLE-UPSTREAM", "M0346-T-ASSEMBLE", "workflow_depends_on", "M0346-L-CARLESON-HUNT"), edge("FLOW-CUTOFF-UPSTREAM", "M0346-N-CUTOFF", "workflow_depends_on", "M0346-L-CARLESON-HUNT"), edge("FLOW-AEREP-REP", "M0346-T-AE-REP", "workflow_depends_on", "M0346-C-REPRESENTATIVE"), edge("FLOW-PROV-ASSEMBLE", "M0346-X-PROVENANCE", "workflow_depends_on", "M0346-T-ASSEMBLE")],
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
    "registry_id": "THM-M-0346-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0346-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0346-C-REPRESENTATIVE", "M0346-N-NORMALIZATION", "M0346-N-CUTOFF", "M0346-L-CARLESON-HUNT", "M0346-T-AE-REP"], "composition_certificates": ["Stage1.THM_M_0346.root_of_transported_carleson_hunt"], "reason": "The final assembly is conditional; its analytic and transport premises have no accepted proof bodies."},
}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
