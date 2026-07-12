#!/usr/bin/env python3
"""Fail-closed structural and Lean validation of the THM-M-1010 freeze."""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
tasks = json.loads((HERE / "task-dag.json").read_text())
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == tasks["item_id"] == "S56-M-1010-OBLIGATION_TREE"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor_audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
nodes = bundle["nodes"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 15 and ids[0] == registry["root_obligation_id"]
projection = [{key: row[key] for key in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
for key, field, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == value]

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert len(nodes) == 15 and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
seen = set()
for graph in bundle["graphs"].values():
    for item in graph["edges"]:
        assert item["edge_id"] not in seen and item["type"] in allowed
        assert item["from"] in ids and item["to"] in ids
        assert item["edge_id"] in graph["out"][item["from"]]
        assert item["edge_id"] in graph["in"][item["to"]]
        seen.add(item["edge_id"])

proof = {item["edge_id"]: item for item in bundle["graphs"]["proof"]["edges"]}
children = {}
for item in proof.values():
    reverse = proof[item["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == item["edge_id"]
    assert (reverse["from"], reverse["to"]) == (item["to"], item["from"])
    assert {item["type"], reverse["type"]} == {"proof_requires", "composes"}
    if item["type"] == "proof_requires":
        children.setdefault(item["from"], []).append(item["to"])

visiting, visited = set(), set()


def visit(node):
    assert node not in visiting, f"proof cycle at {node}"
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)


visit("M1010-ROOT")
expected_proof = {"M1010-ROOT", "M1010-T-ASSEMBLE", "M1010-C-COUPLING", "M1010-N-PARTITIONS", "M1010-C-INTERVAL", "M1010-L-MEASURABLE", "M1010-L-LAWS", "M1010-L-METRIC-CONVERGENCE", "M1010-L-AE-STABILIZE"}
assert visited == expected_proof
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
for recipe in specs["recipes"]:
    assert isinstance(recipe["argv"], list) and recipe["network_policy"] == "denied"
    assert recipe["covered_obligation_ids"] and set(recipe["covered_obligation_ids"]) <= set(ids)
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
assert tasks["tasks"][-1]["state"] == "open"

lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
with tempfile.TemporaryDirectory(prefix="thm-m-1010-obligations-") as directory:
    cache = Path(directory)
    olean = cache / "Stage1_Instances" / "THM-M-1010" / "Statement.olean"
    olean.parent.mkdir(parents=True)
    first = subprocess.run(["lake", "env", "lean", "-R", str(ROOT), "-o", str(olean), str(HERE / "Statement.lean")], cwd=LEAN_DIR, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sys.stdout.write(first.stdout)
    assert first.returncode == 0
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{cache}:{env.get('LEAN_PATH', '')}"
    second = subprocess.run(["lake", "env", "lean", str(HERE / "ObligationTree.lean")], cwd=LEAN_DIR, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sys.stdout.write(second.stdout)
    assert second.returncode == 0

print(f"PASS THM-M-1010 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M3); partition and common-space coupling packages remain open")
