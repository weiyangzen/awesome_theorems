#!/usr/bin/env python3
"""Fail-closed validation of the THM-M-0861 obligation freeze."""

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
ITEM = "S56-M-0861-OBLIGATION_TREE"
THEOREM = "THM-M-0861"
ROOT_ID = "M0861-ROOT"
BASE_REVISION = "b243ebc0f9058ba5afafef8240b92c2dfb2edc6e"
BASE_TREE = "b4b092069141ac54ea1ab5a6ea946192a30ec78c"
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


def main() -> None:
    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    specs = load("validation-specs.json")
    receipt_path = HERE / "obligation-tree-receipt.json"
    receipt = load("obligation-tree-receipt.json") if receipt_path.exists() else None

    module_spec = importlib.util.spec_from_file_location(
        "m0861_obligation_builder", HERE / "build_obligation_artifacts.py"
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
    assert registry["item_id"] == bundle["item_id"] == specs["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == specs["theorem_id"] == THEOREM
    assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
    assert registry["frozen_against_statement_sha256"] == "a6ce9ee3edd720d38fa9306324e38b48d5f0430a8b9513b9207e7808ea1b380d"
    assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
    assert registry["append_only_delta"] == [] and registry["registry_version"] == 1
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
    assert len(ids) == len(id_set) == 54
    assert ids[0] == registry["root_obligation_id"] == ROOT_ID
    projection = [{key: value[key] for key in registry_fields} for value in obligations]
    denominator = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert denominator == registry["denominator_sha256"]
    assert denominator == bundle["registry_denominator_sha256"]
    assert denominator == specs["registry_denominator_sha256"]
    for value in obligations:
        assert set(value) == registry_fields
        assert value["root_relevant"] is True
        assert value["kind"] in {
            "root", "definition", "reduction", "branch", "construction", "lemma",
            "computation", "transport", "terminal",
        }
        assert value["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert value["human_source_eligibility"] in {"required", "not_applicable"}
        assert value["readable_eligibility"] in {"required", "not_applicable"}
        assert value["risk_class"] in {"critical", "high", "normal", "low"}
        if value["machine_eligibility"] != "required" or value["human_source_eligibility"] != "required":
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
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    assert registry["status_observed_after_freeze"]["authoritative_root_machine_debt"] == "M4"

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
    node_by_id = {value["obligation_id"]: value for value in nodes}
    step_ids: set[str] = set()
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
        assert f'<a id="{anchor}"></a>' in (HERE / "obligation-tree.md").read_text(encoding="utf-8")
        assert value["owner"] and value["reviewer"] and value["validity"]["review_due"]
    assert node_by_id[ROOT_ID]["machine_debt"] == "M4"
    assert node_by_id[ROOT_ID]["readability_debt"] == "R4"
    assert all(not value["evidence_ids"] for value in nodes)

    assert bundle["root_node_id"] == ROOT_ID
    assert set(bundle["graphs"]) == GRAPH_NAMES
    all_edge_ids: set[str] = set()
    workflow_ids = set(bundle["workflow_task_nodes"])
    for name, graph in bundle["graphs"].items():
        endpoints = workflow_ids if name == "workflow" else id_set
        assert set(graph["out"]) == set(graph["in"]) == endpoints
        directional = []
        for value in graph["edges"]:
            assert value["edge_id"] not in all_edge_ids
            assert value["type"] in ALLOWED_EDGES
            assert value["from"] in endpoints and value["to"] in endpoints
            assert value["edge_id"] in graph["out"][value["from"]]
            assert value["edge_id"] in graph["in"][value["to"]]
            all_edge_ids.add(value["edge_id"])
            if value["type"] not in {"composes", "logical_decomposition"} or name != "proof":
                directional.append(value)
        check_acyclic(directional)
    assert len(all_edge_ids) == 244
    assert bundle["graphs"]["evidence"]["edges"] == []

    proof = {value["edge_id"]: value for value in bundle["graphs"]["proof"]["edges"]}
    children: dict[str, list[str]] = {}
    composes = []
    for value in proof.values():
        reciprocal = proof[value["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == value["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (value["to"], value["from"])
        assert value["type"] == "proof_requires" or reciprocal["type"] == "proof_requires"
        assert {value["type"], reciprocal["type"]} in (
            {"proof_requires", "composes"}, {"proof_requires", "logical_decomposition"}
        )
        if value["type"] == "proof_requires":
            children.setdefault(value["from"], []).append(value["to"])
        if value["type"] == "composes":
            composes.append(value)
    assert {(value["from"], value["to"]) for value in composes} == {
        ("M0861-S-TRANSPORT", ROOT_ID),
        ("M0861-T-ASSEMBLE", ROOT_ID),
        ("M0861-T-UPPER", "M0861-T-ASSEMBLE"),
        ("M0861-T-LOWER", "M0861-T-ASSEMBLE"),
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
        "M0861-S-TARGET", "M0861-S-REPRESENTATION", "M0861-S-COLORING",
        "M0861-S-BIPARTITE", "M0861-S-BOUNDARY", "M0861-S-FOUNDATION",
        "M0861-N-BOUNDED", "M0861-X-SOURCE", "M0861-X-PROVENANCE",
        "M0861-X-TRUST", "M0861-X-READABLE", "M0861-X-WORKFLOW",
    }
    assert reachable == id_set - proof_overlays
    assert len(bundle["unverified_decomposition_plans"]) == 61
    assert {value["parent_obligation_id"] for value in bundle["composition_certificates"]} == {
        ROOT_ID, "M0861-T-ASSEMBLE"
    }

    boundary = bundle["closure_boundary"]
    assert boundary["accepted_closed_obligations"] == []
    assert boundary["root_closed"] is boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["authoritative_root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert boundary["minimal_open_proof_cut_set"] == ["M0861-T-UPPER", "M0861-T-LOWER"]

    required_recipe_fields = {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations",
    }
    recipes = specs["recipes"]
    assert len(recipes) == len(ids)
    assert {value["validation_spec_id"] for value in nodes} == {value["recipe_id"] for value in recipes}
    for value in recipes:
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
        "import Statement", "def DegreeBound", "def BoundedSatzCTarget",
        "def UpperBoundTarget", "def LowerBoundTarget",
        "def RootTransportTarget", "def AssemblyTarget", "theorem assembly_of_upper_and_lower",
        "theorem expanded_of_assembly",
        "theorem checked_root_transport", "theorem root_of_assembly", "theorem root_of_upper_and_lower",
        "assembly.1 G vertexFinite edgeFinite hBipartite",
        "assembly.2 G vertexFinite edgeFinite hBipartite", "#print axioms root_of_upper_and_lower",
    ):
        assert marker in source, marker

    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    base_lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0861-obligation-") as temp_dir:
        statement = subprocess.run(
            [lean_exe, "Statement.lean", "-o", str(Path(temp_dir) / "Statement.olean")],
            cwd=HERE,
            env=os.environ | {"LEAN_PATH": base_lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        lean = subprocess.run(
            ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM}/ObligationTree.lean"],
            cwd=LEAN_ROOT,
            env=os.environ | {"LEAN_PATH": temp_dir + ":" + base_lean_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
        )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized_lean = re.sub(r"\s+", " ", lean.stdout)
    assert normalized_lean.count("depends on axioms: [propext, Classical.choice, Quot.sound]") == 5
    for declaration in (
        "DegreeBound", "BoundedSatzCTarget", "UpperBoundTarget", "LowerBoundTarget",
        "RootTransportTarget", "AssemblyTarget", "assembly_of_upper_and_lower",
        "expanded_of_assembly", "checked_root_transport", "root_of_assembly",
        "root_of_upper_and_lower",
    ):
        assert declaration in lean.stdout
    lean_output_hash = hashlib.sha256(lean.stdout.encode()).hexdigest()

    if receipt is not None:
        assert receipt["schema_version"] == "stage1-obligation-tree-receipt/1.0"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["registry_denominator_sha256"] == denominator
        assert receipt["obligation_count"] == len(ids)
        assert receipt["typed_edge_count"] == len(all_edge_ids)
        assert receipt["semantic_ledger_step_count"] == len(step_ids)
        assert receipt["unverified_decomposition_count"] == len(bundle["unverified_decomposition_plans"])
        assert receipt["lean_output_sha256"] == lean_output_hash
        assert receipt["accepted_closed_obligations"] == []
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M4", "R": "R4"}
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["audit_complete"] is receipt["theorem_complete"] is False
        packet = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]

    print(
        f"PASS {THEOREM} obligation tree: {len(ids)} obligations, "
        f"{len(all_edge_ids)} typed edges, {len(step_ids)} structured ledger steps, "
        f"{len(bundle['unverified_decomposition_plans'])} unverified decompositions"
    )
    print(f"registry denominator sha256: {denominator}")
    print(f"Lean conditional composition stdout sha256: {lean_output_hash}")
    print("root closure: open (H1/M4/R4); accepted_closed_obligations=0; theorem_complete=false")


if __name__ == "__main__":
    main()
