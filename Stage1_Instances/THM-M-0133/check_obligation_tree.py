#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())

registry_fields = {
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
}
node_fields = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
    "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
    "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
    "task_ids", "owned_sources", "owner", "reviewer", "validity",
}
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-0133"
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 38
assert ids[0] == registry["root_obligation_id"] == "M0133-ROOT"
assert all(registry_fields <= row.keys() for row in rows)

projection = [{key: row[key] for key in (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)} for row in rows]
raw = json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
assert hashlib.sha256(raw).hexdigest() == registry["denominator_sha256"]
for key, field, value in (
    ("required_machine", "machine_eligibility", "required"),
    ("required_human_source", "human_source_eligibility", "required"),
    ("required_readable", "readable_eligibility", "required"),
):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == value]
assert registry["frozen_denominators"]["inventory"] == ids

nodes = bundle["nodes"]
assert len(nodes) == len(ids)
assert {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert node_fields <= node.keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100
    assert node["semantic_step_ledger"]

expected = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
assert set(bundle["graphs"]) == expected
allowed = {"proof_requires", "logical_decomposition", "source_map", "provenance_of",
           "evidence_for", "documents", "trusts", "workflow_depends_on"}
seen_edges = set()
adjacency = {}
for name, graph in bundle["graphs"].items():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in seen_edges
        seen_edges.add(edge["edge_id"])
        assert edge["type"] in allowed and edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        if name in {"proof", "refinement"}:
            adjacency.setdefault(edge["from"], []).append(edge["to"])

active, visited = set(), set()
def visit(node):
    assert node not in active, f"cycle at {node}"
    if node in visited:
        return
    active.add(node)
    for child in adjacency.get(node, []):
        visit(child)
    active.remove(node)
    visited.add(node)
visit("M0133-ROOT")
required = {r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"}
assert required <= visited
assert bundle["closure_boundary"]["closed_obligations"] == []
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M0133-L-MOD", "M0133-L-LOWER"]

lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom "):
    assert forbidden not in lean
assert "root_compose" in lean and "#print axioms root_compose" in lean
print(f"PASS THM-M-0133 obligation tree: {len(ids)} obligations, {len(seen_edges)} typed edges")
print(f"registry denominator sha256: {registry['denominator_sha256']}")
print("root remains open at M2; cut set: semistable modularity and level lowering")
