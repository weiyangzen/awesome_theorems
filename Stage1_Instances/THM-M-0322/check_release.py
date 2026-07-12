#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0322 release decision."""

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0322"


def fail(message: str) -> None:
    print(f"release-decision: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
validation = load("validation-receipt.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next((entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0322"), None)
if target is None or target["execution_rank"] != 819:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the fail-closed decision")
expected_vector = {"H": "H2", "M": "M3", "R": "R4"}
if instance["lifecycle"] != "planned" or instance["root_vector"] != expected_vector:
    fail("instance lifecycle or root vector drifted")
if instance["audit_complete"] is not False or instance["theorem_complete"] is not False:
    fail("instance authority unexpectedly claims a terminal state")

if decision["item_id"] != "S56-M-0322-RELEASE" or decision["verdict"] != "blocked":
    fail("release decision has the wrong item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("blocked release decision must not promote lifecycle")
if decision["root_vector_before"] != expected_vector or decision["root_vector_after"] != expected_vector:
    fail("blocked release decision must preserve the authoritative root vector")
if any(decision["terminal_decisions"].values()):
    fail("missing release gates require both terminal decisions to remain false")
if decision["accepted_receipt_ids"]:
    fail("worker-provisional receipts cannot be represented as accepted")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"] or dependency["receipt_id"] != validation["receipt_id"]:
    fail("release dependency does not identify the validation receipt")
if dependency["receipt_sha256"] != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")
if validation["support_state"] != "provisional_worker_selftest" or dependency["master_accepted"] is not False:
    fail("validation dependency is not correctly classified as unaccepted worker evidence")
if validation["result"]["exact_root_kernel_closed"] is not True:
    fail("provisional exact-root kernel evidence drifted")
if validation["result"]["audit_complete"] is not False or validation["result"]["theorem_complete"] is not False:
    fail("validation receipt unexpectedly claims a terminal decision")

if decision["first_failed_gate"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
    fail("first failed gate is not dependency acceptance")
reconciliation = decision["evidence_reconciliation"]
for key in (
    "authoritative_graph_reconciliation",
    "human_source_acceptance",
    "readability_acceptance",
    "transitive_provenance_and_tcb_closure",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "supply_chain_archive",
    "deterministic_release_bundle",
    "master_acceptance",
):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in ("H0", "R0", "empty-cache", "SBOM", "Two distinct signed", "minimal release verifier", "deterministic"):
    if fragment not in cut_set:
        fail(f"remaining root cut set omits {fragment!r}")

print(
    "release-decision: ok (blocked at dependency acceptance; provisional exact root only; "
    "audit_complete=false; theorem_complete=false)"
)
