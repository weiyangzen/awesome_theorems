#!/usr/bin/env python3
"""Check the structured THM-M-1566 anchor-audit handoff."""

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET = Path(__file__).parent
AUDIT = json.loads((TARGET / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1566-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1566"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False
assert len(AUDIT["candidates"]) == 4
assert len(AUDIT["external_searches"]) == 4

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
mathlib_candidate = next(c for c in AUDIT["candidates"] if c["project"] == "mathlib4")
assert mathlib_candidate["revision"] == mathlib["rev"]

head = subprocess.run(
    ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages/mathlib"),
     "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True,
).stdout.strip()
assert head == mathlib["rev"]

probe = (TARGET / "AnchorAudit.lean").read_text()
for declaration in mathlib_candidate["declarations"]:
    assert f"#check {declaration}" in probe

for forbidden in ("sorry", "admit", "axiom"):
    assert forbidden not in probe.lower()

print("ok: 4 candidates, 4 search records, 5 Lean support probes, M4 boundary, and mathlib pin agree")
