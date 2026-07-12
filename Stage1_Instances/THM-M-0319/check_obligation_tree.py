#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-0319 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == "S56-M-0319-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-0319"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 12
assert ids[0] == registry["root_obligation_id"] == "M0319-ROOT"
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
for dimension, eligibility in (("required_machine", "machine_eligibility"), ("required_human_source", "human_source_eligibility"), ("required_readable", "readable_eligibility")):
    assert registry["frozen_denominators"][dimension] == [r["obligation_id"] for r in rows if r[eligibility] == "required"]

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
for graph in bundle["graphs"].values():
    assert set(graph["out"]) == set(graph["in"]) == set(ids)
    for value in graph["edges"]:
        assert value["edge_id"] not in all_edges and value["type"] in allowed
        assert value["from"] in ids and value["to"] in ids
        assert value["edge_id"] in graph["out"][value["from"]]
        assert value["edge_id"] in graph["in"][value["to"]]
        all_edges.add(value["edge_id"])

proof = {value["edge_id"]: value for value in bundle["graphs"]["proof"]["edges"]}
children = {}
for value in proof.values():
    reverse = proof[value["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == value["edge_id"]
    assert (reverse["from"], reverse["to"]) == (value["to"], value["from"])
    assert {value["type"], reverse["type"]} == {"proof_requires", "composes"}
    if value["type"] == "proof_requires":
        children.setdefault(value["from"], []).append(value["to"])

visiting, visited = set(), set()
def visit(node):
    assert node not in visiting
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)

visit("M0319-ROOT")
assert visited == {"M0319-ROOT", "M0319-T-SUBTYPE", "M0319-T-EXTERNAL", "M0319-N-FINITE-DIM", "M0319-R-CONVEX-CUBE", "M0319-L-UNIT-CUBE"}
assert bundle["closure_boundary"] == {"root_closed": False, "minimal_open_root_cut": ["M0319-T-EXTERNAL"], "theorem_complete": False}
lean = (HERE / "ObligationTree.lean").read_text()
for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in lean
assert "root_of_external_body" in lean and "#print axioms" in lean
print(f"PASS THM-M-0319 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); external terminal body remains outside pinned closure")
