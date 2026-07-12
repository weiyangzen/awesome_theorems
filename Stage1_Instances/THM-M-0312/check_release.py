#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0312 release decision."""

import hashlib
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0312"


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

target = next((entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0312"), None)
if target is None or target["execution_rank"] != 814:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the blocked decision")
if instance["lifecycle"] != "planned" or instance["theorem_complete"] is not False:
    fail("instance no longer records planned and theorem-incomplete")
if instance["root_vector"] != {"H": "H1", "M": "M3", "R": "R3"}:
    fail("authoritative root vector drifted")

if decision["item_id"] != "S56-M-0312-RELEASE" or decision["verdict"] != "blocked":
    fail("release item or verdict is wrong")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("blocked worker decision must not promote lifecycle")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("terminal booleans must fail closed")
if decision["accepted_receipt_ids"]:
    fail("worker evidence cannot create accepted receipt IDs")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"]:
    fail("validation dependency identity drifted")
if validation["support_state"] != "provisional_worker_selftest":
    fail("validation receipt is no longer the recorded provisional evidence")
if dependency["master_accepted"] is not False:
    fail("worker decision cannot assert master acceptance")
if dependency["receipt_sha256"] != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")
if validation["result"]["audit_complete"] is not False:
    fail("validation unexpectedly claims audit completion")
if validation["result"]["theorem_complete"] is not False:
    fail("validation unexpectedly claims theorem completion")

reconciliation = decision["evidence_reconciliation"]
if reconciliation["proof_source_sha256"] != sha256("Proof.lean"):
    fail("proof source digest drifted")
if reconciliation["differential_source_sha256"] != sha256("Validation.lean"):
    fail("differential source digest drifted")
if reconciliation["observed_axioms"] != ["Classical.choice", "Quot.sound", "propext"]:
    fail("observed axiom boundary drifted")
for key in (
    "human_source_acceptance",
    "readability_acceptance",
    "hermetic_release_reproduction",
    "independent_release_verification",
    "release_bundle",
):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")

cut = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "master acceptance",
    "M0312-S-FOUNDATION",
    "H0 primary-source",
    "R0 structured",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    if fragment not in cut:
        fail(f"release cut set omits {fragment!r}")

print(
    "release-decision: ok (blocked; dependency unaccepted; authoritative state unreconciled; "
    "audit_complete=false; theorem_complete=false)"
)
