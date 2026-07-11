#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0106 release decision."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0106"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
target = next(
    (item for item in targets["targets"] if item["theorem_id"] == "THM-M-0106"),
    None,
)

assert target is not None and target["execution_rank"] == 30
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert instance["execution"]["theorem_complete"] is False
assert instance["execution"]["accepted_execution_state"] == []
assert registry["root_obligation_id"] == "M0106-ROOT"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

assert decision["item_id"] == "S56-M-0106-RELEASE"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False
assert decision["root_vector"]["accepted_before"] == ["H4", "M2", "R4"]
assert decision["root_vector"]["accepted_after"] == ["H4", "M2", "R4"]

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0106-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"]
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False
assert proof["support_state"] == "provisional_worker_selftest"

assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "AUDIT-Z",
    "H0 primary-source",
    "R0 structured reconstruction",
    "transitive declaration",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

missing = decision["evidence_reconciliation"]
for key in (
    "audit_inventory_reconciliation",
    "human_source_acceptance",
    "readability_acceptance",
    "complete_trust_closure",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "release_bundle",
):
    assert missing[key] == "missing", f"release blocker {key!r} was cleared"

print(
    "release-decision: ok (blocked; dependency unaccepted; H4/M2/R4 unchanged; "
    "audit_complete=false; theorem_complete=false)"
)
