#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in registry["obligations"]]
raw = json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
digest = hashlib.sha256(raw).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == 17 == len(set(ids))
assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == "M0311-ROOT"
for row in rows:
    assert set(fields) <= row.keys()
    assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
    assert row["human_source_eligibility"] in {"required", "not_applicable"}
    assert row["readable_eligibility"] in {"required", "not_applicable"}

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt",
                 "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id",
                 "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger",
                 "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources",
                 "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert {n["obligation_id"] for n in nodes} == set(ids) and len(nodes) == 17
for node in nodes:
    assert required_node <= node.keys(), node["obligation_id"]
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}
    assert node["semantic_step_ledger"]
    assert node["step_budget"] == "split-required" or 0 < node["step_budget"] <= 100

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids, proof_adj = set(), {}
proof_pairs, compose_pairs = set(), set()
for name, graph in bundle["graphs"].items():
    local = {edge["edge_id"]: edge for edge in graph["edges"]}
    assert len(local) == len(graph["edges"])
    assert not edge_ids.intersection(local)
    edge_ids.update(local)
    for edge in graph["edges"]:
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
        if edge["type"] == "proof_requires":
            proof_pairs.add((edge["from"], edge["to"]))
            proof_adj.setdefault(edge["from"], []).append(edge["to"])
        if edge["type"] == "composes":
            compose_pairs.add((edge["to"], edge["from"]))
assert proof_pairs == compose_pairs

seen, active = set(), set()
def visit(node):
    assert node not in active, f"proof cycle at {node}"
    if node in seen:
        return
    active.add(node)
    for child in proof_adj.get(node, []):
        visit(child)
    active.remove(node)
    seen.add(node)
visit("M0311-ROOT")
proof_required = {row["obligation_id"] for row in rows if row["machine_eligibility"] == "required" and not row["obligation_id"].startswith("M0311-X-")}
assert proof_required <= seen

for key, field, value in (("required_machine", "machine_eligibility", "required"),
                          ("required_human_source", "human_source_eligibility", "required"),
                          ("required_readable", "readable_eligibility", "required")):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == value]
assert registry["frozen_denominators"]["inventory"] == ids
assert bundle["closure_boundary"]["root_machine_debt"] == "M3"
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M0311-B-REAL", "M0311-B-COMPLEX"]

source = (HERE / "ObligationTree.lean").read_text()
for forbidden in (r"\bsorry\b", r"\badmit\b", r"\baxiom\s", r"\bunsafe\b"):
    assert re.search(forbidden, source.lower()) is None, forbidden
print(f"PASS THM-M-0311 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); scalar candidate bodies are not accepted in this phase")
