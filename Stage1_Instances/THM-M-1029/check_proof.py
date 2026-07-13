#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, and handoff checks for THM-M-1029 proof."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1029-PROOF"
THEOREM = "THM-M-1029"
BASE_REVISION = "dd9bc71d70586d022d87833d780fbe15959b89b0"
BASE_TREE = "d096d4ef8804532c9165b75d369f49b7b74945d8"
TARGET_EXPRESSION = "f3e443377f8cac2eba62a6ebcf6f05ce5bd453f3075d9de573641856e21331b2"
REGISTRY_DENOMINATOR = "f5ba78d2ff64231db87b356cdf2827f4d9173387c0a387c3acfbddad19cf0fb4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_DECLARATIONS = {
    "bracketCompensated_deterministicTime_eq",
    "deterministicTimeProcess_continuousPaths",
    "deterministicTimeProcess_monotonePaths",
    "deterministicTimeProcess_startsAtZero",
    "bracketCompensated_martingale_of_quadratic",
    "quadraticCompensated_stronglyAdapted",
    "square_stronglyAdapted",
    "deterministicTime_stronglyAdapted_of_martingales",
    "quadratic_coordinate_integrable",
    "coordinate_memLp_two",
    "increment_memLp_two",
    "increment_square_integrable",
    "increment_condExp_eq_zero",
    "increment_condExp_sq",
    "integral_process_eq_zero",
    "integral_process_sq_eq_time",
    "variance_process_eq_time",
    "zeroElapsedIncrement",
    "hasLaw_gaussianReal_of_charFun",
    "hasLaw_gaussianReal_zero",
    "incrementLawPackage_of_components",
    "incrementLawPackage_of_strict",
    "root_of_assumedIncrementComponents",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker-2026-07-14.json",
    f"Stage1_Instances/{THEOREM}/proof-execution.md",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker-2026-07-14.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 222
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1029-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        assert prohibited.search((HERE / name).read_text(encoding="utf-8")) is None, name

    declared = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", proof, re.MULTILINE))
    assert declared == EXPECTED_DECLARATIONS, (declared, EXPECTED_DECLARATIONS)
    assert proof.count("#print axioms") == len(EXPECTED_DECLARATIONS)
    for marker in (
        "import ObligationTree",
        "theorem increment_condExp_eq_zero",
        "theorem increment_condExp_sq",
        "theorem zeroElapsedIncrement",
        "theorem hasLaw_gaussianReal_of_charFun",
        "def GaussianIncrementLawPackage : Prop",
        "def IncrementIndependencePackage : Prop",
        "def StrictIncrementLawPackage : Prop",
        "theorem root_of_assumedIncrementComponents",
        "(gaussian : GaussianIncrementLawPackage.{u})",
        "(independent : IncrementIndependencePackage.{u})",
    ):
        assert marker in proof, marker

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == TARGET_EXPRESSION
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR
    assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M1029-T-INCREMENTS"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), filename
    receipt_names = {name.rsplit(".", 1)[-1] for name in receipt["exact_declarations"]}
    assert receipt_names == EXPECTED_DECLARATIONS
    assert receipt["closed_obligation_ids"] == []
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == ["M1029-T-INCREMENTS"]

    assert blocker["outcome"] == "blocked" and blocker["proof_body_added"] is True
    assert blocker["closed_obligation_ids"] == []
    assert blocker["remaining_root_cut_set"] == ["M1029-T-INCREMENTS"]
    assert blocker["root_closed"] is blocker["theorem_complete"] is False

    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1029 proof phase: 23 placeholder-free partial bodies checked")
    print("closed frozen obligations: none; partial subbranches await graph reconciliation")
    print("root closure: open (M3); theorem_complete=false")


if __name__ == "__main__":
    main()
