#!/usr/bin/env python3
"""Fail-closed structural validation for THM-M-1063's architecture freeze."""
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == "S56-M-1063-OBLIGATION_TREE"
assert registry["theorem_id"] == bundle["theorem_id"] == "THM-M-1063"
rows = registry["obligations"]; ids = [r["obligation_id"] for r in rows]
assert len(ids) == len(set(ids)) == 31
assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == "M1063-ROOT"
row_fields = {"obligation_id","statement_fingerprint","kind","root_relevant","machine_eligibility","human_source_eligibility","readable_eligibility","risk_class","exclusion_reason","terminal_proof_body_id"}
assert all(row_fields <= r.keys() for r in rows)
assert all(r["statement_fingerprint"].startswith(("lean-expression-sha256:","planned:v1:sha256:")) for r in rows)
assert all(r["terminal_proof_body_id"] is None for r in rows)
den = registry["frozen_denominators"]
assert den["inventory"] == ids
assert den["required_machine"] == [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"]
assert den["required_human_source"] == [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"]
assert den["required_readable"] == ids
assert set(den["informational_overlays"]) == {"M1063-X-SOURCE","M1063-X-PROVENANCE"}
digest = hashlib.sha256(json.dumps(den, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == bundle["registry_denominator_sha256"]
assert bundle["statement_source_sha256"] == hashlib.sha256((HERE / "DonskerTarget.lean").read_bytes()).hexdigest()
node_fields = {"node_id","obligation_id","kind","human_statement","formal_target","output","human_debt","machine_debt","readability_debt","evidence_ids","source_crosswalk_id","provenance_id","foundation_profile","tcb_profile","computation_record","step_budget","semantic_step_ledger","public_readable_target","validation_spec_id","status_boundary","task_ids","owned_sources","owner","reviewer","validity"}
nodes = bundle["nodes"]
assert [n["node_id"] for n in nodes] == ids and all(node_fields <= n.keys() for n in nodes)
assert all(0 < n["step_budget"] <= 100 and n["step_budget"] == len(n["semantic_step_ledger"]) for n in nodes)
assert set(bundle["graphs"]) == {"proof","refinement","provenance","evidence","trust","documentation","workflow"}
all_edges, proof_adj = set(), {}
for name, graph in bundle["graphs"].items():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in all_edges; all_edges.add(edge["edge_id"])
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"].get(edge["from"], [])
        assert edge["edge_id"] in graph["in"].get(edge["to"], [])
        if name == "proof": proof_adj.setdefault(edge["from"], []).append(edge["to"])
def reaches_root(start):
    frontier, seen = [start], set()
    while frontier:
        node = frontier.pop()
        if node == "M1063-ROOT": return True
        assert node not in seen, f"proof cycle at {node}"
        seen.add(node); frontier.extend(proof_adj.get(node, []))
    return False
assert all(reaches_root(oid) for oid in den["required_machine"])
closure = bundle["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M4"
assert set(closure["remaining_root_cut_set"]) <= set(den["required_machine"])
for path in HERE.glob("*.lean"):
    text = path.read_text()
    assert not any(line.lstrip().startswith(("sorry", "admit", "axiom ")) for line in text.splitlines())
print(f"PASS THM-M-1063 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M4); no proof or theorem completion claimed")
