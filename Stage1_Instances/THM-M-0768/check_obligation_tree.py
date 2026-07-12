#!/usr/bin/env python3
"""Fail-closed checks for the THM-M-0768 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert reg["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0768-OBLIGATION_TREE"
assert reg["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0768"
assert reg["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert reg["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = reg["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 16 and ids[0] == reg["root_obligation_id"]
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
frozen = [{key: row[key] for key in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(frozen, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert denominator == reg["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert reg["frozen_denominators"]["inventory"] == ids
assert reg["frozen_denominators"]["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for item in graph["edges"]:
        assert item["edge_id"] not in edge_ids and item["type"] in allowed
        assert item["from"] in ids and item["to"] in ids
        assert item["edge_id"] in graph["out"][item["from"]] and item["edge_id"] in graph["in"][item["to"]]
        edge_ids.add(item["edge_id"])
proof = {item["edge_id"]: item for item in bundle["graphs"]["proof"]["edges"]}
children = {}
for item in proof.values():
    reverse = proof[item["reciprocal_edge_id"]]
    assert (reverse["from"], reverse["to"]) == (item["to"], item["from"])
    assert {item["type"], reverse["type"]} == {"proof_requires", "composes"}
    if item["type"] == "proof_requires":
        children.setdefault(item["from"], []).append(item["to"])
visiting = set()
def visit(node):
    assert node not in visiting
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
visit("M0768-ROOT")
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M0768-L-RELATIONAL"]
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_relational_package" in lean and "#print axioms" in lean
print(f"PASS THM-M-0768 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M3); relational bridge remains the minimal root cut")
