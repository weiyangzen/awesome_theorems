#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-0420 architecture."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0420-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0420"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_statement_record_sha256"] == hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
          "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 16 and ids[0] == registry["root_obligation_id"] == "M0420-ROOT"
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
for key in ("inventory", "required_machine", "required_human_source", "required_readable"):
    assert registry["frozen_denominators"][key] == ids
assert all(row["root_relevant"] and row["machine_eligibility"] == "required" for row in rows)

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
            "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
            "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
            "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
            "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == 16 and {node["obligation_id"] for node in nodes} == set(ids)
recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
for node in nodes:
    assert required <= node.keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}
    assert node["semantic_step_ledger"]
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100
    assert node["validation_spec_id"] in recipe_ids
assert all(recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0 for recipe in specs["recipes"])

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
allowed = {"proof_requires", "composes", "logical_decomposition", "provenance_of", "documents", "trusts", "workflow_depends_on"}
edge_ids, proof_children = set(), {}
for graph in bundle["graphs"].values():
    local_ids = {edge["edge_id"] for edge in graph["edges"]}
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        edge_ids.add(edge["edge_id"])
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        if edge["type"] == "proof_requires":
            proof_children.setdefault(edge["from"], []).append(edge["to"])
            assert edge["reciprocal_edge_id"] in local_ids
            reverse = next(x for x in graph["edges"] if x["edge_id"] == edge["reciprocal_edge_id"])
            assert reverse["type"] == "composes"
            assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])

seen, active = set(), set()
def visit(node):
    assert node not in active
    if node in seen:
        return
    active.add(node)
    for child in proof_children.get(node, []):
        visit(child)
    active.remove(node)
    seen.add(node)

visit("M0420-ROOT")
assert {"M0420-T", "M0420-C", "M0420-L1", "M0420-L2", "M0420-L3", "M0420-L4", "M0420-X1"} <= seen
closure = bundle["closure_boundary"]
assert closure["closed_obligations"] == ["M0420-S1", "M0420-S2", "M0420-T"]
assert closure["root_closed"] is False and closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == ["M0420-C", "M0420-L1", "M0420-L2", "M0420-L3", "M0420-L4"]

print(f"PASS THM-M-0420 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); construction and four substantive property obligations remain M4")
