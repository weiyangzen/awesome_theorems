#!/usr/bin/env python3
"""Fail-closed artifact checks for the THM-M-0500 proof-phase wrapper."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
required = [
    "def DirichletPrimesInAPTarget : Prop :=",
    "theorem dirichletPrimesInAP_proof : DirichletPrimesInAPTarget := by",
    "exact Nat.infinite_setOf_prime_and_eq_mod ha",
    "#print axioms Nat.infinite_setOf_prime_and_eq_mod",
    "#print axioms dirichletPrimesInAP_proof",
]
for fragment in required:
    if fragment not in proof:
        raise SystemExit(f"FAIL missing proof fragment: {fragment}")

prohibited = ["sorry", "admit", "sorryAx", "axiom "]
for token in prohibited:
    if token in proof:
        raise SystemExit(f"FAIL prohibited token in Proof.lean: {token}")

receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
checks = {
    "item_id": "S56-M-0500-PROOF",
    "theorem_id": "THM-M-0500",
    "proof_sha256": digest(HERE / "Proof.lean"),
    "statement_sha256": digest(HERE / "Statement.lean"),
    "obligation_tree_sha256": digest(HERE / "ObligationTree.lean"),
    "obligation_registry_sha256": digest(HERE / "obligation-registry.json"),
}
for key, expected in checks.items():
    if receipt.get(key) != expected:
        raise SystemExit(f"FAIL receipt {key}: expected {expected}, got {receipt.get(key)}")

if receipt.get("result", {}).get("theorem_complete") is not False:
    raise SystemExit("FAIL proof receipt must not claim theorem completion")

print("PASS THM-M-0500 proof artifacts")
for key, value in checks.items():
    print(f"{key}={value}")
