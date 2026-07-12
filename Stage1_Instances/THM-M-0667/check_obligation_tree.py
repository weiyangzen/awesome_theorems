#!/usr/bin/env python3
"""Validate THM-M-0667 frozen architecture and scoped Lean composition."""

import hashlib, json, os, subprocess, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
reg = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: o[k] for k in fields} for o in reg["obligations"]]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == reg["denominator_sha256"] == bundle["registry_denominator_sha256"]
ids = [o["obligation_id"] for o in reg["obligations"]]
assert len(ids) == len(set(ids)) == 16 and ids[0] == reg["root_obligation_id"] == "M0667-ROOT"
assert reg["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
assert {n["obligation_id"] for n in bundle["nodes"]} == set(ids)
required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt",
            "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id",
            "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger",
            "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources",
            "owner", "reviewer", "validity"}
for n in bundle["nodes"]:
    assert required <= n.keys()
    assert n["step_budget"] == "split-required" or 0 < n["step_budget"] <= 100
    assert set(n["semantic_step_ledger"]) == {"premises", "inference", "output", "source_anchors", "outgoing_use"}
assert set(bundle["graphs"]) == {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
edge_ids, adjacency = set(), {}
for name, graph in bundle["graphs"].items():
    for e in graph["edges"]:
        assert e["edge_id"] not in edge_ids and e["from"] in ids and e["to"] in ids
        edge_ids.add(e["edge_id"])
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        if name == "refinement" or (name == "proof" and e["type"] == "proof_requires"):
            adjacency.setdefault(e["from"], []).append(e["to"])
proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
for e in proof.values():
    reverse = proof[e["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == e["edge_id"] and (reverse["from"], reverse["to"]) == (e["to"], e["from"])
seen, active = set(), set()
def visit(x):
    assert x not in active
    if x in seen: return
    active.add(x)
    for y in adjacency.get(x, []): visit(y)
    active.remove(x); seen.add(x)
visit("M0667-ROOT")
assert {o["obligation_id"] for o in reg["obligations"] if o["machine_eligibility"] == "required"} <= seen
for key, field, value in (("required_machine", "machine_eligibility", "required"), ("required_human_source", "human_source_eligibility", "required"), ("required_readable", "readable_eligibility", "required")):
    assert reg["frozen_denominators"][key] == [o["obligation_id"] for o in reg["obligations"] if o[field] == value]
assert bundle["closure_boundary"]["theorem_complete"] is False
assert bundle["closure_boundary"]["remaining_root_cut_set"] == ["M0667-N-DOMINATION", "M0667-X-FOUNDATION", "M0667-X-SOURCE"]

lean_root = ROOT / "Formalizations" / "Lean"
lp = subprocess.run(["lake", "env", "printenv", "LEAN_PATH"], cwd=lean_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
assert lp.returncode == 0, lp.stdout
lb = subprocess.run(["lake", "env", "which", "lean"], cwd=lean_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
assert lb.returncode == 0, lb.stdout
with tempfile.TemporaryDirectory(prefix="thm-m-0667-") as td:
    statement = subprocess.run([lb.stdout.strip(), "-o", str(Path(td) / "Statement.olean"), "Statement.lean"], cwd=HERE,
                               env={**os.environ, "LEAN_PATH": lp.stdout.strip()}, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert statement.returncode == 0, statement.stdout
    result = subprocess.run([lb.stdout.strip(), "ObligationTree.lean"], cwd=HERE,
                            env={**os.environ, "LEAN_PATH": td + ":" + lp.stdout.strip()}, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert result.returncode == 0, result.stdout
    assert "root_of_domination" in result.stdout and "sorryAx" not in result.stdout
print(f"PASS THM-M-0667 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("conditional composition elaborated; root remains open at M3")
