#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1148-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1148"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["debt_classification"] == "formalization_debt"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
candidate = next(c for c in AUDIT["candidates"] if c["project"] == "mathlib4")
assert candidate["revision"] == mathlib["rev"]

source = (HERE / "AnchorAudit.lean").read_text()
for declaration in candidate["declarations"]:
    assert f"#check {declaration.removeprefix('InnerProductSpace.')}" in source

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: anchor audit boundary, four Lean anchors, and installed mathlib revision agree")
