#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0529 frozen obligation tree."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == registry["frozen_against_statement_sha256"]
assert hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest() == registry["frozen_against_anchor_audit_sha256"]
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [r["obligation_id"] for r in rows]
projection = [{k: r[k] for k in fields} for r in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert len(ids) == len(set(ids)) == 7
assert ids[0] == registry["root_obligation_id"] == "M0529-ROOT"
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids

nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "semantic_step_ledger", "step_budget", "validation_spec_id", "validity"}
for node in nodes:
    assert required_node <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidenced_by", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in all_edges and e["type"] in allowed
        assert e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        all_edges.add(e["edge_id"])

proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for e in proof.values():
    reverse = proof[e["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == e["edge_id"]
    assert (reverse["from"], reverse["to"]) == (e["to"], e["from"])
    assert {e["type"], reverse["type"]} == {"proof_requires", "composes"}
    if e["type"] == "proof_requires":
        children.setdefault(e["from"], []).append(e["to"])

visited = set()
def visit(node):
    if node in visited:
        return
    visited.add(node)
    for child in children.get(node, []):
        visit(child)
visit("M0529-ROOT")
assert visited == {"M0529-ROOT", "M0529-C-MAP", "M0529-B-HOMEO", "M0529-B-FUNCTOR"}
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
for recipe in specs["recipes"]:
    assert {"cwd", "argv", "env", "timeout_seconds", "network", "covered_ids"} <= recipe.keys()
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "map_isIso_of_source_isIso" in lean and "#print axioms" in lean
print(f"PASS THM-M-0529 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); proof-phase bridge acceptance and provenance remain open")
