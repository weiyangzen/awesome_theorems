#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0992"
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"

audit = json.loads((OWNED / "anchor-audit.json").read_text())
statement = json.loads((OWNED / "statement.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-0992-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0992"
assert audit["audited_target"]["elaborated_expression_sha256"] == \
    statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert audit["audited_target"]["statement_file_sha256"] == \
    statement["canonical_formal_target"]["statement_file_sha256"]

pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
head = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
assert pin == head == audit["immutable_environment"]["mathlib_revision"]

module = MATHLIB / "Mathlib" / "Probability" / "Moments" / "Variance.lean"
assert hashlib.sha256(module.read_bytes()).hexdigest() == \
    audit["immutable_environment"]["mathlib_module_sha256"]
source = module.read_text()
assert "theorem meas_ge_le_variance_div_sq" in source
terminal = source.split("theorem meas_ge_le_variance_div_sq", 1)[1].split(
    "theorem IndepFun.variance_add", 1
)[0]
assert "@meas_ge_le_evariance_div_sq" in terminal
assert "sorry" not in terminal

probe = (OWNED / "AnchorAudit.lean").read_text()
frozen = (OWNED / "Statement.lean").read_text()
for clause in ["IsProbabilityMeasure P", "MemLp X 2 P", "0 < r", "variance X P / r ^ 2"]:
    assert clause in probe and clause in frozen
assert "exactTarget_from_pinned_mathlib" in probe
assert "ProbabilityTheory.meas_ge_le_variance_div_sq" in probe

assert len(audit["candidates"]) == 5
assert audit["candidates"][0]["classification"] == \
    "M0-W_candidate_pending_downstream_gates"
assert all(c["classification"] != "M1" for c in audit["candidates"])
assert audit["theorem_proved"] is False
assert audit["theorem_complete"] is False
assert audit["gate_state"] == "self_tested_pending_master_acceptance"

print("check_anchor_audit: ok (exact pin, module hash, target clauses, 5 candidates)")
