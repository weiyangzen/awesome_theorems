#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "obligation-tree.json").read_text(encoding="utf-8"))

required_node_fields = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
    "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
    "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
    "task_ids", "owned_sources", "owner", "reviewer", "validity",
}
allowed_edges = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}

assert DATA["item_id"] == "S56-M-0400-OBLIGATION_TREE"
obligations = DATA["obligations"]
ids = [item["obligation_id"] for item in obligations]
assert len(ids) == len(set(ids)), "duplicate obligation ID"
digest = hashlib.sha256(json.dumps(obligations, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
assert digest == DATA["registry_sha256"], f"registry digest mismatch: {digest}"

nodes = DATA["nodes"]
assert {node["obligation_id"] for node in nodes} == set(ids), "nodes must cover the registry exactly"
assert len({node["node_id"] for node in nodes}) == len(nodes), "duplicate node ID"
for node in nodes:
    missing = required_node_fields - node.keys()
    assert not missing, f"{node['node_id']} missing {sorted(missing)}"
    budget = node["step_budget"]
    assert budget == "split-required" or isinstance(budget, int) and 0 < budget <= 100
    assert node["semantic_step_ledger"], f"empty ledger: {node['node_id']}"
    assert node["public_readable_target"].startswith("Stage1_Instances/THM-M-0400/")

workflow_ids = {
    "S56-M-0400-OBLIGATION_TREE", "S56-M-0400-PROOF",
    "S56-M-0400-VALIDATION", "S56-M-0400-RELEASE",
}
for graph_name, edges in DATA["graphs"].items():
    for edge in edges:
        assert edge["type"] in allowed_edges, f"illegal edge type in {graph_name}"
        endpoints = workflow_ids if graph_name == "workflow" else set(ids)
        assert edge["from"] in endpoints and edge["to"] in endpoints, f"bad endpoint in {graph_name}"

proof_edges = DATA["graphs"]["proof"]
children = {}
for edge in proof_edges:
    children.setdefault(edge["from"], []).append(edge["to"])

seen = set()
stack = ["M0400-ROOT"]
while stack:
    current = stack.pop()
    if current in seen:
        continue
    seen.add(current)
    stack.extend(children.get(current, []))
required_proof = set(DATA["denominators"]["required_machine_ids"]) - {"M0400-X-FOUNDATION"}
assert required_proof <= seen, f"proof graph unreachable required nodes: {sorted(required_proof - seen)}"

visiting = set()
done = set()
def visit(node):
    assert node not in visiting, f"proof cycle at {node}"
    if node in done:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    done.add(node)
visit("M0400-ROOT")

for key, eligibility in [
    ("required_machine_ids", "machine_eligibility"),
    ("required_human_source_ids", "human_source_eligibility"),
    ("required_readable_ids", "readable_eligibility"),
]:
    expected = {o["obligation_id"] for o in obligations if o[eligibility] == "required"}
    assert set(DATA["denominators"][key]) == expected, f"denominator mismatch: {key}"

assert DATA["denominators"]["closed_machine_ids"] == []
assert DATA["theorem_complete"] is False and DATA["audit_complete"] is False
print(f"obligation-tree: ok ({len(ids)} obligations, {sum(len(v) for v in DATA['graphs'].values())} typed edges, registry {digest})")
