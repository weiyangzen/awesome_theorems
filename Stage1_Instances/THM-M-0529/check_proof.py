#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0529-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()
receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert receipt["schema_version"] == "stage1-proof-receipt/1.0"
assert receipt["item_id"] == "S56-M-0529-PROOF"
assert receipt["theorem_id"] == "THM-M-0529"
assert receipt["statement_fingerprint"] == (
    "lean-expression-sha256:"
    "346202448f85225bd2460d494524132adb745ad2711c1c4c587a816499c30aea"
)
assert receipt["proof_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["closed_machine_obligations"] == [
    "M0529-ROOT", "M0529-C-MAP", "M0529-B-HOMEO", "M0529-B-FUNCTOR",
    "M0529-S-STATEMENT",
]

for pattern in (
    r"^\s*sorry(?:\s|$)", r"^\s*admit(?:\s|$)", r"^\s*axiom(?:\s|$)",
    r"\bsorryAx\b", r"^\s*unsafe(?:\s|$)",
):
    assert re.search(pattern, proof, re.MULTILINE) is None, pattern

for declaration in (
    "theorem homeomorphismHomIsIso",
    "theorem integralSingularHomologyMapIsIso",
    "theorem homologyIsHomeomorphismInvariant : CanonicalTarget := by",
    "#print axioms homeomorphismHomIsIso",
    "#print axioms integralSingularHomologyMapIsIso",
    "#print axioms homologyIsHomeomorphismInvariant",
):
    assert declaration in proof

assert "letI := homeomorphismHomIsIso X Y e\n  infer_instance" in proof
assert receipt["proof_status"] == "repo_local_machine_root_closed"
assert receipt["theorem_complete"] is False
print("PASS THM-M-0529 proof phase: exact machine root closed by pinned categorical instances")
