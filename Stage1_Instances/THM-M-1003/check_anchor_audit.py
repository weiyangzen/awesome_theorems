#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1003-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1003"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert AUDIT["candidates"][2]["revision"] == mathlib["rev"]
assert AUDIT["candidates"][3]["revision"] == mathlib["rev"]

probe = (HERE / "AnchorAudit.lean").read_text()
for candidate_index in (2, 3):
    for declaration in AUDIT["candidates"][candidate_index]["declarations"]:
        short_name = declaration.removeprefix("MeasureTheory.")
        assert f"#check {short_name}" in probe

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_283.lean").read_text()
for declaration in AUDIT["candidates"][1]["declarations"]:
    assert declaration.rsplit(".", 1)[-1] in legacy

print("ok: bounded anchor inventory, 10 Lean probes, negative status boundary, and pinned mathlib revision")
