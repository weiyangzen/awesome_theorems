#!/usr/bin/env python3
"""Build the frozen THM-M-1088 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1088-OBLIGATION_TREE"
THEOREM = "THM-M-1088"

# This inventory is architectural, not status-driven. The central analytic packages remain open.
SPECS = [
    ("M1088-ROOT", "root", "Prove the exact canonical countable-index Borell--TIS target.", "Stage1Instances.THM_M_1088.BorellTISTarget", "critical", "required", "required", 20),
    ("M1088-S-CONTEXT", "definition", "Preserve the ordered universes, measurable space, countable nonempty index, process, supremum representative, and variance proxy.", "Stage1Instances.THM_M_1088.BorellTISTarget binder context", "high", "required", "required", 35),
    ("M1088-S-SUPREMUM", "definition", "Use the supplied pointwise real supremum representative together with boundedness, measurability, and integrability conventions.", "Stage1Instances.THM_M_1088.IsSupremum X S and Integrable S P", "critical", "required", "required", 55),
    ("M1088-S-BOUNDARY", "branch", "Retain u = 0 and the strict event, while treating sigma2 > 0 as the frozen exclusion of the degenerate variance case.", "0 < σ2 and forall u, 0 <= u -> UpperTailBound P S σ2", "high", "required", "required", 45),
    ("M1088-S-FOUNDATION", "certificate", "Audit classical measure theory, imports, axioms, and the noncomputable integration boundary.", "planned transitive Lean foundation and axiom report", "critical", "required", "not_applicable", 40),
    ("M1088-N-ENUMERATION", "normalization", "Choose a countable exhaustion of T by nonempty finite index sets without changing the canonical supremum.", "planned exact Lean finite exhaustion and supremum convergence signature", "critical", "required", "required", 90),
    ("M1088-C-FINITE-MAX", "construction", "Construct measurable finite maxima S_n and their finite variance suprema, proving monotonicity and pointwise convergence to S.", "planned exact Lean finite-maximum construction and invariants", "critical", "required", "required", 100),
    ("M1088-L-FINITE-CONCENTRATION", "core_lemma", "Establish sharp one-sided Gaussian concentration for each finite maximum with its covariance-derived variance proxy.", "planned finite-dimensional Gaussian Lipschitz concentration theorem", "critical", "required", "required", 100),
    ("M1088-L-COVARIANCE", "core_lemma", "Represent each finite Gaussian vector with covariance control and show the maximum Lipschitz constant is bounded by the finite variance supremum.", "planned covariance factorization and Lipschitz normalization package", "critical", "required", "required", 100),
    ("M1088-B-POSITIVE-TAIL", "branch", "Transport the finite concentration inequality for u > 0 to the target's strict probability event.", "planned checked event and ENNReal probability transport for 0 < u", "high", "required", "required", 70),
    ("M1088-B-ZERO-TAIL", "branch", "Discharge u = 0 directly from probability normalization and positivity of the exponential bound.", "planned exact Lean u = 0 boundary proof", "high", "required", "required", 45),
    ("M1088-B-MERGE", "transport", "Merge the positive-tail and zero-tail branches into the quantified u >= 0 conclusion.", "planned checked branch exhaustiveness and recomposition", "high", "required", "required", 35),
    ("M1088-L-MEAN-LIMIT", "core_lemma", "Show integrals of the increasing finite maxima converge to the integral of S under the frozen integrability assumptions.", "planned exact Lean expectation convergence theorem", "critical", "required", "required", 100),
    ("M1088-L-PROBABILITY-LIMIT", "core_lemma", "Pass finite strict-event bounds to the countable supremum event without losing the sharp constant.", "planned exact Lean event-limit and measure-continuity theorem", "critical", "required", "required", 100),
    ("M1088-T-ENGINE", "bridge", "Compose finite approximation, concentration, mean convergence, event convergence, and boundary branches into the exact upper-tail engine.", "Stage1Instances.THM_M_1088.ObligationTree.UpperTailEngine", "critical", "required", "required", 100),
    ("M1088-T-ASSEMBLE", "terminal", "Consume the exact upper-tail engine and all canonical hypotheses to yield BorellTISTarget.", "Stage1Instances.THM_M_1088.ObligationTree.target_of_upperTailEngine", "critical", "required", "required", 25),
    ("M1088-X-SOURCE", "terminal", "Pinpoint the primary Borell--TIS proof and map every material transition and convention to the obligation inventory.", "human source boundary; no Lean proof proposition", "high", "not_applicable", "required", 80),
    ("M1088-X-PROVENANCE", "certificate", "Classify terminal proof bodies, wrappers, imports, and transitive declaration origins without duplicate credit.", "planned content-addressed provenance closure", "critical", "informational", "not_applicable", 50),
    ("M1088-X-TRUST", "certificate", "Record kernel, toolchain, automation, computation, compiled artifacts, and replay trust boundaries.", "planned release trust record", "critical", "informational", "not_applicable", 50),
]


def file_sha(name):
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def fingerprint(oid, target):
    if oid == "M1088-ROOT":
        return "lean-source-bound-sha256:" + hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()


obligations = []
nodes = []
for oid, kind, statement, target, risk, machine, human, budget in SPECS:
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(oid, target), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": "governance_overlay_no_proof_credit" if machine == "informational" else "human_source_boundary_only" if machine == "not_applicable" else None,
        "terminal_proof_body_id": "local:ObligationTree.lean#target_of_upperTailEngine" if oid == "M1088-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-1088-" + oid[6:], "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": statement,
        "human_debt": "H2", "machine_debt": "M3" if oid in {"M1088-ROOT", "M1088-T-ASSEMBLE"} else "M4",
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-pinpoint-pending" if human == "required" else "not-applicable",
        "provenance_id": "local-composition-body-provisional" if oid == "M1088-T-ASSEMBLE" else "pending",
        "foundation_profile": "lean4-mathlib-classical/audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386ffc0/transitive-closure-pending",
        "computation_record": "none credited", "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "Canonical hypotheses plus declared proof_requires children only.",
            "inference": statement, "output": statement,
            "outgoing_use": "Only through reciprocal composes edges; support graphs carry no proof credit.",
        },
        "public_readable_target": "Stage1_Instances/THM-M-1088/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional interface only; no Borell--TIS proof closure is credited.",
        "task_ids": [ITEM, "S56-M-1088-PROOF"], "owned_sources": ["ObligationTree.lean"] if oid == "M1088-T-ASSEMBLE" else [],
        "owner": "THM-M-1088 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.md", "registry", "toolchain"], "revocation_state": "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in FIELDS} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated countable-index target and bounded immutable anchor audit; finite-exhaustion Gaussian concentration route selected before proof closure was observed.",
    "frozen_against_statement_sha256": file_sha("Statement.lean"),
    "frozen_against_anchor_audit_sha256": file_sha("anchor-audit.md"),
    "root_obligation_id": "M1088-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "eligibility_policy": "Every semantic package on the selected finite-exhaustion route is required regardless of current library availability; source, trust, and provenance overlays cannot earn proof credit.",
    "delta_policy": "Any target correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.",
    "exclusions": ["The zero-variance extension is outside the frozen target because Statement.lean requires 0 < sigma2.", "Two-sided concentration, uncountable separability transports, and lower-tail bounds are outside the frozen target.", "Aliases, wrappers, and transports cannot duplicate semantic or proof-body credit."],
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"provisionally_checked_interfaces": ["M1088-T-ASSEMBLE"], "closed_obligations": [], "root_machine_debt": "M3"},
    "status_boundary": "Architecture only; the central concentration, approximation, limit, source, provenance, readability, and release obligations remain open.",
}

PAIRS = [
    ("M1088-ROOT", "M1088-T-ASSEMBLE"), ("M1088-T-ASSEMBLE", "M1088-T-ENGINE"),
    ("M1088-T-ENGINE", "M1088-S-CONTEXT"), ("M1088-T-ENGINE", "M1088-S-SUPREMUM"),
    ("M1088-T-ENGINE", "M1088-N-ENUMERATION"), ("M1088-T-ENGINE", "M1088-L-MEAN-LIMIT"),
    ("M1088-T-ENGINE", "M1088-L-PROBABILITY-LIMIT"), ("M1088-T-ENGINE", "M1088-B-MERGE"),
    ("M1088-N-ENUMERATION", "M1088-C-FINITE-MAX"), ("M1088-C-FINITE-MAX", "M1088-L-FINITE-CONCENTRATION"),
    ("M1088-L-FINITE-CONCENTRATION", "M1088-L-COVARIANCE"), ("M1088-B-MERGE", "M1088-B-POSITIVE-TAIL"),
    ("M1088-B-MERGE", "M1088-B-ZERO-TAIL"), ("M1088-B-MERGE", "M1088-S-BOUNDARY"),
    ("M1088-L-MEAN-LIMIT", "M1088-C-FINITE-MAX"), ("M1088-L-PROBABILITY-LIMIT", "M1088-L-FINITE-CONCENTRATION"),
]
proof = []
for parent, child in PAIRS:
    req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
    proof.extend([{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}])

OTHER = {
    "refinement": [("REF-ROOT-CONTEXT", "M1088-ROOT", "logical_decomposition", "M1088-S-CONTEXT"), ("REF-ROOT-BOUNDARY", "M1088-ROOT", "logical_decomposition", "M1088-S-BOUNDARY")],
    "provenance": [("SRC-FINITE", "M1088-L-FINITE-CONCENTRATION", "source_map", "M1088-X-SOURCE"), ("SRC-LIMIT", "M1088-L-PROBABILITY-LIMIT", "source_map", "M1088-X-SOURCE"), ("PROV-ASSEMBLE", "M1088-X-PROVENANCE", "provenance_of", "M1088-T-ASSEMBLE")],
    "evidence": [],
    "trust": [("TRUST-FOUNDATION", "M1088-ROOT", "trusts", "M1088-S-FOUNDATION"), ("TRUST-RELEASE", "M1088-ROOT", "trusts", "M1088-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1088-X-SOURCE", "documents", "M1088-ROOT"), ("DOC-BOUNDARY", "M1088-S-BOUNDARY", "documents", "M1088-B-MERGE")],
    "workflow": [("FLOW-PROOF", "M1088-T-ASSEMBLE", "workflow_depends_on", "M1088-T-ENGINE"), ("FLOW-PROV", "M1088-X-PROVENANCE", "workflow_depends_on", "M1088-T-ASSEMBLE")],
}


def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [{"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges]
    incoming, outgoing = {}, {}
    for edge in cooked:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}


graphs = {"proof": graph(proof), **{name: graph(edges) for name, edges in OTHER.items()}}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1088-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "statement_source_sha256": file_sha("Statement.lean"), "anchor_audit_sha256": file_sha("anchor-audit.md"),
    "root_node_id": "M1088-ROOT", "edge_direction": "proof_requires runs parent to child; reciprocal composes runs child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1088-T-ENGINE"], "composition_certificates": ["ObligationTree.target_of_upperTailEngine (conditional interface only)"], "reason": "The exact upper-tail engine and all substantive analytic children remain unproved."},
}
recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1088/check_obligation_tree.py"], "env": {}, "timeout_seconds": 60, "network_policy": "denied", "covered_ids": [oid], "expected": "structural registry and typed-graph validation passes; this does not close the obligation"} for oid, *_ in SPECS]}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
(HERE / "validation-specs.json").write_text(json.dumps(recipes, indent=2) + "\n")
print(f"generated {len(obligations)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
