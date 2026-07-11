#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0389 release decision."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances" / "THM-M-0389"


def fail(message: str) -> None:
    print(f"release-decision: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(name: str) -> dict:
    return json.loads((DOSSIER / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((DOSSIER / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next((row for row in targets["targets"] if row["theorem_id"] == "THM-M-0389"), None)
if target is None or target["execution_rank"] != 20:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the recorded fail-closed decision")
if instance["lifecycle_mode"] != "planned" or instance["assurance"]["theorem_complete"] is not False:
    fail("instance authority no longer has the recorded planned/open state")
if [instance["assurance"][key] for key in ("human_source", "machine", "readability")] != ["H4", "M3", "R3"]:
    fail("accepted root vector drifted")

if decision["item_id"] != "S56-M-0389-RELEASE" or decision["verdict"] != "blocked":
    fail("release decision has the wrong item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("blocked worker decision must not promote lifecycle")
if decision["accepted_receipt_ids"]:
    fail("worker-provisional receipts must not be represented as accepted")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("open release gates require both terminal booleans to remain false")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"]:
    fail("release dependency does not identify the validation receipt")
if validation["support_state"] != "provisional_worker_selftest" or dependency["master_accepted"] is not False:
    fail("validation evidence is not eligible for dependency acceptance")
if dependency["receipt_sha256"] != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")
result = validation["result"]
if result["root_kernel_closed"] is not True or result["theorem_complete"] is not False:
    fail("release decision disagrees with provisional kernel closure or terminal status")
if result["axioms"] != ["propext", "Classical.choice", "Quot.sound"]:
    fail("validated root axiom profile drifted")

reconciliation = decision["evidence_reconciliation"]
for key in (
    "hermetic_release_reproduction",
    "independent_release_verification",
    "human_source_acceptance",
    "readability_acceptance",
    "release_bundle",
):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")

required_cut_fragments = (
    "master acceptance",
    "H0 primary-source",
    "R0 structured",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
)
cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in required_cut_fragments:
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

replay = subprocess.run(
    ["python3", str(DOSSIER / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=240,
    check=False,
)
if replay.returncode != 0 or "validation ok:" not in replay.stdout:
    fail(f"upstream validation replay failed\n{replay.stdout}")

print("release-decision: ok (blocked; dependency provisional; root kernel evidence local only; audit_complete=false; theorem_complete=false)")
