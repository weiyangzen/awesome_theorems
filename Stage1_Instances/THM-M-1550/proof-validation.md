# THM-M-1550 proof validation

Item: `S56-M-1550-PROOF`  
Base revision: `262914c2855c083501ba7f4334980a4287403f3c`

## Implemented proof

`Statement.lean` now contains `laxPairIsospectrality`, a proof of the exact
frozen `LaxPairIsospectrality` declaration. For each pair of times, the
supplied `ConjugatingEvolutionOn` premise yields a matrix unit and its exact
conjugation equality. `spectrumUnderConjugation` rewrites by that equality,
uses the matrix-unit inverse coercion lemma, and closes the sole mathematical
leaf with pinned mathlib theorem `spectrum.units_conjugate`. The Lax-equation
premise is retained unchanged, although the deliberately stronger evolution
premise makes it logically redundant.

`Proof.lean` independently repeats the frozen interface and proof assembly as
a narrow proof-phase elaboration target. Neither file contains a placeholder,
new axiom declaration, unsafe declaration, or weakened root.

## Commands and exact results

Commands ran in this worker clone on 2026-07-12. Lean reused the existing
canonical pinned `.lake`; no update, build, clone, fetch, or dependency
mutation was performed.

```text
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1550/Proof.lean
  exit 0
  spectrumEqOfUnitsConjugate axioms: [propext, Classical.choice, Quot.sound]
  spectrumUnderConjugation axioms: [propext, Classical.choice, Quot.sound]
  laxPairIsospectrality axioms: [propext, Classical.choice, Quot.sound]

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1550/Statement.lean
  exit 0
  spectrumUnderConjugation axioms: [propext, Classical.choice, Quot.sound]
  laxPairIsospectrality axioms: [propext, Classical.choice, Quot.sound]
  canonical target and all four statement mutations printed; one pre-existing
  unused-variable linter warning was emitted

python3 Stage1_Instances/THM-M-1550/check_statement.py
  exit 0
  canonical expression SHA-256 657174522ed3122ec3776afaa7bcb826593d652cd089e6bc4e15e6ee1ecc194c;
  all four mutations differed

python3 Stage1_Instances/THM-M-1550/check_proof.py
  exit 0: exact frozen root and spectrum leaf are implemented

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1550
  exit 0: rank 209, planned, theorem_complete false

rg -n '\b(sorry|admit|axiom|unsafe)\b' \
  Stage1_Instances/THM-M-1550/Proof.lean \
  Stage1_Instances/THM-M-1550/Statement.lean
  exit 1 with empty output: pass, no prohibited token

git diff --check -- Stage1_Instances/THM-M-1550
  exit 0: no whitespace errors
```

This is self-tested proof-phase evidence pending master acceptance. It does
not claim the later hermetic validation, independent review, source/readability
acceptance, release node, or theorem completion.
