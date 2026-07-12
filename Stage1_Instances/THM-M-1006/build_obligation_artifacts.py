#!/usr/bin/env python3
"""Build the frozen THM-M-1006 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1006-OBLIGATION_TREE"
THEOREM = "THM-M-1006"
PREFIX = "M1006"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("M1006-ROOT", "root", "critical", "The exact finite discrete-time real-valued BDG proposition frozen in Statement.lean.", "Stage1Instances.THM_M_1006.StatementShape", "The canonical two-sided inequality with constants uniform in the process and horizon."),
    ("M1006-S-DEFINITIONS", "definition", "high", "Freeze the finite maximal process and discrete quadratic variation definitions.", "Stage1Instances.THM_M_1006.{maximalProcess,quadraticVariation}", "The exact pointwise quantities occurring under the lintegrals."),
    ("M1006-S-SCOPE", "normalization", "critical", "Preserve p > 0, probability-space, filtration, real-valued martingale, zero-start, finite-horizon, and constant-uniformity binders.", "Stage1Instances.THM_M_1006.StatementShape", "The exact ordered scope with no weakened or moved hypothesis."),
    ("M1006-S-BOUNDARY", "branch", "high", "Account for horizon zero, the zero martingale, infinite moments, and exclusion of nonzero initial values.", "planned exact boundary lemmas for StatementShape", "Boundary behavior matching the frozen ENNReal formulation."),
    ("M1006-S-FOUNDATION", "certificate", "critical", "Fix classical choice, measure-theory imports, axiom closure, TCB, and no-oracle policy.", "planned transitive axiom and trust report", "An accepted foundation and trust boundary."),
    ("M1006-N-DIFFERENCES", "construction", "high", "Pass from the zero-start martingale to its adapted martingale-difference sequence and reconstruct every finite partial sum.", "planned martingale-difference decomposition", "A checked difference process whose partial sums equal f."),
    ("M1006-N-SQUARE", "normalization", "high", "Identify the sum of squared differences with quadraticVariation and its square root p-moment with the p/2 power used in the target.", "planned square-function encoding equivalence", "Exact transport between the proof architecture and frozen integrands."),
    ("M1006-C-STOPPING", "construction", "critical", "Construct first-crossing stopping times for maximal and square functions and prove measurability, adaptedness, and bounded-horizon invariants.", "planned finite stopping-time package", "Valid stopped processes at every distribution threshold."),
    ("M1006-L-STOPPED", "core_lemma", "critical", "Prove the required stopped-martingale estimates without assuming integrability beyond the frozen extended-moment statement.", "planned stopped increment estimate", "Quantitative control for the good-lambda argument."),
    ("M1006-L-GOOD-UPPER", "core_lemma", "critical", "Derive the good-lambda distribution inequality controlling the maximal function by the square function.", "planned upper good-lambda inequality", "A tail bound sufficient for the upper BDG direction."),
    ("M1006-L-GOOD-LOWER", "core_lemma", "critical", "Derive the reverse distribution inequality controlling the square function by the maximal function.", "planned lower good-lambda inequality", "A tail bound sufficient for the lower BDG direction."),
    ("M1006-L-LAYERCAKE", "core_lemma", "critical", "Convert nonnegative tail inequalities to ENNReal p-moment inequalities for every real p > 0.", "planned layer-cake/lintegral identity", "Exact rpow moment bounds, including infinite-value cases."),
    ("M1006-B-P-RANGE", "branch", "critical", "Discharge the distinct subunit, unit, and superunit exponent regimes while retaining constants depending only on p.", "planned exhaustive p-range recomposition", "One theorem valid for all p > 0."),
    ("M1006-T-LOWER", "terminal", "critical", "Combine reverse good-lambda, layer-cake, exponent cases, and square-function transport into the lower inequality.", "Stage1Instances.THM_M_1006.LowerBDG", "A positive finite lower constant uniform in all later binders."),
    ("M1006-T-UPPER", "terminal", "critical", "Combine good-lambda, layer-cake, exponent cases, and square-function transport into the upper inequality.", "Stage1Instances.THM_M_1006.UpperBDG", "A positive finite upper constant uniform in all later binders."),
    ("M1006-T-ASSEMBLE", "transport", "high", "Pair independently uniform directional constants and compose their pointwise estimates into the exact conjunction.", "Stage1Instances.THM_M_1006.root_of_directional_BDG", "The exact canonical root conditional on both directional packages."),
    ("M1006-X-SOURCE", "terminal", "high", "Map every stopping, good-lambda, layer-cake, and exponent-range step to reviewed primary-source passages and conventions.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("M1006-X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, imports, wrappers, axioms, TCB, placeholders, and replay evidence.", "planned machine-derived provenance closure", "Release provenance without mathematical proof credit."),
]

checked = {"M1006-S-DEFINITIONS", "M1006-S-SCOPE", "M1006-T-ASSEMBLE"}
source_na = {"M1006-S-DEFINITIONS", "M1006-S-SCOPE", "M1006-S-BOUNDARY", "M1006-S-FOUNDATION", "M1006-X-PROVENANCE"}
machine_special = {"M1006-X-SOURCE": "not_applicable", "M1006-X-PROVENANCE": "informational"}
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor_audit.json").read_bytes()).hexdigest()

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in rows:
    fp = ("lean-source:v1:sha256:" + statement_hash) if oid in {"M1006-ROOT", "M1006-S-DEFINITIONS", "M1006-S-SCOPE"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    exclusion = {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine)
    body = "local:Stage1_Instances/THM-M-1006/ObligationTree.lean#root_of_directional_BDG" if oid == "M1006-T-ASSEMBLE" else None
    obligations.append({"obligation_id": oid, "statement_fingerprint": fp, "kind": kind, "root_relevant": True, "machine_eligibility": machine, "human_source_eligibility": "not_applicable" if oid in source_na else "required", "readable_eligibility": "required", "risk_class": risk, "exclusion_reason": exclusion, "terminal_proof_body_id": body})
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX + "-"), "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M1006-ROOT" else "M4"), "readability_debt": "R3",
        "evidence_ids": [], "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending", "provenance_id": "local-conditional-composition" if body else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending", "computation_record": "none; no numerical experiment, native oracle, or external result may close this node",
        "step_budget": 100 if risk == "critical" else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof_requires conclusions and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or non-proof support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-1006/obligation-tree.md#" + oid.lower(), "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Frozen architecture or checked conditional interface only; no unlisted premise and no BDG closure is supplied.", "task_ids": [ITEM, "S56-M-1006-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1006/ObligationTree.lean"] if body else [], "owner": "THM-M-1006 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"}
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact finite discrete-time statement and bounded anchor audit; stopping-time/good-lambda architecture expanded and eligibility assigned before observing closure.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash, "root_obligation_id": "M1006-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M1006-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires registry version 2 and an append-only old/new ID delta.", "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no directional BDG proof, source acceptance, audit completion, or theorem completion."
}


def edge(eid, source, typ, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {
    "M1006-ROOT": ["M1006-T-ASSEMBLE"],
    "M1006-T-ASSEMBLE": ["M1006-T-LOWER", "M1006-T-UPPER"],
    "M1006-T-LOWER": ["M1006-N-DIFFERENCES", "M1006-N-SQUARE", "M1006-L-GOOD-LOWER", "M1006-L-LAYERCAKE", "M1006-B-P-RANGE"],
    "M1006-T-UPPER": ["M1006-N-DIFFERENCES", "M1006-N-SQUARE", "M1006-L-GOOD-UPPER", "M1006-L-LAYERCAKE", "M1006-B-P-RANGE"],
    "M1006-L-GOOD-LOWER": ["M1006-C-STOPPING", "M1006-L-STOPPED"],
    "M1006-L-GOOD-UPPER": ["M1006-C-STOPPING", "M1006-L-STOPPED"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", "M1006-ROOT", "logical_decomposition", "M1006-S-DEFINITIONS"), edge("REF-ROOT-SCOPE", "M1006-ROOT", "logical_decomposition", "M1006-S-SCOPE"), edge("REF-ROOT-BOUND", "M1006-ROOT", "logical_decomposition", "M1006-S-BOUNDARY"), edge("REF-ROOT-FOUND", "M1006-ROOT", "logical_decomposition", "M1006-S-FOUNDATION")],
    "provenance": [edge("SRC-STOP", "M1006-C-STOPPING", "source_map", "M1006-X-SOURCE"), edge("SRC-GOOD-U", "M1006-L-GOOD-UPPER", "source_map", "M1006-X-SOURCE"), edge("SRC-GOOD-L", "M1006-L-GOOD-LOWER", "source_map", "M1006-X-SOURCE"), edge("PROV-ROOT", "M1006-X-PROVENANCE", "provenance_of", "M1006-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", "M1006-ROOT", "trusts", "M1006-S-FOUNDATION"), edge("TRUST-PROV", "M1006-ROOT", "trusts", "M1006-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", "M1006-S-DEFINITIONS", "documents", "M1006-ROOT"), edge("DOC-ANALYTIC", "M1006-X-SOURCE", "documents", "M1006-L-LAYERCAKE")],
    "workflow": [edge("FLOW-ASSEMBLE-LOWER", "M1006-T-ASSEMBLE", "workflow_depends_on", "M1006-T-LOWER"), edge("FLOW-ASSEMBLE-UPPER", "M1006-T-ASSEMBLE", "workflow_depends_on", "M1006-T-UPPER"), edge("FLOW-PROV-ASSEMBLE", "M1006-X-PROVENANCE", "workflow_depends_on", "M1006-T-ASSEMBLE")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for row in edges:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "registry_id": "THM-M-1006-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1006-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.", "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "root_machine_debt": "M3", "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M1006-T-LOWER", "M1006-T-UPPER"], "composition_certificates": ["Stage1Instances.THM_M_1006.root_of_directional_BDG"], "reason": "The assembly is conditional; neither directional BDG package has a proof body."}
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": []}
for oid, *_ in rows:
    recipes["recipes"].append({"recipe_id": "VAL-" + oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-1006/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 30, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-1006 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": []})

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(value) for value in graph_edges.values())} typed edges")
print(denominator)
