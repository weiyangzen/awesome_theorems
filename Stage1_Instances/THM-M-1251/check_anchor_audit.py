#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-1251-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-1251"
assert AUDIT["root_machine_classification"] == "M0-W"
assert AUDIT["stronger_branch_classification"] == "M4"
assert AUDIT["repo_local_integration_debt"] is False
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(p for p in MANIFEST["packages"] if p["name"] == "mathlib")
assert mathlib["rev"] == AUDIT["immutable_environment"]["mathlib_revision"]
mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

source = (HERE / "AnchorAudit.lean").read_text()
assert "theorem exactMathlibAnchor" in source
assert "def CanonicalTarget" in source
assert "#print axioms" in source
assert "sorry" not in source

mathlib_source = mathlib_root / "Mathlib/Analysis/Distribution/TemperedDistribution.lean"
text = mathlib_source.read_text()
assert "abbrev TemperedDistribution :=" in text
assert "→Lₚₜ[ℂ] F" in text
assert "use the pointwise topology for now" in text
assert "and not the strong topology" in text

print("ok: exact M0-W anchor, stronger-branch boundary, manifest pin, installed HEAD, and Lean probe")
