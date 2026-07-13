#!/usr/bin/env python3
"""Fail-closed structural checks for THM-M-0995 registry version 2."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
registry = json.loads((HERE / "obligation-registry.json").read_text())
bundle = json.loads((HERE / "typed-graphs.json").read_text())
specs = json.loads((HERE / "validation-specs.json").read_text())

assert registry["schema_version"] == "stage1-obligation-registry/1.0"
assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
assert specs["schema_version"] == "stage1-validation-specs/1.0"
assert registry["registry_version"] == bundle["registry_version"] == specs["registry_version"] == 2
assert {registry["item_id"], bundle["item_id"], specs["item_id"]} == {"S56-M-0995-OBLIGATION_TREE"}
assert {registry["theorem_id"], bundle["theorem_id"], specs["theorem_id"]} == {"THM-M-0995"}
assert registry["frozen_against_statement_sha256"] == hashlib.sha256((HERE / "statement.json").read_bytes()).hexdigest()
assert registry["frozen_against_anchor_audit_sha256"] == hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()

history = registry["registry_history"]
assert history == [{
    "registry_version": 1,
    "registry_sha256": "1150adeecf0ca78639706ee32c082dfebbbd58d576db1d17ca039852d0bce100",
    "denominator_sha256": "40ec266a8614befd347bb0f00848703182aac04f6446a113a6a2e6b1a0348794",
    "inventory": ["M0995-ROOT", "M0995-S-EXACT", "M0995-L-IND-MGF", "M0995-L-SUM-MGF",
                  "M0995-L-CHERNOFF", "M0995-L-OPTIMIZE", "M0995-B-ZERO-DENOM",
                  "M0995-B-EMPTY", "M0995-T-ASSEMBLE", "M0995-X-MATHLIB",
                  "M0995-X-EXTERNAL", "M0995-X-SOURCE", "M0995-X-TCB"],
    "supersession_reason": "M0995-L-OPTIMIZE was false on an allowed positive-denominator, zero-variance input; the root requires an explicit zero/positive variance split.",
}]

delta = registry["append_only_delta"]
assert delta["from_version"] == 1 and delta["to_version"] == 2
assert delta["retired_ids"] == [{
    "obligation_id": "M0995-L-OPTIMIZE",
    "reason": "false_interface_refuted_by_local_kernel_proof",
    "replacement_ids": ["M0995-L-OPTIMIZE-POS", "M0995-L-VAR-ZERO-AE", "M0995-B-VAR-ZERO", "M0995-T-VAR-ZERO"],
}]
assert delta["replaced_ids"] == [{
    "old_id": "M0995-T-ASSEMBLE", "new_id": "M0995-T-ASSEMBLE-V2",
    "reason": "composition now consumes the exhaustive zero/positive variance branches",
}]

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
assert len(ids) == len(set(ids)) == 21
assert registry["root_obligation_id"] == "M0995-ROOT"
assert "M0995-L-OPTIMIZE" not in ids and "M0995-T-ASSEMBLE" not in ids
assert set(delta["preserved_ids"]) | set(delta["added_ids"]) | {"M0995-T-ASSEMBLE-V2"} == set(ids)

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
          "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in rows]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
assert digest == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert digest == specs["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
for key, field in (("required_machine", "machine_eligibility"),
                   ("required_human_source", "human_source_eligibility"),
                   ("required_readable", "readable_eligibility")):
    assert registry["frozen_denominators"][key] == [r["obligation_id"] for r in rows if r[field] == "required"]

required = {"node_id", "obligation_id", "kind", "human_statement", "formal_target", "human_debt",
            "machine_debt", "readability_debt", "step_budget", "semantic_step_ledger",
            "public_readable_target", "validation_spec_id", "status_boundary", "owner", "reviewer", "validity"}
nodes = bundle["nodes"]
assert len(nodes) == len(ids) and {node["obligation_id"] for node in nodes} == set(ids)
for node in nodes:
    assert required <= node.keys()
    assert 0 < node["step_budget"] <= 100
    assert {"premises", "inference", "output", "outgoing_use"} <= node["semantic_step_ledger"].keys()
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}

allowed = {"proof_requires", "composes", "logical_decomposition", "source_map", "provenance_of",
           "evidence_for", "trusts", "documents", "workflow_depends_on"}
edge_ids = set()
for graph in bundle["graphs"].values():
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed
        assert edge["from"] in ids and edge["to"] in ids
        assert edge["edge_id"] in graph["out"][edge["from"]]
        assert edge["edge_id"] in graph["in"][edge["to"]]
        edge_ids.add(edge["edge_id"])

proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
children = {}
for edge in proof.values():
    reverse = proof[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert {edge["type"], reverse["type"]} == {"proof_requires", "composes"}
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])

active, visited = set(), set()
def visit(node):
    assert node not in active, f"proof cycle at {node}"
    if node in visited:
        return
    active.add(node)
    for child in children.get(node, []):
        visit(child)
    active.remove(node)
    visited.add(node)

visit("M0995-ROOT")
assert visited == {"M0995-ROOT", "M0995-T-ASSEMBLE-V2", "M0995-L-SUM-MGF", "M0995-T-SUM-MGF",
                   "M0995-L-IND-MGF", "M0995-T-IND-MGF", "M0995-L-EXP-REMAINDER",
                   "M0995-L-PREFIX-MGF", "M0995-L-CHERNOFF", "M0995-L-OPTIMIZE-POS",
                   "M0995-B-VAR-ZERO", "M0995-T-VAR-ZERO", "M0995-B-ZERO-DENOM",
                   "M0995-L-VAR-ZERO-AE"}
assert set(registry["frozen_denominators"]["required_machine"]) - visited == {
    "M0995-S-EXACT", "M0995-B-EMPTY"
}

recipe_ids = {recipe["recipe_id"] for recipe in specs["recipes"]}
assert len(recipe_ids) == len(ids) and {node["validation_spec_id"] for node in nodes} == recipe_ids
for recipe in specs["recipes"]:
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["argv"] == ["bash", "check_proof.sh"]
    assert set(recipe["covered_obligation_ids"]) <= set(ids)
    assert {"cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations"} <= recipe.keys()

boundary = bundle["closure_boundary"]
required_machine = registry["frozen_denominators"]["required_machine"]
assert boundary["closed_obligations"] == required_machine
assert boundary["root_closed"] is True and boundary["root_machine_debt"] == "M0-L"
assert boundary["remaining_root_cut_set"] == []
assert boundary["audit_complete"] is False and boundary["theorem_complete"] is False

assert "root_compose_v2" in (HERE / "ObligationTree.lean").read_text()
assert "bernsteinInequality_via_registry_v2" in (HERE / "Proof.lean").read_text()
assert "#print axioms Stage1Instances.THM_M_0995.Proof.bernsteinInequality_via_registry_v2" in (HERE / "Proof.lean").read_text()
receipt_path = HERE / "proof-receipt.json"
if receipt_path.exists():
    receipt = json.loads(receipt_path.read_text())
    assert receipt["item_id"] == "S56-M-0995-PROOF"
    assert receipt["inputs"]["registry_denominator_sha256"] == digest
    assert receipt["inputs"]["obligation_registry_sha256"] == hashlib.sha256((HERE / "obligation-registry.json").read_bytes()).hexdigest()
    assert receipt["inputs"]["obligation_tree_sha256"] == hashlib.sha256((HERE / "ObligationTree.lean").read_bytes()).hexdigest()
    assert receipt["proof_body"]["source_sha256"] == hashlib.sha256((HERE / "Proof.lean").read_bytes()).hexdigest()

print(f"PASS THM-M-0995 registry v2: {len(ids)} obligations, {len(edge_ids)} typed edges")
print(f"registry denominator sha256: {digest}")
print("exact root proof machine-closed provisionally; downstream assurance gates remain open")
