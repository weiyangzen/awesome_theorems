#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0583 frozen architecture."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
typed = json.loads((HERE / "typed-graphs.json").read_text())

assert registry["theorem_id"] == typed["theorem_id"] == "THM-M-0583"
assert registry["registry_id"] == typed["registry_id"] == "THM-M-0583-OBLIGATIONS-v1"
obligations = registry["obligations"]
ids = [o["obligation_id"] for o in obligations]
assert len(ids) == len(set(ids)) == 16
assert {n["node_id"] for n in typed["nodes"]} == set(ids)

keys = ["obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason"]
projection = [{k: o[k] for k in keys} for o in obligations]
actual = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert actual == registry["denominator_sha256"]
assert all(o["root_relevant"] and o["machine_eligibility"] == "required" for o in obligations)

required_graphs = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
assert set(typed["graphs"]) == required_graphs
edge_ids = set()
for graph in typed["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids
        edge_ids.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]

for node in typed["nodes"]:
    assert 0 < node["step_budget"] <= 100
    assert node["semantic_step_ledger"] and not node["evidence_ids"]
    assert node["machine_debt"] == "M2"

proof = typed["graphs"]["proof"]["edges"]
reachable, changed = {"M0583-ROOT"}, True
while changed:
    changed = False
    for edge in proof:
        if edge["from"] in reachable and edge["to"] not in reachable:
            reachable.add(edge["to"]); changed = True
assert {"M0583-X-FREEDMAN-CORE", "M0583-L-DISK-EMBEDDING", "M0583-L-SURGERY", "M0583-L-S-COBORDISM"} <= reachable
assert typed["closure_boundary"]["root_machine_debt"] == "M2"
assert not typed["closure_boundary"]["closed_obligations"]
assert typed["closure_boundary"]["theorem_complete"] is False

lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom "):
    assert forbidden not in lean
for declaration in ("FreedmanTopologicalCore", "canonicalRoot_of_freedmanTopologicalCore", "freedmanTopologicalCore_iff_canonicalRoot"):
    assert declaration in lean

print(f"ok: 16 obligations, {len(edge_ids)} typed edges, seven graph kinds; denominator {actual}; root open M2")
