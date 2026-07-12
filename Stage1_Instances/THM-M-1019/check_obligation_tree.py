#!/usr/bin/env python3
"""Validate the THM-M-1019 registry and all typed graph indexes."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())

assert registry["item_id"] == bundle["item_id"] == "S56-M-1019-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-1019"
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in registry["obligations"]]
raw = json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
digest = hashlib.sha256(raw).hexdigest()
assert digest == registry["denominator_sha256"]

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == 22 == len(set(ids))
assert registry["root_obligation_id"] == ids[0] == "M1019-ROOT"
root_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert rows[0]["statement_fingerprint"] == "lean-expression-sha256:" + root_hash
for key in ("inventory", "required_machine", "required_human_source", "required_readable"):
    assert registry["frozen_denominators"][key] == ids
assert registry["frozen_denominators"]["informational_overlays"] == []
for row in rows:
    assert set(fields) <= row.keys()
    assert row["machine_eligibility"] == row["human_source_eligibility"] == row["readable_eligibility"] == "required"

required_node = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt",
                 "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id",
                 "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger",
                 "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources",
                 "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == 22 and {node["obligation_id"] for node in nodes} == set(ids)
tree_text = (HERE / "obligation-tree.md").read_text()
for node in nodes:
    assert required_node <= node.keys()
    assert 0 < node["step_budget"] <= 100 and node["semantic_step_ledger"]
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}
    anchor = node["public_readable_target"].split("#", 1)[1]
    assert f'<a id="{anchor}"></a>' in tree_text

expected = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
assert set(bundle["graphs"]) == expected
allowed = {"proof": {"proof_requires", "composes"}, "refinement": {"logical_decomposition", "equivalent_to", "transports"},
           "provenance": {"provenance_of", "source_map"}, "evidence": {"evidence_for"}, "trust": {"trusts"},
           "documentation": {"documents"}, "workflow": {"workflow_depends_on"}}
edge_ids, adjacency = set(), {}
for name, graph in bundle["graphs"].items():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids
        edge_ids.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids and edge["type"] in allowed[name]
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
        if name in {"proof", "refinement"}: adjacency.setdefault(edge["from"], []).append(edge["to"])

seen, active = set(), set()
def visit(oid):
    assert oid not in active, f"cycle at {oid}"
    if oid in seen: return
    active.add(oid)
    for child in adjacency.get(oid, []): visit(child)
    active.remove(oid); seen.add(oid)
visit("M1019-ROOT")
assert seen == set(ids)
assert bundle["closure_boundary"] == {"closed_obligations": [], "root_machine_debt": "M1",
                                      "remaining_root_cut_set": ["M1019-X2"], "composition_certificates_checked": [],
                                      "theorem_complete": False}
print(f"PASS THM-M-1019 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M1); no proof or theorem completion claimed")
