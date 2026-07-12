#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-1088 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
recipes = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == recipes["item_id"] == "S56-M-1088-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == recipes["theorem_id"] == "THM-M-1088"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.md").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 19
assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == "M1088-ROOT"
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
for field, key, value in (("machine_eligibility", "required_machine", "required"), ("human_source_eligibility", "required_human_source", "required"), ("readable_eligibility", "required_readable", "required")):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == value]

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}

expected_graphs = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
assert set(bundle["graphs"]) == expected_graphs
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])

proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])

visiting, visited = set(), set()
def visit(node):
    assert node not in visiting, f"proof cycle at {node}"
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)
visit("M1088-ROOT")
proof_required = {row["obligation_id"] for row in rows if row["machine_eligibility"] == "required" and row["obligation_id"] != "M1088-S-FOUNDATION"}
assert proof_required <= visited

recipe_ids = {recipe["recipe_id"] for recipe in recipes["recipes"]}
assert {node["validation_spec_id"] for node in nodes} == recipe_ids
for recipe in recipes["recipes"]:
    assert {"cwd", "argv", "env", "timeout_seconds", "network_policy", "covered_ids"} <= recipe.keys()
    assert recipe["network_policy"] == "denied" and recipe["covered_ids"]

assert bundle["closure_boundary"]["closed_obligations"] == []
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M1088-T-ENGINE"]
for name in ("Statement.lean", "ObligationTree.lean"):
    source = (HERE / name).read_text()
    assert all(token not in source for token in ("sorry", "admit", "axiom ", "sorryAx"))

print(f"PASS THM-M-1088 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); exact upper-tail engine remains M4")
