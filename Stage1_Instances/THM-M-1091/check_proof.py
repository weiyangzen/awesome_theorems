#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1091 proof-phase artifact."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()
record = json.loads((HERE / "proof.json").read_text())

assert record["item_id"] == "S56-M-1091-PROOF"
assert record["theorem_id"] == "THM-M-1091"
assert record["depends_on"] == "S56-M-1091-OBLIGATION_TREE"
assert record["declaration"] == "Stage1Instances.THM_M_1091.chapmanKolmogorov"
assert record["target"] == "Stage1Instances.THM_M_1091.ChapmanKolmogorovTarget"
assert record["gate_state"] == "self_tested_pending_master_acceptance"
assert record["proof_phase_complete"] is True
assert record["theorem_complete"] is False

for token in ("sorry", "admit", "sorryAx", "axiom ", "unsafe"):
    assert token not in proof
for token in (
    "theorem chapmanKolmogorov : ChapmanKolmogorovTarget",
    "Kernel.pow_add kappa n m",
    "simpa only [add_comm]",
    "target_iff_integralTarget.mp chapmanKolmogorov",
    "#print axioms chapmanKolmogorov",
):
    assert token in proof

print("PASS THM-M-1091 proof: exact root and integral transport are present")
print("proof phase self-tested; downstream validation, release, and master acceptance remain open")
