#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0982-PROOF."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof

for required in (
    "import Statement",
    "theorem continuityFromBelow : ContinuityFromBelowTarget.{u}",
    "theorem continuityFromAbove : ContinuityFromAboveTarget.{u}",
    "theorem probabilityContinuity : ProbabilityContinuityTarget.{u}",
    "tendsto_measure_iUnion_atTop",
    "tendsto_measure_iInter_atTop",
    "nullMeasurableSet",
    "measure_ne_top",
    "#print axioms probabilityContinuity",
):
    assert required in proof

print("PASS THM-M-0982 proof phase: exact frozen target has a placeholder-free proof body")
