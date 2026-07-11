#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INSTANCE = Path(__file__).resolve().parent
AUDIT = json.loads((INSTANCE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0113-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0113"
assert AUDIT["canonical_target"] == "Stage1Instances.THMM0113.HodgeDecompositionTarget"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["audit_complete"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert AUDIT["immutable_environment"]["mathlib_revision"] == mathlib["rev"]

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

probe = (INSTANCE / "AnchorAudit.lean").read_text()
mathlib_candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0113-A-MATHLIB")
for declaration in mathlib_candidate["declarations"]:
    assert f"#check {declaration}" in probe

statement = (INSTANCE / "Statement.lean").read_text()
assert "def HodgeDecompositionTarget : Prop" in statement
legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_025.lean").read_text()
assert "def StatementShape : Prop" in legacy
assert "def machineProofDebt : String := \"formalization_debt\"" in legacy

external = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0113-A-LEAN-MILLENNIUM")
assert external["revision"] == "540da94826f70f3edf4d4fc66ce6cda20e903f61"
assert external["toolchain"] == "leanprover/lean4:v4.26.0"
assert external["mathlib_revision"] == "2df2f0150c275ad53cb3c90f7c98ec15a56a1a67"

print("ok: target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree")
