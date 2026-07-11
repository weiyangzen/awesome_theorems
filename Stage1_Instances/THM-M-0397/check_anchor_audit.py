#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0397 anchor audit."""

from pathlib import Path
import hashlib
import json
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MATHLIB_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
STATEMENT_SHA = "78327c7641064bddbf5acb119253a5956e27c78a5c69b3fc04de7563b055c07f"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"anchor audit check failed: {message}")


require(AUDIT["item_id"] == "S56-M-0397-ANCHOR_AUDIT", "wrong item")
require(AUDIT["theorem_id"] == "THM-M-0397", "wrong theorem")
require(AUDIT["environment"]["mathlib_revision"] == MATHLIB_REV, "mathlib pin drift")
require(hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == STATEMENT_SHA,
        "canonical statement drift")
decision = AUDIT["decision"]
require(decision["audit_complete_for_phase"] is True, "phase audit is open")
require(decision["audit_complete_for_theorem"] is False, "whole audit incorrectly closed")
require(decision["theorem_complete"] is False, "theorem incorrectly closed")
require(decision["proof_credit"] is False, "audit claimed proof credit")
require(decision["accepted_receipts"] == [], "worker invented accepted receipts")
require(all(row["exact_root_closed"] is False for row in AUDIT["candidates"]),
        "candidate ledger contradicts root decision")

head = subprocess.run(
    ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages/mathlib"),
     "rev-parse", "HEAD"], check=True, text=True, capture_output=True
).stdout.strip()
require(head == MATHLIB_REV, "checked-out mathlib does not match pin")

filter_source = ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Data/Finset/Filter.lean"
require("theorem mem_filter" in filter_source.read_text(), "pinned Finset.mem_filter missing")
legacy = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_010.lean"
require("does not claim a kernel-checked proof of Baker's" in legacy.read_text(),
        "legacy non-completion boundary changed")

print("anchor audit check: ok; immutable pin and three non-closing candidates verified")
