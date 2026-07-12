#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0510-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0510"
assert AUDIT["canonical_declaration"] == (
    "Stage1Instances.THM_M_0510.HardyRamanujanAsymptoticTarget"
)
assert AUDIT["root_machine_classification"] == "M3"
assert AUDIT["external_terminal_proof_found"] is False
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert AUDIT["mathlib_revision"] == mathlib["rev"]
assert AUDIT["candidates"][1]["revision"] == mathlib["rev"]

probe = (HERE / "AnchorAudit.lean").read_text()
for declaration in AUDIT["candidates"][1]["declarations"]:
    assert f"#check {declaration}" in probe

mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

genfun = mathlib_root / "Mathlib/Combinatorics/Enumerative/Partition/GenFun.lean"
text = genfun.read_text()
assert "When $f(i, c) = 1$, this is the generating function for partition function $p(n)$" in text
assert "(TODO: prove this)." in text

print("ok: bounded anchor inventory, 9 Lean probes, negative status boundary, and pinned mathlib revision")

