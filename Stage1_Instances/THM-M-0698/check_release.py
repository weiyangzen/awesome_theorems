#!/usr/bin/env python3
"""Fail-closed release reconciliation check for THM-M-0698."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0698"
UPSTREAM_HASHES = {
    "validation-receipt.json": "2ed0f716f284b5284b2eba6f26050779c619906d63cba01230b68e816206a5d6",
    "proof-receipt.json": "a26b9f36c8a9a2066290d530728586a175be3679a5d943ce3d8738b5fa3f208a",
    "obligation-registry.json": "b6badf160ca06f4bfa7de518b35175a2609f216932c9de139ac906ebc06cd1f0",
    "typed-graphs.json": "e7482376bb32dee19d7d68215c67dd0fc3d145a95f11aa7a1863a33b421d8fc4",
    "statement.json": "867fd13b43bc26216db39c541e0faf750874f0697a4cb52909242e8acec2d518",
}


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


for name, expected in UPSTREAM_HASHES.items():
    if digest(name) != expected:
        fail(f"release input hash mismatch: {name}")

validation = json.loads((HERE / "validation-receipt.json").read_text())
proof = json.loads((HERE / "proof-receipt.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
decision = json.loads((HERE / "release-decision.json").read_text())
spec = json.loads((HERE / "release-spec.json").read_text())

replay = subprocess.run(
    [sys.executable, str(HERE / "check_validation.py")], cwd=ROOT,
    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180,
)
if replay.returncode:
    fail(f"upstream validation replay failed\n{replay.stdout}")

if spec["recipe"]["argv"] != ["python3", "Stage1_Instances/THM-M-0698/check_release.py"]:
    fail("release recipe drift")
dependency = decision["dependency"]
if dependency["receipt_sha256"] != digest("validation-receipt.json"):
    fail("dependency receipt hash drift")
if dependency["receipt_id"] != validation["receipt_id"]:
    fail("dependency receipt identity drift")
if validation["support_state"] != "provisional_worker_selftest" or validation["release_grade"]:
    fail("validation is not the expected provisional nonrelease evidence")
if not proof["result"]["root_closed"] or validation["result"]["root_kernel_closed"] is not True:
    fail("provisional exact-root kernel evidence disappeared")

result = decision["decision"]
if result["verdict"] != "blocked" or result["lifecycle_after"] != "planned":
    fail("release verdict must remain blocked and planned")
if result["audit_complete"] or result["theorem_complete"] or result["accepted_receipt_ids"]:
    fail("negative terminal decision was promoted")
if result["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
    fail("unexpected first failed gate")

closure = graphs["closure_boundary"]
if closure["root_closed"] or closure["theorem_complete"]:
    fail("frozen authoritative graph unexpectedly claims completion")
if closure["remaining_root_cut_set"] != ["M0698-B-REVERSE"]:
    fail("frozen graph cut set drift")
for gate, value in decision["evidence_reconciliation"].items():
    if gate in {"exact_root_kernel_candidate", "observed_axioms"}:
        continue
    if value is not False:
        fail(f"open release gate promoted: {gate}")

print("PASS S56-M-0698-RELEASE negative reconciliation")
print("PASS upstream exact-root Lean validation replay; provisional M0-W candidate only")
print("BLOCKED first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
print("BLOCKED audit/H0/R0, graph freshness, hermetic, supply-chain, independent verifier, bundle, and master gates")
print("verdict=blocked lifecycle=planned audit_complete=false theorem_complete=false accepted_receipts=0")
