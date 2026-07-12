#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1082 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1082-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-1082"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 10
assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == "M1082-ROOT"
projection = [{key: row[key] for key in fields} for row in rows]
raw = json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
denominator = hashlib.sha256(raw).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
for graph in bundle["graphs"].values():
    for item in graph["edges"]:
        assert item["edge_id"] not in all_edges and item["type"] in allowed
        assert item["from"] in ids and item["to"] in ids
        assert item["edge_id"] in graph["out"][item["from"]]
        assert item["edge_id"] in graph["in"][item["to"]]
        all_edges.add(item["edge_id"])

proof = {item["edge_id"]: item for item in bundle["graphs"]["proof"]["edges"]}
children = {}
for item in proof.values():
    reverse = proof[item["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == item["edge_id"]
    assert (reverse["from"], reverse["to"]) == (item["to"], item["from"])
    assert {item["type"], reverse["type"]} == {"proof_requires", "composes"}
    if item["type"] == "proof_requires":
        children.setdefault(item["from"], []).append(item["to"])

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

visit("M1082-ROOT")
assert visited == {"M1082-ROOT", "M1082-T-COMPOSE", "M1082-T-FORWARD", "M1082-T-REVERSE", "M1082-S-CONTEXT", "M1082-S-BOUNDARY", "M1082-X-DEFINITION"}
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
closure = bundle["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom ", "sorryAx"):
    assert forbidden not in lean
for declaration in ("forward_from_projection", "reverse_from_constructor", "root_of_directions", "#print axioms"):
    assert declaration in lean

print(f"PASS THM-M-1082 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M3); source, trust, provenance, proof acceptance, and release remain open")
