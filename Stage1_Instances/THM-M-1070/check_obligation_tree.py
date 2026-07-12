#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1070 architecture freeze."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
recipes = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == recipes["item_id"] == "S56-M-1070-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == recipes["theorem_id"] == "THM-M-1070"
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 13
assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == "M1070-ROOT"

row_fields = {"obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
              "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
              "terminal_proof_body_id"}
assert all(row_fields <= row.keys() for row in rows)
assert all(row["statement_fingerprint"].startswith(("lean-expression-sha256:", "planned:v1:sha256:")) for row in rows)

canonical = [{key: row[key] for key in (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
    "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
    "terminal_proof_body_id")} for row in rows]
denominator = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

frozen = registry["frozen_denominators"]
assert frozen["inventory"] == ids
assert frozen["required_machine"] == [row["obligation_id"] for row in rows if row["machine_eligibility"] == "required"]
assert frozen["required_human_source"] == [row["obligation_id"] for row in rows if row["human_source_eligibility"] == "required"]
assert frozen["required_readable"] == ids
assert set(frozen["informational_overlays"]) == {"M1070-X-SOURCE", "M1070-X-PROVENANCE"}

node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
               "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
               "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
               "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
               "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert [node["node_id"] for node in nodes] == ids
assert all(node_fields <= node.keys() for node in nodes)
assert all(0 < node["step_budget"] <= 100 and node["step_budget"] == len(node["semantic_step_ledger"]) for node in nodes)
assert {recipe["obligation_id"] for recipe in recipes["recipes"]} == set(ids)
assert {recipe["recipe_id"] for recipe in recipes["recipes"]} == {node["validation_spec_id"] for node in nodes}

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids = set()
composes = {}
for graph_name, graph in bundle["graphs"].items():
    for item in graph["edges"]:
        assert item["edge_id"] not in edge_ids
        edge_ids.add(item["edge_id"])
        assert item["from"] in ids and item["to"] in ids
        assert item["edge_id"] in graph["out"].get(item["from"], [])
        assert item["edge_id"] in graph["in"].get(item["to"], [])
        if graph_name == "proof":
            assert item["type"] in {"proof_requires", "composes"}
            if item["type"] == "composes":
                composes.setdefault(item["from"], []).append(item["to"])
            reciprocal = item.get("reciprocal_edge_id")
            assert reciprocal and any(other["edge_id"] == reciprocal and other["from"] == item["to"] and other["to"] == item["from"] for other in graph["edges"])

def reaches_root(start):
    frontier, seen = [start], set()
    while frontier:
        current = frontier.pop()
        if current == "M1070-ROOT":
            return True
        assert current not in seen, f"composition cycle at {current}"
        seen.add(current)
        frontier.extend(composes.get(current, []))
    return False

semantic_required = [oid for oid in frozen["required_machine"] if oid not in {"M1070-S-DEFINITIONS", "M1070-S-BOUNDARY", "M1070-S-FOUNDATION"}]
assert all(reaches_root(oid) for oid in semantic_required)
closure = bundle["closure_boundary"]
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M3"
assert set(closure["remaining_root_cut_set"]) <= set(frozen["required_machine"])

for path in HERE.glob("*.lean"):
    text = path.read_text()
    assert not re.search(r"\b(sorry|admit)\b", text)
    assert not re.search(r"^\s*axiom\b", text, re.MULTILINE)

print(f"PASS THM-M-1070 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M3); all six process clauses remain explicit premises")
