#!/usr/bin/env python3
"""Fail-closed validation of the THM-M-1356 obligation freeze."""

from __future__ import annotations

import hashlib
import importlib.util
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
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1356-OBLIGATION_TREE"
THEOREM = "THM-M-1356"
ROOT_ID = "M1356-ROOT"
BASE_REVISION = "431e77db6367a2eda83060b7212cb490d11ca39f"
BASE_TREE = "7ed0ffdf78a9b7a5d8d474b30aca0d8809c1d087"
STATEMENT_SHA256 = "f8d0588db753f9411bcaa440bec1ab853d08682896c194841d0b35f6a8ef5e7e"
ANCHOR_SHA256 = "dacd7c30b6e1d3e9ee06569ecdc46c8a4d7904dd99f4c5aaaafb56310468f8a1"
EXPRESSION_SHA256 = "7901eb74686f457348ec06812b8584c69eb09649779637cbb28b2e7bd84b98bf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
GRAPH_NAMES = {
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"
}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def check_acyclic(edges: list[dict]) -> None:
    children: dict[str, list[str]] = {}
    for value in edges:
        children.setdefault(value["from"], []).append(value["to"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        assert node not in visiting, f"cycle through {node}"
        if node in visited:
            return
        visiting.add(node)
        for child in children.get(node, []):
            visit(child)
        visiting.remove(node)
        visited.add(node)

    for node in children:
        visit(node)


def validate_lean() -> tuple[str, str]:
    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-1356-obligation-") as temp_dir:
        temp = Path(temp_dir)
        statement = subprocess.run(
            [lean_exe, "-o", str(temp / "Statement.olean"), "Statement.lean"],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        obligation = subprocess.run(
            [lean_exe, "ObligationTree.lean"],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": str(temp) + os.pathsep + lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
        )
        if obligation.returncode:
            sys.stdout.write(obligation.stdout)
            raise SystemExit(obligation.returncode)
    return statement.stdout, obligation.stdout


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    recipes = load("validation-specs.json")
    receipt = load("obligation-tree-receipt.json")
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8")) if packet_path.exists() else None

    module_spec = importlib.util.spec_from_file_location(
        "m1356_obligation_builder", HERE / "build_obligation_artifacts.py"
    )
    assert module_spec is not None and module_spec.loader is not None
    builder = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(builder)
    expected_registry, expected_bundle, expected_recipes, expected_markdown = builder.build()
    assert registry == expected_registry
    assert bundle == expected_bundle
    assert recipes == expected_recipes
    assert (HERE / "obligation-tree.md").read_text(encoding="utf-8") == expected_markdown

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert recipes["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == recipes["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == recipes["theorem_id"] == THEOREM
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["registry_denominator_sha256"] == registry["denominator_sha256"]
    assert receipt["inventory_count"] == len(registry["obligations"])
    assert receipt["typed_edge_count"] == sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    assert receipt["semantic_ledger_step_count"] == sum(len(node["semantic_step_ledger"]) for node in bundle["nodes"])
    assert receipt["accepted_closed_obligations"] == []
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert len(receipt["validation"]["commands"]) >= 13
    assert all(command["exit_code"] in {0, 1} for command in receipt["validation"]["commands"])
    assert "Pending" not in receipt["validation"]["output_summary"]
    if packet is not None:
        assert packet["item_id"] == ITEM and packet["theorem_id"] == THEOREM
        assert packet["state"] == "[_]" and packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["accepted_receipt_ids"] == []
        assert packet["audit_complete"] is packet["theorem_complete"] is False
        assert packet["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    validation_text = (HERE / "obligation-tree-validation.md").read_text(encoding="utf-8")
    for marker in (
        "50 unique obligations", "335", "122 structured ledger entries",
        "[H1, M3, R4]", "No obligation is accepted closed",
    ):
        assert marker in validation_text
    assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean") == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json") == ANCHOR_SHA256
    statement_record = load("statement.json")
    assert statement_record["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    layers = registry["mandatory_layer_analysis"]
    assert set(layers) == {"S", "N", "B", "C", "L", "X", "T", "not_applicable_layers"}
    assert layers["not_applicable_layers"] == []
    assert all(layers[name] for name in ("S", "N", "B", "C", "L", "X", "T"))

    registry_fields = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    }
    obligations = registry["obligations"]
    ids = [value["obligation_id"] for value in obligations]
    id_set = set(ids)
    assert len(ids) == len(id_set) == 50
    assert ids[0] == registry["root_obligation_id"] == bundle["root_node_id"] == ROOT_ID
    projection = [{key: value[key] for key in builder.DENOMINATOR_FIELDS} for value in obligations]
    denominator = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert denominator == registry["denominator_sha256"]
    assert denominator == bundle["registry_denominator_sha256"]
    assert denominator == recipes["registry_denominator_sha256"]
    assert registry["append_only_delta"] == [] and registry["registry_version"] == 1
    for value in obligations:
        assert set(value) == registry_fields
        assert value["root_relevant"] is True
        assert value["kind"] in {
            "root", "definition", "normalization", "reduction", "branch", "construction",
            "bridge", "core_lemma", "lemma", "computation", "certificate", "transport", "terminal",
        }
        assert value["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert value["human_source_eligibility"] in {"required", "not_applicable"}
        assert value["readable_eligibility"] in {"required", "not_applicable"}
        assert value["risk_class"] in {"critical", "high", "normal", "low"}
        assert value["terminal_proof_body_id"] is None
        if value["machine_eligibility"] != "required":
            assert value["exclusion_reason"] and value["exclusion_reason"].endswith("pending_independent_approval")
    frozen = registry["frozen_denominators"]
    assert frozen["inventory"] == ids
    assert frozen["required_machine"] == [
        value["obligation_id"] for value in obligations if value["machine_eligibility"] == "required"
    ]
    assert frozen["required_human_source"] == [
        value["obligation_id"] for value in obligations if value["human_source_eligibility"] == "required"
    ]
    assert frozen["required_readable"] == ids
    assert frozen["informational_overlays"] == [
        "M1356-X-PROVENANCE", "M1356-X-TRUST", "M1356-X-READABLE", "M1356-X-WORKFLOW"
    ]
    observed = registry["status_observed_after_freeze"]
    assert observed["accepted_closed_obligations"] == []
    assert observed["authoritative_root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}

    required_node_fields = {
        "node_id", "obligation_id", "kind", "human_statement", "formal_target", "output",
        "human_debt", "machine_debt", "readability_debt", "evidence_ids",
        "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
        "computation_record", "step_budget", "semantic_step_ledger", "public_readable_target",
        "validation_spec_id", "status_boundary", "task_ids", "owned_sources", "owner",
        "reviewer", "validity",
    }
    nodes = bundle["nodes"]
    assert len(nodes) == len(ids)
    assert {value["obligation_id"] for value in nodes} == id_set
    assert len({value["node_id"] for value in nodes}) == len(nodes)
    step_ids: set[str] = set()
    markdown = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    for value in nodes:
        assert set(value) == required_node_fields
        assert value["kind"] in {
            "root", "definition", "normalization", "reduction", "branch", "construction",
            "bridge", "core_lemma", "computation", "certificate", "transport", "terminal",
        }
        assert value["human_debt"] in {f"H{index}" for index in range(6)}
        assert value["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert value["readability_debt"] in {f"R{index}" for index in range(5)}
        assert 0 < value["step_budget"] <= 100
        assert value["semantic_step_ledger"]
        for step in value["semantic_step_ledger"]:
            assert set(step) == {
                "step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use"
            }
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"]
            assert step["output"] and step["outgoing_use"]
            step_ids.add(step["step_id"])
        assert value["public_readable_target"].startswith(
            f"Stage1_Instances/{THEOREM}/obligation-tree.md#"
        )
        anchor = value["public_readable_target"].split("#", 1)[1]
        assert f'<a id="{anchor}"></a>' in markdown
        assert value["owner"] and value["reviewer"] and value["validity"]["review_due"]
        assert not value["evidence_ids"]

    assert set(bundle["graphs"]) == GRAPH_NAMES
    all_edge_ids: set[str] = set()
    workflow_ids = set(bundle["workflow_task_nodes"])
    for name, graph in bundle["graphs"].items():
        endpoints = workflow_ids if name == "workflow" else id_set
        directional = []
        for value in graph["edges"]:
            assert value["edge_id"] not in all_edge_ids
            assert value["type"] in ALLOWED_EDGES
            assert value["from"] in endpoints and value["to"] in endpoints
            assert value["edge_id"] in graph["out"].get(value["from"], [])
            assert value["edge_id"] in graph["in"].get(value["to"], [])
            all_edge_ids.add(value["edge_id"])
            if not (name == "proof" and value["type"] in {"composes", "logical_decomposition"}):
                directional.append(value)
        check_acyclic(directional)
    assert len(all_edge_ids) == 335

    proof = {value["edge_id"]: value for value in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    composes = []
    for value in proof.values():
        reciprocal = proof[value["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == value["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (value["to"], value["from"])
        assert {value["type"], reciprocal["type"]} in (
            {"proof_requires", "composes"}, {"proof_requires", "logical_decomposition"}
        )
        if value["type"] == "proof_requires":
            children.setdefault(value["from"], []).append(value["to"])
        if value["type"] == "composes":
            composes.append(value)
    assert {(value["from"], value["to"]) for value in composes} == {
        ("M1356-T-ASSEMBLE", "M1356-ROOT"),
        ("M1356-B-STABLE-TO-MINORS", "M1356-T-ASSEMBLE"),
        ("M1356-B-MINORS-TO-STABLE", "M1356-T-ASSEMBLE"),
    }
    reachable: set[str] = set()

    def reach(identifier: str) -> None:
        if identifier in reachable:
            return
        reachable.add(identifier)
        for child in children.get(identifier, []):
            reach(child)

    reach(ROOT_ID)
    proof_overlays = {
        "M1356-S-STATEMENT", "M1356-S-COEFFICIENT", "M1356-S-BOUNDARIES",
        "M1356-S-FOUNDATION", "M1356-X-SOURCE", "M1356-X-PROVENANCE", "M1356-X-TRUST",
        "M1356-X-READABLE", "M1356-X-WORKFLOW",
    }
    assert reachable == id_set - proof_overlays
    assert {value["parent_obligation_id"] for value in bundle["composition_certificates"]} == {
        "M1356-ROOT", "M1356-T-ASSEMBLE"
    }
    assert len(bundle["unverified_decomposition_plans"]) == 31

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["authoritative_root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert boundary["minimal_open_proof_cut_set"] == [
        "M1356-B-STABLE-TO-MINORS", "M1356-B-MINORS-TO-STABLE"
    ]

    required_recipe_fields = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations",
    }
    recipe_rows = recipes["recipes"]
    assert len(recipe_rows) == len(ids)
    assert {value["validation_spec_id"] for value in nodes} == {value["recipe_id"] for value in recipe_rows}
    for value in recipe_rows:
        assert set(value) == required_recipe_fields
        assert value["cwd"] == "."
        assert value["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"]
        assert set(value["env_allowlist"]) == {"PATH", "HOME", "TMPDIR", "PYTHONDONTWRITEBYTECODE"}
        assert value["timeout_seconds"] == 180 and value["network_policy"] == "denied"
        assert value["expected_exit"] == 0 and len(value["covered_obligation_ids"]) == 1
        assert value["covered_obligation_ids"][0] in id_set

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    assert sha(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert not re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b",
        without_comments,
    )
    for marker in (
        "import Statement", "def StableToPositiveMinorsTarget",
        "def PositiveMinorsToStableTarget", "def DirectionPackage",
        "theorem directionPackage_of_directions", "theorem root_of_directionPackage",
        "theorem root_of_directions", "directions.1 n hn a ha", "directions.2 n hn a ha",
        "#print axioms root_of_directions",
    ):
        assert marker in source, marker

    statement_stdout, obligation_stdout = validate_lean()
    assert "RouthHurwitzTarget : Prop" in statement_stdout
    for declaration in (
        "directionPackage_of_directions", "root_of_directionPackage", "root_of_directions"
    ):
        marker = f"'Stage1Instances.THM_M_1356.ObligationTree.{declaration}' depends on axioms: [propext,"
        assert marker in obligation_stdout
    assert obligation_stdout.count("Classical.choice") == 3
    assert obligation_stdout.count("Quot.sound") == 3

    print(f"PASS THM-M-1356 obligation tree: {len(ids)} obligations, {len(all_edge_ids)} typed edges, {len(step_ids)} ledger steps")
    print(f"registry denominator sha256: {denominator}")
    print("Lean composition: exact two-direction conditional harness; axioms [propext, Classical.choice, Quot.sound]")
    print("root closure: open (H1/M3/R4); no accepted proof body or theorem completion")


if __name__ == "__main__":
    main()
