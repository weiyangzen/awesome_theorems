#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0772-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
receipt_path = HERE / "proof-receipt.json"
proof = proof_path.read_text()
receipt = json.loads(receipt_path.read_text())

assert receipt["item_id"] == "S56-M-0772-PROOF"
assert receipt["theorem_id"] == "THM-M-0772"
assert receipt["state"] == "provisional_worker_selftest"
assert receipt["result"]["root_machine_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(
    proof_path.read_bytes()
).hexdigest()

for declaration in (
    "theorem hausdorffMaximalPrinciple",
    "theorem expandedHausdorffMaximalPrinciple",
    "maxChain_spec",
    "#print axioms Stage1Instances.THM_M_0772.Proof.hausdorffMaximalPrinciple",
):
    assert declaration in proof

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
assert prohibited.search(proof) is None

print("PASS THM-M-0772 proof: exact maximal-chain root body and receipt verified")
