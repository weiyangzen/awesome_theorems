#!/usr/bin/env python3
"""Build the frozen THM-M-1027 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1027-OBLIGATION_TREE"
THEOREM = "THM-M-1027"

# Eligibility and architecture are declared here before the status overlay below.
SPECS = [
    ("M1027-ROOT", "root", "The exact abstract-space Wiener existence target.", "Stage1Instances.THM_M_1027.WienerExistenceTarget", "The canonical proposition.", "critical", "required", "required", "required", 20),
    ("M1027-S-DEFS", "definition", "Fix nonnegative time, real processes, ordered increment variance, and the five Wiener laws.", "Stage1Instances.THM_M_1027.{Time,RealProcess,IncrementVariance,IsWienerProcess}", "The exact objects and predicates used downstream.", "high", "required", "not_applicable", "required", 30),
    ("M1027-S-DOMAIN", "definition", "Preserve the existential carrier universe, measurable-space instance, probability measure, NNReal time, and Real values.", "Stage1Instances.THM_M_1027.WienerExistenceTarget", "The exact quantified context without a path-space substitution.", "critical", "required", "required", "required", 25),
    ("M1027-S-BOUNDARY", "terminal", "Cover time zero and equal-time increments, with zero variance and no negative-time obligation.", "Stage1Instances.THM_M_1027.incrementVariance_self", "Checked equal-time variance plus planned zero-start compatibility.", "high", "required", "required", "required", 35),
    ("M1027-S-TRANSPORT", "transport", "Relate the structured predicate to the direct frozen conjunction without adding Gaussian-process or adaptedness fields.", "Stage1Instances.THM_M_1027.wienerExistenceTarget_iff_pinnedIntakeSourceShape", "A checked bidirectional statement transport.", "high", "required", "required", "required", 20),
    ("M1027-S-FOUNDATION", "certificate", "Fix the classical-choice, quotient, axiom, import, and no-oracle policy for every terminal body.", "planned transitive axiom and TCB report", "An accepted foundation profile.", "critical", "required", "not_applicable", "required", 50),
    ("M1027-N-API", "normalization", "Normalize an immutable external IsBrownian construction to the frozen NNReal-indexed component interface.", "planned adapter from ProbabilityTheory.IsBrownian", "One carrier, measure, and process shared by every law child.", "critical", "required", "required", "required", 80),
    ("M1027-N-INCREMENT", "normalization", "Convert the external subtraction-law parameter convention to W t - W s with centered Gaussian variance t-s for s <= t.", "planned ordered-increment HasLaw adapter", "The exact frozen incrementLaw field.", "critical", "required", "required", "required", 80),
    ("M1027-C-CONSTRUCTION", "construction", "Integrate the pinned Brownian construction and its Kolmogorov-extension dependency at immutable revisions.", "ProbabilityTheory.brownian / ProbabilityTheory.wienerMeasure (external, not installed)", "A concrete process and probability measure.", "critical", "required", "required", "required", 100),
    ("M1027-L-PROBABILITY", "bridge", "Prove that the construction measure is a probability measure.", "planned IsProbabilityMeasure wienerMeasure", "The probability field of the witness package.", "high", "required", "required", "required", 45),
    ("M1027-L-MEASURABLE", "bridge", "Derive coordinate measurability for every nonnegative time.", "planned adapter using ProbabilityTheory.measurable_brownian", "The measurable field of IsWienerProcess.", "high", "required", "required", "required", 45),
    ("M1027-L-ZERO", "lemma", "Derive W 0 = 0 almost surely for the chosen construction.", "planned zero-start theorem for brownian", "The startsAtZero field.", "high", "required", "required", "required", 50),
    ("M1027-L-INDEPENDENCE", "bridge", "Transport the external independent-increments theorem to mathlib HasIndepIncrements on the frozen process.", "planned adapter using ProbabilityTheory.hasIndepIncrements_brownian", "The independentIncrements field.", "critical", "required", "required", "required", 70),
    ("M1027-L-CONTINUITY", "bridge", "Convert everywhere continuity of the constructed path to almost-sure continuity under its measure.", "planned adapter using ProbabilityTheory.continuous_brownian", "The continuousPaths field.", "critical", "required", "required", "required", 50),
    ("M1027-T-PACKAGE", "terminal", "Assemble one coherent carrier, measure, process, and all five laws into WienerWitnessPackage.", "Stage1Instances.THM_M_1027.WienerWitnessPackage (planned inhabitant)", "A fully assembled exact witness package.", "critical", "required", "required", "required", 40),
    ("M1027-T-ASSEMBLE", "transport", "Eliminate the assembled witness package into the exact frozen existential root.", "Stage1Instances.THM_M_1027.wienerExistenceTarget_of_witnessPackage", "WienerExistenceTarget conditional on WienerWitnessPackage.", "high", "required", "required", "required", 10),
    ("M1027-X-EXTERNAL", "bridge", "Audit and pin the external Brownian terminal declarations, additional dependency, license, and source blobs.", "brownian-motion@fdcef67f41b51b7635b3c2d08eb61768604f8f74", "An importable, provenance-closed external boundary.", "critical", "required", "not_applicable", "required", 80),
    ("M1027-X-SOURCE", "terminal", "Pinpoint a primary construction proof and map every assumption and transition to the frozen nodes.", "human source boundary; no Lean proposition", "A reviewed premise-level human-source crosswalk.", "high", "not_applicable", "required", "required", 80),
    ("M1027-X-PROVENANCE", "certificate", "Resolve wrapper, terminal declaration, proof-body, dependency, and source origin for every credited formal node.", "planned formal provenance closure", "Content-addressed terminal-body provenance.", "critical", "informational", "not_applicable", "required", 60),
    ("M1027-X-TRUST", "certificate", "Record Lean, mathlib, external dependencies, compiled artifacts, automation, and computation trust boundaries.", "planned release trust record", "Replayable TCB and no-oracle evidence.", "critical", "informational", "not_applicable", "required", 60),
]

ROOT_FP = "lean-expression-sha256:be0e748b7e1efd3bbe66636dedd6f5fcde9a5c73afb22b3b5ae7d50a2625cf5e"

def fp(oid, target):
    return ROOT_FP if oid == "M1027-ROOT" else "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()

obligations, nodes = [], []
closed = {"M1027-S-DEFS", "M1027-S-DOMAIN", "M1027-S-BOUNDARY", "M1027-S-TRANSPORT", "M1027-T-ASSEMBLE"}
for oid, kind, statement, target, output, risk, machine, human, readable, budget in SPECS:
    body = None
    if oid == "M1027-T-ASSEMBLE":
        body = "local:Stage1_Instances/THM-M-1027/ObligationTree.lean#wienerExistenceTarget_of_witnessPackage"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp(oid, target), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": readable,
        "risk_class": risk,
        "exclusion_reason": "human_source_boundary_only" if machine == "not_applicable" else ("provenance_or_trust_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": body,
    })
    is_closed = oid in closed
    nodes.append({
        "node_id": "THM-M-1027-" + oid[6:], "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if is_closed else ("M3" if oid == "M1027-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-pinpoint-pending" if human == "required" else "not-applicable",
        "provenance_id": body or "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386+external-closure-pending",
        "computation_record": "none; no oracle, randomness, or experiment is credited",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Only the stated formal context and incoming proof_requires children.", "inference": statement, "output": output, "outgoing_use": "Consumed only through the declared reciprocal composition edge or a non-proof support edge."},
        "public_readable_target": f"Stage1_Instances/THM-M-1027/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Architecture or conditional interface only; no unlisted premise and no Wiener construction is supplied.",
        "task_ids": [ITEM, "S56-M-1027-PROOF"], "owned_sources": [],
        "owner": "THM-M-1027 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if is_closed else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "external pin", "source map", "toolchain"], "revocation_state": "provisional" if is_closed else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in FIELDS} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated abstract-space statement and immutable anchor audit; external Brownian construction adapter route selected independently of closure status.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1027-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(closed), "root_machine_debt": "M3"},
    "status_boundary": "The architecture is frozen; external integration, witness construction, source review, trust closure, and the exact root remain open.",
}

proof_pairs = [
    ("M1027-ROOT", "M1027-T-PACKAGE"), ("M1027-ROOT", "M1027-T-ASSEMBLE"),
    ("M1027-T-PACKAGE", "M1027-C-CONSTRUCTION"), ("M1027-T-PACKAGE", "M1027-L-PROBABILITY"),
    ("M1027-T-PACKAGE", "M1027-L-MEASURABLE"), ("M1027-T-PACKAGE", "M1027-L-ZERO"),
    ("M1027-T-PACKAGE", "M1027-N-INCREMENT"), ("M1027-T-PACKAGE", "M1027-L-INDEPENDENCE"),
    ("M1027-T-PACKAGE", "M1027-L-CONTINUITY"), ("M1027-C-CONSTRUCTION", "M1027-X-EXTERNAL"),
    ("M1027-C-CONSTRUCTION", "M1027-N-API"), ("M1027-N-API", "M1027-S-DEFS"),
    ("M1027-N-API", "M1027-S-DOMAIN"), ("M1027-N-INCREMENT", "M1027-N-API"),
    ("M1027-N-INCREMENT", "M1027-S-BOUNDARY"),
]
proof_edges = []
for parent, child in proof_pairs:
    req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof_edges.extend([{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": comp}, {"edge_id": comp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}])

other = {
    "refinement": [("REF-ROOT-TRANSPORT", "M1027-ROOT", "logical_decomposition", "M1027-S-TRANSPORT")],
    "provenance": [("SRC-CONSTRUCTION", "M1027-C-CONSTRUCTION", "source_map", "M1027-X-SOURCE"), ("PROV-EXTERNAL", "M1027-X-PROVENANCE", "provenance_of", "M1027-X-EXTERNAL"), ("PROV-ASSEMBLE", "M1027-X-PROVENANCE", "provenance_of", "M1027-T-ASSEMBLE")],
    "evidence": [],
    "trust": [("TRUST-FOUNDATION", "M1027-ROOT", "trusts", "M1027-S-FOUNDATION"), ("TRUST-RELEASE", "M1027-ROOT", "trusts", "M1027-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1027-X-SOURCE", "documents", "M1027-C-CONSTRUCTION"), ("DOC-BOUNDARY", "M1027-S-BOUNDARY", "documents", "M1027-N-INCREMENT")],
    "workflow": [("FLOW-PACKAGE", "M1027-T-PACKAGE", "workflow_depends_on", "M1027-X-EXTERNAL"), ("FLOW-PROVENANCE", "M1027-X-PROVENANCE", "workflow_depends_on", "M1027-T-ASSEMBLE")],
}

def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [{"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges]
    incoming, outgoing = {}, {}
    for edge in cooked:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}

graphs = {"proof": graph(proof_edges), **{name: graph(edges) for name, edges in other.items()}}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1027-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1027-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(closed), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1027-T-PACKAGE"], "composition_certificates": ["Stage1Instances.THM_M_1027.wienerExistenceTarget_of_witnessPackage"], "reason": "The witness-to-root interface is checked, but no witness package or external dependency is integrated."},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
