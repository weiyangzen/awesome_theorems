#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0390 release decision."""

import hashlib
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0390"


def fail(message: str) -> None:
    print(f"release-decision: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(name: str) -> dict:
    return json.loads((DOSSIER / name).read_text())


def sha256(name: str) -> str:
    return hashlib.sha256((DOSSIER / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
units = load("proof-units.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())

target = next((entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0390"), None)
if target is None or target["execution_rank"] != 4:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the recorded fail-closed decision")
if instance["lifecycle"] != "planned" or instance["theorem_complete"] is not False:
    fail("instance authority no longer has the recorded planned/open state")

if decision["item_id"] != "S56-M-0390-RELEASE" or decision["verdict"] != "blocked":
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
if validation["support_state"] != "provisional_worker_selftest":
    fail("validation receipt is not the recorded worker-provisional evidence")
if dependency["master_accepted"] is not False:
    fail("worker-provisional validation was represented as master accepted")
if dependency["receipt_sha256"] != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")
if validation["result"]["theorem_complete"] is not False:
    fail("validation no longer supports an open-root release decision")

obligations = registry.get("obligations", [])
if len(obligations) != 14 or any(node.get("root_relevant") is not True for node in obligations):
    fail("the frozen fourteen-node root-relevant denominator drifted")
root = next((node for node in units.get("nodes", []) if node.get("node_id") == "THM-M-0390-ROOT"), None)
if root is None or root.get("machine_debt") not in {"M3", "M4", "M5"}:
    fail("exact root is not explicitly machine-open")

required_cut_fragments = (
    "kernel closure",
    "H0 primary-source",
    "R0 structured",
    "empty-cache network-denied cold build",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
)
cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in required_cut_fragments:
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

reconciliation = decision["evidence_reconciliation"]
for key in (
    "exact_root_kernel_check",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "human_source_acceptance",
    "readability_acceptance",
    "release_bundle",
):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")
if reconciliation.get("open_root_relevant_obligation_count") != 14:
    fail("release decision must not credit the NP.4 ledger step as a closed canonical obligation")

print(
    "release-decision: ok (blocked; dependency unaccepted; exact root open; "
    "audit_complete=false; theorem_complete=false; release cut set preserved)"
)
