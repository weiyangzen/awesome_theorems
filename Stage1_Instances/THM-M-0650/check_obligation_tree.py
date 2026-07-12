#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-0650 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
instance = json.loads((HERE / "instance.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0650-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0650"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 19
assert ids[0] == registry["root_obligation_id"] == "M0650-ROOT"
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert instance["obligation_registry_hash"] == "sha256:" + digest
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]
assert registry["frozen_denominators"]["required_human_source"] == [row["obligation_id"] for row in rows if row["human_source_eligibility"] == "required"]

required_node = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity",
}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "source_anchors", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    assert node["task_ids"] == ["S56-M-0650-OBLIGATION_TREE", "S56-M-0650-PROOF"]

allowed = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "provenance_of", "trusts", "documents", "workflow_depends_on",
}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
for graph in bundle["graphs"].values():
    for row in graph["edges"]:
        assert row["edge_id"] not in all_edges and row["type"] in allowed
        assert row["from"] in ids and row["to"] in ids
        assert row["edge_id"] in graph["out"][row["from"]]
        assert row["edge_id"] in graph["in"][row["to"]]
        all_edges.add(row["edge_id"])

proof = {row["edge_id"]: row for row in bundle["graphs"]["proof"]["edges"]}
children = {}
for row in proof.values():
    reverse = proof[row["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == row["edge_id"]
    assert (reverse["from"], reverse["to"]) == (row["to"], row["from"])
    assert {row["type"], reverse["type"]} == {"proof_requires", "composes"}
    if row["type"] == "proof_requires":
        children.setdefault(row["from"], []).append(row["to"])

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


visit("M0650-ROOT")
assert visited == {
    "M0650-ROOT", "M0650-T-SUBSTRUCTURE", "M0650-N-SUBTYPE",
    "M0650-N-WITNESS", "M0650-T-EMBEDDING", "M0650-B-FORMULA",
    "M0650-B-ATOMIC", "M0650-B-IMPLIES", "M0650-B-FORALL",
    "M0650-L-WITNESS-NOT", "M0650-L-REINDEX",
}
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
assert {covered for recipe in specs["recipes"] for covered in recipe["covered_obligation_ids"]} == set(ids)
closure = bundle["closure_boundary"]
assert closure["root_closed"] is False and closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == ["M0650-T-EMBEDDING"]
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_embeddingTarskiVaughtPackage" in lean and "#print axioms" in lean

print(f"PASS THM-M-0650 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); pinned embedding body is an uncredited proof-phase candidate")
