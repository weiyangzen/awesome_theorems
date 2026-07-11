#!/usr/bin/env python3
"""Fail-closed release reconciliation check for THM-M-0415."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0415"
EXPECTED = {
    "validation-receipt.json": "d4c2f134bd8701f9a81bbf44b739d3bbdc32f1776e77a7ea774e0e05b1379d8f",
    "proof-receipt.json": "c645b2826ad5c9175c29d6c0559d1268185ab8ec5d28c9ccece21f250fc87bf5",
    "obligation-registry.json": "5ef47516d28f8fffcf7005d13ca2736729041b53aaceeb09726fd958a9105016",
    "typed-graphs.json": "cda4d7b9979136e87b7ecbb97415c55137294b57a207129682cddbdef17bc10a",
    "statement.json": "c20cf727fa2f9f8837803dcef8eed8327fa12bb25d3260a282c3c92bcb06c5c0",
    "source-statement-crosswalk.md": "aceea04d44e31333acc135dddcd7d7230960db4667e7924c1d0f715f1ace0d6d",
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
if not validation["result"]["proof_phase_root_elaborated"]:
    fail("validation receipt no longer records exact-root elaboration")
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
if set(closure["remaining_root_cut_set"]) != {"M0415-X-PROVENANCE", "M0415-X-SOURCE"}:
    fail("frozen root cut set changed")

print("ok: upstream narrow Lean validation replayed against pinned Lean/mathlib")
print("ok: provisional exact-root M0-W candidate evidence reconciled without promotion")
print("open: H0/R0 and frozen source/provenance reconciliation; AUDIT-Z is false")
print("blocked: dependency acceptance, hermetic, supply-chain, independent-verifier, and bundle gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts")
