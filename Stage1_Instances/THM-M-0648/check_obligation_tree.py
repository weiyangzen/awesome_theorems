#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
r = json.loads((HERE / "obligation-registry.json").read_text())
g = json.loads((HERE / "typed-graphs.json").read_text())
ids = [x["obligation_id"] for x in r["obligations"]]
assert r["theorem_id"] == g["theorem_id"] == "THM-M-0648"
assert len(ids) == len(set(ids)) == 12 and ids[0] == r["root_obligation_id"]
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: x[k] for k in fields} for x in r["obligations"]]
raw = json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
assert hashlib.sha256(raw).hexdigest() == r["denominator_sha256"] == g["registry_denominator_sha256"]
assert {n["obligation_id"] for n in g["nodes"]} == set(ids)
assert set(g["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
seen, adjacency = set(), {}
for name, graph in g["graphs"].items():
    for e in graph["edges"]:
        assert e["edge_id"] not in seen and e["from"] in ids and e["to"] in ids
        seen.add(e["edge_id"])
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        if name in {"proof", "refinement"} and e["type"] in {"proof_requires", "logical_decomposition"}:
            adjacency.setdefault(e["from"], []).append(e["to"])
active, visited = set(), set()
def visit(x):
    assert x not in active, "proof/refinement cycle"
    if x in visited: return
    active.add(x)
    for y in adjacency.get(x, []): visit(y)
    active.remove(x); visited.add(x)
visit("M0648-ROOT")
required = {x["obligation_id"] for x in r["obligations"] if x["machine_eligibility"] == "required"}
assert required <= visited
assert g["closure_boundary"]["closed_obligations"] == [] and not g["closure_boundary"]["theorem_complete"]
lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom "): assert forbidden not in lean
assert "root_compose" in lean and "#print axioms root_compose" in lean
print(f"PASS THM-M-0648 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print("registry denominator sha256:", r["denominator_sha256"])
print("root remains open at M4; no proof credit awarded")
