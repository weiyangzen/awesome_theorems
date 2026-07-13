#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0025-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0025-PROOF"
THEOREM = "THM-M-0025"
BASE_REVISION = "72f928bdf1a47d7c119826db45575bd02a3a63ce"
BASE_TREE = "171a6bfae88220f5df9b39cdd6c7e1bf17639889"
EXPRESSION_SHA256 = "9bb5ed6dd01550f3481d4a66e1d81009272b717997f9752ff422029da2828564"
DENOMINATOR_SHA256 = "a93e848c6941b5069b7e79e2d5f88ddea8663e7443f7ebcf3719e5b0022ebc3c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE_SHA256 = "7cedafd3e1fc910b152c699375e8670f0db7d6261d7ebdd3dd8ff2420fda5b9c"
MATHLIB_SOURCE_BLOB = "1ae18244a4534f336f1d9280a1f5f8fd1a5acd9f"
CLOSED_IDS = [
    "M0025-ROOT",
    "M0025-T-ROOT-COMPOSE",
    "M0025-T-IDEAL-FG-COMPOSE",
    "M0025-X-MATHLIB-BODY",
    "M0025-N-IDEAL-FG",
    "M0025-C-WF-MIN",
    "M0025-L-MIN-DOMINATES",
    "M0025-C-BOUNDED-GENERATORS",
    "M0025-L-BOUNDED-SPAN",
    "M0025-L-GENERATOR-SPAN-SUBSET",
    "M0025-L-STRONG-INDUCTION-SPAN",
    "M0025-B-DEGREE-SPLIT",
    "M0025-B-HIGH-DEGREE-NONTRIVIAL",
    "M0025-C-LEADING-REPRESENTATIVE",
    "M0025-L-DEGREE-CANCELLATION",
    "M0025-T-SPAN-COMPOSE",
    "M0025-T-FG-COMPOSE",
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
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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

    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip() == BASE_REVISION
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True
    ).strip() == BASE_TREE

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1070
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0025-OBLIGATION_TREE"]
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
        "theorem exactPolynomialAnchor : ExactPolynomialAnchor.{u}",
        "exact Polynomial.isNoetherianRing",
        "theorem hilbertBasisTheorem_direct : HilbertBasisTheoremTarget.{u}",
        "theorem hilbertBasisTheorem_via_frozen_composition",
        "root_of_exactPolynomialAnchor exactPolynomialAnchor",
        "#print sorries Polynomial.isNoetherianRing",
        "#print axioms hilbertBasisTheorem_via_frozen_composition",
    ):
        assert marker in proof, marker

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["closed_obligation_ids"] == CLOSED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["inputs"]["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
    assert receipt["inputs"]["obligation_registry_sha256"] == sha256(
        HERE / "obligation-registry.json"
    )
    assert receipt["inputs"]["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
    assert receipt["inputs"]["anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(HERE / "check_proof.sh")
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["theorem_complete"] is False

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0025-ROOT"
    architecture_ids = {
        row["obligation_id"]
        for row in registry["obligations"]
        if row["machine_eligibility"] == "required"
        and not row["obligation_id"].startswith("M0025-S-")
    }
    assert architecture_ids == set(CLOSED_IDS)
    assert receipt["recipe"]["covered_ids"] == CLOSED_IDS

    proof_edges = graphs["graphs"]["proof"]["edges"]
    proof_path_pairs = {
        (edge["from"], edge["to"])
        for edge in proof_edges
        if edge["type"] == "proof_requires"
    }
    assert {
        ("M0025-ROOT", "M0025-T-ROOT-COMPOSE"),
        ("M0025-T-ROOT-COMPOSE", "M0025-T-IDEAL-FG-COMPOSE"),
        ("M0025-T-IDEAL-FG-COMPOSE", "M0025-X-MATHLIB-BODY"),
    } == proof_path_pairs

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    source_rel = Path("Mathlib/RingTheory/Polynomial/Basic.lean")
    source = mathlib / source_rel
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip() == MATHLIB_REVISION
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip() == MATHLIB_TREE
    assert subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{source_rel}"], cwd=mathlib, text=True
    ).strip() == MATHLIB_SOURCE_BLOB
    assert not subprocess.check_output(
        ["git", "status", "--porcelain=v1"], cwd=mathlib, text=True
    ).strip()
    assert sha256(source) == MATHLIB_SOURCE_SHA256
    source_text = source.read_text(encoding="utf-8")
    body_lines = source.read_bytes().splitlines(keepends=True)[731:806]
    assert hashlib.sha256(b"".join(body_lines)).hexdigest() == (
        receipt["proof_body"]["terminal_body_sha256"]
    )
    start = source_text.index("protected theorem Polynomial.isNoetherianRing")
    end = source_text.index("attribute [instance] Polynomial.isNoetherianRing")
    terminal = without_comments(source_text[start:end])
    assert prohibited.search(terminal) is None
    for marker in (
        "isNoetherianRing_iff.2",
        "inst.wf.min (Set.range I.leadingCoeffNth)",
        "let ⟨s, hs⟩ := I.is_fg_degreeLE N",
        "induction k using Nat.strong_induction_on",
        "have := Polynomial.degree_sub_lt h1 hp0 h2",
    ):
        assert marker in terminal, marker

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "M0025-S-FOUNDATION" in validation
    for path in (proof_path, HERE / "check_proof.py", HERE / "check_proof.sh"):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "PASS THM-M-0025 proof phase: exact pinned M0-W body closes the frozen machine route"
    )


if __name__ == "__main__":
    main()
