#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-1333 architecture."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == "S56-M-1333-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-1333"
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 16
assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == "M1333-ROOT"

required = {"obligation_id", "statement_fingerprint", "kind", "root_relevant",
            "machine_eligibility", "human_source_eligibility", "readable_eligibility",
            "risk_class", "exclusion_reason", "terminal_proof_body_id"}
assert all(required <= row.keys() for row in rows)
assert all(row["statement_fingerprint"].startswith(("lean-source-sha256:", "planned:v1:sha256:")) for row in rows)
assert all(row["terminal_proof_body_id"] is None for row in rows)

denominator = registry["frozen_denominators"]
assert denominator["inventory"] == ids
assert denominator["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
assert denominator["required_human_source"] == [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"]
assert denominator["required_readable"] == ids
assert denominator["informational_overlays"] == ["M1333-X-PROVENANCE"]
digest = hashlib.sha256(json.dumps(denominator, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert registry["denominator_sha256"] == bundle["registry_denominator_sha256"] == digest

assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

nodes = bundle["nodes"]
assert [n["obligation_id"] for n in nodes] == ids
node_required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
                 "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
                 "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
                 "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
                 "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert all(node_required <= n.keys() for n in nodes)
assert all(isinstance(n["step_budget"], int) and 0 < n["step_budget"] <= 100 for n in nodes)
assert all(0 < len(n["semantic_step_ledger"]) <= n["step_budget"] for n in nodes)
assert all(n["public_readable_target"].endswith("#" + n["obligation_id"].lower()) for n in nodes)

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
semantic_adjacency = {}
for name, graph in bundle["graphs"].items():
    edge_ids = [edge["edge_id"] for edge in graph["edges"]]
    assert len(edge_ids) == len(set(edge_ids))
    assert not all_edges.intersection(edge_ids)
    all_edges.update(edge_ids)
    for edge in graph["edges"]:
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
        if name in {"proof", "refinement"}:
            semantic_adjacency.setdefault(edge["from"], []).append(edge["to"])


def reaches_root(start):
    frontier, seen = [start], set()
    while frontier:
        current = frontier.pop()
        if current == "M1333-ROOT":
            return True
        assert current not in seen, f"semantic cycle at {current}"
        seen.add(current)
        frontier.extend(semantic_adjacency.get(current, []))
    return False


assert all(reaches_root(oid) for oid in denominator["required_machine"])
recipes = bundle["validation_recipes"]
recipe_required = {"recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
                   "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations"}
assert all(recipe_required <= recipe.keys() for recipe in recipes)
assert all(recipe["network_policy"] == "denied" for recipe in recipes)
assert set(recipes[0]["covered_obligation_ids"]) == set(ids)

closure = bundle["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M4"
assert set(closure["remaining_root_cut_set"]) == {"M1333-C-EULER", "M1333-L-COMPACT", "M1333-L-INTEGRAL", "M1333-L-DERIV"}

print(f"PASS THM-M-1333 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M4); no proof or theorem completion claimed")
