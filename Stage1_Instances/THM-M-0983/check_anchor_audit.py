#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
MANIFEST = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert AUDIT["item_id"] == "S56-M-0983-ANCHOR_AUDIT"
assert AUDIT["theorem_id"] == "THM-M-0983"
assert AUDIT["theorem_proved"] is False
assert AUDIT["theorem_complete"] is False
assert AUDIT["gate_state"] == "self_tested_pending_master_acceptance"

mathlib = next(package for package in MANIFEST["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert AUDIT["candidates"][0]["revision"] == mathlib["rev"]

head = subprocess.run(
    ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages/mathlib"), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True,
).stdout.strip()
assert head == mathlib["rev"]

anchor = (HERE / "AnchorAudit.lean").read_text()
statement = (HERE / "Statement.lean").read_text()
for fragment in [
    "Integrable (X 0) mu ->",
    "ProbabilityTheory.iIndepFun X mu ->",
    "ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu",
    "X i omega = 0 \\/ X i omega = 1",
    "mu[X 0] = p ->",
]:
    assert fragment in statement
    assert fragment in anchor
for declaration in [
    "ProbabilityTheory.strong_law_ae_real",
    "ProbabilityTheory.strong_law_ae",
    "ProbabilityTheory.strong_law_Lp",
    "ProbabilityTheory.iIndepFun.indepFun",
]:
    assert f"#check {declaration}" in anchor
assert "sorry" not in anchor.lower()

print("ok: exact anchor bridge, status boundary, four Lean probes, and pinned mathlib revision")
