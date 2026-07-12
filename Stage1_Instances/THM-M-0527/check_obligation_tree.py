#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
load = lambda name: json.loads((HERE / name).read_text())
sha = lambda name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
registry = load("obligation-registry.json")
bundle = load("typed-graphs.json")
receipt = load("obligation-tree-receipt.json")

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in registry["obligations"]]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"]
ids = [row["obligation_id"] for row in registry["obligations"]]
assert len(ids) == 34 == len(set(ids))
assert registry["root_obligation_id"] == ids[0] == "M0527-ROOT"
assert all(row["machine_eligibility"] == row["human_source_eligibility"] == row["readable_eligibility"] == "required" for row in registry["obligations"])
for key in ("inventory", "required_machine", "required_human_source", "required_readable"):
    assert registry["frozen_denominators"][key] == ids

nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {n["obligation_id"] for n in nodes} == set(ids)
required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
for node in nodes:
    assert required_node <= node.keys()
    assert node["semantic_step_ledger"]
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids, adjacency = set(), {}
for name, graph in bundle["graphs"].items():
    for row in graph["edges"]:
        assert row["edge_id"] not in edge_ids
        edge_ids.add(row["edge_id"])
        assert row["from"] in ids and row["to"] in ids
        assert row["edge_id"] in graph["out"].get(row["from"], [])
        assert row["edge_id"] in graph["in"].get(row["to"], [])
        if name == "proof":
            adjacency.setdefault(row["from"], []).append(row["to"])

seen, active = set(), set()
def visit(node):
    assert node not in active, f"cycle at {node}"
    if node in seen: return
    active.add(node)
    for child in adjacency.get(node, []): visit(child)
    active.remove(node); seen.add(node)
visit("M0527-ROOT")
assert seen == set(ids)
assert bundle["closure_boundary"]["closed_obligations"] == []
assert bundle["closure_boundary"]["theorem_complete"] is False
assert receipt["outputs"]["obligation_registry_sha256"] == sha("obligation-registry.json")
assert receipt["outputs"]["typed_graphs_sha256"] == sha("typed-graphs.json")
assert receipt["inputs"]["statement_sha256"] == sha("Statement.lean")
assert receipt["inputs"]["anchor_audit_sha256"] == sha("anchor-audit.json")
assert receipt["counts"] == {"obligations": 34, "typed_edges": len(edge_ids)}
print(f"PASS THM-M-0527 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); no proof or theorem completion claimed")
