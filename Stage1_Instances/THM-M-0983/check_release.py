#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0983-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0983"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
intake = load("intake.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(item for item in targets["targets"] if item["theorem_id"] == "THM-M-0983")

assert target["execution_rank"] == 263
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
assert intake["root_vector"] == {"human": "H1", "machine": "M3", "readability": "R3"}
assert registry["root_obligation_id"] == "M0983-ROOT"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

assert decision["item_id"] == "S56-M-0983-RELEASE"
assert decision["theorem_id"] == "THM-M-0983" and decision["intent"] == "release"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["root_vector"]["accepted_before"] == ["H1", "M3", "R3"]
assert decision["root_vector"]["accepted_after"] == ["H1", "M3", "R3"]
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0983-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

assert validation["result"]["root_kernel_closed"] is True
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["minimal_open_root_cut"] == [
    "M0983-R-PAIRWISE", "M0983-B-STRONG-LAW", "M0983-T-EXPECTATION"
]
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "typed-graph reconciliation", "AUDIT-Z", "H0 primary-source", "R0 readable",
    "transitive declaration/body provenance", "empty-cache network-denied cold build",
    "SBOM and license", "Two signed attestations", "minimal release verifier",
    "deterministic content-addressed release bundle", "Master acceptance of THEOREM-Z",
):
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

for key in (
    "audit_inventory_reconciliation", "human_source_acceptance", "readability_acceptance",
    "complete_provenance_and_trust_closure", "hermetic_release_reproduction",
    "independent_release_verification", "deterministic_release_bundle",
):
    assert decision["evidence_reconciliation"][key] == "missing"

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
)
assert replay.returncode == 0, replay.stdout
assert "exact proof root and independently reconstructed exact target kernel-replayed" in replay.stdout
assert "structured state predates proof closure" in replay.stdout

print("release-decision: ok (blocked; dependency unaccepted; H1/M3/R3 unchanged)")
print("validation replay: ok (exact root provisional; authoritative graph stale)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
