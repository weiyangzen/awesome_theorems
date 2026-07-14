#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-1078-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROOF = HERE / "Proof.lean"
RECEIPT = HERE / "proof-receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


proof = PROOF.read_text(encoding="utf-8")
receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))

prohibited = re.compile(
    r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
    r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
    re.MULTILINE,
)
assert prohibited.search(without_comments(proof)) is None

for marker in (
    "theorem memLp_condExp_of_one_lt",
    "theorem earlierMemLpUpTo : EarlierMemLpUpTo.{u}",
    "hphi_convex.map_condExp_le_univ",
    "hmart.condExp_ae_eq hkn",
    "#print axioms memLp_condExp_of_one_lt",
    "#print axioms earlierMemLpUpTo",
):
    assert marker in proof, marker

node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1078-T-ALLTIME")
assert node["formal_target"] == (
    "Martingale f F mu -> MemLp (f n) p mu -> forall k <= n, MemLp (f k) p mu"
)
assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert receipt["item_id"] == "S56-M-1078-PROOF"
assert receipt["theorem_id"] == "THM-M-1078"
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["closed_obligation_ids"] == ["M1078-T-ALLTIME"]
assert receipt["proof_body"]["source_sha256"] == sha256(PROOF)
assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_registry_sha256"] == sha256(
    HERE / "obligation-registry.json"
)
assert receipt["inputs"]["registry_denominator_sha256"] == graphs[
    "registry_denominator_sha256"
]
assert receipt["inputs"]["check_proof_sha256"] == sha256(HERE / "check_proof.py")
assert receipt["inputs"]["proof_validation_sha256"] == sha256(HERE / "proof-validation.md")
assert receipt["inputs"]["proof_blocker_sha256"] == sha256(HERE / "proof-blocker.md")
assert "M1078-T-ALLTIME" in registry["frozen_denominators"]["required_machine"]
assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
assert receipt["result"]["root_closed"] is False
assert receipt["result"]["theorem_complete"] is False
assert graphs["closure_boundary"]["root_closed"] is False

print("PASS THM-M-1078 proof unit: horizon-local MemLp bridge pinned and checked")
print("root closure: open (M2); frozen conditional interface mismatch remains")
