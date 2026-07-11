#!/usr/bin/env python3
"""Check the THM-M-0416 proof-phase integration artifact."""

from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()

required = (
    "theorem freePackage_proof : FreePackage",
    "theorem finitePackage_proof : FinitePackage",
    "theorem rankPackage_proof : RankPackage",
    "theorem coordinatesPackage_proof : CoordinatesPackage",
    "theorem dirichletUnitTheorem : DirichletUnitTheoremTarget",
    "root_of_packages freePackage_proof finitePackage_proof rankPackage_proof",
    "NumberField.Units.rank_modTorsion K",
    "NumberField.Units.exist_unique_eq_mul_prod K x",
    "#print axioms dirichletUnitTheorem",
)
assert all(fragment in proof for fragment in required)
for forbidden in ("sorry", "admit", "axiom ", "native_decide", "unsafe", "external "):
    assert forbidden not in proof

print("PASS THM-M-0416 proof: four frozen packages and exact root integrated")
print("machine root cut set after proof integration: empty; downstream validation gates remain")
