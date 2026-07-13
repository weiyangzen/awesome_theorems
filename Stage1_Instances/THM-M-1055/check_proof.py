#!/usr/bin/env python3
"""Fail-closed checks for the THM-M-1055 proof installation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1055-PROOF"
THEOREM = "THM-M-1055"
BASE_REVISION = "bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad"
BASE_TREE = "ca999baf360c6ce2440bbc2c01aeb8d519269a90"
STATEMENT_EXPRESSION = "8d7956f1f5f46ae435293eef17df7881f26d9c18fad6ac54c870e232cdb26181"
REGISTRY_DENOMINATOR = "cb67895834a856b780f44cbcf8c3de106f574f5035d3003486181876fd382d06"
UPSTREAM_REVISION = "ed3fa6b8a30594eeb791160563942ba115581aa0"
UPSTREAM_ARCHIVE_SHA256 = "3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52"
UPSTREAM_MAXIMAL_SHA256 = "6b9c40bd0e8d7238919283ad8666d0563d780a3b31eeb67d0ca66aae821817cc"
PORT_MAXIMAL_SHA256 = "b310154abc8a2407785ddc42dc3c1d4a1e45643cca47c9a2ff77fda7999298d4"
UPSTREAM_BIRKHOFF_SHA256 = "bed8d81c6eb7f0ba74548255779dad7c3dc4e75ecf7ad935e1c68ef6fcb6ea6a"
PORT_BIRKHOFF_SHA256 = "de397519e3d49a8362270695ee860365ee1f6b41fd1d13829562d0cf752c0f12"
LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MACHINE_IDS = [
    "M1055-ROOT",
    "M1055-S-DEFINITIONS",
    "M1055-S-BOUNDARY",
    "M1055-S-FOUNDATION",
    "M1055-A-EXTERNAL-INTEGRATION",
    "M1055-L-POINTWISE-LIMIT",
    "M1055-L-LIMIT-MEASURABLE",
    "M1055-L-LIMIT-INVARIANT",
    "M1055-L-ERGODIC-CONSTANCY",
    "M1055-L-INTEGRAL-IDENTIFICATION",
    "M1055-T-INVARIANT-LIMIT",
    "M1055-T-ASSEMBLE",
]
PROVISIONALLY_CLOSED_IDS = [
    "M1055-S-DEFINITIONS",
    "M1055-S-BOUNDARY",
    "M1055-L-LIMIT-MEASURABLE",
    "M1055-L-LIMIT-INVARIANT",
    "M1055-L-ERGODIC-CONSTANCY",
]
ALTERNATE_PORT_IDS = [
    "M1055-ROOT",
    "M1055-A-EXTERNAL-INTEGRATION",
    "M1055-L-POINTWISE-LIMIT",
    "M1055-L-INTEGRAL-IDENTIFICATION",
    "M1055-T-INVARIANT-LIMIT",
    "M1055-T-ASSEMBLE",
]


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
    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 247
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1055-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    receipt = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1055.BirkhoffErgodicTarget"
    )
    assert formal["elaborated_expression_sha256"] == STATEMENT_EXPRESSION
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS

    proof_edges = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    assert proof_edges == {
        ("M1055-ROOT", "M1055-T-ASSEMBLE"),
        ("M1055-T-ASSEMBLE", "M1055-T-INVARIANT-LIMIT"),
        ("M1055-T-INVARIANT-LIMIT", "M1055-L-POINTWISE-LIMIT"),
        ("M1055-T-INVARIANT-LIMIT", "M1055-L-ERGODIC-CONSTANCY"),
        ("M1055-T-INVARIANT-LIMIT", "M1055-L-INTEGRAL-IDENTIFICATION"),
        ("M1055-L-POINTWISE-LIMIT", "M1055-A-EXTERNAL-INTEGRATION"),
        ("M1055-L-ERGODIC-CONSTANCY", "M1055-L-LIMIT-MEASURABLE"),
        ("M1055-L-ERGODIC-CONSTANCY", "M1055-L-LIMIT-INVARIANT"),
        ("M1055-L-INTEGRAL-IDENTIFICATION", "M1055-L-POINTWISE-LIMIT"),
        ("M1055-L-INTEGRAL-IDENTIFICATION", "M1055-L-ERGODIC-CONSTANCY"),
    }

    proof_path = HERE / "Proof.lean"
    maximal_path = HERE / "External/MaximalErgodic.lean"
    birkhoff_path = HERE / "External/Birkhoff.lean"
    sources = [proof_path, maximal_path, birkhoff_path]
    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    for path in sources:
        assert prohibited.search(without_comments(path.read_text(encoding="utf-8"))) is None, path

    proof = proof_path.read_text(encoding="utf-8")
    for marker in (
        "import ObligationTree",
        "import Birkhoff",
        "theorem invariantLimitPackage_proof : InvariantLimitPackage.{u}",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral hT hf",
        "theorem birkhoffErgodicTarget : BirkhoffErgodicTarget.{u}",
        "root_of_invariantLimitPackage invariantLimitPackage_proof",
        "#print sorries birkhoffErgodicTarget",
        "#print axioms birkhoffErgodicTarget",
    ):
        assert marker in proof, marker

    assert sha256(maximal_path) == PORT_MAXIMAL_SHA256
    assert sha256(birkhoff_path) == PORT_BIRKHOFF_SHA256
    assert sha256(HERE / "LICENSE.external") == LICENSE_SHA256
    assert "integrable_finset_sum" in maximal_path.read_text(encoding="utf-8")
    assert "integrable_finsetSum" not in maximal_path.read_text(encoding="utf-8")
    assert birkhoff_path.read_text(encoding="utf-8").startswith("/-\nCopyright (c) 2026")

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["provisionally_closed_machine_obligation_ids"] == PROVISIONALLY_CLOSED_IDS
    assert receipt["kernel_closed_via_alternate_port_obligation_ids"] == ALTERNATE_PORT_IDS
    assert receipt["machine_root_cut_set"] == [
        "M1055-S-FOUNDATION",
        "M1055-A-EXTERNAL-INTEGRATION",
    ]
    assert receipt["frozen_proof_graph_cut_set"] == [
        "M1055-A-EXTERNAL-INTEGRATION"
    ]
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["upstream"]["revision"] == UPSTREAM_REVISION
    assert receipt["upstream"]["archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert receipt["upstream"]["maximal_ergodic_sha256"] == UPSTREAM_MAXIMAL_SHA256
    assert receipt["upstream"]["birkhoff_sha256"] == UPSTREAM_BIRKHOFF_SHA256
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["frozen_graph_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["inputs"]["proof_sha256"] == sha256(proof_path)
    assert receipt["inputs"]["maximal_ergodic_port_sha256"] == sha256(maximal_path)
    assert receipt["inputs"]["birkhoff_port_sha256"] == sha256(birkhoff_path)
    assert receipt["inputs"]["license_sha256"] == sha256(HERE / "LICENSE.external")
    assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(HERE / "check_proof.sh")

    changed = set(receipt["changed_paths"])
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == changed
    assert packet["known_failures"] == receipt["known_failures"]
    assert receipt["inputs"]["check_proof_py_sha256"] == sha256(HERE / "check_proof.py")
    assert receipt["inputs"]["proof_validation_sha256"] == sha256(HERE / "proof-validation.md")

    status = git_output("status", "--short", "--untracked-files=all")
    actual = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == changed

    print(
        "PASS THM-M-1055 proof attempt: exact Birkhoff root kernel proof passes; "
        "the frozen graph remains dependency-open"
    )
    print(f"upstream revision: {UPSTREAM_REVISION}")
    print("axioms: propext, Classical.choice, Quot.sound")
    print("machine root cut: M1055-S-FOUNDATION plus M1055-A-EXTERNAL-INTEGRATION")
    print("frozen proof-graph cut: M1055-A-EXTERNAL-INTEGRATION (route reconciliation required)")


if __name__ == "__main__":
    main()
