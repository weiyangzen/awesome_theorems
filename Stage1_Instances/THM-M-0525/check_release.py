#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0525-RELEASE."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0525"

decision = json.loads((HERE / "release-decision.json").read_text())
validation = json.loads((HERE / "validation-receipt.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert decision["item_id"] == "S56-M-0525-RELEASE"
assert decision["theorem_id"] == validation["theorem_id"] == "THM-M-0525"
assert decision["depends_on"] == ["S56-M-0525-VALIDATION"]

for relative, expected in decision["inputs"].items():
    actual = hashlib.sha256((HERE / relative).read_bytes()).hexdigest()
    assert actual == expected, f"stale release input: {relative}"

root = next(node for node in graphs["nodes"] if node["node_id"] == "THM-M-0525-ROOT")
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["root_machine_debt"] == root["machine_debt"] == "M2"

evidence = decision["evidence_reconciliation"]
assert evidence["exact_root_kernel_checked_locally"] is True
required_release_gates = (
    "validation_dependency_master_accepted",
    "structured_root_state_fresh",
    "human_source_h0_accepted",
    "readability_r0_accepted",
    "transitive_tcb_and_provenance_accepted",
    "hermetic_cold_offline_replay",
    "sbom_and_license_closure",
    "distinct_runner_independent_verification",
    "deterministic_release_bundle",
    "master_acceptance",
)
assert all(evidence[gate] is False for gate in required_release_gates)

result = decision["decision"]
assert result["verdict"] == "blocked"
assert result["audit_complete"] is result["theorem_complete"] is False
assert result["release_accepted"] is False
assert result["accepted_receipt_ids"] == []
assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
assert result["first_failed_gate"] == "dependency.S56-M-0525-VALIDATION.master_acceptance"
assert decision["release_grade"] is False
assert decision["support_state"] == "provisional_worker_selftest"

print("PASS THM-M-0525 release reconciliation")
print("verdict=blocked audit_complete=false theorem_complete=false release_accepted=false")
print(f"first_failed_gate={result['first_failed_gate']}")
