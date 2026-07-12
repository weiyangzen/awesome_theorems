#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-1016"

audit = json.loads((OWNED / "anchor-audit.json").read_text())
statement = json.loads((OWNED / "statement.json").read_text())

assert audit["item_id"] == "S56-M-1016-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-1016"
assert audit["canonical_target_expression_sha256"] == statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert audit["root_decision"]["classification"] == "M3"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["audit_complete"] is False and audit["theorem_complete"] is False
assert {candidate["classification"] for candidate in audit["candidates"]} == {"M2", "M3"}

mathlib = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"
for relative, expected in audit["candidates"][0]["source_sha256"].items():
    actual = hashlib.sha256((mathlib / relative).read_bytes()).hexdigest()
    assert actual == expected, (relative, actual, expected)

legacy = ROOT / audit["candidates"][1]["file"]
assert hashlib.sha256(legacy.read_bytes()).hexdigest() == audit["candidates"][1]["source_sha256"]

probe = (OWNED / "AnchorAudit.lean").read_text()
for name in audit["candidates"][0]["declarations"]:
    assert name.split(".")[-1] in probe

print("anchor audit structure, immutable source hashes, classifications, and status boundary passed")
