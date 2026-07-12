#!/usr/bin/env python3
"""Fail-closed source checks for S56-M-0988-PROOF."""

import hashlib
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text(encoding="utf-8")

required = (
    "import Statement",
    "import ObligationTree",
    "theorem pinnedMathlibBridge : StatementShape.{u, v}",
    "tendstoInDistribution_inv_sqrt_mul_sum_sub",
    "theorem pinnedObligationBridge : ObligationTree.Root.{u, v}",
    "ObligationTree.root_compose pinnedObligationBridge",
    "theorem lindebergLevyCentralLimit : StatementShape.{u, v}",
)
missing = [needle for needle in required if needle not in proof]
if missing:
    raise SystemExit(f"missing required proof surface: {missing}")

forbidden = re.compile(r"\b(sorry|admit)\b|^[ \t]*(axiom|unsafe)\b", re.MULTILINE)
match = forbidden.search(proof)
if match:
    raise SystemExit(f"forbidden proof token: {match.group(0)!r}")
if proof.count("#print axioms") != 4:
    raise SystemExit("expected four axiom-closure probes")

print("PASS THM-M-0988 proof: pinned bridge, frozen composition, and exact root have bodies")
print(f"proof sha256: {hashlib.sha256(proof_path.read_bytes()).hexdigest()}")
