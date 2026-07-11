#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "obligation-graphs.json").read_text())
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason")
projection = [{key: row[key] for key in fields} for row in registry["obligations"]]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert registry["denominator_sha256"] == digest

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) and "M0402-ROOT" in ids
nodes = bundle["nodes"]
assert set(ids) == {node["node_id"] for node in nodes} == {node["obligation_id"] for node in nodes}
required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
            "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
            "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
            "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
            "task_ids", "owned_sources", "owner", "reviewer", "validity"}
for node in nodes:
    assert required <= node.keys()
    assert 0 < node["step_budget"] <= 100 and node["semantic_step_ledger"]

assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = set()
for name, graph in bundle["graphs"].items():
    edge_map = {edge["edge_id"]: edge for edge in graph["edges"]}
    assert len(edge_map) == len(graph["edges"]) and not (all_edges & edge_map.keys())
    all_edges |= edge_map.keys()
    for edge in graph["edges"]:
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
    assert set(edge_map) == {x for xs in graph["out"].values() for x in xs}
    assert set(edge_map) == {x for xs in graph["in"].values() for x in xs}, name

children = {}
for edge in bundle["graphs"]["proof"]["edges"]:
    children.setdefault(edge["from"], []).append(edge["to"])
seen, active = set(), set()
def visit(node):
    assert node not in active, f"proof cycle at {node}"
    if node in seen:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    seen.add(node)
visit("M0402-ROOT")
mathematical = {row["obligation_id"] for row in rows if row["root_relevant"] and
                row["machine_eligibility"] == "required" and row["kind"] not in {"definition", "trust", "provenance"}}
assert mathematical <= seen
for key, eligibility in (("required_machine", "machine_eligibility"),
                         ("required_human_source", "human_source_eligibility"),
                         ("required_readable", "readable_eligibility")):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[eligibility] == "required"]
assert registry["frozen_denominators"]["inventory"] == ids
assert bundle["closure_boundary"]["closed_obligations"] == []
assert bundle["closure_boundary"]["theorem_complete"] is False
print(f"PASS THM-M-0402 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); no proof or theorem completion claimed")
