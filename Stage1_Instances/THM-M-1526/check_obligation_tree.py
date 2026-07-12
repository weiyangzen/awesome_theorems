#!/usr/bin/env python3
"""Validate THM-M-1526's frozen registry, typed graphs, and Lean composition."""

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in registry["obligations"]]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_against_statement_expression_sha256"] == statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 17
assert ids[0] == registry["root_obligation_id"] == "M1526-ROOT"

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
                 "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
                 "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
                 "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
                 "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert {node["obligation_id"] for node in nodes} == set(ids) and len(nodes) == len(ids)
for node in nodes:
    assert required_node <= node.keys()
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "source_anchors", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    assert "no stronger conclusion" in node["semantic_step_ledger"]["outgoing_use"].lower()

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids, adjacency = set(), {}
for name, graph in bundle["graphs"].items():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids
        edge_ids.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
        if name == "refinement" or (name == "proof" and edge["type"] == "proof_requires"):
            adjacency.setdefault(edge["from"], []).append(edge["to"])

proof_edges = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
for edge in proof_edges.values():
    reverse = proof_edges[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}

seen, active = set(), set()
def visit(current):
    assert current not in active, f"cycle at {current}"
    if current in seen:
        return
    active.add(current)
    for child in adjacency.get(current, []):
        visit(child)
    active.remove(current)
    seen.add(current)
visit("M1526-ROOT")
assert {r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"} <= seen

for key, field, value in (("required_machine", "machine_eligibility", "required"),
                          ("required_human_source", "human_source_eligibility", "required"),
                          ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == value]
assert registry["frozen_denominators"]["inventory"] == ids
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M1526-N-PRODUCT", "M1526-L-SLASH-SQUARE"]

lean_root = ROOT / "Formalizations" / "Lean"
lean_path_result = subprocess.run(["lake", "env", "printenv", "LEAN_PATH"], cwd=lean_root,
                                  text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
assert lean_path_result.returncode == 0, lean_path_result.stdout
lean_bin_result = subprocess.run(["lake", "env", "which", "lean"], cwd=lean_root,
                                 text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
assert lean_bin_result.returncode == 0, lean_bin_result.stdout
lean_bin = lean_bin_result.stdout.strip()
with tempfile.TemporaryDirectory(prefix="thm-m-1526-") as temporary:
    temporary = Path(temporary)
    compile_statement = subprocess.run(
        [lean_bin, "-o", str(temporary / "Statement.olean"), "Statement.lean"],
        cwd=HERE, env={**os.environ, "LEAN_PATH": lean_path_result.stdout.strip()},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if compile_statement.returncode:
        print(compile_statement.stdout, end="")
        raise SystemExit(compile_statement.returncode)
    env = {**os.environ, "LEAN_PATH": str(temporary) + ":" + lean_path_result.stdout.strip()}
    result = subprocess.run([lean_bin, "ObligationTree.lean"], cwd=HERE, env=env,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    assert "root_of_factorization" in result.stdout
    assert "sorryAx" not in result.stdout

print(f"PASS THM-M-1526 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("conditional composition elaborated; root remains open at M3")
