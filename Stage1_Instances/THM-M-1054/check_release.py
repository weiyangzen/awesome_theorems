#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-1054 release decision."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
proof = load("proof-receipt.json")
targets = json.loads(
    (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)
target = next(entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-1054")

assert target["execution_rank"] == 246
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False
assert target["legacy_artifacts_accepted"] is False

assert decision["item_id"] == "S56-M-1054-RELEASE"
assert decision["depends_on"] == ["S56-M-1054-VALIDATION"]
assert decision["verdict"] == "blocked"
assert decision["support_state"] == "provisional_worker_selftest"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["root_vector_before"] == decision["root_vector_after"] == {
    "H": "H1", "M": "M1", "R": "R3"
}
assert decision["terminal_decisions"] == {
    "audit_complete": False, "theorem_complete": False
}
assert decision["accepted_receipt_ids"] == []

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"]
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"]
assert dependency["master_accepted"] is False
assert validation["root_decision"] == {
    "machine_debt": "M1",
    "kernel_closed": True,
    "audit_complete": False,
    "theorem_complete": False,
}
assert proof["machine_root_cut_set"] == []
assert proof["audit_complete"] is False and proof["theorem_complete"] is False

reconciliation = decision["evidence_reconciliation"]
for gate in (
    "accepted_foundation_profile",
    "complete_tcb_inventory",
    "human_source_acceptance",
    "readability_acceptance",
    "audit_terminal_acceptance",
    "hermetic_release_reproduction",
    "supply_chain_archive",
    "independent_release_verification",
    "deterministic_release_bundle",
    "master_acceptance",
):
    assert reconciliation[gate] == "missing", f"release gate silently cleared: {gate}"

required_cut_fragments = (
    "foundation profile",
    "TCB, SBOM, and license",
    "H0 primary-source",
    "AUDIT-Z",
    "empty-cache network-denied cold build",
    "distinct signed attestations",
    "minimal verifier",
    "deterministic content-addressed release bundle",
    "master acceptance",
)
cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in required_cut_fragments:
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

print(
    "PASS THM-M-1054 release: blocked; M1/H1/R3; "
    "audit_complete=false; theorem_complete=false"
)
