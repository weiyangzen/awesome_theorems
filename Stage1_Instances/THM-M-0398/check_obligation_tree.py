#!/usr/bin/env python3
"""Fail-closed structural validation for THM-M-0398's obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0398-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0398"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.md").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 15 and ids[0] == registry["root_obligation_id"] == "M0398-ROOT"
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
assert registry["frozen_denominators"]["required_human_source"] == [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"]
assert registry["frozen_denominators"]["required_readable"] == ids

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
    "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
    "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
    "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
    "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys()
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of",
           "evidence_for", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edge_ids = set()
for graph in bundle["graphs"].values():
    local = {e["edge_id"]: e for e in graph["edges"]}
    assert len(local) == len(graph["edges"])
    for edge in graph["edges"]:
        assert edge["edge_id"] not in all_edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        all_edge_ids.add(edge["edge_id"])

proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])
seen, active = set(), set()
def visit(node):
    assert node not in active, f"proof cycle at {node}"
    if node in seen:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    seen.add(node)
visit("M0398-ROOT")
assert seen == {"M0398-ROOT", "M0398-T", "M0398-L4", "M0398-N1", "M0398-C1", "M0398-C2", "M0398-L1", "M0398-L2", "M0398-L3"}

recipe_ids = {r["recipe_id"] for r in specs["recipes"]}
assert {n["validation_spec_id"] for n in nodes} == recipe_ids
assert all(r["network_policy"] == "denied" and r["expected_exit"] == 0 for r in specs["recipes"])
assert bundle["closure_boundary"]["closed_obligations"] == ["M0398-S1", "M0398-S2", "M0398-T"]
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M0398-L4"]
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_finiteExceptionalWithConstant" in lean and "#print axioms" in lean

print(f"PASS THM-M-0398 obligation tree: {len(ids)} obligations, {len(all_edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); uniform constant-factor Roth engine remains M4")
