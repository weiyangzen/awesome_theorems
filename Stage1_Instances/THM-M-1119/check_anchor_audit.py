#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads(Path(__file__).with_name("anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1119-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1119"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["audit_complete"] is True
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == AUDIT["candidates"][1]["revision"]
head = subprocess.run(
    ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages/mathlib"), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True,
).stdout.strip()
assert head == mathlib["rev"]

probe = Path(__file__).with_name("AnchorAudit.lean").read_text()
for declaration in AUDIT["candidates"][1]["declarations"]:
    assert f"#check {declaration}" in probe

external = AUDIT["candidates"][2]
assert external["revision"] == "1c8502fd40113ba0141652c23d542e04c1aa872d"
assert "sorry" in external["placeholder_or_axiom_status"]
assert external["normalized_match"].startswith("finite Van den Berg-Kesten-Reimer")

print("ok: bounded audit, 8 pinned probes, mathlib revision, rejected placeholder candidate, and fail-closed M4 boundary")

