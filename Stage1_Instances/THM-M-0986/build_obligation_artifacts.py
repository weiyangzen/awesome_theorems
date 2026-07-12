#!/usr/bin/env python3
"""Generate the frozen THM-M-0986 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEOREM = "THM-M-0986"
ITEM = "S56-M-0986-OBLIGATION_TREE"
PREFIX = "M0986"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen real-valued Khinchin weak-law target.", "Stage1Instances.THM_M_0986.KhinchinWeakLawTarget", "Convergence in probability of empirical averages to the common expectation."),
    ("S-DEFINITIONS", "definition", "high", "Freeze empirical averages, iid hypotheses, expectation, and convergence-in-probability encoding.", "Stage1Instances.THM_M_0986.{empiricalAverage,KhinchinWeakLawTarget}", "The exact elaborated vocabulary and binder context."),
    ("S-BOUNDARY", "terminal", "normal", "Fix the empty average at zero and preserve all three root hypotheses.", "Stage1Instances.THM_M_0986.{empiricalAverage_zero,target_iff_expandedIntakeShape}", "Checked boundary and expanded target shape."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, quotient, measure integration, imports, and the no-oracle boundary.", "planned transitive axiom and trust certificate", "Accepted foundation and TCB profile."),
    ("N-MEASURABILITY", "reduction", "high", "Transfer integrability and identical distribution to strong measurability of every observation.", "planned IdentDistrib/Integrable measurability bridge", "AEStronglyMeasurable (X i) mu for every i."),
    ("C-AVERAGE-MEASURABLE", "construction", "high", "Prove every finite empirical average is strongly measurable.", "Stage1Instances.THM_M_0986.AverageMeasurabilityPackage", "Strong measurability of every function in the average sequence."),
    ("L-STRONG-LAW", "bridge", "critical", "Obtain almost-everywhere convergence of empirical averages under the exact iid integrability hypotheses.", "Stage1Instances.THM_M_0986.StrongLawPackage", "Almost-everywhere convergence to the common expectation."),
    ("T-AE-IN-MEASURE", "transport", "critical", "Transport almost-everywhere convergence of measurable averages to convergence in measure.", "MeasureTheory.tendstoInMeasure_of_tendsto_ae", "The convergence-in-probability conclusion."),
    ("T-ASSEMBLE", "transport", "high", "Compose measurability, the strong-law package, and the AE-to-in-measure bridge into the exact root.", "Stage1Instances.THM_M_0986.root_of_strongLaw_packages", "The exact canonical proposition conditional on both packages."),
    ("X-SOURCE", "terminal", "high", "Map the historical weak-law claim and stronger proof route to pinpoint primary sources, assumptions, and errata.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory the local adapter, mathlib terminal body, imports, axioms, wrappers, and replay evidence.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
statement_fp = "lean-expression-sha256:9a4e61a6c5dea73eb277213b8f95796bcff74d53f63c13fd0d5317ebde502204"
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}

obligations, nodes = [], []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fp = statement_fp if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0986/ObligationTree.lean#root_of_strongLaw_packages" if suffix == "T-ASSEMBLE" else ("mathlib:ProbabilityTheory.strong_law_ae" if suffix == "L-STRONG-LAW" else None),
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if suffix in {"ROOT", "L-STRONG-LAW", "C-AVERAGE-MEASURABLE"} else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else ("candidate-mathlib-strong-law" if suffix == "L-STRONG-LAW" else "none"),
        "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 80 if suffix in {"L-STRONG-LAW", "T-AE-IN-MEASURE"} else 40,
        "semantic_step_ledger": {"premises": "Only the exact declared proof children and formal context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed parents may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-0986/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-0986-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0986/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-0986 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; iid strong-law then AE-to-in-measure architecture; eligibility is independent of candidate closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": oids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"candidate_closed_obligations": [f"{PREFIX}-L-STRONG-LAW"], "accepted_closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and denominators only; candidate availability is not proof acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-AE-IN-MEASURE"],
    f"{PREFIX}-T-AE-IN-MEASURE": [f"{PREFIX}-L-STRONG-LAW", f"{PREFIX}-C-AVERAGE-MEASURABLE"],
    f"{PREFIX}-C-AVERAGE-MEASURABLE": [f"{PREFIX}-N-MEASURABILITY"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-STRONG", f"{PREFIX}-L-STRONG-LAW", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-L-STRONG-LAW")],
    "workflow": [edge("FLOW-PROOF-ASSEMBLE", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-L-STRONG-LAW"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": f"{THEOREM}-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"accepted_closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-L-STRONG-LAW", f"{PREFIX}-C-AVERAGE-MEASURABLE"], "composition_certificates": ["Stage1Instances.THM_M_0986.root_of_strongLaw_packages"], "reason": "Composition is conditional; candidate discovery does not accept either package as proof evidence."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-0986/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in oids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
