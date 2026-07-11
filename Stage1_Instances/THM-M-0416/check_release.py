#!/usr/bin/env python3
"""Fail-closed release reconciliation check for THM-M-0416."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0416"
EXPECTED = {
    "validation-receipt.json": "2d6f0dee6a334cfe89e78513cac27c1aad5e7873738e5633b9a765784117fbcc",
    "proof-receipt.json": "26bf8054c90f2fec0cab2fe61bca3823af04929268bbebcefbe98e99a258612c",
    "obligation-registry.json": "5c8bdb97fc222a201b7b940a20dfde39bcfdae488b3f2598638ebaaebf27db95",
    "typed-graphs.json": "f0ae41c76b14fcafb48fe3228b84c4750a0f940c1e97907e1446b9c5e4805df9",
    "statement.json": "35dd1027cc1d9d51ec10a1c52bd5f33e24d4b198a9f329e3538108207782e472",
    "source_statement_crosswalk.md": "f89f991e713f6a0bbaa878bb715c577e923053569c9627bb09169841b288cf90",
}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


for name, expected in EXPECTED.items():
    actual = hashlib.sha256((OWNED / name).read_bytes()).hexdigest()
    if actual != expected:
        fail(f"release input hash mismatch: {name}")

validation = json.loads((OWNED / "validation-receipt.json").read_text())
decision = json.loads((OWNED / "release-decision.json").read_text())
graphs = json.loads((OWNED / "typed-graphs.json").read_text())
intake = json.loads((OWNED / "intake.json").read_text())

result = subprocess.run(
    [sys.executable, str(OWNED / "check_validation.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
    timeout=180,
)
if result.returncode != 0:
    fail(f"upstream validation replay failed\n{result.stdout}{result.stderr}")

if validation["support_state"] != "provisional_worker_selftest" or validation["release_grade"]:
    fail("validation dependency is not the expected provisional nonrelease receipt")
if not validation["result"]["machine_root_closed"]:
    fail("validation receipt no longer records local exact-root closure")
if intake["lifecycle_mode"] != "planned" or intake["theorem_complete"]:
    fail("instance authority no longer records the planned, incomplete lifecycle")
if decision["verdict"] != "blocked" or decision["lifecycle_after"] != "planned":
    fail("release decision must remain blocked and planned")
if decision["accepted_receipt_ids"]:
    fail("worker release decision cannot contain accepted receipts")
if decision["terminal_decisions"] != {
    "audit_complete": False,
    "theorem_complete": False,
    "audit_z": "blocked",
    "theorem_z": "blocked",
}:
    fail("terminal decisions are not fail-closed")
if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
    fail("unexpected first failed gate")

closure = graphs["closure_boundary"]
if closure["root_closed"] or closure["theorem_complete"]:
    fail("frozen graph unexpectedly claims root or theorem completion")
if set(closure["remaining_root_cut_set"]) != {
    "M0416-I-FREE",
    "M0416-I-FINITE",
    "M0416-T-RANK",
    "M0416-T-COORDINATES",
}:
    fail("frozen root cut set changed")

print("ok: upstream narrow Lean validation replayed against pinned Lean/mathlib")
print("ok: provisional exact-root M0-W candidate evidence reconciled without promotion")
print("open: H1/R3 and frozen graph reconciliation; AUDIT-Z is false")
print("blocked: dependency acceptance, hermetic, supply-chain, independent-verifier, and bundle gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts")
