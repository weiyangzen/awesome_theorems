#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1271 anchor audit."""

from pathlib import Path
import hashlib
import json
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUDIT = json.loads((HERE / "anchor-audit.json").read_text())
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_FLT = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
EXPECTED_STATEMENT = "984ec64013fa92caf23696c39017a28b7c8a908224ae8e1018a156734469f70c"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"anchor audit check failed: {message}")


require(AUDIT["item_id"] == "S56-M-1271-ANCHOR_AUDIT", "wrong item")
require(AUDIT["theorem_id"] == "THM-M-1271", "wrong theorem")
require(AUDIT["canonical_source_sha256"] == EXPECTED_STATEMENT, "recorded statement drift")
require(hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() == EXPECTED_STATEMENT,
        "canonical statement drift")
require(AUDIT["audit_complete"] is True, "bounded audit is not closed")
require(AUDIT["theorem_complete"] is False, "audit claims theorem completion")
require(AUDIT["accepted_receipts"] == [], "worker invented accepted receipts")
require(AUDIT["discovery_protocol"]["exhaustive_public_search_claimed"] is False,
        "search boundary was broadened")
require(len(AUDIT["candidates"]) == 7, "candidate ledger changed")
require(all(candidate["exact_root_closed"] is False for candidate in AUDIT["candidates"]),
        "candidate ledger contradicts root decision")
require(AUDIT["root_decision"]["kernel_closed"] is False, "root incorrectly closed")

for package, expected in (("mathlib", EXPECTED_MATHLIB), ("flt-regular", EXPECTED_FLT)):
    head = subprocess.run(
        ["git", "-C", str(ROOT / "Formalizations/Lean/.lake/packages" / package),
         "rev-parse", "HEAD"], check=True, text=True, capture_output=True
    ).stdout.strip()
    require(head == expected, f"checked-out {package} does not match pin")

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib"
checks = {
    "Analysis/Calculus/ContDiff/Basic.lean": "theorem ContDiff.continuous",
    "Topology/Path.lean": "structure Path",
    "Topology/Order/Compact.lean": "theorem IsCompact.exists_isMaxOn",
    "Topology/Sequences.lean": "theorem IsCompact.tendsto_subseq",
}
for relative, witness in checks.items():
    require(witness in (mathlib / relative).read_text(), f"missing pinned witness: {witness}")

legacy = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_164.lean"
require(hashlib.sha256(legacy.read_bytes()).hexdigest() ==
        "40b6967b485874d9ed1ab46feaa1bde2bf82ac0c3a53f55aafe77381c7098fd5",
        "legacy candidate source drift")
legacy_text = legacy.read_text()
for witness in ("structure MinimaxDeformationLemma", "def StatementShape : Prop :=",
                "not_terminalWrapperCreationGate_without_proof_source"):
    require(witness in legacy_text, f"missing legacy boundary witness: {witness}")

print("anchor audit check: ok; 7 candidates, immutable pins, and non-closing boundary verified")
