#!/usr/bin/env python3
"""Generate the frozen THM-M-0771 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0771-OBLIGATION_TREE"
THEOREM = "THM-M-0771"
PREFIX = "M0771"

# Semantic units are frozen independently of later proof results. In particular,
# the short upstream invocation remains a substantive construction obligation.
ROWS = [
    ("M0771-ROOT", "root", "Every type admits a strict well-order relation.", "Stage1Instances.THM_M_0771.WellOrderingTarget", "required", "required", 20),
    ("M0771-S-INTERFACE", "definition", "Preserve the universe-polymorphic carrier and the complete IsWellOrder relation witness.", "Stage1Instances.THM_M_0771.WellOrderingTarget", "required", "not_applicable", 25),
    ("M0771-L-WELLORDER-CONSTRUCTION", "foundational_bridge", "For an arbitrary carrier, construct a relation together with its IsWellOrder laws; a short use of the pinned mathlib anchor does not erase this obligation.", "Stage1Instances.THM_M_0771.ObligationTree.RelationWitness", "required", "required", 45),
    ("M0771-T-UNIVERSAL", "composition", "Generalize the pointwise relation witness over every carrier and discharge the exact target.", "Stage1Instances.THM_M_0771.ObligationTree.root_of_relationWitness", "required", "required", 15),
    ("M0771-X-SOURCE", "source_boundary", "Map the arbitrary-set claim and foundational assumptions to an inspected primary passage and controlled translation.", "primary source node map pending", "not_applicable", "required", 60),
    ("M0771-X-FOUNDATION", "trust_boundary", "Audit the choice, quotient, and extensionality dependencies of the cardinal embedding and pulled-back well-order construction.", "pinned transitive axiom report", "required", "not_applicable", 40),
    ("M0771-X-PROVENANCE", "certificate", "Bind terminal bodies, immutable mathlib revision, source locators, licenses, receipts, freshness, and revocation inputs.", "provenance ledger pending proof and validation phases", "informational", "not_applicable", 40),
    ("M0771-X-READABLE", "documentation", "Produce a uniquely anchored reconstruction of the cardinal embedding, pulled-back order, and universal packaging.", "readable reconstruction pending", "not_applicable", "not_applicable", 60),
    ("M0771-X-WORKFLOW", "workflow_gate", "Require node-scoped proof, validation, and release receipts before any root promotion.", "rev-5.6 proof -> validation -> release workflow", "informational", "not_applicable", 20),
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def planned(oid, statement):
    return "planned:v1:sha256:" + sha((oid + "\0" + statement).encode())

statement_sha = sha((HERE / "Statement.lean").read_bytes())
anchor_sha = sha((HERE / "anchor-audit.json").read_bytes())
obligations = []
for oid, kind, human, formal, machine, source, budget in ROWS:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-source-sha256:" + statement_sha if oid in {"M0771-ROOT", "M0771-S-INTERFACE"} else planned(oid, human),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": source,
        "readable_eligibility": "required",
        "risk_class": "critical" if oid in {"M0771-ROOT", "M0771-L-WELLORDER-CONSTRUCTION", "M0771-X-SOURCE", "M0771-X-FOUNDATION"} else "high",
        "step_budget": budget,
        "exclusion_reason": "human_source_boundary_only" if oid == "M0771-X-SOURCE" else ("release_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0771/ObligationTree.lean#root_of_relationWitness" if oid == "M0771-T-UNIVERSAL" else None,
    })
ids = [row[0] for row in ROWS]
denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated relation-level target plus pinned anchor audit; pointwise well-order construction and universal packaging selected before proof closure observation.",
    "frozen_against_statement_sha256": statement_sha, "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0771-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility change, or re-fingerprint requires a new registry version and append-only old/new ID delta.",
    "obligations": obligations,
}

nodes = []
for oid, kind, human, formal, machine, source, budget in ROWS:
    checked = oid in {"M0771-S-INTERFACE", "M0771-T-UNIVERSAL"}
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX + "-"), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": formal, "output": human,
        "human_debt": "H1", "machine_debt": "M0-L" if oid == "M0771-T-UNIVERSAL" else ("M3" if oid in {"M0771-ROOT", "M0771-S-INTERFACE"} else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md; exact primary passage review pending",
        "provenance_id": "anchor-audit.json" if oid in {"M0771-L-WELLORDER-CONSTRUCTION", "M0771-X-FOUNDATION"} else "none",
        "foundation_profile": "Lean dependent type theory; pinned anchor reports propext, Classical.choice, and Quot.sound",
        "tcb_profile": "Lean 4.29.0 + mathlib 8a178386; transitive release audit pending",
        "computation_record": "none; noncomputable well-order construction; no oracle or external computation credited",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only exact formal context and declared proof-requires children.", "inference": human, "output": human, "outgoing_use": "Only declared typed proof or support edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0771/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen interface" + (" and kernel-checked conditional composition" if checked else " only") + "; no root proof credit.",
        "task_ids": [ITEM, "S56-M-0771-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0771/ObligationTree.lean"] if checked else [],
        "owner": "THM-M-0771 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if checked else "open"},
    })

def graph(edges):
    outgoing, incoming = ({x: [] for x in ids}, {x: [] for x in ids})
    for edge in edges:
        outgoing[edge["from"]].append(edge["edge_id"]); incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_pairs = [("M0771-ROOT", "M0771-S-INTERFACE"), ("M0771-ROOT", "M0771-T-UNIVERSAL"), ("M0771-T-UNIVERSAL", "M0771-L-WELLORDER-CONSTRUCTION")]
proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges += [{"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req}]

def simple(prefix, edge_type, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": edge_type, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]

core = ["M0771-ROOT", "M0771-L-WELLORDER-CONSTRUCTION", "M0771-T-UNIVERSAL"]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(simple("R", "logical_decomposition", [("M0771-ROOT", "M0771-L-WELLORDER-CONSTRUCTION"), ("M0771-ROOT", "M0771-T-UNIVERSAL")])),
    "provenance": graph(simple("V", "provenance_of", [("M0771-X-PROVENANCE", x) for x in core])),
    "evidence": graph(simple("E", "source_map", [("M0771-X-SOURCE", x) for x in core])),
    "trust": graph(simple("T", "trusts", [(x, "M0771-X-FOUNDATION") for x in core])),
    "documentation": graph(simple("D", "documents", [("M0771-X-READABLE", x) for x in core])),
    "workflow": graph(simple("W", "workflow_depends_on", [("M0771-ROOT", x) for x in ["M0771-X-SOURCE", "M0771-X-FOUNDATION", "M0771-X-PROVENANCE", "M0771-X-READABLE", "M0771-X-WORKFLOW"]])),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0771-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0771-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "theorem_complete": False, "first_open_cut": ["M0771-L-WELLORDER-CONSTRUCTION", "M0771-X-SOURCE", "M0771-X-FOUNDATION", "M0771-X-PROVENANCE", "M0771-X-READABLE", "M0771-X-WORKFLOW"]},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "state": "provisional" if oid in {"M0771-S-INTERFACE", "M0771-T-UNIVERSAL"} else "open", "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"]} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
