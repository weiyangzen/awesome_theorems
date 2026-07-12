#!/usr/bin/env python3
"""Validate the THM-M-1228 frozen registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text())


registry = load("obligation-registry.json")
bundle = load("typed-graphs.json")
specs = load("validation-specs.json")
assert registry["schema_version"] == "stage1-obligation-registry/1.0"
assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
assert specs["schema_version"] == "stage1-validation-specs/1.0"
assert {registry["item_id"], bundle["item_id"], specs["item_id"]} == {"S56-M-1228-OBLIGATION_TREE"}
assert {registry["theorem_id"], bundle["theorem_id"], specs["theorem_id"]} == {"THM-M-1228"}
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 15
assert registry["root_obligation_id"] == "M1228-ROOT"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
for key, field, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == value]
assert registry["frozen_denominators"]["inventory"] == ids

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
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
    assert node not in active, f"proof cycle at {node}"
    if node in visited:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    visited.add(node)
visit("M1228-ROOT")
for required in ("M1228-T-ASSEMBLE", "M1228-E-EPSILON", "M1228-D-DECAY", "M1228-C-COVER", "M1228-L-MEASURE", "M1228-G-PARABOLIC"):
    assert required in visited

recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
assert len(recipe_ids) == len(ids) and {n["validation_spec_id"] for n in nodes} == recipe_ids
for recipe in specs["recipes"]:
    assert set(recipe) >= {"recipe_id", "cwd", "argv", "env", "timeout_seconds", "network", "covered_ids"}
    assert recipe["network"] == "forbidden" and set(recipe["covered_ids"]) <= set(ids)

boundary = bundle["closure_boundary"]
assert boundary["closed_obligations"] == [] and boundary["root_closed"] is False
assert boundary["root_machine_debt"] == "M4"
assert boundary["audit_complete"] is False and boundary["theorem_complete"] is False
assert boundary["remaining_root_cut_set"] == ["M1228-S-CONCRETE", "M1228-E-EPSILON", "M1228-C-COVER", "M1228-L-MEASURE"]
lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom ", "sorryAx"):
    assert forbidden not in lean
assert "root_compose" in lean and "#print axioms root_compose" in lean
statement_lean = (HERE / "Statement.lean").read_text()
for token in ("SpaceTime", "SolutionData", "IsSuitableWeakSolution", "RegularAt", "ParabolicHausdorffOneMeasureZero", "SingularSet"):
    assert token in lean and token in statement_lean

print(f"PASS THM-M-1228 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root remains open at M4; frozen analytic cut set has four obligations")
