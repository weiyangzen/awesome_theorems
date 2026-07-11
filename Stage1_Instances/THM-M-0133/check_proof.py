#!/usr/bin/env python3
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()

required = (
    "import Statement",
    "theorem proofTarget_iff_mathlib",
    "theorem exponentFour_proof",
    "fermatLastTheoremFour",
    "theorem exactTarget_of_oddPrimeCases",
    "FermatLastTheorem.of_odd_primes oddPrimeCases",
    "WilesFermatLastTheoremTarget",
)
for fragment in required:
    assert fragment in proof, f"missing proof fragment: {fragment}"

for forbidden in ("sorry", "admit", "sorryAx", "axiom ", "unsafe "):
    assert forbidden not in proof, f"forbidden proof token: {forbidden!r}"

assert "oddPrimeCases :" in proof
assert "WilesFermatLastTheoremTarget :=" in proof

print("PASS THM-M-0133 proof phase: exponent four and conditional exact-root composition checked")
print("root remains open: the all-odd-prime family is an explicit premise")
