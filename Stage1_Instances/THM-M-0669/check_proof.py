#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, and claim checks for THM-M-0669 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0669-PROOF"
THEOREM = "THM-M-0669"
BASE_REVISION = "a23d86cd84f03c26102b43c6b1b3b6d0a7a31e61"
BASE_TREE = "9268aa9f5379837642b6f748f01255e8744c4e78"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TARGET_EXPRESSION_SHA256 = (
    "91efc0e7986951efbb4f667a73f31de3eae2f0221d397c37c13a303f3769badd"
)
DENOMINATOR_SHA256 = (
    "9ec85645aa13399fb7dd6255e1cb66f90fc3694c536f6a282a6b30f19173afb4"
)
PROVISIONAL_IDS = ["M0669-C-BOOLEAN"]
PARTIAL_IDS = ["M0669-C-ATOMIC", "M0669-I-FORMULA", "M0669-T-ASSEMBLE"]
REMAINING_CUT = [
    "M0669-E-ONE-VAR",
    "M0669-E-SIGN",
    "M0669-E-ROOTS",
    "M0669-E-PROJECT",
    "M0669-E-SEMANTICS",
    "M0669-I-FORMULA",
    "M0669-T-ASSEMBLE",
    "M0669-ROOT",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/instance.json",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
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
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 713
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-0669-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "theorem atomicEqualityNormalization",
        "theorem atomicPolynomialNormalization",
        "theorem qfBooleanClosure",
        "def OneVariableEliminationPackage : Prop",
        "theorem formulaElimination_of_oneVariable",
        "theorem tarskiQuantifierElimination_of_oneVariable",
        "(oneVariable : OneVariableEliminationPackage)",
        "assert_no_sorry formulaElimination_of_oneVariable",
        "#print axioms tarskiQuantifierElimination_of_oneVariable",
    ):
        assert marker in proof, marker
    assert "theorem tarskiQuantifierElimination :" not in proof

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0669-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["root_machine_classification"] == "M3"
    assert graphs["closure_boundary"]["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["provisional_remaining_machine_cut"] == REMAINING_CUT
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
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    result = receipt["result"]
    assert result["exit_code"] == 0
    assert result["root_closed"] is False
    assert result["accepted_closed_obligation_ids"] == []
    assert result["audit_complete"] is False
    assert result["theorem_complete"] is False

    assert blocker["partial_proof_receipt_id"] == receipt["receipt_id"]
    assert blocker["proof_body_added"] is True
    assert blocker["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert blocker["accepted_closed_obligation_ids"] == []
    assert blocker["first_failed_gate"].startswith("M0669-E-ONE-VAR")
    assert blocker["remaining_root_cut_set"] == REMAINING_CUT
    assert blocker["root_closed"] is blocker["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0669 partial proof: syntax and conditional recursion checked")
    print("provisional closure: M0669-C-BOOLEAN")
    print("accepted closure: none; root open M3; theorem_complete=false")


if __name__ == "__main__":
    main()
