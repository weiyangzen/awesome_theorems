#!/usr/bin/env python3
"""Fail-closed consistency and kernel replay for S56-M-0118-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0118"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
intake = load("intake.json")
proof = load("proof-blocker.json")
validation = load("validation-receipt.json")
targets = json.loads(
    (ROOT / "Docs" / "Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)
target = next(entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0118")

assert target["execution_rank"] == 329
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False
assert intake["lifecycle_mode"] == "planned"
assert intake["root_vector"] == {"human": "H2", "machine": "M4", "readability": "R3"}

assert decision["item_id"] == "S56-M-0118-RELEASE"
assert decision["theorem_id"] == "THM-M-0118"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["provisional_receipt_ids_inspected"] == []
assert decision["root_vector"]["accepted_before"] == ["H2", "M4", "R3"]
assert decision["root_vector"]["accepted_after"] == ["H2", "M4", "R3"]
assert decision["root_vector"]["best_provisional_evidence"] == ["H5", "M5", "R3"]
terminal = decision["terminal_decisions"]
assert terminal["audit_complete"] is False
assert terminal["theorem_complete"] is False

for name, expected in decision["reconciled_inputs"].items():
    assert digest(name) == expected, f"reconciled input drifted: {name}"

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0118-VALIDATION"
assert dependency["receipt_id"] is None
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["receipt_support_state"] == validation["gate_state"]
assert dependency["receipt_release_grade"] is False
assert dependency["master_accepted"] is False

assert proof["result"] == "blocked_by_checked_countermodel"
assert proof["root_closed"] is False
assert proof["theorem_complete"] is False
assert validation["result"] == "blocked"
assert validation["root_vector_after"] == {"H": "H5", "M": "M5", "R": "R3"}
assert validation["audit_complete"] is False
assert validation["theorem_complete"] is False
assert validation["positive_root_precondition"]["result"] == "fail"
assert validation["hermetic_release_gate"]["result"] == "not_run"
assert validation["independent_release_gate"]["result"] == "not_run"

assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_theorem_gate"]["gate_id"] == "S56-5.1-EXACT-TARGET-CONSISTENCY"
reconciliation = decision["evidence_reconciliation"]
assert reconciliation["exact_positive_root_kernel_closure"].startswith("failed:")
for key in (
    "human_source_acceptance",
    "readability_acceptance",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "deterministic_release_bundle",
):
    assert reconciliation[key] == "missing"

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "replacement of the disconnected abstract fields",
    "kernel closure of the repaired exact root",
    "H0 primary-source",
    "R0 structured",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=180,
    check=False,
)
assert replay.returncode == 0, replay.stdout
assert "independent ZMod 2 model confirms the frozen root is false" in replay.stdout
assert "VALIDATION BLOCKED" in replay.stdout

print("release-decision: ok (blocked; validation dependency unaccepted)")
print("validation replay: ok (independent checked countermodel; positive root M5)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
