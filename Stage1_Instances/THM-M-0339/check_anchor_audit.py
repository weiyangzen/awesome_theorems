#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0339-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0339"
assert AUDIT["target"] == "Stage1.THM_M_0339.MSSPartitionStatement"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
mathlib_candidate = next(c for c in AUDIT["candidates"] if c["project"] == "mathlib4")
assert mathlib_candidate["revision"] == mathlib["rev"]

probe = (HERE / "AnchorAudit.lean").read_text()
for declaration in mathlib_candidate["declarations"]:
    assert f"#check {declaration}" in probe

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: anchor audit boundary, 8 Lean probes, and pinned mathlib revision agree")
