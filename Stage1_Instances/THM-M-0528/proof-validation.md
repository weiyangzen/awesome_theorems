# THM-M-0528 proof-phase validation

Item: `S56-M-0528-PROOF`. Base revision:
`79350f6756ac2f7d72136216ef446106f56a6fb9`.

`Proof.lean` installs a genuine proof of the exact frozen
`CoveringLiftUniquenessTarget`. The wrapper introduces every canonical binder
and applies the pinned terminal body `IsCoveringMap.eq_of_comp_eq`; it neither
weakens the target nor assumes the pointwise anchor. This closes the frozen
machine proof cut provisionally, subject to master acceptance and the separate
validation gates. It does not claim H0, R0, audit completion, or theorem
completion.

Validation ran on 2026-07-12 using only the existing pinned Lake artifacts. No
update, build, dependency clone, fetch, or `.lake` mutation was performed.

```text
cd Stage1_Instances/THM-M-0528
export ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  lake env lean -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  lake env lean Proof.lean
rm -f Statement.olean
  exit 0
  coveringLiftUniqueness depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0528
  exit 0: rank 585, planned, theorem_complete false

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0528/Proof.lean
  exit 1 with empty output: pass; no prohibited declaration or placeholder
```

The exact pinned mathlib revision was
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Validation, transitive provenance
and trust review, primary-source acceptance, readable reconstruction, hermetic
replay, and independent verification remain downstream.
