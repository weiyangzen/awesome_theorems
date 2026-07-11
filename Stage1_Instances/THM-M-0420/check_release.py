#!/usr/bin/env python3
"""Fail-closed release reconciliation check for THM-M-0420."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0420"
EXPECTED = {
    "validation-receipt.json": "f5fc5c971a013693df91ec74c6d667296b583cf864a9eea98d6402ff13427459",
    "obligation-registry.json": "ce872985846b4565ef1973d2021c36cbb66a6fe01338633e2799d5eab71970a9",
    "typed-graphs.json": "1ccae2101ed73c52d6d1dc7fdda738abac232df189d793e9b5b72eec0de81aed",
    "statement.json": "d724f524597c921180d01fe7d73aeadfa4ced3c25f2a021f5df9d4b52b408637",
    "source_statement_crosswalk.md": "e94b40056c36f3494030d022fb1be6c21dc06379493e1451219462933dbea1fd",
    "proof-phase.json": "dda119f77af822813f6eba273bfd587d6e5ca56702eff41cd7c13882ae2dc9c6",
}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def digest(name: str) -> str:
    return hashlib.sha256((OWNED / name).read_bytes()).hexdigest()


for name, expected in EXPECTED.items():
    if digest(name) != expected:
        fail(f"release input hash mismatch: {name}")

validation = json.loads((OWNED / "validation-receipt.json").read_text())
decision = json.loads((OWNED / "release-decision.json").read_text())
graphs = json.loads((OWNED / "typed-graphs.json").read_text())
proof = json.loads((OWNED / "proof-phase.json").read_text())
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
if validation["result"]["authoritative_root_closed"]:
    fail("validation receipt unexpectedly records exact-root closure")
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
    fail("unexpected first failed workflow gate")
if decision["first_failed_theorem_gate"]["gate_id"] != "S56-M-0420-EXACT-ROOT-KERNEL-CLOSURE":
    fail("unexpected first failed theorem gate")

closure = graphs["closure_boundary"]
expected_cut = ["M0420-C", "M0420-L1", "M0420-L2", "M0420-L3", "M0420-L4"]
if closure["root_closed"] or closure["theorem_complete"]:
    fail("frozen graph unexpectedly claims root or theorem completion")
if closure["remaining_root_cut_set"] != expected_cut:
    fail("frozen root cut set changed")
if proof["closed_obligation_ids"] != ["M0420-N1"]:
    fail("local proof closure boundary changed")
if decision["evidence_reconciliation"]["accepted_closed_obligation_ids"]:
    fail("provisional obligation closure was represented as accepted")

cut_text = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "M0420-C",
    "M0420-L1",
    "M0420-L2",
    "M0420-L3",
    "M0420-L4",
    "H0 primary-source",
    "R0 structured",
    "empty-cache network-denied cold build",
    "independently implemented minimal verifier",
    "deterministic evidence bundle",
):
    if fragment not in cut_text:
        fail(f"remaining cut set omits {fragment!r}")

print("ok: upstream narrow Lean validation replayed against pinned Lean/mathlib")
print("ok: M0420-N1 evidence and the five-obligation open root cut were reconciled without promotion")
print("open: exact Hilbert class field root remains M3; AUDIT-Z is false")
print("blocked: dependency acceptance, root closure, H0/R0, hermetic, and independent-verifier gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false; no accepted receipts")
