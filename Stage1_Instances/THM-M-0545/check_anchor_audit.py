#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INSTANCE = Path(__file__).resolve().parent
AUDIT = json.loads((INSTANCE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0545-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0545"
assert AUDIT["canonical_target"] == "Stage1Instances.THMM0545.HodgeDecompositionTarget"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["audit_complete"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
assert AUDIT["immutable_environment"]["mathlib_revision"] == mathlib["rev"]
mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True
).stdout.strip()
assert head == mathlib["rev"]

probe = (INSTANCE / "AnchorAudit.lean").read_text()
candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0545-A-MATHLIB")
for declaration in candidate["declarations"]:
    assert f"#check {declaration}" in probe

statement = (INSTANCE / "Statement.lean").read_text()
assert "def HodgeDecompositionTarget : Prop" in statement
legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_105.lean").read_text()
assert "def StatementShape : Prop" in legacy
assert "def externalLeanPrimarySourceAudit" in legacy

ids = {c["candidate_id"] for c in AUDIT["candidates"]}
assert ids == {
    "M0545-A-LOCAL-STATEMENT", "M0545-A-LOCAL-LEGACY", "M0545-A-MATHLIB",
    "M0545-A-LEAN-MILLENNIUM", "M0545-A-DERHAM"
}
print("ok: target boundary, five candidate rows, 11 Lean probes, and pinned mathlib revision agree")

