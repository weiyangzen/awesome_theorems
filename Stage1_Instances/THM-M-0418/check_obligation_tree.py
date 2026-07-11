#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-0418 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
instance = json.loads((HERE / "instance.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0418-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0418"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 14
assert ids[0] == registry["root_obligation_id"] == "M0418-ROOT"
wire = json.dumps([{key: row[key] for key in fields} for row in rows], sort_keys=True, separators=(",", ":")).encode()
denominator = hashlib.sha256(wire).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert instance["obligation_registry_hash"] == "sha256:" + denominator
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "evidence_for", "provenance_of", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])

proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])

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

visit("M0418-ROOT")
assert visited == {"M0418-ROOT", "M0418-T-ADAPTER", "M0418-T-UPSTREAM-BODY", "M0418-N-INVERSE-CLASS", "M0418-L-MINKOWSKI-ELEMENT", "M0418-C-QUOTIENT-IDEAL", "M0418-C-NONZERO-IDEAL", "M0418-L-CLASS-IDENTITY", "M0418-L-NORM-TRANSPORT"}
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
for recipe in specs["recipes"]:
    assert {"cwd", "argv", "env", "timeout_seconds", "network", "covered_ids"} <= recipe.keys()
assert bundle["closure_boundary"]["root_closed"] is True
assert bundle["closure_boundary"]["theorem_complete"] is False
assert len(bundle["closure_boundary"]["distinct_terminal_proof_bodies"]) == 1
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "minkowskiIdealClassBound_obligationRoot" in lean and "#print axioms" in lean

print(f"PASS THM-M-0418 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root machine closure: M0-W via one pinned mathlib terminal body; theorem completion remains false")
