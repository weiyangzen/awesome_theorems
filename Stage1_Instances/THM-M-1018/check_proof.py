#!/usr/bin/env python3
"""Fail-closed checks for the THM-M-1018 partial proof receipt."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1018-PROOF"
THEOREM = "THM-M-1018"
BASE = "00f98378e8c1c63097871ae62aeed895d83b0cb4"
BASE_TREE = "4f2396db6d6d1c2b9948f401079f136dd0ed8f16"
DENOMINATOR = "c5662da4255541baea4a76c8de113b36bfb571e2b65376597ad2bcc8cf13d6c2"
MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
RECEIPT_NAME = "proof-receipt-2026-07-15-head-00f98378.json"
CHANGED = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-execution-2026-07-15-head-00f98378.md",
    f"Stage1_Instances/{THEOREM}/{RECEIPT_NAME}",
}
DECLARATIONS = {
    "frontier_Ioc_null",
    "tendsto_Ioc_mass_of_tendsto",
    "measureReal_Icc_eq_Ioc",
    "measureReal_Ioo_eq_Ioc",
    "interval_mass_of_weak_limit",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / RECEIPT_NAME)
    packet = load(ROOT / ".stage1-worker-selftest.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 494
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1018-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert git("rev-parse", "HEAD") == BASE
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        assert prohibited.search((HERE / name).read_text(encoding="utf-8")) is None, name
    declared = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", proof, re.MULTILINE))
    assert declared == DECLARATIONS, (declared, DECLARATIONS)
    assert proof.count("#print axioms") == len(DECLARATIONS)

    assert registry["denominator_sha256"] == DENOMINATOR
    assert graphs["registry_denominator_sha256"] == DENOMINATOR
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is boundary["theorem_complete"] is False
    assert boundary["remaining_root_cut_set"] == ["M1018-T-ANALYTIC"]

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["registry_denominator_sha256"] == DENOMINATOR
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for name, digest in receipt["inputs"].items():
        assert sha256(HERE / name) == digest, name
    receipt_declarations = {name.rsplit(".", 1)[-1] for name in receipt["exact_declarations"]}
    assert receipt_declarations == DECLARATIONS
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == ["M1018-T-ANALYTIC"]

    assert packet["state"] == "[_]"
    assert packet["known_failures"] == [
        "The five bodies do not inhabit LevyInversionTarget or close a whole frozen obligation.",
        "M1018-T-ANALYTIC remains the root cut; M1018-L-DIRICHLET is the first unavailable sharp analytic package.",
        "Accepted state remains [ ]; accepted root remains H2/M3/R4; audit and theorem completion remain false.",
        "The untracked canonical .lake link makes the replay nonrelease evidence.",
    ]
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED
    assert packet["output_summary"].startswith(
        "PASS: five placeholder-free endpoint and conditional weak-limit bodies"
    )
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED, (actual, CHANGED)

    for relative in CHANGED:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1018 proof evidence: 5 placeholder-free partial bodies")
    print("closed frozen obligations: none; root cut M1018-T-ANALYTIC remains open")
    print("root closure: open (M3); theorem_complete=false")


if __name__ == "__main__":
    main()
