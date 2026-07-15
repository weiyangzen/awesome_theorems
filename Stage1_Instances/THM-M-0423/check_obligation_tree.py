#!/usr/bin/env python3
"""Fail-closed structural, receipt, packet, and Lean checks for THM-M-0423."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import build_obligation_artifacts


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0423-OBLIGATION_TREE"
THEOREM = "THM-M-0423"
BASE_REVISION = "80f0191c83a1bb4026c2d490be957cf109464de1"
BASE_TREE = "b89a01cfc623bf97d1896fb3534a1ac24381fa71"
ROOT_EXPRESSION = "4b5061f2c6f01173d7cb6c9b7005ca489aaa1da1f5740e980ea477d37ae04738"
V1_DENOMINATOR = "1476e01a2281846a9ba95f86c32ccbb018134eed8dad8bbd69104b112b3a13ca"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE_HASHES = {
    "Mathlib/RingTheory/Flat/FaithfullyFlat/Algebra.lean": "6b6de1d1ddd72de049d54082e1789b99d1653c114ab373fc7de2a574d66b8adc",
    "Mathlib/LinearAlgebra/QuadraticForm/TensorProduct.lean": "602b94e9fef1b494e662d6010d6197d9cd54a71b19a27a28c8ca2cd06205b06f",
}
GRAPH_NAMES = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
ALLOWED_GRAPH_TYPES = {
    "proof": {"proof_requires", "logical_decomposition"},
    "refinement": {"expository_decomposition", "documents"},
    "provenance": {"source_map", "provenance_of"},
    "evidence": {"evidence_for"},
    "trust": {"trusts", "trusted_by"},
    "documentation": {"documents"},
    "workflow": {"workflow_depends_on"},
}
EXPECTED_PACKET_KEYS = {
    "item_id", "changed_paths", "commands", "output_summary", "base_revision",
    "known_failures", "state",
}
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0423/README.md",
    "Stage1_Instances/THM-M-0423/intake.json",
    "Stage1_Instances/THM-M-0423/source_statement_crosswalk.md",
    "Stage1_Instances/THM-M-0423/ObligationTree.lean",
    "Stage1_Instances/THM-M-0423/build_obligation_artifacts.py",
    "Stage1_Instances/THM-M-0423/check_obligation_tree.py",
    "Stage1_Instances/THM-M-0423/obligation-registry.json",
    "Stage1_Instances/THM-M-0423/typed-graphs.json",
    "Stage1_Instances/THM-M-0423/validation-specs.json",
    "Stage1_Instances/THM-M-0423/obligation-tree.md",
    "Stage1_Instances/THM-M-0423/obligation-tree-validation.md",
    "Stage1_Instances/THM-M-0423/obligation-tree-receipt.json",
}
RECEIPT_ARTIFACTS = {
    "README.md", "intake.json", "source_statement_crosswalk.md", "ObligationTree.lean",
    "build_obligation_artifacts.py", "check_obligation_tree.py", "obligation-registry.json",
    "typed-graphs.json", "validation-specs.json", "obligation-tree.md",
    "obligation-tree-validation.md",
}
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": ROOT / "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md": ROOT / "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md": ROOT / "skills/execute-stage1-rev56/SKILL.md",
    "Formalizations/Lean/lean-toolchain": LEAN_ROOT / "lean-toolchain",
    "Formalizations/Lean/lake-manifest.json": LEAN_ROOT / "lake-manifest.json",
    "Stage1_Instances/THM-M-0423/Statement.lean": HERE / "Statement.lean",
    "Stage1_Instances/THM-M-0423/statement.json": HERE / "statement.json",
    "Stage1_Instances/THM-M-0423/anchor-audit.json": HERE / "anchor-audit.json",
    "mathlib/Mathlib/RingTheory/Flat/FaithfullyFlat/Algebra.lean": MATHLIB / "Mathlib/RingTheory/Flat/FaithfullyFlat/Algebra.lean",
    "mathlib/Mathlib/LinearAlgebra/QuadraticForm/TensorProduct.lean": MATHLIB / "Mathlib/LinearAlgebra/QuadraticForm/TensorProduct.lean",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode()


def output(*argv: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(argv, cwd=cwd, text=True).strip()


def run(argv: list[str], cwd: Path, env: dict[str, str] | None = None, timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )


def assert_acyclic(edges: list[dict], edge_types: set[str], label: str) -> None:
    adjacency: dict[str, list[str]] = {}
    for item in edges:
        if item["type"] in edge_types:
            adjacency.setdefault(item["from"], []).append(item["to"])
    active: set[str] = set()
    done: set[str] = set()

    def visit(node: str) -> None:
        assert node not in active, f"{label} cycle at {node}"
        if node in done:
            return
        active.add(node)
        for child in adjacency.get(node, []):
            visit(child)
        active.remove(node)
        done.add(node)

    for node in adjacency:
        visit(node)


def strip_lean_comments(source: str) -> str:
    """Remove nested block and line comments before the proof-escape scan."""
    result: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth and source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            result.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(result)


def validate_generated_bytes() -> tuple[dict, dict, dict]:
    expected = build_obligation_artifacts.build()
    for name, value in expected.items():
        actual = (HERE / name).read_bytes()
        target = value.encode() if isinstance(value, str) else canonical_json(value)
        assert actual == target, f"stale generated artifact: {name}"
    generator = run(["python3", "-B", str(HERE / "build_obligation_artifacts.py"), "--check"], ROOT)
    assert generator.returncode == 0, generator.stdout
    return (
        expected["obligation-registry.json"],
        expected["typed-graphs.json"],
        expected["validation-specs.json"],
    )


def validate_registry(registry: dict, bundle: dict) -> tuple[list[str], set[str], set[str]]:
    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert registry["registry_id"] == bundle["registry_id"] == "THM-M-0423-OBLIGATIONS-v2"
    assert registry["registry_version"] == 2
    assert registry["item_id"] == bundle["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == THEOREM
    assert registry["root_obligation_id"] == "M0423-ROOT"
    assert registry["canonical_expression_sha256"] == ROOT_EXPRESSION
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_statement_record_sha256"] == sha256(HERE / "statement.json")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    delta = registry["append_only_delta"]
    assert len(delta) == 1
    change = delta[0]
    assert change["from_registry_id"] == "THM-M-0423-OBLIGATIONS-v1"
    assert change["from_denominator_sha256"] == V1_DENOMINATOR
    assert change["from_inventory_count"] == 40
    assert change["to_registry_id"] == registry["registry_id"]
    assert change["to_denominator_sha256"] == registry["denominator_sha256"]
    assert change["to_inventory_count"] == len(registry["obligations"])
    assert set(change["added_obligation_ids"]).isdisjoint(change["removed_obligation_ids"])
    assert change["removed_obligation_ids"] == [
        "M0423-B-DIMENSION", "M0423-B-DIM-LOW", "M0423-B-DIM-HIGH",
        "M0423-T-DIMENSION-MERGE",
    ]
    assert change["reason"] and change["status_effect"]

    fields = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    }
    rows = registry["obligations"]
    ids = [row["obligation_id"] for row in rows]
    assert len(ids) == len(set(ids))
    assert len(ids) >= 99
    for row in rows:
        assert set(row) == fields, row["obligation_id"]
        assert row["root_relevant"] is True
        assert row["kind"] in {"root", "definition", "normalization", "reduction", "branch", "construction", "bridge", "core_lemma", "computation", "certificate", "transport", "terminal"}
        assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert row["human_source_eligibility"] in {"required", "not_applicable"}
        assert row["readable_eligibility"] in {"required", "not_applicable"}
        assert row["risk_class"] in {"critical", "high", "normal", "low"}
        excluded = any(row[key] != "required" for key in ("machine_eligibility", "human_source_eligibility", "readable_eligibility"))
        assert (row["exclusion_reason"] is not None) == excluded
        if excluded:
            assert row["exclusion_reason"]["independent_approval"].startswith("pending")
    assert rows[ids.index("M0423-ROOT")]["statement_fingerprint"] == "lean-expression-sha256:" + ROOT_EXPRESSION
    denominator = build_obligation_artifacts.digest(build_obligation_artifacts.registry_projection(rows))
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"]
    frozen = registry["frozen_denominators"]
    assert frozen["inventory"] == ids
    for key, field, value in (
        ("required_machine", "machine_eligibility", "required"),
        ("required_human_source", "human_source_eligibility", "required"),
        ("required_readable", "readable_eligibility", "required"),
        ("informational_overlays", "machine_eligibility", "informational"),
    ):
        assert frozen[key] == [row["obligation_id"] for row in rows if row[field] == value]
    required = set(frozen["required_machine"])
    overlays = set(frozen["informational_overlays"])
    assert required.isdisjoint(overlays) and required | overlays == set(ids)
    metrics = registry["classification_metrics"]
    assert metrics["inventory_obligation_ids"] == ids
    assert set(metrics["required_machine_obligation_ids"]) == required
    assert metrics["accepted_machine_numerator_ids"] == []
    assert metrics["accepted_h0_numerator_ids"] == []
    assert metrics["accepted_r0_numerator_ids"] == []
    assert metrics["accepted_root_or_critical_path_ids"] == []
    metric_sets = metrics["numerator_denominator_sets"]
    assert set(metric_sets) == {"inventory_classification", "unique_logical_leaf_closure", "distinct_proof_body_closure", "interface_transport_closure", "readable_closure", "human_source_closure", "source_boundary_coverage", "root_closure"}
    assert all(isinstance(value["numerator"], list) and isinstance(value["denominator"], list) for value in metric_sets.values())
    assert metric_sets["inventory_classification"] == {"numerator": ids, "denominator": ids}
    assert all(not metric_sets[key]["numerator"] for key in metric_sets if key != "inventory_classification")
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["accepted_root_machine_debt"] == "M3"
    assert registry["audit_complete"] is False and registry["theorem_complete"] is False
    intake = load(HERE / "intake.json")
    assert intake["canonical_formal_target"]["declaration_or_expression"] == "Stage1.THM_M_0423.HasseMinkowskiStatement"
    assert intake["canonical_formal_target"]["elaborated_expression_hash"] == "sha256:" + ROOT_EXPRESSION
    assert intake["obligation_registry_hash"] == "sha256:" + denominator
    assert intake["root_vector"] == {"human": "H1", "machine": "M3", "readability": "R3"}
    assert intake["audit_complete"] is False and intake["theorem_complete"] is False
    return ids, required, overlays


def validate_nodes_and_ledgers(registry: dict, bundle: dict, ids: list[str], required: set[str]) -> tuple[dict[str, list[str]], int]:
    required_node = {
        "node_id", "obligation_id", "kind", "human_statement", "formal_target",
        "output", "human_debt", "machine_debt", "readability_debt",
        "candidate_machine_classification", "evidence_ids", "source_crosswalk_id",
        "provenance_id", "foundation_profile", "tcb_profile", "computation_record",
        "step_budget", "semantic_step_ledger", "public_readable_target",
        "validation_spec_id", "status_boundary", "task_ids", "owned_sources",
        "owner", "reviewer", "validity", "leaf_stop_record",
    }
    nodes = bundle["nodes"]
    assert len(nodes) == len(ids)
    by_id = {node["obligation_id"]: node for node in nodes}
    assert set(by_id) == set(ids)
    proof_children: dict[str, list[str]] = {}
    for item in bundle["graphs"]["proof"]["edges"]:
        if item["type"] == "proof_requires":
            proof_children.setdefault(item["from"], []).append(item["to"])
    all_steps: set[str] = set()
    ledger_count = 0
    allowed_external_premises = {"frozen-formal-context"}
    markdown = (HERE / "obligation-tree.md").read_text()
    task_nodes = set(bundle["workflow_task_nodes"])
    for oid in ids:
        node = by_id[oid]
        assert set(node) == required_node, oid
        assert node["node_id"] == THEOREM + "-" + oid.removeprefix("M0423-")
        assert node["human_debt"] in {f"H{i}" for i in range(6)}
        assert node["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert node["machine_debt"] not in {"M0-L", "M0-W", "M0-P", "M1", "M2"}, oid
        assert node["evidence_ids"] == [], oid
        assert node["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < node["step_budget"] <= 100
        assert node["owner"] and node["reviewer"]
        assert set(node["task_ids"]) <= task_nodes
        assert node["owned_sources"]
        assert all(source.startswith("Stage1_Instances/THM-M-0423/") and not source.startswith("/") for source in node["owned_sources"])
        ledger = node["semantic_step_ledger"]
        assert ledger and len(ledger) <= node["step_budget"]
        ledger_count += len(ledger)
        earlier: set[str] = set()
        obligation_premises: set[str] = set()
        for index, item in enumerate(ledger):
            assert set(item) == {"step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use"}
            assert item["step_id"] not in all_steps
            all_steps.add(item["step_id"])
            assert item["premise_ids"] and item["inference"] and item["source_locator"] and item["output"]
            assert item["inference"] != node["human_statement"]
            assert item["inference"] != node["output"]
            for premise in item["premise_ids"]:
                assert premise in set(ids) | earlier | allowed_external_premises, (oid, premise)
                if premise in ids:
                    obligation_premises.add(premise)
            expected_use = [ledger[index + 1]["step_id"]] if index + 1 < len(ledger) else (proof_parents(bundle).get(oid, []) or ["terminal-root-output"])
            assert item["outgoing_use"] == expected_use, (oid, item["outgoing_use"], expected_use)
            earlier.add(item["step_id"])
        assert ledger[-1]["output"] == node["output"], oid
        assert obligation_premises == set(proof_children.get(oid, [])), (oid, obligation_premises, proof_children.get(oid, []))
        anchor = node["public_readable_target"].split("#", 1)[1]
        assert f"### {anchor}" in markdown
        leaf = oid in required and oid not in proof_children
        assert node["leaf_stop_record"]["is_proof_leaf"] is leaf
        if leaf:
            assert node["leaf_stop_record"]["explicit_blocker"]
            assert node["leaf_stop_record"]["retry_event"]
    assert set(bundle["proof_obligation_ids"]) == required
    return proof_children, ledger_count


def proof_parents(bundle: dict) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for item in bundle["graphs"]["proof"]["edges"]:
        if item["type"] == "proof_requires":
            result.setdefault(item["to"], []).append(item["from"])
    return result


def validate_graphs(bundle: dict, ids: list[str], required: set[str], overlays: set[str], children: dict[str, list[str]]) -> int:
    assert bundle["root_node_id"] == "THM-M-0423-ROOT"
    assert set(bundle["graphs"]) == GRAPH_NAMES
    assert set(bundle["proof_obligation_ids"]) == required
    assert set(bundle["assurance_overlay_ids"]) == overlays
    all_edge_ids: set[str] = set()
    proof_by_id: dict[str, dict] = {}
    for graph_name, graph in bundle["graphs"].items():
        expected_out: dict[str, list[str]] = {}
        expected_in: dict[str, list[str]] = {}
        endpoints = set(bundle["workflow_task_nodes"]) if graph_name == "workflow" else set(ids)
        for item in graph["edges"]:
            assert item["edge_id"] not in all_edge_ids
            all_edge_ids.add(item["edge_id"])
            assert item["type"] in ALLOWED_GRAPH_TYPES[graph_name]
            assert item["from"] in endpoints and item["to"] in endpoints
            expected_out.setdefault(item["from"], []).append(item["edge_id"])
            expected_in.setdefault(item["to"], []).append(item["edge_id"])
            if graph_name == "proof":
                proof_by_id[item["edge_id"]] = item
                assert item["from"] in required and item["to"] in required
        assert graph["out"] == expected_out and graph["in"] == expected_in
    for item in proof_by_id.values():
        assert "reciprocal_edge_id" in item
        reverse = proof_by_id[item["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == item["edge_id"]
        assert reverse["from"] == item["to"] and reverse["to"] == item["from"]
        assert {item["type"], reverse["type"]} == {"proof_requires", "logical_decomposition"}
    assert_acyclic(bundle["graphs"]["proof"]["edges"], {"proof_requires"}, "proof")
    seen: set[str] = set()
    def visit(oid: str) -> None:
        if oid in seen:
            return
        seen.add(oid)
        for child in children.get(oid, []):
            visit(child)
    visit("M0423-ROOT")
    assert seen == required
    leaves = sorted(required - set(children))
    assert bundle["closure_boundary"]["executable_open_leaf_cut_set"] == leaves
    assert bundle["composition_certificates"] == []
    assert all(item["type"] != "composes" for item in bundle["graphs"]["proof"]["edges"])
    plans = bundle["unverified_decomposition_plans"]
    assert {item["parent_obligation_id"] for item in plans} == set(children)
    for item in plans:
        parent = item["parent_obligation_id"]
        assert item["planned_child_ids"] == children[parent]
        assert item["status"] == "unverified_child_to_parent_composition"
        assert item["required_future_certificate"]
    # Semantic regression gates for the v1 defects.
    assert children["M0423-T-INFINITE-MERGE"] == ["M0423-C-INFINITE-DICHOTOMY", "M0423-B-INFINITE-REAL", "M0423-B-INFINITE-COMPLEX"]
    assert children["M0423-L-INFINITE"] == ["M0423-T-INFINITE-MERGE"]
    assert set(children["M0423-T-HASSE-MERGE"]) == {"M0423-C-HASSE-DIAGONAL", "M0423-L-HASSE-PRESENTATION-MOVES", "M0423-L-DIAGONAL-PRESENTATION-CONNECTIVITY"}
    assert "M0423-L-FINITE" not in descendants(children, "M0423-C-HASSE-INVARIANT")
    assert "M0423-L-GLOBAL-CLASSIFICATION" not in descendants(children, "M0423-L-GLOBAL-UNIQUENESS")
    assert "M0423-C-GLOBAL-REALIZATION" in descendants(children, "M0423-C-ISOTROPIC-COMPARISON")
    assert "M0423-C-GLOBAL-REALIZATION" in children["M0423-T-COMPARISON-MERGE"]
    assert "M0423-C-LOCAL-RESIDUALS" in children["M0423-T-GLOBAL-CLASSIFICATION-MERGE"]
    assert "M0423-L-WITT-INJECTIVITY" in children["M0423-T-GLOBAL-UNIQUENESS-MERGE"]
    workflow = bundle["graphs"]["workflow"]["edges"]
    assert [(item["from"], item["to"]) for item in workflow] == [
        (ITEM, "S56-M-0423-ANCHOR_AUDIT"),
        ("S56-M-0423-PROOF", ITEM),
        ("S56-M-0423-VALIDATION", "S56-M-0423-PROOF"),
        ("S56-M-0423-RELEASE", "S56-M-0423-VALIDATION"),
    ]
    source_mapped = {item["from"] for item in bundle["graphs"]["provenance"]["edges"] if item["type"] == "source_map"}
    provenance_mapped = {item["to"] for item in bundle["graphs"]["provenance"]["edges"] if item["type"] == "provenance_of"}
    readable_mapped = {item["to"] for item in bundle["graphs"]["documentation"]["edges"]}
    source_required = {row["obligation_id"] for row in load(HERE / "obligation-registry.json")["obligations"] if row["human_source_eligibility"] == "required"}
    assert source_mapped == source_required - {"M0423-X-SOURCE"}
    assert "M0423-X-SOURCE" in source_required
    assert provenance_mapped == required
    assert readable_mapped == {row["obligation_id"] for row in load(HERE / "obligation-registry.json")["obligations"] if row["readable_eligibility"] == "required" and row["obligation_id"] != "M0423-X-READABLE"}
    assert next(row for row in load(HERE / "obligation-registry.json")["obligations"] if row["obligation_id"] == "M0423-X-READABLE")["readable_eligibility"] == "required"
    assert bundle["graphs"]["evidence"]["edges"] == []
    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == [] and closure["accepted_evidence_ids"] == []
    assert closure["root_machine_debt"] == "M3" and closure["root_closed"] is False
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert closure["immediate_mathematical_cut_under_assumed_valid_top_harnesses"] == ["M0423-T-LOCAL-GLOBAL"]
    assert closure["missing_composition_certificate_cut_set"] == sorted(children)
    assert "M0423-X-TRUST" in closure["release_gate_cut_set"]
    return len(all_edge_ids)


def descendants(children: dict[str, list[str]], root: str) -> set[str]:
    seen: set[str] = set()
    stack = list(children.get(root, []))
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(children.get(node, []))
    return seen


def validate_recipe(specs: dict, ids: list[str]) -> None:
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert specs["item_id"] == ITEM and specs["theorem_id"] == THEOREM
    assert len(specs["recipes"]) == 1
    recipe = specs["recipes"][0]
    assert recipe["recipe_id"] == "VAL-M0423-OBLIGATION-BUNDLE"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == ["python3", "-B", "Stage1_Instances/THM-M-0423/check_obligation_tree.py", "--worker-packet", ".stage1-worker-selftest.json"]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert 0 < recipe["timeout_seconds"] <= 300
    assert set(recipe["covered_obligation_ids"]) == set(ids)
    assert recipe["coverage_boundary"]


def validate_repository_inputs() -> None:
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(item for item in targets["targets"] if item["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 67 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    dag = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in dag["items"] if row["id"] == ITEM)
    assert item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-0423-ANCHOR_AUDIT"]
    assert item["owned_paths"] == ["Stage1_Instances/THM-M-0423"]
    prerequisite = next(row for row in dag["items"] if row["id"] == "S56-M-0423-ANCHOR_AUDIT")
    assert prerequisite["state"] == "[_]"
    assert MATHLIB.is_dir()
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    for name, expected in MATHLIB_SOURCE_HASHES.items():
        assert sha256(MATHLIB / name) == expected


def validate_lean() -> tuple[str, str]:
    source = strip_lean_comments((HERE / "ObligationTree.lean").read_text())
    prohibited = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque|implemented_by|extern|native_decide|oracle)\b")
    match = prohibited.search(source)
    assert match is None, match.group(0) if match else ""
    before = (output("git", "rev-parse", "HEAD", cwd=MATHLIB), output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB), output("git", "status", "--short", cwd=MATHLIB))
    with tempfile.TemporaryDirectory(prefix="stage1-m0423-obligation-") as raw_tmp:
        tmp = Path(raw_tmp)
        statement = tmp / "Statement.lean"
        obligation = tmp / "ObligationTree.lean"
        shutil.copy2(HERE / "Statement.lean", statement)
        shutil.copy2(HERE / "ObligationTree.lean", obligation)
        env = os.environ.copy()
        env["LEAN_NUM_THREADS"] = "1"
        lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], LEAN_ROOT, env)
        assert lean_path.returncode == 0, lean_path.stdout
        statement_result = run([
            "lake", "env", "lean", "--trust=0", "-t0", f"--root={tmp}",
            str(statement), "-o", str(tmp / "Statement.olean"),
        ], LEAN_ROOT, env)
        assert statement_result.returncode == 0, statement_result.stdout
        lean_env = env.copy()
        lean_env["LEAN_PATH"] = str(tmp) + os.pathsep + lean_path.stdout.strip()
        obligation_result = run([
            "lake", "env", "lean", "--trust=0", "-t0", f"--root={tmp}", str(obligation),
        ], LEAN_ROOT, lean_env)
        assert obligation_result.returncode == 0, obligation_result.stdout
    after = (output("git", "rev-parse", "HEAD", cwd=MATHLIB), output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB), output("git", "status", "--short", cwd=MATHLIB))
    assert before == after == (MATHLIB_REVISION, MATHLIB_TREE, "")
    statement_hash = hashlib.sha256(statement_result.stdout.encode()).hexdigest()
    assert statement_hash == ROOT_EXPRESSION
    normalized = " ".join(obligation_result.stdout.split())
    declarations = ["isotropic_after_baseChange", "global_to_local", "root_composition", "direction_package", "root_from_direction_package"]
    for name in declarations:
        full = "Stage1.THM_M_0423.ObligationTree." + name
        assert f"'{full}' depends on axioms: [propext, Classical.choice, Quot.sound]" in normalized
    assert "sorryAx" not in obligation_result.stdout
    return statement_hash, hashlib.sha256(obligation_result.stdout.encode()).hexdigest()


def validate_receipt(registry: dict, bundle: dict, edge_count: int, ledger_count: int, statement_hash: str, lean_hash: str) -> dict:
    receipt = load(HERE / "obligation-tree-receipt.json")
    assert receipt["schema_version"] == "stage1-worker-obligation-tree-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "obligation_tree"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False and receipt["accepted"] is False
    assert receipt["accepted_receipt_ids"] == [] and receipt["accepted_closed_obligations"] == []
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    patch = subprocess.check_output([
        "git", "diff", "--binary", "--",
        "Stage1_Instances/THM-M-0423/README.md",
        "Stage1_Instances/THM-M-0423/intake.json",
        "Stage1_Instances/THM-M-0423/source_statement_crosswalk.md",
    ], cwd=ROOT)
    assert receipt["repository_dirty_state"]["tracked_patch_sha256"] == "sha256:" + hashlib.sha256(patch).hexdigest()
    assert receipt["registry_id"] == registry["registry_id"]
    assert receipt["registry_version"] == 2
    assert receipt["registry_denominator_sha256"] == registry["denominator_sha256"]
    assert receipt["obligation_count"] == len(registry["obligations"])
    assert receipt["typed_edge_count"] == edge_count
    assert receipt["substantive_ledger_step_count"] == ledger_count
    assert receipt["composition_certificate_count"] == 0
    assert receipt["unverified_decomposition_plan_count"] == len(bundle["unverified_decomposition_plans"])
    assert receipt["executable_open_leaf_count"] == len(bundle["closure_boundary"]["executable_open_leaf_cut_set"])
    assert set(receipt["graph_names"]) == GRAPH_NAMES
    assert receipt["canonical_statement_fingerprint"] == "lean-expression-sha256:" + ROOT_EXPRESSION
    assert receipt["statement_output_sha256"] == statement_hash
    assert receipt["lean_output_sha256"] == lean_hash
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert set(receipt["changed_paths"]) == EXPECTED_CHANGED_PATHS
    assert set(receipt["artifact_hashes"]) == RECEIPT_ARTIFACTS
    for name, expected in receipt["artifact_hashes"].items():
        assert expected == "sha256:" + sha256(HERE / name), name
    assert set(receipt["source_inputs"]) == set(SOURCE_INPUTS)
    for name, path in SOURCE_INPUTS.items():
        assert receipt["source_inputs"][name] == "sha256:" + sha256(path), name
    assert receipt["cut_sets"] == bundle["closure_boundary"] | {"executable_open_leaf_count": len(bundle["closure_boundary"]["executable_open_leaf_cut_set"])}
    assert receipt["commands"] and all(command["exit_code"] == 0 for command in receipt["commands"])
    assert receipt["status_boundary"] and receipt["known_failures"]
    return receipt


def validate_worker_packet(path: Path, receipt: dict) -> dict:
    assert path.is_file(), f"missing worker packet: {path}"
    packet = load(path)
    assert set(packet) == EXPECTED_PACKET_KEYS
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == EXPECTED_CHANGED_PATHS
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"])
    assert isinstance(packet["commands"], list) and packet["commands"]
    for command in packet["commands"]:
        assert set(command) == {"cwd", "argv", "exit_code", "output_summary"}
        assert command["cwd"] == "."
        assert isinstance(command["argv"], list) and all(isinstance(item, str) and item for item in command["argv"])
        assert command["exit_code"] == 0 and command["output_summary"]
    assert packet["commands"][:-1] == receipt["commands"]
    assert all(command["argv"] != ["python3", "-B", "Stage1_Instances/THM-M-0423/check_obligation_tree.py", "--worker-packet", ".stage1-worker-selftest.json"] for command in receipt["commands"])
    final_command = packet["commands"][-1]
    assert final_command["argv"] == ["python3", "-B", "Stage1_Instances/THM-M-0423/check_obligation_tree.py", "--worker-packet", ".stage1-worker-selftest.json"]
    assert final_command["exit_code"] == 0
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert any("master acceptance" in item for item in packet["known_failures"])
    status = output("git", "status", "--porcelain=v1", "--untracked-files=all")
    observed: set[str] = set()
    outside: set[str] = set()
    for line in status.splitlines():
        path_text = line[3:] if line.startswith("?? ") else line[2:].lstrip()
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        if path_text == "Formalizations/Lean/.lake":
            continue
        if path_text == ".stage1-worker-selftest.json" or path_text.startswith("Stage1_Instances/THM-M-0423/"):
            observed.add(path_text)
        else:
            outside.add(path_text)
    assert outside == set(), outside
    assert observed == EXPECTED_CHANGED_PATHS, (observed, EXPECTED_CHANGED_PATHS)
    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    assert MATHLIB.resolve().is_dir()
    return packet


def expect_failure(callback, label: str) -> None:
    try:
        callback()
    except (AssertionError, KeyError, TypeError, ValueError, OSError):
        return
    raise AssertionError(f"negative fixture did not fail: {label}")


def validate_negative_fixtures(registry: dict, bundle: dict) -> None:
    bad = copy.deepcopy(registry)
    bad["denominator_sha256"] = "0" * 64
    expect_failure(lambda: assert_denominator(bad), "corrupt denominator")
    bad_bundle = copy.deepcopy(bundle)
    edge = bad_bundle["graphs"]["proof"]["edges"][0]
    edge["reciprocal_edge_id"] = "missing"
    expect_failure(lambda: assert_reciprocity(bad_bundle), "broken reciprocal")
    node = copy.deepcopy(bundle["nodes"][0])
    node["machine_debt"] = "M0-L"
    expect_failure(lambda: assert_evidence_status(node), "M0 without E0")
    node = copy.deepcopy(bundle["nodes"][0])
    node["semantic_step_ledger"][0]["premise_ids"] = ["undefined-premise"]
    expect_failure(lambda: assert_ledger_refs(node, set(row["obligation_id"] for row in registry["obligations"])), "undefined ledger premise")
    certificate = {"parent_statement_fingerprint": "planned:v2:sha256:" + "0" * 64}
    expect_failure(lambda: assert_certificate_fingerprint(certificate), "planned composition fingerprint")
    cycle_edges = [
        {"from": "a", "to": "b", "type": "proof_requires"},
        {"from": "b", "to": "a", "type": "proof_requires"},
    ]
    expect_failure(lambda: assert_acyclic(cycle_edges, {"proof_requires"}, "fixture"), "proof cycle")
    closure = copy.deepcopy(bundle["closure_boundary"])
    closure["theorem_complete"] = True
    expect_failure(lambda: assert_open_closure(closure), "false closure")
    count = len(registry["obligations"])
    stale_doc = (HERE / "obligation-tree.md").read_text().replace(f"Registry version 2 freezes {count}", f"Registry version 2 freezes {count - 1}", 1)
    expect_failure(lambda: assert_doc_projection(stale_doc, registry), "stale document count")
    missing = ROOT / ".definitely-missing-worker-packet.json"
    expect_failure(lambda: load(missing), "missing worker packet")
    assert_metric_metamorphism(registry, bundle)


def assert_denominator(registry: dict) -> None:
    assert registry["denominator_sha256"] == build_obligation_artifacts.digest(build_obligation_artifacts.registry_projection(registry["obligations"]))


def assert_reciprocity(bundle: dict) -> None:
    by_id = {item["edge_id"]: item for item in bundle["graphs"]["proof"]["edges"]}
    for item in by_id.values():
        reverse = by_id[item["reciprocal_edge_id"]]
        assert reverse["reciprocal_edge_id"] == item["edge_id"]


def assert_evidence_status(node: dict) -> None:
    assert not node["machine_debt"].startswith("M0") or node["evidence_ids"]


def assert_ledger_refs(node: dict, ids: set[str]) -> None:
    earlier: set[str] = set()
    for item in node["semantic_step_ledger"]:
        assert all(premise in ids | earlier | {"frozen-formal-context"} for premise in item["premise_ids"])
        earlier.add(item["step_id"])


def assert_certificate_fingerprint(certificate: dict) -> None:
    assert certificate["parent_statement_fingerprint"].startswith("lean-expression-sha256:")


def assert_open_closure(closure: dict) -> None:
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["theorem_complete"] is False


def assert_doc_projection(document: str, registry: dict) -> None:
    assert f"Registry version 2 freezes {len(registry['obligations'])}" in document
    assert registry["denominator_sha256"] in document


def assert_metric_metamorphism(registry: dict, bundle: dict) -> None:
    metrics = registry["classification_metrics"]
    baseline = (
        tuple(metrics["numerator_denominator_sets"]["unique_logical_leaf_closure"]["denominator"]),
        tuple(metrics["numerator_denominator_sets"]["distinct_proof_body_closure"]["denominator"]),
        tuple(bundle["closure_boundary"]["remaining_root_cut_set"]),
        tuple(metrics["accepted_root_or_critical_path_ids"]),
    )
    cloned_evidence = copy.deepcopy(bundle)
    cloned_evidence["graphs"]["evidence"]["edges"].append({
        "edge_id": "FIXTURE-ALIAS-EVIDENCE", "from": "M0423-X-PROVENANCE",
        "type": "evidence_for", "to": "M0423-ROOT",
    })
    observed = (
        tuple(metrics["numerator_denominator_sets"]["unique_logical_leaf_closure"]["denominator"]),
        tuple(metrics["numerator_denominator_sets"]["distinct_proof_body_closure"]["denominator"]),
        tuple(cloned_evidence["closure_boundary"]["remaining_root_cut_set"]),
        tuple(metrics["accepted_root_or_critical_path_ids"]),
    )
    assert observed == baseline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path, required=True)
    args = parser.parse_args()
    validate_repository_inputs()
    registry, bundle, specs = validate_generated_bytes()
    ids, required, overlays = validate_registry(registry, bundle)
    children, ledger_count = validate_nodes_and_ledgers(registry, bundle, ids, required)
    edge_count = validate_graphs(bundle, ids, required, overlays, children)
    validate_recipe(specs, ids)
    statement_hash, lean_hash = validate_lean()
    receipt = validate_receipt(registry, bundle, edge_count, ledger_count, statement_hash, lean_hash)
    validate_worker_packet(args.worker_packet, receipt)
    validate_negative_fixtures(registry, bundle)
    print(f"PASS THM-M-0423 obligation tree: {len(ids)} obligations, {edge_count} typed edges, {ledger_count} ledger steps")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")
    print(f"statement output sha256: {statement_hash}")
    print(f"obligation Lean output sha256: {lean_hash}")
    print(f"open executable leaves: {len(bundle['closure_boundary']['executable_open_leaf_cut_set'])}; missing composition certificates: {len(children)}")
    print("accepted closures: 0; root H1/M3/R3; audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
