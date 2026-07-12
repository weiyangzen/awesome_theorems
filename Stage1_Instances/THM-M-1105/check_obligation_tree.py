#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
reg = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())

assert reg["item_id"] == "S56-M-1105-OBLIGATION_TREE"
assert reg["theorem_id"] == bundle["theorem_id"] == "THM-M-1105"
assert reg["registry_version"] == bundle["registry_version"] == 1
obs = reg["obligations"]
ids = [o["obligation_id"] for o in obs]
assert len(ids) == len(set(ids)) == 22
assert reg["root_obligation_id"] == "M1105-ROOT"

required_obligation = {"obligation_id", "statement_fingerprint", "kind", "root_relevant",
  "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class",
  "exclusion_reason", "terminal_proof_body_id"}
assert all(set(o) == required_obligation for o in obs)
den = reg["frozen_denominators"]
assert den["inventory"] == ids
assert set(den["required_machine"]) == {o["obligation_id"] for o in obs if o["machine_eligibility"] == "required"}
assert set(den["required_human_source"]) == {o["obligation_id"] for o in obs if o["human_source_eligibility"] == "required"}
assert set(den["required_readable"]) == set(ids)
assert set(den["informational_overlays"]) == {"M1105-X-SOURCE", "M1105-X-PROVENANCE"}
assert all(o["terminal_proof_body_id"] is None for o in obs)

nodes = bundle["nodes"]
assert {n["obligation_id"] for n in nodes} == set(ids)
node_fields = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
 "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id",
 "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget",
 "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary",
 "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert all(set(n) == node_fields for n in nodes)
assert all(0 < n["step_budget"] <= 100 and n["semantic_step_ledger"] for n in nodes)
assert all(n["machine_debt"] == "M3" and not n["evidence_ids"] for n in nodes)

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map",
 "expository_decomposition", "equivalent_to", "transports", "evidence_for", "provenance_of",
 "documents", "trusts", "workflow_depends_on"}
graphs = bundle["graphs"]
assert set(graphs) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
all_edges = [e for es in graphs.values() for e in es]
assert all(set(e) == {"from", "to", "type"} and e["type"] in allowed for e in all_edges)
assert len({(e["from"], e["to"], e["type"]) for e in all_edges}) == len(all_edges)
assert all(e["from"] in ids and e["to"] in ids for g in ["proof", "refinement", "provenance", "trust", "documentation"] for e in graphs[g])
assert all(e["type"] == "workflow_depends_on" for e in graphs["workflow"])

proof_adj = {}
for e in graphs["proof"]:
    if e["type"] == "proof_requires":
        proof_adj.setdefault(e["from"], []).append(e["to"])
def reaches_root(start):
    stack, seen = [start], set()
    while stack:
        cur = stack.pop()
        if cur == "M1105-ROOT": return True
        assert cur not in seen, f"proof cycle at {cur}"
        seen.add(cur); stack.extend(proof_adj.get(cur, []))
    return False
assert all(reaches_root(x) for x in den["required_machine"])

certs = bundle["composition_certificates"]
assert certs == [{"parent":"M1105-ROOT","children":["M1105-T-COMPOSE"],
 "lean_declaration":"root_of_sample_weak_convergence","status":"interface_checked_children_open"}]
closure = bundle["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["root_machine_debt"] == "M3"
assert set(closure["remaining_root_cut_set"]) <= set(den["required_machine"])

statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert bundle["source_bindings"]["statement_source_sha256"] == statement_hash
for path in HERE.glob("*.lean"):
    text = path.read_text()
    assert "sorry" not in text and "admit" not in text and "axiom " not in text

digest = hashlib.sha256("\n".join(ids).encode()).hexdigest()
print(f"PASS THM-M-1105 obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges")
print(f"registry denominator sha256: {digest}")
print("root closure: open (M3); no proof or theorem completion claimed")
