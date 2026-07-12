#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1111 statement node."""

from pathlib import Path
import hashlib
import re
import sys

root = Path(__file__).resolve().parent
source = (root / "Statement.lean").read_text()

required = [
    "∃ c0 : ℝ, 0 < c0",
    "∀ ε : ℝ, 0 < ε → ε < 1",
    "∀ k : Nat, 1 ≤ k",
    "S.offDiagonalMatch M M' i j 4",
    "S.diagonalMatch M M' i 2",
    "derivativeOrder ≤ 5",
    "StrictMono" if False else "r < s → (indices r).val < (indices s).val",
    "ε * (n : ℝ)",
    "S.powerBound n (-c0)",
]
for fragment in required:
    if fragment not in source:
        sys.exit(f"missing canonical fragment: {fragment}")

for mutation in [
    "mutationOffDiagonalOrderThree",
    "mutationNoBulkRestriction",
    "mutationDiagonalOrderFour",
]:
    if not re.search(rf"def {mutation}\b", source):
        sys.exit(f"missing mutation: {mutation}")

# The statement phase may declare propositions, but it must not smuggle proof gaps.
forbidden = re.compile(r"\b(sorry|admit|axiom)\b")
code = "\n".join(line.split("--", 1)[0] for line in source.splitlines())
if forbidden.search(code):
    sys.exit("forbidden proof-gap declaration")

print("statement structural check: ok")
print("statement sha256:", hashlib.sha256(source.encode()).hexdigest())
