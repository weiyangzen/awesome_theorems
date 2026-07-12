#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0534 release decision."""

import hashlib
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0534"


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
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next((entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0534"), None)
if target is None or target["execution_rank"] != 591:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the blocked decision")
if instance["lifecycle"] != "planned" or instance["theorem_complete"] is not False:
    fail("instance authority no longer records planned/open state")
if instance["root_vector"] != {"H": "H2", "M": "M3", "R": "R4"}:
    fail("accepted intake root vector drifted")

if decision["item_id"] != "S56-M-0534-RELEASE" or decision["verdict"] != "blocked":
    fail("release decision has the wrong item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("a blocked worker decision must not promote lifecycle")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("open release gates require both terminal booleans to remain false")
if decision["accepted_receipt_ids"]:
    fail("worker-provisional receipts must not be represented as accepted")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"]:
    fail("release dependency does not identify the validation receipt")
if validation["support_state"] != "provisional_worker_selftest" or dependency["master_accepted"] is not False:
    fail("validation evidence is not eligible for dependency acceptance")
if dependency["receipt_sha256"] != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")
if proof["support_state"] != "provisional_worker_selftest":
    fail("proof receipt support state drifted")

result = validation["result"]
if result["root_kernel_closed"] is not True or result["theorem_complete"] is not False:
    fail("validation closure boundary drifted")
closure = graphs["closure_boundary"]
if closure["root_closed"] is not False or closure["root_machine_debt"] != "M1":
    fail("the frozen pre-proof graph no longer has the recorded stale boundary")
if result["structured_state_freshness"].split(":", 1)[0] != "fail_closed":
    fail("validation no longer fails closed on structured-state freshness")

reconciliation = decision["evidence_reconciliation"]
for key in (
    "authoritative_graph_freshness",
    "complete_transitive_provenance",
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
    "stale pre-proof typed graph",
    "H0 primary-source",
    "R0 node-anchored",
    "empty-cache network-denied cold build",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
)
cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in required_cut_fragments:
    if fragment not in cut_set:
        fail(f"release cut set omits {fragment!r}")

print(
    "release-decision: ok (blocked; validation dependency unaccepted; exact root only "
    "provisional; audit_complete=false; theorem_complete=false)"
)
