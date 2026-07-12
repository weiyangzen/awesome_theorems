#!/usr/bin/env python3
"""Build the frozen THM-M-1244 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1244-OBLIGATION_TREE"
THEOREM = "THM-M-1244"

# id, kind, human statement, formal target, output, risk, machine, human, readable, budget
SPECS = [
    ("M1244-ROOT", "root", "Prove the exact frozen GaussianLogSobolevTarget.", "Stage1Instances.THM_M_1244.GaussianLogSobolevTarget", "The canonical proposition.", "critical", "required", "required", "required", 20),
    ("M1244-S-DEFS", "definition", "Fix product Gaussian measure, zero-safe entropy, Frechet derivative, and both energy densities.", "Stage1Instances.THM_M_1244.{standardGaussian,xlogx,entropySquare,coordinateEnergy}", "Definitions used by every proof child.", "high", "required", "not_applicable", "required", 30),
    ("M1244-S-DOMAIN", "definition", "Preserve all dimensions, C1 regularity, and the three explicit integrability assumptions.", "binders and hypotheses of GaussianLogSobolevTarget", "The exact quantified context.", "critical", "required", "required", "required", 20),
    ("M1244-S-BOUNDARY", "branch", "Cover n = 0, f = 0, constant functions, and zero mass without an unstated positivity premise.", "planned exact boundary lemmas", "All degenerate inputs remain covered.", "high", "required", "required", "required", 70),
    ("M1244-S-FOUNDATION", "certificate", "Audit classical principles, imports, axioms, and the pinned Lean/mathlib TCB.", "planned transitive axiom and trust report", "Accepted foundation and TCB profile.", "critical", "required", "not_applicable", "required", 40),
    ("M1244-N-MEASURE", "transport", "Identify the upstream product Gaussian with standardGaussian at the pinned encodings.", "planned checked equality or measure transport", "A directional measure bridge for all displayed integrals.", "critical", "required", "required", "required", 80),
    ("M1244-N-ENTROPY", "transport", "Relate upstream entropy to entropySquare including xlogx zero behavior and mass normalization.", "planned checked entropy identity", "The canonical entropy expression.", "critical", "required", "required", "required", 100),
    ("M1244-N-REGULARITY", "bridge", "Derive the upstream differentiability, coordinate-gradient continuity, and W12 premises from the frozen assumptions or identify needed lemmas.", "planned implication from canonical hypotheses to upstream hypotheses", "All upstream regularity premises.", "critical", "required", "required", "required", 100),
    ("M1244-B-ZEROMASS", "branch", "Separate zero and positive square mass when the entropy transport requires logarithmic normalization.", "planned zero-mass/positive-mass split and recomposition", "An exhaustive normalization branch.", "high", "required", "required", "required", 60),
    ("M1244-C-COORD", "construction", "Construct coordinate derivative values from fderiv using Pi.single basis directions.", "Stage1Instances.THM_M_1244.coordinateEnergy", "The finite coordinate-square energy density.", "high", "required", "required", "required", 40),
    ("M1244-L-UPSTREAM", "bridge", "Instantiate the immutable external tensorized Gaussian LSI after all checked transports.", "Stage1Instances.THM_M_1244.CoordinateLogSobolevPackage", "Entropy is bounded by twice coordinate energy.", "critical", "required", "required", "required", 100),
    ("M1244-L-POINTWISE", "core_lemma", "Bound the sum of squared coordinate evaluations by the squared operator norm for Lean's product norm.", "planned pointwise coordinateEnergy/operator-norm inequality", "Pointwise energy domination in the required direction.", "critical", "required", "required", "required", 80),
    ("M1244-L-INTEGRAL", "core_lemma", "Lift pointwise energy domination through Gaussian integration and multiplication by two.", "Stage1Instances.THM_M_1244.CoordinateToOperatorEnergyPackage", "The integrated energy bridge.", "critical", "required", "required", "required", 70),
    ("M1244-T-PACKAGES", "terminal", "Provide both complete analytic packages under exactly the canonical hypotheses.", "CoordinateLogSobolevPackage and CoordinateToOperatorEnergyPackage", "Both premises of the final composition theorem.", "critical", "required", "required", "required", 20),
    ("M1244-T-ASSEMBLE", "terminal", "Compose the coordinate inequality and energy bridge without changing the root.", "Stage1Instances.THM_M_1244.gaussianLogSobolevTarget_of_packages", "GaussianLogSobolevTarget conditional on both packages.", "high", "required", "required", "required", 10),
    ("M1244-X-SOURCE", "terminal", "Pinpoint the primary mathematical proof and map every material transition.", "human source boundary; no Lean proposition", "Reviewed source crosswalk.", "high", "not_applicable", "required", "required", 70),
    ("M1244-X-PROVENANCE", "certificate", "Track the external body, local wrappers, and terminal proof bodies without duplicate credit.", "planned proof-body provenance closure", "Content-addressed provenance graph.", "critical", "informational", "not_applicable", "required", 50),
    ("M1244-X-TRUST", "certificate", "Record toolchain, dependency, automation, computation, and external-project trust boundaries.", "planned release trust record", "Replayable trust boundary.", "critical", "informational", "not_applicable", "required", 50),
]

def planned_fingerprint(oid, target):
    if oid == "M1244-ROOT":
        return "lean-expression-sha256:eeff335a47ceaf9d469f25e1570640f17008c1f38d8173499a5429e7ab6397b3"
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

obligations = []
nodes = []
for oid, kind, statement, target, output, risk, machine, human, readable, budget in SPECS:
    body = "local:Stage1_Instances/THM-M-1244/ObligationTree.lean#gaussianLogSobolevTarget_of_packages" if oid == "M1244-T-ASSEMBLE" else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": planned_fingerprint(oid, target), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": ("provenance_or_trust_overlay_no_proof_credit" if machine == "informational" else "human_source_boundary_only" if machine == "not_applicable" else None),
        "terminal_proof_body_id": body,
    })
    closed = oid == "M1244-T-ASSEMBLE"
    nodes.append({
        "node_id": "THM-M-1244-" + oid[6:], "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if closed else "M4", "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "source-pinpoint-pending" if human == "required" else "not-applicable",
        "provenance_id": body or "none", "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, native computation, or experiment is credited", "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "The exact frozen context and incoming proof_requires conclusions only.",
            "inference": statement, "output": output,
            "outgoing_use": "Only the declared reciprocal composition edge or a typed non-proof support edge.",
        },
        "public_readable_target": f"Stage1_Instances/THM-M-1244/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture or conditional interface only; no open analytic premise is discharged.",
        "task_ids": [ITEM, "S56-M-1244-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-1244/ObligationTree.lean"] if closed else [],
        "owner": "THM-M-1244 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if closed else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in FIELDS} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable anchor audit; upstream coordinate-energy route plus an explicit directional energy bridge selected before closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor_audit.md").read_bytes()).hexdigest(),
    "root_obligation_id": "M1244-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1244-T-ASSEMBLE"], "root_machine_debt": "M4"},
    "status_boundary": "Scope and denominators only; both analytic packages, source review, trust audit, and exact root remain open.",
}

proof_pairs = [
    ("M1244-ROOT", "M1244-T-PACKAGES"), ("M1244-ROOT", "M1244-T-ASSEMBLE"),
    ("M1244-T-PACKAGES", "M1244-L-UPSTREAM"), ("M1244-T-PACKAGES", "M1244-L-INTEGRAL"),
    ("M1244-L-UPSTREAM", "M1244-N-MEASURE"), ("M1244-L-UPSTREAM", "M1244-N-ENTROPY"),
    ("M1244-L-UPSTREAM", "M1244-N-REGULARITY"), ("M1244-N-ENTROPY", "M1244-B-ZEROMASS"),
    ("M1244-N-REGULARITY", "M1244-S-DOMAIN"), ("M1244-L-INTEGRAL", "M1244-L-POINTWISE"),
    ("M1244-L-POINTWISE", "M1244-C-COORD"), ("M1244-C-COORD", "M1244-S-DEFS"),
    ("M1244-B-ZEROMASS", "M1244-S-BOUNDARY"),
]
proof_edges = []
for parent, child in proof_pairs:
    req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof_edges.extend([
        {"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp},
        {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req},
    ])

OTHER = {
    "refinement": [("REF-ROOT-DOMAIN", "M1244-ROOT", "logical_decomposition", "M1244-S-DOMAIN")],
    "provenance": [("SRC-UPSTREAM", "M1244-L-UPSTREAM", "source_map", "M1244-X-SOURCE"), ("PROV-ROOT", "M1244-X-PROVENANCE", "provenance_of", "M1244-ROOT")],
    "evidence": [],
    "trust": [("TRUST-FOUNDATION", "M1244-ROOT", "trusts", "M1244-S-FOUNDATION"), ("TRUST-RELEASE", "M1244-ROOT", "trusts", "M1244-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1244-X-SOURCE", "documents", "M1244-L-UPSTREAM"), ("DOC-BOUNDARY", "M1244-S-BOUNDARY", "documents", "M1244-ROOT")],
    "workflow": [("FLOW-PROOF", "M1244-T-PACKAGES", "workflow_depends_on", "M1244-L-UPSTREAM"), ("FLOW-ENERGY", "M1244-T-PACKAGES", "workflow_depends_on", "M1244-L-INTEGRAL"), ("FLOW-PROV", "M1244-X-PROVENANCE", "workflow_depends_on", "M1244-T-ASSEMBLE")],
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
    "registry_id": "THM-M-1244-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1244-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": ["M1244-T-ASSEMBLE"], "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M1244-L-UPSTREAM", "M1244-L-INTEGRAL"],
        "composition_certificates": ["Stage1Instances.THM_M_1244.gaussianLogSobolevTarget_of_packages"],
        "reason": "The conditional final composition is checked, but neither analytic package has a proof body.",
    },
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
