#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads((Path(__file__).with_name("anchor-audit.json")).read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0419-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0419"
assert AUDIT["root_machine_classification"] == "M3"
assert AUDIT["debt_classification"] == "formalization_debt"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert AUDIT["candidates"][1]["revision"] == mathlib["rev"]

source = (Path(__file__).with_name("AnchorAudit.lean")).read_text()
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

external = AUDIT["candidates"][2]
assert external["revision"] == "34ffed396f376454c1a9b297f3fd74c5c801fb50"
assert "sorry" in external["placeholder_or_axiom_status"]
assert AUDIT["external_candidate_evidence"]["source_sorry_count"] == 22

print("ok: negative status boundary, 13 Lean probes, pinned mathlib revision, and placeholder candidate classification")
