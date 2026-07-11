#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0085 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
load = lambda name: json.loads((HERE / name).read_text())
registry, bundle, specs = load("obligation-registry.json"), load("typed-graphs.json"), load("validation-specs.json")
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0085-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0085"
digest = lambda p: hashlib.sha256((HERE / p).read_bytes()).hexdigest()
assert registry["frozen_against_statement_sha256"] == digest("Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == digest("anchor-audit.json")
rows, ids = registry["obligations"], registry["frozen_denominators"]["inventory"]
assert len(ids) == len(set(ids)) == len(rows) == 5
assert ids == [r["obligation_id"] for r in rows] and ids[0] == registry["root_obligation_id"]
projection = [{k: r[k] for k in r} for r in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert {n["obligation_id"] for n in bundle["nodes"]} == set(ids)
for node in bundle["nodes"]:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]] and edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])
proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
assert {n["validation_spec_id"] for n in bundle["nodes"]} == {r["recipe_id"] for r in specs["recipes"]}
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "monadicOfCreatesGSplitCoequalizers" in lean and "letI" in lean and "#print axioms" in lean
print(f"PASS THM-M-0085 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open; exact pinned candidate composition elaborated, named proof and receipts pending")
