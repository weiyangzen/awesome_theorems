#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1278-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1278"
assert AUDIT["exact_anchor"] is None
assert AUDIT["classification"]["machine"] == "M3"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
assert AUDIT["environment"]["mathlib_revision"] == mathlib["rev"]
assert AUDIT["candidates"][1]["revision"] == mathlib["rev"]

source = (HERE / "AnchorAudit.lean").read_text()
for declaration in AUDIT["candidates"][1]["declarations"]:
    assert f"#check {declaration}" in source

mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: negative anchor disposition, 11 Lean probes, and pinned mathlib revision")
