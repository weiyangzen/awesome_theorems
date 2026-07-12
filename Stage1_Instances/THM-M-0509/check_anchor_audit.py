#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads((Path(__file__).with_name("anchor-audit.json")).read_text())
LAKE = ROOT / "Formalizations/Lean"

assert AUDIT["item_id"] == "S56-M-0509-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0509"
assert AUDIT["target"] == "Stage1Instances.THM_M_0509.ChenTheoremTarget"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False
assert AUDIT["gate_state"] == "self_tested_pending_master_acceptance"
assert len(AUDIT["candidates"]) == 3
assert len(AUDIT["external_searches"]) == 4

manifest = (LAKE / "lakefile.lean").read_text()
mathlib_pin = AUDIT["candidates"][1]["revision"]
assert mathlib_pin in manifest
head = subprocess.check_output(
    ["git", "-C", str(LAKE / ".lake/packages/mathlib"), "rev-parse", "HEAD"],
    text=True,
).strip()
assert head == mathlib_pin

probe = Path(__file__).with_name("AnchorAudit.lean").read_text()
for declaration in AUDIT["candidates"][1]["declarations"]:
    assert f"#check {declaration}" in probe

print("anchor audit invariant check: ok")
