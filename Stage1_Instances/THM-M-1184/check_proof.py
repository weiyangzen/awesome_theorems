#!/usr/bin/env python3
"""Fail-closed source and frozen-architecture checks for S56-M-1184-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
receipt = json.loads((HERE / "proof-receipt.json").read_text())

for pattern in (
    r"\bsorry\b",
    r"\badmit\b",
    r"\bsorryAx\b",
    r"^[ \t]*axiom\b",
    r"^[ \t]*unsafe\b",
    r"^[ \t]*opaque\b",
    r"^[ \t]*extern\b",
    r"implemented_by",
    r"native_decide",
):
    assert re.search(pattern, proof, re.MULTILINE) is None, pattern

for declaration in (
    "def productCoupling",
    "theorem integral_fst_of_coupling",
    "theorem integral_snd_of_coupling",
    "theorem dualValue_le_primalValue",
    "theorem constantDualPair_nonempty",
    "theorem objectiveRanges_wellFounded",
    "theorem weakDuality",
    "theorem kantorovichDuality_of_reverse",
):
    assert declaration in proof, declaration

assert "(reverse : ReverseDualityPackage.{u, v})" in proof
assert "root_of_duality_packages weakDuality reverse" in proof
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
assert registry["root_obligation_id"] == "M1184-ROOT"
proof_sha256 = hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["item_id"] == "S56-M-1184-PROOF"
assert receipt["theorem_id"] == "THM-M-1184"
assert receipt["accepted"] is False
assert receipt["proof_body"]["source_sha256"] == proof_sha256
assert receipt["registry_denominator_sha256"] == registry["denominator_sha256"]
assert receipt["provisionally_closed_obligation_ids"] == [
    "M1184-C-PRODUCT",
    "M1184-C-CONSTANT",
    "M1184-W-INTEGRATE",
    "M1184-W-ORDER",
    "M1184-T-WEAK",
]
assert receipt["result"]["root_kernel_closed"] is False
assert receipt["result"]["theorem_complete"] is False

print(
    "PASS THM-M-1184 proof phase: product coupling and weak-duality package "
    "closed; reverse-duality package and root remain open"
)
