#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0536-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0536"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
graphs = load("typed-graphs.json")
targets = json.loads(
    (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)
target = next(
    (entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0536"),
    None,
)

assert target is not None and target["execution_rank"] == 593
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert instance["lifecycle"] == "planned" and instance["theorem_complete"] is False
assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}

assert decision["item_id"] == "S56-M-0536-RELEASE"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["root_vector"]["accepted_before"] == ["H1", "M4", "R4"]
assert decision["root_vector"]["accepted_after"] == ["H1", "M4", "R4"]
assert decision["root_vector"]["best_provisional_machine_evidence"] == "M0-W"
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0536-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["master_accepted"] is False
assert validation["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False
assert proof["support_state"] == "provisional_worker_selftest"
assert validation["result"]["root_closed"] is True
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_verification_gate"] == "fail_closed"

assert graphs["closure_boundary"]["accepted_root_closed"] is False
assert graphs["closure_boundary"]["audit_complete"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert decision["evidence_reconciliation"]["frozen_graph_reconciliation"].startswith("missing")
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["next_failed_theorem_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"

cut_set = "\n".join(decision["remaining_root_cut_set"])
for required in (
    "master acceptance",
    "stale frozen typed graph",
    "H0 primary-source",
    "R0 structured",
    "empty-cache network-denied cold build",
    "SBOM",
    "two signed attestations",
    "minimal release verifier",
    "mutation",
    "deterministic content-addressed release bundle",
):
    assert required in cut_set, f"release cut set omits {required!r}"

print(
    "PASS THM-M-0536 release reconciliation: blocked; provisional root check retained; "
    "audit_complete=false; theorem_complete=false"
)
