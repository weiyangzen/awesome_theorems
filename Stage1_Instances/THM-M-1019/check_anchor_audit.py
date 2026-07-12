#!/usr/bin/env python3
"""Validate immutable identities and status boundaries for the THM-M-1019 anchor audit."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-1019"
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"

audit = json.loads((OWNED / "anchor-audit.json").read_text())
statement = json.loads((OWNED / "statement.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-1019-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-1019"
assert audit["audited_target"]["elaborated_expression_sha256"] == \
    statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert audit["audited_target"]["statement_file_sha256"] == \
    statement["canonical_formal_target"]["statement_file_sha256"]

pin = next(package["rev"] for package in manifest["packages"] if package["name"] == "mathlib")
head = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
tree = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD^{tree}"], text=True
).strip()
env = audit["immutable_environment"]
assert pin == head == env["mathlib_revision"]
assert tree == env["mathlib_tree"]

candidate = audit["candidates"][0]
module = MATHLIB / candidate["source_path"]
assert hashlib.sha256(module.read_bytes()).hexdigest() == candidate["source_file_sha256"]
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "hash-object", candidate["source_path"]], text=True
).strip() == candidate["source_file_git_object"]
source = module.read_text()
assert "theorem Measure.ext_of_charFun" in source
assert "ext_of_integral_char_eq" in source

probe = (OWNED / "AnchorAudit.lean").read_text()
assert "theorem pinned_mathlib_candidate" in probe
assert "exact Measure.ext_of_charFun hchar" in probe
assert "#print axioms pinned_mathlib_candidate" in probe

assert len(audit["candidates"]) == 3
assert candidate["classification"] == "M0-W_candidate_pending_downstream_gates"
assert audit["gate_state"] == "self_tested_pending_master_acceptance"
assert audit["audit_complete"] is False
assert audit["theorem_proved_by_this_node"] is False
assert audit["theorem_complete"] is False

print("check_anchor_audit: ok (target fingerprint, pin/tree, source identity, 3 candidates)")
