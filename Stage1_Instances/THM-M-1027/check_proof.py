#!/usr/bin/env python3
"""Structural checks for the THM-M-1027 proof-phase artifacts."""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
proof = (ROOT / "Proof.lean").read_text()
receipt = json.loads((ROOT / "proof-receipt.json").read_text())

required = [
    "theorem incrementVariance_eq_tsub",
    "theorem incrementVariance_eq_max_tsub",
    "theorem hasLaw_gaussianReal_zero_ae_eq_zero",
    "def WienerWitnessPackage.ofExternalBrownianComponents",
    "theorem wienerExistenceTarget_of_externalBrownianComponents",
]
missing = [name for name in required if name not in proof]
assert not missing, f"missing proof declarations: {missing}"
assert not re.search(r"(?m)^\s*(sorry|admit|axiom)(?:\s|$)|:=\s*sorry\b|by\s+sorry\b", proof)
assert receipt["item_id"] == "S56-M-1027-PROOF"
assert receipt["result"]["root_closed"] is False
assert receipt["result"]["theorem_complete"] is False
assert receipt["remaining_root_cut_set"] == ["M1027-X-EXTERNAL"]
print("PASS THM-M-1027 proof phase: local Brownian adapter bodies close; external construction remains")
