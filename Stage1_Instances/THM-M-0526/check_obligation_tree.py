#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
registry_path = ROOT / "obligation-registry.json"
graphs_path = ROOT / "typed-graphs.json"

registry = json.loads(registry_path.read_text())
graphs = json.loads(graphs_path.read_text())

assert registry["item_id"] == "S56-M-0526-OBLIGATION_TREE"
assert graphs["registry"] == registry_path.name

nodes = registry["obligations"]
ids = [node["id"] for node in nodes]
assert len(ids) == len(set(ids)) == registry["closure_summary"]["required"] == 17
assert all(node["required"] for node in nodes)
assert registry["closure_summary"] == {
    "required": 17, "closed": 0, "open": 17, "root_closed": False
}

leaves = {node["id"] for node in nodes if node["leaf"]}
assert leaves == set(registry["root_cut_set"])
assert all(1 <= node["step_budget"] <= 100 for node in nodes if node["leaf"])
assert all("step_budget" not in node for node in nodes if not node["leaf"])

proof_edges = graphs["graphs"]["proof"]
known = set(ids)
assert all(child in known and parent in known and edge_type == "required_child"
           for child, parent, edge_type in proof_edges)

children = {node_id: [] for node_id in ids}
for child, parent, _ in proof_edges:
    children[parent].append(child)
assert {node_id for node_id, value in children.items() if not value} == leaves

visiting = set()
visited = set()
def visit(node_id):
    assert node_id not in visiting, "proof graph cycle"
    if node_id in visited:
        return
    visiting.add(node_id)
    for child in children[node_id]:
        visit(child)
    visiting.remove(node_id)
    visited.add(node_id)
visit("SVK-ROOT")
assert visited == known, "orphan proof obligation"

required_graphs = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
assert set(graphs["graphs"]) == required_graphs
assert graphs["deduplication"]["distinct_terminal_proof_bodies"] == 0

certificates = {entry["parent"]: entry for entry in graphs["composition_certificates"]}
assert certificates["SVK-UP"]["required_children"] == ["SVK-SQUARE", "SVK-EXISTS", "SVK-UNIQUE"]
assert certificates["SVK-ROOT"]["required_children"] == ["SVK-UP"]

canonical = json.dumps(
    [{key: value for key, value in node.items() if key != "status_vector"} for node in nodes],
    ensure_ascii=True, sort_keys=True, separators=(",", ":")
).encode()
digest = hashlib.sha256(canonical).hexdigest()
expected = registry["frozen_denominator_sha256"]
assert expected == digest, f"denominator digest mismatch: expected {expected}, computed {digest}"

lean = (ROOT / "ObligationTree.lean").read_text()
for name in ("SquareCommutativity", "LiftExistence", "LiftUniqueness", "compose_pushout", "compose_root"):
    assert name in lean
for prohibited in ("sorry", "admit", "axiom "):
    assert prohibited not in lean.lower(), f"prohibited Lean token: {prohibited}"

print(f"validated {len(nodes)} obligations, {len(leaves)} leaves, {len(proof_edges)} proof edges")
print(f"frozen denominator sha256: {digest}")
print("typed graphs: " + ", ".join(sorted(required_graphs)))
