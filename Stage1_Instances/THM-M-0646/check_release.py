#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0646-RELEASE."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
instance = load("instance.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0646")

assert decision["item_id"] == "S56-M-0646-RELEASE"
assert decision["theorem_id"] == validation["theorem_id"] == instance["theorem_id"] == "THM-M-0646"
assert target["execution_rank"] == 692
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0646-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

assert validation["result"]["root_kernel_closed"] is True
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["audit_complete"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert instance["lifecycle"] == "planned"
assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
assert instance["audit_complete"] is instance["theorem_complete"] is False

result = decision["decision"]
assert result["verdict"] == "blocked"
assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
assert result["root_vector_before"] == result["root_vector_after"] == ["H2", "M4", "R4"]
assert result["audit_complete"] is result["theorem_complete"] is result["release_accepted"] is False
assert result["accepted_receipt_ids"] == []
assert result["first_failed_gate"].startswith("S56-10.2-DEPENDENCY-ACCEPTANCE")

gates = decision["evidence_reconciliation"]
assert gates["exact_root_kernel_replay"] == "provisional_pass"
assert gates["accepted_root_machine_state"] == "open_M4"
for name in (
    "authoritative_graph_reconciled", "pinpoint_h0_source_review",
    "independent_r0_review", "audit_z_accepted", "hermetic_cold_offline_replay",
    "tcb_sbom_license_closure", "independent_clean_runner_attestation",
    "independently_implemented_minimal_verifier", "deterministic_release_bundle",
    "master_acceptance",
):
    assert gates[name] is False, name

cut = "\n".join(result["remaining_root_cut_set"])
for fragment in ("graph reconciliation", "H0", "R0", "SBOM", "empty-cache",
                 "minimal verifier", "deterministic content-addressed"):
    assert fragment in cut, fragment

print("PASS S56-M-0646-RELEASE reconciliation")
print("verdict=blocked audit_complete=false theorem_complete=false release_accepted=false")
print(f"first_failed_gate={result['first_failed_gate']}")
