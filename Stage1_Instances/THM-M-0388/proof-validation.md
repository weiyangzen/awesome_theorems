# THM-M-0388 Proof Validation

## Implemented closure

`Proof.lean` proves the exact frozen integer existence proposition. The local proof converts
`not exists k, k*k=D` to mathlib's `not IsSquare D`, then invokes the terminal proof body
`Pell.exists_of_not_isSquare` from pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The wrapper neither strengthens nor weakens the
canonical conclusion. The upstream body remains owned by mathlib; this is an `M0-W` proposal, not a
repo-local reimplementation and not theorem release.

## Commands and results

Commands ran from base revision `fbc2d39d72ad14c2a116e6f9e3721b6e4af8218d` on 2026-07-12
(validation timestamp `2026-07-11T19:02:24Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0388/Proof.lean
  exit 0
  Pell.exists_of_not_isSquare has the expected integer Pell existence type
  not_isSquare_of_isNonsquareInteger has no axioms
  Pell.exists_of_not_isSquare and pellEquationStatement use only:
    propext, Classical.choice, Quot.sound

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0388/Proof.lean \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/Pell.lean
  exit 1 with empty output: pass, no prohibited declarations or placeholders found

git diff --check -- Stage1_Instances/THM-M-0388
  exit 0: no whitespace errors
```

No `lake update`, build, clone, fetch, or `.lake` mutation was performed. The proof phase is
self-tested and remains provisional pending master acceptance. Validation and release phases,
including hermetic replay, independent verification, H0, R0, and the theorem-completion decision,
remain outside this item's claim.
