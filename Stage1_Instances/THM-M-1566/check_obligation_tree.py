#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1566 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1566-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-1566"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 15 and ids[0] == registry["root_obligation_id"] == "M1566-ROOT"
projection = [{k:r[k] for k in fields} for r in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
for key, eligibility in (("required_machine","machine_eligibility"),("required_human_source","human_source_eligibility"),("required_readable","readable_eligibility")):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[eligibility] == "required"]
required = {"node_id","obligation_id","kind","human_statement","formal_target","output","human_debt","machine_debt","readability_debt","evidence_ids","source_crosswalk_id","provenance_id","foundation_profile","tcb_profile","computation_record","step_budget","semantic_step_ledger","public_readable_target","validation_spec_id","status_boundary","task_ids","owned_sources","owner","reviewer","validity"}
nodes = bundle["nodes"]
assert len(nodes) == 15 and {n["obligation_id"] for n in nodes} == set(ids)
for n in nodes:
    assert required <= n.keys() and 0 < n["step_budget"] <= 100
    assert {"premises","inference","output","outgoing_use"} <= n["semantic_step_ledger"].keys()
allowed = {"proof_requires","composes","logical_decomposition","source_map","provenance_of","trusts","documents","workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in edge_ids and e["type"] in allowed and e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        edge_ids.add(e["edge_id"])
proof = {e["edge_id"]:e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for e in proof.values():
    reverse = proof[e["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == e["edge_id"] and (reverse["from"],reverse["to"]) == (e["to"],e["from"])
    assert {e["type"],reverse["type"]} == {"proof_requires","composes"}
    if e["type"] == "proof_requires": children.setdefault(e["from"],[]).append(e["to"])
visiting, visited = set(), set()
def visit(node):
    assert node not in visiting
    if node in visited: return
    visiting.add(node)
    for child in children.get(node,[]): visit(child)
    visiting.remove(node); visited.add(node)
visit("M1566-ROOT")
assert visited == {"M1566-ROOT","M1566-T-ASSEMBLE","M1566-T-EXISTENCE","M1566-T-UNIQUENESS","M1566-C-RENORMALIZATION","M1566-L-FIXEDPOINT","M1566-C-NOISE","M1566-L-PARAPRODUCT","M1566-L-SCHAUDER","M1566-N-SPACES"}
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE/"ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry","admit","axiom ","sorryAx"))
assert "root_of_existence_and_uniqueness" in lean and "#print axioms" in lean
print(f"PASS THM-M-1566 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M4); existence and uniqueness packages remain M4")
