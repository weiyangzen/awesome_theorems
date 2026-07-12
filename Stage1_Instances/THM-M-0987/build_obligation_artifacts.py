#!/usr/bin/env python3
"""Build the frozen THM-M-0987 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0987-OBLIGATION_TREE"
THEOREM = "THM-M-0987"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("M0987-ROOT", "root", "critical", "The exact real-valued iid finite-second-moment CLT proposition frozen in Statement.lean.", "Stage1Instances.THM_M_0987.CentralLimitTheoremTarget", "The canonical convergence-in-distribution conclusion."),
    ("M0987-S-DEFS", "definition", "high", "Fix HasLaw, variance, expectation, MemLp, iIndepFun, IdentDistrib, finite sums, Gaussian law, and TendstoInDistribution conventions.", "definitions used by CentralLimitTheoremTarget", "An unambiguous canonical interface."),
    ("M0987-S-CONTEXT", "definition", "high", "Fix both universes, measurable spaces, probability measures, real observations, and ordered binders.", "the binder context of CentralLimitTheoremTarget", "The exact typeclass and universe context."),
    ("M0987-S-BOUNDARY", "branch", "critical", "Include n = 0 and both zero and nonzero variance without adding positivity assumptions.", "planned exact boundary package", "All degenerate cases admitted by the root."),
    ("M0987-S-TRANSPORT", "transport", "normal", "Identify the canonical target with the locally transcribed pinned mathlib source shape.", "Stage1Instances.THM_M_0987.target_iff_pinnedMathlibSourceShape", "A checked bidirectional statement transport."),
    ("M0987-S-FOUNDATION", "certificate", "critical", "Fix the accepted Lean kernel, classical axioms, quotient, computation, and no-oracle policy.", "planned transitive axiom and TCB certificate", "An accepted foundation boundary."),
    ("M0987-N-CENTER", "normalization", "high", "Center every summand by the common expectation and preserve independence and identical distribution.", "pinned mathlib centering reduction", "A centered iid sequence."),
    ("M0987-N-STANDARDIZE", "normalization", "critical", "For nonzero variance, divide centered variables by the positive square root of variance and prove mean zero and second moment one.", "pinned mathlib standardization reduction", "A variance-one iid sequence."),
    ("M0987-B-ZERO", "branch", "critical", "When variance is zero, show every observation is almost everywhere its expectation and the normalized centered sum has the degenerate Gaussian law.", "zero-variance branch of tendstoInDistribution_inv_sqrt_mul_sum_sub", "The root conclusion for variance zero."),
    ("M0987-B-NONZERO", "branch", "critical", "When variance is nonzero, use the standardized CLT and scale the limiting Gaussian back by sqrt variance.", "nonzero-variance branch of tendstoInDistribution_inv_sqrt_mul_sum_sub", "The root conclusion for nonzero variance."),
    ("M0987-B-MERGE", "terminal", "high", "Split exhaustively on variance = 0 and recompose both branches.", "eq_or_ne Var[X 0; P] 0", "The exact arbitrary-variance CLT conclusion."),
    ("M0987-L-CHARFUN-SUM", "core_lemma", "critical", "Factor the characteristic function of the normalized independent finite sum into the nth power of the common characteristic function.", "ProbabilityTheory.charFun_inv_sqrt_mul_sum", "The characteristic-function product identity."),
    ("M0987-L-TAYLOR", "core_lemma", "critical", "Use the second-order characteristic-function expansion at zero for a centered variance-one random variable.", "MeasureTheory.taylor_charFun_two", "The quadratic small-o approximation."),
    ("M0987-L-POWER-LIMIT", "core_lemma", "critical", "Convert the quadratic expansion at t/sqrt n into convergence of the nth powers to exp(-t^2/2).", "ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow", "Pointwise Gaussian characteristic-function convergence."),
    ("M0987-L-LEVY", "bridge", "critical", "Transport pointwise characteristic-function convergence to convergence in distribution.", "MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun", "The standardized convergence-in-distribution result."),
    ("M0987-L-GAUSSIAN", "computation", "high", "Identify the limiting expression exp(-t^2/2) with the characteristic function of gaussianReal 0 1 and transport Gaussian scaling.", "ProbabilityTheory.charFun_gaussianReal; gaussianReal_div_const", "The required Gaussian target law."),
    ("M0987-X-PINNED", "bridge", "critical", "Cross the pinned mathlib proof boundary at the exact declaration type without weakening or changing binders.", "ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub", "An exact proof premise for the canonical root."),
    ("M0987-T-ASSEMBLE", "terminal", "high", "Consume the exact pinned bridge conclusion and yield the canonical Prop definition.", "Stage1Instances.THM_M_0987.ObligationTree.root_of_pinnedBridge", "The exact canonical root, conditionally."),
    ("M0987-X-SOURCE", "terminal", "high", "Map every material analytic step to pinpoint primary-source statements, assumptions, and conventions.", "node-specific human-source crosswalk pending", "Human-source coverage without proof credit."),
    ("M0987-X-PROVENANCE", "certificate", "critical", "Inventory the imported terminal body, transitive declarations, axioms, TCB, license, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

checked = {"M0987-S-DEFS", "M0987-S-CONTEXT", "M0987-S-TRANSPORT", "M0987-T-ASSEMBLE"}
source_na = {"M0987-S-DEFS", "M0987-S-CONTEXT", "M0987-S-TRANSPORT", "M0987-S-FOUNDATION", "M0987-T-ASSEMBLE", "M0987-X-PROVENANCE"}
machine_special = {"M0987-X-SOURCE": "not_applicable", "M0987-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations, nodes = [], []
for oid, kind, risk, claim, target, output in rows:
    fp = "lean-source:v1:sha256:" + statement_hash if oid in {"M0987-ROOT", "M0987-S-DEFS", "M0987-S-CONTEXT", "M0987-S-TRANSPORT"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    body = "local:Stage1_Instances/THM-M-0987/ObligationTree.lean#root_of_pinnedBridge" if oid == "M0987-T-ASSEMBLE" else None
    obligations.append({"obligation_id": oid, "statement_fingerprint": fp, "kind": kind, "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": "not_applicable" if oid in source_na else "required", "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": body})
    nodes.append({
        "node_id": "THM-M-0987-" + oid.removeprefix("M0987-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0987-ROOT" else "M4"), "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "primary-source-node-map-pending" if oid not in source_na else "not-applicable",
        "provenance_id": "pinned-mathlib-candidate-C02" if oid == "M0987-X-PINNED" else ("local-conditional-composition" if body else "none"),
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no numerical experiment or oracle may close this node", "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires conclusions and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0987/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional interface only; no unlisted premise, imported proof credit, H0/R0, or theorem completion is supplied.",
        "task_ids": [ITEM, "S56-M-0987-PROOF"], "owned_sources": ["Stage1_Instances/THM-M-0987/ObligationTree.lean"] if body else [],
        "owner": "THM-M-0987 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00", "freeze_basis": "Exact statement and bounded anchor audit; the zero/nonzero variance and characteristic-function route was expanded before proof-phase closure metrics.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash, "root_obligation_id": "M0987-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0987-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.", "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "The obligation universe is frozen, but the imported bridge is not credited or installed as the root proof; audit and theorem completion remain false.",
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0987-ROOT": ["M0987-T-ASSEMBLE"], "M0987-T-ASSEMBLE": ["M0987-X-PINNED"], "M0987-X-PINNED": ["M0987-B-MERGE"],
    "M0987-B-MERGE": ["M0987-B-ZERO", "M0987-B-NONZERO"], "M0987-B-NONZERO": ["M0987-N-CENTER", "M0987-N-STANDARDIZE", "M0987-L-LEVY", "M0987-L-GAUSSIAN"],
    "M0987-L-LEVY": ["M0987-L-CHARFUN-SUM", "M0987-L-POWER-LIMIT"], "M0987-L-POWER-LIMIT": ["M0987-L-TAYLOR"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M0987-ROOT", "logical_decomposition", "M0987-S-DEFS"), edge("REF-ROOT-CONTEXT", "M0987-ROOT", "logical_decomposition", "M0987-S-CONTEXT"), edge("REF-ROOT-BOUNDARY", "M0987-ROOT", "logical_decomposition", "M0987-S-BOUNDARY"), edge("REF-ROOT-TRANSPORT", "M0987-ROOT", "logical_decomposition", "M0987-S-TRANSPORT")],
    "provenance": [edge("PROV-PIN", "M0987-X-PROVENANCE", "provenance_of", "M0987-X-PINNED"), edge("SRC-TAYLOR", "M0987-L-TAYLOR", "source_map", "M0987-X-SOURCE")],
    "evidence": [], "trust": [edge("TRUST-FOUND", "M0987-ROOT", "trusts", "M0987-S-FOUNDATION"), edge("TRUST-PROV", "M0987-ROOT", "trusts", "M0987-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", "M0987-S-DEFS", "documents", "M0987-ROOT"), edge("DOC-SOURCE", "M0987-X-SOURCE", "documents", "M0987-X-PINNED")],
    "workflow": [edge("FLOW-PROOF-PIN", "M0987-T-ASSEMBLE", "workflow_depends_on", "M0987-X-PINNED"), edge("FLOW-VALIDATE-PROOF", "M0987-X-PROVENANCE", "workflow_depends_on", "M0987-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"]); incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-0987-OBLIGATIONS-v1", "registry_denominator_sha256": denominator, "root_node_id": "M0987-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composition edges run child to parent.", "nodes": nodes, "graphs": graphs, "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0987-X-PINNED"], "composition_certificates": ["Stage1Instances.THM_M_0987.ObligationTree.root_of_pinnedBridge"], "reason": "The checked composition consumes an explicit exact bridge premise; proof-phase integration and full provenance remain open."}}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0987/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0987 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": []} for oid in ids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(ids)} obligations and {sum(len(v) for v in graph_edges.values())} typed edges")
print(denominator)
