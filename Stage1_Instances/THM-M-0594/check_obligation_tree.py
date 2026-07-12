#!/usr/bin/env python3
"""Fail-closed structural checks for THM-M-0594 obligation artifacts."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-0594-OBLIGATION_TREE"
obligations = registry["obligations"]
ids = {o["obligation_id"] for o in obligations}
assert len(ids) == len(obligations) == 16 and registry["root_obligation_id"] == "M0594-ROOT"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: o[k] for k in fields} for o in obligations]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == [o["obligation_id"] for o in obligations]

required_node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert {n["obligation_id"] for n in nodes} == ids
assert all(required_node_fields <= set(n) and 0 < n["step_budget"] <= 100 for n in nodes)

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "evidence_for", "trusts", "documents", "workflow_depends_on"}
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
visit("M0594-ROOT")
expected_proof = {"M0594-ROOT", "M0594-T-ASSEMBLE", "M0594-C-GLOBAL", "M0594-L-TOPOLOGICAL", "M0594-N-EXHAUSTION", "M0594-N-DIMENSION", "M0594-C-LOCAL", "M0594-L-DIFFERENTIAL", "M0594-L-POINT-SEPARATION", "M0594-L-PROPERNESS"}
assert visited == expected_proof
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert all(set(r) >= {"cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy", "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations"} for r in specs["recipes"])
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_smooth_embedding_witness" in lean and "#print axioms" in lean
print(f"PASS THM-M-0594 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); noncompact construction and topological bridge remain M4")
