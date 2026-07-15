#!/usr/bin/env python3
"""Fail-closed source and receipt checks for the THM-M-0321 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0321-PROOF"
THEOREM = "THM-M-0321"
BASE_REVISION = "5bb515438bd0e1d53584e5243c5d434dfde7158e"
BASE_TREE = "8055b8d863f0978f110a628ab3ccc7ab1e146b12"
STATEMENT_EXPRESSION_SHA256 = "7a9628fca04eb72d787efad1f852517f4385377b3ad16f3eba662ccea4bb86a5"
REGISTRY_DENOMINATOR = "9963eb2002e7418a51e79b3ed2dd651e2c29a701cdfa1e18f47123041207f9ac"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SUPPORTED_IDS = [
    "M0321-ROOT",
    "M0321-N-FINITE",
    "M0321-B-FINITE-EMPTY",
    "M0321-B-FINITE-INSERT",
    "M0321-B-RECOMPOSE",
    "M0321-C-FIXSET",
    "M0321-C-RESTRICT",
    "M0321-C-AVERAGE",
    "M0321-C-FIP",
    "M0321-L-SINGLE",
    "M0321-L-AVERAGE-IN-K",
    "M0321-L-AVERAGE-DEFECT",
    "M0321-L-CLUSTER",
    "M0321-L-FIXSET-COMPACT",
    "M0321-L-FIXSET-CONVEX",
    "M0321-L-COMMUTE-INVARIANT",
    "M0321-L-FIP-COMPACT",
    "M0321-T-FINITE",
    "M0321-T-ASSEMBLE",
]
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
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 687
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["depends_on"] == ["S56-M-0321-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["state"] == "[ ]"
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    without_comments = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert prohibited.search(without_comments) is None
    for fragment in (
        "theorem isClosed_fixedSetWithin",
        "theorem isCompact_fixedSetWithin",
        "theorem convex_fixedSetWithin",
        "theorem mapsTo_fixedSetWithin_of_commute",
        "noncomputable def cesaroAverage",
        "theorem cesaroAverage_mem",
        "theorem tendsto_cesaro_defect_zero",
        "theorem singleMap_fixedPoint",
        "theorem finiteFamilyStep : ObligationTree.FiniteFamilyStep",
        "theorem continuousCompactnessUpgrade",
        "hCompact.inter_iInter_nonempty",
        "theorem markovKakutani_of_finiteFamily",
        "theorem markovKakutani_proof : MarkovKakutaniTarget",
    ):
        assert fragment in proof, fragment

    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR
    assert registry["frozen_against_statement_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert graphs["closure_boundary"]["closed_obligations"] == []
    assert graphs["closure_boundary"]["root_machine_debt"] == "M3"
    assert graphs["closure_boundary"]["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), filename
    assert receipt["supported_obligation_ids"] == SUPPORTED_IDS
    assert receipt["provisionally_closed_obligation_ids"] == SUPPORTED_IDS
    assert receipt["result"]["root_closed"] is True
    assert receipt["result"]["root_machine_classification_after_proposed"] == "M0-L"
    assert receipt["result"]["theorem_complete"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    assert blocker["outcome"] == "exact_root_kernel_closed_frozen_helper_defect_recorded"
    assert blocker["proof_body_added"] is True
    assert blocker["supported_obligation_ids"] == SUPPORTED_IDS
    assert blocker["provisionally_closed_obligation_ids"] == SUPPORTED_IDS
    assert blocker["root_closed"] is True and blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == ["M0321-T-UPGRADE"]

    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual = {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0321 proof artifacts: exact root kernel closure checked")
    print("frozen proof obligations provisionally supported:", len(SUPPORTED_IDS))
    print("root closure: provisional M0-L candidate; theorem_complete=false")


if __name__ == "__main__":
    main()
