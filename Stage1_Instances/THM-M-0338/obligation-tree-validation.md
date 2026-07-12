# THM-M-0338 obligation-tree validation

Item: `S56-M-0338-OBLIGATION_TREE`. Base revision:
`c9694802ae049af37973e49a65f11b833135333f`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake artifacts were reused; no
update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0338/build_obligation_artifacts.py
  exit 0
  e53a0b15267ae38e68bb1b727edd51b52d0b60c8f244fd912fc2153c2a0cca6e

python3 Stage1_Instances/THM-M-0338/check_obligation_tree.py
  exit 0
  PASS THM-M-0338 obligation tree: 16 obligations, 70 typed edges
  registry denominator sha256: e53a0b15267ae38e68bb1b727edd51b52d0b60c8f244fd912fc2153c2a0cca6e
  root closure: open (M3); exact existence, paving/MSS, source, and trust leaves remain open

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0338
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_components depends on axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0338
  exit 0; rank 831, planned, theorem_complete false
git diff --check
  exit 0
```

The structural checker validates source freeze hashes, the deterministic registry denominator,
eligibility projections, complete node coverage, typed adjacency, reciprocal proof edges, proof DAG
acyclicity, per-node recipe coverage, step budgets, open closure status, and placeholder hygiene.
Lean validates the exact statement and the child-to-root composition theorem. The reported axioms
are pinned mathlib/Lean dependencies; `sorryAx` is absent.

This phase freezes interfaces only. It does not prove extension existence, paving, Weaver KS2, any
MSS analytic leaf, source fidelity, trust closure, or the theorem. Master acceptance remains
required.
