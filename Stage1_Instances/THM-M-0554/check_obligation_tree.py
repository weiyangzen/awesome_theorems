#!/usr/bin/env python3
"""Validate the frozen THM-M-0554 registry and typed graph bundle."""

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
assert {registry["item_id"], bundle["item_id"], specs["item_id"]} == {"S56-M-0554-OBLIGATION_TREE"}
assert {registry["theorem_id"], bundle["theorem_id"], specs["theorem_id"]} == {"THM-M-0554"}
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 32
assert registry["root_obligation_id"] == "M0554-ROOT"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{field: row[field] for field in fields} for row in rows]
payload = json.dumps(projection, sort_keys=True, separators=(",", ":"))
denominator = hashlib.sha256(payload.encode()).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
for key, field, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == value]
assert registry["frozen_denominators"]["inventory"] == ids

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}
    if isinstance(node["step_budget"], int):
        assert 0 < node["step_budget"] <= 100
        assert len(node["semantic_step_ledger"]["steps"]) == node["step_budget"]
    else:
        assert node["step_budget"] == "split-required" and node["semantic_step_ledger"]["children"]
    path, anchor = node["public_readable_target"].split("#", 1)
    assert path == "Stage1_Instances/THM-M-0554/obligation-tree.md" and anchor

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
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
    reciprocal = proof[edge["reciprocal_edge_id"]]
    assert reciprocal["reciprocal_edge_id"] == edge["edge_id"]
    assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reciprocal["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])

active, reached = set(), set()
def visit(node):
    assert node not in active, f"proof cycle at {node}"
    if node in reached:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    reached.add(node)

visit("M0554-ROOT")
required_machine = {row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"}
assert required_machine <= reached

recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
assert len(recipe_ids) == len(ids) and {node["validation_spec_id"] for node in nodes} == recipe_ids
for recipe in specs["recipes"]:
    assert set(recipe) >= {"recipe_id", "cwd", "argv", "env", "timeout_seconds", "network", "covered_ids"}
    assert recipe["network"] == "forbidden" and set(recipe["covered_ids"]) <= set(ids)

boundary = bundle["closure_boundary"]
assert boundary["closed_obligations"] == [] and boundary["root_closed"] is False
assert boundary["composition_certificates_checked"] == []
assert boundary["audit_complete"] is False and boundary["theorem_complete"] is False
assert boundary["remaining_root_cut_set"] == ["M0554-X-GENCOH", "M0554-C-EXACT-COUPLE", "M0554-C-E2-MODEL", "M0554-L-STRONG"]
for path in HERE.glob("*.lean"):
    source = path.read_text()
    for forbidden in ("sorry", "admit", "axiom ", "sorryAx"):
        assert forbidden not in source

print(f"PASS THM-M-0554 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root remains open at M4; no composition certificate or proof closure credited")
