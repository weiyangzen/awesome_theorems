#!/usr/bin/env python3
"""Fail-closed structural and Lean validation of the THM-M-1133 freeze."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
intake = json.loads((HERE / "intake.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1133-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-1133"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 16
assert ids[0] == registry["root_obligation_id"] == "M1133-ROOT"
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert intake["obligation_registry_hash"] == "sha256:" + digest
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in all_edges and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        all_edges.add(edge["edge_id"])

proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])

visiting, visited = set(), set()
def visit(node):
    assert node not in visiting
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)

visit("M1133-ROOT")
expected = {"M1133-ROOT", "M1133-T-ASSEMBLE", "M1133-T-LIMIT", "M1133-N-PERTURB", "M1133-T-STRICT", "M1133-L-EXTREMUM", "M1133-S-BOUNDARY", "M1133-B-LOCATION", "M1133-L-SPATIAL", "M1133-B-TIME", "M1133-L-TIME"}
assert visited == expected
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
assert all(recipe["network_policy"] == "denied" and recipe["covered_obligation_ids"] for recipe in specs["recipes"])
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M1133-T-LIMIT"]

lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_subsolutionMaximumPrinciple" in lean and "#print axioms" in lean

# The target path is not a Lean module name because it contains a hyphen.
# Concatenate the exact sources after their imports into a temporary file, then
# elaborate without generating an olean or touching the pinned Lake artifacts.
def without_imports(source: str) -> str:
    return "\n".join(line for line in source.splitlines() if not line.startswith("import "))

combined = "import Mathlib.Analysis.Calculus.ContDiff.Basic\nimport Mathlib.Analysis.InnerProductSpace.PiL2\n\n"
combined += without_imports((HERE / "Statement.lean").read_text()) + "\n"
combined += without_imports(lean) + "\n"
fd, temp_name = tempfile.mkstemp(prefix="THM_M_1133_ObligationTree_", suffix=".lean", dir=HERE)
try:
    with os.fdopen(fd, "w") as stream:
        stream.write(combined)
    lean_cwd = ROOT / "Formalizations/Lean"
    relative_temp = os.path.relpath(temp_name, lean_cwd)
    result = subprocess.run(["lake", "env", "lean", relative_temp], cwd=lean_cwd, text=True, capture_output=True, timeout=120)
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    assert "caloric_isSubcaloric" in result.stdout
    assert "root_of_subsolutionMaximumPrinciple" in result.stdout
finally:
    Path(temp_name).unlink(missing_ok=True)
    Path(temp_name).with_suffix(".olean").unlink(missing_ok=True)

print(f"PASS THM-M-1133 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("Lean composition elaborated; root closure remains open (M3), with T-LIMIT at M4")
