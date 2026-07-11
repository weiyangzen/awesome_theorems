#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
registry = json.loads((root / "obligation-registry.json").read_text())
graphs = json.loads((root / "typed-graphs.json").read_text())

assert registry["theorem_id"] == graphs["theorem_id"] == "THM-M-0393"
assert registry["registry_id"] == graphs["registry_id"]
statement_hash = hashlib.sha256((root / "Statement.lean").read_bytes()).hexdigest()
assert statement_hash == registry["freeze_basis"]["statement_sha256"]

obligations = registry["obligations"]
ids = [node["id"] for node in obligations]
assert len(ids) == len(set(ids)) and "M0393-ROOT" in ids
hash_input = json.dumps([{"id": node["id"], "fingerprint": node["fingerprint"]}
                         for node in obligations], sort_keys=True, separators=(",", ":")).encode()
assert "sha256:" + hashlib.sha256(hash_input).hexdigest() == registry["registry_content_hash"]
required = {"id", "kind", "statement", "fingerprint", "risk", "source", "body"}
assert all(required <= node.keys() for node in obligations)
assert all(node["body"] is None for node in obligations)
assert registry["uniform_node_fields"]["machine_debt"] == "M4"
assert registry["eligibility_exclusions"] == []

proof = graphs["proof_graph"]
proof_edges = proof["edges"]
assert all(edge["type"] == "proof_requires" for edge in proof_edges)
assert all(edge["from"] in ids and edge["to"] in ids for edge in proof_edges)
reachable = {proof["root"]}
while True:
    expanded = reachable | {e["to"] for e in proof_edges if e["from"] in reachable}
    if expanded == reachable:
        break
    reachable = expanded
assert reachable == set(ids), (set(ids) - reachable)

def acyclic(nodes, edges):
    incoming = {node: 0 for node in nodes}
    outgoing = {node: [] for node in nodes}
    for source, target in edges:
        outgoing[source].append(target)
        incoming[target] += 1
    queue = [node for node, degree in incoming.items() if degree == 0]
    seen = 0
    while queue:
        node = queue.pop()
        seen += 1
        for target in outgoing[node]:
            incoming[target] -= 1
            if incoming[target] == 0:
                queue.append(target)
    return seen == len(nodes)

assert acyclic(set(ids), [(e["from"], e["to"]) for e in proof_edges])
for cert in proof["composition_certificates"]:
    actual = {e["to"] for e in proof_edges if e["from"] == cert["parent"]}
    assert actual == set(cert["required_children"])
    assert cert["state"] == "planned_open"

allowed = {"proof_requires", "logical_decomposition", "source_map", "provenance_of",
           "trusts", "documents", "workflow_depends_on"}
for graph_name in ("proof_graph", "refinement_graph", "provenance_graph", "evidence_graph",
                   "trust_graph", "documentation_graph", "workflow_graph"):
    for edge in graphs[graph_name].get("edges", []):
        assert edge["type"] in allowed

tasks = {task["id"] for task in graphs["workflow_graph"]["tasks"]}
workflow_edges = graphs["workflow_graph"]["edges"]
assert all(e["from"] in tasks and e["to"] in tasks for e in workflow_edges)
assert acyclic(tasks, [(e["from"], e["to"]) for e in workflow_edges])
assert graphs["evidence_graph"]["evidence_nodes"] == []
assert registry["theorem_complete"] is False

print(f"obligation_tree: ok ({len(ids)} obligations, {len(proof_edges)} proof edges, "
      f"{len(tasks)} workflow tasks; root M4/open)")
