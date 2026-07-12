#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-0452 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0452-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0452"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 23
assert ids[0] == registry["root_obligation_id"] == "M0452-ROOT"
projection = [{key: row[key] for key in fields} for row in rows]
encoded = json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
denominator = hashlib.sha256(encoded).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
for graph in bundle["graphs"].values():
    for relation in graph["edges"]:
        assert relation["edge_id"] not in all_edges and relation["type"] in allowed
        assert relation["from"] in ids and relation["to"] in ids
        assert relation["edge_id"] in graph["out"][relation["from"]]
        assert relation["edge_id"] in graph["in"][relation["to"]]
        all_edges.add(relation["edge_id"])

proof = {relation["edge_id"]: relation for relation in bundle["graphs"]["proof"]["edges"]}
children = {}
for relation in proof.values():
    reverse = proof[relation["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == relation["edge_id"]
    assert (reverse["from"], reverse["to"]) == (relation["to"], relation["from"])
    assert {relation["type"], reverse["type"]} == {"proof_requires", "composes"}
    if relation["type"] == "proof_requires":
        children.setdefault(relation["from"], []).append(relation["to"])

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

visit("M0452-ROOT")
expected_proof_nodes = {"M0452-ROOT", "M0452-T-ASSEMBLE", "M0452-H-LIMIT", "M0452-H-NAIVE", "M0452-H-DUPLICATION", "M0452-H-CAUCHY", "M0452-P-ASSEMBLE", "M0452-Q-QUADRATIC", "M0452-P-POLARIZATION", "M0452-P-ADDITIVITY", "M0452-P-ZSMUL", "M0452-K-KERNEL", "M0452-K-NONNEG", "M0452-K-TORSION-FWD", "M0452-K-ZERO-TORSION", "M0452-K-BOUNDED-HEIGHT", "M0452-D-POSITIVE", "M0452-D-WELLDEFINED"}
assert visited == expected_proof_nodes
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["audit_complete"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M0452-H-LIMIT", "M0452-P-ASSEMBLE", "M0452-D-POSITIVE"]

lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_height_polarization_quotient" in lean and "#print axioms" in lean
print(f"PASS THM-M-0452 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M3); height, polarization, and quotient packages remain M4")
