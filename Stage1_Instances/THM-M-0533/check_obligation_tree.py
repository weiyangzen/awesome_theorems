#!/usr/bin/env python3
"""Fail-closed structural validation for THM-M-0533's architecture freeze."""
import hashlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
r = json.loads((HERE / "obligation-registry.json").read_text())
b = json.loads((HERE / "typed-graphs.json").read_text())
assert r["item_id"] == b["item_id"] == "S56-M-0533-OBLIGATION_TREE"
assert r["theorem_id"] == b["theorem_id"] == "THM-M-0533"
rows = r["obligations"]; ids = [x["obligation_id"] for x in rows]
assert len(ids) == len(set(ids)) == 19
assert ids[0] == r["root_obligation_id"] == b["root_node_id"] == "M0533-ROOT"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
den = hashlib.sha256(json.dumps([{k: x[k] for k in fields} for x in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert den == r["denominator_sha256"] == b["registry_denominator_sha256"]
assert b["statement_source_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
d = r["frozen_denominators"]
assert d["inventory"] == ids and d["required_readable"] == ids
assert d["required_machine"] == [x["obligation_id"] for x in rows if x["machine_eligibility"] == "required"]
assert set(b["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = {}; proof_composes = {}
for name, graph in b["graphs"].items():
    for e in graph["edges"]:
        assert e["edge_id"] not in all_edges and e["from"] in ids and e["to"] in ids
        all_edges[e["edge_id"]] = e
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        if name == "proof" and e["type"] == "composes": proof_composes.setdefault(e["from"], []).append(e["to"])
for e in b["graphs"]["proof"]["edges"]:
    assert all_edges[e["reciprocal_edge_id"]]["reciprocal_edge_id"] == e["edge_id"]
def reaches_root(start):
    todo, seen = [start], set()
    while todo:
        x = todo.pop()
        if x == "M0533-ROOT": return True
        if x in seen: continue
        seen.add(x); todo.extend(proof_composes.get(x, []))
    return False
assert all(reaches_root(x) for x in d["required_machine"] if x not in {"M0533-S-DEFINITIONS", "M0533-S-BOUNDARY", "M0533-S-FOUNDATION"})
assert all(0 < n["step_budget"] <= 100 and n["step_budget"] == len(n["semantic_step_ledger"]) for n in b["nodes"])
c = b["closure_boundary"]
assert c["root_closed"] is c["audit_complete"] is c["theorem_complete"] is False
for p in HERE.glob("*.lean"):
    text = p.read_text().replace("assert_no_sorry", "")
    assert "sorry" not in text and "admit" not in text
print(f"PASS THM-M-0533 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {den}")
print("root closure: open (M3); no theorem completion claimed")
