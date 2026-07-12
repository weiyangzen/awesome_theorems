#!/usr/bin/env python3
"""Build the frozen THM-M-1111 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1111-OBLIGATION_TREE"
THEOREM = "THM-M-1111"

# id, kind, human statement, formal target, output, risk, machine, human, readable, budget
SPECS = [
    ("M1111-ROOT", "root", "Prove the exact four-moment branch frozen in TaoVuFourMomentTarget for a source-faithful semantics.", "Stage1Instances.THM_M_1111.TaoVuFourMomentTarget S", "The canonical proposition.", "critical", "required", "required", "required", 20),
    ("M1111-S-DEFS", "definition", "Implement Wigner Hermitian ensembles, atom distributions, ordered eigenvalues, expectations, and real powers with the source normalization.", "planned Lean definitions implementing FourMomentSemantics", "A source-faithful semantic implementation.", "critical", "required", "required", "required", 100),
    ("M1111-S-DOMAIN", "definition", "Preserve the ordered quantifiers, uniform constants, matching orders, smoothness order, bulk indices, and sufficiently-large-n dependence.", "Stage1Instances.THM_M_1111.TaoVuFourMomentTarget S", "The exact quantified context and admissible inputs.", "critical", "required", "required", "required", 50),
    ("M1111-S-BOUNDARY", "branch", "Discharge k >= 1, Fin-index inhabitation, epsilon-bulk feasibility, and small-n cases below the selected threshold.", "planned boundary lemmas for TaoVuFourMomentTarget", "All degenerate cases are compatible with the comparison argument.", "high", "required", "required", "required", 80),
    ("M1111-S-FOUNDATION", "certificate", "Audit classical probability, spectral theory, imports, axioms, and the Lean/mathlib TCB.", "planned transitive axiom and trust report", "Accepted foundation and TCB profiles.", "critical", "required", "not_applicable", "required", 60),
    ("M1111-N-NORMALIZE", "normalization", "Normalize both ensembles and the ordered eigenvalue statistic to the source scaling and Condition C0 conventions.", "planned normalization theorem over the semantic implementation", "Two normalized ensembles satisfying the hypotheses used by replacement.", "critical", "required", "required", "required", 90),
    ("M1111-C-REPLACEMENT", "construction", "Construct the entry-by-entry Lindeberg replacement chain, preserving Hermitian symmetry and distinguishing diagonal entries.", "planned replacement-chain construction", "A finite chain from M to M' with one atom pair changed per step.", "critical", "required", "required", "required", 100),
    ("M1111-L-GOODCONFIG", "core_lemma", "Establish the high-probability good-configuration event with eigenvalue separation and eigenvector/resolvent control uniformly along the chain.", "planned good-configuration theorem", "Uniform control needed for Taylor expansion at every replacement.", "critical", "required", "required", "required", 100),
    ("M1111-L-RIGIDITY", "core_lemma", "Prove the bulk localization, level-repulsion/gap, and delocalization estimates used by the good-configuration theorem.", "planned random-matrix rigidity and gap package", "Quantitative exceptional-event bounds at source strength.", "critical", "required", "required", "required", 100),
    ("M1111-L-TAYLOR", "core_lemma", "Expand the smooth eigenvalue observable through the required order for a single matrix-entry perturbation.", "planned one-swap Taylor/resolvent expansion", "Main terms through order four and a controlled remainder.", "critical", "required", "required", "required", 100),
    ("M1111-L-MOMENT", "lemma", "Cancel the Taylor coefficients using off-diagonal matching through order four and diagonal matching through order two.", "planned moment-cancellation lemma", "Only source-permitted remainder terms remain for each swap.", "critical", "required", "required", "required", 70),
    ("M1111-L-REMAINDER", "core_lemma", "Bound Taylor remainders and bad-event contributions using Condition C0, derivative bounds through five, and good-configuration estimates.", "planned one-swap error theorem", "A summable quantitative error for one replacement.", "critical", "required", "required", "required", 100),
    ("M1111-B-OFFDIAGONAL", "branch", "Apply the order-four expansion and cancellation to every off-diagonal replacement.", "planned off-diagonal replacement theorem", "Total off-diagonal comparison error.", "critical", "required", "required", "required", 80),
    ("M1111-B-DIAGONAL", "branch", "Apply the source diagonal normalization and order-two matching argument to every diagonal replacement.", "planned diagonal replacement theorem", "Total diagonal comparison error.", "critical", "required", "required", "required", 80),
    ("M1111-T-TELESCOPE", "terminal", "Telescope all replacement errors and choose the uniform large-n threshold and positive exponent.", "planned telescoping comparison theorem", "The n^(-c0) expectation bound with the frozen dependencies.", "critical", "required", "required", "required", 100),
    ("M1111-T-ASSEMBLE", "transport", "Transport the completed comparison package to the exact public target without changing any binder or hypothesis.", "Stage1Instances.THM_M_1111.taoVuFourMomentTarget_of_comparisonPackage", "TaoVuFourMomentTarget S conditional on the comparison package.", "high", "required", "required", "required", 10),
    ("M1111-X-SOURCE", "terminal", "Map every material proof transition to Theorem 15 and its cited prerequisite estimates at immutable source pinpoints.", "human source boundary; no Lean proposition", "Reviewed primary-source crosswalk.", "high", "not_applicable", "required", "required", 100),
    ("M1111-X-PROVENANCE", "certificate", "Classify every local/imported terminal proof body and its transitive origin.", "planned provenance closure", "Content-addressed proof-body provenance.", "critical", "informational", "not_applicable", "required", 60),
    ("M1111-X-TRUST", "certificate", "Record automation, executable, compiled-artifact, dependency, and computation trust boundaries.", "planned release trust record", "Replayable trust and computation boundary.", "critical", "informational", "not_applicable", "required", 60),
]

def fingerprint(oid, target):
    if oid == "M1111-ROOT":
        return "lean-source-sha256:" + hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

obligations, nodes = [], []
for oid, kind, statement, target, output, risk, machine, human, readable, budget in SPECS:
    body = "local:Stage1_Instances/THM-M-1111/ObligationTree.lean#taoVuFourMomentTarget_of_comparisonPackage" if oid == "M1111-T-ASSEMBLE" else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(oid, target), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": human,
        "readable_eligibility": readable, "risk_class": risk,
        "exclusion_reason": "provenance_or_trust_overlay_no_proof_credit" if machine == "informational" else ("human_source_boundary_only" if machine == "not_applicable" else None),
        "terminal_proof_body_id": body,
    })
    closed = oid == "M1111-T-ASSEMBLE"
    nodes.append({
        "node_id": f"THM-M-1111-{oid[6:]}", "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if closed else ("M3" if oid == "M1111-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-pinpoint-pending" if human == "required" else "not-applicable",
        "provenance_id": body or "none", "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or numerical experiment is credited", "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the formal context and declared proof_requires children.", "inference": statement, "output": output, "outgoing_use": "Consumed only by declared reciprocal composition or non-proof support edges."},
        "public_readable_target": f"Stage1_Instances/THM-M-1111/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture only; no unlisted premise or analytic closure is supplied.",
        "task_ids": [ITEM, "S56-M-1111-PROOF"], "owned_sources": [], "owner": "THM-M-1111 proof lane",
        "reviewer": "independent Stage1 integration lane", "validity": {"validated_at": "2026-07-12" if closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if closed else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in FIELDS} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and bounded anchor audit; Tao-Vu replacement route frozen before observing closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1111-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1111-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "Denominators and architecture only. The abstract semantics currently carry no laws connecting their predicates and statistic, so the analytic root remains open and no theorem completion is claimed.",
}

PAIRS = [
    ("M1111-ROOT", "M1111-T-ASSEMBLE"), ("M1111-T-ASSEMBLE", "M1111-T-TELESCOPE"),
    ("M1111-T-TELESCOPE", "M1111-B-OFFDIAGONAL"), ("M1111-T-TELESCOPE", "M1111-B-DIAGONAL"),
    ("M1111-T-TELESCOPE", "M1111-S-DOMAIN"), ("M1111-T-TELESCOPE", "M1111-S-BOUNDARY"),
    ("M1111-B-OFFDIAGONAL", "M1111-C-REPLACEMENT"), ("M1111-B-OFFDIAGONAL", "M1111-L-TAYLOR"),
    ("M1111-B-OFFDIAGONAL", "M1111-L-MOMENT"), ("M1111-B-OFFDIAGONAL", "M1111-L-REMAINDER"),
    ("M1111-B-DIAGONAL", "M1111-C-REPLACEMENT"), ("M1111-B-DIAGONAL", "M1111-L-MOMENT"),
    ("M1111-B-DIAGONAL", "M1111-L-REMAINDER"), ("M1111-L-TAYLOR", "M1111-L-GOODCONFIG"),
    ("M1111-L-REMAINDER", "M1111-L-GOODCONFIG"), ("M1111-L-GOODCONFIG", "M1111-L-RIGIDITY"),
    ("M1111-C-REPLACEMENT", "M1111-N-NORMALIZE"), ("M1111-N-NORMALIZE", "M1111-S-DEFS"),
]
proof_edges = []
for parent, child in PAIRS:
    req, cmp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof_edges.extend([{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": cmp}, {"edge_id": cmp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}])

OTHER = {
    "refinement": [("REF-ROOT-DOMAIN", "M1111-ROOT", "logical_decomposition", "M1111-S-DOMAIN")],
    "provenance": [("SRC-REPLACEMENT", "M1111-C-REPLACEMENT", "source_map", "M1111-X-SOURCE"), ("SRC-RIGIDITY", "M1111-L-RIGIDITY", "source_map", "M1111-X-SOURCE"), ("PROV-ROOT", "M1111-X-PROVENANCE", "provenance_of", "M1111-ROOT")],
    "evidence": [],
    "trust": [("TRUST-FOUNDATION", "M1111-ROOT", "trusts", "M1111-S-FOUNDATION"), ("TRUST-RELEASE", "M1111-ROOT", "trusts", "M1111-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1111-X-SOURCE", "documents", "M1111-ROOT"), ("DOC-BOUNDARY", "M1111-S-BOUNDARY", "documents", "M1111-T-TELESCOPE")],
    "workflow": [("FLOW-PROOF", "M1111-T-TELESCOPE", "workflow_depends_on", "M1111-B-OFFDIAGONAL"), ("FLOW-PROV", "M1111-X-PROVENANCE", "workflow_depends_on", "M1111-T-ASSEMBLE")],
}

def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [{"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges]
    incoming, outgoing = {}, {}
    for edge in cooked:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}

graphs = {"proof": graph(proof_edges), **{name: graph(edges) for name, edges in OTHER.items()}}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1111-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1111-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": ["M1111-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1111-T-TELESCOPE"], "composition_certificates": ["Stage1Instances.THM_M_1111.taoVuFourMomentTarget_of_comparisonPackage"], "reason": "Only the conditional final transport is checked; the comparison package and its analytic semantics remain open."},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
