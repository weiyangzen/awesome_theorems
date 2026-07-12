#!/usr/bin/env python3
"""Fail-closed release reconciliation check for THM-M-1028."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1028"


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
target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-1028")

assert target["execution_rank"] == 221
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert instance["lifecycle"] == "planned" and instance["theorem_complete"] is False
assert decision["item_id"] == "S56-M-1028-RELEASE"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-1028-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"]
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

closure = graphs["closure_boundary"]
root = decision["reconciled_root"]
assert registry["root_obligation_id"] == "M1028-ROOT"
assert root["machine_debt"] == "M2"
assert root["kernel_closed"] is closure["root_closed"] is False
assert root["remaining_root_cut_set"] == closure["remaining_root_cut_set"]
assert root["remaining_root_cut_set"] == [
    "M1028-C-CONTINUOUS-MODIFICATION", "M1028-T-NONDIFFERENTIABLE"
]
assert root["audit_complete"] is closure["audit_complete"] is False
assert root["theorem_complete"] is closure["theorem_complete"] is False
assert decision["terminal_decisions"] == {
    "audit_z": "blocked", "theorem_z": "blocked", "release": "blocked",
    "worker_item_selftest": "pass",
}
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_theorem_gate"] == "root.kernel_closure"

cut_set = "\n".join(decision["remaining_release_cut_set"])
for fragment in (
    "master acceptance", "M1028-C-CONTINUOUS-MODIFICATION",
    "M1028-T-NONDIFFERENTIABLE", "AUDIT-Z", "H0 primary-source", "R0 structured",
    "transitive provenance", "empty-cache network-denied cold build", "SBOM and license",
    "two signed attestations", "minimal release verifier", "deterministic content-addressed",
):
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

for key in (
    "audit_inventory_reconciliation", "human_source_acceptance", "readability_acceptance",
    "complete_trust_closure", "hermetic_release_reproduction", "supply_chain_archive",
    "independent_release_verification", "release_bundle",
):
    assert decision["evidence_reconciliation"][key] == "missing"

validation_check = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120, check=False,
)
assert validation_check.returncode == 0, validation_check.stdout
assert "root remains open (M2)" in validation_check.stdout

print("release reconciliation ok: provisional validation receipt hash and frozen root agree")
print("release blocked: exact Wiener root remains M2 with two substantive packages open")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
