#!/usr/bin/env python3
"""Validate THM-M-1108 frozen obligations and typed graph integrity."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
r = json.loads((HERE / "obligation-registry.json").read_text())
b = json.loads((HERE / "typed-graphs.json").read_text())
v = json.loads((HERE / "validation-specs.json").read_text())
assert r["item_id"] == b["item_id"] == v["item_id"] == "S56-M-1108-OBLIGATION_TREE"
assert r["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert r["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = r["obligations"]; ids = [x["obligation_id"] for x in rows]
assert len(ids) == len(set(ids)) == 18 and ids[0] == r["root_obligation_id"]
projection = [{k: x[k] for k in fields} for x in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == r["denominator_sha256"] == b["registry_denominator_sha256"]
assert r["frozen_denominators"]["inventory"] == ids
for key, field, val in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert r["frozen_denominators"][key] == [x["obligation_id"] for x in rows if x[field] == val]

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert {n["obligation_id"] for n in b["nodes"]} == set(ids)
for n in b["nodes"]:
    assert required <= n.keys() and 0 < n["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= n["semantic_step_ledger"].keys()
assert set(b["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = []
for graph in b["graphs"].values():
    edge_ids = {e["edge_id"] for e in graph["edges"]}; all_edges += graph["edges"]
    assert set(sum(graph["out"].values(), [])) == edge_ids
    assert set(sum(graph["in"].values(), [])) == edge_ids
    assert all(e["from"] in ids and e["to"] in ids for e in graph["edges"])
proof = {e["edge_id"]: e for e in b["graphs"]["proof"]["edges"]}
for e in proof.values():
    mate = proof[e["reciprocal_edge_id"]]
    assert mate["from"] == e["to"] and mate["to"] == e["from"]
    assert {mate["type"], e["type"]} == {"proof_requires", "composes"}
children = {}
for e in proof.values():
    if e["type"] == "proof_requires": children.setdefault(e["from"], []).append(e["to"])
seen, stack = set(), set()
def visit(x):
    assert x not in stack
    if x in seen: return
    stack.add(x)
    for y in children.get(x, []): visit(y)
    stack.remove(x); seen.add(x)
visit(r["root_obligation_id"])
assert {"M1108-T-POISSONIZED", "M1108-T-DEPOISSONIZE", "M1108-C-RSK", "M1108-C-RHP"} <= seen
assert [x["obligation_id"] for x in v["recipes"]] == ids
lean = (HERE / "ObligationTree.lean").read_text()
for forbidden in ("sorry", "admit", "axiom ", "unsafe"):
    assert forbidden not in lean
assert "canonicalStatement_of_poissonized_depoissonized" in lean and "#print axioms" in lean
assert b["closure_boundary"]["root_closed"] is False and b["closure_boundary"]["theorem_complete"] is False
print(f"PASS THM-M-1108 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); Poissonized and de-Poissonization packages remain M4")
