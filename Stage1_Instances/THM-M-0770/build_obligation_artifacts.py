#!/usr/bin/env python3
"""Deterministically build the THM-M-0770 obligation registry and graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def planned(text):
    return "planned:v1:sha256:" + sha(text)


ROOT_FP = "lean-expression-sha256:e4f371f43c1ebee6f62e093d1102857b339c6e4bf70778ea18b1877fa43631fc"
rows = [
    ("M0770-ROOT", "root", "required", "required", "required", "critical", None, ROOT_FP),
    ("M0770-S-DEFINITIONS", "definition", "required", "not_applicable", "required", "high", None, ROOT_FP),
    ("M0770-S-DOMAINS", "terminal", "required", "not_applicable", "required", "high", None, planned("partial order, nonempty carrier, nonempty-chain boundedness")),
    ("M0770-S-BOUNDARY", "terminal", "required", "not_applicable", "required", "high", None, planned("empty carrier rejected; maximal not greatest; empty chain excluded")),
    ("M0770-S-TRANSPORT", "transport", "required", "not_applicable", "required", "critical", None, planned("AuditedAnchorTarget iff ZornsLemmaTarget")),
    ("M0770-S-FOUNDATION", "certificate", "required", "not_applicable", "required", "critical", None, planned("propext Classical.choice Quot.sound; no oracle")),
    ("M0770-N-NONE", "normalization", "not_applicable", "not_applicable", "required", "low", "canonical_order_form_has_no_normalization", planned("normalization layer not applicable")),
    ("M0770-B-NONE", "branch", "not_applicable", "not_applicable", "required", "low", "single_anchor_route_has_no_case_split", planned("branch layer not applicable")),
    ("M0770-C-NONE", "construction", "not_applicable", "not_applicable", "required", "low", "construction_is_inside_audited_upstream_bridge", planned("construction layer externalized")),
    ("M0770-L-ZORN-ANCHOR", "lemma", "required", "required", "required", "critical", None, planned("pinned zorn_le_nonempty exact specialized type")),
    ("M0770-T-ASSEMBLE", "transport", "required", "required", "required", "critical", None, planned("abstract exact anchor implies canonical root")),
    ("M0770-X-SOURCE", "terminal", "not_applicable", "required", "required", "high", "human_source_boundary_only", planned("primary source pinpoint and node map")),
    ("M0770-X-PROVENANCE", "certificate", "informational", "not_applicable", "required", "critical", "release_provenance_overlay_no_proof_credit", planned("terminal body provenance and transitive trust")),
]
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
obligations = []
for oid, kind, machine, human, readable, risk, reason, fp in rows:
    obligations.append(dict(zip(fields, (oid, fp, kind, True, machine, human, readable, risk, reason, None))))
obligations[10]["terminal_proof_body_id"] = "local:Stage1_Instances/THM-M-0770/ObligationTree.lean#root_of_audited_anchor"
projection = [{k: row[k] for k in fields} for row in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")))
ids = [row[0] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0770-OBLIGATION_TREE",
    "theorem_id": "THM-M-0770", "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and immutable anchor audit; eligibility fixed before downstream proof acceptance.",
    "frozen_against_statement_sha256": sha((HERE / "Statement.lean").read_bytes()),
    "frozen_against_anchor_audit_sha256": sha((HERE / "anchor-audit.json").read_bytes()),
    "root_obligation_id": "M0770-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r[0] for r in rows if r[2] == "required"],
        "required_human_source": [r[0] for r in rows if r[3] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0770-X-PROVENANCE"],
    },
    "delta_policy": "Any split, merge, exclusion, eligibility, statement, or anchor change creates a new version and append-only delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M0770-S-DEFINITIONS", "M0770-S-DOMAINS", "M0770-S-BOUNDARY", "M0770-S-TRANSPORT"], "root_machine_debt": "M3"},
    "status_boundary": "Frozen scope and graph denominator only; anchor proof credit, H0, M0, R0, and theorem completion remain downstream.",
}

descriptions = {
    "M0770-ROOT": ("The exact nonempty-poset formulation of Zorn's lemma.", "Stage1Instances.THM_M_0770.ZornsLemmaTarget", "The canonical proposition."),
    "M0770-S-DEFINITIONS": ("Fix chains, boundedness, and order-theoretic maximality.", "Stage1Instances.THM_M_0770.ZornsLemmaTarget", "Exact statement vocabulary."),
    "M0770-S-DOMAINS": ("Fix universe, PartialOrder, Nonempty, and nonempty-chain quantifier scopes.", "binder interface of ZornsLemmaTarget", "Exact domain interface."),
    "M0770-S-BOUNDARY": ("Exclude the empty carrier and distinguish maximal from greatest and nonempty from empty chains.", "mutationAllowsEmptyCarrier_is_false; isMax_iff_no_strictly_larger", "Checked boundary contract."),
    "M0770-S-TRANSPORT": ("Transport bidirectionally between the audited bridge shape and canonical target.", "ObligationTree.{root_of_audited_anchor,audited_anchor_of_root}", "Exact identity transport."),
    "M0770-S-FOUNDATION": ("Audit classical choice and the transitive kernel trust boundary.", "#print axioms zorn_le_nonempty and accepted wrapper", "Accepted axiom and TCB report."),
    "M0770-N-NONE": ("Record that the canonical order formulation needs no normalization.", "not applicable by frozen exclusion", "Reviewed exclusion only."),
    "M0770-B-NONE": ("Record that the selected wrapper route introduces no project-level case split.", "not applicable by frozen exclusion", "Reviewed exclusion only."),
    "M0770-C-NONE": ("Expose that the maximal-chain construction remains inside the upstream bridge.", "Mathlib.Order.Zorn.exists_maximal_of_nonempty_chains_bounded", "No duplicate local construction."),
    "M0770-L-ZORN-ANCHOR": ("Supply the exact result via pinned mathlib zorn_le_nonempty specialized to PartialOrder.", "@zorn_le_nonempty specialized to PartialOrder", "AuditedAnchorTarget."),
    "M0770-T-ASSEMBLE": ("Consume the exact anchor conclusion and yield the canonical target.", "ObligationTree.root_of_audited_anchor", "ZornsLemmaTarget."),
    "M0770-X-SOURCE": ("Map the root and bridge to a reviewed primary human source.", "planned primary-source node crosswalk", "H0 source packet."),
    "M0770-X-PROVENANCE": ("Bind the wrapper, upstream body, max-chain body, revisions, and evidence.", "planned transitive declaration graph", "Release provenance packet."),
}
nodes = []
for oid, kind, machine, human, readable, risk, reason, fp in rows:
    hs, formal, output = descriptions[oid]
    debt = "M0-L" if oid in {"M0770-S-DEFINITIONS", "M0770-S-DOMAINS", "M0770-S-BOUNDARY", "M0770-S-TRANSPORT"} else ("M3" if oid in {"M0770-ROOT", "M0770-L-ZORN-ANCHOR", "M0770-T-ASSEMBLE"} else "M4")
    nodes.append({
        "node_id": "THM-M-0770-" + oid.removeprefix("M0770-"), "obligation_id": oid, "kind": kind,
        "human_statement": hs, "formal_target": formal, "output": output,
        "human_debt": "H1", "machine_debt": debt, "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk" if human == "required" else "not-applicable",
        "provenance_id": "anchor-audit:S56-M-0770-C02" if oid in {"M0770-L-ZORN-ANCHOR", "M0770-T-ASSEMBLE"} else "none",
        "foundation_profile": "lean4-mathlib-classical/choice-expected", "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-release-audit-pending",
        "computation_record": "none; no external computation or oracle", "step_budget": 20,
        "semantic_step_ledger": {"premises": "Only typed proof children and the frozen formal context.", "inference": hs, "output": output, "outgoing_use": "Only declared typed edges may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0770/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture/interface only; no downstream proof or release acceptance is implied.",
        "task_ids": ["S56-M-0770-OBLIGATION_TREE", "S56-M-0770-PROOF"], "owned_sources": [],
        "owner": "THM-M-0770 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if debt == "M0-L" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "anchor", "toolchain"], "revocation_state": "provisional" if debt == "M0-L" else "open"},
    })

def graph(edges):
    out = {i: [] for i in ids}; incoming = {i: [] for i in ids}
    packed = []
    for eid, typ, source, target, reciprocal in edges:
        e = {"edge_id": eid, "type": typ, "from": source, "to": target}
        if reciprocal: e["reciprocal_edge_id"] = reciprocal
        packed.append(e); out[source].append(eid); incoming[target].append(eid)
    return {"edges": packed, "out": out, "in": incoming}

proof_pairs = [("P1", "M0770-ROOT", "M0770-T-ASSEMBLE"), ("P2", "M0770-T-ASSEMBLE", "M0770-S-TRANSPORT"), ("P3", "M0770-T-ASSEMBLE", "M0770-L-ZORN-ANCHOR")]
proof_edges = []
for eid, parent, child in proof_pairs:
    proof_edges += [(eid + "R", "proof_requires", parent, child, eid + "C"), (eid + "C", "composes", child, parent, eid + "R")]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([("R" + str(i), "logical_decomposition", "M0770-ROOT", x, None) for i, x in enumerate(("M0770-S-DEFINITIONS", "M0770-S-DOMAINS", "M0770-S-BOUNDARY", "M0770-N-NONE", "M0770-B-NONE", "M0770-C-NONE"), 1)]),
    "provenance": graph([("PV1", "provenance_of", "M0770-X-PROVENANCE", "M0770-L-ZORN-ANCHOR", None)]),
    "evidence": graph([]),
    "trust": graph([("TR1", "trusts", "M0770-ROOT", "M0770-S-FOUNDATION", None)]),
    "documentation": graph([("D1", "documents", "M0770-X-SOURCE", "M0770-ROOT", None)]),
    "workflow": graph([("W1", "workflow_depends_on", "M0770-T-ASSEMBLE", "M0770-L-ZORN-ANCHOR", None), ("W2", "workflow_depends_on", "M0770-ROOT", "M0770-T-ASSEMBLE", None)]),
}
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": registry["item_id"], "theorem_id": registry["theorem_id"],
    "registry_id": "THM-M-0770-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M0770-ROOT", "edge_direction": "Proof requirements run parent to child; composes edges are reciprocal child to parent.",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_debt": "M3", "theorem_complete": False, "first_open_proof_cut": ["M0770-L-ZORN-ANCHOR"], "reason": "Audited candidate is not accepted proof-node evidence in this phase."},
}
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": registry["item_id"], "theorem_id": registry["theorem_id"], "recipes": [{"recipe_id": "VAL-" + oid, "command": "python3 Stage1_Instances/THM-M-0770/check_obligation_tree.py", "expected": "exit 0 and exact registry/graph/Lean interface validation"} for oid in ids]}
for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n")
print(denominator)
