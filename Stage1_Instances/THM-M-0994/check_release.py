#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0994 release decision."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0994"


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
target = next((x for x in targets["targets"] if x["theorem_id"] == "THM-M-0994"), None)

if target is None or target["execution_rank"] != 274:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("manifest no longer supports the fail-closed release decision")
if instance["lifecycle"] != "planned" or instance["root_vector"] != {"H": "H2", "M": "M3", "R": "R4"}:
    fail("accepted lifecycle or root vector drifted")

for name, expected in decision["reconciled_inputs"].items():
    if digest(name) != expected:
        fail(f"reconciled input drifted: {name}")

if decision["item_id"] != "S56-M-0994-RELEASE" or decision["verdict"] != "blocked":
    fail("wrong release item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("blocked worker reconciliation must not advance lifecycle")
if decision["accepted_receipt_ids"]:
    fail("worker evidence was represented as accepted")
if decision["root_vector"]["before"] != ["H2", "M3", "R4"]:
    fail("release vector does not match structured intake authority")
if decision["root_vector"]["after"] != decision["root_vector"]["before"]:
    fail("release silently promoted the root vector")
if decision["terminal_decisions"] != {
    "audit_complete": False, "theorem_complete": False,
    "audit_z": "blocked", "theorem_z": "blocked",
}:
    fail("terminal decisions are not fail-closed")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"] or dependency["receipt_id"] != validation["receipt_id"]:
    fail("validation dependency identity mismatch")
if dependency["receipt_sha256"] != digest("validation-receipt.json"):
    fail("validation dependency digest drifted")
if validation["support_state"] != "provisional_worker_selftest" or dependency["master_accepted"] is not False:
    fail("validation dependency is incorrectly release-eligible")
if validation["result"]["root_kernel_closed"] is not True:
    fail("provisional exact-root kernel evidence unexpectedly disappeared")
if validation["result"]["theorem_complete"] is not False:
    fail("validation receipt unexpectedly claims theorem completion")
boundary = graphs["closure_boundary"]
if boundary["root_closed"] is not False or boundary["root_machine_debt"] != "M1":
    fail("frozen graph freshness boundary drifted")

required = (
    "master acceptance", "stale frozen graph", "H0 primary-source", "R0 structured",
    "proof-body provenance", "empty-cache network-denied cold build", "SBOM",
    "two signed attestations", "minimal release verifier", "protected CI",
    "deterministic content-addressed release bundle",
)
cut = "\n".join(decision["remaining_root_cut_set"])
for fragment in required:
    if fragment not in cut:
        fail(f"remaining root cut set omits {fragment!r}")

for key in (
    "human_source_acceptance", "readability_acceptance", "complete_provenance_and_tcb",
    "hermetic_release_reproduction", "supply_chain_closure",
    "independent_release_verification", "deterministic_release_bundle", "master_acceptance",
):
    if decision["evidence_reconciliation"][key] != "missing":
        fail(f"release blocker {key!r} was silently cleared")

replay = subprocess.run(
    [sys.executable, str(HERE / "check_validation.py")], cwd=ROOT,
    text=True, capture_output=True, timeout=180, check=False,
)
if replay.returncode:
    fail(f"upstream validation replay failed:\n{replay.stdout}{replay.stderr}")

print("release-decision: ok (blocked; validation dependency provisional; H2/M3/R4 unchanged)")
print("evidence: exact-root local kernel replay passed; hermetic and independent release gates remain open")
print("terminal: AUDIT-Z=false; THEOREM-Z=false; accepted receipts=none")
