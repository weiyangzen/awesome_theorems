#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0415 obligation tree."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0415-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0415"
assert registry["registry_id"] == bundle["registry_id"] == "THM-M-0415-OBLIGATIONS-v1"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

obligations = registry["obligations"]
ids = [o["obligation_id"] for o in obligations]
assert len(ids) == len(set(ids)) == 15
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
actual = hashlib.sha256(json.dumps([{k: o[k] for k in fields} for o in obligations], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert actual == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys()
    assert node["human_debt"] in {"H0", "H1", "H2", "H3", "H4", "H5"}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {"R0", "R1", "R2", "R3", "R4"}
    assert 0 < node["step_budget"] <= 100 and node["semantic_step_ledger"]

edge_ids = set()
proof = bundle["graphs"]["proof"]["edges"]
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids
        edge_ids.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
for edge in proof:
    if edge["type"] == "proof_requires":
        reciprocal = next(e for e in proof if e["edge_id"] == edge["reciprocal_edge_id"])
        assert reciprocal["type"] == "composes" and reciprocal["from"] == edge["to"] and reciprocal["to"] == edge["from"]

adj = {}
for edge in proof:
    if edge["type"] == "proof_requires":
        adj.setdefault(edge["from"], []).append(edge["to"])
visiting, done = set(), set()
def visit(oid):
    assert oid not in visiting
    if oid in done:
        return
    visiting.add(oid)
    for child in adj.get(oid, []):
        visit(child)
    visiting.remove(oid); done.add(oid)
visit("M0415-ROOT")

assert {r["obligation_id"] for r in specs["recipes"]} == set(ids)
for recipe in specs["recipes"]:
    assert isinstance(recipe["argv"], list) and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0 and recipe["obligation_id"] in recipe["covered_obligation_ids"]
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False

lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "finiteTarget_of_fintypePresentation" in lean and "idealClassGroupFinite_mathlib" in lean
print(f"PASS THM-M-0415 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {actual}")
print("root state: M3 pending full provenance/trust and master acceptance; theorem_complete=false")
