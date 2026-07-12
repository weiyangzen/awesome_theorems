#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
audit = json.loads((HERE / "anchor-audit.json").read_text())
lean = (HERE / "AnchorAudit.lean").read_text()
report = (HERE / "anchor-audit.md").read_text()

assert audit["item_id"] == "S56-M-0353-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0353"
assert audit["mathlib"]["commit"] == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert audit["machine_classification"] == "M3"
assert audit["audit_complete"] is False and audit["theorem_complete"] is False
assert len(audit["external_candidates"]) == 3
for token in ("hermite_monic", "deriv_gaussian_eq_hermite_mul_gaussian", "#print axioms"):
    assert token in lean
for token in ("4d055b0bf3722c73bd6c327eeabd8a8a72ab4c7e", "M3", "grep.app"):
    assert token in report
for forbidden in ("sorry", "admit", "axiom "):
    assert forbidden not in lean.lower()

print("anchor audit invariant check: ok")
print("anchor-audit.json sha256:", hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest())
