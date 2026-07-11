# THM-M-0414 proof-phase validation

Item: `S56-M-0414-PROOF`. Base revision:
`d597fdb5ebb83567497a9aedd50af4142cf18c58`.

This phase directly integrates the two terminal declarations identified by the
immutable anchor audit. `idealUniqueFactorizationTarget_proof` has precisely the
canonical type frozen in `Statement.lean`; its first component is
`Ideal.uniqueFactorizationMonoid`, and its second component is
`Ideal.finprod_heightOneSpectrum_factorization` with the unchanged nonzero premise.
Thus the unit ideal remains in scope and only the zero ideal is excluded.

Validation ran from the worker clone on 2026-07-12 local time. Existing canonical pinned
`.lake` artifacts were reused through the worker symlink. No update, build, dependency clone,
fetch, or network operation was run.

```text
bash Stage1_Instances/THM-M-0414/check_proof.sh
  exit 0
  idealUniqueFactorizationMonoid_proof depends on [propext, Classical.choice, Quot.sound]
  idealFiniteProductFactorization_proof depends on [propext, Classical.choice, Quot.sound]
  idealUniqueFactorizationTarget_proof depends on [propext, Classical.choice, Quot.sound]
  PASS: exact root and both frozen components are present without forbidden proof tokens

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0414
  exit 0: rank 69; planned; L0/rework_required; theorem_complete=false
git diff --check -- Stage1_Instances/THM-M-0414 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The source scan rejects `sorry`, `admit`, axiom declarations, `sorryAx`, and unsafe declarations.
This is self-tested proof-node evidence pending master acceptance. It closes the three proof-graph
obligations, but it does not close the separate trust obligation, validation, source/readability,
release, or theorem-completion gates.
