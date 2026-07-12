#!/usr/bin/env python3
"""Fail-closed structural checks for the frozen THM-M-1080 architecture."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1080-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-1080"
rows = registry["obligations"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 18
assert registry["root_obligation_id"] == bundle["root_node_id"] == "M1080-ROOT"

row_fields = {"obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id"}
assert all(row_fields <= r.keys() for r in rows)
assert all(r["statement_fingerprint"].startswith(("lean-source:v1:sha256:", "planned:v1:sha256:")) for r in rows)
assert [r["obligation_id"] for r in rows if r["terminal_proof_body_id"]] == ["M1080-T-ASSEMBLE"]

den = registry["frozen_denominators"]
assert den["inventory"] == ids
assert den["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
assert den["required_human_source"] == [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"]
assert den["required_readable"] == ids
assert set(den["informational_overlays"]) == {"M1080-X-MATHLIB", "M1080-X-SOURCE", "M1080-X-PROVENANCE"}
digest = hashlib.sha256(json.dumps(den, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert bundle["statement_source_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert bundle["anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert [n["node_id"] for n in nodes] == ids
assert all(node_fields <= n.keys() for n in nodes)
assert all(0 < n["step_budget"] <= 100 for n in nodes)
assert all(set(n["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"} for n in nodes)

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
proof_requires = {}
composes = {}
for name, graph in bundle["graphs"].items():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in all_edges
        all_edges.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
        if edge["type"] == "proof_requires":
            proof_requires[edge["edge_id"]] = edge
        if edge["type"] == "composes":
            composes[edge["edge_id"]] = edge
assert len(proof_requires) == len(composes)
for eid, edge in proof_requires.items():
    reciprocal = composes[edge["reciprocal_edge_id"]]
    assert reciprocal["reciprocal_edge_id"] == eid
    assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])

adj = {}
for edge in proof_requires.values():
    parent, child = edge["from"], edge["to"]
    adj.setdefault(child, set()).add(parent)

def reaches_root(start):
    frontier, seen = [start], set()
    while frontier:
        node = frontier.pop()
        if node == "M1080-ROOT":
            return True
        assert node not in seen, f"proof cycle at {node}"
        seen.add(node)
        frontier.extend(adj.get(node, []))
    return False

assert all(reaches_root(oid) for oid in den["required_machine"])
cert = bundle["composition_certificates"]
assert len(cert) == 1 and cert[0]["required_children"] == ["M1080-T-POSITIVE", "M1080-T-ZERO"]
closure = bundle["closure_boundary"]
assert closure["closed_obligations"] == ["M1080-T-ASSEMBLE"]
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M3"
assert closure["remaining_root_cut_set"] == ["M1080-T-POSITIVE", "M1080-T-ZERO"]
assert {r["recipe_id"] for r in specs["recipes"]} == {f"VAL-{oid}" for oid in ids}

for path in HERE.glob("*.lean"):
    text = path.read_text()
    assert "sorry" not in text and "admit" not in text and "axiom " not in text

print(f"PASS THM-M-1080 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); conditional threshold composition only")
