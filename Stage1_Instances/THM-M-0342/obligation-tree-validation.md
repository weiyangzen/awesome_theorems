# THM-M-0342 obligation-tree validation

Item: `S56-M-0342-OBLIGATION_TREE`. Base revision:
`cc46a50150dae27c90dca0938294d8da17db9109`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake artifacts were reused; no
update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0342/build_obligation_artifacts.py
  exit 0
  3edd37bd18a01f2c706b2960cabe72fefea79f6ceec00e758840694d3791980d

python3 Stage1_Instances/THM-M-0342/check_obligation_tree.py
  exit 0
  PASS THM-M-0342 obligation tree: 15 obligations, 102 typed edges
  registry denominator sha256: 3edd37bd18a01f2c706b2960cabe72fefea79f6ceec00e758840694d3791980d
  root closure: open (M2); proof acceptance, source, trust, provenance, and documentation gates remain open

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0342
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  'Stage1Instances.THM_M_0342.root_of_exact_norm_anchor' depends on axioms:
  [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0342
  exit 0; rank 835, planned, theorem_complete false
git diff --check
  exit 0
```

The structural validator checks the exact statement and anchor-audit freeze hashes, deterministic
denominator and eligibility projections, stable node coverage, all eight required typed graphs,
reciprocal proof/composition edges, proof DAG acyclicity, semantic ledgers, step budgets, validation
recipe coverage, open closure, and placeholder hygiene. Lean checks the frozen statement and the
child-to-root composition. The reported axioms come through the pinned imported environment;
`sorryAx` is absent.

This phase freezes interfaces and denominators only. It does not install or accept the discovered
mathlib proof, complete primary-source fidelity or transitive provenance/trust review, produce R0
documentation, or complete the theorem. Master acceptance remains required.
