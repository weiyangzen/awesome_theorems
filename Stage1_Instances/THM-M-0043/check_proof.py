#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0043-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0043-PROOF"
THEOREM = "THM-M-0043"
BASE_REVISION = "75ab5edd624df749325d391b41b669f8d72774b2"
BASE_TREE = "26562e2b8168d91a92a8164c9d8f0fc55178836e"
EXPRESSION_SHA256 = "a46ee23911b8027aa5de93149fd781def441429e386cb9181fc2064b2898557a"
DENOMINATOR_SHA256 = "1a92339af83640c1cf5d8853722d8c381b11a9d4139c4cb251cea3781d5b2af8"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROOF_IDS = [
    "M0043-ROOT",
    "M0043-N-NORMAL-COMMUTE",
    "M0043-C-HERMITIAN-PARTS",
    "M0043-L-H-HERMITIAN",
    "M0043-L-K-HERMITIAN",
    "M0043-T-M-RECONSTRUCT",
    "M0043-L-HK-COMMUTE",
    "M0043-T-LINEAR-COMMUTE",
    "M0043-C-JOINT-EIGENSPACE",
    "M0043-L-JOINT-DECOMP",
    "M0043-L-JOINT-ORTHOGONAL",
    "M0043-L-FINITE-EIGENVALUES",
    "M0043-B-NONZERO-SUBTYPE",
    "M0043-L-SUBORDINATE-BASIS",
    "M0043-C-BASIS-REINDEX",
    "M0043-T-OPERATOR-DECOMP",
    "M0043-C-EIGENVALUES",
    "M0043-L-BASIS-EIGENVECTORS",
    "M0043-L-UNITARY-BASIS",
    "M0043-C-UNITARY-MATRIX",
    "M0043-L-MATRIX-EIGEN-RELATION",
    "M0043-T-CONJUGATED-DIAGONAL",
    "M0043-T-ROOT-COMPOSE",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}
PINNED_SOURCES = {
    "Mathlib/Analysis/InnerProductSpace/JointEigenspace.lean": (
        "9342a846990506a5240299915ff3788c89a12856",
        "901b240b008bc3c2e240072ba271db3076c43ea600fd57da95df20d05380902c",
    ),
    "Mathlib/Analysis/Matrix/Spectrum.lean": (
        "1e6809ddfb7d49841b23b4084e45141277c8daf8",
        "1a1a96a6f057a73b0d428b62cdbb3da824981928c162b52a15335abdafc8b0db",
    ),
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
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1083
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0043-OBLIGATION_TREE"]
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
        "theorem commutingHermitianParts_conjugatedDiagonal",
        "hHs.directSum_isInternal_of_commute hKs hcomm",
        "hActiveInternal.subordinateOrthonormalBasis",
        "theorem normalComplexConjugatedDiagonal : ExactConjugatedDiagonalAnchor.{u}",
        "theorem spectralTheorem_via_frozen_composition : SpectralTheoremTarget.{u}",
        "root_of_exactConjugatedDiagonalAnchor normalComplexConjugatedDiagonal",
        "#print sorries spectralTheorem_via_frozen_composition",
        "#print axioms spectralTheorem_via_frozen_composition",
    ):
        assert marker in proof, marker

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["closed_obligation_ids"] == PROOF_IDS
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

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0043-ROOT"
    assert graphs["metrics_projection"]["proof_reachable_ids"] == PROOF_IDS
    assert receipt["recipe"]["covered_ids"] == PROOF_IDS
    proof_pairs = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    for edge in (
        ("M0043-ROOT", "M0043-T-ROOT-COMPOSE"),
        ("M0043-T-ROOT-COMPOSE", "M0043-T-CONJUGATED-DIAGONAL"),
        ("M0043-T-CONJUGATED-DIAGONAL", "M0043-L-MATRIX-EIGEN-RELATION"),
        ("M0043-L-HK-COMMUTE", "M0043-N-NORMAL-COMMUTE"),
    ):
        assert edge in proof_pairs

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip() == MATHLIB_REVISION
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip() == MATHLIB_TREE
    assert not subprocess.check_output(
        ["git", "status", "--porcelain=v1"], cwd=mathlib, text=True
    ).strip()
    for source_rel, (blob, digest) in PINNED_SOURCES.items():
        source = mathlib / source_rel
        assert subprocess.check_output(
            ["git", "rev-parse", f"HEAD:{source_rel}"], cwd=mathlib, text=True
        ).strip() == blob
        assert sha256(source) == digest

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
    assert "M0-L" in validation and "M0043-S-FOUNDATION" in validation
    for path in (proof_path, HERE / "check_proof.py", HERE / "check_proof.sh"):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0043 proof phase: local exact root closes the frozen machine route")


if __name__ == "__main__":
    main()
