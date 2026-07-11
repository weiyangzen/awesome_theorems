#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0393 release decision."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0393"


def load(name: str) -> dict:
    return json.loads((DOSSIER / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((DOSSIER / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
registry = load("obligation-registry.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0393")

assert target["execution_rank"] == 6
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert registry["root_vector"] == {"human": "H3", "machine": "M4", "readability": "R3"}
assert registry["theorem_complete"] is False

assert decision["item_id"] == "S56-M-0393-RELEASE"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["terminal_decisions"] == {
    "audit_complete": False,
    "theorem_complete": False,
    "audit_z": "blocked",
    "theorem_z": "blocked",
}
assert decision["accepted_receipt_ids"] == []

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0393-VALIDATION"
assert dependency["master_accepted"] is False
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert validation["support_state"] == proof["support_state"] == "provisional_worker_selftest"
assert validation["result"]["root_closed"] is False
assert validation["result"]["validated_closed_obligation_ids"] == []
assert validation["result"]["validated_partial_obligation_ids"] == ["M0393-N1"]

reconciliation = decision["evidence_reconciliation"]
assert reconciliation["closed_obligation_ids"] == []
assert reconciliation["partial_obligation_ids"] == ["M0393-N1"]
assert reconciliation["open_root_relevant_obligation_count"] == 17
for key in (
    "canonical_statement_replay",
    "exact_root_kernel_check",
    "root_composition",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "human_source_acceptance",
    "readability_acceptance",
    "release_bundle",
):
    assert reconciliation[key] == "missing"

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "all seventeen root-relevant obligations",
    "statement compilation defect",
    "H0 primary-source",
    "R0 structured",
    "empty-cache network-denied cold build",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut_set

print(
    "release-decision: ok (blocked; dependency unaccepted; root H3/M4/R3 open; "
    "audit_complete=false; theorem_complete=false)"
)
