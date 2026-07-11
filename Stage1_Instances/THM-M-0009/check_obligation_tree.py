#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0009 obligation architecture."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0009-OBLIGATION_TREE"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = registry["obligations"]
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 15 and registry["root_obligation_id"] in ids
assert registry["frozen_denominators"]["inventory"] == ids
assert {n["obligation_id"] for n in bundle["nodes"]} == set(ids)
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}

edge_ids = set()
proof_requires = {}
composes = {}
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["from"] in ids and edge["to"] in ids
        edge_ids.add(edge["edge_id"])
        if edge["type"] == "proof_requires": proof_requires[edge["edge_id"]] = edge
        if edge["type"] == "composes": composes[edge["edge_id"]] = edge
for edge in proof_requires.values():
    rev = composes[edge["reciprocal_edge_id"]]
    assert rev["from"] == edge["to"] and rev["to"] == edge["from"] and rev["reciprocal_edge_id"] == edge["edge_id"]

# Proof-requires edges must be acyclic and every required root-relevant node must be reachable.
children = {}
for edge in proof_requires.values(): children.setdefault(edge["from"], []).append(edge["to"])
seen, active = set(), set()
def visit(node):
    assert node not in active
    if node in seen: return
    active.add(node)
    for child in children.get(node, []): visit(child)
    active.remove(node); seen.add(node)
visit(registry["root_obligation_id"])
assert set(bundle["closure_boundary"]["remaining_root_cut_set"]) == {"M0009-L-COV-EXACT", "M0009-L-CONTRA-EXACT"}
assert bundle["closure_boundary"]["closed_obligations"] == [] and not bundle["closure_boundary"]["root_closed"]

recipe_ids = {r["recipe_id"] for r in specs["recipes"]}
for node in bundle["nodes"]:
    assert 0 < node["step_budget"] <= 100
    assert set(node["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"}
    assert node["validation_spec_id"] in recipe_ids
for recipe in specs["recipes"]:
    assert recipe["cwd"] == "Formalizations/Lean" and recipe["argv"][:3] == ["lake", "env", "lean"]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert set(recipe["covered_obligation_ids"]) <= set(ids)

lean = (HERE / "ObligationTree.lean").read_text()
assert not re.search(r"\b(sorry|admit|axiom|unsafe|implemented_by)\b", lean)
assert "theorem root_compose" in lean and "cov : CovariantBranch" in lean and "contra : ContravariantBranch" in lean
print(f"validated {len(ids)} obligations, {len(edge_ids)} typed edges, reciprocal composition, recipes, budgets, and open-root boundary")
