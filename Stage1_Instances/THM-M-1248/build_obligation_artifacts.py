#!/usr/bin/env python3
"""Build the frozen THM-M-1248 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1248-OBLIGATION_TREE"
THEOREM = "THM-M-1248"
PREFIX = "M1248"
ROOT_EXPRESSION = "f6a65804d336bcc7f72d03e35c0e43715fc92c648507b805117a09ec13648d5b"

# id, kind, human statement, formal target, output, risk, M eligibility,
# H eligibility, R eligibility, semantic-step ceiling
specs = [
    ("M1248-ROOT", "root", "Prove the exact frozen Caffarelli-Kohn-Nirenberg sufficiency target.", "Stage1Instances.THM_M_1248.CaffarelliKohnNirenbergTarget", "The canonical proposition.", "critical", "required", "required", "required", 20),
    ("M1248-S-DEFS", "definition", "Preserve the explicit real-power weighted quantities and Frechet-derivative norm.", "Stage1Instances.THM_M_1248.{weightedLp,weightedDerivativeLp}", "The two weighted quantities in the conclusion.", "critical", "required", "not_applicable", "required", 30),
    ("M1248-S-ADMISSIBLE", "definition", "Preserve every scaling, positivity, convexity, and conditional alpha-sigma restriction.", "Stage1Instances.THM_M_1248.AdmissibleParameters", "The exact admissible parameter region.", "critical", "required", "required", "required", 40),
    ("M1248-S-TEST", "definition", "Use all and only compactly supported smooth real functions on Euclidean n-space.", "ContDiff Real top u and HasCompactSupport u", "The exact test-function domain, including behavior near the origin.", "critical", "required", "required", "required", 35),
    ("M1248-S-FOUNDATION", "certificate", "Audit imports, axioms, classical principles, real integration, and Real.rpow trust boundaries.", "planned transitive axiom and TCB report", "An accepted foundation, computation, and TCB profile.", "critical", "required", "not_applicable", "required", 50),
    ("M1248-N-PARAM", "normalization", "Normalize the scaling identities and split a = 0, a = 1, and 0 < a < 1 without losing endpoint restrictions.", "planned exact parameter-normalization lemmas", "A dependency-complete disjoint parameter case split.", "critical", "required", "required", "required", 90),
    ("M1248-B-A0", "terminal", "Prove the a = 0 lower-order endpoint with the source-implied exponent and weight relations.", "planned Lean endpoint theorem for a = 0", "The exact estimate in the a = 0 case.", "high", "required", "required", "required", 80),
    ("M1248-B-A1", "core_lemma", "Prove the a = 1 weighted first-order Sobolev/Hardy endpoint throughout its admissible range.", "planned Lean weighted derivative endpoint theorem", "The exact estimate in the a = 1 case.", "critical", "required", "required", "required", 100),
    ("M1248-B-INTERIOR", "construction", "For 0 < a < 1, choose the source endpoint parameters and factor the weighted integrand for interpolation.", "planned Lean interior parameter construction", "Endpoint exponents and weights satisfying the interpolation identities.", "critical", "required", "required", "required", 100),
    ("M1248-L-WEIGHTED", "core_lemma", "Establish the weighted Sobolev/Hardy inequality used by both endpoint and interior branches.", "planned Lean weighted Sobolev-Hardy theorem on EuclideanSpace", "A finite positive constant and the required weighted derivative bound.", "critical", "required", "required", "required", 100),
    ("M1248-L-HOLDER", "bridge", "Apply Holder to the factored nonnegative weighted integrand with exactly the derived conjugate exponents.", "planned exact Holder bridge over volume", "The interpolated integral bound before taking real powers.", "critical", "required", "required", "required", 90),
    ("M1248-L-RPOW", "bridge", "Transport the integral inequality through Real.rpow and assemble constants without assuming r >= 1.", "planned Real.rpow monotonicity and arithmetic bridge", "The exact weightedLp inequality for the interior branch.", "critical", "required", "required", "required", 90),
    ("M1248-L-ORIGIN", "terminal", "Justify measurability, nonnegativity, and integrability at the singular origin and at infinity from admissibility and compact support.", "planned weighted-integrand analytic boundary lemmas", "All integrals and Holder factors satisfy their analytic side conditions.", "critical", "required", "required", "required", 100),
    ("M1248-T-ALL-PARAMS", "terminal", "Recombine the three parameter cases with one positive parameter-dependent constant per tuple.", "Stage1Instances.THM_M_1248.CKNAnalyticPackage (planned body)", "CKNAnalyticPackage.", "critical", "required", "required", "required", 50),
    ("M1248-T-ASSEMBLE", "transport", "Unfold the analytic package to the exact public root without changing binders, hypotheses, or constant scope.", "Stage1Instances.THM_M_1248.caffarelliKohnNirenbergTarget_of_analyticPackage", "The public target conditional on CKNAnalyticPackage.", "high", "required", "required", "required", 10),
    ("M1248-X-SOURCE", "terminal", "Map every parameter restriction and material proof transition to pinpoint pages in the primary paper and audit errata.", "human source boundary; no Lean proposition", "Reviewed source crosswalk for every material transition.", "critical", "not_applicable", "required", "required", 90),
    ("M1248-X-PROVENANCE", "certificate", "Classify every local or imported terminal proof body and its transitive origin.", "planned proof-body provenance closure", "Content-addressed provenance for every terminal body.", "critical", "informational", "not_applicable", "required", 60),
    ("M1248-X-TRUST", "certificate", "Record automation, executable, compiled-artifact, dependency, and computation trust boundaries.", "planned release trust record", "Replayable trust and computation boundary.", "critical", "informational", "not_applicable", "required", 60),
]


def fingerprint(oid, target):
    if oid == "M1248-ROOT":
        return "lean-expression-sha256:" + ROOT_EXPRESSION
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()


obligations = []
nodes = []
for oid, kind, statement, target, output, risk, machine, human, readable, budget in specs:
    closed = oid == "M1248-T-ASSEMBLE"
    body = "local:Stage1_Instances/THM-M-1248/ObligationTree.lean#caffarelliKohnNirenbergTarget_of_analyticPackage" if closed else None
    exclusion = None
    if machine == "informational":
        exclusion = "provenance_or_trust_overlay_no_proof_credit"
    elif machine == "not_applicable":
        exclusion = "human_source_boundary_only"
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint(oid, target),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": human,
        "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": exclusion,
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": f"THM-M-1248-{oid[len(PREFIX) + 1:]}",
        "obligation_id": oid,
        "kind": kind,
        "human_statement": statement,
        "formal_target": target,
        "output": output,
        "human_debt": "H1" if human == "required" else "not_applicable",
        "machine_debt": "M0-L" if closed else ("M3" if oid == "M1248-ROOT" else "M4"),
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "primary-paper-pinpoint-review-pending" if human == "required" else "not-applicable",
        "provenance_id": body or "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, numerical experiment, or certificate is credited",
        "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "Only the frozen formal context and incoming proof_requires children.",
            "inference": statement,
            "output": output,
            "outgoing_use": "Consumed only through a declared reciprocal composition edge or a typed non-proof support edge.",
        },
        "public_readable_target": f"Stage1_Instances/THM-M-1248/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Architecture or conditional interface only; no unlisted analytic premise and no exact CKN closure is supplied.",
        "task_ids": [ITEM, "S56-M-1248-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1248/ObligationTree.lean"] if closed else [],
        "owner": "THM-M-1248 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-12" if closed else None,
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["statement", "registry", "source map", "toolchain"],
            "revocation_state": "provisional" if closed else "open",
        },
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated sufficiency statement plus immutable anchor audit; endpoint/interpolation route selected before proof closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_expression_sha256": ROOT_EXPRESSION,
    "root_obligation_id": "M1248-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations,
    "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1248-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; the analytic package, pinpoint source review, provenance/trust audits, and exact root remain open.",
}

proof_pairs = [
    ("M1248-ROOT", "M1248-T-ALL-PARAMS"),
    ("M1248-ROOT", "M1248-T-ASSEMBLE"),
    ("M1248-T-ALL-PARAMS", "M1248-N-PARAM"),
    ("M1248-T-ALL-PARAMS", "M1248-B-A0"),
    ("M1248-T-ALL-PARAMS", "M1248-B-A1"),
    ("M1248-T-ALL-PARAMS", "M1248-B-INTERIOR"),
    ("M1248-N-PARAM", "M1248-S-ADMISSIBLE"),
    ("M1248-B-A0", "M1248-S-DEFS"),
    ("M1248-B-A0", "M1248-S-TEST"),
    ("M1248-B-A1", "M1248-L-WEIGHTED"),
    ("M1248-B-INTERIOR", "M1248-L-WEIGHTED"),
    ("M1248-B-INTERIOR", "M1248-L-HOLDER"),
    ("M1248-B-INTERIOR", "M1248-L-RPOW"),
    ("M1248-L-WEIGHTED", "M1248-L-ORIGIN"),
    ("M1248-L-HOLDER", "M1248-L-ORIGIN"),
]
proof_edges = []
for parent, child in proof_pairs:
    req, cmp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof_edges.extend([
        {"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": cmp},
        {"edge_id": cmp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req},
    ])

other = {
    "refinement": [
        ("REF-ROOT-DEFS", "M1248-ROOT", "logical_decomposition", "M1248-S-DEFS"),
        ("REF-ROOT-TEST", "M1248-ROOT", "logical_decomposition", "M1248-S-TEST"),
    ],
    "provenance": [
        ("SRC-PARAM", "M1248-S-ADMISSIBLE", "source_map", "M1248-X-SOURCE"),
        ("SRC-WEIGHTED", "M1248-L-WEIGHTED", "source_map", "M1248-X-SOURCE"),
        ("SRC-INTERIOR", "M1248-B-INTERIOR", "source_map", "M1248-X-SOURCE"),
        ("PROV-ROOT", "M1248-X-PROVENANCE", "provenance_of", "M1248-ROOT"),
    ],
    "evidence": [],
    "trust": [
        ("TRUST-FOUNDATION", "M1248-ROOT", "trusts", "M1248-S-FOUNDATION"),
        ("TRUST-RELEASE", "M1248-ROOT", "trusts", "M1248-X-TRUST"),
    ],
    "documentation": [
        ("DOC-SOURCE", "M1248-X-SOURCE", "documents", "M1248-ROOT"),
        ("DOC-ORIGIN", "M1248-L-ORIGIN", "documents", "M1248-S-TEST"),
    ],
    "workflow": [
        ("FLOW-PROOF", "M1248-T-ALL-PARAMS", "workflow_depends_on", "M1248-N-PARAM"),
        ("FLOW-PROV", "M1248-X-PROVENANCE", "workflow_depends_on", "M1248-T-ASSEMBLE"),
        ("FLOW-TRUST", "M1248-X-TRUST", "workflow_depends_on", "M1248-S-FOUNDATION"),
    ],
}


def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [
        {"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges
    ]
    incoming, outgoing = {}, {}
    for edge in cooked:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}


graphs = {"proof": graph(proof_edges), **{name: graph(edges) for name, edges in other.items()}}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": "THM-M-1248-OBLIGATIONS-v1",
    "registry_denominator_sha256": denominator,
    "root_node_id": "M1248-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes,
    "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": ["M1248-T-ASSEMBLE"],
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1248-T-ALL-PARAMS"],
        "composition_certificates": ["Stage1Instances.THM_M_1248.caffarelliKohnNirenbergTarget_of_analyticPackage"],
        "reason": "The exact final interface is checked, but the weighted analytic package remains open.",
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
