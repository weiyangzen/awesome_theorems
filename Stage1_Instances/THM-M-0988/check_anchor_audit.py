#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0988"
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"

audit = json.loads((OWNED / "anchor-audit.json").read_text())
statement = json.loads((OWNED / "statement.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-0988-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0988"
assert audit["audited_target"]["elaborated_expression_sha256"] == \
    statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert audit["audited_target"]["statement_file_sha256"] == \
    statement["canonical_formal_target"]["statement_file_sha256"]

pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
head = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
assert pin == head == audit["immutable_environment"]["mathlib_revision"]

module = MATHLIB / "Mathlib" / "Probability" / "CentralLimitTheorem.lean"
digest = hashlib.sha256(module.read_bytes()).hexdigest()
assert digest == audit["immutable_environment"]["mathlib_module_sha256"]
source = module.read_text()
assert "theorem tendstoInDistribution_inv_sqrt_mul_sum_sub" in source
terminal = source.split("theorem tendstoInDistribution_inv_sqrt_mul_sum_sub", 1)[1]
assert "obtain h | h := eq_or_ne Var[X 0; P] 0" in terminal
assert "by sorry" not in terminal

probe = (OWNED / "AnchorAudit.lean").read_text()
frozen = (OWNED / "Statement.lean").read_text()
for clause in [
    "HasLaw Y (gaussianReal 0 (variance (X 0) P).toNNReal) P'",
    "MemLp (X 0) 2 P",
    "iIndepFun X P",
    "IdentDistrib (X i) (X 0) P P",
    "TendstoInDistribution",
]:
    assert clause in probe and clause in frozen
assert "exactTarget_from_pinned_mathlib" in probe
assert "tendstoInDistribution_inv_sqrt_mul_sum_sub" in probe

assert len(audit["candidates"]) == 4
assert audit["candidates"][0]["kind"] == "exact_terminal_theorem"
assert audit["candidates"][2]["classification"] == \
    "external_upstream_anchor_only_redundant"
assert audit["candidates"][3]["classification"] == "M5_noncandidate"
assert audit["theorem_proved"] is False
assert audit["theorem_complete"] is False
assert audit["gate_state"] == "self_tested_pending_master_acceptance"

print("check_anchor_audit: ok (exact pin, module hash, target clauses, 4 candidates)")
