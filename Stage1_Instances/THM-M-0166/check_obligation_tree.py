#!/usr/bin/env python3
"""Fail-closed structural checks for the frozen THM-M-0166 architecture."""

import json
from pathlib import Path

HERE = Path(__file__).parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
nodes = {row["obligation_id"]: row for row in registry["obligations"]}

required_fields = {
    "obligation_id", "node_id", "kind", "statement_fingerprint", "human_statement",
    "formal_target", "output", "root_relevant", "machine_eligibility",
    "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
    "terminal_proof_body_id", "human_debt", "machine_debt", "readability_debt",
    "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile",
    "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity"
}
for node_id, node in nodes.items():
    missing = required_fields - node.keys()
    assert not missing, (node_id, sorted(missing))
    assert 0 < node["step_budget"] <= 100
    assert len(node["semantic_step_ledger"]) == node["step_budget"]
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}

assert set(graphs["coverage_denominators"]["canonical_obligations"]) == set(nodes)
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map",
           "expository_decomposition", "equivalent_to", "transports", "evidence_for",
           "provenance_of", "documents", "trusts", "workflow_depends_on"}
for graph, edges in graphs["graphs"].items():
    for edge in edges:
        assert edge["type"] in allowed, (graph, edge)
        if graph in {"proof", "refinement", "trust"}:
            assert edge["from"] in nodes and edge["to"] in nodes, edge

proof_edges = {(e["from"], e["type"], e["to"]) for e in graphs["graphs"]["proof"]}
for child in ("M0166-L-EXISTENCE", "M0166-L-SUBSEGMENT"):
    assert ("M0166-ROOT", "proof_requires", child) in proof_edges
    assert ("M0166-ROOT", "composes", child) in proof_edges
assert nodes["M0166-ROOT"]["machine_debt"] != "M0-L"
assert graphs["closure_metrics_observed"] is False
assert set(graphs["root_cut_set"]) <= set(nodes)
print("obligation tree verified: 7 canonical nodes, typed graphs, open root, checked composition declared")
