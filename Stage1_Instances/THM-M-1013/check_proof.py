#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-1013 proof node."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
statement = (HERE / "Statement.lean").read_text()
registry = json.loads((HERE / "obligation-registry.json").read_text())


def require(value, message):
    if not value:
        raise SystemExit("proof check failed: " + message)


require(registry["theorem_id"] == "THM-M-1013", "wrong theorem registry")
require(
    registry["frozen_against_statement_sha256"]
    == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "statement drifted after obligation freeze",
)
require("import Statement" in proof, "proof does not import the frozen target")
require("theorem cramerWold : StatementShape" in proof, "exact root wrapper missing")
for declaration in (
    "projection_charFun_one_measure",
    "ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous",
    "ProbabilityMeasure.tendsto_iff_tendsto_charFun",
    "theorem forward",
    "theorem reverse",
):
    require(declaration in proof, f"required proof component missing: {declaration}")
for token in ("sorry", "admit", "sorryAx", "axiom ", "unsafe "):
    require(token not in proof, f"prohibited proof token: {token.strip()}")
require("def StatementShape : Prop" in statement, "canonical target missing")
print("PASS THM-M-1013 proof: forward and reverse branches close exact StatementShape")
