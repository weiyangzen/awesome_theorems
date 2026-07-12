#!/usr/bin/env python3
"""Fail-closed structural and Lean validation of the THM-M-1246 freeze."""

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
intake = json.loads((HERE / "intake.json").read_text())
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1246-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-1246"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 15 and ids[0] == registry["root_obligation_id"] == "M1246-ROOT"
digest = hashlib.sha256(json.dumps([{k: r[k] for k in fields} for r in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert intake["obligation_registry_hash"] == "sha256:" + digest
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in all_edges and e["type"] in allowed
        assert e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        all_edges.add(e["edge_id"])

proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for e in proof.values():
    reverse = proof[e["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == e["edge_id"]
    assert (reverse["from"], reverse["to"]) == (e["to"], e["from"])
    assert {e["type"], reverse["type"]} == {"proof_requires", "composes"}
    if e["type"] == "proof_requires": children.setdefault(e["from"], []).append(e["to"])
visiting, visited = set(), set()
def visit(node):
    assert node not in visiting
    if node in visited: return
    visiting.add(node)
    for child in children.get(node, []): visit(child)
    visiting.remove(node); visited.add(node)
visit("M1246-ROOT")
assert visited == set(ids) - {"M1246-S-FOUNDATION", "M1246-X-SOURCE", "M1246-X-PROVENANCE"}
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M1246-T-ANALYTIC"]
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False

lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
with tempfile.TemporaryDirectory(prefix="m1246-obligation-", dir=ROOT / "Formalizations/Lean") as tmp:
    tmp = Path(tmp)
    shutil.copy2(HERE / "Statement.lean", tmp / "Statement.lean")
    shutil.copy2(HERE / "ObligationTree.lean", tmp / "ObligationTree.lean")
    statement = subprocess.run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], cwd=ROOT / "Formalizations/Lean", text=True, capture_output=True)
    assert statement.returncode == 0, statement.stdout + statement.stderr
    env = os.environ.copy()
    env["LEAN_PATH"] = str(tmp) + (":" + env["LEAN_PATH"] if env.get("LEAN_PATH") else "")
    result = subprocess.run(["lake", "env", "lean", str(tmp / "ObligationTree.lean")], cwd=ROOT / "Formalizations/Lean", env=env, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "root_of_hardyTerminal" in result.stdout
print(f"PASS THM-M-1246 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("Lean conditional composition: passed; root open at M1246-T-ANALYTIC (M3)")
