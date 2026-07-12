#!/usr/bin/env python3
"""Fail-closed structural and Lean validation of the THM-M-1524 freeze."""

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
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1524-OBLIGATION_TREE"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows, nodes = registry["obligations"], bundle["nodes"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 14 and ids[0] == registry["root_obligation_id"]
denominator = hashlib.sha256(json.dumps([{k: row[k] for k in fields} for row in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert len(nodes) == 14 and {node["obligation_id"] for node in nodes} == set(ids)
readable = (HERE / "obligation-tree.md").read_text().lower()
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    assert "## " + node["public_readable_target"].split("#", 1)[1] in readable
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "transports", "trusts", "documents", "workflow_depends_on"}
seen = set()
for graph in bundle["graphs"].values():
    for value in graph["edges"]:
        assert value["edge_id"] not in seen and value["type"] in allowed and value["from"] in ids and value["to"] in ids
        assert value["edge_id"] in graph["out"][value["from"]] and value["edge_id"] in graph["in"][value["to"]]
        seen.add(value["edge_id"])
proof = {value["edge_id"]: value for value in bundle["graphs"]["proof"]["edges"]}
children = {}
for value in proof.values():
    reverse = proof[value["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == value["edge_id"] and (reverse["from"], reverse["to"]) == (value["to"], value["from"])
    assert {value["type"], reverse["type"]} == {"proof_requires", "composes"}
    if value["type"] == "proof_requires":
        children.setdefault(value["from"], []).append(value["to"])
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


visit("M1524-ROOT")
assert visited == {"M1524-ROOT", "M1524-T-ASSEMBLE", "M1524-L-ROBERTSON", "M1524-T-CCR", "M1524-N-CENTER", "M1524-L-SYMMETRY", "M1524-L-CAUCHY-SCHWARZ", "M1524-L-CCR-SCALAR"}
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
with tempfile.TemporaryDirectory(prefix="thm-m-1524-obligations-") as directory:
    cache = Path(directory)
    olean = cache / "Stage1_Instances" / "THM-M-1524" / "Statement.olean"
    olean.parent.mkdir(parents=True)
    first = subprocess.run(["lake", "env", "lean", "-R", str(ROOT), "-o", str(olean), str(HERE / "Statement.lean")], cwd=LEAN_DIR, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sys.stdout.write(first.stdout)
    assert first.returncode == 0
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{cache}:{env.get('LEAN_PATH', '')}"
    second = subprocess.run(["lake", "env", "lean", str(HERE / "ObligationTree.lean")], cwd=LEAN_DIR, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sys.stdout.write(second.stdout)
    assert second.returncode == 0
print(f"PASS THM-M-1524 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M2); centering, symmetry, and CCR scalar evaluation remain open")
