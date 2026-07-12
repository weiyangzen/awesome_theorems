# THM-M-1521 proof-phase validation

Item: `S56-M-1521-PROOF`. Base revision:
`2b5a356f0d547597e745bab548db0caac12e6c96`.

`Proof.lean` imports the two pinned mathlib terminal bodies, implements both
frozen bridge-package interfaces, and composes them through
`ObligationTree.exactTarget_of_packages` at the exact statement-phase target.
The explicit finite-measure proposition is installed as the typeclass needed
by `MeasurePreserving.conservative`. The recurrence package is discharged by
`Conservative.ae_mem_imp_frequently_image_mem` without changing its set,
null-measurability, almost-everywhere, or `Frequently atTop` binders.

This supports a provisional `M0-W` proposal for the exact root. It is not
theorem completion: validation, release, H0/R0, full transitive provenance and
trust review, hermetic replay, independent verification, and master acceptance
remain open.

Validation ran in the worker clone on 2026-07-12. Existing pinned `.lake`
artifacts were reused; no update, build, clone, fetch, or dependency mutation
was run.

```text
python3 Stage1_Instances/THM-M-1521/check_proof.py
  exit 0
  Both frozen bridge packages and the exact root wrapper elaborated.
  The two imported terminal declarations and all three local declarations
  each depend only on [propext, Classical.choice, Quot.sound].

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1521
  exit 0: rank 180, planned, theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-1521/proof-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-1521 \
  .stage1-worker-selftest.json
  exit 0: no output
```

The proof source has no placeholder, new axiom, or unsafe declaration. The
terminal source is pinned mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; exact source and compiled artifact
hashes are recorded in `proof-receipt.json`. Master acceptance must preserve
the downstream assurance boundary above.
