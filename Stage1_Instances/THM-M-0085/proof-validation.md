# THM-M-0085 proof-phase validation

Item: `S56-M-0085-PROOF`. Base revision:
`89e6fb566792fc6447b4005d3171c493c6fb435d`.

## Implemented proof

`Proof.lean` imports the exact target frozen in `Statement.lean` and proves its
named canonical wrapper. For each category pair, functor pair, and fixed
adjunction, the proof installs the explicit
`CreatesColimitOfIsSplitPair G` premise as a local instance and applies the
pinned `monadicOfCreatesGSplitCoequalizers` constructor. Its `eqv` field has
the exact conclusion `(Monad.comparison adj).IsEquivalence` for the same
adjunction.

The source has no `sorry`, `admit`, new axiom, unsafe declaration, or weakened
target. Lean reports only `propext`, `Classical.choice`, and `Quot.sound` in
the wrapper's axiom closure.

## Commands and results

Validation ran in the worker clone on 2026-07-12 using the existing pinned
Lake environment. No update, build, dependency clone, fetch, or `.lake`
mutation was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0085
  exit 0: execution rank 140; planned; theorem_complete=false

cd Stage1_Instances/THM-M-0085
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
  -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
rm -f Statement.olean
  exit 0: exact target and proof wrapper elaborated; beckMonadicity depends on
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0085/check_proof.py
  exit 0: PASS THM-M-0085 proof phase: exact frozen target has a
  placeholder-free proof body

python3 Stage1_Instances/THM-M-0085/check_obligation_tree.py
  exit 0: PASS; 5 obligations and 11 typed edges; frozen candidate
  composition elaborated

git diff --check -- Stage1_Instances/THM-M-0085 .stage1-worker-selftest.json
  exit 0; no output
```

This self-tests proof execution only. Master acceptance and the later
validation and release gates remain required, so theorem completion is not claimed.
