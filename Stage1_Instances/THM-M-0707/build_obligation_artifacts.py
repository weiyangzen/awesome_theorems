#!/usr/bin/env python3
"""Build the frozen THM-M-0707 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0707-OBLIGATION_TREE"
THEOREM = "THM-M-0707"
PREFIX = "M0707-"

SPECS = [
    ("M0707-ROOT", "root", "The exact canonical arbitrary-code/arbitrary-input halting undecidability proposition.", "Stage1Instances.THM_M_0707.HaltingProblemUndecidable", "critical", "required", "required", "required", 12),
    ("M0707-S-STATEMENT", "definition", "Expand halting as definedness of Code.eval on Code x Nat and effective decidability as ComputablePred.", "Stage1Instances.THM_M_0707.HaltingProblemUndecidable", "critical", "required", "required", "required", 20),
    ("M0707-S-BOUNDARY", "branch", "Retain every code and input, including terminating zero code and a witnessed divergent rfind code.", "Stage1Instances.THM_M_0707.{zero_halts,rfind_succ_does_not_halt}", "high", "required", "required", "required", 20),
    ("M0707-N-FIXED-ZERO", "reduction", "Reduce an alleged uniform pair decider to the fixed input zero without weakening the root conclusion.", "Stage1Instances.THM_M_0707.fixedInputDecider_of_pairDecider", "critical", "required", "required", "required", 18),
    ("M0707-C-PAIR-ZERO", "construction", "Construct the computable embedding c maps to (c, 0).", "Stage1Instances.THM_M_0707.codePairZero_computable", "high", "required", "not_applicable", "required", 8),
    ("M0707-L-RESTRICT", "core_lemma", "Restrict both the DecidablePred witness and its computable Boolean characteristic along the pair-zero embedding.", "Stage1Instances.THM_M_0707.fixedInputDecider_of_pairDecider", "critical", "required", "required", "required", 18),
    ("M0707-X-HALTING", "terminal", "Use the pinned mathlib fixed-input halting undecidability theorem at input zero.", "ComputablePred.halting_problem 0", "critical", "required", "required", "required", 10),
    ("M0707-T-CONTRADICTION", "transport", "Apply the fixed-input impossibility to the restricted alleged pair decider.", "Stage1Instances.THM_M_0707.root_of_fixed_input_anchor", "critical", "required", "required", "required", 12),
    ("M0707-T-ASSEMBLE", "terminal", "Instantiate the checked composition with the pinned terminal anchor and return the exact canonical target.", "Stage1Instances.THM_M_0707.haltingProblemUndecidable_via_obligation_tree", "critical", "required", "required", "required", 8),
    ("M0707-X-SOURCE", "terminal", "Pinpoint a primary human proof and map its model and reduction to every material proof node.", "human source boundary; no Lean proposition", "high", "not_applicable", "required", "required", 60),
    ("M0707-X-FOUNDATION", "certificate", "Audit the observed Classical.choice, Quot.sound, and propext closure against an accepted foundation and TCB profile.", "transitive #print axioms and dependency closure", "critical", "informational", "not_applicable", "required", 40),
    ("M0707-X-PROVENANCE", "certificate", "Bind the local wrappers to the pinned mathlib terminal proof body, revision, source digest, and license.", "content-addressed terminal proof-body provenance", "critical", "informational", "not_applicable", "required", 35),
]


def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()


def planned(oid, target):
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()


statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
terminal_body = "mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95:Mathlib/Computability/Halting.lean#ComputablePred.halting_problem"
local_bodies = {
    "M0707-C-PAIR-ZERO": "local:Stage1_Instances/THM-M-0707/ObligationTree.lean#codePairZero_computable",
    "M0707-L-RESTRICT": "local:Stage1_Instances/THM-M-0707/ObligationTree.lean#fixedInputDecider_of_pairDecider",
    "M0707-T-CONTRADICTION": "local:Stage1_Instances/THM-M-0707/ObligationTree.lean#root_of_fixed_input_anchor",
    "M0707-T-ASSEMBLE": "local:Stage1_Instances/THM-M-0707/ObligationTree.lean#haltingProblemUndecidable_via_obligation_tree",
    "M0707-X-HALTING": terminal_body,
}

obligations = []
for oid, kind, human, target, risk, machine, source, readable, budget in SPECS:
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": ("lean-expression-sha256:" + expression_hash if oid in {"M0707-ROOT", "M0707-S-STATEMENT"} else planned(oid, target)),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": source,
        "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": ("human_source_boundary_only" if machine == "not_applicable" else "release_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": local_bodies.get(oid),
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row[0] for row in SPECS]

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The exact elaborated pair target and immutable anchor audit determine a fixed-input restriction architecture. Eligibility follows semantic root relevance, not available proof status; observed closure is recorded separately after the denominator.",
    "freeze_timing_boundary": "This workflow phase follows anchor audit, so it cannot claim that anchor availability was unobserved. The denominator is nevertheless independent of success metrics and includes all model, boundary, reduction, source, trust, and provenance obligations.",
    "frozen_against_statement_sha256": sha("Statement.lean"),
    "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
    "root_obligation_id": "M0707-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta; version 1 denominators remain reportable.",
    "obligations": obligations,
    "append_only_delta": [],
    "status_observed_after_freeze": {
        "provisional_machine_evidence": ["M0707-C-PAIR-ZERO", "M0707-L-RESTRICT", "M0707-X-HALTING", "M0707-T-CONTRADICTION", "M0707-T-ASSEMBLE", "M0707-ROOT"],
        "accepted_obligations": [],
        "root_machine_debt": "M0-W provisional pending master acceptance and release gates",
    },
    "status_boundary": "The registry and checked composition do not accept source fidelity, trust closure, readability, AUDIT-Z, THEOREM-Z, or theorem completion.",
}

machine_debt = {
    "M0707-ROOT": "M0-W", "M0707-S-STATEMENT": "M3", "M0707-S-BOUNDARY": "M0-L",
    "M0707-N-FIXED-ZERO": "M0-L", "M0707-C-PAIR-ZERO": "M0-L", "M0707-L-RESTRICT": "M0-L",
    "M0707-X-HALTING": "M0-W", "M0707-T-CONTRADICTION": "M0-L", "M0707-T-ASSEMBLE": "M0-L",
    "M0707-X-SOURCE": "M4", "M0707-X-FOUNDATION": "M3", "M0707-X-PROVENANCE": "M3",
}
nodes = []
for oid, kind, human, target, risk, machine, source, readable, budget in SPECS:
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX), "obligation_id": oid, "kind": kind,
        "human_statement": human, "formal_target": target, "output": human,
        "human_debt": "H1", "machine_debt": machine_debt[oid], "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "primary-source-pinpoint-pending" if source == "required" else "not-applicable",
        "provenance_id": "anchor-audit:S56-M-0707-C02" if oid in local_bodies else "pending",
        "foundation_profile": "lean4-mathlib/observed-Classical.choice+Quot.sound+propext; acceptance-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, timeout, or external computation receives proof credit",
        "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "The exact formal context and only the declared proof_requires children.",
            "inference": human,
            "output": human,
            "source_anchors": "anchor-audit:S56-M-0707-C02" if oid in local_bodies else "primary source map pending",
            "outgoing_use": "Only reciprocal composes edges carry proof credit; support graphs do not.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-0707/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Provisional node classification only; no master acceptance or theorem-release conclusion.",
        "task_ids": [ITEM, "S56-M-0707-PROOF"],
        "owned_sources": (["Stage1_Instances/THM-M-0707/ObligationTree.lean"] if oid in local_bodies else []),
        "owner": "THM-M-0707 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in local_bodies else None, "review_due": "before master acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "ObligationTree.lean", "toolchain"], "revocation_state": "provisional" if oid in local_bodies else "open"},
    })

proof_pairs = [
    ("M0707-ROOT", "M0707-T-ASSEMBLE"),
    ("M0707-T-ASSEMBLE", "M0707-T-CONTRADICTION"),
    ("M0707-T-ASSEMBLE", "M0707-S-STATEMENT"),
    ("M0707-T-CONTRADICTION", "M0707-X-HALTING"),
    ("M0707-T-CONTRADICTION", "M0707-N-FIXED-ZERO"),
    ("M0707-N-FIXED-ZERO", "M0707-L-RESTRICT"),
    ("M0707-L-RESTRICT", "M0707-C-PAIR-ZERO"),
]
proof_edges = []
for index, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{index:02d}-REQ", f"P{index:02d}-COMP"
    proof_edges.extend([
        {"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp},
        {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req},
    ])


def edges(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{i:02d}", "from": a, "type": typ, "to": b} for i, (a, b) in enumerate(pairs, 1)]


def graph(edge_rows):
    incoming, outgoing = {oid: [] for oid in ids}, {oid: [] for oid in ids}
    for edge in edge_rows:
        outgoing[edge["from"]].append(edge["edge_id"])
        incoming[edge["to"]].append(edge["edge_id"])
    return {"edges": edge_rows, "out": outgoing, "in": incoming}


graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(edges("R", "logical_decomposition", [("M0707-S-STATEMENT", "M0707-S-BOUNDARY"), ("M0707-N-FIXED-ZERO", "M0707-C-PAIR-ZERO")])),
    "provenance": graph(edges("V", "provenance_of", [("M0707-X-PROVENANCE", oid) for oid in local_bodies])),
    "evidence": graph(edges("E", "source_map", [("M0707-X-SOURCE", oid) for oid in ["M0707-ROOT", "M0707-N-FIXED-ZERO", "M0707-X-HALTING", "M0707-T-CONTRADICTION"]])),
    "trust": graph(edges("T", "trusts", [(oid, "M0707-X-FOUNDATION") for oid in ["M0707-ROOT", "M0707-X-HALTING", "M0707-T-ASSEMBLE"]])),
    "documentation": graph(edges("D", "documents", [("M0707-X-SOURCE", "M0707-ROOT"), ("M0707-X-PROVENANCE", "M0707-ROOT"), ("M0707-S-BOUNDARY", "M0707-S-STATEMENT")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M0707-ROOT", "M0707-X-SOURCE"), ("M0707-ROOT", "M0707-X-FOUNDATION"), ("M0707-ROOT", "M0707-X-PROVENANCE")])),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0707-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0707-ROOT", "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent.",
    "nodes": nodes, "graphs": graphs,
    "composition_certificates": [
        {"certificate_id": "COMP-M0707-RESTRICT", "declaration": "Stage1Instances.THM_M_0707.fixedInputDecider_of_pairDecider", "parent": "M0707-N-FIXED-ZERO", "consumes": ["M0707-L-RESTRICT", "M0707-C-PAIR-ZERO"], "state": "kernel_checked_provisional"},
        {"certificate_id": "COMP-M0707-ROOT", "declaration": "Stage1Instances.THM_M_0707.root_of_fixed_input_anchor", "parent": "M0707-ROOT", "consumes": ["M0707-X-HALTING", "M0707-N-FIXED-ZERO"], "state": "kernel_checked_provisional"},
    ],
    "closure_boundary": {
        "accepted_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "provisional_root_machine_classification": "M0-W",
        "remaining_root_cut_set": ["M0707-X-SOURCE", "M0707-X-FOUNDATION", "M0707-X-PROVENANCE"],
        "reason": "Kernel composition exists, but source, accepted trust/provenance, readability, independent validation, and master acceptance remain open.",
    },
}

recipes = {
    "schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "recipes": [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "argv": ["python3", "Stage1_Instances/THM-M-0707/check_obligation_tree.py"], "network_policy": "denied", "expected": "structural and narrow Lean composition checks pass; no release closure is implied"} for oid in ids],
}

for name, value in [("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)]:
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(f"generated {len(obligations)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
