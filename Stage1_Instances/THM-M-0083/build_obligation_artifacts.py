#!/usr/bin/env python3
"""Build THM-M-0083's frozen obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0083-OBLIGATION_TREE"
THEOREM = "THM-M-0083"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# This architecture and its eligibility are fixed independently of the closure labels below.
ROWS = [
    ("M0083-ROOT", "root", "critical", "The exact frozen universal-element criterion is equivalent to representability.", "Stage1Instances.THM_M_0083.RepresentableFunctorTarget F", "The canonical proposition."),
    ("M0083-S-DEFINITIONS", "definition", "high", "Fix presheaf variance, opposite morphisms, evaluation, bijectivity, and mathlib's IsRepresentable/IsRepresentedBy predicates.", "Stage1Instances.THM_M_0083.UniversalElementCriterion F", "The exact statement interface."),
    ("M0083-S-BOUNDARY", "branch", "high", "Preserve empty categories and avoid an undeclared nonemptiness premise.", "Stage1Instances.THM_M_0083.empty_category_boundary", "Both sides are false for the empty category."),
    ("M0083-S-FOUNDATION", "certificate", "critical", "Record classical choice, propositional extensionality, quotient soundness, kernel, dependency, and no-oracle boundaries.", "planned transitive foundation and TCB report", "An accepted trust boundary."),
    ("M0083-N-REPRESENTED", "normalization", "critical", "Expand IsRepresentedBy x to bijectivity of f |-> F.map f.op x for every test object.", "CategoryTheory.Functor.isRepresentedBy_iff", "Equivalence between a universal element and IsRepresentedBy."),
    ("M0083-L-EXISTS", "core_lemma", "critical", "Relate representability to the existence of an object and a representing element.", "CategoryTheory.Functor.IsRepresentable.iff_exists_isRepresentedBy", "The existential representation criterion."),
    ("M0083-B-FORWARD", "branch", "critical", "Convert a universal element into a representation witness and hence representability.", "Stage1Instances.THM_M_0083.forwardPackage_mathlib F", "UniversalElementCriterion F -> F.IsRepresentable."),
    ("M0083-B-REVERSE", "branch", "critical", "Extract a representing object and element and recover bijectivity for every test object.", "Stage1Instances.THM_M_0083.reversePackage_mathlib F", "F.IsRepresentable -> UniversalElementCriterion F."),
    ("M0083-T-ASSEMBLE", "terminal", "critical", "Consume both directed packages to construct the exact iff root.", "Stage1Instances.THM_M_0083.root_of_direction_packages F", "The exact canonical root from both directions."),
    ("M0083-X-SOURCE", "terminal", "high", "Map definitions and both directions to pinpoint primary human-source passages and assumptions.", "non-machine node-specific source crosswalk", "Human-source coverage only."),
    ("M0083-X-PROVENANCE", "certificate", "critical", "Trace wrappers to unique mathlib bodies, imports, axioms, dependency closure, and replay receipts.", "planned transitive provenance closure", "Release provenance without proof credit."),
]

statement = json.loads((HERE / "statement.json").read_text())
statement_fp = statement["canonical_formal_target"]["elaborated_expression_sha256"]
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
closed = {"M0083-S-DEFINITIONS", "M0083-S-BOUNDARY", "M0083-N-REPRESENTED", "M0083-L-EXISTS", "M0083-B-FORWARD", "M0083-B-REVERSE", "M0083-T-ASSEMBLE", "M0083-ROOT"}
local = {"M0083-S-DEFINITIONS", "M0083-S-BOUNDARY", "M0083-T-ASSEMBLE"}
wrapped = closed - local
source_na = {"M0083-S-DEFINITIONS", "M0083-S-BOUNDARY", "M0083-S-FOUNDATION", "M0083-X-PROVENANCE"}
machine_special = {"M0083-X-SOURCE": "not_applicable", "M0083-X-PROVENANCE": "informational"}

obligations, nodes = [], []
for oid, kind, risk, claim, target, output in ROWS:
    fp = "lean-expression-sha256:" + statement_fp if oid == "M0083-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    body = None
    if oid in local:
        body = "local:Stage1_Instances/THM-M-0083/" + ("Statement.lean" if oid != "M0083-T-ASSEMBLE" else "ObligationTree.lean")
    elif oid in wrapped:
        body = "pinned-mathlib:Mathlib/CategoryTheory/RepresentedBy.lean"
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": body,
    })
    debt = "M0-L" if oid in local else ("M0-W" if oid in wrapped else "M4")
    nodes.append({
        "node_id": "THM-M-0083-" + oid.removeprefix("M0083-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": debt, "readability_debt": "R4",
        "evidence_ids": [], "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "anchor-audit:M0083-C01" if oid in wrapped else ("repo-local-body" if oid in local else "none"),
        "foundation_profile": "lean4-mathlib-classical/propext-choice-quot-pending-acceptance",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, solver, native_decide, or external computation is credited",
        "step_budget": 40,
        "semantic_step_ledger": {"premises": "Only the exact typed proof children and frozen categorical context.", "inference": claim, "output": output, "outgoing_use": "Only declared typed proof or non-proof support edges may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0083/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "This node records architecture or scoped kernel evidence; it does not accept source, readability, provenance, trust, reproducibility, or theorem-release gates.",
        "task_ids": [ITEM, "S56-M-0083-PROOF"],
        "owned_sources": (["Stage1_Instances/THM-M-0083/ObligationTree.lean"] if oid in {"M0083-B-FORWARD", "M0083-B-REVERSE", "M0083-T-ASSEMBLE", "M0083-ROOT"} else []),
        "owner": "THM-M-0083 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in closed else None, "review_due": "before master acceptance", "invalidation_inputs": ["statement", "registry", "mathlib revision", "foundation/TCB profile"], "revocation_state": "provisional" if oid in closed else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Frozen exact expression and bounded anchor inventory; two-direction universal-element architecture; eligibility assigned independently of observed closure.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0083-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0083-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new version with an append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(closed), "root_machine_debt": "M0-W", "master_accepted": False},
    "status_boundary": "The denominator and graph are frozen. Candidate kernel closure does not close source, readability, transitive provenance/trust, replay, independent verification, or release gates."
}


def edge(eid, source, kind, target, reciprocal=None):
    value = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {"M0083-ROOT": ["M0083-T-ASSEMBLE"], "M0083-T-ASSEMBLE": ["M0083-B-FORWARD", "M0083-B-REVERSE"], "M0083-B-FORWARD": ["M0083-S-DEFINITIONS", "M0083-N-REPRESENTED", "M0083-L-EXISTS"], "M0083-B-REVERSE": ["M0083-S-DEFINITIONS", "M0083-N-REPRESENTED", "M0083-L-EXISTS"]}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof.extend([edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)])

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-BOUNDARY", "M0083-ROOT", "logical_decomposition", "M0083-S-BOUNDARY")],
    "provenance": [edge("SRC-DEFINITIONS", "M0083-S-DEFINITIONS", "source_map", "M0083-X-SOURCE"), edge("PROV-REPRESENTED", "M0083-X-PROVENANCE", "provenance_of", "M0083-N-REPRESENTED"), edge("PROV-EXISTS", "M0083-X-PROVENANCE", "provenance_of", "M0083-L-EXISTS"), edge("PROV-ROOT", "M0083-X-PROVENANCE", "provenance_of", "M0083-ROOT")],
    "evidence": [],
    "trust": [edge("TRUST-FOUNDATION", "M0083-ROOT", "trusts", "M0083-S-FOUNDATION"), edge("TRUST-PROVENANCE", "M0083-ROOT", "trusts", "M0083-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE-ROOT", "M0083-X-SOURCE", "documents", "M0083-ROOT"), edge("DOC-BOUNDARY", "M0083-S-BOUNDARY", "documents", "M0083-ROOT")],
    "workflow": [edge("FLOW-ASSEMBLE-FORWARD", "M0083-T-ASSEMBLE", "workflow_depends_on", "M0083-B-FORWARD"), edge("FLOW-ASSEMBLE-REVERSE", "M0083-T-ASSEMBLE", "workflow_depends_on", "M0083-B-REVERSE"), edge("FLOW-PROVENANCE-ASSEMBLE", "M0083-X-PROVENANCE", "workflow_depends_on", "M0083-T-ASSEMBLE")],
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
    "registry_id": "THM-M-0083-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0083-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"candidate_closed_obligations": sorted(closed), "root_kernel_checked": True, "root_master_accepted": False, "audit_complete": False, "theorem_complete": False, "remaining_release_cut_set": ["M0083-S-FOUNDATION", "M0083-X-SOURCE", "M0083-X-PROVENANCE"], "composition_certificates": ["Stage1Instances.THM_M_0083.root_of_direction_packages", "Stage1Instances.THM_M_0083.representableFunctorTarget_mathlib"], "reason": "The exact root and both directions elaborate, but later source, readability, provenance/trust, reproducibility, independent-verification, and release gates remain open."}
}

recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0083/check_obligation_tree.py"], "env_allowlist": {"PATH": "runner-provided-pinned-toolchain"}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS and denominator digest"}], "covered_obligation_ids": [oid], "covered_declarations": (["Stage1Instances.THM_M_0083.representableFunctorTarget_mathlib"] if oid == "M0083-ROOT" else [])} for oid, *_ in ROWS]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
