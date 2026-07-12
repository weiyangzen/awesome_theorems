#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1054 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
state = json.loads((HERE / "obligation-tree-state.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == state["item_id"] == "S56-M-1054-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == state["theorem_id"] == "THM-M-1054"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 13
assert ids[0] == registry["root_obligation_id"] == "M1054-ROOT"
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert state["registry_hash"] == "sha256:" + digest
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]
assert registry["frozen_denominators"]["required_human_source"] == [row["obligation_id"] for row in rows if row["human_source_eligibility"] == "required"]

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in all_edges and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        all_edges.add(edge["edge_id"])

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
    assert node not in visiting
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)

visit("M1054-ROOT")
expected = {"M1054-ROOT", "M1054-T-ASSEMBLE", "M1054-B-SUBSINGLETON", "M1054-B-NONTRIVIAL", "M1054-T-FIXED-PROJECTION", "M1054-L-CONTRACTION", "M1054-C-KOOPMAN", "M1054-L-ABSTRACT-MEAN-ERGODIC"}
assert visited == expected
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
for recipe in specs["recipes"]:
    assert recipe["cwd"] == "." and isinstance(recipe["argv"], list)
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert len(recipe["covered_obligation_ids"]) == 1
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M1054-L-ABSTRACT-MEAN-ERGODIC"]
assert state["audit_complete"] is False and state["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_nontrivialMeanErgodicPackage" in lean and "#print axioms" in lean

print(f"PASS THM-M-1054 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); abstract mean-ergodic proof credit remains for the proof phase")
