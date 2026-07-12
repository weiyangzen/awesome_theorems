#!/usr/bin/env python3
"""Validate the THM-M-0981 frozen registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0981-OBLIGATION_TREE"
THEOREM = "THM-M-0981"


def load(name):
    return json.loads((HERE / name).read_text())


registry = load("obligation-registry.json")
bundle = load("typed-graphs.json")
specs = load("validation-specs.json")
assert registry["schema_version"] == "stage1-obligation-registry/1.0"
assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
assert specs["schema_version"] == "stage1-validation-specs/1.0"
assert {registry["item_id"], bundle["item_id"], specs["item_id"]} == {ITEM}
assert {registry["theorem_id"], bundle["theorem_id"], specs["theorem_id"]} == {THEOREM}
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 14
assert registry["root_obligation_id"] == "M0981-ROOT"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
encoded = json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
denominator = hashlib.sha256(encoded).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
for key, field, value in (("required_machine", "machine_eligibility", "required"),
                          ("required_human_source", "human_source_eligibility", "required"),
                          ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == value]
assert registry["frozen_denominators"]["inventory"] == ids

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
                 "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
                 "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
                 "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
                 "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys() and 0 < node["step_budget"] <= 100
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    path, anchor = node["public_readable_target"].split("#", 1)
    assert path == "Stage1_Instances/THM-M-0981/obligation-tree.md" and anchor

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "transports",
           "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for item in graph["edges"]:
        assert item["edge_id"] not in edge_ids and item["type"] in allowed
        assert item["from"] in ids and item["to"] in ids
        assert item["edge_id"] in graph["out"][item["from"]]
        assert item["edge_id"] in graph["in"][item["to"]]
        edge_ids.add(item["edge_id"])

proof = {item["edge_id"]: item for item in bundle["graphs"]["proof"]["edges"]}
children = {}
for item in proof.values():
    reverse = proof[item["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == item["edge_id"]
    assert (reverse["from"], reverse["to"]) == (item["to"], item["from"])
    assert {item["type"], reverse["type"]} == {"proof_requires", "composes"}
    if item["type"] == "proof_requires":
        children.setdefault(item["from"], []).append(item["to"])

active, visited = set(), set()


def visit(node):
    assert node not in active, f"proof cycle at {node}"
    if node in visited:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    visited.add(node)


visit("M0981-ROOT")
assert {"M0981-T-ASSEMBLE", "M0981-B-CLAUSES", "M0981-L-EMPTY", "M0981-L-UNIT", "M0981-L-ADDITIVITY", "M0981-N-INSTANCE"} <= visited

recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
assert len(recipe_ids) == len(ids) and {node["validation_spec_id"] for node in nodes} == recipe_ids
for recipe in specs["recipes"]:
    assert {"recipe_id", "cwd", "argv", "env", "timeout_seconds", "network", "covered_ids", "expected_exit"} <= recipe.keys()
    assert recipe["network"] == "forbidden" and set(recipe["covered_ids"]) <= set(ids)

boundary = bundle["closure_boundary"]
assert boundary["closed_obligations"] == [] and boundary["root_closed"] is False
assert boundary["audit_complete"] is False and boundary["theorem_complete"] is False
assert boundary["remaining_root_cut_set"] == ["M0981-L-EMPTY", "M0981-L-UNIT", "M0981-L-ADDITIVITY"]

lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom ", "sorryAx"):
    assert forbidden not in lean
assert "theorem root_compose" in lean and "#print axioms root_compose" in lean

print(f"PASS THM-M-0981 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root remains open at M1; frozen cut set: L-EMPTY, L-UNIT, L-ADDITIVITY")
