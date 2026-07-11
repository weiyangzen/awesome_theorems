#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0395 anchor audit."""

from pathlib import Path
import hashlib
import json
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_STATEMENT = "de1bfb399ccec48a224e867c55f6eab12589e458949d6d409260be65f0920ba6"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"anchor audit check failed: {message}")


require(AUDIT["item_id"] == "S56-M-0395-ANCHOR_AUDIT", "wrong item")
require(AUDIT["theorem_id"] == "THM-M-0395", "wrong theorem")
require(AUDIT["environment"]["mathlib_revision"] == EXPECTED_MATHLIB, "mathlib pin drift")
require(hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == EXPECTED_STATEMENT,
        "canonical statement drift")
require(AUDIT["audit_complete"] is True, "audit is not closed")
require(AUDIT["theorem_complete"] is False, "audit claims theorem completion")
require(AUDIT["accepted_receipts"] == [], "worker invented accepted receipts")
require(AUDIT["negative_results"]["exhaustive_public_search_claimed"] is False,
        "search boundary was broadened")
require(all(candidate["exact_root_closed"] is False for candidate in AUDIT["candidates"]),
        "candidate ledger contradicts root decision")
require(AUDIT["root_decision"]["kernel_closed"] is False, "root incorrectly closed")

head = subprocess.run(
    ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages/mathlib"),
     "rev-parse", "HEAD"], check=True, text=True, capture_output=True
).stdout.strip()
require(head == EXPECTED_MATHLIB, "checked-out mathlib does not match pin")

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
checks = {
    "Mathlib/AlgebraicGeometry/Morphisms/Smooth.lean": "class Smooth",
    "Mathlib/AlgebraicGeometry/Morphisms/Proper.lean": "class IsProper",
    "Mathlib/NumberTheory/Height/Northcott.lean": "class Northcott",
    "Mathlib/GroupTheory/Descent.lean": "fg_of_descent'",
    "docs/1000.yaml": "title: Faltings's theorem",
}
for relative, witness in checks.items():
    require(witness in (mathlib / relative).read_text(), f"missing pinned witness: {witness}")

legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_008.lean").read_text()
require("def externalPrimarySourceAuditFoundTerminalFaltingsProof : Bool :=\n  false" in legacy,
        "legacy discovery boundary changed")

print("anchor audit check: ok; immutable mathlib pin and 7 non-closing candidates verified")
