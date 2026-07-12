#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0529-RELEASE."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0529"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next(x for x in targets["targets"] if x["theorem_id"] == "THM-M-0529")

assert target["execution_rank"] == 586
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert instance["theorem_complete"] is False and instance["accepted_proof_state"] == []
assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
assert registry["root_obligation_id"] == "M0529-ROOT"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

assert decision["item_id"] == "S56-M-0529-RELEASE"
assert decision["verdict"] == "blocked" and decision["release_grade"] is False
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["root_vector"]["accepted_before"] == ["H1", "M3", "R4"]
assert decision["root_vector"]["accepted_after"] == ["H1", "M3", "R4"]
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False

for name, expected in decision["reconciled_inputs"].items():
    assert digest(name) == expected, f"reconciled input drifted: {name}"

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0529-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False
assert proof["theorem_complete"] is False and validation["result"]["root_closed"] is True

root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0529-ROOT")
assert root["machine_debt"] == "M3" and root["readability_debt"] == "R4"
assert decision["evidence_reconciliation"]["structured_state_freshness"].startswith("failed:")
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "typed-graph reconciliation", "AUDIT-Z", "H0 primary-source", "R0 node-by-node",
    "transitive declaration", "empty-cache network-denied cold build", "SBOM and license",
    "Two signed attestations", "minimal release verifier", "deterministic content-addressed release bundle",
    "THEOREM-Z",
):
    assert fragment in cut_set, f"release cut set omits {fragment!r}"

for key in (
    "audit_inventory_reconciliation", "human_source_acceptance", "readability_acceptance",
    "complete_provenance_and_trust_closure", "hermetic_release_reproduction",
    "supply_chain_closure", "independent_release_verification", "deterministic_release_bundle",
):
    assert decision["evidence_reconciliation"][key] == "missing"

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180, check=False,
)
assert replay.returncode == 0, replay.stdout

print("release-decision: ok (blocked; dependency unaccepted; H1/M3/R4 unchanged)")
print("validation replay: ok (exact root provisional; authoritative state stale)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
