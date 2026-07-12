#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1078 architecture freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == "S56-M-1078-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-1078"
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 15
assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == "M1078-ROOT"
required = {"obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id"}
assert all(required <= row.keys() for row in rows)
assert all(row["terminal_proof_body_id"] is None for row in rows)

denominator = registry["frozen_denominators"]
assert denominator["inventory"] == ids
assert denominator["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]
assert denominator["required_human_source"] == [row["obligation_id"] for row in rows if row["human_source_eligibility"] == "required"]
assert denominator["required_readable"] == ids
assert set(denominator["informational_overlays"]) == {"M1078-X-SOURCE", "M1078-X-PROVENANCE"}
digest = hashlib.sha256(json.dumps(denominator, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert bundle["registry_denominator_sha256"] == digest

nodes = bundle["nodes"]
assert [node["obligation_id"] for node in nodes] == ids
assert all(0 < node["step_budget"] <= 100 for node in nodes)
assert all(len(node["semantic_step_ledger"]) == node["step_budget"] for node in nodes)
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}

all_edges, proof_adjacency = set(), {}
for name, graph in bundle["graphs"].items():
    local = {edge["edge_id"] for edge in graph["edges"]}
    assert len(local) == len(graph["edges"]) and not (all_edges & local)
    all_edges |= local
    for edge in graph["edges"]:
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
        if name in {"proof", "refinement"}:
            proof_adjacency.setdefault(edge["from"], []).append(edge["to"])

def reaches_root(start: str) -> bool:
    frontier, seen = [start], set()
    while frontier:
        node = frontier.pop()
        if node == "M1078-ROOT":
            return True
        assert node not in seen, f"cycle at {node}"
        seen.add(node)
        frontier.extend(proof_adjacency.get(node, []))
    return False

assert all(reaches_root(oid) for oid in denominator["required_machine"])
closure = bundle["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M2"
assert set(closure["remaining_root_cut_set"]) == {"M1078-C-EXTERNAL-PIN", "M1078-T-ALLTIME", "M1078-B-PREDICTABLE", "M1078-B-NORM"}
assert bundle["composition_certificates"][0]["status"] == "checked_conditional_composition_only"

statement_sha = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert bundle["statement_source_sha256"] == statement_sha
tree_text = (HERE / "obligation-tree.md").read_text()
assert all(f"### {oid}" in tree_text for oid in ids)
assert "All 13 semantic machine obligations are open" in tree_text

print(f"PASS THM-M-1078 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M2); conditional composition only")
