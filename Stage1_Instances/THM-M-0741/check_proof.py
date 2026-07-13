#!/usr/bin/env python3
"""Fail-closed source, pin, graph, and receipt checks for S56-M-0741-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0741-PROOF"
THEOREM = "THM-M-0741"
BASE_REVISION = "72e9e8092182121a6794921f61fcc9cae22f726d"
BASE_TREE = "0d6c1fdf06d1573c256af331c6b198e5a787af43"
EXPRESSION_SHA256 = "1a96ad274a14ef0c7285734258d28a7ff6e49febe1470bfbb957d757a92e718c"
DENOMINATOR_SHA256 = "ee9b5029b7cb4a820132e16aeeb1a5c6e304e81bb8624f0f931aee9547cb9bcd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE = "Mathlib/Computability/Halting.lean"
MATHLIB_SOURCE_BLOB = "0834371356762db805d37208b9cf8a1fc0efd217"
MATHLIB_SOURCE_SHA256 = "c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de"
RICE_BODY_SHA256 = "7b1ffed124cbbab29edb690e35fedff63aabb101470802ee0d2dbf8c8fd4f7a1"
HALTING_BODY_SHA256 = "c79df2fcf31c93fe6ac57f179d2b03c41416baa313d68b9bbe76dc3499c5d41d"
MACHINE_PROOF_IDS = [
    "M0741-ROOT",
    "M0741-N-FIXED-ZERO",
    "M0741-C-PAIR-ZERO",
    "M0741-L-RESTRICT",
    "M0741-X-FIXED-HALTING",
    "M0741-X-RICE",
    "M0741-B-FIXED-WITNESSES",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1329
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0741-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem riceBridge_pinned : RiceBridge",
        "exact ComputablePred.rice C h hf hg hfC",
        "theorem fixedInputZeroUndecidable_via_rice : FixedInputZeroUndecidable",
        "fixedInputZeroUndecidable_of_rice riceBridge_pinned fixedZeroWitnessPackage",
        "theorem fixedInputZeroUndecidable_pinned : FixedInputZeroUndecidable",
        "exact ComputablePred.halting_problem 0",
        "theorem fixedInputReduction_checked : FixedInputReduction",
        "pairToFixedRestriction_of_embedding pairZeroEmbedding_computable",
        "theorem haltingProblemUndecidable : HaltingProblemUndecidable",
        "root_of_reduction_and_fixedInput fixedInputReduction_checked",
        "#print sorries haltingProblemUndecidable",
        "#print axioms haltingProblemUndecidable",
    ):
        assert marker in proof, marker

    assert registry["frozen_denominators"]["required_machine"] == MACHINE_PROOF_IDS
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0741-ROOT"
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0741.HaltingProblemUndecidable"
    )
    proof_pairs = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    assert proof_pairs == {
        ("M0741-ROOT", "M0741-N-FIXED-ZERO"),
        ("M0741-ROOT", "M0741-X-FIXED-HALTING"),
        ("M0741-N-FIXED-ZERO", "M0741-L-RESTRICT"),
        ("M0741-L-RESTRICT", "M0741-C-PAIR-ZERO"),
        ("M0741-X-FIXED-HALTING", "M0741-X-RICE"),
        ("M0741-X-FIXED-HALTING", "M0741-B-FIXED-WITNESSES"),
    }

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["provisionally_closed_proof_obligation_ids"] == MACHINE_PROOF_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    recipe = receipt["recipe"]
    assert set(recipe) == {
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    }
    assert recipe["recipe_id"] == "S56-M-0741-PROOF-LEAN"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "bash", "Stage1_Instances/THM-M-0741/check_proof.sh"
    ]
    assert recipe["env_allowlist"] == {} and recipe["timeout_seconds"] == 180
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["expected_outputs"] == [
        {
            "path_or_stream": "stdout",
            "semantic_hash_policy": (
                "contains Stage1Instances.THM_M_0741.Proof."
                "haltingProblemUndecidable : HaltingProblemUndecidable"
            ),
        },
        {
            "path_or_stream": "stdout",
            "semantic_hash_policy": "contains exactly 8 Declarations are sorry-free! reports",
        },
        {
            "path_or_stream": "stdout",
            "semantic_hash_policy": (
                "contains exactly 8 axiom reports, each equal to "
                "[propext, Classical.choice, Quot.sound]"
            ),
        },
    ]
    assert recipe["covered_obligation_ids"] == MACHINE_PROOF_IDS
    assert set(recipe["covered_declarations"]) == {
        "ComputablePred.rice",
        "ComputablePred.halting_problem",
        "Stage1Instances.THM_M_0741.Proof.riceBridge_pinned",
        "Stage1Instances.THM_M_0741.Proof.fixedInputZeroUndecidable_via_rice",
        "Stage1Instances.THM_M_0741.Proof.fixedInputZeroUndecidable_pinned",
        "Stage1Instances.THM_M_0741.Proof.fixedInputReduction_checked",
        "Stage1Instances.THM_M_0741.Proof.haltingProblemUndecidable",
        "Stage1Instances.THM_M_0741.Proof.haltingProblemUndecidable_via_rice",
    }
    assert receipt["proof_graph_composition"]["all_required_proof_edges_consumed"] is True
    evidence = {
        row["obligation_id"]: row for row in receipt["provisional_obligation_evidence"]
    }
    assert list(evidence) == MACHINE_PROOF_IDS
    assert all(row["declarations"] for row in evidence.values())

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    source = mathlib / MATHLIB_SOURCE
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    assert git_output("rev-parse", f"HEAD:{MATHLIB_SOURCE}", cwd=mathlib) == MATHLIB_SOURCE_BLOB
    assert sha256(source) == MATHLIB_SOURCE_SHA256
    assert sha256_lines(source, 208, 218) == RICE_BODY_SHA256
    assert sha256_lines(source, 240, 242) == HALTING_BODY_SHA256

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert receipt["inputs"]["proof_validation_sha256"] == sha256(
        HERE / "proof-validation.md"
    )
    assert receipt["inputs"]["worker_packet_sha256"] == sha256(
        ROOT / ".stage1-worker-selftest.json"
    )
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "M0741-S-FOUNDATION" in validation
    for path in (
        proof_path,
        HERE / "check_proof.py",
        HERE / "check_proof.sh",
        HERE / "proof-receipt.json",
        HERE / "proof-validation.md",
        ROOT / ".stage1-worker-selftest.json",
    ):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "PASS THM-M-0741 proof phase: exact frozen root closes through all "
        "seven required machine obligations"
    )


if __name__ == "__main__":
    main()
