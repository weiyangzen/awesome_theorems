#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0156-RELEASE."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0156"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
validation = load("validation-receipt.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next((x for x in targets["targets"] if x["theorem_id"] == "THM-M-0156"), None)

if target is None or target["execution_rank"] != 655:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target authority no longer supports the recorded open state")
if instance["lifecycle"] != "planned" or instance["theorem_complete"] is not False:
    fail("instance authority no longer supports the recorded planned/open state")
if instance["root_vector"] != {"H": "H1", "M": "M3", "R": "R4"}:
    fail("accepted root vector drifted")

if decision["item_id"] != "S56-M-0156-RELEASE" or decision["verdict"] != "blocked":
    fail("wrong release item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("blocked worker reconciliation must not advance lifecycle")
if decision["accepted_receipt_ids"]:
    fail("worker-provisional evidence was represented as accepted")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("open release gates require both terminal decisions to remain false")

for name, expected in decision["reconciled_inputs"].items():
    if digest(name) != expected:
        fail(f"reconciled input drifted: {name}")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"] or dependency["receipt_id"] != validation["receipt_id"]:
    fail("validation dependency identity mismatch")
if dependency["receipt_sha256"] != digest("validation-receipt.json"):
    fail("validation receipt digest mismatch")
if validation["support_state"] != "provisional_worker_selftest":
    fail("validation support state drifted")
if dependency["release_grade"] is not False or dependency["master_accepted"] is not False:
    fail("validation dependency was silently promoted")

result = validation["result"]
if result["root_machine_closed"] is not True or result["theorem_complete"] is not False:
    fail("provisional root/completion boundary drifted")
boundary = graphs["closure_boundary"]
if boundary["root_closed"] is not False or boundary["remaining_root_cut_set"] != ["M0156-B-CANDIDATE"]:
    fail("frozen graph no longer records the pre-proof open boundary")
if decision["root_vector"]["accepted_before"] != ["H1", "M3", "R4"]:
    fail("release root vector disagrees with instance authority")
if decision["root_vector"]["accepted_after"] != decision["root_vector"]["accepted_before"]:
    fail("release silently changed accepted debt state")
if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
    fail("first failed node gate drifted")
if decision["first_failed_release_gate"] != "S56-10.6-HERMETIC-COLD-BUILD":
    fail("first failed release gate drifted")

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "Master acceptance", "fresh authoritative structured graph", "AUDIT-Z",
    "H0 primary-source", "R0 node-by-node", "transitive declaration/body provenance",
    "empty-cache network-denied cold build", "SBOM and license", "Two signed attestations",
    "minimal verifier", "deterministic content-addressed release bundle", "THEOREM-Z",
):
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

for key in (
    "audit_inventory_reconciliation", "human_source_acceptance", "readability_acceptance",
    "complete_transitive_provenance_and_tcb", "hermetic_release_reproduction",
    "supply_chain_closure", "independent_release_verification", "deterministic_release_bundle",
):
    if decision["evidence_reconciliation"][key] != "missing":
        fail(f"release blocker {key!r} was silently cleared")

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT,
    capture_output=True, text=True, timeout=180, check=False,
)
if replay.returncode:
    fail(f"validation replay failed:\n{replay.stdout}{replay.stderr}")

print("release-decision: ok (blocked; dependency unaccepted; H1/M3/R4 unchanged)")
print("validation replay: ok (exact root provisional; authoritative graph stale)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
