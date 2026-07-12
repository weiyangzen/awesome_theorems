#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0311-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()

required = (
    "import Statement",
    "import ObligationTree",
    "theorem realL2Complete_proof : RealL2Complete.{u}",
    "theorem complexL2Complete_proof : ComplexL2Complete.{u}",
    "obligationTreeTarget_of_scalar_children realL2Complete_proof complexL2Complete_proof",
    "theorem rieszFischerTarget_proof : RieszFischerTarget.{u}",
    "exact ⟨realL2Complete_proof alpha mu, complexL2Complete_proof alpha mu⟩",
    "#check MeasureTheory.Lp.instCompleteSpace",
)
missing = [fragment for fragment in required if fragment not in proof]
assert not missing, f"missing proof surface: {missing}"
assert proof.count("infer_instance") == 2, "each scalar branch must admit the pinned instance"
forbidden = re.compile(r"\b(sorry|admit|sorryAx)\b|^[ \t]*(axiom|unsafe)\b", re.MULTILINE)
assert forbidden.search(proof) is None, "placeholder, added axiom, or unsafe declaration"
assert proof.count("#print axioms") == 4

receipt = json.loads((HERE / "proof-receipt.json").read_text())
assert receipt["item_id"] == "S56-M-0311-PROOF"
assert receipt["theorem_id"] == "THM-M-0311"
for key, filename in receipt["inputs"].items():
    assert key.endswith("_sha256")
    expected = hashlib.sha256((HERE / filename).read_bytes()).hexdigest()
    assert receipt["input_hashes"][key] == expected, (key, expected)
assert receipt["proof_body"]["source_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["result"]["root_declaration"] == "Stage1Instances.THM_M_0311.rieszFischerTarget_proof"
assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
assert receipt["result"]["proof_node_self_tested"] is True
assert receipt["result"]["theorem_complete"] is False

print("PASS THM-M-0311 proof: both scalar bodies, frozen composition, and exact root are closed")
print(f"proof sha256: {hashlib.sha256(proof_path.read_bytes()).hexdigest()}")
