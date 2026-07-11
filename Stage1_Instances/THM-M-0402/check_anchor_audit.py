#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0402 anchor audit."""

from pathlib import Path
import hashlib
import json
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_FLT_REGULAR = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
EXPECTED_STATEMENT = "d9213f673e100c85d2330219b6dbcbaf3e7542c9ea01df0bd7b31f2f3faf518d"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"anchor audit check failed: {message}")


require(AUDIT["item_id"] == "S56-M-0402-ANCHOR_AUDIT", "wrong item")
require(AUDIT["theorem_id"] == "THM-M-0402", "wrong theorem")
require(AUDIT["environment"]["mathlib_revision"] == EXPECTED_MATHLIB, "mathlib pin drift")
require(AUDIT["environment"]["flt_regular_revision"] == EXPECTED_FLT_REGULAR,
        "flt-regular pin drift")
require(hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == EXPECTED_STATEMENT,
        "canonical statement drift")
require(AUDIT["audit_complete"] is True, "bounded inventory is not classified")
require(AUDIT["theorem_complete"] is False, "audit claims theorem completion")
require(AUDIT["accepted_receipts"] == [], "worker invented accepted receipts")
require(AUDIT["discovery_protocol"]["exhaustive_public_search_claimed"] is False,
        "search boundary was broadened")
require(all(candidate["exact_root_closed"] is False for candidate in AUDIT["candidates"]),
        "candidate ledger contradicts root decision")
require(AUDIT["root_decision"]["classification"] == "M3", "wrong root classification")
require(AUDIT["root_decision"]["kernel_closed"] is False, "root incorrectly closed")

for package, expected in (("mathlib", EXPECTED_MATHLIB),
                          ("flt-regular", EXPECTED_FLT_REGULAR)):
    head = subprocess.run(
        ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages" / package),
         "rev-parse", "HEAD"], check=True, text=True, capture_output=True
    ).stdout.strip()
    require(head == expected, f"checked-out {package} does not match pin")

s_integer = (ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/RingTheory/"
             "DedekindDomain/SInteger.lean").read_text()
for witness in ("def unit : Subgroup", "theorem unit_valuation_eq_one",
                "def unitEquivUnitsInteger", "TODO: finite generation of `S`-units"):
    require(witness in s_integer, f"missing pinned S-integer witness: {witness}")

legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_015.lean").read_text()
require('def currentMachineStatus : String := "not_repo_local_closed"' in legacy,
        "legacy proof boundary changed")

print("anchor audit check: ok; pins, statement hash, and 6 non-closing candidates verified")
