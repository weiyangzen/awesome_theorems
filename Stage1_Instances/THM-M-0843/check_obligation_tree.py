#!/usr/bin/env python3
"""Fail-closed structural and Lean checks for THM-M-0843 obligations."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
LEAN_EXE = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0843-OBLIGATION_TREE"
THEOREM = "THM-M-0843"
BASE_REVISION = "02cc55f883d5b5d091ead6851bffe89199eb8391"
BASE_TREE = "035212d041a1e61553b3d2f465964c9bbb35e47d"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
STATEMENT_SHA256 = "6afd11f23d5245eaa4c487ad4484249b517f6fcf4f99373a2f437d5307aee9ec"
ANCHOR_SHA256 = "8c581b2d671b928481cd73876bf71c3ea0a3b4f1a06c2021946401741f814d20"
REGULARITY_SOURCE_HASHES = {
    "Bound.lean": "4b8f892d4cede7359c792bbcff09d4f9a86136edc405f1e287b767d3b362b99a",
    "Chunk.lean": "238f19d5547c346f7eeaff02e84b4ab78279594d38dacfa990e51bc666d82008",
    "Energy.lean": "e2ead2d6b414091f83a91e8561b014394407eaedab6a9801bc467d9fa54fc95c",
    "Equitabilise.lean": "546ad28d80d0b064fa928bb791cf8204bc2f10ab734f250101408cdee8ee868f",
    "Increment.lean": "74f073e00ff00483af32a7a32168bd157ffb3d54c6952216399d60371045eb4c",
    "Lemma.lean": "eee7f2c505130c4a09fa8e62dca7bc1bbfaff90c18e86e9ad43f44f7f0ea8fd6",
    "Uniform.lean": "05197020a8ccd5a34989502d2e0ef1f271f9b6cd1436970406f4d72be4e5d77c",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


registry = load("obligation-registry.json")
bundle = load("typed-graphs.json")
specs = load("validation-specs.json")
receipt_path = HERE / "obligation-tree-receipt.json"
receipt = load("obligation-tree-receipt.json") if receipt_path.exists() else None

assert registry["schema_version"] == "stage1-obligation-registry/1.0"
assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
assert specs["schema_version"] == "stage1-validation-specs/1.0"
assert {registry["item_id"], bundle["item_id"], specs["item_id"]} == {ITEM}
assert {registry["theorem_id"], bundle["theorem_id"], specs["theorem_id"]} == {THEOREM}
assert registry["registry_id"] == bundle["registry_id"] == "THM-M-0843-OBLIGATIONS-v1"
assert registry["registry_version"] == 1 and registry["append_only_delta"] == []
assert output("git", "rev-parse", "HEAD") == BASE_REVISION
assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
assert sha256(HERE / "anchor-audit.json") == ANCHOR_SHA256
assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
assert registry["frozen_against_anchor_audit_sha256"] == ANCHOR_SHA256

manifest = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
assert target["execution_rank"] == 1032
assert target["baseline"] == "L0" and target["rework_required"] is True
assert target["theorem_complete"] is False
execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["phase"] == "obligation_tree" and item["layer"] == 3
assert item["depends_on"] == ["S56-M-0843-ANCHOR_AUDIT"]
assert item["owned_paths"] == ["Stage1_Instances/THM-M-0843"]
assert item["state"] in {"[ ]", "[_]"}

rows = registry["obligations"]
ids = [row["obligation_id"] for row in rows]
id_set = set(ids)
assert len(ids) == len(id_set) == 44
assert registry["root_obligation_id"] == "M0843-ROOT"
assert bundle["root_node_id"] == "THM-M-0843-ROOT"
required_obligation = {
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
}
for row in rows:
    assert required_obligation == set(row)
    assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
    assert row["human_source_eligibility"] in {"required", "not_applicable"}
    assert row["readable_eligibility"] in {"required", "not_applicable"}
    assert row["risk_class"] in {"critical", "high", "normal", "low"}
    assert row["root_relevant"] is True
    if row["machine_eligibility"] == "required":
        assert row["exclusion_reason"] is None
    else:
        assert row["exclusion_reason"] == "support_overlay_no_proof_credit"

fields = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)
projection = [{key: row[key] for key in fields} for row in rows]
denominator = canonical_digest(projection)
assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
assert registry["frozen_denominators"]["inventory"] == ids
for key, field, value in (
    ("required_machine", "machine_eligibility", "required"),
    ("required_human_source", "human_source_eligibility", "required"),
    ("required_readable", "readable_eligibility", "required"),
):
    assert registry["frozen_denominators"][key] == [row["obligation_id"] for row in rows if row[field] == value]
assert registry["frozen_denominators"]["informational_overlays"] == ["M0843-X-PROVENANCE", "M0843-X-TRUST"]
for oid in ("M0843-T-ADAPTER", "M0843-T-UPSTREAM"):
    assert next(row for row in rows if row["obligation_id"] == oid)["statement_fingerprint"].startswith("lean-declaration-type-sha256:")
local_dag = json.loads((HERE / "task-dag.json").read_text(encoding="utf-8"))
local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
assert local_task["state"] == "open" and local_task["accepted_state"] == "open"
assert local_task["provisional_worker_state"] == "[_]"
assert local_task["covered_obligation_ids"] == ids
assert local_task["validation_spec_ids"] == ["VAL-M0843-OBLIGATION-BUNDLE"]
assert local_task["evidence_ids"] == ["S56-M-0843-OBLIGATION_TREE-worker-02cc55f8"]
status = registry["status_observed_after_freeze"]
assert status["closed_obligations"] == []
assert status["accepted_root_machine_debt"] == "M3"
assert "E2" in status["candidate_route"] and "not accepted" in status["candidate_route"]

required_node = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity",
}
nodes = bundle["nodes"]
node_by_id = {node["obligation_id"]: node for node in nodes}
assert len(nodes) == len(node_by_id) == len(ids) and set(node_by_id) == id_set
readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8").lower()
step_ids = set()
for node in nodes:
    assert required_node == set(node)
    assert node["node_id"] == THEOREM + "-" + node["obligation_id"].removeprefix("M0843-")
    assert node["human_debt"] in {f"H{i}" for i in range(6)}
    assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
    assert node["readability_debt"] in {f"R{i}" for i in range(5)}
    assert node["machine_debt"] not in {"M0-L", "M0-W", "M0-P", "M1", "M2"}
    assert 0 < node["step_budget"] <= 100
    ledger = node["semantic_step_ledger"]
    assert isinstance(ledger, list) and 0 < len(ledger) <= node["step_budget"]
    for step in ledger:
        assert set(step) == {"step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use"}
        assert step["step_id"] not in step_ids and step["inference"] and step["source_locator"]
        assert step["output"] and step["outgoing_use"] and step["premise_ids"]
        step_ids.add(step["step_id"])
    path, anchor = node["public_readable_target"].split("#", 1)
    assert path == "Stage1_Instances/THM-M-0843/obligation-tree.md"
    assert f"### {anchor}" in readable
    assert node["validation_spec_id"] == "VAL-M0843-OBLIGATION-BUNDLE"
    assert node["validity"]["revocation_state"] == "not-accepted"
    assert "no m0" in node["status_boundary"].lower()
    assert node["task_ids"] == [ITEM]
allowed_external_premises = {
    "frozen-formal-context", "frozen-finite-partition-context",
    "frozen-nonuniform-pair-witnesses", "frozen-nonuniform-partition-context",
    "frozen-finpartition-context",
}
for node in nodes:
    for step in node["semantic_step_ledger"]:
        assert set(step["premise_ids"]) <= id_set | step_ids | allowed_external_premises

allowed_edges = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "provenance_of", "evidence_for", "trusts", "documents",
    "workflow_depends_on",
}
assert set(bundle["graphs"]) == {
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow",
}
workflow_nodes = set(bundle["workflow_task_nodes"])
assert workflow_nodes == {
    "S56-M-0843-ANCHOR_AUDIT", ITEM, "S56-M-0843-PROOF",
    "S56-M-0843-VALIDATION", "S56-M-0843-RELEASE",
}
edge_ids = set()
for name, graph in bundle["graphs"].items():
    expected_in: dict[str, list[str]] = {}
    expected_out: dict[str, list[str]] = {}
    for edge in graph["edges"]:
        assert edge["edge_id"] not in edge_ids and edge["type"] in allowed_edges
        endpoints = workflow_nodes if name == "workflow" else id_set
        assert edge["from"] in endpoints and edge["to"] in endpoints
        if name == "workflow":
            assert edge["type"] == "workflow_depends_on"
        else:
            assert edge["type"] != "workflow_depends_on"
        expected_out.setdefault(edge["from"], []).append(edge["edge_id"])
        expected_in.setdefault(edge["to"], []).append(edge["edge_id"])
        edge_ids.add(edge["edge_id"])
    assert graph["out"] == expected_out and graph["in"] == expected_in

for graph_name in ("refinement", "provenance", "evidence", "trust", "documentation", "workflow"):
    adjacency: dict[str, list[str]] = {}
    for edge in bundle["graphs"][graph_name]["edges"]:
        adjacency.setdefault(edge["from"], []).append(edge["to"])
    graph_visiting: set[str] = set()
    graph_visited: set[str] = set()

    def visit_graph(node_id: str) -> None:
        assert node_id not in graph_visiting, f"{graph_name} cycle at {node_id}"
        if node_id in graph_visited:
            return
        graph_visiting.add(node_id)
        for target_id in adjacency.get(node_id, []):
            visit_graph(target_id)
        graph_visiting.remove(node_id)
        graph_visited.add(node_id)

    for source_id in adjacency:
        visit_graph(source_id)

source_edges = bundle["graphs"]["provenance"]["edges"]
for oid in ids:
    obligation = next(row for row in rows if row["obligation_id"] == oid)
    if oid != "M0843-X-SOURCE" and obligation["human_source_eligibility"] == "required":
        assert any(edge["from"] == oid and edge["type"] == "source_map" and edge["to"] == "M0843-X-SOURCE" for edge in source_edges)
    if oid not in {"M0843-X-PROVENANCE", "M0843-X-SOURCE", "M0843-X-TRUST"}:
        assert any(edge["from"] == "M0843-X-PROVENANCE" and edge["type"] == "provenance_of" and edge["to"] == oid for edge in source_edges)
        assert any(edge["from"] == "M0843-X-PROVENANCE" and edge["type"] == "evidence_for" and edge["to"] == oid for edge in bundle["graphs"]["evidence"]["edges"])
    if oid != "M0843-X-SOURCE":
        assert any(edge["from"] == "M0843-X-SOURCE" and edge["type"] == "documents" and edge["to"] == oid for edge in bundle["graphs"]["documentation"]["edges"])

proof_edges = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
children: dict[str, list[str]] = {}
for edge in proof_edges.values():
    assert edge["type"] in {"proof_requires", "composes", "logical_decomposition"}
    reverse = proof_edges[edge["reciprocal_edge_id"]]
    assert reverse["reciprocal_edge_id"] == edge["edge_id"]
    assert (reverse["from"], reverse["to"]) == (edge["to"], edge["from"])
    assert "proof_requires" in {edge["type"], reverse["type"]}
    other_type = reverse["type"] if edge["type"] == "proof_requires" else edge["type"]
    expected_reverse = "composes" if (edge["from"] == "M0843-ROOT" or edge["to"] == "M0843-ROOT") else "logical_decomposition"
    assert other_type == expected_reverse
    if edge["type"] == "proof_requires":
        children.setdefault(edge["from"], []).append(edge["to"])

visiting: set[str] = set()
visited: set[str] = set()


def visit(oid: str) -> None:
    assert oid not in visiting, f"proof cycle at {oid}"
    if oid in visited:
        return
    visiting.add(oid)
    for child in children.get(oid, []):
        visit(child)
    visiting.remove(oid)
    visited.add(oid)


visit("M0843-ROOT")
assert set(children) <= visited
assert len(visited) == 38
assert all(node_by_id[oid]["machine_debt"] == "M3" for oid in visited)
closure_required = set(visited)
for edge in bundle["graphs"]["refinement"]["edges"]:
    if edge["type"] == "logical_decomposition" and edge["from"] == "M0843-ROOT":
        closure_required.add(edge["to"])
assert {"M0843-S-TARGET", "M0843-S-BOUNDARY"} <= closure_required
assert all(node_by_id[oid]["machine_debt"] not in {"M0-L", "M0-W", "M0-P"} for oid in closure_required)

certificates = {row["parent_obligation_id"]: row for row in bundle["composition_certificates"]}
assert set(certificates) == {"M0843-ROOT"}
for parent, cert in certificates.items():
    required_children = children[parent]
    assert cert["required_child_ids"] == required_children
    assert cert["parent_statement_fingerprint"] == next(
        row["statement_fingerprint"] for row in rows
        if row["obligation_id"] == parent
    )
    assert cert["required_child_statement_fingerprints"] == {
        child: next(
            row["statement_fingerprint"] for row in rows
            if row["obligation_id"] == child
        ) for child in required_children
    }
    assert cert["introduces_undeclared_premises"] is False
    assert cert["status"] == "provisionally_elaborated_not_accepted"
    assert cert["certificate_kind"] == "lean_abstract_child_harness"
plans = {row["parent_obligation_id"]: row for row in bundle["unverified_decomposition_plans"]}
assert set(plans) == set(children) - set(certificates)
for parent, plan in plans.items():
    assert plan["planned_child_ids"] == children[parent]
    assert plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
    assert "exact abstract-child harness" in plan["required_future_certificate"]

closure = bundle["closure_boundary"]
assert closure["closed_obligations"] == [] and closure["root_closed"] is False
assert closure["accepted_root_machine_debt"] == "M3"
assert closure["audit_complete"] is False and closure["theorem_complete"] is False
assert set(closure["proof_leaf_cut_set"]) == visited - set(children)
assert "M0843-C01/E2" in closure["candidate_evidence"]

assert len(specs["recipes"]) == 1
recipe = specs["recipes"][0]
assert recipe["recipe_id"] == "VAL-M0843-OBLIGATION-BUNDLE"
assert recipe["argv"] == ["python3", "-B", "Stage1_Instances/THM-M-0843/check_obligation_tree.py"]
assert recipe["network_policy"] == "denied"
assert set(recipe["covered_obligation_ids"]) == id_set
assert set(recipe["covered_declarations"]) == {
    "Stage1Instances.THM_M_0843.SzemerediRegularityTarget",
    "szemeredi_regularity",
    "Stage1Instances.THM_M_0843_Obligations.terminal_adapter",
    "Stage1Instances.THM_M_0843_Obligations.compose_root",
}
assert "kernel declaration coverage is limited" in recipe["coverage_boundary"]
assert set(recipe["env_allowlist"]) == {"PATH", "HOME", "TMPDIR", "PYTHONDONTWRITEBYTECODE"}
assert all(set(row) == {"path_or_stream", "semantic_hash_policy"} for row in recipe["expected_outputs"])
assert recipe["expected_exit"] == 0

assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
assert output("git", "status", "--short", cwd=MATHLIB) == ""
regularity = MATHLIB / "Mathlib/Combinatorics/SimpleGraph/Regularity"
for name, expected in REGULARITY_SOURCE_HASHES.items():
    assert sha256(regularity / name) == expected, name

lemma = (regularity / "Lemma.lean").read_text(encoding="utf-8")
increment = (regularity / "Increment.lean").read_text(encoding="utf-8")
for marker in (
    "obtain hα | hα := le_total (card α) (bound ε l)",
    "exists_equipartition_card_eq",
    "obtain hε₁ | hε₁ := le_total 1 ε",
    "suffices h : ∀ i",
    "induction i with",
    "by_cases huniform : P.IsUniform G ε",
    "energy_increment hP₁",
):
    assert marker in lemma, marker
for marker in (
    "theorem card_increment",
    "theorem increment_isEquipartition",
    "private theorem distinctPairs_increment",
    "private lemma pairwiseDisjoint_distinctPairs",
    "lemma le_sum_distinctPairs_edgeDensity_sq",
    "theorem energy_increment",
):
    assert marker in increment, marker

lean_source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
without_comments = re.sub(r"/-.*?-/", "", lean_source, flags=re.DOTALL)
without_comments = re.sub(r"--.*", "", without_comments)
assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|implemented_by)\b", without_comments)
for marker in (
    "import Statement",
    "def MathlibTerminal : Prop",
    "theorem terminal_adapter",
    "theorem pinned_mathlib_terminal",
    "theorem compose_root",
    "adapter terminal",
    "#print sorries szemeredi_regularity",
    "#print axioms compose_root",
):
    assert marker in lean_source, marker

with tempfile.TemporaryDirectory(prefix="thm-m-0843-obligation-") as temp_dir:
    statement_olean = str(Path(temp_dir) / "Statement.olean")
    statement_lean = subprocess.run(
        [str(LEAN_EXE), "Statement.lean", "-o", statement_olean],
        cwd=HERE,
        env=os.environ | {"LEAN_PATH": output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)},
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    if statement_lean.returncode:
        sys.stdout.write(statement_lean.stdout)
        raise SystemExit(statement_lean.returncode)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    lean_env = os.environ | {"LEAN_PATH": temp_dir + ":" + lean_path}
    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0843/ObligationTree.lean"],
        cwd=LEAN_ROOT,
        env=lean_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
normalized = re.sub(r"\s+", " ", lean.stdout)
assert "Declarations are sorry-free!" in lean.stdout
assert normalized.count("propext, Classical.choice, Quot.sound") == 4
for declaration in (
    "szemeredi_regularity", "terminal_adapter", "pinned_mathlib_terminal", "compose_root",
):
    assert declaration in lean.stdout

if receipt is not None:
    assert receipt["schema_version"] == "stage1-obligation-tree-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["registry_denominator_sha256"] == denominator
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["obligation_count"] == len(ids)
    assert receipt["typed_edge_count"] == len(edge_ids)
    assert receipt["substantive_ledger_step_count"] == len(step_ids)
    assert receipt["unverified_internal_decomposition_count"] == len(plans)
    assert receipt["composition_declarations"] == ["Stage1Instances.THM_M_0843_Obligations.compose_root"]
    assert receipt["closed_obligations"] == []
    packet = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
    assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] and packet["output_summary"]

print(f"PASS THM-M-0843 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges, {len(step_ids)} substantive ledger steps")
print(f"registry denominator sha256: {denominator}")
print("Lean: exact terminal/adapter/root composition elaborated; sorry-free terminal; axioms propext, Classical.choice, Quot.sound")
print("accepted root remains H1/M3/R4; closed obligations 0; theorem_complete=false")
