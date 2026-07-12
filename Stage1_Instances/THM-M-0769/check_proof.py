#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0769-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()

required = (
    "import Statement",
    "noncomputable def fiberSelector_proof",
    "fun i => Classical.choice (h i)",
    "theorem axiomOfChoice_proof : AxiomOfChoiceTarget.{u, v}",
    "Nonempty.intro (fiberSelector_proof ι A h)",
    "#print axioms fiberSelector_proof",
    "#print axioms axiomOfChoice_proof",
)
for fragment in required:
    assert fragment in proof, f"missing proof fragment: {fragment}"

for forbidden in ("sorry", "admit", "sorryAx"):
    assert forbidden not in proof, f"forbidden proof token: {forbidden!r}"
assert not re.search(r"^\s*(axiom|unsafe)\b", proof, re.MULTILINE), "added axiom or unsafe declaration"

receipt = json.loads((HERE / "proof-receipt.json").read_text())
assert receipt["item_id"] == "S56-M-0769-PROOF"
assert receipt["theorem_id"] == "THM-M-0769"
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["inputs"]["statement_sha256"] == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
assert receipt["inputs"]["obligation_tree_sha256"] == hashlib.sha256((HERE / "ObligationTree.lean").read_bytes()).hexdigest()
assert receipt["inputs"]["obligation_registry_sha256"] == hashlib.sha256((HERE / "obligation-registry.json").read_bytes()).hexdigest()
assert receipt["result"]["axioms"] == ["Classical.choice"]
assert receipt["result"]["theorem_complete"] is False

print("PASS THM-M-0769 proof phase: exact target closed with disclosed Classical.choice")
