#!/usr/bin/env python3
"""Validate the structured THM-M-1553 anchor inventory and Lean probes."""

import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"

data = json.loads((HERE / "anchor-audit.json").read_text())
assert data["theorem_id"] == "THM-M-1553"
assert data["item_id"] == "S56-M-1553-ANCHOR_AUDIT"
assert data["root_machine_classification"] == "M4"
assert data["theorem_complete"] is False
assert data["external_search"]["discovery_exhaustive"] is False
assert data["external_search"]["verified_external_candidates"] == []
ids = [row["id"] for row in data["candidates"]]
assert len(ids) == len(set(ids)) == 4
assert all(row["revision"] for row in data["candidates"])

run = subprocess.run(
    ["lake", "env", "lean", os.path.relpath(HERE / "AnchorAudit.lean", LEAN_ROOT)],
    cwd=LEAN_ROOT,
    text=True,
    capture_output=True,
    check=False,
)
if run.returncode:
    raise SystemExit(run.stdout + run.stderr)
for name in ["ContDiff", "Real.hasDerivAt_log", "iteratedDeriv", "LinearMap.BilinMap"]:
    assert name in run.stdout, f"missing probe output: {name}"
print("anchor audit: ok (4 classified candidates, exact root M4, external discovery limited)")
