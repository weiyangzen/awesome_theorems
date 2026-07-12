#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0993"
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"

audit = json.loads((OWNED / "anchor-audit.json").read_text())
statement = json.loads((OWNED / "statement.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-0993-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0993"
assert audit["audited_target"]["elaborated_expression_sha256"] == \
    statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert audit["audited_target"]["statement_file_sha256"] == \
    statement["canonical_formal_target"]["statement_file_sha256"]

pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
head = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
assert pin == head == audit["immutable_environment"]["mathlib_revision"]

module = MATHLIB / "Mathlib" / "Probability" / "Moments" / "Basic.lean"
assert hashlib.sha256(module.read_bytes()).hexdigest() == \
    audit["immutable_environment"]["mathlib_module_sha256"]
source = module.read_text()
for declaration in [
    "theorem iIndepFun.integrable_exp_mul_sum",
    "theorem iIndepFun.mgf_sum",
    "theorem measure_ge_le_exp_mul_mgf",
]:
    assert declaration in source

probe = (OWNED / "AnchorAudit.lean").read_text()
frozen = (OWNED / "Statement.lean").read_text()
for clause in [
    "0 < t",
    "forall i, Measurable (X i)",
    "iIndepFun X mu",
    "forall i, Integrable",
    "mu.real {omega | a <= ∑ i, X i omega}",
]:
    assert clause in probe and clause in frozen
for declaration in [
    "measure_ge_le_exp_mul_mgf",
    "integrable_exp_mul_sum",
    "hindep.mgf_sum",
]:
    assert declaration in probe

assert [c["candidate_id"] for c in audit["candidates"]] == [
    "S56-M-0993-C01", "S56-M-0993-C02", "S56-M-0993-C03", "S56-M-0993-C04"
]
assert audit["root_machine_classification"] == \
    "M0-L_candidate_pending_downstream_gates"
assert audit["integration_blocker"] is None
assert audit["theorem_proved"] is False
assert audit["theorem_complete"] is False
assert audit["gate_state"] == "self_tested_pending_master_acceptance"

print("check_anchor_audit: ok (exact pin, module hash, clauses, route, 4 candidates)")
