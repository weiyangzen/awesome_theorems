#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1184 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == "S56-M-1184-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-1184"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 16 and ids[0] == registry["root_obligation_id"] == "M1184-ROOT"
projection = [{k: r[k] for k in fields} for r in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
required = {"node_id", "obligation_id", "human_statement", "formal_target", "human_debt", "machine_debt", "readability_debt", "step_budget", "semantic_step_ledger", "validation_spec_id", "status_boundary", "task_ids", "validity"}
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
seen = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in seen and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]]
        seen.add(edge["edge_id"])
proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])
visiting, visited = set(), set()
def visit(node):
    assert node not in visiting
    if node in visited: return
    visiting.add(node)
    for child in children.get(node, []): visit(child)
    visiting.remove(node); visited.add(node)
visit("M1184-ROOT")
assert visited == {"M1184-ROOT", "M1184-T-ASSEMBLE", "M1184-T-WEAK", "M1184-W-ORDER", "M1184-W-INTEGRATE", "M1184-C-PRODUCT", "M1184-C-CONSTANT", "M1184-T-STRONG", "M1184-W-REVERSE", "M1184-L-GAP", "M1184-S-SEPARATION", "M1184-C-POTENTIALS"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_duality_packages" in lean and "#print axioms" in lean
print(f"PASS THM-M-1184 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M2); weak and reverse duality packages remain open")
