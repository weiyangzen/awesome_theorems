#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0406 architecture."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
typed = json.loads((HERE / "typed-graphs.json").read_text())
assert registry["theorem_id"] == typed["theorem_id"] == "THM-M-0406"
assert registry["registry_id"] == typed["registry_id"] == "THM-M-0406-OBLIGATIONS-v1"
obligations = registry["obligations"]
ids = [o["obligation_id"] for o in obligations]
assert len(ids) == len(set(ids)) == 14
assert {n["node_id"] for n in typed["nodes"]} == set(ids)

keys = ["obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason"]
projection = [{k: o[k] for k in keys} for o in obligations]
actual = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert actual == registry["denominator_sha256"]
assert all(o["root_relevant"] and o["machine_eligibility"] == "required" for o in obligations)
counts = registry["eligibility_counts"]
assert counts == {"total": 14, "root_relevant": 14, "machine_required": 14,
                  "human_source_required": 11, "readable_required": 14,
                  "informational": 0}

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
    "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
    "reviewer", "validity"}
for node in typed["nodes"]:
    assert required <= node.keys()
    assert node["machine_debt"] == "M4" and not node["evidence_ids"]
    assert 0 < node["step_budget"] <= 100 and node["semantic_step_ledger"]

edge_ids = set()
for graph in typed["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids
        edge_ids.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]

for graph_name in ("proof", "workflow"):
    edges = typed["graphs"][graph_name]["edges"]
    visiting, visited = set(), set()
    adjacency = {oid: [] for oid in ids}
    for edge in edges:
        adjacency[edge["from"]].append(edge["to"])
    def visit(node):
        assert node not in visiting
        if node in visited:
            return
        visiting.add(node)
        for child in adjacency[node]:
            visit(child)
        visiting.remove(node); visited.add(node)
    for oid in ids:
        visit(oid)

proof = typed["graphs"]["proof"]["edges"]
reachable, changed = {"M0406-ROOT"}, True
while changed:
    changed = False
    for edge in proof:
        if edge["from"] in reachable and edge["to"] not in reachable:
            reachable.add(edge["to"]); changed = True
assert set(ids) - reachable == {"M0406-S-DEFINITIONS", "M0406-S-FOUNDATION", "M0406-X-PROVENANCE"}
boundary = typed["closure_boundary"]
assert boundary["root_machine_debt"] == "M4" and not boundary["closed_obligations"]
assert boundary["minimal_open_root_cut_set"] == ["M0406-T-ENGINE"]
assert not boundary["audit_complete"] and not boundary["theorem_complete"]

lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom "):
    assert forbidden not in lean
for declaration in ("IntegralPointsLieOnProperCurve", "SurfaceDegeneracyEngine",
                    "corvajaZannierTheoremOne_of_engine",
                    "engine_of_corvajaZannierTheoremOne"):
    assert declaration in lean
print(f"ok: 14 obligations, {len(edge_ids)} typed edges, denominator {actual}; root open M4")
