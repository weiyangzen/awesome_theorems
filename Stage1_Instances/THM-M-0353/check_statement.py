#!/usr/bin/env python3
"""Fail-closed source-level checks for the frozen THM-M-0353 statement."""

from hashlib import sha256
from pathlib import Path

path = Path(__file__).with_name("Statement.lean")
text = path.read_text(encoding="utf-8")

required = [
    "def HermiteCompletenessTarget : Prop :=",
    "Polynomial.hermite n",
    "Real.sqrt 2 * x",
    "Real.exp (-(x ^ 2 / 2))",
    "MemLp (hermiteFunction n) (2 : ENNReal) leb",
    "HilbertBasis Nat Complex (Lp Complex (2 : ENNReal) leb)",
    "mutationRemovedIntegrability",
    "mutationChangedDomain",
    "mutationChangedBinderScope",
    "mutationFiniteTruncation",
]
for needle in required:
    if needle not in text:
        raise SystemExit(f"missing frozen statement component: {needle}")

for forbidden in ("sorry", "admit", "axiom"):
    if forbidden in text:
        raise SystemExit(f"prohibited token in Statement.lean: {forbidden}")

print(f"statement source SHA-256: {sha256(text.encode()).hexdigest()}")
print("four structural mutations present and canonical components frozen")
