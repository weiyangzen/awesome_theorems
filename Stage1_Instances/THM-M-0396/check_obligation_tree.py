#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-0396 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0396"
assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == registry["frozen_against_statement_sha256"]
assert hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest() == registry["frozen_against_anchor_audit_sha256"]

required_registry = {"obligation_id", "statement_fingerprint", "kind", "root_relevant",
                     "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                     "risk_class", "exclusion_reason", "terminal_proof_body_id"}
required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
                 "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
                 "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
                 "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
                 "task_ids", "owned_sources", "owner", "reviewer", "validity"}
rows = registry["obligations"]
assert len(rows) == 15 and all(required_registry <= set(row) for row in rows)
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) and registry["root_obligation_id"] == "M0396-ROOT"
assert all(row["root_relevant"] for row in rows)
assert [row["obligation_id"] for row in rows if row["machine_eligibility"] == "not_applicable"] == ["M0396-X1"]
assert all(row["human_source_eligibility"] == row["readable_eligibility"] == "required" for row in rows)

projection_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
                     "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                     "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in projection_fields} for row in rows]
actual_hash = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert actual_hash == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]

nodes = bundle["nodes"]
assert len(nodes) == len(ids) and all(required_node <= set(node) for node in nodes)
assert {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    budget = node["step_budget"]
    assert budget == "split-required" or isinstance(budget, int) and 0 < budget <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= set(node["semantic_step_ledger"])

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of",
           "evidence_for", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
for graph in bundle["graphs"].values():
    edge_ids = {edge["edge_id"] for edge in graph["edges"]}
    assert len(edge_ids) == len(graph["edges"])
    assert all(edge["type"] in allowed for edge in graph["edges"])
    assert {edge_id for values in graph["in"].values() for edge_id in values} <= edge_ids
    assert {edge_id for values in graph["out"].values() for edge_id in values} <= edge_ids

proof = bundle["graphs"]["proof"]["edges"]
proof_by_id = {edge["edge_id"]: edge for edge in proof}
for edge in proof:
    reciprocal = proof_by_id[edge["reciprocal_edge_id"]]
    assert reciprocal["reciprocal_edge_id"] == edge["edge_id"]
    assert reciprocal["from"] == edge["to"] and reciprocal["to"] == edge["from"]
    assert {edge["type"], reciprocal["type"]} == {"proof_requires", "composes"}

requires = [(edge["from"], edge["to"]) for edge in proof if edge["type"] == "proof_requires"]
children = {}
for parent, child in requires:
    assert parent in ids and child in ids
    children.setdefault(parent, []).append(child)
visiting, visited = set(), set()
def visit(node):
    assert node not in visiting, f"proof cycle at {node}"
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)
visit("M0396-ROOT")
assert {"M0396-ROOT", "M0396-T", "M0396-N1", "M0396-N2", "M0396-C1", "M0396-C2",
        "M0396-L1", "M0396-L2", "M0396-L3", "M0396-L4"} == visited

recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
assert all(node["validation_spec_id"] in recipe_ids for node in nodes)
assert bundle["closure_boundary"] == {
    "closed_obligations": ["M0396-S2", "M0396-S3"], "root_closed": False,
    "audit_complete": False, "theorem_complete": False,
    "remaining_root_cut_set": ["M0396-T"],
    "reason": "No terminal Baker-Matveev proof body was located or implemented."
}
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_compose" in lean and "#print axioms root_compose" in lean
print(f"PASS THM-M-0396 obligation tree: {len(ids)} obligations, {len(requires)} proof requirements; root M3/open")
