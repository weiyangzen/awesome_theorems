#!/usr/bin/env python3
"""Fail-closed checks for the truthful THM-M-0399 proof-phase receipt."""

from pathlib import Path
import json
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RECEIPT = json.loads((HERE / "proof-phase.json").read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"proof phase check failed: {message}")


require(RECEIPT["item_id"] == "S56-M-0399-PROOF", "wrong item")
require(RECEIPT["theorem_id"] == "THM-M-0399", "wrong theorem")
require(RECEIPT["theorem_complete"] is False, "open Roth proof reported complete")
require(RECEIPT["phase_self_tested"] is True, "proof-phase audit not self-tested")
require(RECEIPT["closed_obligation_ids"] == ["M0399-ROOT-COMPOSE"],
        "unexpected proof credit")
require("M0399-STRONG-FINITE" in RECEIPT["remaining_root_cut_set"],
        "central formalization debt omitted")

source = (HERE / "RothComposition.lean").read_text()
for forbidden in (r"\bsorry\b", r"\baxiom\b", r"\badmit\b"):
    require(re.search(forbidden, source) is None, f"forbidden token matches {forbidden}")
require("theorem rothStatement_of_strongFinite" in source, "composition body missing")

statement = (HERE / "RothStatement.lean").read_text()
exceptional_pattern = (
    r"def exceptionalRationals \(alpha epsilon : ℝ\) : Set ℚ :=\s*"
    r"\{x \| \|alpha - \(x : ℝ\)\| < Real\.rpow \(x\.den : ℝ\) \(-\(2 \+ epsilon\)\)\}"
)
root_pattern = (
    r"def RothStatement : Prop :=\s*"
    r"∀ \(alpha : ℝ\), IsAlgebraic ℚ alpha → Irrational alpha →\s*"
    r"∀ \(epsilon : ℝ\), 0 < epsilon → \(exceptionalRationals alpha epsilon\)\.Finite"
)
for name, text in (("frozen statement", statement), ("composition target", source)):
    require(re.search(exceptional_pattern, text) is not None, f"{name} exceptional set drift")
    require(re.search(root_pattern, text) is not None, f"{name} root drift")

lean = subprocess.run(
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0399/RothComposition.lean"],
    cwd=ROOT / "Formalizations" / "Lean",
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
require(lean.returncode == 0, f"Lean replay failed:\n{lean.stdout}")
require("rothStatement_of_strongFinite" in lean.stdout, "checked declaration not printed")

print("proof phase check: ok; 1 composition body closed, exact Roth root remains open")
