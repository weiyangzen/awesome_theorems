#!/usr/bin/env python3
"""Fail-closed structural and regeneration checks for THM-M-1131 graphs."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text())


before = {name: (HERE / name).read_bytes() for name in ("obligation-registry.json", "typed-graphs.json", "validation-specs.json")}
run = subprocess.run([sys.executable, str(HERE / "build_obligation_artifacts.py")], capture_output=True, text=True)
assert run.returncode == 0, run.stderr
for name, original in before.items():
    assert (HERE / name).read_bytes() == original, f"non-deterministic generated artifact: {name}"

registry = load("obligation-registry.json")
bundle = load("typed-graphs.json")
recipes = load("validation-specs.json")
assert registry["item_id"] == bundle["item_id"] == recipes["item_id"] == "S56-M-1131-OBLIGATION_TREE"
obligations = registry["obligations"]
ids = [row["obligation_id"] for row in obligations]
assert len(ids) == len(set(ids)) and registry["root_obligation_id"] in ids
assert set(registry["frozen_denominators"]["inventory"]) == set(ids)
assert bundle["registry_denominator_sha256"] == registry["denominator_sha256"]
assert len(bundle["nodes"]) == len(ids)
assert {node["obligation_id"] for node in bundle["nodes"]} == set(ids)
assert all(0 < node["step_budget"] <= 100 for node in bundle["nodes"])

required_node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
for node in bundle["nodes"]:
    assert required_node_fields <= node.keys(), node["node_id"]
    assert set(node["semantic_step_ledger"]) == {"premises", "inference", "output", "outgoing_use"}

all_edges = []
for graph in bundle["graphs"].values():
    all_edges.extend(graph["edges"])
    for item in graph["edges"]:
        assert item["from"] in ids and item["to"] in ids
edge_by_id = {item["edge_id"]: item for item in all_edges}
assert len(edge_by_id) == len(all_edges)
for item in bundle["graphs"]["proof"]["edges"]:
    if item["type"] == "proof_requires":
        reciprocal = edge_by_id[item["reciprocal_edge_id"]]
        assert reciprocal["type"] == "composes"
        assert reciprocal["from"] == item["to"] and reciprocal["to"] == item["from"]
        assert reciprocal["reciprocal_edge_id"] == item["edge_id"]

assert bundle["closure_boundary"]["root_closed"] is False
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M1131-T-FLUXDIV"]
assert len(recipes["recipes"]) == len(ids)

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
payload = [{key: row[key] for key in fields} for row in obligations]
actual = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert actual == registry["denominator_sha256"]
assert hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == registry["frozen_against_statement_sha256"]
assert hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest() == registry["frozen_against_anchor_audit_sha256"]
print(f"obligations: {len(ids)}; typed edges: {len(all_edges)}; denominator: {actual}")
print("deterministic regeneration, schemas, reciprocity, hashes, and open-root boundary: ok")
