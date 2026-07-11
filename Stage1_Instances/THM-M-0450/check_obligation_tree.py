#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0450 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())

def require(value, message):
    if not value:
        raise SystemExit("obligation-tree check failed: " + message)

require(registry["item_id"] == bundle["item_id"] == "S56-M-0450-OBLIGATION_TREE", "wrong item")
require(registry["theorem_id"] == bundle["theorem_id"] == "THM-M-0450", "wrong theorem")
require(registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(), "statement drift")
require(registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(), "anchor audit drift")

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
require(len(ids) == len(set(ids)) == 14, "obligation IDs are not 14 unique values")
require(ids[0] == registry["root_obligation_id"] == bundle["root_obligation_id"], "root mismatch")
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
require(digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"], "denominator drift")
require(registry["frozen_denominators"]["inventory"] == ids, "inventory denominator mismatch")
require(registry["frozen_denominators"]["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"], "machine denominator mismatch")
require(registry["frozen_denominators"]["required_human_source"] == [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"], "human denominator mismatch")
require(registry["frozen_denominators"]["required_readable"] == [r["obligation_id"] for r in rows if r["readable_eligibility"] == "required"], "readable denominator mismatch")
require(all(isinstance(r["step_budget"], int) and 0 < r["step_budget"] <= 100 for r in rows), "invalid leaf budget")

nodes = bundle["nodes"]
require({n["obligation_id"] for n in nodes} == set(ids) and len(nodes) == len(ids), "node coverage mismatch")
require(set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}, "typed graph families missing")
allowed = {"proof_requires", "refines", "provenance_of", "evidence_for", "trusts", "documents", "source_map", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        require(edge["edge_id"] not in edge_ids, "duplicate edge ID")
        require(edge["type"] in allowed, "unknown edge type")
        require(edge["from"] in ids and edge["to"] in ids, "edge endpoint outside registry")
        require(edge["edge_id"] in graph["out"].get(edge["from"], []), "out adjacency mismatch")
        require(edge["edge_id"] in graph["in"].get(edge["to"], []), "in adjacency mismatch")
        edge_ids.add(edge["edge_id"])

children = {}
for edge in bundle["graphs"]["proof"]["edges"]:
    children.setdefault(edge["from"], []).append(edge["to"])
visiting, visited = set(), set()
def visit(node):
    require(node not in visiting, "proof graph cycle")
    if node in visited:
        return
    visiting.add(node)
    for child in children.get(node, []):
        visit(child)
    visiting.remove(node)
    visited.add(node)
visit("M0450-ROOT")
require({"M0450-ROOT", "M0450-T-ASSEMBLE", "M0450-B-WEAKMW", "M0450-B-KUMMER", "M0450-B-QUOTIENT", "M0450-H-HEIGHT", "M0450-H-NONNEG", "M0450-H-PARALLEL", "M0450-H-NORTHCOTT", "M0450-X-TRANSPORT"} == visited, "proof reachability mismatch")
lean = (HERE / "ObligationTree.lean").read_text()
require(all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx")), "prohibited Lean token")
require("root_of_descent_packages" in lean and "#print axioms" in lean, "composition probe missing")
require(bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False, "false closure claim")
print(f"PASS THM-M-0450 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); weak Mordell-Weil and elliptic-height packages remain open")
