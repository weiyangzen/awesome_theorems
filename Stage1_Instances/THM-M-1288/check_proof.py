#!/usr/bin/env python3
"""Fail-closed source/evidence checks for S56-M-1288-PROOF."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
validation = (HERE / "proof-validation.md").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof
for declaration in (
    "theorem domain_facts",
    "theorem norm_gradient_eq_norm_fderiv",
    "theorem vectorLpNorm_gradient_eq_fderiv",
    "theorem lpNorm_zero",
    "theorem vectorLpNorm_gradient_zero",
    "theorem zero_test_function_branch",
    "theorem talentiSharpSobolevTarget_of_open_analytic_packages",
):
    assert declaration in proof
assert "TalentiAdmissibilityPackage" in proof
assert "TalentiOptimalityPackage" in proof
assert "root remains open" in validation
assert "M1288-N-REARRANGEMENT" in validation
print(
    "PASS THM-M-1288 proof phase: domain, gradient transport, and zero branch "
    "closed; root remains conditional"
)
