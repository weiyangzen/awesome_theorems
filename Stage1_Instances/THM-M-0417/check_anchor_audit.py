#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0417-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0417"
assert AUDIT["root_machine_classification"] == "M0-W candidate"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
candidate = AUDIT["candidates"][0]
assert candidate["revision"] == mathlib["rev"]

mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True,
).stdout.strip()
assert head == mathlib["rev"]

source_path = mathlib_root / "Mathlib/MeasureTheory/Group/GeometryOfNumbers.lean"
assert hashlib.sha256(source_path.read_bytes()).hexdigest() == candidate["source_sha256"]
blob = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD:Mathlib/MeasureTheory/Group/GeometryOfNumbers.lean"],
    check=True, capture_output=True, text=True,
).stdout.strip()
assert blob == candidate["source_blob"]

source = source_path.read_text()
terminal_start = source.index("theorem exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure")
terminal_end = source.index("set_option backward.isDefEq.respectTransparency", terminal_start)
terminal_body = source[terminal_start:terminal_end]
for prohibited in ("sorry", "admit", "axiom "):
    assert prohibited not in terminal_body
assert ":= by" in terminal_body

probe = (HERE / "AnchorAudit.lean").read_text()
assert "theorem mathlibCandidateClosesFrozenTarget" in probe
assert "#print axioms mathlibCandidateClosesFrozenTarget" in probe

print("ok: exact wrapper, terminal body, placeholder scan, source blob, and pinned mathlib revision")
