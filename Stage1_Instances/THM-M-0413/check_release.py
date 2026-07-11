#!/usr/bin/env python3
"""Fail-closed release reconciliation check for THM-M-0413."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0413"
EXPECTED = {
    "validation-receipt.json": "102a66da24df1e62fb0d55c1a29eff9158af3ae88a05817e31c88b3722dea6f1",
    "proof-receipt.json": "13f84f3ae0b1b176b9ed7f94e8fa7c3c09d082a7ec63ba10bbfb837ab05eb8d7",
    "obligation-registry.json": "884be3f3bf1c3ab8a7b18463147e604c55d020d399b0abcb9ceb7c39c16e752d",
    "typed-graphs.json": "167d81820491367fab533ed337b7b780a0c3e5b0c3ea711d288aac88be54a2a2",
    "statement.json": "61ade3e1b30b6350c5c89990177dc7beeb540fa4c7dd776e755084a0343bc56f",
    "source_statement_crosswalk.md": "0798e27c04075f05a281ca79fcef78015286f4b2fecc0f7522bd25a7931982ea",
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
if not validation["result"]["root_kernel_closed_locally"]:
    fail("validation receipt no longer records local exact-root closure")
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

open_composition = [
    edge for edge in graphs["proof_graph"]["composition_edges"] if edge["status"] == "open"
]
if len(open_composition) != 4:
    fail("frozen graph no longer has the four recorded open composition edges")
trust_edges = graphs["trust_graph"]["edges"]
if not any(edge.get("status") == "open_release_gate" for edge in trust_edges):
    fail("frozen graph no longer records the open release trust gate")

print("ok: upstream narrow Lean validation replayed against pinned Lean/mathlib")
print("ok: provisional exact-root M0-W candidate evidence reconciled without promotion")
print("open: H1/R3 audit and frozen composition/trust reconciliation; AUDIT-Z is false")
print("blocked: dependency acceptance, hermetic, supply-chain, independent-verifier, and bundle gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts")
