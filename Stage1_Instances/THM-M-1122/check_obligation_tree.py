#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-1122 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert reg["item_id"] == graphs["item_id"] == specs["item_id"] == "S56-M-1122-OBLIGATION_TREE"
assert reg["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert reg["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = reg["obligations"]; ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 11 and ids[0] == reg["root_obligation_id"]
projection = [{k: r[k] for k in fields} for r in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == reg["denominator_sha256"] == graphs["registry_denominator_sha256"]
assert reg["frozen_denominators"]["inventory"] == ids
required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert {n["obligation_id"] for n in graphs["nodes"]} == set(ids)
for n in graphs["nodes"]:
    assert required <= n.keys() and 0 < n["step_budget"] <= 100
    assert set(n["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"}
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in graphs["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in edge_ids and e["type"] in allowed and e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        edge_ids.add(e["edge_id"])
proof = {e["edge_id"]: e for e in graphs["graphs"]["proof"]["edges"]}
for e in proof.values():
    other = proof[e["reciprocal_edge_id"]]
    assert other["reciprocal_edge_id"] == e["edge_id"] and (other["from"], other["to"]) == (e["to"], e["from"])
assert {n["validation_spec_id"] for n in graphs["nodes"]} == {r["recipe_id"] for r in specs["recipes"]}
assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M1122-L-IDENTIFICATION"]
assert graphs["closure_boundary"]["root_closed"] is False and graphs["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "root_of_conditionalIdentification" in lean and "#print axioms" in lean
print(f"PASS THM-M-1122 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); ConditionalIdentification remains M4")
