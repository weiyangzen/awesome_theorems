#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances/THM-M-1285"
LEAN = ROOT / "Formalizations/Lean"
MATHLIB = LEAN / ".lake/packages/mathlib"

audit = json.loads((OWNED / "anchor-audit.json").read_text())
statement = json.loads((OWNED / "statement.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-1285-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-1285"
assert audit["audited_target"]["elaborated_expression_sha256"] == \
    statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert audit["audited_target"]["statement_file_sha256"] == \
    statement["canonical_formal_target"]["statement_file_sha256"]

pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
head = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
assert pin == head == audit["immutable_environment"]["mathlib_revision"]
assert hashlib.sha256((MATHLIB / "LICENSE").read_bytes()).hexdigest() == \
    audit["immutable_environment"]["mathlib_license_sha256"]

probe = (OWNED / "AnchorAudit.lean").read_text()
for declaration in audit["candidates"][1]["declarations"]:
    short = declaration.split(".")[-1]
    assert f"#check {declaration}" in probe or f"#check {short}" in probe

assert len(audit["candidates"]) == 3
assert audit["root_machine_classification"] == "M3"
assert audit["gate_state"] == "self_tested_pending_master_acceptance"
assert audit["audit_complete"] is False
assert audit["theorem_proved"] is False
assert audit["theorem_complete"] is False

print("check_anchor_audit: ok (target fingerprint, pin, license, 8 probes, 3 candidates)")
