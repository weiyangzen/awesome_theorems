#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0536-PROOF."""

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
target = (HERE / "Target.lean").read_text()
receipt = (HERE / "proof-receipt.json").read_text()

for token in ("sorry", "admit", "axiom ", "sorryAx", "unsafe"):
    assert token not in proof, f"prohibited token in Proof.lean: {token}"
for declaration in (
    "theorem induced_left_identity",
    "theorem induced_right_identity",
    "theorem homotopyInvariance : HomotopyInvarianceStatement",
    "#print axioms homotopyInvariance",
):
    assert declaration in proof, f"missing declaration: {declaration}"

target_body = target.split("def HomotopyInvarianceStatement : Prop :=", 1)[1].split(
    "#check HomotopyInvarianceStatement", 1
)[0].strip()
proof_body = proof.split("def HomotopyInvarianceStatement : Prop :=", 1)[1].split(
    "/-- The forward-then-inverse", 1
)[0].strip()
assert target_body == proof_body, "Proof.lean target differs from frozen Target.lean"

proof_sha = hashlib.sha256((HERE / "Proof.lean").read_bytes()).hexdigest()
assert proof_sha in receipt, "receipt does not bind the current Proof.lean"
print(
    "PASS THM-M-0536 proof phase: exact root and both induced inverse laws closed; "
    f"proof_sha256={proof_sha}"
)
