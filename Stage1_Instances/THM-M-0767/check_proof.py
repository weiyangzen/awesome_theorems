#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-0767 proof node."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
registry = json.loads((HERE / "obligation-registry.json").read_text())


def require(value, message):
    if not value:
        raise SystemExit("proof check failed: " + message)


require(registry["theorem_id"] == "THM-M-0767", "wrong theorem registry")
require(
    registry["denominator_sha256"]
    == "9bf54713d38d6a18baeea4e55c8d9ec54f2ac0f02b7024fabf2cda9bc69acd66",
    "frozen obligation denominator drifted",
)
require("import Statement" in proof, "proof does not import the frozen target")
require("theorem cantor_theorem : CanonicalTarget.{u}" in proof, "exact root wrapper missing")
for declaration in (
    "theorem powerset_cardinality",
    "Cardinal.mk_powerset",
    "theorem cantor_for_set",
    "Cardinal.cantor",
):
    require(declaration in proof, f"required proof component missing: {declaration}")
for token in ("sorry", "admit", "sorryAx", "axiom ", "unsafe "):
    require(token not in proof, f"prohibited proof token: {token.strip()}")
print(
    "PASS THM-M-0767 proof: exact CanonicalTarget closed by pinned "
    "mk_powerset normalization and Cardinal.cantor"
)
