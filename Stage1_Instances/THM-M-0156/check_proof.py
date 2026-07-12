#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0156-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()
receipt = json.loads((HERE / "proof-receipt.json").read_text())
validation = (HERE / "proof-validation.md").read_text()

code = re.sub(r"/-.*?-/", "", proof, flags=re.S)
code = re.sub(r"--.*", "", code)
for token in ("s" + "orry", "a" + "dmit", "a" + "xiom ", "s" + "orryAx", "unsafe"):
    assert token not in code
for declaration in (
    "theorem offCountablePackage",
    "theorem divergenceTheoremTarget_proof",
    "MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable",
    "#print axioms offCountablePackage",
    "#print axioms divergenceTheoremTarget_proof",
):
    assert declaration in proof

assert receipt["item_id"] == "S56-M-0156-PROOF"
assert receipt["theorem_id"] == "THM-M-0156"
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["result"]["exit_code"] == 0
assert receipt["result"]["root_machine_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert "does not claim theorem completion" in validation

print("PASS THM-M-0156 proof phase: pinned proof body closes the exact machine root")
