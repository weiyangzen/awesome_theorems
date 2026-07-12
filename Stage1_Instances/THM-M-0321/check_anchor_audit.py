#!/usr/bin/env python3
"""Validate the scoped immutable-anchor audit for THM-M-0321."""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
OWNED = ROOT / "Stage1_Instances" / "THM-M-0321"
AUDIT = json.loads((OWNED / "anchor-audit.json").read_text(encoding="utf-8"))
STATEMENT = json.loads((OWNED / "statement.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((LEAN_ROOT / "lake-manifest.json").read_text(encoding="utf-8"))

assert AUDIT["theorem_id"] == "THM-M-0321"
assert AUDIT["item_id"] == "S56-M-0321-ANCHOR_AUDIT"
assert AUDIT["exact_candidate"] is None
assert AUDIT["machine_classification"] == "M3"
assert AUDIT["canonical_expression_sha256"] == STATEMENT["canonical_formal_target"]["expression_sha256"]

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
pin = AUDIT["local_environment"]["mathlib_revision"]
assert pin == mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert AUDIT["local_environment"]["dependency_mutation"] is False
assert len(AUDIT["searches"]) >= 4
assert len(AUDIT["candidates"]) >= 4

for candidate in AUDIT["candidates"]:
    assert candidate["classification"].startswith("rejected_")
    assert candidate["reason"]
    assert candidate["placeholder_and_axiom_audit"]
    if candidate["repository"].endswith("mathlib4.git"):
        assert candidate["revision"] == pin

probe = (OWNED / "AnchorAuditProbe.lean").read_text(encoding="utf-8")
for forbidden in ("sorry", "admit", "axiom"):
    if re.search(rf"\b{forbidden}\b", probe):
        raise SystemExit(f"forbidden token in AnchorAuditProbe.lean: {forbidden}")

result = subprocess.run(
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0321/AnchorAuditProbe.lean"],
    cwd=LEAN_ROOT,
    text=True,
    capture_output=True,
    check=False,
)
sys.stdout.write(result.stdout)
sys.stderr.write(result.stderr)
if result.returncode:
    raise SystemExit(result.returncode)

for declaration in (
    "ContractingWith.exists_fixedPoint'",
    "exists_mem_Icc_isFixedPt_of_mapsTo",
    "RealRMK.integral_rieszMeasure",
):
    if declaration not in result.stdout:
        raise SystemExit(f"missing elaborated candidate type: {declaration}")

print(f"mathlib_revision={pin}")
print(f"canonical_expression_sha256={AUDIT['canonical_expression_sha256']}")
print("anchor audit checks: ok")
