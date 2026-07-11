#!/usr/bin/env python3
"""Build the frozen THM-M-0088 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0088-OBLIGATION_TREE"
THEOREM = "THM-M-0088"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


ROWS = [
    ("M0088-ROOT", "root", "critical", "Construct the exact data-valued FullyFaithful target for the canonical Yoneda functor.", "Stage1Instances.THM_M_0088.YonedaEmbeddingTarget C", "The frozen root."),
    ("M0088-T-CONSTRUCT", "terminal", "critical", "Assemble FullyFaithful from a hom preimage and its two inverse laws.", "Stage1Instances.THM_M_0088.yonedaEmbedding_of_inverseLaws", "An inhabitant of the exact root, conditional on all three fields."),
    ("M0088-C-PREIMAGE", "construction", "high", "For a natural transformation between representables, evaluate it at X on the identity of X.", "fun f => f.app (Opposite.op X) (CategoryStruct.id X)", "A morphism X ⟶ Y for every transformation yoneda.obj X ⟶ yoneda.obj Y."),
    ("M0088-L-RIGHT", "core_lemma", "critical", "Show that mapping the selected preimage by Yoneda recovers the original natural transformation componentwise.", "forall f, yoneda.map (preimage f) = f", "The right-inverse law FullyFaithful.map_preimage."),
    ("M0088-L-LEFT", "core_lemma", "critical", "Show that evaluating yoneda.map f at X and identity X recovers f.", "forall f, preimage (yoneda.map f) = f", "The left-inverse law FullyFaithful.preimage_map."),
    ("M0088-B-NATURALITY", "bridge", "high", "Expose the naturality equation used to determine every component from the identity component.", "CategoryTheory.Yoneda.naturality", "The componentwise equality needed by M0088-L-RIGHT."),
    ("M0088-X-SOURCE", "documentation", "high", "Pinpoint the human Yoneda lemma and fully-faithful corollary at node level, including assumptions and errata.", "non-machine source crosswalk", "Reviewed H evidence without machine proof credit."),
    ("M0088-X-PROVENANCE", "certificate", "critical", "Inventory the terminal mathlib body, transitive declarations, imports, axioms, TCB, and unique body identity.", "machine-derived provenance and trust closure", "Release provenance without proof credit."),
]

statement = json.loads((HERE / "statement.json").read_text())
statement_fp = statement["canonical_formal_target"]["elaborated_expression_sha256"]
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor_audit.json").read_bytes()).hexdigest()
checked = {"M0088-T-CONSTRUCT"}
source_na = {"M0088-X-PROVENANCE"}
machine_special = {"M0088-X-SOURCE": "not_applicable", "M0088-X-PROVENANCE": "informational"}

obligations = []
nodes = []
for oid, kind, risk, claim, target, output in ROWS:
    fp = "lean-expression-sha256:" + statement_fp if oid == "M0088-ROOT" else "planned:v1:sha256:" + digest([oid, kind, claim, target, output])
    machine = machine_special.get(oid, "required")
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fp, "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in source_na else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": {"not_applicable": "human_source_boundary_only", "informational": "release_provenance_overlay_no_proof_credit"}.get(machine),
        "terminal_proof_body_id": "local:Stage1_Instances/THM-M-0088/ObligationTree.lean#yonedaEmbedding_of_inverseLaws" if oid == "M0088-T-CONSTRUCT" else None,
    })
    nodes.append({
        "node_id": "THM-M-0088-" + oid.removeprefix("M0088-"), "obligation_id": oid,
        "kind": kind, "human_statement": claim, "formal_target": target, "output": output,
        "human_debt": "H1", "machine_debt": "M0-L" if oid in checked else ("M3" if oid == "M0088-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "not-applicable" if oid in source_na else "primary-source-node-map-pending",
        "provenance_id": "local-conditional-composition" if oid in checked else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation may close this node",
        "step_budget": 24,
        "semantic_step_ledger": {"premises": "Only the declared typed children and frozen categorical context.", "inference": claim, "output": output, "outgoing_use": "Only a declared typed parent or support edge may consume this output."},
        "public_readable_target": f"Stage1_Instances/THM-M-0088/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional composition only; no imported anchor is credited as root closure here.",
        "task_ids": [ITEM, "S56-M-0088-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0088/ObligationTree.lean"] if oid == "M0088-T-CONSTRUCT" else [],
        "owner": "THM-M-0088 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if oid in checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor audit", "source map", "toolchain"], "revocation_state": "provisional" if oid in checked else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and bounded anchor audit; direct FullyFaithful constructor architecture; eligibility assigned before closure observation.",
    "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0088-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {"inventory": ids, "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"], "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"], "required_readable": ids, "informational_overlays": ["M0088-X-PROVENANCE"]},
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": sorted(checked), "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and conditional constructor only; inverse-law leaves and root remain open in this phase."
}


def edge(eid, source, kind, target, reciprocal=None):
    result = {"edge_id": eid, "from": source, "type": kind, "to": target}
    if reciprocal:
        result["reciprocal_edge_id"] = reciprocal
    return result


requires = {"M0088-ROOT": ["M0088-T-CONSTRUCT"], "M0088-T-CONSTRUCT": ["M0088-C-PREIMAGE", "M0088-L-RIGHT", "M0088-L-LEFT"], "M0088-L-RIGHT": ["M0088-B-NATURALITY", "M0088-C-PREIMAGE"], "M0088-L-LEFT": ["M0088-C-PREIMAGE"]}
proof = []
for parent, children in requires.items():
    for child in children:
        req, comp = "REQ-" + parent + "-" + child, "CMP-" + child + "-" + parent
        proof += [edge(req, parent, "proof_requires", child, comp), edge(comp, child, "composes", parent, req)]

edge_sets = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-FIELDS", "M0088-ROOT", "logical_decomposition", "M0088-T-CONSTRUCT")],
    "provenance": [edge("PROV-ANCHOR", "M0088-X-PROVENANCE", "provenance_of", "M0088-ROOT"), edge("SRC-NAT", "M0088-B-NATURALITY", "source_map", "M0088-X-SOURCE")],
    "evidence": [],
    "trust": [edge("TRUST-ROOT", "M0088-ROOT", "trusts", "M0088-X-PROVENANCE")],
    "documentation": [edge("DOC-SOURCE", "M0088-X-SOURCE", "documents", "M0088-ROOT")],
    "workflow": [edge("FLOW-PROOF", "M0088-T-CONSTRUCT", "workflow_depends_on", "M0088-C-PREIMAGE"), edge("FLOW-PROV", "M0088-X-PROVENANCE", "workflow_depends_on", "M0088-T-CONSTRUCT")],
}
graphs = {}
for name, edges in edge_sets.items():
    incoming, outgoing = {}, {}
    for e in edges:
        outgoing.setdefault(e["from"], []).append(e["edge_id"])
        incoming.setdefault(e["to"], []).append(e["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-0088-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0088-ROOT", "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": sorted(checked), "root_closed": False, "audit_complete": False, "theorem_complete": False, "remaining_root_cut_set": ["M0088-C-PREIMAGE", "M0088-L-RIGHT", "M0088-L-LEFT"], "composition_certificates": ["Stage1Instances.THM_M_0088.yonedaEmbedding_of_inverseLaws"], "reason": "The exact constructor is checked conditionally, but its preimage and inverse-law premises receive no proof credit in this phase."}
}

recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid, "cwd": ".", "argv": ["python3", "Stage1_Instances/THM-M-0088/check_obligation_tree.py"], "env_allowlist": {"PATH": "runner-provided-pinned-toolchain"}, "timeout_seconds": 120, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS and denominator digest"}], "covered_obligation_ids": [oid], "covered_declarations": ["Stage1Instances.THM_M_0088.yonedaEmbedding_of_inverseLaws"] if oid == "M0088-T-CONSTRUCT" else []} for oid, *_ in ROWS]
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
print(denominator)
