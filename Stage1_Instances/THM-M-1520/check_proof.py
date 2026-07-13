#!/usr/bin/env python3
"""Fail-closed local checks for S56-M-1520-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1520-PROOF"
THEOREM = "THM-M-1520"
BASE_REVISION = "f510617dd7a5509521db0a7ee0e5080a341b0a49"
BASE_TREE = "eeb5ae2931cc805f85de886f026ff61b02e28521"
EXPRESSION_SHA256 = "547fe7d61d57e7ea242aaff7a97763a769275f0c6f1c64d03ca5db45e82a012b"
DENOMINATOR_SHA256 = "3e5ecbc29279547f4e05323bfea6cdbda08b8e69545cffba35df81df8b460e4c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ChangeOfVariables.lean",
    f"Stage1_Instances/{THEOREM}/VectorFieldRegularity.lean",
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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    receipt = load(HERE / "proof-receipt.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 189
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 189
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1520-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)[ \t]+|\bextern[ \t]+",
        re.MULTILINE,
    )
    for path in sorted(HERE.glob("*.lean")):
        assert prohibited.search(without_comments(path.read_text(encoding="utf-8"))) is None, path

    vector = (HERE / "VectorFieldRegularity.lean").read_text(encoding="utf-8")
    change = (HERE / "ChangeOfVariables.lean").read_text(encoding="utf-8")
    for marker in (
        "theorem hamiltonianVectorField_contDiff_one",
        "ContDiff Real 1 (hamiltonianVectorField H)",
        "hH.fderiv_right",
        "#print sorries hamiltonianVectorField_contDiff_one",
    ):
        assert marker in vector, marker
    for marker in (
        "theorem timeMap_measurePreserving_of_differentiable_det_eq_one",
        "theorem allTimeMaps_measurePreserving_of_differentiable_det_eq_one",
        "timeMap_bijective hzero hflow t",
        "measurePreserving_of_det_fderiv_eq_one hdiff",
        "hdiff : forall t, Differentiable Real (Phi t)",
        "hdet : forall t z, (fderiv Real (Phi t) z).det = 1",
    ):
        assert marker in change, marker

    assert registry["root_obligation_id"] == "M1520-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_bodies"]["VectorFieldRegularity.lean"]["source_sha256"] == sha256(
        HERE / "VectorFieldRegularity.lean"
    )
    assert receipt["proof_bodies"]["ChangeOfVariables.lean"]["source_sha256"] == sha256(
        HERE / "ChangeOfVariables.lean"
    )
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["new_declarations_sorry_free"] is True
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == ["M1520-T-ALL-TIMES"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "no whole frozen obligation is claimed closed" in validation
    assert "not a premise-free proof of the exact root" in validation
    for path in [ROOT / path for path in CHANGED_PATHS]:
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1520 proof phase: C1 vector-field and conditional measure bridge self-test")
    print("no whole obligation or root closed; M1520-T-ALL-TIMES remains the minimal root cut")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
