#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-1248-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1248-PROOF"
THEOREM = "THM-M-1248"
BASE = "80f0191c83a1bb4026c2d490be957cf109464de1"
MATHLIB_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


proof_path = HERE / "Proof.lean"
source = proof_path.read_text(encoding="utf-8")
scannable = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
scannable = re.sub(r"--.*", "", scannable)
forbidden = re.compile(
    r"\b(sorry|admit|sorryAx|axiom|unsafe|implemented_by|native_decide|extern|opaque)\b"
)
assert forbidden.search(scannable) is None

for marker in (
    "import Mathlib.Analysis.Analytic.Uniqueness",
    "theorem compactlySupported_analytic_eq_zero",
    "hu.analyticOnNhd",
    "notMem_tsupport_iff_eventuallyEq.mp hz",
    "theorem caffarelliKohnNirenbergTarget : CaffarelliKohnNirenbergTarget",
    "#print axioms caffarelliKohnNirenbergTarget",
    "#print sorries caffarelliKohnNirenbergTarget",
):
    assert marker in source, marker

receipt = load(HERE / "proof-receipt.json")
assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["base_revision"] == BASE
assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
assert receipt["proof_body"]["source_sha256"] == sha(proof_path)
assert receipt["inputs"]["statement_sha256"] == sha(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_tree_sha256"] == sha(HERE / "ObligationTree.lean")
assert receipt["inputs"]["obligation_registry_sha256"] == sha(
    HERE / "obligation-registry.json"
)
assert receipt["inputs"]["typed_graphs_sha256"] == sha(HERE / "typed-graphs.json")
assert receipt["result"]["exact_frozen_root_kernel_closed"] is True
assert receipt["result"]["source_claim_proved"] is False
assert receipt["result"]["theorem_complete"] is False
assert receipt["debt_vector"]["proposed_after_proof_master_acceptance"]["M"] == "M5"
assert receipt["first_failed_completion_gate"] == (
    "S56-5.1-EXACT-TARGET-IDENTITY-OR-TRANSPORT"
)
reason = receipt["debt_vector"]["proposal_reason"]
assert "analytic order omega rather than smooth order infinity" in reason
assert "Pi/sup and Euclidean/L2" in reason

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True
).strip() == MATHLIB_REV

selftest = load(ROOT / ".stage1-worker-selftest.json")
assert set(selftest) == {
    "item_id",
    "changed_paths",
    "commands",
    "output_summary",
    "base_revision",
    "known_failures",
    "state",
}
assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
assert selftest["base_revision"] == BASE
assert selftest["changed_paths"] == receipt["changed_paths"]
assert selftest["known_failures"] == receipt["known_failures"]

status = subprocess.check_output(
    ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
)
actual_changes = {
    line[3:]
    for line in status.splitlines()
    if line[3:] != "Formalizations/Lean/.lake"
}
assert actual_changes == set(selftest["changed_paths"]), (
    actual_changes,
    set(selftest["changed_paths"]),
)

print("PASS THM-M-1248 proof packet: exact frozen root has a local proof body")
print(f"proof source sha256: {sha(proof_path)}")
print("source theorem rejected: statement mismatch keeps machine status at M5")
