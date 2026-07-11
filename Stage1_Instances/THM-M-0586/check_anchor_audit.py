#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0586-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0586"
assert AUDIT["canonical_expression_sha256"] == (
    "48062820803a28b54a2bcf9b1122a10ce4d4b53b1d9e37e5f0c8b119955346e7"
)
assert AUDIT["root_machine_classification"] == "M4"
assert AUDIT["machine_debt"] == "formalization_debt"
assert AUDIT["audit_complete"] is False
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
mathlib_candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"].endswith("C02"))
assert mathlib_candidate["revision"] == mathlib["rev"]

mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]

poincare_source = mathlib_root / "Mathlib/Geometry/Manifold/PoincareConjecture.lean"
source = poincare_source.read_text()
marker = "proof_wanted ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere"
assert source.count(marker) == 1
assert "theorem ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere" not in source
assert "axiom ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere" not in source

probe = (HERE / "AnchorAudit.lean").read_text()
for declaration in mathlib_candidate["supporting_declarations_checked"]:
    assert f"#check {declaration}" in probe

external = next(c for c in AUDIT["candidates"] if c["candidate_id"].endswith("C03"))
assert external["revision"] == "540da94826f70f3edf4d4fc66ce6cda20e903f61"
assert external["classification"] == "M3_adjacent_only"

print("ok: THM-M-0586 anchor inventory, proof_wanted boundary, 8 probes, and immutable pins")

