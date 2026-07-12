#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-1245-PROOF."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
validation = (HERE / "proof-validation.md").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for declaration in (
    "theorem auditedTerminalEstimate_proof",
    "theorem sobolevInequalityTarget_proof",
    "eLpNorm_le_eLpNorm_fderiv_of_eq_inner",
    "root_of_audited_terminal_estimate auditedTerminalEstimate_proof",
    "#print axioms auditedTerminalEstimate_proof",
    "#print axioms sobolevInequalityTarget_proof",
):
    assert declaration in proof
assert "M1245-A-TERMINAL" in validation
assert "does not claim theorem completion" in validation
print("PASS THM-M-1245 proof phase: terminal and exact root proof bodies installed")
