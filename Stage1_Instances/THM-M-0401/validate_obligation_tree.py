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
projection = [{k: row[k] for k in projection_fields} for row in registry["obligations"]]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert registry["denominator_sha256"] == digest, (registry["denominator_sha256"], digest)

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) and "M0401-ROOT" in ids
node_ids = [node["node_id"] for node in bundle["nodes"]]
assert set(ids) == set(node_ids) and len(node_ids) == len(set(node_ids))
required_node_fields = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
    "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
    "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
    "task_ids", "owned_sources", "owner", "reviewer", "validity",
}
for node in bundle["nodes"]:
    assert required_node_fields <= node.keys(), node["node_id"]
    assert 0 < node["step_budget"] <= 100
    if node["obligation_id"] != "M0401-S-COORDINATEWISE-TRANSPORT":
        assert node["semantic_step_ledger"]

expected_graphs = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
assert set(bundle["graphs"]) == expected_graphs
all_edge_ids = set()
for graph_name, graph in bundle["graphs"].items():
    edges = graph["edges"]
    by_id = {edge["edge_id"]: edge for edge in edges}
    assert len(by_id) == len(edges)
    assert not (all_edge_ids & by_id.keys())
    all_edge_ids |= by_id.keys()
    for edge in edges:
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
    recorded = {eid for values in graph["out"].values() for eid in values}
    reverse = {eid for values in graph["in"].values() for eid in values}
    assert recorded == set(by_id) == reverse, graph_name

proof_edges = bundle["graphs"]["proof"]["edges"]
children = {}
for edge in proof_edges:
    children.setdefault(edge["from"], []).append(edge["to"])
seen = set()
active = set()
def visit(node):
    assert node not in active, f"proof cycle at {node}"
    if node in seen:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    seen.add(node)
visit("M0401-ROOT")
required_math = {
    row["obligation_id"] for row in rows
    if row["root_relevant"] and row["machine_eligibility"] == "required"
    and row["kind"] not in {"definition"}
} - {"M0401-S-FOUNDATION", "M0401-X-PROVENANCE"}
assert required_math <= seen

for key, eligibility in (("required_machine", "machine_eligibility"),
                         ("required_human_source", "human_source_eligibility"),
                         ("required_readable", "readable_eligibility")):
    expected = [row["obligation_id"] for row in rows if row[eligibility] == "required"]
    assert registry["frozen_denominators"][key] == expected, key
assert registry["frozen_denominators"]["inventory"] == ids
assert bundle["closure_boundary"]["closed_obligations"] == []
assert bundle["closure_boundary"]["theorem_complete"] is False
print(f"PASS THM-M-0401 obligation tree: {len(ids)} obligations, {len(all_edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M4); no proof or theorem completion claimed")
