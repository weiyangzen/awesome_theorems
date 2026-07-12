#!/usr/bin/env python3
"""Build the frozen THM-M-1029 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1029-OBLIGATION_TREE"
THEOREM = "THM-M-1029"
PREFIX = "M1029"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen Levy martingale-characterization target.", "Stage1Instances.THM_M_1029.LevyMartingaleCharacterizationTarget", "The canonical proposition."),
    ("S-DEFINITIONS", "definition", "high", "Freeze nonnegative-real time, compensated square, relative Brownian conclusion, and filtration dependence.", "Stage1Instances.THM_M_1029.{Time,QuadraticCompensated,IsBrownianMotionRelative}", "The exact elaborated vocabulary."),
    ("S-BOUNDARY", "terminal", "high", "Preserve pathwise continuity, almost-everywhere zero start, and the s=t zero-variance increment case.", "Stage1Instances.THM_M_1029.{target_iff_expandedSourceShape,zeroElapsedVariance}", "Checked statement and boundary behavior."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, measure-theory axioms, imports, TCB, and the no-oracle boundary.", "planned transitive axiom and import certificate", "Accepted foundation and trust profile."),
    ("N-QUADRATIC-VARIATION", "normalization", "critical", "Derive that the continuous martingale has deterministic quadratic variation t from the compensated-square martingale hypothesis.", "planned exact predictable/quadratic-variation theorem", "Quadratic variation [X]_t=t in the representation required downstream."),
    ("C-EXPONENTIAL", "construction", "critical", "For every real frequency construct the complex exponential process associated with X and its deterministic quadratic variation, proving measurability and integrability.", "planned exponential-process construction with invariants", "A well-defined integrable exponential process for every frequency."),
    ("L-EXPONENTIAL-MARTINGALE", "core_lemma", "critical", "Prove the constructed exponential process is a martingale, using the quadratic-variation identity and an explicitly audited stochastic-calculus bridge.", "planned exponential-martingale theorem", "The exponential martingale needed for conditional characteristic functions."),
    ("L-CONDITIONAL-CHARACTERISTIC", "bridge", "critical", "Derive the conditional characteristic function of X_t-X_s given F_s for every s<=t and frequency.", "planned conditional characteristic-function identity", "E[exp(i u (X_t-X_s)) | F_s] = exp(-u^2 (t-s)/2)."),
    ("L-GAUSSIAN-LAW", "core_lemma", "critical", "Identify the increment law as the centered real Gaussian of variance t-s from equality of characteristic functions, including variance zero.", "planned characteristic-function uniqueness and Gaussian identification", "HasLaw (X_t-X_s) (gaussianReal 0 (t-s)) P."),
    ("L-INDEPENDENCE", "core_lemma", "critical", "Turn the deterministic conditional characteristic function into independence of the increment from F_s.", "planned conditional-characteristic independence criterion", "Indep (F s) (comap increment (borel Real)) P."),
    ("T-INCREMENTS", "terminal", "critical", "Combine Gaussian-law and independence conclusions uniformly for every s<=t.", "Stage1Instances.THM_M_1029.IncrementLawPackage", "The complete increment-law package."),
    ("T-ASSEMBLE", "transport", "high", "Combine unchanged continuity and zero-start hypotheses with the increment-law package to obtain the exact root.", "Stage1Instances.THM_M_1029.root_of_incrementLawPackage", "The exact canonical root, conditional on the increment package."),
    ("X-SOURCE", "terminal", "high", "Map every analytic bridge to a reviewed primary-source theorem/page, assumptions, conventions, and errata record.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory every terminal body, wrapper, import, axiom, TCB edge, and replay receipt.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-expression-sha256:f3e443377f8cac2eba62a6ebcf6f05ce5bd453f3075d9de573641856e21331b2"

obligations = []
nodes = []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fingerprint = statement_fp if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-1029/ObligationTree.lean#root_of_incrementLawPackage" if suffix == "T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if oid in checked else ("M3" if suffix == "ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if suffix == "T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 100 if suffix in {"N-QUADRATIC-VARIATION", "L-EXPONENTIAL-MARTINGALE", "L-CONDITIONAL-CHARACTERISTIC"} else 40,
        "semantic_step_ledger": {"premises": "Only the exact declared proof children and formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-1029/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1029-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1029/ObligationTree.lean"] if suffix == "T-ASSEMBLE" else [],
        "owner": "THM-M-1029 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus bounded anchor audit; quadratic-variation/exponential-martingale architecture; eligibility frozen independently of closure.",
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
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Scope and denominators only; no Levy proof, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-INCREMENTS"],
    f"{PREFIX}-T-INCREMENTS": [f"{PREFIX}-L-GAUSSIAN-LAW", f"{PREFIX}-L-INDEPENDENCE"],
    f"{PREFIX}-L-GAUSSIAN-LAW": [f"{PREFIX}-L-CONDITIONAL-CHARACTERISTIC"],
    f"{PREFIX}-L-INDEPENDENCE": [f"{PREFIX}-L-CONDITIONAL-CHARACTERISTIC"],
    f"{PREFIX}-L-CONDITIONAL-CHARACTERISTIC": [f"{PREFIX}-L-EXPONENTIAL-MARTINGALE"],
    f"{PREFIX}-L-EXPONENTIAL-MARTINGALE": [f"{PREFIX}-N-QUADRATIC-VARIATION", f"{PREFIX}-C-EXPONENTIAL"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-ANALYTIC", f"{PREFIX}-L-EXPONENTIAL-MARTINGALE", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-L-EXPONENTIAL-MARTINGALE")],
    "workflow": [edge("FLOW-PROOF-TREE", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-INCREMENTS"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-INCREMENTS"], "composition_certificates": ["Stage1Instances.THM_M_1029.root_of_incrementLawPackage"], "reason": "Final composition is conditional; the increment-law package has no proof body."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1029/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in oids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

instance_path = HERE / "instance.json"
instance = json.loads(instance_path.read_text())
instance["obligation_registry_hash"] = "sha256:" + denominator
instance["obligation_registry_version"] = 1
instance["obligation_tree_state"] = "self_tested_pending_master_acceptance"
instance["canonical_claim_status"] = "exact_formal_statement_elaborated_obligation_architecture_frozen"
instance["status_boundary"] = "Planned lifecycle with an elaborated exact statement and self-tested obligation freeze pending master acceptance. Root remains H2/M3/R4; no Levy proof, H0 source fidelity, audit completion, or theorem completion is claimed."
instance["owned_artifacts"] = sorted(set(instance["owned_artifacts"] + ["ObligationTree.lean", "obligation-registry.json", "typed-graphs.json", "validation-specs.json", "obligation-tree.md", "obligation-tree-validation.md", "build_obligation_artifacts.py", "check_obligation_tree.py"]))
instance_path.write_text(json.dumps(instance, indent=2, ensure_ascii=True) + "\n")
print(denominator)
