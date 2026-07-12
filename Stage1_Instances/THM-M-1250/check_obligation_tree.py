#!/usr/bin/env python3
"""Fail-closed structural validation of the THM-M-1250 obligation freeze."""
import hashlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
r = json.loads((HERE / "obligation-registry.json").read_text())
b = json.loads((HERE / "typed-graphs.json").read_text())
assert r["item_id"] == b["item_id"] == "S56-M-1250-OBLIGATION_TREE"
assert r["theorem_id"] == b["theorem_id"] == "THM-M-1250"
assert r["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert r["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = r["obligations"]; ids = [x["obligation_id"] for x in rows]
assert len(ids) == len(set(ids)) == 15 and ids[0] == r["root_obligation_id"]
digest = hashlib.sha256(json.dumps([{k:x[k] for k in fields} for x in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == r["denominator_sha256"] == b["registry_denominator_sha256"]
assert r["frozen_denominators"]["inventory"] == ids
required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert len(b["nodes"]) == 15 and {n["obligation_id"] for n in b["nodes"]} == set(ids)
for n in b["nodes"]:
    assert required <= n.keys() and 0 < n["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= n["semantic_step_ledger"].keys()
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
assert set(b["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
for g in b["graphs"].values():
    for e in g["edges"]:
        assert e["edge_id"] not in edge_ids and e["type"] in allowed and e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in g["out"][e["from"]] and e["edge_id"] in g["in"][e["to"]]; edge_ids.add(e["edge_id"])
proof = {e["edge_id"]: e for e in b["graphs"]["proof"]["edges"]}
children = {}
for e in proof.values():
    rev = proof[e["reciprocal_edge_id"]]
    assert rev["reciprocal_edge_id"] == e["edge_id"] and (rev["from"], rev["to"]) == (e["to"], e["from"])
    assert {e["type"], rev["type"]} == {"proof_requires", "composes"}
    if e["type"] == "proof_requires": children.setdefault(e["from"], []).append(e["to"])
visiting, visited = set(), set()
def visit(x):
    assert x not in visiting
    if x in visited: return
    visiting.add(x)
    for y in children.get(x, []): visit(y)
    visiting.remove(x); visited.add(x)
visit("M1250-ROOT")
assert visited == {"M1250-ROOT", "M1250-T-ASSEMBLE", "M1250-F-PACKAGE", "M1250-F-SMOOTH", "M1250-F-DECAY", "M1250-S-EQUALITY", "M1250-R-PACKAGE", "M1250-R-SMOOTH", "M1250-R-DECAY", "M1250-R-CONSTRUCT", "M1250-S-BOUNDARY"}
assert b["closure_boundary"]["remaining_root_cut_set"] == ["M1250-F-PACKAGE", "M1250-R-PACKAGE"]
assert not b["closure_boundary"]["root_closed"] and not b["closure_boundary"]["theorem_complete"]
lean = (HERE / "ObligationTree.lean").read_text()
assert all(x not in lean for x in ("sorry", "admit", "axiom ", "sorryAx"))
assert "characterization_of_packages" in lean and "#print axioms" in lean
print(f"PASS THM-M-1250 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); forward and reverse packages remain explicit")
