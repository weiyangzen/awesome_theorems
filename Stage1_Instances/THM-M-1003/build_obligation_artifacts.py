#!/usr/bin/env python3
"""Generate the frozen THM-M-1003 registry and typed graph records."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1003-OBLIGATION_TREE"
THEOREM = "THM-M-1003"
PREFIX = "M1003"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen Lp martingale convergence target.", "Stage1Instances.THM_M_1003.LpMartingaleConvergenceTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze the finite-measure, Nat-indexed real martingale data, strict exponent, and common-limit predicate.", "Stage1Instances.THM_M_1003.{LpBoundedMartingale,ConvergesAEAndInLp}", "The exact elaborated vocabulary."),
    ("S-BOUNDARY", "terminal", "high", "Preserve strict 1<p<infinity while admitting zero finite measure and arbitrary measurable spaces.", "Stage1Instances.THM_M_1003.{exponent_ne_one,exponent_ne_top}", "Checked endpoint exclusions and explicit degenerate-case policy."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, measure-theory axioms, imports, TCB, and the no-oracle boundary.", "planned transitive axiom and import certificate", "Accepted foundation and trust profile."),
    ("N-L1-BOUND", "reduction", "critical", "Derive the uniform L1 bound required by the pinned a.e.-convergence theorem from the uniform Lp bound, p>1, and finite measure.", "planned exact Holder/finite-measure reduction", "A uniform eLpNorm bound at exponent one."),
    ("B-ENDPOINTS", "branch", "high", "Discharge endpoint and degenerate branches without silently proving p=1 or p=infinity variants.", "planned boundary composition over exponent_ne_one/exponent_ne_top and zero measure", "Exhaustive confirmation that the downstream route remains in the strict exponent regime."),
    ("C-LIMIT", "construction", "critical", "Construct the selected Filtration.limitProcess and establish its measurability conventions.", "MeasureTheory.Filtration.limitProcess", "A concrete common limit candidate."),
    ("L-AE-LIMIT", "bridge", "critical", "Apply the pinned martingale/submartingale convergence anchor using the derived L1 bound.", "MeasureTheory.Submartingale.ae_tendsto_limitProcess", "Almost-everywhere convergence to the selected limit."),
    ("L-LIMIT-MEMLP", "bridge", "critical", "Apply the pinned limit MemLp anchor at the original exponent using the uniform Lp bound.", "MeasureTheory.Submartingale.memLp_limitProcess", "MemLp of the selected limit at the same exponent."),
    ("L-COND-REP", "core_lemma", "critical", "Prove each martingale value is the conditional expectation of the selected terminal limit.", "planned same-limit conditional-expectation representation", "D.process n = E[limit | filtration n] almost everywhere."),
    ("L-COND-APPROX", "core_lemma", "critical", "Prove increasing-filtration conditional expectations of the terminal MemLp variable converge in Lp for 1<p<infinity.", "planned same-exponent conditional-expectation approximation theorem", "The eLpNorm difference tends to zero at D.exponent."),
    ("T-CANDIDATE", "terminal", "critical", "Combine limit MemLp and a.e. convergence for the same selected limit.", "Stage1Instances.THM_M_1003.LimitCandidatePackage", "The complete common-limit candidate package."),
    ("T-SAME-EXPONENT", "terminal", "critical", "Compose conditional representation and approximation into same-exponent norm convergence.", "Stage1Instances.THM_M_1003.SameExponentNormPackage", "Lp norm convergence to the selected common limit."),
    ("T-ASSEMBLE", "transport", "critical", "Consume candidate and same-exponent packages to produce the exact canonical root.", "Stage1Instances.THM_M_1003.root_of_limit_packages", "The exact root, conditional on both open child packages."),
    ("X-SOURCE", "terminal", "high", "Map every analytic bridge to reviewed primary-source theorem/page, assumptions, conventions, and errata.", "non-machine primary-source node crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, wrappers, imports, axiom closure, TCB edges, and replay receipts.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-expression-sha256:ead76891696316502f96466e97e0ec725b72cb1f2dfdc6d8afa4e405e79b8e9f"

obligations = []
nodes = []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fingerprint = statement_fp if suffix == "ROOT" else "planned:v1:sha256:" + digest([oid, claim, target, output])
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint,
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1003/ObligationTree.lean#root_of_limit_packages" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}",
        "obligation_id": oid,
        "kind": kind,
        "human_statement": claim,
        "formal_target": target,
        "output": output,
        "human_debt": "H3",
        "machine_debt": "M0-L" if oid in checked else ("M4" if machine == "required" else "M3"),
        "readability_debt": "R3",
        "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if suffix in {"N-L1-BOUND", "L-COND-REP", "L-COND-APPROX"} else 40,
        "semantic_step_ledger": {"premises": "Only the exact declared proof children and formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-1003/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1003-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1003/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1003 proof lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus bounded anchor audit; L1 reduction, pinned a.e./MemLp anchors, conditional-expectation representation and approximation architecture; eligibility frozen independently of closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": oids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": oids,
        "informational_overlays": [f"{PREFIX}-X-PROVENANCE"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M4"},
    "status_boundary": "Scope and denominators only; no full Lp proof, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-CANDIDATE", f"{PREFIX}-T-SAME-EXPONENT"],
    f"{PREFIX}-T-CANDIDATE": [f"{PREFIX}-C-LIMIT", f"{PREFIX}-L-AE-LIMIT", f"{PREFIX}-L-LIMIT-MEMLP"],
    f"{PREFIX}-L-AE-LIMIT": [f"{PREFIX}-N-L1-BOUND"],
    f"{PREFIX}-T-SAME-EXPONENT": [f"{PREFIX}-L-COND-REP", f"{PREFIX}-L-COND-APPROX"],
    f"{PREFIX}-L-COND-REP": [f"{PREFIX}-T-CANDIDATE"],
    f"{PREFIX}-L-COND-APPROX": [f"{PREFIX}-L-COND-REP", f"{PREFIX}-L-LIMIT-MEMLP", f"{PREFIX}-B-ENDPOINTS"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-ANALYTIC", f"{PREFIX}-L-COND-APPROX", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-DEFS", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-L-COND-APPROX")],
    "workflow": [edge("FLOW-PROOF-CAND", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-CANDIDATE"), edge("FLOW-PROOF-NORM", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-SAME-EXPONENT"), edge("FLOW-PROV", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-CANDIDATE", f"{PREFIX}-T-SAME-EXPONENT"], "composition_certificates": ["Stage1Instances.THM_M_1003.root_of_limit_packages"], "reason": "Final composition is conditional; both proof-package hypotheses remain open, with same-exponent conditional-expectation approximation central."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1003/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in oids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

intake_path = HERE / "intake.json"
intake = json.loads(intake_path.read_text())
intake["obligation_registry_hash"] = "sha256:" + denominator
intake["obligation_registry_version"] = 1
intake["obligation_tree_state"] = "self_tested_pending_master_acceptance"
intake["status_boundary"] = "Planned lifecycle with an elaborated exact statement and self-tested obligation freeze pending master acceptance. Root remains open at H3/M4/R3; no full Lp proof, source acceptance, validation, or theorem completion is claimed."
intake_path.write_text(json.dumps(intake, indent=2, ensure_ascii=True) + "\n")
print(denominator)
