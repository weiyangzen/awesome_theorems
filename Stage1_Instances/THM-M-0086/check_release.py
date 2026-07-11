#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0086-RELEASE."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0086"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0086")

assert target["execution_rank"] == 134
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert instance["lifecycle"] == "planned" and instance["theorem_complete"] is False
assert instance["accepted_proof_state"] == []
assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
assert registry["root_obligation_id"] == "M0086-ROOT"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

assert decision["item_id"] == "S56-M-0086-RELEASE"
assert decision["theorem_id"] == "THM-M-0086"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False
assert decision["root_vector"]["accepted_before"] == ["H2", "M4", "R4"]
assert decision["root_vector"]["accepted_after"] == ["H2", "M4", "R4"]

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0086-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["receipt_support_state"] == validation["support_state"]
assert dependency["master_accepted"] is False
assert validation["release_grade"] is False
assert validation["result"]["theorem_complete"] is False

for name, expected in decision["reconciled_inputs"].items():
    assert digest(name) == expected, f"stale reconciled input: {name}"

assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert graphs["closure_boundary"]["remaining_root_cut_set"] == [
    "M0086-L-EMBED", "M0086-L-INJECTIVE", "M0086-L-PROJECTIVE"
]
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_specific_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "master acceptance", "frozen typed graph", "H0 pinpoint primary-source",
    "R0 unique structured", "transitive declaration", "empty-cache network-denied cold build",
    "SBOM and license", "two signed attestations", "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

for key in (
    "audit_inventory_acceptance", "human_source_acceptance", "readability_acceptance",
    "hermetic_release_reproduction", "supply_chain_closure",
    "independent_release_verification", "deterministic_release_bundle",
):
    assert decision["evidence_reconciliation"][key] == "missing"

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
)
assert replay.returncode == 0, replay.stdout
assert "exact statement and proof elaborate" in replay.stdout
assert "cold hermetic replay" in replay.stdout

print("release-decision: ok (blocked; validation dependency unaccepted; H2/M4/R4 unchanged)")
print("validation replay: ok (exact root provisional; release gates remain open)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
