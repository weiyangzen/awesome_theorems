#!/usr/bin/env python3
"""Build the frozen THM-M-1184 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1184-OBLIGATION_TREE"
TASKS = [ITEM, "S56-M-1184-PROOF"]

ROWS = [
    ("M1184-ROOT", "root", "critical", "The exact compact continuous Kantorovich-duality target.", "Stage1Instances.THM_M_1184.KantorovichDualityTarget", "required", "required"),
    ("M1184-S-DEFINITIONS", "definition", "high", "Freeze couplings, signed continuous potentials, and the two extended-order extrema.", "Stage1Instances.THM_M_1184.{Coupling,DualPair,PrimalValue,DualValue}", "not_applicable", "required"),
    ("M1184-S-FOUNDATION", "certificate", "critical", "Audit classical choice, integration, order-completeness, TCB, and the no-oracle boundary.", "planned exact axiom and transitive trust report", "not_applicable", "required"),
    ("M1184-C-PRODUCT", "construction", "high", "Construct the product probability coupling and prove both mapped marginals.", "planned Lean product-coupling constructor", "required", "required"),
    ("M1184-C-CONSTANT", "construction", "high", "Construct constant feasible signed potentials and prove both objective ranges are nonempty and bounded.", "planned Lean feasibility and bounded-range package", "required", "required"),
    ("M1184-W-INTEGRATE", "bridge", "critical", "Integrate the pointwise potential inequality against an arbitrary coupling and rewrite both marginals.", "planned Lean marginal-integration bridge", "required", "required"),
    ("M1184-W-ORDER", "lemma", "high", "Lift coupling-wise inequalities to dual-supremum below primal-infimum.", "planned Lean csSup/csInf order argument", "required", "required"),
    ("M1184-T-WEAK", "terminal", "critical", "Establish the uniform WeakDualityPackage interface.", "Stage1Instances.THM_M_1184.WeakDualityPackage", "required", "required"),
    ("M1184-S-SEPARATION", "bridge", "critical", "Separate the compact convex transport image from a strict lower-cost epigraph.", "planned finite-measure-space separation theorem", "required", "required"),
    ("M1184-C-POTENTIALS", "construction", "critical", "Extract continuous coordinate potentials from the separating functional with the pointwise cost constraint.", "planned separator-to-potentials construction", "required", "required"),
    ("M1184-L-GAP", "core_lemma", "critical", "For every value below the primal infimum, produce a feasible dual pair whose value exceeds it.", "planned no-duality-gap approximation lemma", "required", "required"),
    ("M1184-W-REVERSE", "lemma", "critical", "Convert the no-gap approximation statement into primal-infimum below dual-supremum.", "planned Lean order-limit argument", "required", "required"),
    ("M1184-T-STRONG", "terminal", "critical", "Establish the uniform ReverseDualityPackage interface.", "Stage1Instances.THM_M_1184.ReverseDualityPackage", "required", "required"),
    ("M1184-T-ASSEMBLE", "composition", "high", "Compose the two inequalities by antisymmetry into the exact root.", "Stage1Instances.THM_M_1184.root_of_duality_packages", "required", "required"),
    ("M1184-X-SOURCE", "source_boundary", "high", "Map every material strong-duality transition to a primary source with assumptions and errata.", "human source crosswalk pending", "required", "required"),
    ("M1184-X-PROVENANCE", "certificate", "critical", "Resolve terminal proof bodies, imports, axioms, licenses, and source boundaries.", "formal provenance and trust closure pending", "not_applicable", "required"),
]

def fingerprint(oid, statement):
    if oid == "M1184-ROOT":
        return "lean-expression-sha256:edb496494c51e51e63988c1b32c3fd639f1c911af60db1557a364968ff01cc29"
    return "planned:v1:sha256:" + hashlib.sha256(statement.encode()).hexdigest()

obligations = []
for oid, kind, risk, statement, formal, human, readable in ROWS:
    machine = "informational" if oid == "M1184-X-PROVENANCE" else ("not_applicable" if oid == "M1184-X-SOURCE" else "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(oid, statement),
        "kind": kind, "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": ({"M1184-X-SOURCE": "human_source_boundary_only", "M1184-X-PROVENANCE": "release_overlay_no_proof_credit"}.get(oid)),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1184/ObligationTree.lean#root_of_duality_packages" if oid == "M1184-T-ASSEMBLE" else None,
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row[0] for row in ROWS]

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": "THM-M-1184", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact compact/continuous signed-real statement and bounded anchor audit; weak-duality plus separation/no-gap architecture; eligibility fixed without consulting closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1184-ROOT", "denominator_sha256": digest,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M1184-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, or eligibility change requires a new registry version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1184-S-DEFINITIONS", "M1184-T-ASSEMBLE"], "root_machine_debt": "M2"},
    "status_boundary": "Architecture and denominators only; neither inequality package, source acceptance, nor theorem completion is supplied.",
}

nodes = []
for oid, kind, risk, statement, formal, human, readable in ROWS:
    closed = oid in {"M1184-S-DEFINITIONS", "M1184-T-ASSEMBLE"}
    nodes.append({
        "node_id": "THM-M-1184-" + oid.removeprefix("M1184-"), "obligation_id": oid,
        "kind": kind, "human_statement": statement, "formal_target": formal,
        "output": statement, "human_debt": "H3", "machine_debt": "M0-L" if closed else ("M2" if oid == "M1184-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if human == "not_applicable" else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid == "M1184-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if risk == "critical" else 60,
        "semantic_step_ledger": {"premises": "Only typed proof_requires children and the exact formal context.", "inference": statement, "output": statement, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1184/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen obligation or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": TASKS, "owned_sources": ["Stage1_Instances/THM-M-1184/ObligationTree.lean"] if oid == "M1184-T-ASSEMBLE" else [],
        "owner": "THM-M-1184 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if closed else "open"},
    })

proof_pairs = [
    ("M1184-ROOT", "M1184-T-ASSEMBLE"),
    ("M1184-T-ASSEMBLE", "M1184-T-WEAK"), ("M1184-T-ASSEMBLE", "M1184-T-STRONG"),
    ("M1184-T-WEAK", "M1184-W-ORDER"), ("M1184-W-ORDER", "M1184-W-INTEGRATE"),
    ("M1184-W-INTEGRATE", "M1184-C-PRODUCT"), ("M1184-W-INTEGRATE", "M1184-C-CONSTANT"),
    ("M1184-T-STRONG", "M1184-W-REVERSE"), ("M1184-W-REVERSE", "M1184-L-GAP"),
    ("M1184-L-GAP", "M1184-S-SEPARATION"), ("M1184-L-GAP", "M1184-C-POTENTIALS"),
    ("M1184-S-SEPARATION", "M1184-C-PRODUCT"), ("M1184-C-POTENTIALS", "M1184-C-CONSTANT"),
]

def graph(edges):
    return {"edges": edges, "out": {i: [e["edge_id"] for e in edges if e["from"] == i] for i in ids}, "in": {i: [e["edge_id"] for e in edges if e["to"] == i] for i in ids}}

proof_edges = []
for n, (parent, child) in enumerate(proof_pairs, 1):
    req, comp = f"P{n:02d}-REQ", f"P{n:02d}-COMP"
    proof_edges += [{"edge_id": req, "type": "proof_requires", "from": parent, "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "type": "composes", "from": child, "to": parent, "reciprocal_edge_id": req}]

def edges(prefix, typ, pairs):
    return [{"edge_id": f"{prefix}{n:02d}", "type": typ, "from": a, "to": b} for n, (a, b) in enumerate(pairs, 1)]

graphs = {
    "proof": graph(proof_edges),
    "refinement": graph(edges("R", "logical_decomposition", [("M1184-ROOT", "M1184-S-DEFINITIONS"), ("M1184-ROOT", "M1184-S-FOUNDATION")])),
    "provenance": graph(edges("V", "provenance_of", [("M1184-X-PROVENANCE", x) for x in ("M1184-T-WEAK", "M1184-T-STRONG", "M1184-T-ASSEMBLE")])),
    "evidence": graph(edges("E", "workflow_depends_on", [("M1184-ROOT", "M1184-X-PROVENANCE")])),
    "trust": graph(edges("T", "trusts", [(x, "M1184-S-FOUNDATION") for x in ("M1184-ROOT", "M1184-T-WEAK", "M1184-T-STRONG", "M1184-T-ASSEMBLE")])),
    "documentation": graph(edges("D", "documents", [("M1184-X-SOURCE", x) for x in ("M1184-ROOT", "M1184-S-SEPARATION", "M1184-L-GAP")])),
    "workflow": graph(edges("W", "workflow_depends_on", [("M1184-T-ASSEMBLE", "M1184-T-WEAK"), ("M1184-T-ASSEMBLE", "M1184-T-STRONG"), ("M1184-ROOT", "M1184-X-SOURCE"), ("M1184-ROOT", "M1184-X-PROVENANCE")])),
}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": "THM-M-1184",
    "registry_id": "THM-M-1184-OBLIGATIONS-v1", "registry_denominator_sha256": digest,
    "root_node_id": "M1184-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "minimal_open_root_cut_sets": [["M1184-T-WEAK"], ["M1184-T-STRONG"]],
    "closure_boundary": {"root_closed": False, "audit_complete": False, "theorem_complete": False, "root_vector": ["H3", "M2", "R4"], "reason": "Both exact inequality packages and all release overlays remain unaccepted."},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(digest)
