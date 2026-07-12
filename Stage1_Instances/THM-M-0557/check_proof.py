#!/usr/bin/env python3
"""Fail-closed source and exact-expression checks for S56-M-0557-PROOF."""

from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
statement = (HERE / "Statement.lean").read_text()

for pattern in (r"\bsorry\b", r"\badmit\b", r"^\s*axiom\b", r"\bsorryAx\b", r"^\s*unsafe\b"):
    assert re.search(pattern, proof, re.MULTILINE) is None, pattern

target = re.search(
    r"def HomotopyGroupStructureTarget : Prop :=\n(?P<body>.*?)\n\n-- Separately",
    statement,
    re.DOTALL,
)
proved = re.search(
    r"theorem homotopyGroupStructureTarget :\n(?P<body>.*?) := by",
    proof,
    re.DOTALL,
)
assert target and proved
normalize = lambda value: "".join(value.split())
assert normalize(target.group("body")) == normalize(proved.group("body"))

for declaration in (
    "theorem groupStructureBranch",
    "theorem commutativeStructureBranch",
    "theorem homotopyGroupStructureTarget",
    "#print axioms homotopyGroupStructureTarget",
):
    assert declaration in proof

print("PASS THM-M-0557 proof: exact frozen expression and both structure branches implemented")
