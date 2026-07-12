#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1045 obligation freeze."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
instance = json.loads((HERE / "intake.json").read_text())
assert reg["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1045-OBLIGATION_TREE"
assert reg["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == "THM-M-1045"
assert reg["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert reg["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = reg["obligations"]; ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 15 and ids[0] == reg["root_obligation_id"]
digest = hashlib.sha256(json.dumps([{k:r[k] for k in fields} for r in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == reg["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert instance["obligation_registry_hash"] == "sha256:" + digest
assert reg["frozen_denominators"]["inventory"] == ids
required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert {n["obligation_id"] for n in nodes} == set(ids)
for n in nodes:
    assert required <= n.keys() and 0 < n["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= n["semantic_step_ledger"].keys()
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
allowed = {"proof_requires", "composes", "logical_decomposition", "provenance_of", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in edge_ids and e["type"] in allowed and e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        edge_ids.add(e["edge_id"])
proof = {e["edge_id"]:e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for e in proof.values():
    rev = proof[e["reciprocal_edge_id"]]
    assert rev["reciprocal_edge_id"] == e["edge_id"] and (rev["from"], rev["to"]) == (e["to"], e["from"])
    if e["type"] == "proof_requires": children.setdefault(e["from"], []).append(e["to"])
visiting, seen = set(), set()
def visit(x):
    assert x not in visiting
    if x in seen: return
    visiting.add(x)
    for y in children.get(x, []): visit(y)
    visiting.remove(x); seen.add(x)
visit("M1045-ROOT")
assert seen == {"M1045-ROOT", "M1045-T-ASSEMBLE", "M1045-B-EQUIVALENCE", "M1045-B-DENSITY", "M1045-B-SINGULARITY", "M1045-L-CYLINDER-SHIFT", "M1045-L-PALEY-WIENER", "M1045-L-EXTENSION", "M1045-L-SEPARATION"}
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(t not in lean for t in ("sorry", "admit", "axiom ", "sorryAx")) and "#print axioms" in lean
print(f"PASS THM-M-1045 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); equivalence, density, and singularity branches remain M4")
