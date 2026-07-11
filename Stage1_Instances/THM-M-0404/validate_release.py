#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0404-RELEASE."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0404"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str):
    return json.loads((HERE / name).read_text())


spec = load("release-spec.json")
receipt = load("release-receipt.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
instance = load("instance.json")

assert spec["item_id"] == receipt["item_id"] == "S56-M-0404-RELEASE"
assert spec["theorem_id"] == receipt["theorem_id"] == "THM-M-0404"
for name, digest in receipt["inputs"].items():
    assert digest == sha256(HERE / name), name

result = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=150,
    check=False,
)
assert result.returncode == 0, result.stdout
assert "open: exact root has an explicit EventuallyPeriodicZeroSets premise" in result.stdout
assert "blocked: cold hermetic replay" in result.stdout

assert validation["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False
assert validation["result"]["root_closed"] is False
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["result"]["minimal_mathematical_open_root_cut_set"] == [
    "M0404-T-EVENTUAL"
]
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_verification_gate"] == "fail_closed"
assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert instance["lifecycle_mode"] == "planned"
assert instance["audit_complete"] is False
assert instance["theorem_complete"] is False

decision = receipt["decision"]
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["root_vector_before"] == decision["root_vector_after"] == [
    "H3", "M3", "R4"
]
assert decision["audit_complete"] is False
assert decision["theorem_complete"] is False
assert decision["accepted_receipt_ids"] == []
assert decision["first_failed_gate"] == "exact_root_kernel_closure"
assert decision["remaining_root_cut_set"] == ["M0404-T-EVENTUAL"]
assert receipt["release_grade"] is False
assert receipt["master_acceptance"] == "pending_and_not_claimed"

print("ok: upstream node-scoped validation replayed against pinned Lean/mathlib")
print("open: exact root M3; conditional composition is not root closure")
print("open: audit H3/R4; AUDIT-Z is not established")
print("blocked: hermetic, supply-chain, independent-verifier, and master-acceptance gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false; cut M0404-T-EVENTUAL")
