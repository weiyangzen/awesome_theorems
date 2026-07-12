#!/usr/bin/env python3
"""Fail-closed consistency check for the THM-M-1270 release decision."""

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1270"


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
validation = load("validation-receipt.json")
graphs = load("typed-graphs.json")
intake = load("intake.json")
targets = json.loads(
    (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)
target = next(x for x in targets["targets"] if x["theorem_id"] == "THM-M-1270")

assert target["execution_rank"] == 163
assert target["lifecycle_mode"] == "planned"
assert target["theorem_complete"] is False
assert intake["lifecycle_mode"] == "planned"
assert intake["theorem_complete"] is False
assert decision["item_id"] == "S56-M-1270-RELEASE"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-1270-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == sha256("validation-receipt.json")
assert dependency["master_accepted"] is False
assert validation["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False

result = validation["result"]
boundary = graphs["closure_boundary"]
assert result["root_closed"] is False
assert result["root_machine_debt"] == "M3"
assert result["audit_complete"] is False
assert result["theorem_complete"] is False
assert boundary["root_closed"] is False
assert boundary["theorem_complete"] is False
assert decision["remaining_root_cut_set"] == result["remaining_root_cut_set"]

required_release_fragments = (
    "master acceptance",
    "descent-maximal-point",
    "accepted H0",
    "accepted R0",
    "empty-cache network-denied cold replay",
    "SBOM and license",
    "independently provisioned runners",
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
assert "open: exact root remains conditional" in replay.stdout
assert "blocked: cold hermetic replay" in replay.stdout

print("release-decision: ok (blocked; validation dependency unaccepted)")
print("open: exact root M3 with six frozen root-cut obligations")
print("open: audit H1/R3; AUDIT-Z and THEOREM-Z are false")
print("blocked: hermetic, supply-chain, independent-verifier, bundle, and master gates")
