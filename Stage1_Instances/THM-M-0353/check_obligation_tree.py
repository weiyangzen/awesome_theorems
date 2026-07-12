#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0353 obligation freeze."""
import hashlib
import json
from pathlib import Path

H = Path(__file__).resolve().parent
r = json.loads((H / "obligation-registry.json").read_text())
b = json.loads((H / "typed-graphs.json").read_text())
assert r["item_id"] == b["item_id"] == "S56-M-0353-OBLIGATION_TREE"
assert r["theorem_id"] == b["theorem_id"] == "THM-M-0353"
assert r["frozen_against_statement_sha256"] == hashlib.sha256((H / "Statement.lean").read_bytes()).hexdigest()
assert r["frozen_against_anchor_audit_sha256"] == hashlib.sha256((H / "anchor-audit.json").read_bytes()).hexdigest()
rows = r["obligations"]
ids = [x["obligation_id"] for x in rows]
fields = tuple(rows[0])
assert len(ids) == len(set(ids)) == 16 and ids[0] == r["root_obligation_id"]
digest = hashlib.sha256(json.dumps([{k: x[k] for k in fields} for x in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == r["denominator_sha256"] == b["registry_denominator_sha256"]
assert r["frozen_denominators"]["inventory"] == ids
nodes = b["nodes"]
assert len(nodes) == 16 and {n["obligation_id"] for n in nodes} == set(ids)
required_node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
for node in nodes:
    assert required_node_fields <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "workflow_depends_on"}
seen = set()
for graph in b["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in seen and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        seen.add(edge["edge_id"])
proof = {e["edge_id"]: e for e in b["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reciprocal = proof[edge["reciprocal_edge_id"]]
    assert reciprocal["reciprocal_edge_id"] == edge["edge_id"]
    assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])
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
visit("M0353-ROOT")
expected = {"M0353-ROOT", "M0353-T-ASSEMBLE", "M0353-P-MEMLP", "M0353-P-BASIS", "M0353-C-LP-VECTORS", "M0353-L-ORTHONORMAL", "M0353-L-DENSE", "M0353-C-HILBERT-BASIS", "M0353-L-GAUSSIAN-ORTH", "M0353-L-POLY-DENSE", "M0353-T-MEASURE", "M0353-S-NORMALIZATION", "M0353-X-HERMITE-POLY"}
assert visited == expected
assert b["closure_boundary"] == {"root_closed": False, "theorem_complete": False, "minimal_open_root_cut": ["M0353-P-MEMLP", "M0353-P-BASIS"]}
lean = (H / "ObligationTree.lean").read_text()
assert all(x not in lean for x in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_hermite_packages" in lean and "#print axioms" in lean
print(f"PASS THM-M-0353 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); MemLp and HilbertBasis packages remain M4")
