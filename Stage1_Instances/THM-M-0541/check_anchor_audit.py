#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0541 anchor-audit receipt."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
audit = json.loads((ROOT / "anchor-audit.json").read_text())
statement = json.loads((ROOT / "statement.json").read_text())
manifest = json.loads((REPO / "Formalizations/Lean/lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-0541-ANCHOR_AUDIT"
assert audit["theorem_id"] == statement["theorem_id"] == "THM-M-0541"
assert audit["exact_candidate_found"] is False
assert audit["classification"]["machine"] == "M3"
assert audit["theorem_proved"] is False and audit["theorem_complete"] is False
assert audit["gate_state"] == "self_tested_pending_master_acceptance"
assert audit["remaining_anchor_cut_set"]

packages = {p["name"].strip("«»"): p for p in manifest["packages"]}
assert packages["mathlib"]["rev"] == audit["environment"]["mathlib_revision"]

mathlib = REPO / "Formalizations/Lean/.lake/packages/mathlib"
for candidate in audit["candidates"][:2]:
    module = candidate["module"].replace(".", "/") + ".lean"
    source = mathlib / module
    assert source.is_file(), source
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest == candidate["source_file_sha256"], (source, digest)
    assert candidate["exact_target_match"] is False

probe = (ROOT / "AnchorProbe.lean").read_text()
for decl in audit["candidates"][0]["declarations"]:
    assert f"#check {decl}" in probe

print("anchor audit invariant check: ok")
