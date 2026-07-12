#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0981-RELEASE."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0981"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
intake = load("intake.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0981")

assert target["execution_rank"] == 261
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert intake["lifecycle_mode"] == "planned"
assert intake["root_vector"] == {"human": "H1", "machine": "M3", "readability": "R3"}
assert intake["theorem_complete"] is False
assert registry["root_obligation_id"] == "M0981-ROOT"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

assert decision["item_id"] == "S56-M-0981-RELEASE"
assert decision["theorem_id"] == "THM-M-0981"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False
assert decision["root_vector"]["accepted_before"] == ["H1", "M3", "R3"]
assert decision["root_vector"]["accepted_after"] == ["H1", "M3", "R3"]

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0981-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"]
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False
assert proof["support_state"] == "provisional_worker_selftest"
assert proof["result"]["root_closed"] is True
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False

for name, expected in decision["reconciled_inputs"].items():
    assert digest(name) == expected, f"stale reconciled input: {name}"

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False and closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == [
    "M0981-L-EMPTY", "M0981-L-UNIT", "M0981-L-ADDITIVITY"
]
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "master acceptance", "typed-graph reconciliation", "AUDIT-Z",
    "H0 primary-source", "R0 node-specific", "transitive declaration",
    "empty-cache network-denied cold build", "SBOM and license",
    "two signed attestations", "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

for key in (
    "audit_inventory_acceptance", "human_source_acceptance", "readability_acceptance",
    "complete_trust_closure", "hermetic_release_reproduction", "supply_chain_closure",
    "independent_release_verification", "deterministic_release_bundle",
):
    assert decision["evidence_reconciliation"][key] == "missing"

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
)
assert replay.returncode == 0, replay.stdout
assert "PASS narrow kernel replay" in replay.stdout
assert "BLOCKED release gates" in replay.stdout

print("release-decision: ok (blocked; validation dependency unaccepted; H1/M3/R3 unchanged)")
print("validation replay: ok (exact root provisional; authoritative graph stale)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
