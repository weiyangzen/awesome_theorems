#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-1278 architecture freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == "S56-M-1278-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-1278"
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 15
assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == "M1278-ROOT"

required = {"obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
            "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id"}
assert all(required <= row.keys() for row in rows)
assert rows[0]["statement_fingerprint"] == "lean-expression-sha256:a267837ccca68a9ad86620bd4ce7c26c8d56861b57d76d6198ddce94ae671fdb"
assert all(row["statement_fingerprint"].startswith(("lean-expression-sha256:", "planned:v1:sha256:")) for row in rows)
assert all(row["terminal_proof_body_id"] is None for row in rows)

denom = registry["frozen_denominators"]
assert denom["inventory"] == ids
assert denom["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
assert denom["required_human_source"] == [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"]
assert denom["required_readable"] == ids
assert set(denom["informational_overlays"]) == {"M1278-X-SOURCE", "M1278-X-PROVENANCE"}
digest = hashlib.sha256(json.dumps(denom, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert bundle["registry_denominator_sha256"] == digest

node_required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt",
                 "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id",
                 "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger",
                 "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources",
                 "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert [n["obligation_id"] for n in nodes] == ids
assert all(node_required <= n.keys() for n in nodes)
assert all(0 < n["step_budget"] <= 100 and len(n["semantic_step_ledger"]) == n["step_budget"] for n in nodes)
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}

all_edges, proof_adj = set(), {}
for name, graph in bundle["graphs"].items():
    assert graph["edge_type"]
    for edge in graph["edges"]:
        assert edge["edge_id"] not in all_edges
        all_edges.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
        if name in {"proof", "refinement"}:
            proof_adj.setdefault(edge["from"], []).append(edge["to"])

def reaches_root(start):
    frontier, seen = [start], set()
    while frontier:
        node = frontier.pop()
        if node == "M1278-ROOT":
            return True
        assert node not in seen, f"cycle at {node}"
        seen.add(node)
        frontier.extend(proof_adj.get(node, []))
    return False

assert all(reaches_root(oid) for oid in denom["required_machine"])
closure = bundle["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M3"
assert set(closure["remaining_root_cut_set"]) == {"M1278-L-SHARP-ONOFRI", "M1278-S-AREA", "M1278-S-FINITE"}

lean = (HERE / "ObligationTree.lean").read_text()
assert "theorem compose_root" in lean and "hsharp" in lean and "hshift" in lean
assert not any(token in lean for token in ("sorry", "axiom ", "unsafe "))

print(f"PASS THM-M-1278 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); exact composition harness only")
