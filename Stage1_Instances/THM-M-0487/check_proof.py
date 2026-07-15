#!/usr/bin/env python3
"""Fail-closed source and evidence checks for S56-M-0487-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0487-PROOF"
THEOREM = "THM-M-0487"
BASE_REVISION = "ec3b52a20f5e28de012c23dce1af403343b9a1cb"
BASE_TREE = "b08b83715d8f74868d1f31bbe82a7951b26edad1"
DENOMINATOR_SHA256 = "1d456b6ecd31a58a47bac58a2746bc0f8d16ce4b4e2821348331c511e21c1a41"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
PARTIAL_PROGRESS_IDS = ["M0487-N-REPRESENTATION"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation-current.md",
    f"Stage1_Instances/{THEOREM}/proof-blocker-current.json",
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
    blocker = load(HERE / "proof-blocker-current.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1366
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0487-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"]
        if row["id"] == "S56-M-0487-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "def primeTriples",
        "def representationCount",
        "theorem representationCount_pos_iff",
        "def PositiveRepresentationCountTarget",
        "theorem weakGoldbachTarget_iff_positiveRepresentationCountTarget",
        "#print sorries weakGoldbachTarget_iff_positiveRepresentationCountTarget",
    ):
        assert marker in proof, marker
    assert "theorem weakGoldbachTarget_proof" not in proof

    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    status = registry["status_observed_after_freeze"]
    assert status["root_machine_debt"] == "M3"
    assert status["accepted_closed_obligations"] == []
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["minimal_open_proof_cut_sets"] == [[
        "M0487-T-ANALYTIC", "M0487-T-FINITE-UPPER"
    ]]
    assert closure["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["proof_body"]["classification"] == "local_proof_body_partial_interface"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation-current.md"),
        ("proof_blocker_sha256", "proof-blocker-current.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    result = receipt["result"]
    assert result["root_kernel_closed"] is False
    assert result["root_closed"] is False
    assert result["audit_complete"] is False
    assert result["theorem_complete"] is False
    assert receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == [
        "M0487-T-ANALYTIC", "M0487-T-FINITE-UPPER"
    ]
    recipe = receipt["recipe"]
    assert recipe["recipe_id"] == "VAL-M0487-PROOF-PARTIAL-COUNT-v1"
    assert recipe["cwd"] == "."
    assert recipe["argv"] == ["bash", "Stage1_Instances/THM-M-0487/check_proof.sh"]
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == []
    assert recipe["covered_declarations"] == receipt["exact_declarations"]

    assert blocker["proof_body_added"] is True
    assert blocker["partial_proof_receipt_id"] == receipt["receipt_id"]
    assert blocker["supported_obligation_ids"] == []
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert blocker["root_closed"] is False
    assert blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        packet = load(selftest_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        worktree = subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=ROOT,
            text=True,
        )
        actual_changes = {
            line[3:] for line in worktree.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    validation = (HERE / "proof-validation-current.md").read_text(encoding="utf-8")
    assert "zero frozen obligations are claimed closed" in validation
    assert "not theorem completion" in validation
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0487 proof evidence: hashes, pin, partial scope, and open-root boundary agree")


if __name__ == "__main__":
    main()
