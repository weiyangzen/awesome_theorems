#!/usr/bin/env python3
"""Fail-closed structural check for THM-M-1252 obligation artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 11 and registry["root_obligation_id"] == "M1252-ROOT"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
raw = json.dumps([{key: row[key] for key in fields} for row in rows], sort_keys=True, separators=(",", ":")).encode()
denominator = hashlib.sha256(raw).hexdigest()
assert registry["denominator_sha256"] == bundle["registry_denominator_sha256"] == denominator
for field, key in (("machine_eligibility", "required_machine"), ("human_source_eligibility", "required_human_source"), ("readable_eligibility", "required_readable")):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == "required"]

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for row in graph["edges"]:
        assert row["edge_id"] not in edge_ids and row["type"] in allowed
        assert row["from"] in ids and row["to"] in ids
        assert row["edge_id"] in graph["out"][row["from"]] and row["edge_id"] in graph["in"][row["to"]]
        edge_ids.add(row["edge_id"])

proof = {row["edge_id"]: row for row in bundle["graphs"]["proof"]["edges"]}
children = {}
for row in proof.values():
    reverse = proof[row["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == row["edge_id"]
    assert (reverse["from"], reverse["to"]) == (row["to"], row["from"])
    assert {row["type"], reverse["type"]} == {"proof_requires", "composes"}
    if row["type"] == "proof_requires":
        children.setdefault(row["from"], []).append(row["to"])

visiting, visited = set(), set()
def visit(node):
    assert node not in visiting, f"proof cycle at {node}"
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)
visit("M1252-ROOT")
assert {"M1252-ROOT", "M1252-T-COMPOSE", "M1252-N-SPECIALIZE", "M1252-L-UPSTREAM", "M1252-S-DOMAIN"} <= visited
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert all(r["network_policy"] == "denied" and isinstance(r["argv"], list) for r in specs["recipes"])
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M1252-N-SPECIALIZE"]
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_specializedAnchor" in lean and "#print axioms" in lean
print(f"PASS THM-M-1252 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M3); proof-phase anchor installation remains downstream")
