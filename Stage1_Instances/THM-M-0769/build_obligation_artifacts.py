#!/usr/bin/env python3
"""Generate the frozen THM-M-0769 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0769-OBLIGATION_TREE"
THEOREM = "THM-M-0769"

# Freeze semantic units, not proof-discovery results. A short use of
# Classical.choice remains its own foundational bridge obligation.
ROWS = [
    ("M0769-ROOT", "root", "The exact indexed-family axiom-of-choice target.", "Stage1Instances.THM_M_0769.AxiomOfChoiceTarget", "required", "required", 20),
    ("M0769-S-INTERFACE", "definition", "Preserve the Sort-universe binders, pointwise nonemptiness hypothesis, and Nonempty dependent-function conclusion.", "Stage1Instances.THM_M_0769.AxiomOfChoiceTarget", "required", "not_applicable", 25),
    ("M0769-L-FIBER-CHOICE", "foundational_bridge", "Choose one inhabitant from each fiber under its Nonempty witness.", "Stage1Instances.THM_M_0769.ObligationTree.FiberSelector", "required", "required", 35),
    ("M0769-T-NONEMPTY", "composition", "Package the dependent selector as Nonempty (forall i, A i).", "Stage1Instances.THM_M_0769.ObligationTree.root_of_fiberSelector", "required", "required", 15),
    ("M0769-X-SOURCE", "source_boundary", "Map the indexed-family formulation and foundational status to an inspected primary passage and controlled translation.", "primary source node map pending", "not_applicable", "required", 60),
    ("M0769-X-FOUNDATION", "trust_boundary", "Expose Classical.choice as the terminal axiom and verify that no stronger hidden premise, unsafe code, or oracle enters closure.", "pinned Classical.choice provenance and axiom report", "required", "not_applicable", 30),
    ("M0769-X-PROVENANCE", "certificate", "Bind terminal proof bodies, source locators, immutable revisions, licenses, receipts, freshness, and revocation inputs.", "provenance ledger pending proof and validation phases", "informational", "not_applicable", 40),
    ("M0769-X-READABLE", "documentation", "Produce a unique anchored reconstruction of fiber selection and Nonempty packaging for independent review.", "readable reconstruction pending", "not_applicable", "not_applicable", 50),
    ("M0769-X-WORKFLOW", "workflow_gate", "Require node-scoped proof, validation, and release receipts before any root promotion.", "rev-5.6 proof -> validation -> release workflow", "informational", "not_applicable", 20),
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
        "statement_fingerprint": "lean-source-sha256:" + statement_sha if oid in {"M0769-ROOT", "M0769-S-INTERFACE"} else planned(oid, human),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": source,
        "readable_eligibility": "required",
        "risk_class": "critical" if oid in {"M0769-ROOT", "M0769-L-FIBER-CHOICE", "M0769-X-SOURCE", "M0769-X-FOUNDATION"} else "high",
        "step_budget": budget,
        "exclusion_reason": "human_source_boundary_only" if oid == "M0769-X-SOURCE" else ("release_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0769/ObligationTree.lean#root_of_fiberSelector" if oid == "M0769-T-NONEMPTY" else None,
    })
ids = [row[0] for row in ROWS]
denominator = sha(json.dumps(obligations, sort_keys=True, separators=(",", ":")).encode())
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated indexed-family target plus the pinned anchor audit; direct fiber selection and Nonempty packaging selected before proof closure observation.",
    "frozen_against_statement_sha256": statement_sha,
    "frozen_against_anchor_audit_sha256": anchor_sha,
    "root_obligation_id": "M0769-ROOT",
    "denominator_sha256": denominator,
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
    checked = oid in {"M0769-S-INTERFACE", "M0769-T-NONEMPTY"}
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix("M0769-"),
        "obligation_id": oid,
        "kind": kind,
        "human_statement": human,
        "formal_target": formal,
        "output": human,
        "human_debt": "H2",
        "machine_debt": "M0-L" if oid == "M0769-T-NONEMPTY" else ("M3" if oid in {"M0769-ROOT", "M0769-S-INTERFACE"} else "M4"),
        "readability_debt": "R4",
        "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md; primary-passage review pending",
        "provenance_id": "anchor-audit.json" if oid in {"M0769-L-FIBER-CHOICE", "M0769-X-FOUNDATION"} else "none",
        "foundation_profile": "Lean dependent type theory with disclosed Classical.choice for the open selector",
        "tcb_profile": "Lean 4.29.0 + mathlib 8a178386; transitive release audit pending",
        "computation_record": "none; noncomputable foundational choice; no oracle or external computation credited",
        "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "Only exact formal context and declared proof-requires children.",
            "inference": human,
            "output": human,
            "outgoing_use": "Only the declared typed parent or non-proof support edges may consume this output.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0769/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen interface" + (" and kernel-checked conditional composition" if checked else " only") + "; no root proof credit.",
        "task_ids": [ITEM, "S56-M-0769-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0769/ObligationTree.lean"] if checked else [],
        "owner": "THM-M-0769 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-12" if checked else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"],
            "revocation_state": "provisional" if checked else "open",
        },
    })

def graph(edges):
    outgoing = {x: [] for x in ids}
    incoming = {x: [] for x in ids}
    for edge in edges:
        outgoing[edge["from"]].append(edge["edge_id"])
        incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}

proof_pairs = [("M0769-ROOT", "M0769-S-INTERFACE"), ("M0769-ROOT", "M0769-T-NONEMPTY"), ("M0769-T-NONEMPTY", "M0769-L-FIBER-CHOICE")]
proof_edges = []
for i, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
    proof_edges.extend([
        {"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp},
        {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req},
    ])

def simple(prefix, edge_type, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "type": edge_type, "from": a, "to": b} for i, (a, b) in enumerate(pairs, 1)]

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(simple("R", "logical_decomposition", [("M0769-ROOT", "M0769-L-FIBER-CHOICE"), ("M0769-ROOT", "M0769-T-NONEMPTY")])),
    "provenance": graph(simple("V", "provenance_of", [("M0769-X-PROVENANCE", x) for x in ["M0769-L-FIBER-CHOICE", "M0769-T-NONEMPTY", "M0769-ROOT"]])),
    "evidence": graph(simple("E", "source_map", [("M0769-X-SOURCE", "M0769-ROOT"), ("M0769-X-SOURCE", "M0769-L-FIBER-CHOICE")])),
    "trust": graph(simple("T", "trusts", [(x, "M0769-X-FOUNDATION") for x in ["M0769-ROOT", "M0769-L-FIBER-CHOICE", "M0769-T-NONEMPTY"]])),
    "documentation": graph(simple("D", "documents", [("M0769-X-READABLE", x) for x in ["M0769-ROOT", "M0769-L-FIBER-CHOICE", "M0769-T-NONEMPTY"]])),
    "workflow": graph(simple("W", "workflow_depends_on", [("M0769-ROOT", x) for x in ["M0769-X-SOURCE", "M0769-X-FOUNDATION", "M0769-X-PROVENANCE", "M0769-X-READABLE", "M0769-X-WORKFLOW"]])),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": "THM-M-0769-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": "M0769-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "root_closed": False,
        "root_machine_classification": "M3",
        "theorem_complete": False,
        "first_open_cut": ["M0769-L-FIBER-CHOICE", "M0769-X-SOURCE", "M0769-X-FOUNDATION", "M0769-X-PROVENANCE", "M0769-X-READABLE", "M0769-X-WORKFLOW"],
    },
}
specs = {
    "schema_version": "stage1-validation-specs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "recipes": [{
        "recipe_id": "VAL-" + oid,
        "obligation_id": oid,
        "state": "provisional" if oid in {"M0769-S-INTERFACE", "M0769-T-NONEMPTY"} else "open",
        "required_checks": ["exact_type", "placeholder_scan", "provenance", "composition"],
    } for oid in ids],
}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
