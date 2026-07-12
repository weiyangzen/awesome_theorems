#!/usr/bin/env python3
"""Fail-closed structural validation for the THM-M-0152 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0152-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-0152"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 17 and ids[0] == registry["root_obligation_id"] == "M0152-ROOT"
projection = [{k: r[k] for k in fields} for r in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
assert registry["frozen_denominators"]["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "evidence_for", "provenance_of", "trusts", "documents", "workflow_depends_on"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in all_edges and e["type"] in allowed
        assert e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        all_edges.add(e["edge_id"])

proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for e in proof.values():
    reverse = proof[e["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == e["edge_id"]
    assert (reverse["from"], reverse["to"]) == (e["to"], e["from"])
    assert {e["type"], reverse["type"]} == {"proof_requires", "composes"}
    if e["type"] == "proof_requires":
        children.setdefault(e["from"], []).append(e["to"])

visiting, visited = set(), set()
def visit(node):
    assert node not in visiting
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)
visit("M0152-ROOT")
expected = {"M0152-ROOT", "M0152-T-ASSEMBLE", "M0152-L-INTRINSIC-FORMULA", "M0152-T-INVARIANCE", "M0152-S-REGULAR", "M0152-C-CHRISTOFFEL", "M0152-L-GAUSS-CANCEL", "M0152-B-ORIENTATION", "M0152-L-CHAIN", "M0152-S-LOCAL-INVERSE", "M0152-N-LOCAL", "M0152-L-METRIC-JET"}
assert visited == expected
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert all(r["network"] == "disabled" and r["covered_ids"] for r in specs["recipes"])
assert bundle["closure_boundary"] == {"root_closed": False, "minimal_open_root_cut": ["M0152-L-INTRINSIC-FORMULA", "M0152-T-INVARIANCE"], "audit_complete": False, "theorem_complete": False}
for path in (HERE / "Statement.lean", HERE / "AnchorAudit.lean"):
    source = path.read_text()
    assert all(token not in source for token in ("sorry", "admit", "axiom ", "sorryAx"))
print(f"PASS THM-M-0152 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M4); intrinsic formula and coordinate invariance remain M4")
