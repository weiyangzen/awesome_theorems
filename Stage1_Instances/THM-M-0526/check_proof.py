#!/usr/bin/env python3
"""Fail-closed scope and receipt checks for S56-M-0526-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0526-PROOF"
THEOREM = "THM-M-0526"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
EXPRESSION_SHA256 = "a7550267adfd8bc8d37de8174319c6389cb1bbab62b740595a9c91d831567d45"
DENOMINATOR_SHA256 = "6ee9cb595c6fee2025b76834826de8a48bb4a0bcb6fa86a8d3d91a17632452f5"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-phase-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 583
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0526-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "theorem square_commutativity_proof",
        "theorem square_package",
        "theorem path_subdivision_of_two_open_cover",
        "exists_monotone_Icc_subset_open_cover_unitInterval hcOpen hcCover",
        "Path.range_subpath_of_le",
        "#print axioms Stage1Instances.THM_M_0526.path_subdivision_of_two_open_cover",
    ):
        assert marker in proof, marker
    assert "theorem seifertVanKampen" not in proof

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0526.SeifertVanKampenTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["frozen_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_cut_set"] == [
        "SVK-MAP-FUNCTORIALITY",
        "SVK-LEBESGUE-NUMBER",
        "SVK-CHANGE-BASEPATH",
        "SVK-WORD-DEFINITION",
        "SVK-REFINEMENT-INVARIANCE",
        "SVK-HOMOTOPY-INVARIANCE",
        "SVK-LIFT-HOM",
        "SVK-GENERATION",
        "SVK-AGREEMENT-ON-WORDS",
    ]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["result"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["provisionally_closed_obligation_ids"] == [
        "SVK-MAP-FUNCTORIALITY", "SVK-SQUARE", "SVK-LEBESGUE-NUMBER"
    ]
    assert receipt["accepted_closed_obligation_ids"] == []

    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["root_closed"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["selftest_manifest_written"] is True
    assert blocker["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""

    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    actual_changes.discard("Formalizations/Lean/.lake")
    assert actual_changes == CHANGED_PATHS
    for path in (
        proof_path,
        HERE / "check_proof.py",
        HERE / "check_proof.sh",
        HERE / "proof-blocker.json",
        HERE / "proof-receipt.json",
        HERE / "proof-phase-validation.md",
        ROOT / ".stage1-worker-selftest.json",
    ):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "PASS THM-M-0526 partial proof phase: square and open-cover "
        "subdivision bodies self-tested; exact root remains open"
    )


if __name__ == "__main__":
    main()
