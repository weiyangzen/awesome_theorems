#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-1286 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1286-OBLIGATION_TREE"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows, nodes = registry["obligations"], bundle["nodes"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 18 and ids[0] == registry["root_obligation_id"]
projection = [{key: row[key] for key in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert len(nodes) == 18 and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
seen = set()
for graph in bundle["graphs"].values():
    for row in graph["edges"]:
        assert row["edge_id"] not in seen and row["type"] in allowed
        assert row["from"] in ids and row["to"] in ids
        assert row["edge_id"] in graph["out"][row["from"]]
        assert row["edge_id"] in graph["in"][row["to"]]
        seen.add(row["edge_id"])

proof = {row["edge_id"]: row for row in bundle["graphs"]["proof"]["edges"]}
children = {}
for row in proof.values():
    reverse = proof[row["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == row["edge_id"]
    assert (reverse["from"], reverse["to"]) == (row["to"], row["from"])
    assert {row["type"], reverse["type"]} == {"proof_requires", "composes"}
    if row["type"] == "proof_requires":
        children.setdefault(row["from"], []).append(row["to"])

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
visit("M1286-ROOT")
assert visited == {"M1286-ROOT", "M1286-T-ASSEMBLE", "M1286-C-REARRANGE", "M1286-L-GRADIENT"}
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
print(f"PASS THM-M-1286 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M4); rearrangement construction and gradient estimate remain open")
