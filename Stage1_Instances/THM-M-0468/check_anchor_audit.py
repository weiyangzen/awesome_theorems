#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0468"
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"

audit = json.loads((OWNED / "anchor-audit.json").read_text())
statement = json.loads((OWNED / "statement.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-0468-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0468"
assert audit["audited_target"]["elaborated_expression_sha256"] == \
    statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert audit["audited_target"]["statement_file_sha256"] == \
    statement["canonical_formal_target"]["statement_file_sha256"]

pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
head = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
assert pin == head == audit["immutable_environment"]["mathlib_revision"]

module = MATHLIB / "Mathlib/AlgebraicGeometry/Group/Abelian.lean"
assert hashlib.sha256(module.read_bytes()).hexdigest() == \
    audit["immutable_environment"]["mathlib_module_sha256"]
assert "theorem isCommMonObj_of_isProper_of_geometricallyIntegral" in module.read_text()

probe = (OWNED / "AnchorAudit.lean").read_text()
assert "#check AlgebraicGeometry.isCommMonObj_of_isProper_of_geometricallyIntegral" in probe

assert len(audit["candidates"]) == 4
assert audit["candidates"][0]["classification"] == "M3"
assert audit["candidates"][1]["classification"] == "M3_support_only"
assert audit["candidates"][3]["classification"] == "M4_rejected_placeholder_candidate"
assert audit["root_machine_classification"] == "M4"
assert audit["gate_state"] == "self_tested_pending_master_acceptance"
assert audit["audit_complete"] is False
assert audit["theorem_proved"] is False
assert audit["theorem_complete"] is False

print("check_anchor_audit: ok (target fingerprint, exact pin, module hash, 4 candidates)")

