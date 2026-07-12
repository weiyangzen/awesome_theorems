#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0982"
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"
PIN = "8a178386ffc0f5fef0b77738bb5449d50efeea95"

audit = json.loads((OWNED / "anchor-audit.json").read_text())
assert audit["item_id"] == "S56-M-0982-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0982"
assert audit["immutable_environment"]["mathlib_revision"] == PIN
assert audit["gate_state"] == "self_tested_pending_master_acceptance"
assert audit["theorem_complete"] is False

head = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
assert head == PIN, (head, PIN)
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "status", "--short"], text=True
) == ""

source = MATHLIB / "Mathlib" / "MeasureTheory" / "Measure" / "MeasureSpace.lean"
body = source.read_text()
for token in (
    "theorem tendsto_measure_iUnion_atTop",
    "theorem tendsto_measure_iInter_atTop",
    "rw [hm.measure_iUnion]",
    "rw [hm.measure_iInter hs hf]",
):
    assert token in body
assert hashlib.sha256(source.read_bytes()).hexdigest() == audit["immutable_environment"]["measure_space_source_sha256"]

probe = (OWNED / "AnchorAudit.lean").read_text()
for token in (
    "theorem auditedTarget_mathlib",
    "tendsto_measure_iUnion_atTop",
    "tendsto_measure_iInter_atTop",
    "#print axioms auditedTarget_mathlib",
):
    assert token in probe
assert "sorry" not in probe.lower()
print("check_anchor_audit: ok (pin, clean dependency, source bodies, exact wrapper, status boundary)")
