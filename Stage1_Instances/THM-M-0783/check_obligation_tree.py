#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0783 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert reg["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0783-OBLIGATION_TREE"
assert reg["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0783"
assert reg["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert reg["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = reg["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 12 and ids[0] == reg["root_obligation_id"] == "M0783-ROOT"
digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == reg["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert reg["frozen_denominators"]["inventory"] == ids
for eligibility, key in (("required", "required_machine"),):
    assert reg["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == eligibility]
assert reg["frozen_denominators"]["required_human_source"] == [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"]
assert all(0 < row["step_budget"] <= 100 for row in rows)

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
allowed = {"proof_requires", "composes", "logical_decomposition", "expository_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    assert set(graph["out"]) == set(ids) == set(graph["in"])
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])
proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires": children.setdefault(edge["from"], []).append(edge["to"])
visiting, visited = set(), set()
def visit(node):
    assert node not in visiting
    if node in visited: return
    visiting.add(node)
    for child in children.get(node, []): visit(child)
    visiting.remove(node); visited.add(node)
visit("M0783-ROOT")
assert visited == {"M0783-ROOT", "M0783-S-INTERFACE", "M0783-T-ASSEMBLE", "M0783-L-DENSE-FAMILY"}
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_denseFamilySolver" in lean and "#print axioms" in lean
print(f"PASS THM-M-0783 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M4); dense-family solver and release overlays remain open")
