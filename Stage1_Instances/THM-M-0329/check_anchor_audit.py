#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0329-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0329"
assert AUDIT["decision"]["audit_complete_for_phase"] is True
assert AUDIT["decision"]["audit_complete"] is False
assert AUDIT["decision"]["theorem_complete"] is False

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
candidate = AUDIT["candidates"][0]
assert candidate["revision"] == mathlib["rev"]
mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True,
).stdout.strip()
assert head == candidate["revision"]

source_path = mathlib_root / candidate["file"]
assert hashlib.sha256(source_path.read_bytes()).hexdigest() == candidate["file_sha256"]
adapter = (HERE / "AnchorAudit.lean").read_text()
for declaration in candidate["declarations"]:
    assert declaration.split(".")[-1] in source_path.read_text()
assert "theorem canonicalTarget_mathlib_candidate" in adapter
assert "#print axioms" in adapter

print("ok: exact adapter, immutable mathlib pin/source, candidate inventory, and status boundary")
