#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0528-RELEASE."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0528"


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
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
target = next((row for row in targets["targets"] if row["theorem_id"] == "THM-M-0528"), None)

if target is None or target["execution_rank"] != 585:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target authority no longer supports the open decision")
if instance["lifecycle"] != "planned" or instance["theorem_complete"] is not False:
    fail("instance authority no longer supports the open decision")
if instance["root_vector"] != {"H": "H3", "M": "M3", "R": "R4"}:
    fail("accepted instance root vector drifted")

if decision["item_id"] != "S56-M-0528-RELEASE" or decision["verdict"] != "blocked":
    fail("wrong release item or verdict")
if decision["lifecycle_before"] != decision["lifecycle_after"] or decision["lifecycle_after"] != "planned":
    fail("blocked worker reconciliation must not advance lifecycle")
if decision["accepted_receipt_ids"]:
    fail("worker-provisional evidence was represented as accepted")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("open release gates require false terminal decisions")

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
    fail("validation is not a master-accepted dependency")
if validation["release_grade"] is not False or dependency["release_grade"] is not False:
    fail("validation evidence became release-grade without reconciliation")

result = validation["result"]
if result["root_kernel_closed"] is not True or result["theorem_complete"] is not False:
    fail("validation root/completion boundary changed")
boundary = graphs["closure_boundary"]
if boundary["root_closed"] is not False or boundary["remaining_root_cut_set"] != ["M0528-X-ANCHOR"]:
    fail("frozen pre-proof graph boundary changed")
if decision["root_vector"]["accepted_before"] != ["H3", "M3", "R4"]:
    fail("release root vector disagrees with instance authority")
if decision["root_vector"]["accepted_after"] != decision["root_vector"]["accepted_before"]:
    fail("release silently promoted the root vector")
if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
    fail("first failed node gate drifted")
if decision["first_failed_release_gate"] != "S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY":
    fail("first failed release gate drifted")

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in ("reconciliation", "H0 primary-source", "R0 unique anchored", "transitive declaration/body provenance", "empty-cache network-denied cold build", "SBOM and license", "Two signed attestations", "minimal receipt verifier", "deterministic content-addressed release bundle", "THEOREM-Z"):
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")], cwd=ROOT,
    capture_output=True, text=True, timeout=180, check=False,
)
if replay.returncode:
    fail(f"validation replay failed:\n{replay.stdout}{replay.stderr}")

print("release-decision: ok (blocked; dependency unaccepted; H3/M3/R4 unchanged)")
print("validation replay: ok (exact root provisional; authoritative graph stale)")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
