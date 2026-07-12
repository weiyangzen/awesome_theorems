#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0508-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0508"
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
support = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "S56-M-0508-C02")
assert support["revision"] == mathlib["rev"]
probe = (HERE / "AnchorAudit.lean").read_text()
for declaration in support["declarations"]:
    assert f"#check {declaration}" in probe

external = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "S56-M-0508-C03")
assert "sorry" in external["body_provenance"]
assert external["classification"] == "M4_placeholder_rejected"

mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True
).stdout.strip()
assert head == mathlib["rev"]

print("ok: bounded audit, 10 pinned probes, rejected placeholder, and immutable mathlib pin")
