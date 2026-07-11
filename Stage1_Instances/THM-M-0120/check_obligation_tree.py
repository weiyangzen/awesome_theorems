#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0120 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0120-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0120"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = {"obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id"}
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 25 and ids[0] == registry["root_obligation_id"] == "M0120-ROOT"
assert all(fields <= row.keys() for row in rows)
projection = [{k: row[k] for k in sorted(fields)} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
for key, field in (("required_machine", "machine_eligibility"), ("required_human_source", "human_source_eligibility"), ("required_readable", "readable_eligibility")):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == "required"]
assert registry["frozen_denominators"]["inventory"] == ids

node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt",
               "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id",
               "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger",
               "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources",
               "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
for node in nodes:
    assert node_fields <= node.keys() and node["machine_debt"] in {"M3", "M4"}
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
allowed = {"proof_requires", "logical_decomposition", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
seen, adjacency = set(), {}
for name, graph in bundle["graphs"].items():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in seen and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]]
        seen.add(edge["edge_id"])
        if name in {"proof", "refinement"}:
            adjacency.setdefault(edge["from"], []).append(edge["to"])

active, visited = set(), set()
def visit(node):
    assert node not in active, f"cycle at {node}"
    if node in visited:
        return
    active.add(node)
    for child in adjacency.get(node, []):
        visit(child)
    active.remove(node); visited.add(node)
visit("M0120-ROOT")
assert set(ids) <= visited
assert bundle["closure_boundary"]["closed_obligations"] == []
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False

lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "conclusion_of_packages" in lean and "#print axioms" in lean
print(f"PASS THM-M-0120 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root remains M3; all substantive geometric proof packages remain open")
