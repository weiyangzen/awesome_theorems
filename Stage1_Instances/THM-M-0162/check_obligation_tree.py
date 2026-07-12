#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0162 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
recipes = json.loads((HERE / "validation-specs.json").read_text())
obligations = registry["obligations"]
ids = [row["obligation_id"] for row in obligations]
assert len(ids) == len(set(ids)) and registry["root_obligation_id"] in ids
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
encoded = json.dumps([{key: row[key] for key in fields} for row in obligations], sort_keys=True, separators=(",", ":")).encode()
denominator = hashlib.sha256(encoded).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
assert {node["obligation_id"] for node in bundle["nodes"]} == set(ids)
assert {recipe["obligation_id"] for recipe in recipes["recipes"]} == set(ids)
all_edges = []
for graph in bundle["graphs"].values():
    all_edges.extend(graph["edges"])
    for item in graph["edges"]:
        assert item["from"] in ids and item["to"] in ids
edge_map = {item["edge_id"]: item for item in all_edges}
assert len(edge_map) == len(all_edges)
for item in bundle["graphs"]["proof"]["edges"]:
    reciprocal = edge_map[item["reciprocal_edge_id"]]
    assert reciprocal["from"] == item["to"] and reciprocal["to"] == item["from"]
    assert {item["type"], reciprocal["type"]} == {"proof_requires", "composes"}
requires = [item for item in bundle["graphs"]["proof"]["edges"] if item["type"] == "proof_requires"]
children = {}
for item in requires:
    children.setdefault(item["from"], []).append(item["to"])
seen, active = set(), set()
def visit(node):
    assert node not in active
    if node in seen:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    seen.add(node)
visit(registry["root_obligation_id"])
assert all(node in seen for node in bundle["closure_boundary"]["remaining_root_cut_set"])
assert not bundle["closure_boundary"]["root_closed"]
print(f"PASS THM-M-0162 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M3); tangent, normal, and binormal equation packages remain M4")
