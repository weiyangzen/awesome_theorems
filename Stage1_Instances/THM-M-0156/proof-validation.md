# THM-M-0156 proof-phase validation

## Implemented bodies

`Proof.lean` closes frozen machine bridge `M0156-B-CANDIDATE` by binding its exact
off-countable package to
`MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable` from mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The second theorem specializes the exceptional set
to `empty`, supplies `Set.countable_empty`, and closes the exact rectangular target. It preserves
all dimensions, weak box inequalities, continuity, differentiability, integrability, and signed
face terms from the frozen statement.

This is proof-phase machine closure, not a release verdict. The provisional worker receipt still
requires master acceptance, and this phase does not claim theorem completion. Human-source H0,
readable reconstruction R0, validation, hermetic replay, independent verification, and release
remain open.

## Commands and results

Commands ran from base revision `e51894725a43642d26ce16e4aad3abaf28393de7` on 2026-07-12.
No dependency update, build, fetch, clone, or `.lake` mutation was performed.

```text
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0156/Proof.lean
  exit 0; offCountablePackage and divergenceTheoremTarget_proof elaborated
  axioms for each: propext, Classical.choice, Quot.sound

python3 Stage1_Instances/THM-M-0156/check_proof.py
  exit 0; source, receipt, exact declarations, and fail-closed boundary passed

python3 Stage1_Instances/THM-M-0156/check_obligation_tree.py
  exit 0; predecessor freeze passed (16 obligations, 23 typed edges)

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0156
  exit 0; rank 655, planned, L0/rework_required, theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-0156/proof-receipt.json
  exit 0

git diff --check -- Stage1_Instances/THM-M-0156 .stage1-worker-selftest.json
  exit 0; no output
```

The pre-existing untracked `Formalizations/Lean/.lake` symlink points at canonical pinned artifacts
and was used read-only. It is not a changed path for this item.
