#!/usr/bin/env python3
"""Verify immutable pins and invariants for the THM-M-0156 anchor audit."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MATHLIB = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
DATA = json.loads((HERE / "anchor-audit.json").read_text())

assert DATA["item_id"] == "S56-M-0156-ANCHOR_AUDIT"
assert DATA["canonical_statement_sha256"] == hashlib.sha256(
    (HERE / "Statement.lean").read_bytes()
).hexdigest()

c1, c2 = DATA["candidates"]
head = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
assert head == DATA["immutable_environment"]["mathlib_revision"] == c1["revision"] == c2["revision"]

for candidate in (c1, c2):
    path = MATHLIB / candidate["file"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == candidate["file_sha256"]
    blob = subprocess.check_output(
        ["git", "-C", str(MATHLIB), "rev-parse", f"HEAD:{candidate['file']}"], text=True
    ).strip()
    assert blob == candidate["git_blob"]

assert hashlib.sha256((MATHLIB / "LICENSE").read_bytes()).hexdigest() == DATA[
    "immutable_environment"
]["license_sha256"]

owning_source = (MATHLIB / c1["file"]).read_text()
assert c1["declaration"].split(".")[-1] in owning_source
for forbidden in ("sorry", "proof_wanted", "unsafe theorem", "unsafe def", "axiom "):
    assert forbidden not in owning_source

assert DATA["audit_result"]["theorem_complete"] is False
assert DATA["audit_result"]["audit_complete"] is False
print("anchor audit invariant check: ok; 2 pinned candidates classified; hashes and boundary verified")
