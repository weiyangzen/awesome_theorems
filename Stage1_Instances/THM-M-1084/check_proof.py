#!/usr/bin/env python3
"""Fail-closed source and evidence checks for S56-M-1084-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1084-PROOF"
THEOREM = "THM-M-1084"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
DENOMINATOR = "a2bf7a0e46b0ca64f3ce1259043f8e1f7c85975bb4762a9e2a5256709555111a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
OWNED_CHANGED = {
    f"Stage1_Instances/{THEOREM}/GaussianMGFBridge.lean",
    f"Stage1_Instances/{THEOREM}/CoveringNets.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-attempt.json",
    f"Stage1_Instances/{THEOREM}/proof-blocker.md",
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
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 526
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1084-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    sources = [HERE / "GaussianMGFBridge.lean", HERE / "CoveringNets.lean"]
    for path in sources:
        assert prohibited.search(without_comments(path.read_text(encoding="utf-8"))) is None

    mgf = sources[0].read_text(encoding="utf-8")
    nets = sources[1].read_text(encoding="utf-8")
    for marker in (
        "theorem increment_hasGaussianLaw",
        "theorem hasSubgaussianMGF_of_hasGaussianLaw_of_integral_eq_zero",
        "theorem increment_mgf_eq_dist_sq",
        "theorem increment_hasSubgaussianMGF",
        "theorem gaussianIncrementMGFPackage",
        "#print sorries increment_hasSubgaussianMGF",
    ):
        assert marker in mgf, marker
    for marker in (
        "theorem exists_openBallCover",
        "theorem exists_minimal_openBallCover",
        "theorem coveringNumber_pos",
        "#print sorries coveringNumber_pos",
    ):
        assert marker in nets, marker

    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    assert registry["denominator_sha256"] == DENOMINATOR
    assert graphs["registry_denominator_sha256"] == DENOMINATOR
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == [
        "M1084-T-INTEGRABLE", "M1084-T-ENTROPY"
    ]
    assert graphs["closure_boundary"]["theorem_complete"] is False

    attempt = load(HERE / "proof-attempt.json")
    receipt = load(HERE / "proof-receipt.json")
    assert attempt["item_id"] == receipt["item_id"] == ITEM
    assert attempt["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert attempt["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert attempt["provisionally_closed_obligations"] == ["M1084-N-GAUSSIAN-MGF"]
    assert receipt["supported_obligation_ids"] == ["M1084-N-GAUSSIAN-MGF"]
    assert receipt["accepted"] is False and receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["proof_sources"][0]["sha256"] == sha256(sources[0])
    assert receipt["proof_sources"][1]["sha256"] == sha256(sources[1])
    expected_owned_changed = OWNED_CHANGED | {".stage1-worker-selftest.json"}
    assert set(receipt["changed_paths"]) == expected_owned_changed

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == expected_owned_changed
    assert packet["known_failures"] == receipt["known_failures"]

    status = subprocess.check_output(
        [
            "git", "status", "--short", "--untracked-files=all", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
        ],
        cwd=ROOT,
        text=True,
    )
    actual = {line[3:] for line in status.splitlines()}
    assert actual == expected_owned_changed, (actual, expected_owned_changed)

    for relative in expected_owned_changed:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1084 proof evidence: exact partial bodies, hashes, pin, and open root agree")


if __name__ == "__main__":
    main()
