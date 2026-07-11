#!/usr/bin/env python3
"""Fail-closed structural check for the THM-M-0395 architecture freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == "S56-M-0395-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-0395"
assert specs["theorem_id"] == "THM-M-0395"
assert registry["frozen_against_statement_sha256"] == "de1bfb399ccec48a224e867c55f6eab12589e458949d6d409260be65f0920ba6"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 17 and ids[0] == registry["root_obligation_id"]
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
for key in ("inventory", "required_machine", "required_human_source", "required_readable"):
    assert registry["frozen_denominators"][key] == ids

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
    "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
    "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
    "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == 17 and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}
    assert node["semantic_step_ledger"] and (node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100)
recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
assert {node["validation_spec_id"] for node in nodes} == recipe_ids
assert all(recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0 for recipe in specs["recipes"])

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids, proof_children = set(), {}
for name, graph in bundle["graphs"].items():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["from"] in ids and edge["to"] in ids
        edge_ids.add(edge["edge_id"])
        assert edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]]
        if edge["type"] == "proof_requires":
            proof_children.setdefault(edge["from"], []).append(edge["to"])
            reverse = next(x for x in graph["edges"] if x["edge_id"] == edge["reciprocal_edge_id"])
            assert reverse["type"] == "composes" and (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])

seen, active = set(), set()
def visit(node):
    assert node not in active
    if node in seen: return
    active.add(node)
    for child in proof_children.get(node, []): visit(child)
    active.remove(node); seen.add(node)
visit("M0395-ROOT")
assert {"M0395-T", "M0395-N1", "M0395-C2", "M0395-X1", "M0395-L2"} <= seen
assert bundle["closure_boundary"]["closed_obligations"] == ["M0395-S3"]
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M0395-T"]

print(f"PASS THM-M-0395 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M4); only the statement transport M0395-S3 is checked")
