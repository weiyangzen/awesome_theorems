#!/usr/bin/env python3
"""Validate the THM-M-1188 frozen obligation registry and typed graphs."""

import hashlib
import json
import subprocess
import tempfile
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
assert {registry["item_id"], bundle["item_id"], specs["item_id"]} == {"S56-M-1188-OBLIGATION_TREE"}
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 17
assert registry["root_obligation_id"] == bundle["root_node_id"] == "M1188-ROOT"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
for key, field, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == value]

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = {}
for graph in bundle["graphs"].values():
    assert set(graph["out"]) == set(ids) and set(graph["in"]) == set(ids)
    for edge in graph["edges"]:
        assert edge["edge_id"] not in all_edges and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        all_edges[edge["edge_id"]] = edge

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


visit("M1188-ROOT")
for oid in ("M1188-T-ENGINE", "M1188-C-COMPACT", "M1188-L-SPATIAL", "M1188-L-TEMPORAL", "M1188-L-EPSILON", "M1188-T-ASSEMBLE"):
    assert oid in visited

recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
assert len(recipe_ids) == len(ids) and {node["validation_spec_id"] for node in nodes} == recipe_ids
for recipe in specs["recipes"]:
    assert set(recipe) >= {"recipe_id", "cwd", "argv", "env", "timeout_seconds", "network", "covered_ids"}
    assert recipe["network"] == "forbidden" and set(recipe["covered_ids"]) <= set(ids)

boundary = bundle["closure_boundary"]
assert boundary["closed_obligations"] == [] and boundary["root_closed"] is False
assert boundary["audit_complete"] is False and boundary["theorem_complete"] is False
assert set(boundary["remaining_root_cut_set"]) == {"M1188-C-COMPACT", "M1188-L-ATTAIN", "M1188-C-PERTURB", "M1188-L-SPATIAL", "M1188-L-TEMPORAL", "M1188-B-INTERIOR", "M1188-N-BOUNDARY", "M1188-L-EPSILON"}

lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom ", "sorryAx"):
    assert forbidden not in lean
assert "root_compose" in lean and "#print axioms root_compose" in lean

# Compile both source surfaces in one environment and require definitional
# identity, rather than trusting duplicated prose or declaration names.
statement = (HERE / "Statement.lean").read_text()
combined = statement + "\n" + lean.replace("import Mathlib.Analysis.InnerProductSpace.Laplacian\n", "", 1)
combined += """
example : Stage1Instances.THM_M_1188.HeatEquationWeakMaximumPrincipleTarget ↔
    Stage1Instances.THM_M_1188.ObligationTree.Root := Iff.rfl
"""
lean_dir = HERE.parents[1] / "Formalizations" / "Lean"
with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=HERE, delete=False) as handle:
    handle.write(combined)
    temporary = Path(handle.name)
try:
    checked = subprocess.run(
        ["lake", "env", "lean", str(temporary)], cwd=lean_dir,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120,
    )
finally:
    temporary.unlink()
assert checked.returncode == 0, checked.stdout
print(f"PASS THM-M-1188 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("canonical statement and obligation Root are definitionally identical")
print("root remains open at M3; eight-node analytic cut set is frozen")
