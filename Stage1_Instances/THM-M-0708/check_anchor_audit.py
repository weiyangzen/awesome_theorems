#!/usr/bin/env python3
"""Check the THM-M-0708 immutable anchor-audit receipt."""

import json
from pathlib import Path

root = Path(__file__).resolve().parent
repo = root.parents[1]
data = json.loads((root / "anchor-audit.json").read_text(encoding="utf-8"))
manifest = json.loads((repo / "Formalizations/Lean/lake-manifest.json").read_text(encoding="utf-8"))

assert data["item_id"] == "S56-M-0708-ANCHOR_AUDIT"
assert data["theorem_id"] == "THM-M-0708"
assert data["audit_complete"] is True
assert data["theorem_complete"] is False
mathlib = next(package for package in manifest["packages"] if package["name"] == "mathlib")
candidate = data["candidates"][0]
assert candidate["immutable_revision"] == mathlib["rev"] == mathlib["inputRev"]
assert candidate["declaration"] == "ComputablePred.rice"
source = repo / "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/Halting.lean"
assert source.is_file(), "pinned mathlib source artifact is unavailable"
text = source.read_text(encoding="utf-8")
assert "/-- **Rice's Theorem** -/" in text
assert "theorem rice (C : Set (ℕ →. ℕ))" in text
lean = (root / "AnchorAudit.lean").read_text(encoding="utf-8")
assert "theorem mathlib_rice_exact_candidate : FrozenTarget := by" in lean
assert "sorry" not in lean and "admit" not in lean and "axiom " not in lean
print("check_anchor_audit: ok (pinned mathlib Rice anchor and exact wrapper receipt match)")
