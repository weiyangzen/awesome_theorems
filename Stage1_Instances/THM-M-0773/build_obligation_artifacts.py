#!/usr/bin/env python3
"""Build the frozen THM-M-0773 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0773-OBLIGATION_TREE"
THEOREM = "THM-M-0773"


def sha(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


ROWS = [
    ("M0773-ROOT", "root", "critical", "Prove the exact nonempty-family Teichmuller-Tukey target.", "Stage1Instances.THM_M_0773.TeichmullerTukeyTarget", 20),
    ("M0773-S-INTERFACE", "definition", "high", "Preserve arbitrary universes, finite character, nonemptiness, and relative subset-maximality.", "Stage1Instances.THM_M_0773.TeichmullerTukeyTarget", 25),
    ("M0773-C-SEED", "construction", "high", "Choose a seed x in F from the explicit nonemptiness hypothesis.", "F.Nonempty -> exists x, x in F", 15),
    ("M0773-L-POINTED", "bridge", "critical", "Extend every seed x in F to a member m in F maximal under inclusion.", "Stage1Instances.THM_M_0773.ObligationTree.PointedMaximalPackage", 100),
    ("M0773-T-FORGET", "composition", "high", "Compose seed choice and the pointed extension package, forgetting only x subseteq m.", "Stage1Instances.THM_M_0773.ObligationTree.root_of_pointedPackage", 20),
    ("M0773-X-SOURCE", "source_boundary", "critical", "Map finite character, nonemptiness, and maximality to reviewed primary-source passages.", "primary source node map pending", 60),
    ("M0773-X-FOUNDATION", "trust_boundary", "critical", "Audit Zorn, classical choice, transitive axioms, unsafe declarations, and the complete TCB.", "pinned transitive trust report pending", 50),
    ("M0773-X-PROVENANCE", "certificate", "high", "Bind the pointed terminal body, wrapper, immutable revision, license, and validation receipts.", "proof-body provenance ledger pending", 40),
    ("M0773-X-READABLE", "documentation", "high", "Reconstruct the chain-union finite-character argument and wrapper composition for review.", "readable reconstruction pending", 100),
    ("M0773-X-WORKFLOW", "workflow_gate", "high", "Require proof, validation, and release receipts before root promotion.", "rev-5.6 proof -> validation -> release workflow", 20),
]

checked = {"M0773-S-INTERFACE", "M0773-C-SEED", "M0773-T-FORGET"}
source_na = {"M0773-S-INTERFACE", "M0773-C-SEED", "M0773-X-FOUNDATION", "M0773-X-PROVENANCE", "M0773-X-WORKFLOW"}
machine = {"M0773-X-SOURCE": "not_applicable", "M0773-X-PROVENANCE": "informational", "M0773-X-READABLE": "not_applicable", "M0773-X-WORKFLOW": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, budget in ROWS:
    eligibility = machine.get(oid, "required")
    fp = ("lean-expression-sha256:68aa26cd5bfd9033298490cc521d4c26b0fd5bd62f6431259532573d1a699f14"
          if oid in {"M0773-ROOT", "M0773-S-INTERFACE"}
          else "planned:v1:sha256:" + sha([oid, kind, claim, target]))
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": eligibility,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "step_budget": budget,
        "exclusion_reason": ("human_source_boundary_only" if oid == "M0773-X-SOURCE" else
                             "non_machine_readability_boundary" if oid == "M0773-X-READABLE" else
                             "release_overlay_no_proof_credit" if eligibility == "informational" else None),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0773/ObligationTree.lean#root_of_pointedPackage" if oid == "M0773-T-FORGET" else
                                   "mathlib:Mathlib.Order.TeichmullerTukey#Order.IsOfFiniteCharacter.exists_maximal" if oid == "M0773-L-POINTED" else None),
    })
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0773-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": claim,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0773-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md; primary passage acceptance pending",
        "provenance_id": "anchor-audit.json" if oid in {"M0773-L-POINTED", "M0773-X-FOUNDATION", "M0773-X-PROVENANCE"} else "none",
        "foundation_profile": "Lean dependent type theory; audited candidate reports propext, Classical.choice, Quot.sound; transitive release audit pending",
        "tcb_profile": "Lean 4.29.0 + mathlib 8a178386; full transitive closure and independent replay pending",
        "computation_record": "none; noncomputable existence proof; no oracle or unchecked computation credited",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only declared proof_requires children and the exact formal context.", "inference": claim, "output": claim, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0773/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture" + (" with kernel-checked conditional composition" if oid in checked else " only") + "; no root proof credit.",
        "task_ids": [ITEM, "S56-M-0773-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0773/ObligationTree.lean"] if oid in checked else [],
        "owner": "THM-M-0773 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

ids = [row[0] for row in ROWS]
denominator = sha(obligations)
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated target and pinned anchor audit; seed selection, pointed maximal extension, and forgetful composition are separated independently of closure status.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0773-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility change, or re-fingerprint requires a new version and append-only old/new ID delta.",
    "append_only_delta": [], "obligations": obligations,
    "status_observed_after_freeze": {"provisionally_checked_interfaces": sorted(checked), "accepted_closed_obligations": [], "root_machine_debt": "M3"},
    "status_boundary": "Architecture only; no accepted proof, source, readability, validation, or theorem-completion claim."
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {"M0773-ROOT": ["M0773-S-INTERFACE", "M0773-T-FORGET"], "M0773-T-FORGET": ["M0773-C-SEED", "M0773-L-POINTED"]}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-SEED", "M0773-ROOT", "logical_decomposition", "M0773-C-SEED"), edge("REF-ROOT-POINTED", "M0773-ROOT", "logical_decomposition", "M0773-L-POINTED")],
    "provenance": [edge("PROV-POINTED", "M0773-X-PROVENANCE", "provenance_of", "M0773-L-POINTED"), edge("PROV-WRAPPER", "M0773-X-PROVENANCE", "provenance_of", "M0773-T-FORGET")],
    "evidence": [edge("SRC-ROOT", "M0773-X-SOURCE", "source_map", "M0773-ROOT"), edge("SRC-POINTED", "M0773-X-SOURCE", "source_map", "M0773-L-POINTED")],
    "trust": [edge("TRUST-ROOT", "M0773-ROOT", "trusts", "M0773-X-FOUNDATION"), edge("TRUST-POINTED", "M0773-L-POINTED", "trusts", "M0773-X-FOUNDATION")],
    "documentation": [edge("DOC-ROOT", "M0773-X-READABLE", "documents", "M0773-ROOT"), edge("DOC-POINTED", "M0773-X-READABLE", "documents", "M0773-L-POINTED")],
    "workflow": [edge("FLOW-ROOT-SOURCE", "M0773-ROOT", "workflow_depends_on", "M0773-X-SOURCE"), edge("FLOW-ROOT-PROV", "M0773-ROOT", "workflow_depends_on", "M0773-X-PROVENANCE"), edge("FLOW-ROOT-READ", "M0773-ROOT", "workflow_depends_on", "M0773-X-READABLE"), edge("FLOW-ROOT-GATE", "M0773-ROOT", "workflow_depends_on", "M0773-X-WORKFLOW")],
}
graphs = {}
for name, edges in graph_edges.items():
    outgoing, incoming = {oid: [] for oid in ids}, {oid: [] for oid in ids}
    for e in edges:
        outgoing[e["from"]].append(e["edge_id"])
        incoming[e["to"]].append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0773-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0773-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "audit_complete": False, "theorem_complete": False, "provisionally_checked_interfaces": sorted(checked), "accepted_closed_obligations": [], "remaining_root_cut_set": ["M0773-L-POINTED", "M0773-X-SOURCE", "M0773-X-FOUNDATION", "M0773-X-PROVENANCE", "M0773-X-READABLE", "M0773-X-WORKFLOW"], "composition_certificates": ["Stage1Instances.THM_M_0773.ObligationTree.root_of_pointedPackage"]}
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0773/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
