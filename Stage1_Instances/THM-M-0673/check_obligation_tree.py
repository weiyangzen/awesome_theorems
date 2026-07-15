#!/usr/bin/env python3
"""Fail-closed validation of the THM-M-0673 obligation freeze."""

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
ITEM = "S56-M-0673-OBLIGATION_TREE"
THEOREM = "THM-M-0673"
ROOT_ID = "M0673-ROOT"
BASE_REVISION = "f3b9f5fc99b4675558801fcc47f610b046eb5d14"
BASE_TREE = "5a074129aa628a1d735fc06a68164a056f1d62be"
STATEMENT_SHA256 = "131cab45507a3d3c7249d02f52f8cfbaf9d7b1c004a542e24f1bdb36be9ca424"
ANCHOR_SHA256 = "81b0bdc3e507f19efa0c51f0aee86de4d2d31e0360c5b8454dc76e4e4e4e3350"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
GRAPH_NAMES = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on", "refines",
}
TEXT_ARTIFACTS = {
    "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
    "obligation-registry.json", "typed-graphs.json", "validation-specs.json",
    "obligation-tree.md", "obligation-tree-validation.md", "obligation-tree-receipt.json",
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


def exact_index(graph: dict, endpoints: set[str]) -> None:
    expected_out = {identifier: [] for identifier in endpoints}
    expected_in = {identifier: [] for identifier in endpoints}
    for value in graph["edges"]:
        expected_out[value["from"]].append(value["edge_id"])
        expected_in[value["to"]].append(value["edge_id"])
    assert graph["out"] == expected_out
    assert graph["in"] == expected_in


def reachable(edges: list[dict], root: str) -> set[str]:
    outgoing: dict[str, list[str]] = {}
    for value in edges:
        outgoing.setdefault(value["from"], []).append(value["to"])
    seen: set[str] = set()
    todo = [root]
    while todo:
        current = todo.pop()
        if current in seen:
            continue
        seen.add(current)
        todo.extend(outgoing.get(current, []))
    return seen


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', source)


def check_text(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}"
    assert not any(line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def run_lean() -> str:
    lean = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    env = {**os.environ, "LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"}
    with tempfile.TemporaryDirectory(prefix="m0673-obligation-") as temp:
        temp_path = Path(temp)
        statement = subprocess.run(
            [lean, "-o", str(temp_path / "Statement.olean"),
             "Statement.lean"],
            cwd=HERE, env={**env, "LEAN_PATH": lean_path}, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=180, check=False,
        )
        assert statement.returncode == 0, statement.stdout
        assert (temp_path / "Statement.olean").is_file()
        env["LEAN_PATH"] = str(temp_path) + os.pathsep + lean_path
        result = subprocess.run(
            [lean, "--trust=0", "../../Stage1_Instances/THM-M-0673/ObligationTree.lean"],
            cwd=LEAN_ROOT, env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=180, check=False,
        )
        assert result.returncode == 0, result.stdout
        return result.stdout


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    receipt = load("obligation-tree-receipt.json") if (HERE / "obligation-tree-receipt.json").exists() else None

    module_spec = importlib.util.spec_from_file_location(
        "m0673_obligation_builder", HERE / "build_obligation_artifacts.py",
    )
    assert module_spec is not None and module_spec.loader is not None
    builder = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(builder)
    expected_registry, expected_bundle, expected_specs = builder.build()
    assert registry == expected_registry
    assert bundle == expected_bundle
    assert specs == expected_specs

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["lifecycle_mode"] == bundle["lifecycle_mode"] == specs["lifecycle_mode"] == "executing"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean") == STATEMENT_SHA256
    assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json") == ANCHOR_SHA256
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    manifest = json.loads((ROOT / "Docs" / "Stage1_Targets_rev-5.6.json").read_text())
    target = next(value for value in manifest["targets"] if value["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 717
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    execution = json.loads((ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json").read_text())
    item = next(value for value in execution["items"] if value["id"] == ITEM)
    predecessor = next(value for value in execution["items"] if value["id"] == "S56-M-0673-ANCHOR_AUDIT")
    assert item["phase"] == "obligation_tree" and item["layer"] == 3 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0673-ANCHOR_AUDIT"]
    assert predecessor["state"] == "[_]"
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    instance = load("instance.json")
    assert instance["lifecycle"] == "planned"
    assert instance["obligation_registry_hash"] == "sha256:" + registry["registry_sha256"]
    assert instance["obligation_registry"]["denominator_sha256"] == registry["denominator_sha256"]
    assert instance["obligation_registry"]["accepted_closed_obligations"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    task_dag = load("task-dag.json")
    local_task = next(value for value in task_dag["tasks"] if value["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["provisional_evidence_ids"] == ["S56-M-0673-OBLIGATION-TREE-WORKER-20260715"]
    assert task_dag["accepted_states"] == []

    registry_fields = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    }
    obligations = registry["obligations"]
    ids = [value["obligation_id"] for value in obligations]
    id_set = set(ids)
    assert len(ids) == len(id_set) == 28
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    projection = [{key: value[key] for key in registry["canonical_projection_fields"]}
                  for value in obligations]
    denominator = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    ).hexdigest()
    assert denominator == registry["denominator_sha256"]
    assert denominator == bundle["registry_denominator_sha256"] == specs["registry_denominator_sha256"]
    registry_scope = {
        key: value for key, value in registry.items()
        if key not in {"status_observed_after_freeze", "status_boundary", "registry_sha256"}
    }
    assert builder.digest(registry_scope) == registry["registry_sha256"]
    assert registry["registry_sha256"] == bundle["registry_sha256"] == specs["registry_sha256"]
    assert registry["append_only_delta"] == [] and registry["registry_version"] == 1
    for value in obligations:
        assert set(value) == registry_fields
        assert value["kind"] in {"root", "definition", "reduction", "branch", "construction", "lemma", "computation", "transport", "terminal"}
        assert value["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert value["human_source_eligibility"] in {"required", "not_applicable"}
        assert value["readable_eligibility"] in {"required", "not_applicable"}
        assert value["risk_class"] in {"critical", "high", "normal", "low"}
        excluded = value["machine_eligibility"] != "required" or value["human_source_eligibility"] != "required"
        if excluded:
            assert set(value["exclusion_reason"]) == {"code", "justification", "approval"}
            assert value["exclusion_reason"]["approval"].startswith("pending independent")
        else:
            assert value["exclusion_reason"] is None
    frozen = registry["frozen_denominators"]
    assert frozen["inventory"] == ids
    assert frozen["required_machine"] == [value["obligation_id"] for value in obligations if value["machine_eligibility"] == "required"]
    assert frozen["required_human_source"] == [value["obligation_id"] for value in obligations if value["human_source_eligibility"] == "required"]
    assert frozen["required_readable"] == ids
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"
    layers = registry["mandatory_layer_analysis"]
    assert set(layers) == {"S", "N", "B", "C", "L", "X", "T", "not_applicable_layers"}
    assert all(layers[name] for name in ("S", "B", "C", "L", "X", "T"))
    assert layers["N"] == [] and layers["not_applicable_layers"]

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
    markdown = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    step_ids: set[str] = set()
    for value in nodes:
        assert set(value) == required_node_fields
        assert value["human_debt"] in {f"H{index}" for index in range(6)}
        assert value["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert value["readability_debt"] in {f"R{index}" for index in range(5)}
        if value["obligation_id"] in builder.REQUIRES:
            assert value["step_budget"] == "split-required"
        else:
            assert isinstance(value["step_budget"], int) and 0 < value["step_budget"] <= 100
        assert value["semantic_step_ledger"]
        for step in value["semantic_step_ledger"]:
            assert set(step) == {"step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use", "status"}
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"]
            assert step["output"] and step["outgoing_use"]
            assert step["status"] in {"checked_interface", "planned_substantive_not_proof_accepted"}
            step_ids.add(step["step_id"])
        anchor = value["public_readable_target"].split("#", 1)[1]
        assert f'<a id="{anchor}"></a>' in markdown
        assert value["validation_spec_id"] == f"VAL-{value['obligation_id']}"
        assert value["owner"] and value["reviewer"] and value["validity"]["review_due"]

    assert set(bundle["graphs"]) == GRAPH_NAMES
    edge_ids: set[str] = set()
    allowed_cycles = {"proof", "refinement"}
    for name, graph in bundle["graphs"].items():
        exact_index(graph, id_set)
        for value in graph["edges"]:
            assert value["edge_id"] not in edge_ids
            edge_ids.add(value["edge_id"])
            assert value["from"] in id_set and value["to"] in id_set
            assert value["type"] in ALLOWED_EDGES
        if name not in allowed_cycles:
            check_acyclic(graph["edges"])
    proof_by_id = {value["edge_id"]: value for value in bundle["graphs"]["proof"]["edges"]}
    for value in proof_by_id.values():
        reciprocal = proof_by_id[value["reciprocal_edge_id"]]
        assert reciprocal["from"] == value["to"] and reciprocal["to"] == value["from"]
        assert {value["type"], reciprocal["type"]} == {"proof_requires", "composes"}
    requires_only = [value for value in proof_by_id.values() if value["type"] == "proof_requires"]
    check_acyclic(requires_only)
    refinement_by_id = {value["edge_id"]: value for value in bundle["graphs"]["refinement"]["edges"]}
    for value in refinement_by_id.values():
        if "reciprocal_edge_id" not in value:
            assert value["type"] == "expository_decomposition"
            continue
        reciprocal = refinement_by_id[value["reciprocal_edge_id"]]
        assert reciprocal["from"] == value["to"] and reciprocal["to"] == value["from"]
        assert reciprocal["reciprocal_edge_id"] == value["edge_id"]
        assert {value["type"], reciprocal["type"]} in (
            {"logical_decomposition", "refines"}, {"equivalent_to"},
        )
    logical_only = [value for value in refinement_by_id.values()
                    if value["type"] == "logical_decomposition"]
    check_acyclic(logical_only)
    machine_required = set(frozen["required_machine"])
    assert machine_required <= reachable(requires_only + logical_only, ROOT_ID)
    assert bundle["closure_boundary"]["accepted_closed_obligations"] == []
    assert bundle["closure_boundary"]["root_machine_debt"] == "M3"
    assert bundle["closure_boundary"]["root_closed"] is False
    assert bundle["closure_boundary"]["audit_complete"] is False
    assert bundle["closure_boundary"]["theorem_complete"] is False
    checked_parents = {value["parent_obligation_id"] for value in bundle["composition_certificates"]}
    assert checked_parents == set(builder.CHECKED_COMPOSITIONS)
    for value in bundle["unverified_decomposition_plans"]:
        assert value["parent_obligation_id"] not in checked_parents
        assert value["status"] == "typed_plan_requires_proof_phase_composition_certificate"

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {value["recipe_id"] for value in recipes} == {f"VAL-{identifier}" for identifier in ids}
    for value in recipes:
        assert isinstance(value["argv"], list) and value["argv"]
        assert value["network_policy"] == "denied" and value["expected_exit"] == 0
        assert value["timeout_seconds"] == 180
        assert set(value["covered_obligation_ids"]) <= id_set

    lean_source = without_comments((HERE / "ObligationTree.lean").read_text(encoding="utf-8"))
    prohibited = [r"\bsorry\b", r"\badmit\b", r"\baxiom\b", r"\bunsafe\b", r"sorryAx"]
    for pattern in prohibited:
        assert re.search(pattern, lean_source) is None, f"prohibited Lean token {pattern}"
    assert "FirstOrder.Language.Ultraproduct.sentence_realize phi" not in lean_source
    assert "FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast phi" not in lean_source
    lean_output = run_lean()
    for name in ("formula_of_bounded", "sentence_of_formula", "terminal_of_sentence", "root_of_terminal", "root_of_bounded"):
        assert name in lean_output
    assert "sorryAx" not in lean_output
    assert "depends on axioms:" in lean_output

    if receipt is not None:
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["registry_sha256"] == registry["registry_sha256"]
        assert receipt["obligation_count"] == len(ids)
        assert receipt["typed_edge_count"] == len(edge_ids)
        assert receipt["accepted"] is False and receipt["theorem_complete"] is False
        assert receipt["accepted_closed_obligation_ids"] == []
        for name, expected in receipt["source_hashes"].items():
            if name in {"statement_expression", "obligation-tree-receipt.json"}:
                continue
            assert sha(HERE / name) == expected, name

    for name in TEXT_ARTIFACTS:
        path = HERE / name
        if path.exists():
            check_text(path)

    print(f"PASS THM-M-0673 obligation tree: {len(ids)} obligations, {len(edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print(f"registry scope sha256: {registry['registry_sha256']}")
    print("conditional interfaces elaborated at --trust=0; accepted root remains H1/M3/R4")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, subprocess.SubprocessError, OSError, ValueError) as error:
        print(f"FAIL THM-M-0673 obligation tree: {error}", file=sys.stderr)
        raise
