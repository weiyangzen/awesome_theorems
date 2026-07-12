#!/usr/bin/env python3
"""Validate the THM-M-0988 frozen registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def load(name): return json.loads((HERE / name).read_text())

registry = load("obligation-registry.json")
bundle = load("typed-graphs.json")
specs = load("validation-specs.json")
assert registry["schema_version"] == "stage1-obligation-registry/1.0"
assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
assert specs["schema_version"] == "stage1-validation-specs/1.0"
assert {registry["item_id"], bundle["item_id"], specs["item_id"]} == {"S56-M-0988-OBLIGATION_TREE"}
assert {registry["theorem_id"], bundle["theorem_id"], specs["theorem_id"]} == {"THM-M-0988"}
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

rows = registry["obligations"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 18 and registry["root_obligation_id"] == "M0988-ROOT"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: r[k] for k in fields} for r in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
for key, field, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == value]

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for n in nodes:
    assert required_node <= n.keys() and 0 < n["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= n["semantic_step_ledger"].keys()
    assert n["human_debt"] in {f"H{i}" for i in range(6)}
    assert n["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert n["readability_debt"] in {f"R{i}" for i in range(5)}
    path, anchor = n["public_readable_target"].split("#", 1)
    assert path == "Stage1_Instances/THM-M-0988/obligation-tree.md" and anchor

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in edge_ids and e["type"] in allowed
        assert e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        edge_ids.add(e["edge_id"])

proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for e in proof.values():
    reverse = proof[e["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == e["edge_id"]
    assert (reverse["from"], reverse["to"]) == (e["to"], e["from"])
    assert {e["type"], reverse["type"]} == {"proof_requires", "composes"}
    if e["type"] == "proof_requires": children.setdefault(e["from"], []).append(e["to"])

active, visited = set(), set()
def visit(node):
    assert node not in active, f"proof cycle at {node}"
    if node in visited: return
    active.add(node)
    for child in children.get(node, []): visit(child)
    active.remove(node); visited.add(node)
visit("M0988-ROOT")
assert {"M0988-T-ASSEMBLE", "M0988-X-PINNED"} <= visited

recipe_ids = {r["recipe_id"] for r in specs["recipes"]}
assert len(recipe_ids) == len(ids) and {n["validation_spec_id"] for n in nodes} == recipe_ids
for recipe in specs["recipes"]:
    assert {"recipe_id", "cwd", "argv", "env", "timeout_seconds", "network", "covered_ids"} <= recipe.keys()
    assert recipe["network"] == "forbidden" and set(recipe["covered_ids"]) <= set(ids)

boundary = bundle["closure_boundary"]
assert boundary["closed_obligations"] == [] and boundary["root_closed"] is False
assert boundary["audit_complete"] is False and boundary["theorem_complete"] is False
assert boundary["remaining_root_cut_set"] == ["M0988-X-PINNED"]
lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom ", "sorryAx"):
    assert forbidden not in lean
assert "root_compose" in lean and "#print axioms root_compose" in lean

print(f"PASS THM-M-0988 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root remains open at M1; frozen cut set: X-PINNED")
