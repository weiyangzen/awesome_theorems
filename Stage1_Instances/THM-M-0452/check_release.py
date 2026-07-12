#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-0452 release decision."""

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
DOSSIER = ROOT / "Stage1_Instances/THM-M-0452"


def fail(message: str) -> None:
    print(f"release-decision: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(name: str) -> dict:
    return json.loads((DOSSIER / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((DOSSIER / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
graphs = load("typed-graphs.json")
statement = load("statement.json")
task_dag = load("task-dag.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next(
    (entry for entry in targets["targets"] if entry["theorem_id"] == "THM-M-0452"),
    None,
)
if target is None or target["execution_rank"] != 301:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the fail-closed decision")
if statement["theorem_complete"] is not False:
    fail("statement record unexpectedly claims theorem completion")

release_node = next(node for node in task_dag["nodes"] if node["id"] == decision["item_id"])
if release_node["depends_on"] != ["S56-M-0452-VALIDATION"] or release_node["state"] != "open":
    fail("authoritative task DAG no longer records an open release dependency")
if release_node["accepted_receipt_ids"]:
    fail("release node unexpectedly has an accepted receipt")

if decision["item_id"] != "S56-M-0452-RELEASE" or decision["verdict"] != "blocked":
    fail("release decision has the wrong item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("a blocked worker decision must not promote lifecycle")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("missing release gates require both terminal booleans to remain false")
if decision["accepted_receipt_ids"]:
    fail("worker-provisional evidence must not be represented as accepted")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"]:
    fail("release dependency does not identify the validation receipt")
if dependency["receipt_id"] != validation["receipt_id"]:
    fail("release dependency receipt ID drifted")
if validation["support_state"] != "provisional_worker_selftest":
    fail("validation evidence is no longer worker-provisional")
if dependency["master_accepted"] is not False:
    fail("worker decision cannot assert master acceptance")
if dependency["receipt_sha256"] != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")

result = validation["result"]
expected_closed = ["M0452-D-WELLDEFINED", "M0452-D-POSITIVE"]
if result["root_closed"] is not False or result["theorem_complete"] is not False:
    fail("validation receipt no longer records an open root")
if result["validated_closed_obligation_ids"] != expected_closed:
    fail("validation closure boundary drifted")
if graphs["closure_boundary"]["root_closed"] is not False:
    fail("frozen graph unexpectedly records root closure")
reconciliation = decision["evidence_reconciliation"]
if reconciliation["closed_obligation_ids"] != expected_closed:
    fail("release reconciliation overstates or understates partial closure")
if reconciliation["root_closed"] is not False:
    fail("release reconciliation unexpectedly closes the root")

required_cut_fragments = (
    "CanonicalHeightCore and PolarizationCore",
    "H0 primary-source",
    "R0 structured",
    "root provenance, axiom, trust, and transitive TCB closure",
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
    "release-decision: ok (blocked; dependency unaccepted; exact root open; "
    "audit_complete=false; theorem_complete=false)"
)
