#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0391 release decision."""

import hashlib
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0391"


def fail(message: str) -> None:
    print(f"release-decision: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(name: str) -> dict:
    return json.loads((DOSSIER / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((DOSSIER / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next((entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0391"), None)
if target is None or target["execution_rank"] != 5:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the recorded fail-closed decision")
if instance["lifecycle"] != "planned" or instance["theorem_complete"] is not False:
    fail("instance authority no longer has the recorded planned/open state")
if instance["root_vector"] != {"H": "H1", "M": "M4", "R": "R4"}:
    fail("instance root vector drifted")

if decision["item_id"] != "S56-M-0391-RELEASE" or decision["verdict"] != "blocked":
    fail("release decision has the wrong item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("a blocked worker decision must not promote lifecycle")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("missing release gates require both terminal booleans to remain false")
if decision["accepted_receipt_ids"]:
    fail("worker-provisional receipts must not be represented as accepted")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"]:
    fail("release dependency does not identify the validation receipt")
if validation["support_state"] != "provisional_worker_selftest" or dependency["master_accepted"] is not False:
    fail("validation evidence is not eligible for release dependency acceptance")
if dependency["receipt_sha256"] != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")
if proof["support_state"] != "provisional_worker_selftest":
    fail("proof receipt support state drifted")

validation_result = validation["result"]
if validation_result["root_closed"] is not False or validation_result["theorem_complete"] is not False:
    fail("validation receipt no longer records an open root")
if validation_result["validated_closed_obligation_ids"] != ["M0391-B-EE"]:
    fail("release decision is stale against the validated closure boundary")
reconciliation = decision["evidence_reconciliation"]
if reconciliation["closed_obligation_ids"] != ["M0391-B-EE"]:
    fail("release reconciliation overstates or understates partial closure")
if reconciliation["open_root_relevant_obligation_count"] != 14:
    fail("release reconciliation has the wrong open-obligation count")

required_cut_fragments = (
    "fourteen open root-relevant obligations",
    "H0 primary-source",
    "R0 structured",
    "root provenance, axiom, trust, and TCB closure",
    "empty-cache network-denied cold build",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
)
cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in required_cut_fragments:
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

for key in (
    "exact_root_kernel_check",
    "root_composition",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "human_source_acceptance",
    "readability_acceptance",
    "release_bundle",
):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")

print(
    "release-decision: ok (blocked; dependency unaccepted; root open with 14 obligations; "
    "audit_complete=false; theorem_complete=false)"
)
