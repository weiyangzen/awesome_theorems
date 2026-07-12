#!/usr/bin/env python3
"""Validate the frozen obligation architecture and conditional Lean composition."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())

registry_fields = {"obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id"}
node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert registry["item_id"] == bundle["item_id"] == "S56-M-0321-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-0321"
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 30
assert ids[0] == registry["root_obligation_id"] == "M0321-ROOT"
assert all(registry_fields <= row.keys() for row in rows)

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
raw = json.dumps([{k: row[k] for k in fields} for row in rows], sort_keys=True, separators=(",", ":")).encode()
assert hashlib.sha256(raw).hexdigest() == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
for key, field, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == value]
assert registry["frozen_denominators"]["inventory"] == ids

nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert node_fields <= node.keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100
    assert node["semantic_step_ledger"]

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
allowed = {"proof_requires", "composes", "logical_decomposition", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
seen_edges, adjacency = set(), {}
for name, graph in bundle["graphs"].items():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in seen_edges
        seen_edges.add(edge["edge_id"])
        assert edge["type"] in allowed and edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
        if name in {"proof", "refinement"}:
            adjacency.setdefault(edge["from"], []).append(edge["to"])

active, visited = set(), set()
def visit(node: str) -> None:
    assert node not in active, f"cycle at {node}"
    if node in visited: return
    active.add(node)
    for child in adjacency.get(node, []): visit(child)
    active.remove(node); visited.add(node)
visit("M0321-ROOT")
required = {row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"}
assert required <= visited
assert bundle["closure_boundary"]["closed_obligations"] == []
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M0321-L-SINGLE", "M0321-L-FIP-COMPACT"]

lean_source = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom"):
    if re.search(rf"\b{forbidden}\b", lean_source): raise SystemExit(f"forbidden token: {forbidden}")
assert "finiteFamily" in lean_source and "compactness" in lean_source and "#print axioms root_compose" in lean_source
statement = (HERE / "Statement.lean").read_text()
obligation_body = lean_source.split("\n", 1)[1]
with tempfile.NamedTemporaryFile(mode="w", suffix=".lean", dir=HERE, encoding="utf-8") as handle:
    handle.write(statement + "\n" + obligation_body)
    handle.flush()
    result = subprocess.run(
        ["lake", "env", "lean", os.path.relpath(handle.name, LEAN_ROOT)],
        cwd=LEAN_ROOT, text=True, capture_output=True,
    )
sys.stdout.write(result.stdout); sys.stderr.write(result.stderr)
if result.returncode: raise SystemExit(result.returncode)
assert "root_compose" in result.stdout
print(f"PASS THM-M-0321 obligation tree: {len(ids)} obligations, {len(seen_edges)} typed edges")
print(f"registry denominator sha256: {registry['denominator_sha256']}")
print("root remains open at M3; conditional child-to-parent composition elaborated")
