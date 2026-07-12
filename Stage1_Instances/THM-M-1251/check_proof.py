#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-1251-PROOF."""

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text()
receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert receipt["schema_version"] == "stage1-proof-receipt/1.0"
assert receipt["item_id"] == "S56-M-1251-PROOF"
assert receipt["theorem_id"] == "THM-M-1251"
assert receipt["statement_fingerprint"] == (
    "lean-expression-sha256:"
    "597f3e4b3a8dd3da2a6eb5e14d5451f854d866cfaa214245b3dfc65c078a8ab9"
)
assert receipt["proof_sha256"] == hashlib.sha256(proof_path.read_bytes()).hexdigest()
assert receipt["closed_machine_obligations"] == [
    "M1251-ROOT",
    "M1251-S-DEFINITIONS",
    "M1251-S-DOMAIN",
    "M1251-S-BOUNDARY",
    "M1251-S-TRANSPORT",
    "M1251-N-UNFOLD",
    "M1251-T-ASSEMBLE",
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
    "theorem importedDefinitionExpansion : CanonicalTarget.{u} := by",
    "theorem temperedDistributionsAreSchwartzDual : CanonicalTarget.{u} :=",
    "#print axioms Stage1Instances.THM_M_1251.Proof.importedDefinitionExpansion",
    "#print axioms Stage1Instances.THM_M_1251.Proof.temperedDistributionsAreSchwartzDual",
):
    assert declaration in proof

assert "intro E _ _ _\n  rfl" in proof
assert receipt["proof_status"] == "repo_local_machine_root_closed"
assert receipt["theorem_complete"] is False
print("PASS THM-M-1251 proof phase: exact machine root closed by pinned definition expansion")
