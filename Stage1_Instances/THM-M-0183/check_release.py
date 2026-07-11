#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0183 release decision."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0183"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
validation = load("validation-receipt.json")
targets = json.loads(
    (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)
target = next(
    entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0183"
)

assert target["execution_rank"] == 130
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False
assert instance["lifecycle"] == "planned"
assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
assert instance["audit_complete"] is False
assert instance["theorem_complete"] is False
assert instance["accepted_proof_state"] == []

assert decision["item_id"] == "S56-M-0183-RELEASE"
assert decision["theorem_id"] == "THM-M-0183"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["root_vector"]["accepted_before"] == ["H2", "M4", "R4"]
assert decision["root_vector"]["accepted_after"] == ["H2", "M4", "R4"]
terminal = decision["terminal_decisions"]
assert terminal["audit_complete"] is False
assert terminal["theorem_complete"] is False

for name, expected in decision["reconciled_inputs"].items():
    assert digest(name) == expected, f"reconciled input drifted: {name}"

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0183-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["receipt_support_state"] == validation["support_state"]
assert dependency["receipt_release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

result = validation["result"]
assert result["positive_root_closed"] is False
assert result["root_machine_debt"] == "M4"
assert result["remaining_root_cut_set"] == ["M0183-T-METRIC"]
assert result["countermodel_declaration"] == (
    "Stage1Instances.THMM0183.not_yauCalabiConjectureTarget"
)
assert result["audit_complete"] is False
assert result["theorem_complete"] is False
assert result["hermetic_release_gate"] == "fail_closed"
assert result["independent_verification_gate"] == "fail_closed"
assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M4"
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False

assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_theorem_gate"]["gate_id"] == (
    "S56-5.1-EXACT-TARGET-CONSISTENCY"
)
reconciliation = decision["evidence_reconciliation"]
assert reconciliation["exact_positive_root_kernel_closure"].startswith("failed:")
assert reconciliation["statement_consistency"].startswith("failed")
for key in (
    "human_source_acceptance",
    "readability_acceptance",
    "complete_trust_closure",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "deterministic_release_bundle",
):
    assert reconciliation[key] == "missing"

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "repair of the canonical Lean statement",
    "kernel closure of the repaired exact root",
    "H0 primary-source",
    "R0 structured",
    "foundation, axiom, trust",
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
assert "exact positive target is refuted" in replay.stdout
assert "cold hermetic replay" in replay.stdout

print("release-decision: ok (blocked; validation dependency unaccepted)")
print("validation replay: ok (checked exact negation; positive root M4)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
