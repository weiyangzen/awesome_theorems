#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1083 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
recipes = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == recipes["item_id"] == "S56-M-1083-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == recipes["theorem_id"] == "THM-M-1083"
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 20
assert registry["root_obligation_id"] == bundle["root_node_id"] == "M1083-ROOT"

row_fields = {"obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id"}
assert all(row_fields <= row.keys() for row in rows)
assert all(row["terminal_proof_body_id"] is None for row in rows)
den = registry["frozen_denominators"]
assert den["inventory"] == ids
assert den["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
assert den["required_human_source"] == [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"]
assert den["required_readable"] == ids
digest = hashlib.sha256(json.dumps(den, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert registry["denominator_sha256"] == bundle["registry_denominator_sha256"] == digest
assert registry["frozen_against_statement_sha256"] == bundle["statement_source_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == bundle["anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert [node["obligation_id"] for node in nodes] == ids
assert len({node["node_id"] for node in nodes}) == len(nodes)
assert all(node_fields <= node.keys() for node in nodes)
assert all(0 < node["step_budget"] <= 100 for node in nodes)
assert all(set(node["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"} for node in nodes)

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
proof_adj = {}
for name, graph in bundle["graphs"].items():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in all_edges
        all_edges.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
        if name == "proof":
            proof_adj.setdefault(edge["from"], []).append(edge["to"])

def reaches_root(start):
    frontier, seen = [start], set()
    while frontier:
        node = frontier.pop()
        if node == "M1083-ROOT":
            return True
        assert node not in seen, f"proof cycle at {node}"
        seen.add(node)
        frontier.extend(proof_adj.get(node, []))
    return False

assert all(reaches_root(oid) for oid in den["required_machine"])
assert len(recipes["recipes"]) == len(ids)
assert {recipe["obligation_id"] for recipe in recipes["recipes"]} == set(ids)
closure = bundle["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M3"

# This phase validator owns only the frozen statement/audit/composition sources. Later proof and
# validation modules have their own parser-aware hygiene and transitive kernel checks.
for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean"):
    source = (HERE / name).read_text()
    assert "sorry" not in source and "admit" not in source and "sorryAx" not in source

print(f"PASS THM-M-1083 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); no proof or theorem completion claimed")
