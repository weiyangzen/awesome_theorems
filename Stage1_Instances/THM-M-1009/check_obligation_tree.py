#!/usr/bin/env python3
"""Validate THM-M-1009 frozen obligation artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
load = lambda name: json.loads((HERE / name).read_text())
r, b, s = load("obligation-registry.json"), load("typed-graphs.json"), load("validation-specs.json")
assert {r["item_id"], b["item_id"], s["item_id"]} == {"S56-M-1009-OBLIGATION_TREE"}
assert r["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
assert r["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = r["obligations"]; ids = [x["obligation_id"] for x in rows]
assert len(ids) == len(set(ids)) == 15 and r["root_obligation_id"] == "M1009-ROOT"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
digest = hashlib.sha256(json.dumps([{k:x[k] for k in fields} for x in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == r["denominator_sha256"] == b["registry_denominator_sha256"]
assert r["frozen_denominators"]["inventory"] == ids
assert {n["obligation_id"] for n in b["nodes"]} == set(ids)
assert all(0 < n["step_budget"] <= 100 for n in b["nodes"])
assert set(b["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids = set()
for graph in b["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in edge_ids and e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        edge_ids.add(e["edge_id"])
proof = {e["edge_id"]: e for e in b["graphs"]["proof"]["edges"]}
for e in proof.values():
    q = proof[e["reciprocal_edge_id"]]
    assert (q["from"], q["to"]) == (e["to"], e["from"])
    assert {e["type"], q["type"]} == {"proof_requires", "composes"}
assert len(s["recipes"]) == 15 and all(x["network"] == "forbidden" for x in s["recipes"])
assert b["closure_boundary"]["closed_obligations"] == [] and not b["closure_boundary"]["root_closed"]
lean = (HERE / "ObligationTree.lean").read_text()
for token in ("sorry", "admit", "sorryAx"):
    assert token not in lean
assert "theorem root_compose" in lean and "#print axioms root_compose" in lean
print(f"PASS THM-M-1009 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root remains open at M3; four-leaf proof cut set frozen")
