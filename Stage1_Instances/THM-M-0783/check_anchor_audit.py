#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads(Path(__file__).with_name("anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0783-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0783"
assert AUDIT["target"] == "Stage1Instances.THM_M_0783.MartinsAxiom"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
support = AUDIT["candidates"][1]
assert support["revision"] == mathlib["rev"]

probe = Path(__file__).with_name("AnchorAudit.lean").read_text()
for declaration in support["declarations"]:
    assert f"#check {declaration}" in probe

statement = Path(__file__).with_name("Statement.lean").read_text()
assert "def MartinsAxiom : Prop" in statement
for forbidden in ("axiom MartinsAxiom", "opaque MartinsAxiom", "sorry", "admit"):
    assert forbidden not in statement

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: anchor audit boundary, 6 Lean probes, local statement status, and pinned mathlib revision")

