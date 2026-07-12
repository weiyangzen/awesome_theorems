#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0996 frozen architecture."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
registry = json.loads((ROOT / "obligation-registry.json").read_text())
typed = json.loads((ROOT / "typed-graphs.json").read_text())

def digest(value):
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()

assert registry["schema_version"] == "stage1-obligation-registry/1.0"
assert typed["schema_version"] == "stage1-typed-graphs/1.0"
assert registry["theorem_id"] == typed["theorem_id"] == "THM-M-0996"
ids = [x["obligation_id"] for x in registry["obligations"]]
assert len(ids) == len(set(ids)) == 19
assert ids == registry["frozen_denominators"]["inventory"]
assert digest(registry["frozen_denominators"]) == registry["denominator_sha256"]
assert typed["registry_denominator_sha256"] == registry["denominator_sha256"]
assert {x["obligation_id"] for x in typed["nodes"]} == set(ids)
required_node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
for node in typed["nodes"]:
    assert required_node_fields <= node.keys()
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "source_anchors", "outgoing_use"} <= node["semantic_step_ledger"].keys()
assert set(typed["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}

proof = typed["graphs"]["proof"]["edges"]
by_id = {e["edge_id"]: e for e in proof}
assert len(by_id) == len(proof)
for edge in proof:
    reciprocal = by_id[edge["reciprocal_edge_id"]]
    assert reciprocal["from"] == edge["to"] and reciprocal["to"] == edge["from"]
    assert {edge["type"], reciprocal["type"]} == {"proof_requires", "composes"}

# Required proof edges form an acyclic parent-to-child graph and reach both cut leaves.
adj = {}
for edge in proof:
    if edge["type"] == "proof_requires":
        adj.setdefault(edge["from"], []).append(edge["to"])
seen, active = set(), set()
def visit(node):
    assert node not in active, "proof cycle"
    if node in seen: return
    active.add(node)
    for child in adj.get(node, []): visit(child)
    active.remove(node); seen.add(node)
visit("M0996-ROOT")
assert set(typed["remaining_root_cut_set"]) <= seen
assert not registry["status_observed_after_freeze"]["closed_obligations"]
assert typed["theorem_complete"] is False
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((ROOT / "statement.json").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((ROOT / "anchor-audit.json").read_bytes()).hexdigest()
print("obligation tree check: ok (19 obligations, 7 graph classes, reciprocal proof edges, acyclic open root)")
