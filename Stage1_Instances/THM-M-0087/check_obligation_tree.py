#!/usr/bin/env python3
"""Validate the frozen THM-M-0087 obligation and graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0087-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0087"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
          "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 17
assert ids[0] == registry["root_obligation_id"] == "M0087-ROOT"
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
for key, field, value in (
    ("required_machine", "machine_eligibility", "required"),
    ("required_human_source", "human_source_eligibility", "required"),
    ("required_readable", "readable_eligibility", "required"),
):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == value]

required_node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
    "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
    "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
    "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required_node_fields <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
allowed = {"proof_requires", "composes", "logical_decomposition", "provenance_of", "evidence_for",
           "trusts", "documents", "workflow_depends_on"}
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

active, visited = set(), set()
def visit(node):
    assert node not in active
    if node in visited:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    visited.add(node)
visit("M0087-ROOT")
required = {row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"}
assert required <= visited | {"M0087-S-TARGET", "M0087-S-BOUNDARY"}

recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
assert {node["validation_spec_id"] for node in nodes} == recipe_ids
for recipe in specs["recipes"]:
    assert isinstance(recipe["argv"], list) and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0 and recipe["obligation_id"] in recipe["covered_obligation_ids"]
    assert recipe["cwd"] == "." and recipe["env"] == {} and recipe["timeout_seconds"] == 30

boundary = bundle["closure_boundary"]
assert boundary["closed_obligations"] == [] and boundary["root_closed"] is False
assert boundary["theorem_complete"] is False
assert boundary["remaining_root_cut_set"] == ["M0087-B-FULL", "M0087-B-FAITHFUL", "M0087-B-ADJUNCTION", "M0087-B-FINLIM"]

lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_packages" in lean and "#print axioms root_of_packages" in lean
print(f"PASS THM-M-0087 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); four exact conclusion packages remain the root cut set")
