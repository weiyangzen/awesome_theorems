#!/usr/bin/env python3
"""Fail-closed source, provenance, and Lean checks for S56-M-1522-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1522-PROOF"
THEOREM = "THM-M-1522"
BASE_REVISION = "bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad"
BASE_TREE = "ca999baf360c6ce2440bbc2c01aeb8d519269a90"
EXPRESSION_SHA256 = "1ae3d8a352060fb26372a07d0128af2f465933e4c3c08b6c752b0b5fe72c83b5"
DENOMINATOR_SHA256 = "8a9a7f243137efb0ac3ebafe2b5de3a292f41bcb0cc6bdc4a1a6adc364fb3242"
UPSTREAM_REVISION = "ed3fa6b8a30594eeb791160563942ba115581aa0"
UPSTREAM_MAXIMAL_SHA256 = "6b9c40bd0e8d7238919283ad8666d0563d780a3b31eeb67d0ca66aae821817cc"
UPSTREAM_BIRKHOFF_SHA256 = "bed8d81c6eb7f0ba74548255779dad7c3dc4e75ecf7ad935e1c68ef6fcb6ea6a"
LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Birkhoff.lean",
    f"Stage1_Instances/{THEOREM}/LICENSE",
    f"Stage1_Instances/{THEOREM}/MaximalErgodic.lean",
    f"Stage1_Instances/{THEOREM}/PORT_PROVENANCE.md",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    return result.stdout


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def strip_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 190
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1522-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    receipt = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == [
        "M1522-L-POINTWISE", "M1522-T-IDENTIFY"
    ]
    composition = graphs["composition_certificate"]
    assert composition["declaration"].endswith("root_of_pointwise_and_identification")
    assert composition["children"] == ["M1522-L-POINTWISE", "M1522-T-IDENTIFY"]

    proof_paths = [HERE / "MaximalErgodic.lean", HERE / "Birkhoff.lean", HERE / "Proof.lean"]
    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    for path in proof_paths:
        assert prohibited.search(strip_comments(path.read_text(encoding="utf-8"))) is None, path
    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    for marker in (
        "theorem generalPointwiseLimitPackage : GeneralPointwiseLimitPackage",
        "ErgodicTheory.tendsto_birkhoffAverage_ae hT.toMeasurePreserving hf",
        "ErgodicTheory.condExp_invariants_comp_self",
        "theorem ergodicInvariantLimitIdentification",
        "hT.ae_eq_const_of_ae_eq_comp_ae",
        "theorem birkhoffPointwiseErgodicViaFrozenComposition",
        "root_of_pointwise_and_identification",
        "theorem birkhoffPointwiseErgodicDirect",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral hT hf",
    ):
        assert marker in proof, marker

    assert sha256(HERE / "LICENSE") == LICENSE_SHA256
    upstream_maximal = (HERE / "MaximalErgodic.lean").read_bytes()
    upstream_birkhoff = (HERE / "Birkhoff.lean").read_bytes()

    notice_maximal = (
        b"/-\nPort note: this file is modified from\n"
        + f"`marcmorningstar/lean4-ergodic-theory@{UPSTREAM_REVISION}`.\n".encode()
        + b"The sole compatibility change is the pinned-mathlib spelling\n"
        + b"`integrable_finset_sum`; see `PORT_PROVENANCE.md`.\n-/\n"
    )
    notice_birkhoff = (
        b"/-\nPort note: this file is modified from\n"
        + f"`marcmorningstar/lean4-ergodic-theory@{UPSTREAM_REVISION}`.\n".encode()
        + b"Only the sibling module import below is target-local; see `PORT_PROVENANCE.md`.\n-/\n"
    )
    assert upstream_maximal.count(notice_maximal) == 1
    assert upstream_birkhoff.count(notice_birkhoff) == 1
    reconstructed_maximal = upstream_maximal.replace(notice_maximal, b"", 1).replace(
        b"integrable_finset_sum", b"integrable_finsetSum", 1
    )
    reconstructed_birkhoff = upstream_birkhoff.replace(notice_birkhoff, b"", 1).replace(
        b"import MaximalErgodic", b"import ErgodicTheory.Ergodic.MaximalErgodic", 1
    )
    assert sha256_bytes(reconstructed_maximal) == UPSTREAM_MAXIMAL_SHA256
    assert sha256_bytes(reconstructed_birkhoff) == UPSTREAM_BIRKHOFF_SHA256

    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["maximal_port_sha256"] == sha256(HERE / "MaximalErgodic.lean")
    assert receipt["proof_body"]["birkhoff_port_sha256"] == sha256(HERE / "Birkhoff.lean")
    assert receipt["proof_body"]["proof_sha256"] == sha256(HERE / "Proof.lean")
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["theorem_complete"] is False

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    lean_bin = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    with tempfile.TemporaryDirectory(prefix="thm-m-1522-proof-") as temporary:
        temporary_path = Path(temporary)
        base_env = {**os.environ, "LEAN_PATH": lean_path}
        local_env = {**base_env, "LEAN_PATH": f"{temporary_path}:{lean_path}"}
        for source in ("Statement", "MaximalErgodic", "Birkhoff", "ObligationTree"):
            env = base_env if source in ("Statement", "MaximalErgodic") else local_env
            run(
                [lean_bin, "--trust=0", "--root", str(HERE), "-o",
                 str(temporary_path / f"{source}.olean"), str(HERE / f"{source}.lean")],
                cwd=LEAN_ROOT, env=env,
            )
        output = run(
            [lean_bin, "--trust=0", "--root", str(HERE), str(HERE / "Proof.lean")],
            cwd=LEAN_ROOT, env=local_env,
        )

    declarations = (
        "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
        "ErgodicTheory.tendsto_birkhoffAverage_ae",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
        "Stage1Instances.THM_M_1522.generalPointwiseLimitPackage",
        "Stage1Instances.THM_M_1522.ergodicInvariantLimitIdentification",
        "Stage1Instances.THM_M_1522.birkhoffPointwiseErgodicViaFrozenComposition",
        "Stage1Instances.THM_M_1522.birkhoffPointwiseErgodicDirect",
    )
    for declaration in declarations:
        assert declaration in output, declaration
    assert output.count("Declarations are sorry-free!") == len(declarations)
    assert "sorryAx" not in output
    assert output.count("depends on axioms") == len(declarations)
    assert all(name in output for name in ("propext", "Classical.choice", "Quot.sound"))

    for path in [*proof_paths, HERE / "check_proof.py", HERE / "PORT_PROVENANCE.md"]:
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1522 proof phase: ported bodies close both frozen packages and exact root")
    print("axioms: propext, Classical.choice, Quot.sound; no sorries")


if __name__ == "__main__":
    main()
