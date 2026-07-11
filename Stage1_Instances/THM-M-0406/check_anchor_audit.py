#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0406"

audit = json.loads((OWNED / "anchor-audit.json").read_text())
assert audit["item_id"] == "S56-M-0406-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0406"
assert audit["exact_external_closure_found"] is False
assert audit["theorem_complete"] is False
assert len(audit["candidates"]) == 6

statement_hash = hashlib.sha256((OWNED / "Statement.lean").read_bytes()).hexdigest()
assert statement_hash == audit["statement_file_sha256"]

manifest_hash = hashlib.sha256((ROOT / "Formalizations/Lean/lake-manifest.json").read_bytes()).hexdigest()
assert manifest_hash == audit["environment"]["lake_manifest_sha256"]

for package, key in (("mathlib", "mathlib_commit"), ("flt-regular", "flt_regular_commit")):
    actual = subprocess.check_output(
        ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages" / package), "rev-parse", "HEAD"],
        text=True,
    ).strip()
    assert actual == audit["environment"][key]

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib"
required = {
    "AlgebraicGeometry/Morphisms/Proper.lean": "class IsProper",
    "AlgebraicGeometry/Morphisms/Smooth.lean": "class Smooth",
    "RingTheory/DedekindDomain/SInteger.lean": "def unitEquivUnitsInteger",
    "NumberTheory/Height/Northcott.lean": "class Northcott",
}
for relative, witness in required.items():
    assert witness in (mathlib / relative).read_text()

print("check_anchor_audit: ok (6 candidates, immutable pins and substrate witnesses verified; root open)")
