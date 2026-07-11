# THM-M-0396 validation-phase evidence

Item: `S56-M-0396-VALIDATION`

## Validated boundary

The validation phase replayed the proof receipt against frozen source,
registry, graph, toolchain, and dependency hashes. An independent Lean module
that does not import `Proof` reimplemented the integer-logarithm identity,
finite-product normalization, and conditional binder-level composition.

Both implementations elaborated and reported exactly `propext`,
`Classical.choice`, and `Quot.sound`. The fail-closed verifier also confirms
that the receipt claims only `M0396-N1`, that the required Baker-Matveev
obligations remain `M3`/`M4`/`M5`, and that no source module contains `sorry`,
`admit`, an `axiom` declaration, or `unsafe` declaration.

This is partial validation, not theorem validation. The core estimate
`M0396-T`, its construction and analytic dependencies, and the exact root have
no proof body. The prerequisite proof node also awaits master acceptance.

## Commands and results

Commands ran at base revision
`518315d81e5e2006972fb32b395e2a3a91d55b92` on 2026-07-12
(`2026-07-11T19:40:17Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0396
  exit 0: rank 9, planned, legacy artifacts unaccepted, theorem_complete=false

python3 Stage1_Instances/THM-M-0396/check_validation.py
  exit 0: frozen inputs and 15-node boundary verified; the proof and
  independent probes elaborated; root remains open

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0396/check_proof.sh
  exit 0: Statement, ObligationTree, and Proof elaborated in a disposable
  module directory; declarations reported propext, Classical.choice,
  Quot.sound

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0396/check_validation_lean.sh
  exit 0: independently implemented validation probes elaborated in a
  disposable module directory and reported the same three axioms
```

No network access, Lake update/build, dependency fetch/clone, or `.lake`
mutation occurred. The pre-existing canonical pinned `.lake` symlink was
reused. This is not a cold empty-cache replay, an offline archive replay, or a
distinct runner: hermetic release and independent-verifier gates remain open.
