#!/usr/bin/env python3
"""Fail-closed source, receipt, and claim checks for THM-M-1553 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1553-PROOF"
THEOREM = "THM-M-1553"
BASE_REVISION = "bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad"
BASE_TREE = "ca999baf360c6ce2440bbc2c01aeb8d519269a90"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
TARGET_EXPRESSION_SHA256 = "ef5d4bb909f3eba6d2a347e8bad055e3a4a08402beb725499259bb9bf1a9c3bc"
REGISTRY_DENOMINATOR_SHA256 = "553f66664b7a640a7e299ac12a65bfcf668173fbfb556f179614ae1dd4fbfed1"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/ProofLemmas.lean",
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


def main() -> None:
    proof_path = HERE / "Proof.lean"
    lemmas_path = HERE / "ProofLemmas.lean"
    proof = proof_path.read_text(encoding="utf-8")
    lemmas = lemmas_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 212
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["depends_on"] == ["S56-M-1553-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["state"] == "[ ]"
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b|"
        r"\b(?:implemented_by|native_decide)\b",
        re.MULTILINE,
    )
    assert prohibited.search(lemmas) is None
    proof_without_audit_commands = re.sub(r"^#print sorries .*?$", "", proof, flags=re.MULTILINE)
    assert prohibited.search(proof_without_audit_commands) is None
    for fragment in (
        "theorem logarithmic_bilinear_identity",
        "theorem logDerivativeBridge",
        "theorem hirotaKdVTarget_proof : HirotaKdVTarget",
        "hirotaKdVTarget_of_logDerivativeBridge logDerivativeBridge",
        "assert_no_sorry hirotaKdVTarget_proof",
        "#print axioms hirotaKdVTarget_proof",
    ):
        assert fragment in proof, fragment
    for fragment in (
        "theorem partial_commute",
        "theorem partialT_mixedDerivative",
        "theorem hirotaD_four_zero",
        "theorem hirotaD_one_one",
        "theorem exp_mixed_four_zero",
        "theorem exp_mixed_one_one",
    ):
        assert fragment in lemmas, fragment

    assert statement["canonical_formal_target"]["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1553.HirotaKdVTarget"
    )
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M1553-ROOT"
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["lemmas_sha256"] == sha256(lemmas_path)
    assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["inputs"]["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
    assert receipt["inputs"]["obligation_registry_sha256"] == sha256(HERE / "obligation-registry.json")
    assert receipt["inputs"]["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
    assert receipt["closed_obligation_ids"] == [
        "M1553-S-CONTEXT", "M1553-N-HIROTA", "M1553-N-TRANSFORM",
        "M1553-L-REGULARITY", "M1553-L-LOG", "M1553-L-MIXED",
        "M1553-B-POLYNOMIAL", "M1553-T-ZERO", "M1553-T-ASSEMBLE",
        "M1553-S-BOUNDARY", "M1553-ROOT",
    ]
    assert receipt["result"]["root_machine_proof_body_present"] is True
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1553 proof phase: exact frozen machine root has a local body")
    print("axioms: propext, Classical.choice, Quot.sound; placeholders: none")
    print("theorem_complete=false: validation, source/readability, release, and master gates remain open")


if __name__ == "__main__":
    main()
