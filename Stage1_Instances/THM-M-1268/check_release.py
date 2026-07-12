#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-1268 release decision."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1268"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
dag = load("task-dag.json")
graphs = load("typed-graphs.json")
validation = load("validation-receipt.json")
targets = json.loads(
    (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)
target = next(x for x in targets["targets"] if x["theorem_id"] == "THM-M-1268")

assert target["execution_rank"] == 444
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False
assert instance["lifecycle"] == "planned"
assert instance["theorem_complete"] is False
assert decision["item_id"] == "S56-M-1268-RELEASE"
assert decision["theorem_id"] == instance["theorem_id"] == validation["theorem_id"]
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["root_vector_before"] == decision["root_vector_after"] == instance["root_vector"]
assert decision["accepted_receipt_ids"] == dag["accepted_states"] == []
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False

tasks = {task["id"]: task for task in dag["tasks"]}
assert tasks["S56-M-1268-VALIDATION"]["state"] == "open"
assert tasks["S56-M-1268-RELEASE"]["state"] == "open"
dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-1268-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256("validation-receipt.json")
assert dependency["master_accepted"] is False
assert validation["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False

boundary = graphs["closure_boundary"]
result = validation["result"]
assert boundary["root_closed"] is decision["authoritative_root_closed"] is False
assert boundary["audit_complete"] is result["audit_complete"] is False
assert boundary["theorem_complete"] is result["theorem_complete"] is False
assert boundary["root_machine_debt"] == "M4"
assert decision["remaining_root_cut_set"] == boundary["remaining_root_cut_set"]
assert result["hermetic_release_gate"] == "fail_closed"
assert result["independent_verification_gate"] == "fail_closed"
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

required_release_fragments = (
    "master acceptance",
    "AUDIT-Z",
    "accepted H0",
    "accepted R0",
    "empty-cache network-denied cold replay",
    "SBOM, licenses",
    "independently provisioned clean runners",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
)
release_cut = "\n".join(decision["release_gate_cut_set"])
for fragment in required_release_fragments:
    assert fragment in release_cut, fragment

replay = subprocess.run(
    ["python3", str(HERE / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=150,
    check=False,
)
assert replay.returncode == 0, replay.stdout
assert "stale: authoritative frozen graph" in replay.stdout
assert "blocked: cold empty-cache hermetic replay" in replay.stdout

print("release-decision: ok (blocked; validation dependency unaccepted)")
print("open: authoritative M4 root with three frozen root-cut obligations")
print("open: H2/R4; AUDIT-Z and THEOREM-Z are false")
print("blocked: hermetic, supply-chain, independent-verifier, bundle, and master gates")
