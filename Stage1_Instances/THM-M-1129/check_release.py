#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-1129-RELEASE."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1129"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next((entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-1129"), None)

if target is None or target["execution_rank"] != 334:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("manifest authority no longer supports the recorded open state")
if decision["item_id"] != "S56-M-1129-RELEASE" or decision["verdict"] != "blocked":
    fail("wrong release item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("negative worker reconciliation must not advance lifecycle")
if decision["root_vector_before"] != ["H2", "M3", "R3"]:
    fail("recorded root vector drifted")
if decision["root_vector_after"] != decision["root_vector_before"]:
    fail("release decision silently changed the root vector")
if decision["accepted_receipt_ids"]:
    fail("worker evidence was represented as accepted")
if any(decision["terminal_decisions"].values()):
    fail("open release gates require both terminal decisions to be false")

for name, expected in decision["reconciled_inputs"].items():
    if digest(name) != expected:
        fail(f"reconciled input drifted: {name}")
if graphs["registry_denominator_sha256"] != registry["denominator_sha256"]:
    fail("typed graph and frozen registry denominator disagree")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"] or dependency["receipt_id"] != validation["receipt_id"]:
    fail("validation dependency identity mismatch")
if dependency["receipt_sha256"] != digest("validation-receipt.json"):
    fail("validation receipt hash mismatch")
if validation["support_state"] != "provisional_worker_selftest" or validation["release_grade"] is not False:
    fail("validation support boundary drifted")
if dependency["master_accepted"] is not False:
    fail("worker cannot claim dependency acceptance")

boundary = graphs["closure_boundary"]
if boundary["root_closed"] is not False or boundary["theorem_complete"] is not False:
    fail("typed graph no longer records the open root")
if boundary["remaining_root_cut_set"] != ["M1129-T-REPRESENT"]:
    fail("minimal mathematical root cut drifted")
result = validation["result"]
if result["root_closed"] is not False or result["theorem_complete"] is not False:
    fail("validation receipt no longer supports the negative decision")
if result["minimal_open_root_cut_set"] != ["M1129-T-REPRESENT"]:
    fail("validation root cut disagrees")

if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
    fail("first node gate drifted")
if decision["first_failed_release_gate"] != "S56-10.6-HERMETIC-COLD-BUILD":
    fail("first release-specific gate drifted")
for key in (
    "exact_root_kernel_closure", "audit_z", "human_source_h0", "readability_r0",
    "provenance_and_trust", "hermetic_reproduction", "supply_chain",
    "independent_verification", "deterministic_bundle", "master_acceptance",
):
    if decision["release_gates"][key] not in {"failed", "missing", "incomplete", "pending"}:
        fail(f"release blocker {key!r} was silently cleared")

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT,
    capture_output=True, text=True, timeout=180, check=False,
)
if replay.returncode:
    fail(f"validation replay failed:\n{replay.stdout}{replay.stderr}")

print("release-decision: ok (blocked; H2/M3/R3 unchanged)")
print("validation replay: ok (conditional composition only; exact root open)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
