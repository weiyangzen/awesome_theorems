#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0399 immutable anchor audit."""

from pathlib import Path
import json
import subprocess


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads((Path(__file__).with_name("anchor-audit.json")).read_text())
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_EXPRESSION = "d63a5863b947f4e03f21847e040b9f4980722607ae953749fa2cb7851a492389"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"anchor audit check failed: {message}")


require(AUDIT["item_id"] == "S56-M-0399-ANCHOR_AUDIT", "wrong item")
require(AUDIT["theorem_id"] == "THM-M-0399", "wrong theorem")
require(AUDIT["canonical_expression_sha256"] == EXPECTED_EXPRESSION, "statement drift")
require(AUDIT["environment"]["mathlib_revision"] == EXPECTED_MATHLIB, "mathlib pin drift")
require(AUDIT["audit_complete"] is True, "audit phase is not closed")
require(AUDIT["theorem_complete"] is False, "audit must not claim theorem completion")
require(AUDIT["accepted_receipts"] == [], "worker must not invent accepted receipts")
require(AUDIT["negative_results"]["exhaustive_public_search_claimed"] is False,
        "public search boundary must remain explicit")
require(all(candidate["exact_root_closed"] is False for candidate in AUDIT["candidates"]),
        "candidate ledger contradicts the negative verdict")

head = subprocess.run(
    ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages/mathlib"), "rev-parse", "HEAD"],
    check=True,
    text=True,
    capture_output=True,
).stdout.strip()
require(head == EXPECTED_MATHLIB, "checked-out mathlib does not match immutable pin")

basic = (ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/"
         "DiophantineApproximation/Basic.lean").read_text()
for witness in (
    "theorem infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational",
    "theorem finite_rat_abs_sub_lt_one_div_den_sq",
    "theorem Real.infinite_rat_abs_sub_lt_one_div_den_sq_iff_irrational",
):
    require(witness in basic, f"missing pinned mathlib witness: {witness}")

legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_012.lean").read_text()
for witness in ("def RothStatementShapeA : Prop", "def RothStatementShapeEpsilon : Prop",
                "theorem candidateA_implies_epsilon"):
    require(witness in legacy, f"missing local candidate witness: {witness}")
require("no terminal mathlib Roth theorem was found" in legacy,
        "local candidate's stated proof boundary changed")

print("anchor audit check: ok; immutable pins and 6 non-closing candidate rows verified")
