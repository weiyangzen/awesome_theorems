#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows = registry["obligations"]
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 10
assert ids[0] == registry["root_obligation_id"] == "M1550-ROOT"
for row in rows:
    assert set(fields) <= row.keys()
    assert row["machine_eligibility"] in {"required", "informational", "not_applicable"}
    assert row["human_source_eligibility"] in {"required", "not_applicable"}
    assert row["readable_eligibility"] in {"required", "not_applicable"}

nodes = bundle["nodes"]
required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert len(nodes) == 10 and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required_node <= node.keys()
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100
    assert node["semantic_step_ledger"]

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids, adjacency = set(), {}
for name, graph in bundle["graphs"].items():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids
        edge_ids.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        if name in {"proof", "refinement"}:
            adjacency.setdefault(edge["from"], []).append(edge["to"])

seen, active = set(), set()
def visit(node):
    assert node not in active, f"cycle at {node}"
    if node in seen:
        return
    active.add(node)
    for child in adjacency.get(node, []):
        visit(child)
    active.remove(node)
    seen.add(node)
visit("M1550-ROOT")
required = {r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"}
assert required <= seen
for key, field, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == value]
assert registry["frozen_denominators"]["inventory"] == ids
assert bundle["closure_boundary"]["closed_obligations"] == []
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M1550-L-SPECTRUM"]
print(f"PASS THM-M-1550 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); conditional composition only")
