#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-1082 release decision."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1082"


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
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8"))

target = next((x for x in targets["targets"] if x["theorem_id"] == "THM-M-1082"), None)
if target is None or target["execution_rank"] != 524:
    fail("target membership or execution rank drifted")
if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
    fail("target manifest no longer supports the fail-closed decision")
if instance["lifecycle"] != "planned" or instance["theorem_complete"] is not False:
    fail("instance authority no longer records the planned incomplete state")
if instance["root_vector"] != {"H": "H2", "M": "M4", "R": "R4"}:
    fail("accepted instance root vector drifted")

if decision["item_id"] != "S56-M-1082-RELEASE" or decision["verdict"] != "blocked":
    fail("release decision has the wrong item or verdict")
if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
    fail("blocked worker decision must not promote lifecycle")
if decision["accepted_receipt_ids"]:
    fail("worker-provisional receipts cannot be represented as accepted")
terminal = decision["terminal_decisions"]
if terminal["audit_complete"] is not False or terminal["theorem_complete"] is not False:
    fail("open release gates require both terminal decisions to remain false")

dependency = decision["dependency"]
if dependency["item_id"] != validation["item_id"]:
    fail("release dependency does not identify the validation item")
if dependency["receipt_id"] != validation["receipt_id"]:
    fail("release dependency receipt id drifted")
if dependency["receipt_sha256"] != sha256("validation-receipt.json"):
    fail("validation receipt digest drifted")
if validation["support_state"] != "provisional_worker_selftest":
    fail("validation is not the recorded provisional worker evidence")
if validation["release_grade"] is not False or dependency["master_accepted"] is not False:
    fail("validation evidence is ineligible for release dependency acceptance")

result = validation["result"]
if result["audit_complete"] is not False or result["theorem_complete"] is not False:
    fail("validation receipt no longer records both terminal decisions as open")
if result["hermetic_release_gate"] != "fail_closed":
    fail("hermetic release blocker was silently cleared")
if result["independent_distinct_runner_gate"] != "fail_closed":
    fail("independent-runner blocker was silently cleared")
if registry["status_observed_after_freeze"]["root_machine_debt"] != "M3":
    fail("frozen registry root state drifted")
root = next(x for x in graphs["nodes"] if x["obligation_id"] == "M1082-ROOT")
if root["machine_debt"] != "M3" or root["human_debt"] != "H2" or root["readability_debt"] != "R4":
    fail("frozen graph root boundary drifted")

reconciliation = decision["evidence_reconciliation"]
for key in (
    "authoritative_root_state_reconciliation",
    "human_source_acceptance",
    "readability_acceptance",
    "complete_tcb_and_provenance",
    "hermetic_release_reproduction",
    "supply_chain_archive",
    "independent_release_verification",
    "deterministic_release_bundle",
):
    if reconciliation.get(key) != "missing":
        fail(f"release blocker {key!r} was silently cleared")

required_cut_fragments = (
    "master acceptance",
    "authoritative M4 instance",
    "accepted H0 primary-source",
    "accepted R0 anchored",
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
    [sys.executable, str(HERE / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=150,
    check=False,
)
if replay.returncode != 0:
    fail(f"upstream validation replay failed:\n{replay.stdout}")
if "PASS THM-M-1082 validation" not in replay.stdout:
    fail("upstream replay did not cover the exact root")
if "BLOCKED release gates" not in replay.stdout:
    fail("upstream replay did not preserve its release boundary")

print(
    "release-decision: ok (blocked; validation unaccepted; H2/R4 and release gates open; "
    "audit_complete=false; theorem_complete=false)"
)
