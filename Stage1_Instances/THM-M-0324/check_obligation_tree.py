#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0324 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert reg["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0324-OBLIGATION_TREE"
assert reg["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0324"
assert reg["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert reg["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = reg["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 15 and ids[0] == reg["root_obligation_id"]
digest = hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == reg["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert reg["frozen_denominators"]["inventory"] == ids
for field, eligibility in [("required_machine", "machine_eligibility"), ("required_human_source", "human_source_eligibility"), ("required_readable", "readable_eligibility")]:
    assert reg["frozen_denominators"][field] == [row["obligation_id"] for row in rows if row[eligibility] == "required"]

nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
required_node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
for node in nodes:
    assert required_node_fields <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "source_anchors", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
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
    reciprocal = proof[edge["reciprocal_edge_id"]]
    assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reciprocal["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])

visiting = set()
visited = set()
def visit(node):
    assert node not in visiting
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)
visit("M0324-ROOT")
assert {"M0324-T-ASSEMBLE", "M0324-T-NO-BASIS", "M0324-D-APPROX", "M0324-L-PROJECTIONS"} <= visited

recipes = specs["recipes"]
assert {node["validation_spec_id"] for node in nodes} == {recipe["recipe_id"] for recipe in recipes}
for recipe in recipes:
    assert isinstance(recipe["argv"], list) and recipe["argv"]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
assert set(bundle["closure_boundary"]["first_open_cut"]) == {"M0324-D-APPROX", "M0324-C-SPACE", "M0324-X-SOURCE", "M0324-X-FOUNDATION"}

lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "noBasis_of_basis_implies_property" in lean and "root_of_witness" in lean
assert lean.count("#print axioms") == 2
print(f"PASS THM-M-0324 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); Enflo construction, exact approximation interface, source map, and foundation audit remain open")
