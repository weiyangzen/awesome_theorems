#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0398 release decision."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0398"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision failed: {message}")


def load(name: str) -> dict:
    return json.loads((DOSSIER / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((DOSSIER / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
registry = load("obligation-registry.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next((row for row in targets["targets"] if row["theorem_id"] == "THM-M-0398"), None)
if target is None or target["execution_rank"] != 11:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the blocked decision")
if instance["lifecycle"] != "planned" or instance["root_vector"] != {"H": "H1", "M": "M3", "R": "R4"}:
    fail("instance lifecycle or root vector drifted")
if instance["audit_complete"] is not False or instance["theorem_complete"] is not False:
    fail("instance unexpectedly records a terminal completion")

if decision["item_id"] != "S56-M-0398-RELEASE" or decision["verdict"] != "blocked":
    fail("wrong release item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("blocked worker reconciliation must not promote lifecycle")
if decision["accepted_receipt_ids"]:
    fail("worker-provisional evidence was represented as accepted")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("terminal decisions must remain false")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"] or dependency["receipt_id"] != validation["receipt_id"]:
    fail("validation dependency identity disagrees with its receipt")
if dependency["receipt_sha256"] != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")
if dependency["master_accepted"] is not False or validation["support_state"] != "provisional_worker_selftest":
    fail("validation dependency is not eligible for release acceptance")
if proof["support_state"] != "provisional_worker_selftest":
    fail("proof support state drifted")

result = validation["result"]
if result["root_closed"] is not False or result["theorem_complete"] is not False:
    fail("validation no longer records the open-root boundary")
if result["validated_closed_obligation_ids"] != ["M0398-T"]:
    fail("validated partial closure set drifted")
if len(registry["obligations"]) != 15 or registry["root_obligation_id"] != "M0398-ROOT":
    fail("frozen obligation registry drifted")

reconciliation = decision["evidence_reconciliation"]
if reconciliation["validated_closed_obligation_ids"] != ["M0398-T"]:
    fail("release reconciliation overstates partial closure")
if reconciliation["minimal_open_proof_cut"] != ["M0398-L4"]:
    fail("minimal open proof cut drifted")
for key in ("exact_root_kernel_check", "hermetic_release_reproduction",
            "independent_release_verification", "human_source_acceptance",
            "readability_acceptance", "release_bundle"):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")

cut = "\n".join(decision["remaining_root_cut_set"])
for fragment in ("M0398-L4", "H0 primary-source", "R0 structured",
                 "empty-cache network-denied cold build", "SBOM and license",
                 "two signed attestations", "minimal release verifier",
                 "deterministic content-addressed release bundle"):
    if fragment not in cut:
        fail(f"remaining cut set omits {fragment!r}")

print("release-decision: ok (blocked; validation unaccepted; M0398-L4/root open; audit_complete=false; theorem_complete=false)")
