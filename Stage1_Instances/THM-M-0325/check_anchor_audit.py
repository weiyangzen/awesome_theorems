#!/usr/bin/env python3
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")
MATHLIB = ROOT / "Formalizations/Lean/.lake/packages/mathlib"

data = json.loads(AUDIT.read_text())
assert data["item_id"] == "S56-M-0325-ANCHOR_AUDIT"
assert data["theorem_id"] == "THM-M-0325"
assert data["root_machine_classification"] == "M4"
assert data["theorem_proved"] is False
assert data["theorem_complete"] is False

revision = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
assert revision == "8a178386ffc0f5fef0b77738bb5449d50efeea95"

expected = data["candidates"][1]["source_sha256"]
for filename, digest in expected.items():
    path = MATHLIB / "Mathlib/Analysis/Normed/Module/PiTensorProduct" / filename
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    source = path.read_text()
    for forbidden in ("sorry", "admit", "unsafe", "axiom "):
        assert forbidden not in source

print("anchor audit invariant check: ok")
print(f"mathlib revision: {revision}")
