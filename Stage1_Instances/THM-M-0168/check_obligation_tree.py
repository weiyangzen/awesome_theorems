#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0168 obligation architecture."""

import json
from pathlib import Path

HERE = Path(__file__).parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
nodes = {n["obligation_id"]: n for n in registry["obligations"]}

fields = {"obligation_id", "node_id", "kind", "statement_fingerprint", "human_statement",
 "formal_target", "output", "root_relevant", "machine_eligibility", "human_source_eligibility",
 "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id", "human_debt",
 "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id",
 "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger",
 "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources",
 "owner", "reviewer", "validity"}
assert len(nodes) == 11
for oid, n in nodes.items():
    assert not fields - n.keys(), (oid, sorted(fields - n.keys()))
    assert 0 < n["step_budget"] <= 100
    assert n["step_budget"] == len(n["semantic_step_ledger"])
    assert n["machine_eligibility"] == "required"

assert set(bundle["coverage_denominators"]["canonical_obligations"]) == set(nodes)
internal = {"proof", "refinement", "trust"}
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "evidence_for",
 "provenance_of", "documents", "trusts", "workflow_depends_on"}
for graph, edges in bundle["graphs"].items():
    for e in edges:
        assert e["type"] in allowed
        if graph in internal:
            assert e["from"] in nodes and e["to"] in nodes, e

proof = {(e["from"], e["type"], e["to"]) for e in bundle["graphs"]["proof"]}
for child in ("M0168-L-DERIVATIVE-RIGIDITY", "M0168-T-INTEGRATE"):
    assert ("M0168-ROOT", "proof_requires", child) in proof
    assert ("M0168-ROOT", "composes", child) in proof
assert nodes["M0168-ROOT"]["machine_debt"] == "M2"
assert bundle["closure_metrics_observed"] is False
assert set(bundle["root_cut_set"]) <= set(nodes)

# Proof-requires edges must be acyclic when directed parent -> prerequisite.
adj = {x: [] for x in nodes}
for a, typ, b in proof:
    if typ == "proof_requires": adj[a].append(b)
seen, active = set(), set()
def visit(x):
    assert x not in active, f"proof cycle at {x}"
    if x in seen: return
    active.add(x)
    for y in adj[x]: visit(y)
    active.remove(x); seen.add(x)
visit("M0168-ROOT")
assert set(nodes) - seen == {"M0168-S-INTERFACE", "M0168-X-SOURCE", "M0168-X-TRUST"}
print("obligation tree verified: 11 nodes, typed acyclic proof graph, frozen open root")
