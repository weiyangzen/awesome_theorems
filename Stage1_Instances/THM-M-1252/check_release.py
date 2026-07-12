#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-1252-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1252"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str]) -> str:
    result = subprocess.run(
        argv, cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=180, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


decision = json.loads((HERE / "release-decision.json").read_text())
validation = json.loads((HERE / "validation-receipt.json").read_text())
proof = json.loads((HERE / "proof-receipt.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
instance = json.loads((HERE / "instance.json").read_text())

assert decision["item_id"] == "S56-M-1252-RELEASE"
assert decision["theorem_id"] == "THM-M-1252"
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["dependency"]["master_accepted"] is False
assert decision["dependency"]["receipt_id"] == validation["receipt_id"]
assert validation["support_state"] == "provisional_worker_selftest"
assert validation["release_grade"] is False
assert decision["terminal_decisions"]["audit_complete"] is False
assert decision["terminal_decisions"]["theorem_complete"] is False
assert instance["audit_complete"] is False and instance["theorem_complete"] is False
assert decision["root_vector"]["accepted_before"] == ["H2", "M4", "R4"]
assert decision["root_vector"]["accepted_after"] == ["H2", "M4", "R4"]
assert proof["result"]["root_closed"] is True
assert validation["result"]["provisional_root_kernel_closed"] is True
assert graphs["closure_boundary"]["root_closed"] is False
assert validation["result"]["structured_state_freshness"] == "fail_closed_stale_typed_graph"
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_verification_gate"] == "fail_closed"
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"

for name, expected in decision["input_hashes"].items():
    assert digest(HERE / name) == expected, name

output = run(["python3", "Stage1_Instances/THM-M-1252/check_validation.py"])
assert "ok: exact statement, proof root" in output
assert "stale: frozen typed graph" in output
assert "blocked: cold empty-cache hermetic replay" in output

print("ok: provisional exact-root validation replayed against pinned Lean/mathlib")
print("open: dependency is not master-accepted; authoritative structured state is stale")
print("open: audit H2/R4; AUDIT-Z is not established")
print("blocked: hermetic, supply-chain, independent-verifier, and master-acceptance gates")
print("verdict: blocked; lifecycle planned; theorem_complete=false")
