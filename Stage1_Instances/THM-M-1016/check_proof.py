#!/usr/bin/env python3
"""Fail-closed source and input checks for S56-M-1016-PROOF."""

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
proof_path = HERE / "Proof.lean"
proof = proof_path.read_text(encoding="utf-8")
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))


def require(value, message):
    if not value:
        raise SystemExit("proof check failed: " + message)


require(registry["theorem_id"] == "THM-M-1016", "wrong theorem registry")
require(
    registry["frozen_against_statement_sha256"]
    == hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "statement drifted after obligation freeze",
)

required = (
    "import Statement",
    "import ObligationTree",
    "theorem normalizedLawsTight",
    "isTightMeasureSet_of_isCompact_closure",
    "theorem normalizedTail",
    "tendsto_measure_norm_gt_of_isTightMeasureSet",
    "theorem inputConvergesInMeasure",
    "theorem scaledRemainderTendstoInMeasure",
    "hg_diff.isLittleO.bound",
    "theorem transformedAEMeasurable",
    "theorem deltaMethod",
    "apply deltaMethod_of_remainder",
    "theorem statementProof : StatementShape.{u, v, w}",
)
missing = [needle for needle in required if needle not in proof]
require(not missing, f"missing required proof surface: {missing}")

forbidden = re.compile(r"\b(sorry|admit|sorryAx)\b|^[ \t]*(axiom|unsafe)\b", re.MULTILINE)
match = forbidden.search(proof)
require(match is None, f"forbidden proof token: {match.group(0)!r}" if match else "")
require(proof.count("#print axioms") == 7, "expected seven axiom-closure probes")

print("PASS THM-M-1016 proof: tightness, concentration, Frechet remainder, and exact root have bodies")
print(f"proof sha256: {hashlib.sha256(proof_path.read_bytes()).hexdigest()}")
