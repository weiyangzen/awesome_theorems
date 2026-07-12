# THM-M-0318 proof-phase validation

Date: 2026-07-12

## Implemented body

`Proof.lean` implements `compactLimitEngine`, the exact
`CompactLimitEngine` interface frozen by the obligation tree.  The argument
minimizes `x ↦ dist (f x) x` on the compact carrier and uses approximate fixed
points to force the minimum to zero.  This closes `M0318-L-LIMIT` and
`M0318-L-CONT` together as one local terminal body; it does not close the
finite-dimensional approximation obligations.

No `sorry`, `axiom`, placeholder declaration, or strengthened hypothesis is
used.  Kernel-reported axioms are the expected mathlib foundation profile:
`propext`, `Classical.choice`, and `Quot.sound`.

## Narrow validation

Working directory:
`Formalizations/Lean`

Command:

```text
lake env lean ../../Stage1_Instances/THM-M-0318/Proof.lean
```

Exit code: `0`

Exact output:

```text
Stage1Instances.THM_M_0318.compactLimitEngine.{u} : Stage1Instances.THM_M_0318.CompactLimitEngine
'Stage1Instances.THM_M_0318.compactLimitEngine' depends on axioms: [propext, Classical.choice.{u}, Quot.sound.{u}]
```

Additional checks run from the repository root:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0318
git diff --check
```

All four commands exited `0`.  The first command reported `ok` with 15
assurance groups and 1546 uniform-L0 targets; the second reported 1546 unique
targets with ranks `1..1546`; `show` identified execution rank 684 and
`theorem_complete: false`; `git diff --check` produced no output.

## Honest boundary

This proof phase is **blocked**, not self-tested complete.  The frozen root cut
set still contains `M0318-C-NET`, `M0318-C-MAP`, and
`M0318-B-BROUWER`; consequently `ApproximationEngine` and the exact Schauder
root have no unconditional proof body.  Pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains no matching Schauder or
Brouwer theorem.  The audited external Brouwer candidate at
`harfe/fixed-point-theorems-lean4@11a9f041246d28374edae384241757f9a0cbd5e4`
uses Lean `v4.21.0-rc3` and mathlib
`c873c5d1d1eb371ddca7f0f5eab48e80ed10b7cb`; it is not in the pinned local
dependency closure.  Per worker policy, no moving dependency was fetched and
no `.lake` artifact was mutated.

First failed gate: unconditional implementation of the finite-dimensional
approximation/Brouwer branch.  Because the assigned proof node is not fully
closed, no `.stage1-worker-selftest.json` is emitted and no theorem-completion
claim is made.
