#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0773-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()

required = (
    "import Statement",
    "theorem pointed_maximal_proof : PointedTarget.{u}",
    "hfinite.exists_maximal hx",
    "theorem teichmullerTukey_proof : TeichmullerTukeyTarget.{u}",
    "pointed_implies_unpointed pointed_maximal_proof",
    "#print axioms pointed_maximal_proof",
    "#print axioms teichmullerTukey_proof",
)
for fragment in required:
    assert fragment in proof, f"missing proof fragment: {fragment}"

for forbidden in ("sorry", "admit", "sorryAx"):
    assert forbidden not in proof, f"forbidden proof token: {forbidden!r}"
assert not re.search(r"^\s*(axiom|unsafe)\b", proof, re.MULTILINE), "added axiom or unsafe declaration"

registry = json.loads((HERE / "obligation-registry.json").read_text())
assert registry["theorem_id"] == "THM-M-0773"
assert registry["denominator_sha256"] == "8f19a683c860e2b4563adc27ea17d4d49dd0d899f93a165e6cc5568a0abe4bee"

receipt = json.loads((HERE / "proof-receipt.json").read_text())
assert receipt["item_id"] == "S56-M-0773-PROOF"
assert receipt["theorem_id"] == "THM-M-0773"
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["inputs"]["statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert receipt["inputs"]["obligation_registry_sha256"] == hashlib.sha256((HERE / "obligation-registry.json").read_bytes()).hexdigest()
assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
assert receipt["result"]["root_closed"] is True
assert receipt["result"]["theorem_complete"] is False

print("PASS THM-M-0773 proof phase: exact target closed by pinned Teichmuller-Tukey theorem")
