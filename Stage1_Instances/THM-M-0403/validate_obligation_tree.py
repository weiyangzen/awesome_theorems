#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "obligation-graphs.json").read_text())

projection_fields = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason",
)
projection = [{key: row[key] for key in projection_fields} for row in registry["obligations"]]
digest = hashlib.sha256(
    json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()
assert registry["denominator_sha256"] == digest, (registry["denominator_sha256"], digest)

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) and "M0403-ROOT" in ids
nodes = bundle["nodes"]
node_ids = [node["node_id"] for node in nodes]
assert set(ids) == set(node_ids) and len(node_ids) == len(set(node_ids))

required_node_fields = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
    "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
    "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
    "task_ids", "owned_sources", "owner", "reviewer", "validity",
}
for node in nodes:
    assert required_node_fields <= node.keys(), (node["node_id"], required_node_fields - node.keys())
    assert node["node_id"] == node["obligation_id"]
    assert 0 <= node["step_budget"] <= 100
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}

allowed_graph_types = {
    "proof": {"proof_requires", "composes"},
    "refinement": {"logical_decomposition", "expository_decomposition", "equivalent_to", "transports"},
    "provenance": {"source_map", "provenance_of"},
    "evidence": {"evidence_for"},
    "trust": {"trusts"},
    "documentation": {"documents"},
    "workflow": {"workflow_depends_on"},
}
edge_count = 0
for graph_name, graph in bundle["graphs"].items():
    assert graph_name in allowed_graph_types
    seen = set()
    expected_out = {}
    expected_in = {}
    adjacency = {node_id: [] for node_id in node_ids}
    for edge in graph["edges"]:
        assert set(edge) == {"edge_id", "type", "from", "to"}
        assert edge["edge_id"] not in seen
        seen.add(edge["edge_id"])
        assert edge["type"] in allowed_graph_types[graph_name]
        assert edge["from"] in node_ids and edge["to"] in node_ids and edge["from"] != edge["to"]
        expected_out.setdefault(edge["from"], []).append(edge["edge_id"])
        expected_in.setdefault(edge["to"], []).append(edge["edge_id"])
        adjacency[edge["from"]].append(edge["to"])
        edge_count += 1
    assert graph["out"] == expected_out and graph["in"] == expected_in

    visiting = set()
    visited = set()
    def visit(node_id):
        assert node_id not in visiting, (graph_name, "cycle", node_id)
        if node_id in visited:
            return
        visiting.add(node_id)
        for child in adjacency[node_id]:
            visit(child)
        visiting.remove(node_id)
        visited.add(node_id)
    for node_id in node_ids:
        visit(node_id)

proof_reachable = set()
proof_children = {}
for edge in bundle["graphs"]["proof"]["edges"]:
    proof_children.setdefault(edge["from"], []).append(edge["to"])
def walk(node_id):
    if node_id in proof_reachable:
        return
    proof_reachable.add(node_id)
    for child in proof_children.get(node_id, []):
        walk(child)
walk("M0403-ROOT")
required = {row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"}
support = {"M0403-S-DEFINITIONS", "M0403-S-FOUNDATION", "M0403-X-PROVENANCE"}
assert required - support <= proof_reachable

counts = registry["eligibility_counts"]
assert counts == {
    "total": len(rows),
    "root_relevant": sum(row["root_relevant"] for row in rows),
    "machine_required": sum(row["machine_eligibility"] == "required" for row in rows),
    "human_source_required": sum(row["human_source_eligibility"] == "required" for row in rows),
    "readable_required": sum(row["readable_eligibility"] == "required" for row in rows),
    "informational": sum(row["machine_eligibility"] == "informational" for row in rows),
}
assert not registry["status_observed_after_freeze"]["closed_obligations"]
assert bundle["closure_boundary"]["root_machine_debt"] == "M4"
assert not bundle["closure_boundary"]["composition_certificates"]
assert not bundle["closure_boundary"]["theorem_complete"]
print(f"ok: {len(rows)} obligations, {edge_count} typed edges; denominator {digest}; root open M4")
