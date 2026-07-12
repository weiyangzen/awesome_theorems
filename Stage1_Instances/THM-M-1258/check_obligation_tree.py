#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1258 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
load = lambda name: json.loads((HERE / name).read_text())
registry, bundle = load("obligation-registry.json"), load("typed-graphs.json")
assert registry["item_id"] == bundle["item_id"] == "S56-M-1258-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-1258"
digest = lambda name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
assert registry["frozen_against_statement_sha256"] == digest("Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == digest("anchor-audit.json")
rows = registry["obligations"]
ids = registry["frozen_denominators"]["inventory"]
assert ids == [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == len(rows) == 9
projection = [{key: row[key] for key in row} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert {node["obligation_id"] for node in bundle["nodes"]} == set(ids)
for node in bundle["nodes"]:
    assert required <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert len(node["semantic_step_ledger"]) == node["step_budget"]
    assert all({"premises", "inference", "output", "outgoing_use"} <= step.keys() for step in node["semantic_step_ledger"])

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
allowed = {"proof_requires", "composes", "logical_decomposition", "expository_decomposition", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids
        assert edge["from"] in ids and edge["to"] in ids and edge["type"] in allowed
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])
proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
assert bundle["closure_metrics_observed"] is False
assert bundle["root_cut_set"] == ["M1258-L-SPAN"]
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert all(token in lean for token in ("compose_condition", "empty_domain", "zero_dimension", "#print axioms"))
print(f"PASS THM-M-1258 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open; a concrete family and its pointwise span proof remain required")
