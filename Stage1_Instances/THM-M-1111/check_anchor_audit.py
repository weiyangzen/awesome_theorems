#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads((Path(__file__).with_name("anchor-audit.json")).read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1111-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1111"
assert AUDIT["target"] == "Stage1Instances.THM_M_1111.TaoVuFourMomentTarget"
assert AUDIT["root_machine_classification"] == "M3"
assert AUDIT["audit_complete"] is False
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False
assert all(candidate["classification"] not in {"M0-L", "M0-W", "M0-P", "M1"}
           for candidate in AUDIT["candidates"])

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == AUDIT["candidates"][1]["revision"]

probe = (Path(__file__).with_name("AnchorAudit.lean")).read_text()
for declaration in AUDIT["candidates"][1]["declarations"]:
    assert f"#check {declaration}" in probe

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: anchor inventory boundary, two candidates, four Lean probes, and pinned mathlib revision")
