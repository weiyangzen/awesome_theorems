#!/usr/bin/env python3
"""Validate frozen denominators, typed graphs, and phase boundaries."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
recipes = json.loads((HERE / "validation-specs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == recipes["item_id"] == "S56-M-0416-OBLIGATION_TREE"
obligations = registry["obligations"]
ids = [row["obligation_id"] for row in obligations]
assert len(ids) == len(set(ids)) == 9
assert registry["frozen_denominators"]["inventory"] == ids
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator = digest([{key: row[key] for key in fields} for row in obligations])
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == registry["frozen_against_statement_sha256"]
assert hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest() == registry["frozen_against_anchor_audit_sha256"]
assert {node["obligation_id"] for node in bundle["nodes"]} == set(ids)
required_node_fields = {"semantic_step_ledger", "step_budget", "formal_target", "validation_spec_id", "validity", "status_boundary"}
assert all(required_node_fields <= set(node) and node["step_budget"] <= 100 for node in bundle["nodes"])
all_edges = []
for graph in bundle["graphs"].values():
    all_edges += graph["edges"]
    by_id = {edge["edge_id"]: edge for edge in graph["edges"]}
    assert len(by_id) == len(graph["edges"])
    for node, edge_ids in graph["out"].items():
        assert all(by_id[e]["from"] == node for e in edge_ids)
    for node, edge_ids in graph["in"].items():
        assert all(by_id[e]["to"] == node for e in edge_ids)
proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
for item in proof.values():
    reciprocal = proof[item["reciprocal_edge_id"]]
    assert reciprocal["from"] == item["to"] and reciprocal["to"] == item["from"]
assert {recipe["obligation_id"] for recipe in recipes["recipes"]} == set(ids)
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "axiom ", "native_decide", "unsafe", "external "):
    assert forbidden not in lean
assert "theorem root_of_packages" in lean and "#print axioms root_of_packages" in lean
print(f"PASS THM-M-0416 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M3); four candidate packages await proof integration and later gates")
