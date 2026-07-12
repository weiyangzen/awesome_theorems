#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads(Path(__file__).with_name("anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1188-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1188"
assert AUDIT["canonical_target"] == (
    "Stage1Instances.THM_M_1188.HeatEquationWeakMaximumPrincipleTarget"
)
assert AUDIT["root_machine_classification"] == "M3"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False
assert len(AUDIT["candidates"]) == 3

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert AUDIT["candidates"][1]["revision"] == mathlib["rev"]

probe = (ROOT / "Stage1_Instances/THM-M-1188/AnchorAudit.lean").read_text()
for declaration in AUDIT["candidates"][1]["declarations"]:
    assert f"#check {declaration}" in probe

statement = (ROOT / "Stage1_Instances/THM-M-1188/Statement.lean").read_text()
assert "def HeatEquationWeakMaximumPrincipleTarget : Prop :=" in statement

mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: anchor boundary, three candidates, six Lean probes, statement, and mathlib pin")
