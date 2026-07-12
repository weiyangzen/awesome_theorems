#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1084-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1084"
assert AUDIT["root_machine_classification"] == "M1"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert AUDIT["candidates"][1]["revision"] == mathlib["rev"]

external = AUDIT["candidates"][2]
assert external["revision"] == "be5d5a8a1a1f46f2ec9502980ff10a39e17e3820"
assert external["classification"] == "M1_external_upstream_anchor_only"
assert external["integration_status"].startswith("not present in lake-manifest")

source = (HERE / "AnchorAudit.lean").read_text()
for declaration in AUDIT["candidates"][1]["declarations"]:
    assert f"#check {declaration}" in source

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: bounded anchor inventory, 6 pinned Lean probes, immutable external candidate, and fail-closed status")
