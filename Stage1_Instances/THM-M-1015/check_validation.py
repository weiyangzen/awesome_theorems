#!/usr/bin/env python3
"""Narrow fail-closed validation runner for THM-M-1015."""

import hashlib
import json
from pathlib import Path
import os
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN = ROOT / "Formalizations" / "Lean"


def run(argv, cwd, env=None):
    result = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    return result.stdout + result.stderr


spec = json.loads((HERE / "validation-phase-spec.json").read_text())
receipt = json.loads((HERE / "proof-receipt.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())
assert spec["item_id"] == "S56-M-1015-VALIDATION"
assert spec["theorem_id"] == receipt["theorem_id"] == "THM-M-1015"
assert receipt["result"]["root_closed"] is True
mathlib_pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
mathlib = LEAN / ".lake" / "packages" / "mathlib"
assert run(["git", "rev-parse", "HEAD"], mathlib).strip() == mathlib_pin
assert not run(["git", "status", "--porcelain"], mathlib).strip()

for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    assert not re.search(r"\b(sorry|admit|sorryAx)\b|^[ \t]*(axiom|unsafe)\b", source, re.MULTILINE)

lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], LEAN).strip()
with tempfile.TemporaryDirectory(prefix="m1015-validation-", dir=LEAN) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")], LEAN)
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    proof_output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], LEAN, env)
    independent_output = run(["lake", "env", "lean", str(tmp / "Validation.lean")], LEAN, env)

expected = "[propext, Classical.choice, Quot.sound]"
assert proof_output.count(expected) == 3
assert independent_output.count(expected) == 1
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert statement_hash == receipt["inputs"]["statement_sha256"]
print("PASS THM-M-1015 validation: exact proof and independent reconstruction kernel-check")
print(f"axioms: {expected}")
print(f"statement sha256: {statement_hash}")
print(f"mathlib revision: {mathlib_pin}")
