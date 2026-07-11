#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = json.loads(Path(__file__).with_name("anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0183-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0183"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False
assert AUDIT["search_inventory"]["local_terminal_candidate_count"] == 0

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
assert mathlib["rev"] == AUDIT["immutable_environment"]["mathlib_revision"]
mathlib_candidate = next(c for c in AUDIT["candidates"] if c["project"] == "mathlib4")
assert mathlib_candidate["revision"] == mathlib["rev"]

probe = Path(__file__).with_name("AnchorAudit.lean").read_text()
for declaration in mathlib_candidate["declarations"]:
    assert f"#check {declaration}" in probe

mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True
).stdout.strip()
assert head == mathlib["rev"]

print("ok: bounded anchor audit, 10 Lean probes, status boundary, and pinned mathlib revision")
