#!/usr/bin/env python3
"""Build the frozen THM-M-1008 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1008-OBLIGATION_TREE"
THEOREM = "THM-M-1008"
PREFIX = "M1008"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


rows = [
    ("ROOT", "root", "critical", "The exact frozen finite-permutation-invariant iid zero-one target.", "Stage1Instances.THM_M_1008.HewittSavageZeroOneTarget", "The canonical zero-or-one proposition."),
    ("S-DEFINITIONS", "definition", "high", "Preserve the probability space, iid family, product-measurable path event, finite-support permutation action, and pullback conclusion.", "Stage1Instances.THM_M_1008.{HewittSavageZeroOneTarget,target_iff_expandedSourceShape}", "The exact elaborated statement boundary."),
    ("S-BOUNDARY", "terminal", "high", "Include constant processes, empty and universal events, and the identity permutation; exclude exchangeability-only and almost-everywhere invariance substitutes.", "Stage1Instances.THM_M_1008.identity_hasFiniteSupport", "Checked encoding boundaries."),
    ("S-FOUNDATION", "certificate", "critical", "Audit classical choice, quotient, propositional extensionality, imports, TCB, and no-oracle policy for every terminal body.", "planned transitive axiom and import certificate", "Accepted foundation and trust profile."),
    ("N-CYLINDER", "normalization", "critical", "Approximate the measurable path event in measure by an event depending on finitely many coordinates, with a quantitative error bound.", "planned product-sigma finite-coordinate approximation theorem", "A finite-coordinate measurable approximant and error estimate."),
    ("C-DISJOINT-BLOCK", "construction", "critical", "Choose a finite-support coordinate permutation moving every coordinate used by the approximant to a disjoint finite block.", "planned finite-set displacement permutation", "A checked permutation with finite support and disjoint source/image blocks."),
    ("L-IID-REINDEX", "core_lemma", "high", "Prove reindexing by the chosen permutation preserves mutual independence and the full path law.", "ProbabilityTheory.iIndepFun.precomp; ProbabilityTheory.IdentDistrib.pi", "Independence and identical path distribution after reindexing."),
    ("L-SYMMETRY-TRANSFER", "bridge", "critical", "Use pointwise finite-permutation invariance to identify the original pullback event with its permuted-path pullback, not merely their measures.", "Stage1Instances.THM_M_1008.IsSymmetricEvent", "Exact event equality under the chosen permutation."),
    ("L-BLOCK-INDEPENDENCE", "core_lemma", "critical", "Derive independence of the original finite-coordinate approximant and its disjoint reindexed copy from mutual independence.", "planned iIndepFun finite disjoint-coordinate sigma-algebra bridge", "Independence of the two finite-block events."),
    ("L-LIMIT-FACTOR", "core_lemma", "critical", "Pass the approximation and symmetry identities through the independence factorization and let the error tend to zero.", "planned measure symmetric-difference/error limiting argument", "The identity mu(A intersect A) = mu(A) * mu(A)."),
    ("T-SELF-INDEPENDENCE", "terminal", "critical", "Convert the limiting factorization into self-independence of the exact pulled-back event, including its generated sigma-algebra obligations.", "Stage1Instances.THM_M_1008.SelfIndependencePackage", "IndepSet A A mu for the exact event."),
    ("X-ZERO-ONE", "bridge", "high", "Apply the pinned finite-measure self-independence endpoint without crediting it for the missing Hewitt-Savage bridge.", "ProbabilityTheory.measure_eq_zero_or_one_of_indepSet_self", "The zero-or-one conclusion from self-independence."),
    ("T-ASSEMBLE", "transport", "high", "Compose the self-independence package and pinned endpoint into the exact canonical root.", "Stage1Instances.THM_M_1008.root_of_selfIndependencePackage", "The exact root conditional on the open package."),
    ("X-SOURCE", "terminal", "high", "Map every approximation, permutation, independence, and limiting step to reviewed primary-source theorem passages and conventions.", "non-machine node-specific primary-source crosswalk", "Human-source coverage without machine proof credit."),
    ("X-PROVENANCE", "certificate", "critical", "Inventory terminal bodies, wrappers, imports, axioms, TCB edges, and replay receipts.", "planned machine-derived provenance closure", "Release provenance coverage without proof credit."),
]

oids = [f"{PREFIX}-{suffix}" for suffix, *_ in rows]
checked = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-X-ZERO-ONE", f"{PREFIX}-T-ASSEMBLE"}
source_na = {f"{PREFIX}-S-DEFINITIONS", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-PROVENANCE"}
machine_special = {f"{PREFIX}-X-SOURCE": "not_applicable", f"{PREFIX}-X-PROVENANCE": "informational"}
statement_fp = "lean-expression-sha256:2d9e3cd06b290ffddd906b177c7400dc999028ef45dc0134d845621a4aa7b76c"

obligations = []
nodes = []
for (suffix, kind, risk, claim, target, output), oid in zip(rows, oids):
    machine = machine_special.get(oid, "required")
    fingerprint = statement_fp if suffix in {"ROOT", "S-DEFINITIONS"} else "planned:v1:sha256:" + digest([oid, claim, target, output])
    body = None
    if suffix == "X-ZERO-ONE":
        body = "mathlib:8a178386:ProbabilityTheory.measure_eq_zero_or_one_of_indepSet_self"
    elif suffix == "T-ASSEMBLE":
        body = "local:Stage1_Instances/THM-M-1008/ObligationTree.lean#root_of_selfIndependencePackage"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": body,
    })
    nodes.append({
        "node_id": f"{THEOREM}-{suffix}", "obligation_id": oid, "kind": kind,
        "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-P" if oid == f"{PREFIX}-X-ZERO-ONE" else ("M0-L" if oid in checked else ("M2" if suffix == "ROOT" else "M4")),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "mathlib-self-independence-endpoint" if suffix == "X-ZERO-ONE" else ("local-conditional-composition" if suffix == "T-ASSEMBLE" else "none"),
        "foundation_profile": "lean4-mathlib-measure-theory/classical-policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, simulation, or external computation may close this node",
        "step_budget": 100 if suffix in {"N-CYLINDER", "L-BLOCK-INDEPENDENCE", "L-LIMIT-FACTOR"} else 40,
        "semantic_step_ledger": {"premises": "Only the exact declared proof children and formal context.", "inference": claim, "output": output, "outgoing_use": "Only the declared typed parent may consume this output as proof."},
        "public_readable_target": f"Stage1_Instances/THM-M-1008/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}", "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root closure.",
        "task_ids": [ITEM, "S56-M-1008-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1008/ObligationTree.lean"] if suffix in {"X-ZERO-ONE", "T-ASSEMBLE"} else [],
        "owner": "THM-M-1008 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus bounded anchor audit; finite-coordinate approximation/disjoint permutation/self-independence architecture; eligibility frozen independently of closure.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": oids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": oids, "informational_overlays": [f"{PREFIX}-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M2"},
    "status_boundary": "Scope and denominators only; no Hewitt-Savage proof, source acceptance, audit completion, or theorem completion.",
}


def edge(eid, source, kind, target, reciprocal=None):
    row = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    return row


requires = {
    f"{PREFIX}-ROOT": [f"{PREFIX}-T-ASSEMBLE"],
    f"{PREFIX}-T-ASSEMBLE": [f"{PREFIX}-T-SELF-INDEPENDENCE", f"{PREFIX}-X-ZERO-ONE"],
    f"{PREFIX}-T-SELF-INDEPENDENCE": [f"{PREFIX}-L-LIMIT-FACTOR"],
    f"{PREFIX}-L-LIMIT-FACTOR": [f"{PREFIX}-N-CYLINDER", f"{PREFIX}-C-DISJOINT-BLOCK", f"{PREFIX}-L-IID-REINDEX", f"{PREFIX}-L-SYMMETRY-TRANSFER", f"{PREFIX}-L-BLOCK-INDEPENDENCE"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-DEFS", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-DEFINITIONS"), edge("REF-ROOT-BOUND", f"{PREFIX}-ROOT", "logical_decomposition", f"{PREFIX}-S-BOUNDARY")],
    "provenance": [edge("SRC-APPROX", f"{PREFIX}-N-CYLINDER", "source_map", f"{PREFIX}-X-SOURCE"), edge("SRC-LIMIT", f"{PREFIX}-L-LIMIT-FACTOR", "source_map", f"{PREFIX}-X-SOURCE"), edge("PROV-ROOT", f"{PREFIX}-X-PROVENANCE", "provenance_of", f"{PREFIX}-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUND", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-S-FOUNDATION"), edge("TRUST-PROV", f"{PREFIX}-ROOT", "trusts", f"{PREFIX}-X-PROVENANCE")],
    "documentation": [edge("DOC-ROOT", f"{PREFIX}-S-DEFINITIONS", "documents", f"{PREFIX}-ROOT"), edge("DOC-SOURCE", f"{PREFIX}-X-SOURCE", "documents", f"{PREFIX}-L-LIMIT-FACTOR")],
    "workflow": [edge("FLOW-ASSEMBLE-SELF", f"{PREFIX}-T-ASSEMBLE", "workflow_depends_on", f"{PREFIX}-T-SELF-INDEPENDENCE"), edge("FLOW-SELF-LIMIT", f"{PREFIX}-T-SELF-INDEPENDENCE", "workflow_depends_on", f"{PREFIX}-L-LIMIT-FACTOR"), edge("FLOW-PROV-ASSEMBLE", f"{PREFIX}-X-PROVENANCE", "workflow_depends_on", f"{PREFIX}-T-ASSEMBLE")],
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
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": [f"{PREFIX}-T-SELF-INDEPENDENCE"], "composition_certificates": ["Stage1Instances.THM_M_1008.zeroOne_of_selfIndependence", "Stage1Instances.THM_M_1008.root_of_selfIndependencePackage"], "reason": "Final composition and endpoint are checked, but the finite-coordinate approximation route has not produced the required self-independence package."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": [{"recipe_id": f"VAL-{oid}", "obligation_id": oid, "command": "python3 Stage1_Instances/THM-M-1008/check_obligation_tree.py", "expected_exit": 0, "network_policy": "denied"} for oid in oids]}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

intake_path = HERE / "intake.json"
intake = json.loads(intake_path.read_text())
intake["obligation_registry_hash"] = "sha256:" + denominator
intake["obligation_registry_version"] = 1
intake["obligation_tree_state"] = "self_tested_pending_master_acceptance"
intake["status_boundary"] = "Planned lifecycle with an elaborated exact statement and self-tested obligation freeze pending master acceptance. Root remains H1/M2/R3; no Hewitt-Savage proof, H0 source fidelity, audit completion, or theorem completion is claimed."
intake_path.write_text(json.dumps(intake, indent=2, ensure_ascii=True) + "\n")
print(denominator)
