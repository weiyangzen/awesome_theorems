#!/usr/bin/env python3
"""Fail-closed structural validation for the frozen THM-M-0399 proof architecture."""

from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
units = json.loads((HERE / "proof-units.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"obligation tree check failed: {message}")


expected_expression = "d63a5863b947f4e03f21847e040b9f4980722607ae953749fa2cb7851a492389"
require(registry["item_id"] == "S56-M-0399-OBLIGATION_TREE", "wrong item")
require(registry["theorem_id"] == units["theorem_id"] == bundle["theorem_id"] ==
        specs["theorem_id"] == "THM-M-0399", "theorem identity mismatch")
require(registry["frozen_against_expression_sha256"] == expected_expression,
        "canonical expression drift")

obligations = registry["obligations"]
obligation_ids = [row["obligation_id"] for row in obligations]
require(len(obligation_ids) == len(set(obligation_ids)) == 11, "obligation IDs not unique")
digest = hashlib.sha256("\n".join(obligation_ids).encode()).hexdigest()
require(digest == registry["denominator"]["canonical_ids_sha256"], "denominator hash mismatch")
require(registry["denominator"] == {
    "root_relevant_total": 11, "machine_required": 11, "human_source_required": 9,
    "readable_required": 11, "weight_total": 11, "canonical_ids_sha256": digest,
}, "frozen denominator disagrees with registry")
require(all(row["root_relevant"] and row["machine_eligibility"] == "required"
            and row["terminal_proof_body_id"] is None for row in obligations),
        "registry improperly excludes or closes an obligation")

nodes = units["nodes"]
node_ids = [node["node_id"] for node in nodes]
require(len(node_ids) == len(set(node_ids)) == 11, "proof node IDs not unique")
require({node["obligation_id"] for node in nodes} == set(obligation_ids),
        "proof nodes do not cover the registry exactly")
required_node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "source_crosswalk_id", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources"}
for node in nodes:
    require(required_node_fields <= node.keys(), f"incomplete node {node['node_id']}")
    require(0 < node["step_budget"] <= 100, f"invalid step budget {node['node_id']}")
    require(node["semantic_step_ledger"], f"empty semantic ledger {node['node_id']}")

proof = bundle["graphs"]["proof"]
edge_ids = {edge["edge_id"] for edge in proof}
require(len(edge_ids) == len(proof), "duplicate proof edge ID")
by_id = {edge["edge_id"]: edge for edge in proof}
for edge in proof:
    require(edge["from"] in node_ids and edge["to"] in node_ids, "proof edge endpoint missing")
    reverse = by_id.get(edge["reciprocal_edge_id"])
    require(reverse is not None and reverse["from"] == edge["to"] and
            reverse["to"] == edge["from"], f"bad reciprocal for {edge['edge_id']}")
    require({edge["type"], reverse["type"]} == {"proof_requires", "composes"},
            f"illegal reciprocal types for {edge['edge_id']}")

children = {}
for edge in proof:
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])
seen, active = set(), set()
def visit(node: str) -> None:
    require(node not in active, "cycle in proof_requires graph")
    if node in seen:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    seen.add(node)
visit(bundle["root_node_id"])
require(seen == set(node_ids) - {"THM-M-0399-FOUNDATION"},
        "proof graph has an orphan or improperly proof-linked trust node")

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map",
           "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
all_graph_edges = [edge for edges in bundle["graphs"].values() for edge in edges]
require(all(edge["type"] in allowed for edge in all_graph_edges), "unknown typed edge")
recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
require({node["validation_spec_id"] for node in nodes} <= recipe_ids,
        "node references missing validation recipe")
require(bundle["proof_closure"]["root_closed"] is False and
        bundle["proof_closure"]["closed_nodes"] == 0, "false closure claim")

print("obligation tree check: ok; 11 frozen obligations, 11 typed nodes, 7 graph families")
