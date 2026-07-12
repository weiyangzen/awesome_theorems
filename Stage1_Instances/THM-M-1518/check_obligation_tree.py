#!/usr/bin/env python3
"""Fail-closed structural and Lean validation of the THM-M-1518 freeze."""

import hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())
assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == "S56-M-1518-OBLIGATION_TREE"
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
rows, nodes = registry["obligations"], bundle["nodes"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 12 and ids[0] == registry["root_obligation_id"]
denominator = hashlib.sha256(json.dumps([{k: row[k] for k in fields} for row in rows], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids", "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile", "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target", "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner", "reviewer", "validity"}
assert len(nodes) == 12 and {n["obligation_id"] for n in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys() and 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of", "transports", "trusts", "documents", "workflow_depends_on"}
seen = set()
for graph in bundle["graphs"].values():
    for e in graph["edges"]:
        assert e["edge_id"] not in seen and e["type"] in allowed and e["from"] in ids and e["to"] in ids
        assert e["edge_id"] in graph["out"][e["from"]] and e["edge_id"] in graph["in"][e["to"]]
        seen.add(e["edge_id"])
proof = {e["edge_id"]: e for e in bundle["graphs"]["proof"]["edges"]}
children = {}
for e in proof.values():
    reverse = proof[e["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == e["edge_id"] and (reverse["from"], reverse["to"]) == (e["to"], e["from"])
    assert {e["type"], reverse["type"]} == {"proof_requires", "composes"}
    if e["type"] == "proof_requires": children.setdefault(e["from"], []).append(e["to"])
visiting, visited = set(), set()
def visit(node):
    assert node not in visiting
    if node in visited: return
    visiting.add(node)
    for child in children.get(node, []): visit(child)
    visiting.remove(node); visited.add(node)
visit("M1518-ROOT")
assert visited == {"M1518-ROOT", "M1518-T-ASSEMBLE", "M1518-N-WEAK", "M1518-N-DIFFERENTIATE", "M1518-L-WEAK-POINTWISE", "M1518-L-IBP", "M1518-L-FUNDAMENTAL"}
assert {n["validation_spec_id"] for n in nodes} == {r["recipe_id"] for r in specs["recipes"]}
assert bundle["closure_boundary"]["root_closed"] is False and bundle["closure_boundary"]["theorem_complete"] is False
lean = (HERE / "ObligationTree.lean").read_text()
assert all(token not in lean for token in ("sorry", "admit", "axiom ", "sorryAx"))
with tempfile.TemporaryDirectory(prefix="thm-m-1518-obligations-") as directory:
    cache = Path(directory); olean = cache / "Stage1_Instances" / "THM-M-1518" / "Statement.olean"; olean.parent.mkdir(parents=True)
    first = subprocess.run(["lake", "env", "lean", "-R", str(ROOT), "-o", str(olean), str(HERE / "Statement.lean")], cwd=LEAN_DIR, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sys.stdout.write(first.stdout); assert first.returncode == 0
    env = os.environ.copy(); env["LEAN_PATH"] = f"{cache}:{env.get('LEAN_PATH', '')}"
    second = subprocess.run(["lake", "env", "lean", str(HERE / "ObligationTree.lean")], cwd=LEAN_DIR, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sys.stdout.write(second.stdout); assert second.returncode == 0
print(f"PASS THM-M-1518 obligation tree: {len(ids)} obligations, {len(seen)} typed edges")
print(f"registry denominator sha256: {denominator}")
print("root closure: open (M4); differentiation, integration by parts, and fundamental lemma remain open")
