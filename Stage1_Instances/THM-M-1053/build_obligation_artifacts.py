#!/usr/bin/env python3
"""Build the frozen THM-M-1053 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1053-OBLIGATION_TREE"
THEOREM = "THM-M-1053"
PREFIX = "M1053"


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


rows = [
    ("ROOT", "root", "critical", "Prove the exact frozen real-valued Birkhoff pointwise ergodic theorem on probability spaces.", "Stage1.THM_M_1053.StatementShape", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze forward Cesaro averages, almost-everywhere convergence, integrability, invariance, and ergodicity.", "Stage1.THM_M_1053.{timeAverage,StatementShape}", "The exact elaborated interface."),
    ("S-BOUNDARY", "terminal", "normal", "Preserve n=0, noninvertible transformations, atomic spaces, and the distinction between the general and ergodic conclusions.", "Stage1.THM_M_1053.timeAverage_zero", "Checked zero-average boundary and explicit domain policy."),
    ("S-FOUNDATION", "certificate", "critical", "Fix classical choice, quotient, extensionality, kernel, import, and no-oracle policy for every terminal body.", "planned transitive axiom and TCB report", "Accepted trust boundary."),
    ("N-AVERAGE", "normalization", "high", "Transport the frozen finite-sum average to the formal Birkhoff-average convention, including indexing and normalization.", "Stage1.THM_M_1053.AnchorAudit.auditedTimeAverage_eq_birkhoffAverage", "A checked average-encoding transport."),
    ("L-MAXIMAL", "core_lemma", "critical", "Establish the maximal ergodic inequality needed to control exceptional sets for integrable observables.", "planned maximal ergodic inequality with exact hypotheses", "A maximal estimate usable by the approximation argument."),
    ("L-DENSE-CLASS", "core_lemma", "critical", "Prove pointwise convergence on a dense controlled class and audit the approximation interface.", "planned dense-class pointwise convergence theorem", "Convergence for the controlled class."),
    ("L-AE-CONVERGENCE", "core_lemma", "critical", "Combine maximal control and dense-class convergence to obtain almost-everywhere convergence for every integrable real observable.", "planned a.e. Birkhoff convergence theorem", "Existence of an a.e. pointwise limit."),
    ("L-LIMIT-INTEGRABLE", "core_lemma", "high", "Show the selected almost-everywhere limit is integrable.", "planned integrability theorem for the Birkhoff limit", "Integrability of the limit witness."),
    ("L-LIMIT-INVARIANT", "core_lemma", "high", "Show the selected limit is invariant almost everywhere under the measure-preserving endomorphism.", "planned a.e. invariance theorem for the Birkhoff limit", "Almost-everywhere invariance of the limit witness."),
    ("T-GENERAL", "terminal", "critical", "Assemble convergence, integrability, and invariance into the general invariant-limit package.", "Stage1.THM_M_1053.GeneralInvariantLimitPackage", "The complete nonergodic conclusion."),
    ("L-ERGODIC-IDENTIFICATION", "bridge", "critical", "Use ergodicity and invariance, with integral preservation, to identify the limit with the constant space integral.", "Stage1.THM_M_1053.ErgodicLimitIdentificationPackage", "The ergodic space-average identification."),
    ("T-ASSEMBLE", "transport", "high", "Compose the general invariant-limit and ergodic-identification packages into the exact root.", "Stage1.THM_M_1053.statementShape_of_packages", "The exact root conditional on both packages."),
    ("X-EXTERNAL", "bridge", "critical", "Integrate or independently reconstruct the immutable external pointwise-Birkhoff candidate and check an exact adapter.", "external candidate adapter, currently outside pinned closure", "A kernel-checked repo-local theorem boundary, not merely a citation."),
    ("X-SOURCE", "terminal", "high", "Map every material analytic step to reviewed primary and modern source passages, hypotheses, conventions, and errata.", "node-specific human source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, wrappers, imports, licenses, axioms, TCB edges, and replay receipts.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-N-AVERAGE", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-expression-sha256:f4b06a49160cd083fa4cf1bb3b1ddfe1453dbcb1e521ff2c09ba5d3753a2e562"

obligations = []
nodes = []
for suffix, kind, risk, claim, target, output in rows:
    oid = f"{PREFIX}-{suffix}"
    machine = machine_special.get(oid, "required")
    fp = statement_fp if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1053/ObligationTree.lean#statementShape_of_packages" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M1" if suffix in {"ROOT", "X-EXTERNAL"} else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else ("anchor-audit:M1053-A-ERGODIC-THEORY" if suffix == "X-EXTERNAL" else "none"),
        "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if suffix in {"L-MAXIMAL", "L-DENSE-CLASS", "L-AE-CONVERGENCE", "X-EXTERNAL"} else 40,
        "semantic_step_ledger": {"premises": "Only exact incoming proof children and the stated formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent or support edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-1053/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise or root closure.",
        "task_ids": [ITEM, "S56-M-1053-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1053/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1053 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor inventory; classical maximal-inequality/dense-class Birkhoff architecture; eligibility assigned independently of closure status.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M1"},
    "status_boundary": "Scope and denominators only; no Birkhoff proof, dependency integration, source acceptance, audit completion, or theorem completion."
}


def edge(eid, source, typ, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-GENERAL", f"{PREFIX}-L-ERGODIC-IDENTIFICATION"],
    f"{PREFIX}-T-GENERAL": [f"{PREFIX}-L-AE-CONVERGENCE", f"{PREFIX}-L-LIMIT-INTEGRABLE", f"{PREFIX}-L-LIMIT-INVARIANT"],
    f"{PREFIX}-L-AE-CONVERGENCE": [f"{PREFIX}-L-MAXIMAL", f"{PREFIX}-L-DENSE-CLASS", f"{PREFIX}-N-AVERAGE", f"{PREFIX}-X-EXTERNAL"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY"), edge("REF-ROOT-FOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-FOUNDATION")],
    "provenance": [edge("SRC-ANALYTIC", f"{PREFIX}-L-AE-CONVERGENCE", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-EXT", f"{PREFIX}-X-EXTERNAL", "provenance_of", f"{PREFIX}-L-AE-CONVERGENCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-L-AE-CONVERGENCE")],
    "workflow": [edge("FLOW-ASSEMBLE-GENERAL", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-GENERAL"), edge("FLOW-ASSEMBLE-ERGODIC", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-L-ERGODIC-IDENTIFICATION"), edge("FLOW-GENERAL-CONV", f"{PREFIX}-T-GENERAL", "workflow_depends_on", f"{PREFIX}-L-AE-CONVERGENCE"), edge("FLOW-EXT-INTEGRATE", f"{PREFIX}-L-AE-CONVERGENCE", "workflow_depends_on", f"{PREFIX}-X-EXTERNAL"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-GENERAL", f"{PREFIX}-L-ERGODIC-IDENTIFICATION"], "composition_certificates": ["Stage1.THM_M_1053.statementShape_of_packages"], "reason": "Final composition is conditional; both mathematical input packages remain open and the external candidate is outside the pinned closure."}
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1053/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in ids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
