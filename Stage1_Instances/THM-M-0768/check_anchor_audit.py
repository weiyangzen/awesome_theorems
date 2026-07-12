#!/usr/bin/env python3
"""Validate THM-M-0768 immutable anchor inventory and status boundary."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"

audit = json.loads((HERE / "anchor-audit.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-0768-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0768"
assert audit["audited_target"]["elaborated_expression_sha256"] == \
    statement["canonical_formal_target"]["elaborated_expression_sha256"]

env = audit["immutable_environment"]
pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
head = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip()
tree = subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD^{tree}"], text=True
).strip()
assert pin == head == env["mathlib_revision"]
assert tree == env["mathlib_tree"]
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "status", "--short"], text=True
).strip() == ""

module = MATHLIB / env["module_path"]
assert hashlib.sha256(module.read_bytes()).hexdigest() == env["module_sha256"]
source = module.read_text()
for needle in (
    "theorem schroeder_bernstein_of_rel",
    "theorem schroeder_bernstein",
    "theorem antisymm",
):
    assert needle in source

probe = (HERE / "AnchorAudit.lean").read_text()
assert "theorem pinnedSchroederBernstein" in probe
assert "exact Function.Embedding.schroeder_bernstein hf hg" in probe
assert "#print axioms pinnedSchroederBernstein" in probe

by_id = {c["candidate_id"]: c for c in audit["candidates"]}
assert len(by_id) == 5
assert by_id["S56-M-0768-C02"]["classification"] == "M0-W candidate"
assert by_id["S56-M-0768-C04"]["placeholder_unsafe_oracle_status"].endswith("`sorry`")
assert by_id["S56-M-0768-C05"]["toolchain"] == "Lean 3.42.1"
assert audit["candidate_decision"]["kernel_checked_in_pinned_environment"] is True
assert audit["anchor_audit_phase_complete"] is True
assert audit["audit_complete"] is False
assert audit["theorem_proved"] is False
assert audit["theorem_complete"] is False

print("check_anchor_audit: ok (exact pin/module, 5 candidates, M0-W candidate boundary)")
