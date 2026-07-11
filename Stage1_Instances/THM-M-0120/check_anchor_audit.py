#!/usr/bin/env python3
"""Check the local immutable-candidate facts for THM-M-0120."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
INSTANCE = Path(__file__).resolve().parent
AUDIT = json.loads((INSTANCE / "anchor-audit.json").read_text(encoding="utf-8"))
MANIFEST = json.loads(
    (ROOT / "Formalizations/Lean/lake-manifest.json").read_text(encoding="utf-8")
)

assert AUDIT["item_id"] == "S56-M-0120-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0120"
assert AUDIT["depends_on"] == ["S56-M-0120-STATEMENT"]
assert AUDIT["canonical_target"] == "Stage1Instances.THMM0120.MoriConeTheoremTarget"
assert AUDIT["root_decision"]["machine_classification"] == "M3"
assert AUDIT["root_decision"]["kernel_closed"] is False
assert AUDIT["root_decision"]["exact_external_candidate_found"] is False
assert AUDIT["audit_complete"] is False and AUDIT["theorem_complete"] is False

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == AUDIT["immutable_environment"]["mathlib_revision"]
mathlib_root = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert head == mathlib["rev"]
status = subprocess.run(
    ["git", "-C", str(mathlib_root), "status", "--short"],
    check=True,
    capture_output=True,
    text=True,
).stdout
assert status == ""

statement = (INSTANCE / "Statement.lean").read_text(encoding="utf-8")
assert "def MoriConeTheoremTarget : Prop" in statement
assert hashlib.sha256(statement.encode()).hexdigest() == \
    AUDIT["candidates"][0].get("statement_sha256", "69eabc83cd8b7fe8fa34d598c9de890eea09d8ee8357d551abf3e7727444fd6b")

legacy_path = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_039.lean"
legacy = legacy_path.read_text(encoding="utf-8")
legacy_candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0120-A-LOCAL-LEGACY")
assert hashlib.sha256(legacy.encode()).hexdigest() == legacy_candidate["source_sha256"]
assert "def StatementShape : Prop" in legacy
assert "def externalLeanAuditRows" in legacy

probe = (INSTANCE / "AnchorAudit.lean").read_text(encoding="utf-8")
mathlib_candidate = next(c for c in AUDIT["candidates"] if c["candidate_id"] == "M0120-A-MATHLIB")
for declaration in mathlib_candidate["declarations"]:
    assert f"#check {declaration}" in probe

# Exact domain vocabulary is absent from the immutable mathlib source tree.
search = subprocess.run(
    ["rg", "-n", "-i", "MoriCone|ConeTheorem|ExtremalRay|KltPair|KawamataLogTerminal|NumericalCurve",
     str(mathlib_root / "Mathlib"), "-g", "*.lean"],
    capture_output=True,
    text=True,
)
assert search.returncode == 1 and search.stdout == ""

print("ok: immutable local candidates, clean pinned mathlib, eight Lean probes, and M3 boundary agree")

