#!/usr/bin/env python3
"""Fail-closed structural check for the THM-M-0420 partial proof phase."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
phase = json.loads((HERE / "proof-phase.json").read_text())
proof = (HERE / "Proof.lean").read_text()

assert phase["item_id"] == "S56-M-0420-PROOF"
assert phase["theorem_id"] == "THM-M-0420"
assert phase["statement_source_sha256"] == hashlib.sha256(
    (HERE / "Statement.lean").read_bytes()
).hexdigest()
assert phase["closed_obligation_ids"] == ["M0420-N1"]
assert phase["first_failed_gate"] == "M0420-X1"
assert phase["remaining_root_cut_set"] == [
    "M0420-C", "M0420-L1", "M0420-L2", "M0420-L3", "M0420-L4"
]
assert phase["phase_self_tested"] is True
assert phase["theorem_complete"] is False
assert "everywhereUnramifiedAtFinitePrimes_iff_allPrimesOver" in proof
assert "Algebra.isUnramifiedAt_iff_of_isDedekindDomain" in proof
assert "Ideal.primesOver" in proof

print("PASS THM-M-0420 proof phase: M0420-N1 local body checked")
print("root closure: open (M3); global class-field-theory bridge M0420-X1 unavailable")
