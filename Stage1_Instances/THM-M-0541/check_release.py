#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0541-RELEASE."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0541"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))
target = next((row for row in targets["targets"] if row["theorem_id"] == "THM-M-0541"), None)

if target is None or target["execution_rank"] != 598:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target authority no longer supports the recorded open state")
if instance["lifecycle"] != "planned" or instance["theorem_complete"] is not False:
    fail("instance authority no longer supports the recorded planned/open state")
if instance["root_vector"] != {"H": "H2", "M": "M3", "R": "R4"}:
    fail("accepted instance root vector drifted")

if decision["item_id"] != "S56-M-0541-RELEASE" or decision["verdict"] != "blocked":
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
if graphs["registry_denominator_sha256"] != registry["denominator_sha256"]:
    fail("typed graph and frozen registry denominator disagree")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"] or dependency["receipt_id"] != validation["receipt_id"]:
    fail("validation dependency identity mismatch")
if dependency["receipt_sha256"] != digest("validation-receipt.json"):
    fail("validation receipt hash mismatch")
if validation["support_state"] != "provisional_worker_selftest" or dependency["master_accepted"] is not False:
    fail("validation evidence is not an unaccepted worker receipt")
if validation["release_grade"] is not False or dependency["release_grade"] is not False:
    fail("validation evidence became release-grade without reconciliation")

result = validation["result"]
if result["root_closed"] is not True or result["theorem_complete"] is not False:
    fail("validation root/completion boundary changed")
boundary = graphs["closure_boundary"]
if boundary["closed_obligations"] != [] or boundary["root_machine_debt"] != "M3" or boundary["theorem_complete"] is not False:
    fail("frozen graph no longer records its pre-proof open boundary")
if decision["root_vector"]["accepted_before"] != ["H2", "M3", "R4"]:
    fail("release root vector does not match instance authority")
if decision["root_vector"]["accepted_after"] != decision["root_vector"]["accepted_before"]:
    fail("release silently changed the accepted root vector")
if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
    fail("first failed node gate drifted")
if decision["first_failed_release_gate"] != "S56-10.6-HERMETIC-COLD-BUILD":
    fail("first failed release gate drifted")

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "reconciliation", "AUDIT-Z", "H0 primary-source", "R0 node-by-node",
    "transitive declaration/body provenance", "empty-cache network-denied cold build",
    "SBOM and license", "Two signed attestations", "minimal release verifier",
    "deterministic content-addressed release bundle", "THEOREM-Z",
):
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

for key in (
    "audit_inventory_reconciliation", "human_source_acceptance", "readability_acceptance",
    "complete_provenance_and_trust_closure", "hermetic_release_reproduction",
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

print("release-decision: ok (blocked; dependency unaccepted; H2/M3/R4 unchanged)")
print("validation replay: ok (exact root provisional; authoritative graph stale)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
