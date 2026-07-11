#!/usr/bin/env python3
"""Validate the THM-M-0005 frozen registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
load = lambda name: json.loads((HERE / name).read_text())
registry, bundle, specs = map(load, ("obligation-registry.json", "typed-graphs.json", "validation-specs.json"))

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0005-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0005"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "KunnethStatement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor_candidates.json").read_bytes()).hexdigest()
rows, nodes = registry["obligations"], bundle["nodes"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == len(nodes) == 18 and registry["root_obligation_id"] == "M0005-ROOT"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
digest = hashlib.sha256(json.dumps([{k: r[k] for k in fields} for r in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
assert {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert 0 < node["step_budget"] <= 100
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}
    assert set(node["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"}

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
allowed = {"proof_requires", "composes", "logical_decomposition", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])

proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])
active, visited = set(), set()
def visit(node):
    assert node not in active
    if node in visited: return
    active.add(node)
    for child in children.get(node, []): visit(child)
    active.remove(node); visited.add(node)
visit("M0005-ROOT")
assert set(registry["frozen_denominators"]["required_machine"]) <= visited | {"M0005-SCOPE"}

recipe_ids = {r["recipe_id"] for r in specs["recipes"]}
assert len(recipe_ids) == len(ids) and recipe_ids == {n["validation_spec_id"] for n in nodes}
boundary = bundle["closure_boundary"]
assert boundary["closed_obligations"] == [] and not boundary["root_closed"]
assert not boundary["audit_complete"] and not boundary["theorem_complete"]
lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom ", "sorryAx"):
    assert forbidden not in lean
assert "assemble_sequence" in lean and "root_compose" in lean

print(f"PASS THM-M-0005 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root remains open at M3; no obligation receives closure credit")
