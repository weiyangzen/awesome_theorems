#!/usr/bin/env python3
"""Fail-closed release reconciliation check for THM-M-0987."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0987"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
intake = load("intake.json")
validation = load("validation-receipt.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0987")

assert target["execution_rank"] == 267
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
assert graphs["root_node_id"] == "M0987-ROOT"
root_node = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0987-ROOT")
assert root_node["machine_debt"] == "M3" and root_node["evidence_ids"] == []

assert decision["item_id"] == "S56-M-0987-RELEASE"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0987-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"]
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

assert validation["result"]["root_kernel_closed"] is True
assert validation["result"]["machine_debt"] == "M1"
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
root = decision["reconciled_root"]
assert root["kernel_closed_locally"] is True
assert root["remaining_mathematical_cut_set"] == []
assert root["audit_complete"] is root["theorem_complete"] is False
assert decision["root_vector"]["accepted_before"] == ["H2", "M3", "R3"]
assert decision["root_vector"]["accepted_after"] == ["H2", "M3", "R3"]
assert decision["root_vector"]["best_provisional_evidence"] == ["H2", "M1", "R3"]
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_assurance_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "master acceptance", "typed-graphs.json", "AUDIT-Z", "H0 primary-source",
    "R0 reconstruction", "transitive declaration provenance", "empty-cache network-denied",
    "SBOM and license", "two signed attestations", "minimal release verifier",
    "deterministic content-addressed",
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
assert "ok: exact frozen root, proof composition" in validation_check.stdout
assert "ok: observed axioms are propext, Classical.choice, and Quot.sound" in validation_check.stdout
assert "blocked: frozen state predates proof closure" in validation_check.stdout

print("release reconciliation ok: provisional validation receipt hash and frozen root agree")
print("release blocked: dependency is unaccepted and audit/release assurance remains open")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
