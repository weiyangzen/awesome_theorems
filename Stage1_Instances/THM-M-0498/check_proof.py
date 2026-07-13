#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, and claim checks for THM-M-0498 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0498-PROOF"
THEOREM = "THM-M-0498"
BASE_REVISION = "3bb4cb3ae15dff8b48c93242019edec3bf858e48"
BASE_TREE = "8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TERMINAL_SOURCE_SHA256 = "99118a9578c0891aead06bdf0546fb137b68b12cd44bc311fcb242fc40e23f17"
TERMINAL_OLEAN_SHA256 = "722ba67755d61af55e3c463a962a399a20c760ecd99af75d15a62b5814cca18d"
STATEMENT_EXPRESSION_SHA256 = "4de2508b7d4cc86d13c5d51e1b5d6b8c61e43dec6655035224c21e25745af526"
REGISTRY_DENOMINATOR_SHA256 = "8a964cd4c13dc98d9bfa75e22cf5bab2af31d96d83bde13600049c669d88f144"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
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

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 258
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["depends_on"] == ["S56-M-0498-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["state"] == "[ ]"
    assert item["deliverable"] == "Implement or pin/import the required proof bodies without placeholders."
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b|"
        r"\b(?:implemented_by|native_decide)\b",
        re.MULTILINE,
    )
    assert prohibited.search(proof) is None
    for fragment in (
        "import ObligationTree",
        "theorem LSeries_vonMangoldt_logDerivative",
        "ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div hs",
        "assert_no_sorry ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div",
        "assert_no_sorry LSeries_vonMangoldt_logDerivative",
        "#print sorries LSeries_vonMangoldt_logDerivative",
        "#print axioms LSeries_vonMangoldt_logDerivative",
    ):
        assert fragment in proof, fragment

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    terminal_source = mathlib / "Mathlib/NumberTheory/LSeries/Dirichlet.lean"
    terminal_olean = mathlib / ".lake/build/lib/lean/Mathlib/NumberTheory/LSeries/Dirichlet.olean"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    terminal_text = terminal_source.read_text(encoding="utf-8")
    for marker in (
        "lemma LSeries_vonMangoldt_eq_deriv_riemannZeta_div",
        "rw [LSeries_vonMangoldt_eq hs",
        "Filter.EventuallyEq.deriv_eq",
    ):
        assert marker in terminal_text

    dirichlet = next(
        node for node in graphs["nodes"] if node["obligation_id"] == "M0498-A-DIRICHLET"
    )
    assert dirichlet["formal_target"] == (
        "planned wrapper around ArithmeticFunction."
        "LSeries_vonMangoldt_eq_deriv_riemannZeta_div"
    )
    assert dirichlet["machine_debt"] == "M4"
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M0498-T-ANALYTIC"]
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["terminal_source_sha256"] == TERMINAL_SOURCE_SHA256
    assert receipt["proof_body"]["terminal_olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["inputs"]["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
    assert receipt["inputs"]["obligation_registry_sha256"] == sha256(HERE / "obligation-registry.json")
    assert receipt["inputs"]["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
    assert receipt["closed_obligation_ids"] == []
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == ["M0498-T-ANALYTIC"]

    assert blocker["proof_body_added"] is True
    assert blocker["supported_subbranches"] == ["M0498-A-DIRICHLET"]
    assert "M0498-A-DIRICHLET" not in blocker["open_supporting_obligations"]
    assert blocker["remaining_root_cut_set"] == ["M0498-T-ANALYTIC"]
    assert blocker["root_closed"] is blocker["theorem_complete"] is False

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

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        path = ROOT / relative
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0498 proof phase: pinned logarithmic-derivative bridge checked")
    print("closed frozen obligations: none; exact bridge fingerprint awaits master reconciliation")
    print("root closure: open (M4); theorem_complete=false")


if __name__ == "__main__":
    main()
