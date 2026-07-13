#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0441-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0441-PROOF"
THEOREM = "THM-M-0441"
BASE_REVISION = "8f22279fd1216cdfb5676c758e6bdb08e0ba3e01"
BASE_TREE = "d2e9e68da52ecfcfe15a9c48ac2262400e602667"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
STATEMENT_EXPRESSION_SHA256 = (
    "103f282fc63e0dfa6ac9de4f13736044bf5131a41883196fdca531df00a5a475"
)
PROVISIONAL_IDS = []
PARTIAL_IDS = [
    "M0441-S-HEIGHT",
    "M0441-S-ALG",
    "M0441-B-ZERO",
    "M0441-B-POS",
    "M0441-L-COUNT",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
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

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 87
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-0441-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "theorem finite_transcendentalRationalPoints",
        "theorem ncard_transcendentalRationalPoints_le_height_slice",
        "theorem countingConclusion_zero_dimensional",
        "theorem pilaWilkie_zero_dimensional",
        "theorem countingConclusion_of_diff_eq_empty",
        "theorem countingConclusion_of_semialgebraic_preconnected_nontrivial",
        "#print axioms countingConclusion_zero_dimensional",
    ):
        assert marker in proof, marker
    assert "theorem pilaWilkie : PilaWilkie" not in proof
    assert "CountingEngine where" not in proof

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0441-ROOT"
    assert len(registry["obligations"]) == 21
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M0441-C-PARAM",
        "M0441-L-DET",
        "M0441-C-BLOCKS",
        "M0441-B-INDUCT",
        "M0441-SOURCE",
        "M0441-TRUST",
    ]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for filename, expected in receipt["inputs"].items():
        if filename in {"proof-blocker.json", "proof-validation.md"}:
            continue
        assert expected == sha256(HERE / filename), filename
    result = receipt["result"]
    assert result["zero_dimensional_specialization_kernel_closed"] is True
    assert result["root_kernel_closed"] is False
    assert result["theorem_complete"] is False

    assert blocker["partial_proof_receipt_id"] == receipt["receipt_id"]
    assert blocker["proof_body_added"] is True
    assert blocker["proof_file_sha256"] == sha256(proof_path)
    assert blocker["canonical_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert blocker["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert blocker["root_closed"] is False
    assert blocker["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    packet = load(ROOT / ".stage1-worker-selftest.json")
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
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "PASS THM-M-0441 proof phase: n=0 specialization checked; "
        "general Pila-Wilkie root remains open"
    )


if __name__ == "__main__":
    main()
