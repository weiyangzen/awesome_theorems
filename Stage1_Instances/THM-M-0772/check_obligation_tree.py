#!/usr/bin/env python3
"""Validate THM-M-0772's frozen registry and typed graph contracts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0772-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0772"
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 13 and registry["root_obligation_id"] == "M0772-ROOT"
assert {row["kind"] for row in rows} <= {"root", "definition", "reduction", "branch", "construction", "lemma", "computation", "transport", "terminal"}

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
raw = json.dumps([{key: row[key] for key in fields} for row in rows], sort_keys=True, separators=(",", ":")).encode()
denominator = hashlib.sha256(raw).hexdigest()
assert registry["denominator_sha256"] == bundle["registry_denominator_sha256"] == denominator
for field, key in (("machine_eligibility", "required_machine"), ("human_source_eligibility", "required_human_source"), ("readable_eligibility", "required_readable")):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == "required"]

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "evidence_for", "provenance_of", "trusts", "documents", "workflow_depends_on"}
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
    assert node not in visiting, f"proof cycle at {node}"
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)
visit("M0772-ROOT")
assert {"M0772-ROOT", "M0772-T-ADAPTER", "M0772-N-RELATION", "M0772-C-WITNESS", "M0772-L-MAXCHAIN", "M0772-X-MATHLIB-BODY"} <= visited

assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in specs["recipes"]}
for recipe in specs["recipes"]:
    assert isinstance(recipe["argv"], list) and recipe["network_policy"] == "denied"
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M0772-X-MATHLIB-BODY"]
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_relationGenericMaxChain" in lean and "#print axioms" in lean
print(f"PASS THM-M-0772 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M3); imported body provenance and master proof acceptance remain downstream")
