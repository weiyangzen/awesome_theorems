#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0061-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0061-PROOF"
THEOREM = "THM-M-0061"
BASE_REVISION = "771d5d4800fbd95eaaa343e9bc55ebfdde20b364"
BASE_TREE = "a98ba0c37e56a7c04256f7d7df305c88e5cbe76e"
EXPRESSION_SHA256 = "adff72e9052ea17e3b6e4349c23028f35f4b8e3c610ea5f9f3b4fc02fe136836"
DENOMINATOR_SHA256 = "2d426a22d370fa53b308df9aa74a4cbaa69b1b30864da4ec30e1c8c31ba330d7"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
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
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1093
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0061-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments) is None
    for marker in (
        "import ObligationTree",
        "theorem lagrangeDivisibility : LagrangeDivisibilityTarget.{u}",
        "ObligationTree.root_of_finiteScope finiteGroupDivisibility",
        "ObligationTree.cosetProduct_of_fiber_engines fiberDecomposition",
        "Equiv.sigmaFiberEquiv QuotientGroup.mk",
        "QuotientGroup.eq_class_eq_leftCoset",
        "H.leftCosetEquivSubgroup g",
        "Equiv.sigmaEquivProd (G ⧸ H) H",
        "Nat.card_prod alpha beta",
        "Nat.card_congr e",
        "ObligationTree.cardProduct_of_engines",
        "Subgroup.card_eq_card_quotient_mul_card_subgroup H",
        "ObligationTree.divisibility_of_cardProduct cardProductIdentity",
        "Subgroup.card_subgroup_dvd_card H",
        "#print sorries lagrangeDivisibility",
        "#print axioms lagrangeDivisibility",
    ):
        assert marker in proof, marker

    machine_ids = registry["frozen_denominators"]["required_machine"]
    assert len(machine_ids) == 14 and machine_ids[0] == "M0061-ROOT"
    assert machine_ids[-1] == "M0061-T-SIGMA-PRODUCT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0061-ROOT"
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["closed_obligation_ids"] == machine_ids
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
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-L" in validation and "M0061-S-FOUNDATION" in validation
    for path in (proof_path, HERE / "check_proof.py", HERE / "check_proof.sh"):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0061 proof phase: exact frozen root has a complete local composition")


if __name__ == "__main__":
    main()
