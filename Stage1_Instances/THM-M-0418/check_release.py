#!/usr/bin/env python3
"""Fail-closed release reconciliation check for THM-M-0418."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0418"
EXPECTED = {
    "validation-receipt.json": "4428976180855254dea58c8b3b9087a3a08d39f27d2b58ffd1c3662e37ff6e53",
    "proof-receipt.json": "beb3c6da6111fba947f8190106400d25ff92938189cfdd2f800257b7688916e5",
    "obligation-registry.json": "a24bce3a0c4b61ed36e0ca8bb05551b3ba20b5189c8558070166c883ed2cd8ce",
    "typed-graphs.json": "05d1f3df3f55f4f049e4a1c3ca17d8607272f0267125f6a47cd51f92bacb6db0",
    "statement.json": "4e2b5cdabdca11da80e4e55359661c4af23b7d23e8bea5d66a78914316d47202",
    "source-statement-crosswalk.md": "fc9af102b174353f4ccd13c25f54cf635e639a90aa27552a8d25653a70b7b628",
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
instance = json.loads((OWNED / "instance.json").read_text())

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
if instance["lifecycle"] != "planned" or instance["theorem_complete"]:
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
if not closure["root_closed"] or closure["root_machine_debt"] != "M0-W":
    fail("frozen graph no longer records the provisional M0-W root")
if closure["audit_complete"] or closure["theorem_complete"]:
    fail("frozen graph unexpectedly claims audit or theorem completion")
if set(closure["remaining_release_cut_set"]) != {
    "M0418-X-SOURCE",
    "R0 reconstruction",
    "hermetic and independent validation",
}:
    fail("frozen release cut set changed")

print("ok: upstream narrow Lean validation replayed against pinned Lean/mathlib")
print("ok: provisional exact-root M0-W candidate evidence reconciled without promotion")
print("open: H1/R2, accepted source/readability review, and authority reconciliation; AUDIT-Z is false")
print("blocked: dependency acceptance, hermetic, supply-chain, independent-verifier, and bundle gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts")
