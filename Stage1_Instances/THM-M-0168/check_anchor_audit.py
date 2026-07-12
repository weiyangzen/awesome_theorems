#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0168-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0168"
assert AUDIT["target"] == "Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["debt_classification"] == "formalization_debt"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
mathlib_candidate = next(c for c in AUDIT["candidates"] if c["project"] == "mathlib4")
assert mathlib_candidate["revision"] == mathlib["rev"]

source = (HERE / "AnchorAudit.lean").read_text()
for declaration in mathlib_candidate["declarations"]:
    assert f"#check {declaration}" in source

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

atlas = next(c for c in AUDIT["candidates"] if c["project"] == "facebookresearch/atlas-lean")
assert len(atlas["revision"]) == 40
assert atlas["mathlib_revision"] == mathlib["rev"]
assert atlas["integration_status"].startswith("not a repository dependency")

print("ok: audit boundary, 5 Lean probes, pinned mathlib revision, and immutable external candidate metadata")
