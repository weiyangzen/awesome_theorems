#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-0082 proof phase."""

from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()

assert "S56-M-0082-PROOF" not in proof  # item metadata stays outside Lean code
assert "GeneralRightAdjointBridge.{vC, vD, uC, uD}" in proof
assert "GeneralRightAdjointTarget.{vC, vD, uC, uD}" in proof
assert "isRightAdjoint_of_preservesLimits_of_solutionSetCondition" in proof
assert "root_of_bridge generalRightAdjointBridge" in proof
assert "#print axioms generalRightAdjointBridge" in proof
assert "#print axioms generalRightAdjointTarget" in proof

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|(?:^|\s)axiom\s", re.MULTILINE)
assert prohibited.search(proof) is None

print("PASS THM-M-0082 proof source: exact bridge and root composition present")
