#!/usr/bin/env python3
"""Fail-closed validation for the THM-M-0110 obligation-tree freeze."""

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
ITEM = "S56-M-0110-OBLIGATION_TREE"
THEOREM = "THM-M-0110"
ROOT_ID = "M0110-ROOT"
BASE_REVISION = "6bf9ee93a322e7d25cf9249226222095f95d1cff"
BASE_TREE = "24acf86e69ab2e6fca9480c6269b6429874ba295"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_EXPRESSION = "d0a9a0e873dd388aa37c0bcc77fce1fc38bae5911851a87570b94f50c80eecc6"
GRAPH_SHA256 = "73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca"
CONTEXT_SHA256 = "4f60e4c0e01ec4cc069fbe1a7601aabdc8f2acf1df3e4c917e09e4235cec640b"
SHARED_GROUP = "SHARED-MODULE-735a79718fe89f59"
GRAPH_NAMES = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
REGISTRY_FIELDS = {
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
}
NODE_FIELDS = {
    "node_id", "obligation_id", "kind", "human_statement", "formal_target",
    "output", "human_debt", "machine_debt", "readability_debt", "evidence_ids",
    "source_crosswalk_id", "provenance_id", "foundation_profile", "tcb_profile",
    "computation_record", "step_budget", "semantic_step_ledger",
    "public_readable_target", "validation_spec_id", "status_boundary", "task_ids",
    "owned_sources", "owner", "reviewer", "validity",
}
RECIPE_FIELDS = {
    "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
    "network_policy", "expected_exit", "expected_outputs", "covered_obligation_ids",
    "covered_declarations", "coverage_semantics", "closure_credit",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def check_acyclic(edges: list[dict]) -> None:
    children: dict[str, list[str]] = {}
    for edge in edges:
        children.setdefault(edge["from"], []).append(edge["to"])
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


def lean_check() -> tuple[str, str]:
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    assert sha(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"

    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    fixed_env = os.environ | {
        "LEAN_PATH": lean_path, "LC_ALL": "C", "LANG": "C", "TZ": "UTC", "NO_COLOR": "1",
    }
    with tempfile.TemporaryDirectory(prefix="thm-m-0110-obligation-") as temporary:
        temp = Path(temporary)
        statement = subprocess.run(
            [lean_exe, "Statement.lean", "-o", str(temp / "Statement.olean")],
            cwd=HERE, env=fixed_env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=180, check=False,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        obligation = subprocess.run(
            [lean_exe, "ObligationTree.lean"], cwd=HERE,
            env=fixed_env | {"LEAN_PATH": str(temp) + os.pathsep + lean_path},
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=180, check=False,
        )
        if obligation.returncode:
            sys.stdout.write(obligation.stdout)
            raise SystemExit(obligation.returncode)

    normalized = re.sub(r"\s+", " ", obligation.stdout)
    for declaration in (
        "NativeSemanticTransportPackage", "KodairaVanishingArgumentPackage",
        "KodairaVanishingTarget", "checkedRootAssembly", "root_of_packages",
    ):
        assert declaration in obligation.stdout, declaration
    assert normalized.count("depends on axioms: [propext, Classical.choice, Quot.sound]") == 2
    assert "sorryAx" not in obligation.stdout
    combined = statement.stdout + obligation.stdout
    return hashlib.sha256(combined.encode()).hexdigest(), combined


def validate_dependency_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    assert ledger == {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM,
        "observed_theorem_dag_sha256": GRAPH_SHA256,
        "dependency_context_sha256": CONTEXT_SHA256,
        "repository_revision": BASE_REVISION,
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [SHARED_GROUP],
        "inspections": [],
        "reuse_decisions": ledger["reuse_decisions"],
        "unresolved_compatibility_obligations": [],
    }
    assert sha(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256
    assert len(ledger["reuse_decisions"]) == 1
    decision = ledger["reuse_decisions"][0]
    assert set(decision) == {"source_id", "provider_theorem_id", "decision", "non_reuse_reason", "context_digest"}
    assert decision["source_id"] == SHARED_GROUP
    assert decision["provider_theorem_id"] == "THM-M-0118"
    assert decision["decision"] == "not_applicable"
    assert decision["context_digest"] == CONTEXT_SHA256
    assert "weak co-mention" in decision["non_reuse_reason"]
    graph = load(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json")
    group = next(value for value in graph["shared_lemma_groups"] if value["group_id"] == SHARED_GROUP)
    assert group["member_theorem_ids"] == [THEOREM, "THM-M-0118"]
    assert group["blocking"] is False and group["confidence"] == "hint"


def main() -> None:
    registry = load(HERE / "obligation-registry.json")
    bundle = load(HERE / "typed-graphs.json")
    specs = load(HERE / "validation-specs.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    receipt_path = HERE / "obligation-tree-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None

    module_spec = importlib.util.spec_from_file_location(
        "m0110_obligation_builder", HERE / "build_obligation_artifacts.py"
    )
    assert module_spec is not None and module_spec.loader is not None
    builder = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(builder)
    expected_registry, expected_bundle, expected_specs = builder.build()
    assert registry == expected_registry
    assert bundle == expected_bundle
    assert specs == expected_specs

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert specs["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
    assert registry["frozen_against_statement_record_sha256"] == sha(HERE / "statement.json")
    assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == ROOT_EXPRESSION
    assert anchor["audited_target"]["elaborated_expression_sha256"] == ROOT_EXPRESSION
    assert anchor["root_decision"]["classification_after_proposed"] == "M3"

    layers = registry["mandatory_layer_analysis"]
    assert set(layers) == {"S", "N", "B", "C", "L", "X", "T", "not_applicable_layers"}
    assert layers["not_applicable_layers"] == []
    assert all(layers[name] for name in ("S", "N", "B", "C", "L", "X", "T"))

    obligations = registry["obligations"]
    ids = [value["obligation_id"] for value in obligations]
    id_set = set(ids)
    assert len(ids) == len(id_set) == len(builder.ROWS) == 23
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    projection = [{key: value[key] for key in builder.REGISTRY_FIELDS} for value in obligations]
    denominator = builder.digest(projection)
    assert denominator == registry["denominator_sha256"] == bundle["registry_denominator_sha256"] == specs["registry_denominator_sha256"]
    for value in obligations:
        assert set(value) == REGISTRY_FIELDS
        assert value["root_relevant"] is True
        assert value["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert value["human_source_eligibility"] in {"required", "not_applicable"}
        assert value["readable_eligibility"] in {"required", "not_applicable"}
        assert value["risk_class"] in {"critical", "high", "normal", "low"}
        if any(value[key] != "required" for key in ("machine_eligibility", "human_source_eligibility", "readable_eligibility")):
            assert value["exclusion_reason"].endswith("pending_independent_approval")
        else:
            assert value["exclusion_reason"] is None
    frozen = registry["frozen_denominators"]
    assert frozen["inventory"] == ids
    assert frozen["required_machine"] == [value["obligation_id"] for value in obligations if value["machine_eligibility"] == "required"]
    assert frozen["required_human_source"] == [value["obligation_id"] for value in obligations if value["human_source_eligibility"] == "required"]
    assert frozen["required_readable"] == [value["obligation_id"] for value in obligations if value["readable_eligibility"] == "required"]
    assert registry["append_only_delta"] == [] and registry["registry_version"] == 1
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

    nodes = bundle["nodes"]
    assert len(nodes) == len(ids)
    assert {value["obligation_id"] for value in nodes} == id_set
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8") if (HERE / "obligation-tree.md").exists() else ""
    all_step_ids: set[str] = set()
    for value in nodes:
        assert set(value) == NODE_FIELDS
        assert value["node_id"] == value["obligation_id"]
        assert value["human_debt"] in {f"H{index}" for index in range(6)}
        assert value["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert value["readability_debt"] in {f"R{index}" for index in range(5)}
        assert 0 < value["step_budget"] <= 100
        ledger = value["semantic_step_ledger"]
        assert set(ledger) == {"premises", "inference", "output", "outgoing_use", "steps"}
        assert value["step_budget"] == len(ledger["steps"])
        for step in ledger["steps"]:
            assert set(step) == {"step_id", "premise_ids", "inference_or_source", "exact_output", "outgoing_use_ids"}
            assert step["step_id"] not in all_step_ids
            assert step["premise_ids"] and step["inference_or_source"] and step["exact_output"] and step["outgoing_use_ids"]
            all_step_ids.add(step["step_id"])
        assert value["public_readable_target"].startswith("Stage1_Instances/THM-M-0110/obligation-tree.md#")
        if readable:
            anchor_name = value["public_readable_target"].split("#", 1)[1]
            assert f'<a id="{anchor_name}"></a>' in readable
        assert value["owner"] and value["reviewer"] and value["validity"]["review_due"]
    by_id = {value["obligation_id"]: value for value in nodes}
    assert by_id[ROOT_ID]["machine_debt"] == "M3" and by_id[ROOT_ID]["readability_debt"] == "R3"
    assert all(value["evidence_ids"] == [] for value in nodes)

    assert bundle["root_node_id"] == ROOT_ID and set(bundle["graphs"]) == GRAPH_NAMES
    all_edge_ids: set[str] = set()
    for graph in bundle["graphs"].values():
        assert set(graph["out"]) == set(graph["in"]) == id_set
        directional = []
        for value in graph["edges"]:
            assert value["edge_id"] not in all_edge_ids
            assert value["type"] in ALLOWED_EDGES
            assert value["from"] in id_set and value["to"] in id_set
            assert value["edge_id"] in graph["out"][value["from"]]
            assert value["edge_id"] in graph["in"][value["to"]]
            all_edge_ids.add(value["edge_id"])
            if value["type"] != "composes":
                directional.append(value)
        check_acyclic(directional)
    assert len(all_edge_ids) == 56

    proof = {value["edge_id"]: value for value in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    for value in proof.values():
        reciprocal = proof[value["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == value["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (value["to"], value["from"])
        assert {value["type"], reciprocal["type"]} == {"proof_requires", "composes"}
        if value["type"] == "proof_requires":
            children.setdefault(value["from"], []).append(value["to"])
    reachable: set[str] = set()

    def reach(identifier: str) -> None:
        if identifier in reachable:
            return
        reachable.add(identifier)
        for child in children.get(identifier, []):
            reach(child)

    reach(ROOT_ID)
    assert reachable == {ROOT_ID, "M0110-T-ASSEMBLE", "M0110-S-SEMANTIC", "M0110-T-VANISHING"}
    certificates = bundle["composition_certificates"]
    assert {value["parent_obligation_id"] for value in certificates} == {ROOT_ID, "M0110-T-ASSEMBLE"}
    assert all(value["state"] == "kernel_checked_conditional_provisional" for value in certificates)

    workflow = bundle["workflow_task_graph"]
    task_ids = {value["task_id"] for value in workflow["nodes"]}
    assert task_ids == {"S56-M-0110-INTAKE", "S56-M-0110-STATEMENT", "S56-M-0110-ANCHOR_AUDIT", ITEM, "S56-M-0110-PROOF", "S56-M-0110-VALIDATION", "S56-M-0110-RELEASE"}
    assert all(value["task_id"] in task_ids and value["obligation_id"] in id_set for value in workflow["task_obligation_links"])

    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert closure["authoritative_root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert closure["minimal_open_proof_cut_set"] == ["M0110-S-SEMANTIC", "M0110-T-VANISHING"]

    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {value["recipe_id"] for value in recipes} == {value["validation_spec_id"] for value in nodes}
    covered = []
    for value in recipes:
        assert set(value) == RECIPE_FIELDS
        assert value["cwd"] == "." and value["argv"] == ["python3", "-B", "Stage1_Instances/THM-M-0110/check_obligation_tree.py"]
        assert value["network_policy"] == "denied" and value["expected_exit"] == 0
        assert len(value["covered_obligation_ids"]) == 1 and value["closure_credit"] is False
        covered.extend(value["covered_obligation_ids"])
    assert covered == ids

    validate_dependency_ledger()
    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque|implemented_by|native_decide|extern)\b")
    assert not forbidden.search(without_comments(source))
    for marker in ("import Statement", "structure NativeSemanticTransportPackage", "def KodairaVanishingArgumentPackage", "def RootAssemblyPackage", "theorem checkedRootAssembly", "theorem root_of_packages", "#print axioms root_of_packages"):
        assert marker in source, marker
    lean_output_sha, _lean_output = lean_check()

    if receipt is not None:
        assert receipt["schema_version"] == "stage1-worker-obligation-tree-receipt/1.0"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["inventory_count"] == len(ids) and receipt["typed_edge_count"] == len(all_edge_ids)
        assert receipt["semantic_ledger_step_count"] == len(all_step_ids)
        assert receipt["validation"]["lean_output_sha256"] == lean_output_sha
        assert receipt["dependency_reuse_ledger"]["sha256"] == sha(HERE / "dependency-reuse-ledger.json")
        for name, expected_sha in receipt["artifact_sha256"].items():
            assert expected_sha == sha(HERE / name), name
        assert receipt["accepted_closed_obligations"] == []
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R3"}
        assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
        if packet is not None:
            assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
            assert packet["item_id"] == ITEM and packet["state"] == "[_]"
            assert packet["base_revision"] == BASE_REVISION
            assert packet["known_failures"] == receipt["known_failures"]
            assert packet["changed_paths"] == receipt["changed_paths"]
            status = output("git", "status", "--short", "--untracked-files=all").splitlines()
            actual_changes = {line[2:].lstrip() for line in status}
            actual_changes.discard("Formalizations/Lean/.lake")
            assert actual_changes == set(packet["changed_paths"])

    print(f"PASS THM-M-0110 obligation tree: {len(ids)} obligations, {len(all_edge_ids)} typed edges")
    print(f"registry denominator sha256: {denominator}")
    print(f"lean output sha256: {lean_output_sha}")
    print("dependency closure: 0 hard parents, 0 hints, 1 weak shared group rejected for reuse")
    print("root closure: open (H1/M3/R3); semantic transport, Kodaira proof, and assurance gates remain")


if __name__ == "__main__":
    main()
