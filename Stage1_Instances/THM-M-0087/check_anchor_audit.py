#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads((Path(__file__).with_name("anchor-audit.json")).read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0087-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0087"
assert AUDIT["root_machine_classification"] == "M0-P_candidate"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "S56-M-0087-C02")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert candidate["revision"] == mathlib["rev"]

probe = (ROOT / "Stage1_Instances/THM-M-0087/AnchorAudit.lean").read_text()
for declaration in candidate["declarations"]:
    short_name = declaration.removeprefix("CategoryTheory.")
    assert f"#check {short_name}" in probe
assert "theorem exactMathlibCandidate : AuditedStatement C" in probe

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

print("ok: exact candidate boundary, 6 Lean anchors, and pinned mathlib revision")
