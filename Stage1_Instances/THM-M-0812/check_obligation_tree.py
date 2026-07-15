#!/usr/bin/env python3
"""Validate the frozen THM-M-0812 obligation architecture and Lean harness."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("check_obligation_tree requires Python assertions (__debug__) enabled")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0812-OBLIGATION_TREE"
THEOREM = "THM-M-0812"
BASE_REVISION = "6bf9ee93a322e7d25cf9249226222095f95d1cff"
BASE_TREE = "24acf86e69ab2e6fca9480c6269b6429874ba295"
GRAPH_SHA256 = "73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca"
CONTEXT_SHA256 = "bc99f9e70a837e425f01f88835dda207b07138301527ae3715e6640b0998be7d"
ROOT_EXPRESSION = "b20dc7426179377f6838e3ca384aaa80431d00713953494a5ea789d84ec1d7b4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
GRAPH_NAMES = {"proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow"}
ALLOWED_EDGES = {
    "proof_requires", "composes", "logical_decomposition", "source_map",
    "expository_decomposition", "equivalent_to", "transports", "evidence_for",
    "provenance_of", "documents", "trusts", "workflow_depends_on",
}
PHASES = {"intake", "statement", "anchor_audit", "obligation_tree", "proof", "validation", "release"}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def check_text(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}"
    assert not any(line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {path}"


def check_acyclic(edges: list[dict]) -> None:
    next_nodes: dict[str, list[str]] = {}
    for edge in edges:
        next_nodes.setdefault(edge["from"], []).append(edge["to"])
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        assert node not in visiting, f"cycle through {node}"
        if node in visited:
            return
        visiting.add(node)
        for child in next_nodes.get(node, []):
            visit(child)
        visiting.remove(node)
        visited.add(node)

    for node in next_nodes:
        visit(node)


def load_builder():
    spec = importlib.util.spec_from_file_location("m0812_obligation_builder", HERE / "build_obligation_artifacts.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_dependency_ledger(ledger: dict) -> None:
    assert ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1"
    assert ledger["consumer_theorem_id"] == THEOREM
    assert ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256
    assert ledger["dependency_context_sha256"] == CONTEXT_SHA256
    assert ledger["repository_revision"] == BASE_REVISION
    assert ledger["direct_parent_ids"] == []
    assert ledger["transitive_ancestor_ids"] == []
    assert ledger["hard_edge_ids"] == []
    assert ledger["reuse_hint_ids"] == []
    assert ledger["inspections"] == []
    assert ledger["unresolved_compatibility_obligations"] == []
    groups = {
        "SHARED-MODULE-4750110eb957192c",
        "SHARED-MODULE-5c210052f4f43681",
        "SHARED-MODULE-5c70331f5abc6907",
        "SHARED-MODULE-9a0c699601b049af",
        "SHARED-MODULE-a17e8b8222361802",
    }
    assert set(ledger["shared_group_ids"]) == groups
    decisions = ledger["reuse_decisions"]
    assert len(decisions) == len(groups)
    assert {row["source_id"] for row in decisions} == groups
    for row in decisions:
        assert row["decision"] == "not_applicable"
        assert row["provider_theorem_id"] != THEOREM
        assert row["non_reuse_reason"]
        assert row["context_digest"] == CONTEXT_SHA256
        assert set(row["observed_phase_states"]) == PHASES
        for relative, digest in row["inspected_artifacts"].items():
            assert relative.startswith(f"Stage1_Instances/{row['provider_theorem_id']}/")
            assert sha(ROOT / relative) == digest


def run_lean() -> subprocess.CompletedProcess[str]:
    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    base_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    env = os.environ.copy()
    env.update({"LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"})
    with tempfile.TemporaryDirectory(prefix="thm-m-0812-obligation-") as temp:
        statement_env = env | {"LEAN_PATH": base_path}
        statement = subprocess.run(
            [lean_exe, "Statement.lean", "-o", str(Path(temp) / "Statement.olean")],
            cwd=HERE,
            env=statement_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        return subprocess.run(
            ["lake", "env", "lean", f"../../Stage1_Instances/{THEOREM}/ObligationTree.lean"],
            cwd=LEAN_ROOT,
            env=env | {"LEAN_PATH": temp + ":" + base_path},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path, default=ROOT / ".stage1-worker-selftest.json")
    parser.add_argument("--skip-receipt", action="store_true")
    args = parser.parse_args()

    registry = load("obligation-registry.json")
    bundle = load("typed-graphs.json")
    validation = load("validation-specs.json")
    ledger = load("dependency-reuse-ledger.json")
    builder = load_builder()
    expected_registry, expected_bundle, expected_validation, expected_readable = builder.build()
    assert registry == expected_registry
    assert bundle == expected_bundle
    assert validation == expected_validation
    assert (HERE / "obligation-tree.md").read_text(encoding="utf-8") == expected_readable

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert sha(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256
    validate_dependency_ledger(ledger)

    assert registry["schema_version"] == "stage1-obligation-registry/1.0"
    assert bundle["schema_version"] == "stage1-typed-graphs/1.0"
    assert validation["schema_version"] == "stage1-validation-specs/1.0"
    assert registry["item_id"] == bundle["item_id"] == validation["item_id"] == ITEM
    assert registry["theorem_id"] == bundle["theorem_id"] == validation["theorem_id"] == THEOREM
    assert registry["registry_version"] == 1 and registry["append_only_delta"] == []
    assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
    assert registry["frozen_against_dependency_context_sha256"] == CONTEXT_SHA256

    obligations = registry["obligations"]
    ids = [row["obligation_id"] for row in obligations]
    id_set = set(ids)
    assert len(ids) == len(id_set) == 40
    assert ids[0] == registry["root_obligation_id"] == "M0812-ROOT"
    registry_fields = {
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    }
    projection = [{key: row[key] for key in builder.REGISTRY_FIELDS} for row in obligations]
    assert hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == registry["denominator_sha256"]
    assert bundle["registry_denominator_sha256"] == validation["registry_denominator_sha256"] == registry["denominator_sha256"]
    for row in obligations:
        assert set(row) == registry_fields
        assert row["root_relevant"] is True
        assert re.fullmatch(r"(?:lean-expression-sha256|architecture:v1:sha256):[0-9a-f]{64}", row["statement_fingerprint"])
        assert row["kind"] in {"root", "definition", "reduction", "branch", "construction", "lemma", "computation", "transport", "terminal", "certificate", "normalization"}
        assert row["machine_eligibility"] in {"required", "not_applicable", "informational"}
        assert row["human_source_eligibility"] in {"required", "not_applicable"}
        assert row["readable_eligibility"] == "required"
        if row["machine_eligibility"] != "required" or row["human_source_eligibility"] != "required":
            assert row["exclusion_reason"] and row["exclusion_reason"].endswith("pending_independent_approval")
    frozen = registry["frozen_denominators"]
    assert frozen["inventory"] == ids
    assert frozen["required_machine"] == [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"]
    assert frozen["required_human_source"] == [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"]
    assert frozen["required_readable"] == ids
    assert set(registry["mandatory_layer_analysis"]) == {
        "S_statement_foundation", "N_normalization", "B_branch", "C_construction",
        "L_core_lemma", "X_external_computation", "T_terminal",
    }
    assert all(row["state"] == "required" and row["obligation_ids"] for row in registry["mandatory_layer_analysis"].values())
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []

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
    assert {row["obligation_id"] for row in nodes} == id_set
    assert len({row["node_id"] for row in nodes}) == len(nodes)
    readable = (HERE / "obligation-tree.md").read_text(encoding="utf-8")
    step_ids = set()
    for row in nodes:
        assert set(row) == required_node_fields
        assert row["human_debt"] in {f"H{i}" for i in range(6)}
        assert row["machine_debt"] in {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
        assert row["readability_debt"] in {f"R{i}" for i in range(5)}
        assert 0 < row["step_budget"] <= 100
        assert row["semantic_step_ledger"]
        for step in row["semantic_step_ledger"]:
            assert set(step) == {"step_id", "premise_ids", "inference", "source_locator", "output", "outgoing_use"}
            assert step["step_id"] not in step_ids
            assert step["premise_ids"] and step["inference"] and step["source_locator"] and step["output"] and step["outgoing_use"]
            step_ids.add(step["step_id"])
        anchor = row["public_readable_target"].split("#", 1)[1]
        assert f'<a id="{anchor}"></a>' in readable
        assert row["reviewer"] and row["validity"]["review_due"]
        assert row["evidence_ids"] == []

    assert bundle["root_node_id"] == "M0812-ROOT"
    assert set(bundle["graphs"]) == GRAPH_NAMES
    all_edges = set()
    for name, graph in bundle["graphs"].items():
        endpoints = set(bundle["workflow_task_nodes"]) if name == "workflow" else id_set
        assert set(graph["out"]) == set(graph["in"]) == endpoints
        directional = []
        for edge in graph["edges"]:
            assert edge["edge_id"] not in all_edges
            assert edge["type"] in ALLOWED_EDGES
            assert edge["from"] in endpoints and edge["to"] in endpoints
            assert edge["edge_id"] in graph["out"][edge["from"]]
            assert edge["edge_id"] in graph["in"][edge["to"]]
            all_edges.add(edge["edge_id"])
            if name != "proof" or edge["type"] == "proof_requires":
                directional.append(edge)
        check_acyclic(directional)
    assert len(all_edges) == 204
    assert bundle["graphs"]["evidence"]["edges"] == []

    proof = {edge["edge_id"]: edge for edge in bundle["graphs"]["proof"]["edges"]}
    for edge in proof.values():
        reciprocal = proof[edge["reciprocal_edge_id"]]
        assert reciprocal["reciprocal_edge_id"] == edge["edge_id"]
        assert (reciprocal["from"], reciprocal["to"]) == (edge["to"], edge["from"])
        assert {edge["type"], reciprocal["type"]} in ({"proof_requires", "composes"}, {"proof_requires", "logical_decomposition"})
    compose_pairs = {(e["from"], e["to"]) for e in proof.values() if e["type"] == "composes"}
    assert compose_pairs == {
        ("M0812-T-ASSEMBLE", "M0812-ROOT"),
        ("M0812-T-MATCHING-ATTAIN", "M0812-T-ASSEMBLE"),
        ("M0812-T-COVER-FROM-MAX", "M0812-T-ASSEMBLE"),
        ("M0812-T-WEAK-DUALITY", "M0812-T-ASSEMBLE"),
    }
    assert len(bundle["unverified_decomposition_plans"]) == 34
    assert {row["parent_obligation_id"] for row in bundle["composition_certificates"]} == {"M0812-ROOT", "M0812-T-ASSEMBLE"}
    closure = bundle["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["authoritative_root_vector"] == {"H": "H1", "M": "M3", "R": "R2"}
    assert closure["minimal_open_proof_cut_set"] == ["M0812-T-MATCHING-ATTAIN", "M0812-T-COVER-FROM-MAX", "M0812-T-WEAK-DUALITY"]

    recipes = validation["recipes"]
    assert len(recipes) == len(ids)
    assert {row["validation_spec_id"] for row in nodes} == {row["recipe_id"] for row in recipes}
    for row in recipes:
        assert set(row) == {"recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy", "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations"}
        assert row["cwd"] == "."
        assert row["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"]
        assert row["timeout_seconds"] == 180 and row["network_policy"] == "denied" and row["expected_exit"] == 0
        assert len(row["covered_obligation_ids"]) == 1 and row["covered_obligation_ids"][0] in id_set

    target_manifest = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
    target = next(row for row in target_manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1371 and target["baseline"] == "L0" and target["rework_required"] is True
    execution = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0812-ANCHOR_AUDIT")
    assert item["state"] == "[ ]" and item["phase"] == "obligation_tree" and item["layer"] == 3
    assert item["depends_on"] == [predecessor["id"]] and predecessor["state"] == "[_]"

    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    assert sha(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"

    source = (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    stripped = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    stripped = re.sub(r"--.*", "", stripped)
    stripped = re.sub(r'"(?:\\.|[^"\\])*"', '""', stripped)
    stripped = re.sub(r"^#print axioms .*?$", "", stripped, flags=re.MULTILINE)
    assert not re.search(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe|implemented_by|native_decide|extern)\b", stripped)
    for marker in (
        "import Statement", "def MatchingAttainmentTarget", "def MaximumMatchingCoverTarget",
        "def WeakDualityTarget", "def AssemblyTarget", "theorem assembly_of_construction_and_duality",
        "theorem root_of_assembly", "theorem root_of_construction_and_duality",
        "assembly.1 left right", "assembly.2.1 left right", "assembly.2.2 left right",
        "#print axioms root_of_construction_and_duality",
    ):
        assert marker in source, marker
    lean = run_lean()
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    for declaration in ("MatchingAttainmentTarget", "MaximumMatchingCoverTarget", "WeakDualityTarget", "AssemblyTarget", "assembly_of_construction_and_duality", "root_of_assembly", "root_of_construction_and_duality"):
        assert declaration in lean.stdout
    assert normalized.count("depends on axioms: [propext, Classical.choice, Quot.sound]") == 3
    assert "sorryAx" not in lean.stdout
    lean_hash = hashlib.sha256(lean.stdout.encode()).hexdigest()

    if not args.skip_receipt:
        receipt = load("obligation-tree-receipt.json")
        assert receipt["schema_version"] == "stage1-obligation-tree-receipt/1.0"
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM and receipt["phase"] == "obligation_tree"
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["registry_denominator_sha256"] == registry["denominator_sha256"]
        assert receipt["obligation_count"] == len(ids) and receipt["typed_edge_count"] == len(all_edges)
        assert receipt["semantic_ledger_step_count"] == len(step_ids)
        assert receipt["unverified_decomposition_count"] == len(bundle["unverified_decomposition_plans"])
        assert receipt["lean_output_sha256"] == lean_hash
        assert receipt["accepted_closed_obligations"] == []
        assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R2"}
        assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
        assert receipt["audit_complete"] is receipt["theorem_complete"] is False
        packet = json.loads(args.worker_packet.read_text(encoding="utf-8"))
        assert set(packet) == {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}
        assert packet["item_id"] == ITEM and packet["state"] == "[_]" and packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]

    for name in (
        "ObligationTree.lean", "build_obligation_artifacts.py", "check_obligation_tree.py",
        "dependency-reuse-ledger.json", "obligation-registry.json", "typed-graphs.json",
        "validation-specs.json", "obligation-tree.md",
    ):
        check_text(HERE / name)
    ast.parse((HERE / "build_obligation_artifacts.py").read_text(encoding="utf-8"))
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    print(
        f"PASS {THEOREM} obligation tree: {len(ids)} obligations, {len(all_edges)} typed edges, "
        f"{len(step_ids)} substantive ledgers, {len(bundle['unverified_decomposition_plans'])} open decompositions"
    )
    print(f"registry denominator sha256: {registry['denominator_sha256']}")
    print(f"Lean conditional composition stdout sha256: {lean_hash}")
    print("dependency closure: 0 hard ancestors; 5 weak shared groups inspected; 0 results reused")
    print("root closure: open (H1/M3/R2); accepted_closed_obligations=0; theorem_complete=false")


if __name__ == "__main__":
    main()
