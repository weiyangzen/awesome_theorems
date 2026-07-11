#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-0441 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

def require(condition, message):
    if not condition:
        raise SystemExit(f"obligation-tree check failed: {message}")

require(registry["item_id"] == graphs["item_id"] == "S56-M-0441-OBLIGATION_TREE", "wrong item")
require(registry["theorem_id"] == graphs["theorem_id"] == "THM-M-0441", "wrong theorem")
require(hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() ==
        registry["frozen_against_statement_sha256"], "statement drift")
require(hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest() ==
        registry["frozen_against_anchor_audit_sha256"], "anchor audit drift")

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
require(len(ids) == 21 and len(ids) == len(set(ids)), "registry must have 21 unique obligations")
require(ids == registry["frozen_denominators"]["inventory"], "inventory denominator drift")
require({node["obligation_id"] for node in graphs["nodes"]} == set(ids), "node projection mismatch")
require([row["obligation_id"] for row in rows if row["machine_eligibility"] == "not_applicable"] ==
        ["M0441-SOURCE"], "machine exclusion must be explicit and unique")
for row in rows:
    budget = row["step_budget"]
    require(budget == "split-required" or isinstance(budget, int) and 0 < budget <= 100,
            f"invalid budget for {row['obligation_id']}")

expected_graphs = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
require(set(graphs["graphs"]) == expected_graphs, "typed graph families incomplete")
allowed = {"proof_requires", "refines", "provenance_of", "evidence_for", "trusts",
           "documents", "source_map", "workflow_depends_on"}
edge_ids = []
for graph in graphs["graphs"].values():
    for edge in graph["edges"]:
        edge_ids.append(edge["edge_id"])
        require(edge["type"] in allowed, f"untyped edge {edge['edge_id']}")
require(len(edge_ids) == len(set(edge_ids)), "edge IDs are not globally unique")

children = {}
for edge in graphs["graphs"]["proof"]["edges"]:
    require(edge["from"] in ids and edge["to"] in ids, "proof edge leaves registry")
    children.setdefault(edge["from"], []).append(edge["to"])
visiting, visited = set(), set()
def visit(node):
    require(node not in visiting, f"proof cycle at {node}")
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)
visit("M0441-ROOT")
require(visited == set(ids) - {"M0441-SOURCE", "M0441-TRUST"}, "proof route coverage drift")

boundary = graphs["closure_boundary"]
require(boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False,
        "closure boundary overstated")
require(boundary["closed_obligations"] == [], "architecture freeze must not credit proof closure")
lean = (HERE / "ObligationTree.lean").read_text()
require(all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe")),
        "forbidden Lean mechanism")
require(all(name in lean for name in ("CountingEngine", "engine_compose", "countingConclusion_iff")),
        "typed composition interface missing")
print(f"PASS THM-M-0441 obligation freeze: {len(ids)} obligations, "
      f"{len(graphs['graphs']['proof']['edges'])} proof edges; root open")
