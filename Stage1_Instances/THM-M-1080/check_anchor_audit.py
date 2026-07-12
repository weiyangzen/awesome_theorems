#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads((Path(__file__).with_name("anchor-audit.json")).read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1080-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1080"
assert AUDIT["root_machine_classification"] == "M3"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert AUDIT["mathlib"]["revision"] == mathlib["rev"]

source = (Path(__file__).with_name("AnchorAudit.lean")).read_text()
for declaration in AUDIT["mathlib"]["declarations"]:
    assert f"#check {declaration}" in source

head = subprocess.run(
    ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages/mathlib"),
     "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: negative status boundary, three pinned declarations, and mathlib revision")
