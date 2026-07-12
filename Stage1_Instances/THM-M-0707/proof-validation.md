# THM-M-0707 proof-phase validation

## Implemented proof

`Proof.lean` imports the exact proposition frozen in `Statement.lean`. It
computably embeds each code as `(code, 0)`, restricts a hypothetical uniform
pair decider to input zero (including its `DecidablePred` witness and computable
Boolean characteristic), then applies the pinned theorem
`ComputablePred.halting_problem 0`. Thus the proof closes the arbitrary-code,
arbitrary-input target rather than substituting the fixed-input theorem.

There is no `sorry`, `admit`, new axiom, unsafe declaration, or placeholder.
Lean reports only `propext`, `Classical.choice`, and `Quot.sound`. This is
provisional proof-node evidence pending master acceptance; validation, release,
and theorem completion are not claimed.

## Commands and results

Commands ran at base revision
`ed278d07d4b1fbd48887625b78d32141bebc9441` on 2026-07-12.

```text
cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0707/check_proof.sh
  exit 0; isolated Statement.olean and Proof.lean elaboration passed
  codePairZero_computable: propext, Classical.choice, Quot.sound
  fixedInputDecider_of_pairDecider: propext, Classical.choice, Quot.sound
  haltingProblemUndecidable: propext, Classical.choice, Quot.sound

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0707
  exit 0; rank 748, planned, theorem_complete false

cd Formalizations/Lean && lake env lean --version
  exit 0; Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0; 8a178386ffc0f5fef0b77738bb5449d50efeea95

rg prohibited proof tokens and unsafe declarations in Proof.lean, with
expected-no-match assertions
  exit 0; both scans had no matches
```

No update, build, clone, fetch, network access, or mutation of `.lake` was
performed. `check_proof.sh` deleted its temporary local OLean directory.
