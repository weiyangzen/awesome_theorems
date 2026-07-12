#!/usr/bin/env python3
"""Fail-closed structural check for the THM-M-1270 obligation tree."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1270-OBLIGATION_TREE"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in registry["obligations"]]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
ids = [row["obligation_id"] for row in registry["obligations"]]
assert len(ids) == len(set(ids)) == 17 and registry["frozen_denominators"]["inventory"] == ids
assert set(registry["frozen_denominators"]["required_machine"]) == {r["obligation_id"] for r in registry["obligations"] if r["machine_eligibility"] == "required"}
nodes = bundle["nodes"]
assert {n["obligation_id"] for n in nodes} == set(ids)
required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
for node in nodes:
    assert required_node <= set(node) and 0 < node["step_budget"] <= 100
    assert set(node["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"}
    path, anchor = node["public_readable_target"].split("#", 1)
    assert path == "Stage1_Instances/THM-M-1270/obligation-tree.md" and anchor
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])
proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"] and (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires": children.setdefault(edge["from"], []).append(edge["to"])
active, visited = set(), set()
def visit(node):
    assert node not in active, f"proof cycle at {node}"
    if node in visited: return
    active.add(node)
    for child in children.get(node, []): visit(child)
    active.remove(node); visited.add(node)
visit("M1270-ROOT")
for required in ("M1270-C-SEQUENCE", "M1270-C-INVARIANTS", "M1270-L-CAUCHY", "M1270-L-LIMIT", "M1270-L-LOCALIZE", "M1270-L-MAXIMAL", "M1270-T-ASSEMBLE"):
    assert required in visited
recipe_ids = {r["recipe_id"] for r in specs["recipes"]}
assert len(recipe_ids) == len(ids) and {n["validation_spec_id"] for n in nodes} == recipe_ids
for recipe in specs["recipes"]:
    assert set(recipe) >= {"recipe_id", "cwd", "argv", "env", "timeout_seconds", "network", "covered_ids"}
    assert recipe["network"] == "forbidden" and set(recipe["covered_ids"]) <= set(ids)
boundary = bundle["closure_boundary"]
assert boundary["closed_obligations"] == [] and boundary["root_closed"] is False
assert boundary["audit_complete"] is False and boundary["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom ", "sorryAx"):
    assert forbidden not in lean
assert "root_compose" in lean and "#print axioms" in lean
print(f"PASS THM-M-1270 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root remains open at M3; six hard-core obligations form the frozen cut set")
