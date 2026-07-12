#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0770 release decision."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0770"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0770")

assert target["execution_rank"] == 579
assert target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is instance["theorem_complete"] is False
assert instance["root_vector"] == {"human": "H1", "machine": "M3", "readability": "R3"}

assert decision["item_id"] == "S56-M-0770-RELEASE"
assert decision["theorem_id"] == "THM-M-0770"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["root_vector"]["accepted_before"] == decision["root_vector"]["accepted_after"] == ["H1", "M3", "R3"]
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0770-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["master_accepted"] is False
assert validation["support_state"] == proof["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False

result = validation["result"]
assert result["root_kernel_closed"] is True
assert result["audit_complete"] is result["theorem_complete"] is False
assert result["structured_state_freshness"].startswith("fail_closed")
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert decision["evidence_reconciliation"]["closed_obligation_ids"] == result["validated_closed_obligation_ids"]

required = (
    "master acceptance",
    "stale frozen graph",
    "H0 primary-source",
    "R0 unique anchored",
    "transitive proof-body provenance",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
)
cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in required:
    assert fragment in cut_set, f"missing release blocker: {fragment}"

for key in (
    "authoritative_graph_freshness",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "human_source_acceptance",
    "readability_acceptance",
    "release_bundle",
):
    assert decision["evidence_reconciliation"][key] == "missing"

print("release-decision: ok (blocked; validation unaccepted; release gates open; theorem_complete=false)")
