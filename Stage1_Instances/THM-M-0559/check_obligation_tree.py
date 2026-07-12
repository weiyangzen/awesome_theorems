#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
raw = json.dumps([{k: row[k] for k in fields} for row in registry["obligations"]], sort_keys=True, separators=(",", ":")).encode()
digest = hashlib.sha256(raw).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
rows, nodes = registry["obligations"], bundle["nodes"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 18 and ids[0] == registry["root_obligation_id"] == "M0559-ROOT"
required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert {node["obligation_id"] for node in nodes} == set(ids) and len(nodes) == len(ids)
for node in nodes:
    assert required_node <= node.keys()
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids, adjacency = set(), {}
for name, graph in bundle["graphs"].items():
    for row in graph["edges"]:
        assert row["edge_id"] not in edge_ids and row["from"] in ids and row["to"] in ids
        edge_ids.add(row["edge_id"])
        assert row["edge_id"] in graph["out"].get(row["from"], []) and row["edge_id"] in graph["in"].get(row["to"], [])
        if row["type"] in {"proof_requires", "logical_decomposition"}:
            adjacency.setdefault(row["from"], []).append(row["to"])
proof_pairs = {(r["from"], r["to"], r["type"]) for r in bundle["graphs"]["proof"]["edges"]}
for parent, child, role in list(proof_pairs):
    if role == "proof_requires":
        assert (child, parent, "composes") in proof_pairs
seen, active = set(), set()
def visit(node):
    assert node not in active, f"cycle at {node}"
    if node in seen: return
    active.add(node)
    for child in adjacency.get(node, []): visit(child)
    active.remove(node); seen.add(node)
visit("M0559-ROOT")
assert {r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"} <= seen
for key, field, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == value]
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M0559-N-COMPONENTS", "M0559-T-FORWARD"]
print(f"PASS THM-M-0559 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M4); direct core and theorem completion are not claimed")
