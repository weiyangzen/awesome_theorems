#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0166-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0166"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
intake = load("intake.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(item for item in targets["targets"] if item["theorem_id"] == "THM-M-0166")

assert target["execution_rank"] == 122
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
assert intake["root_vector"] == {"human": "H1", "machine": "M4", "readability": "R3"}

assert decision["item_id"] == "S56-M-0166-RELEASE"
assert decision["theorem_id"] == "THM-M-0166"
assert decision["verdict"] == "blocked" and decision["release_grade"] is False
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False
assert decision["root_vector"]["accepted_before"] == ["H1", "M4", "R3"]
assert decision["root_vector"]["accepted_after"] == ["H1", "M4", "R3"]

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0166-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["receipt_support_state"] == validation["support_state"]
assert dependency["master_accepted"] is False

obligations = {node["obligation_id"]: node for node in registry["obligations"]}
assert set(obligations) == set(graphs["coverage_denominators"]["canonical_obligations"])
assert len(obligations) == 7
assert obligations["M0166-ROOT"]["machine_debt"] == "M2"
assert obligations["M0166-C-PROPER"]["terminal_proof_body_id"] is None
assert obligations["M0166-L-EXISTENCE"]["terminal_proof_body_id"] is None
assert proof["closed_obligation_ids"] == ["M0166-L-SUBSEGMENT"]
assert validation["root_decision"] == {
    "machine_debt": "M2", "kernel_closed": False, "theorem_complete": False
}
assert validation["remaining_root_cut_set"] == ["M0166-C-PROPER", "M0166-L-EXISTENCE"]

assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
reconciliation = decision["evidence_reconciliation"]
assert reconciliation["validated_closed_obligation_ids"] == ["M0166-L-SUBSEGMENT"]
assert reconciliation["minimal_open_proof_cut"] == ["M0166-C-PROPER", "M0166-L-EXISTENCE"]
for key in (
    "exact_root_kernel_check", "audit_inventory_acceptance", "human_source_acceptance",
    "readability_acceptance", "complete_trust_closure", "hermetic_release_reproduction",
    "independent_release_verification", "release_bundle",
):
    assert reconciliation[key] == "missing"

cut = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "M0166-C-PROPER", "M0166-L-EXISTENCE", "AUDIT-Z", "H0 primary-source",
    "R0 structured", "empty-cache network-denied cold build", "SBOM and license",
    "two signed attestations", "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut, f"release cut set omits {fragment!r}"

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
)
assert replay.returncode == 0, replay.stdout
assert "root remains open M2" in replay.stdout

print("release-decision: ok (blocked; validation unaccepted; M0166 root open M2)")
print("validation replay: ok (exact statement and partial proof only)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
