#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0540-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()
receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert receipt["schema_version"] == "stage1-proof-receipt/1.0"
assert receipt["item_id"] == "S56-M-0540-PROOF"
assert receipt["theorem_id"] == "THM-M-0540"
assert receipt["proof_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["statement_file_sha256"] == hashlib.sha256(
    (HERE / "Statement.lean").read_bytes()
).hexdigest()
assert receipt["obligation_denominator_sha256"] == (
    "e845fa732f6d3b06fbbec0c8848b9566a7a3a0f1a847f08094225fffd374b9a7"
)
assert receipt["closed_machine_obligations"] == [
    "M0540-ROOT",
    "M0540-D-CHAINS",
    "M0540-D-HOMOLOGY",
    "M0540-N-SPECIALIZE",
    "M0540-T-UNFOLD",
    "M0540-T-ASSEMBLE",
]

for pattern in (
    r"^\s*sorry(?:\s|$)",
    r"^\s*admit(?:\s|$)",
    r"^\s*axiom(?:\s|$)",
    r"\bsorryAx\b",
    r"^\s*unsafe(?:\s|$)",
):
    assert re.search(pattern, proof, re.MULTILINE) is None, pattern

for declaration in (
    "theorem unfoldingEquation",
    "theorem integralSingularHomology_eq_homology : CanonicalTarget := by",
    "exact unfoldingEquation X n",
    "#print axioms unfoldingEquation",
    "#print axioms integralSingularHomology_eq_homology",
):
    assert declaration in proof, declaration

assert receipt["proof_status"] == "repo_local_machine_root_closed"
assert receipt["theorem_complete"] is False
print("PASS THM-M-0540 proof phase: exact frozen machine root closed by definitional unfolding")
