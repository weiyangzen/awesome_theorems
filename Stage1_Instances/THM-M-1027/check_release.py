#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-1027 release decision."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1027"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
graphs = load("typed-graphs.json")
registry = load("obligation-registry.json")
intake = load("intake.json")
targets = json.loads(
    (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)
target = next(
    (entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-1027"),
    None,
)

if target is None or target["execution_rank"] != 218:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target authority no longer supports the recorded open state")
if decision["item_id"] != "S56-M-1027-RELEASE" or decision["verdict"] != "blocked":
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
if dependency["item_id"] != validation["item_id"]:
    fail("validation dependency identity mismatch")
if dependency["receipt_id"] != validation["receipt_id"]:
    fail("validation receipt identity mismatch")
if dependency["receipt_sha256"] != digest("validation-receipt.json"):
    fail("validation dependency hash mismatch")
if validation["support_state"] != "provisional_worker_selftest":
    fail("validation support state drifted")
if dependency["master_accepted"] is not False or validation["release_grade"] is not False:
    fail("validation evidence is not eligible for release dependency acceptance")

boundary = graphs["closure_boundary"]
if boundary["root_closed"] is not False or boundary["theorem_complete"] is not False:
    fail("authoritative graph no longer records the open root")
if validation["result"]["root_closed"] is not False:
    fail("validation no longer records the open exact root")
if validation["result"]["remaining_root_cut_set"] != ["M1027-X-EXTERNAL"]:
    fail("validation root cut set drifted")
if registry["status_observed_after_freeze"]["root_machine_debt"] != "M3":
    fail("registry root machine debt drifted")
accepted = [intake["root_vector"][axis] for axis in ("human", "machine", "readability")]
if decision["root_vector"]["accepted_before"] != accepted:
    fail("release root vector does not match the planned instance")
if decision["root_vector"]["accepted_after"] != accepted:
    fail("release silently changed the accepted root vector")

required = (
    "master acceptance",
    "M1027-X-EXTERNAL",
    "stale frozen typed graph",
    "H0 primary-source",
    "R0 unique anchored structured reconstruction",
    "executable/bootstrap TCB closure",
    "empty-cache network-denied cold build",
    "SBOM and license closure",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
)
cut = "\n".join(decision["remaining_root_cut_set"])
for fragment in required:
    if fragment not in cut:
        fail(f"release cut set omits {fragment!r}")

for key in (
    "authoritative_root_closure",
    "structured_state_freshness",
    "human_source_acceptance",
    "readability_acceptance",
    "hermetic_release_reproduction",
    "supply_chain_closure",
    "independent_release_verification",
    "deterministic_release_bundle",
    "master_acceptance",
):
    if not decision["evidence_reconciliation"][key].startswith("missing"):
        fail(f"release blocker {key!r} was silently cleared")

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
    timeout=180,
    check=False,
)
if replay.returncode:
    fail(f"validation replay failed:\n{replay.stdout}{replay.stderr}")

print(
    "release-decision: ok (blocked; dependency unaccepted; exact root "
    "H1/M3/R3 and open; AUDIT-Z=false; THEOREM-Z=false)"
)
