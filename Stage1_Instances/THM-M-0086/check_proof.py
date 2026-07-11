#!/usr/bin/env python3
"""Fail-closed structural check for the THM-M-0086 proof-phase source."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
source = (HERE / "Proof.lean").read_text()

required = (
    "theorem embeddingBranch",
    "CategoryTheory.Abelian.freyd_mitchell C",
    "theorem injectiveBranch",
    "CategoryTheory.Abelian.has_injective_coseparator G hG",
    "theorem projectiveBranch",
    "CategoryTheory.Abelian.has_projective_separator G hG",
    "theorem freydTheoremPackage : CanonicalStatement.{v, u}",
    "⟨embeddingBranch C, injectiveBranch C, projectiveBranch C⟩",
    "#print axioms freydTheoremPackage",
)
for needle in required:
    assert needle in source, f"missing exact proof component: {needle}"

for forbidden in ("sorry", "admit", "sorryAx", "axiom ", "unsafe "):
    assert forbidden not in source, f"prohibited proof source token: {forbidden}"

print("PASS THM-M-0086 proof source: three pinned branches compose to CanonicalStatement")
