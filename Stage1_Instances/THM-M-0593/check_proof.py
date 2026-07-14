#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, and claim checks for THM-M-0593 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0593-PROOF"
THEOREM = "THM-M-0593"
BASE_REVISION = "718e166c56e53c552ebb861ee01427f9a606fc72"
BASE_TREE = "f2e15921b967c6f80b9e964361b684b5f9a011d9"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
REGISTRY_DENOMINATOR_SHA256 = (
    "ff56394a72695c35f72ed72fc1c961a3297943517a2e8b8056047678fb1157e2"
)
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
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 633
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["depends_on"] == ["S56-M-0593-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["state"] == "[ ]"
    assert item["deliverable"] == (
        "Implement or pin/import the required proof bodies without placeholders."
    )
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b|"
        r"\b(?:implemented_by|native_decide)\b",
        re.MULTILINE,
    )
    without_comments = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert prohibited.search(without_comments) is None
    for fragment in (
        "import ObligationTree",
        "theorem zeroCodomainBranch_proof : ZeroCodomainBranch",
        "Function.surjective_to_subsingleton",
        "theorem lowDimensionBranch_proof : LowDimensionBranch",
        "dimH_image_le_of_locally_lipschitzOn",
        "hausdorffMeasure_of_dimH_lt",
        "EuclideanSpace.euclideanHausdorffMeasure_eq_volume",
        "theorem sardTarget_of_hardDimensionBranch",
        "(hard : HardDimensionBranch) : SardTarget",
        "assert_no_sorry zeroCodomainBranch_proof",
        "#print sorries lowDimensionBranch_proof",
        "#print axioms sardTarget_of_hardDimensionBranch",
    ):
        assert fragment in proof, fragment

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""

    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["root_machine_debt"] == "M4"
    assert set(graphs["closure_boundary"]["remaining_root_cut_set"]) == {
        "M0593-L-DIMENSION-IMAGE",
        "M0593-L-RANK-REDUCTION",
        "M0593-L-TAYLOR",
    }

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["inputs"]["obligation_tree_sha256"] == sha256(
        HERE / "ObligationTree.lean"
    )
    assert receipt["inputs"]["obligation_registry_sha256"] == sha256(
        HERE / "obligation-registry.json"
    )
    assert receipt["inputs"]["typed_graphs_sha256"] == sha256(
        HERE / "typed-graphs.json"
    )
    assert set(receipt["closed_obligation_ids"]) == {
        "M0593-B-ZERO",
        "M0593-B-LOWDIM",
        "M0593-L-DIMENSION-IMAGE",
        "M0593-B-MERGE",
    }
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert set(receipt["remaining_root_cut_set_after"]) == {
        "M0593-L-RANK-REDUCTION",
        "M0593-L-TAYLOR",
    }

    assert blocker["proof_body_added"] is True
    assert blocker["first_failed_gate"].startswith("M0593-B-HARD")
    assert blocker["root_closed"] is blocker["theorem_complete"] is False
    assert set(blocker["remaining_root_cut_set"]) == {
        "M0593-L-RANK-REDUCTION",
        "M0593-L-TAYLOR",
    }

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

    print("PASS THM-M-0593 partial proof: two dimension branches checked")
    print("closed obligations: M0593-B-ZERO, M0593-L-DIMENSION-IMAGE, M0593-B-LOWDIM, M0593-B-MERGE")
    print("root closure: open (M2); theorem_complete=false")


if __name__ == "__main__":
    main()
