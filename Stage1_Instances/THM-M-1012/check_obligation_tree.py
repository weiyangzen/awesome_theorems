#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1012 obligation freeze."""

import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert reg["item_id"] == graphs["item_id"] == specs["item_id"] == "S56-M-1012-OBLIGATION_TREE"
assert reg["theorem_id"] == graphs["theorem_id"] == specs["theorem_id"] == "THM-M-1012"
assert reg["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert reg["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id")
rows = reg["obligations"]; ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 14 and ids[0] == reg["root_obligation_id"]
digest = hashlib.sha256(json.dumps([{k:r[k] for k in fields} for r in rows], sort_keys=True, separators=(",",":")).encode()).hexdigest()
assert digest == reg["denominator_sha256"] == graphs["registry_denominator_sha256"]
assert reg["frozen_denominators"]["inventory"] == ids
for key, field in (("required_machine","machine_eligibility"),("required_human_source","human_source_eligibility"),("required_readable","readable_eligibility")):
    assert reg["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == "required"]

required = {"node_id","obligation_id","kind","human_statement","formal_target","output","human_debt","machine_debt","readability_debt","evidence_ids","source_crosswalk_id","provenance_id","foundation_profile","tcb_profile","computation_record","step_budget","semantic_step_ledger","public_readable_target","validation_spec_id","status_boundary","task_ids","owned_sources","owner","reviewer","validity"}
nodes = graphs["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for n in nodes:
    assert required <= n.keys() and 0 < n["step_budget"] <= 100
    assert n["human_debt"] in {f"H{i}" for i in range(6)} and n["machine_debt"] in {"M0-L","M0-W","M0-P","M1","M2","M3","M4","M5"} and n["readability_debt"] in {f"R{i}" for i in range(5)}
    assert {"premises","inference","output","outgoing_use"} <= n["semantic_step_ledger"].keys()

assert set(graphs["graphs"]) == {"proof","refinement","provenance","evidence","trust","documentation","workflow"}
allowed = {"proof_requires","composes","logical_decomposition","source_map","provenance_of","evidence_for","trusts","documents","workflow_depends_on"}
all_edges = []
for graph in graphs["graphs"].values():
    for e in graph["edges"]:
        assert e["type"] in allowed and e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        all_edges.append(e)
assert len({e["edge_id"] for e in all_edges}) == len(all_edges)
pedges = {e["edge_id"]: e for e in graphs["graphs"]["proof"]["edges"]}
for e in pedges.values():
    rev = pedges[e["reciprocal_edge_id"]]
    assert rev["reciprocal_edge_id"] == e["edge_id"] and (rev["from"],rev["to"]) == (e["to"],e["from"])
    assert {e["type"],rev["type"]} == {"proof_requires","composes"}

children = {}
for e in all_edges:
    if e["type"] in {"proof_requires","logical_decomposition"}: children.setdefault(e["from"], []).append(e["to"])
visiting=set(); visited=set()
def visit(x):
    assert x not in visiting, f"cycle at {x}"
    if x in visited: return
    visiting.add(x)
    for y in children.get(x,[]): visit(y)
    visiting.remove(x); visited.add(x)
visit("M1012-ROOT")
assert set(reg["frozen_denominators"]["required_machine"]) <= visited
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert all(r["network_policy"] == "denied" and r["expected_exit"] == 0 for r in specs["recipes"])
assert graphs["closure_boundary"]["root_closed"] is False and graphs["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_directions" in lean and "reverse_of_tightness_and_separation" in lean and "#print axioms" in lean
print(f"PASS THM-M-1012 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); proof, source, readability, validation, and release remain downstream")
