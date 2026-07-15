#!/usr/bin/env python3
"""Fail-closed source and evidence checks for S56-M-1085-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1085-PROOF"
THEOREM = "THM-M-1085"
BASE_REVISION = "3d3099d0d4002093cf89da97132bdf954605810b"
BASE_TREE = "17ea0daeddceb9742a5df33c247d624d2842c520"
DENOMINATOR = "c0367c009b2f628b52c7cf782f7785730d0207f7e90ec30afa47c1523a8a4dc4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
OWNED_CHANGED = {
    f"Stage1_Instances/{THEOREM}/LawReduction.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/check_obligation_tree.py",
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
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 527
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1085-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    source = HERE / "LawReduction.lean"
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(source.read_text(encoding="utf-8"))) is None
    markers = (
        "theorem map_apply_belowAllRange",
        "theorem map_toLp_apply_belowAllEuclidean",
        "theorem pushforward_hasLaw",
        "theorem covariance_coordinate_map",
        "theorem covarianceMatrix_posSemidef",
        "theorem covarianceMatrix_order_data",
        "theorem belowAll_eq_multivariateGaussian",
        "theorem gaussian_law_eq_multivariateGaussian",
        "def LawSlepianTarget : Prop",
        "theorem slepianTarget_of_law",
        "#print sorries gaussian_law_eq_multivariateGaussian",
        "#print sorries slepianTarget_of_law",
    )
    text = source.read_text(encoding="utf-8")
    assert all(marker in text for marker in markers)

    graphs = load(HERE / "typed-graphs.json")
    assert graphs["registry_denominator_sha256"] == DENOMINATOR
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is False and closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M4"
    assert closure["remaining_root_cut_set"] == [
        "M1085-N-LAWS", "M1085-C-INTERPOLATION", "M1085-L-INTERPOLATION-ID",
        "M1085-L-MIXED-SIGN", "M1085-L-LIMIT",
    ]

    receipt = load(HERE / "proof-receipt.json")
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["accepted"] is False and receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["partial_progress_toward_obligation_ids"] == [
        "M1085-N-LAWS", "M1085-N-MATRIX"
    ]
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["proof_source"]["sha256"] == sha256(source)
    for row in receipt["frozen_inputs"]:
        assert row["sha256"] == sha256(ROOT / row["path"]), row["path"]
    for row in receipt["validation_sources"]:
        relative = row["path"]
        if "sha256" not in row:
            assert Path(relative).name == "check_proof.py"
            continue  # A validator cannot content-address itself without a fixed-point scheme.
        assert row["sha256"] == sha256(ROOT / relative), relative
    expected_changed = OWNED_CHANGED | {".stage1-worker-selftest.json"}
    assert set(receipt["changed_paths"]) == expected_changed

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
    assert set(packet["changed_paths"]) == expected_changed
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
    assert actual == expected_changed, (actual, expected_changed)

    for relative in expected_changed:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1085 proof evidence: exact reductions, hashes, pin, and open root agree")


if __name__ == "__main__":
    main()
