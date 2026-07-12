#!/usr/bin/env python3
"""Fail-closed structural check for THM-M-0525's obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == "S56-M-0525-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-0525"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
rows = registry["obligations"]
ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 10 and ids[0] == registry["root_obligation_id"]
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
digest = hashlib.sha256(json.dumps([{k: r[k] for k in fields} for r in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
allowed = {"proof_requires", "composes", "logical_decomposition", "provenance_of", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])
proof = bundle["graphs"]["proof"]["edges"]
requirements = {(e["from"], e["to"]) for e in proof if e["type"] == "proof_requires"}
compositions = {(e["to"], e["from"]) for e in proof if e["type"] == "composes"}
assert requirements == compositions
assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
assert "statement_of_left_laws" in lean and "#print axioms" in lean
print(f"PASS THM-M-0525 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M2); conditional composition only")
