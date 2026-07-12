# THM-M-1527 proof validation

Item: `S56-M-1527-PROOF`. Base revision:
`dd9a9ee3ccb2b4ae62a9105910ca0d54da3c9540`.

The proof phase supplies a proof body for the exact conditional target frozen
in `Statement.lean`. The two coordinate bridges are not invented geometric
facts: they are projected from the explicit `CoordinateDecomposition` premise
of that target. The root proof applies the already checked conjunction
assembly to those projections. Dimension, signature, orientation, and
positivity hypotheses remain present with exactly the frozen binder order,
although propositional assembly does not need to inspect them.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, fetch, clone, or dependency mutation
was performed.

```text
cd Stage1_Instances/THM-M-1527
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  combined exit 0
  homogeneous_iff_of_coordinateDecomposition axioms:
    [propext, Classical.choice, Quot.sound]
  inhomogeneous_iff_of_coordinateDecomposition axioms:
    [propext, Classical.choice, Quot.sound]
  maxwell_coordinate_equivalence axioms:
    [propext, Classical.choice, Quot.sound]
rm -f Statement.olean ObligationTree.olean
  exit 0

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1527
  exit 0: rank 195, planned, theorem_complete false
python3 Stage1_Instances/THM-M-1527/check_proof.py
  exit 0: PASS; both premise projections and exact root body present
sha256sum Stage1_Instances/THM-M-1527/Proof.lean
  exit 0: b9d589616d90b27391d20df1ab882c6413506806f7c3aca8421a4f9195a58f61
git diff --check -- Stage1_Instances/THM-M-1527 .stage1-worker-selftest.json
  exit 0; no output
```

No placeholder, axiom declaration, unsafe declaration, or substituted target
occurs in the proof source. This is proof-phase evidence only. Hermetic replay,
source/readability acceptance, independent verification, and release remain
later master-controlled gates; theorem completion is not claimed here.
