# THM-M-0397 proof-phase validation

## Implemented bodies

`Proof.lean` implements the two directions of the frozen finite-search result.
`listed_is_solution` projects the predicate from filter membership.
`solution_is_listed` uses the supplied Baker lower bound through
`Application.reduce_solution`, converts the resulting height inequality with
`heightBall_spec`, and constructs filter membership. `baker_method` composes
these bodies at the exact type `Statement`.

This is exact kernel closure of the frozen conditional method theorem. It is
not a concrete lower-bound theorem and does not construct a reduction or an
enumerator for a newly chosen Diophantine problem: those are explicitly the
premise and fields quantified by the frozen statement. Source fidelity, trust,
readable reconstruction, downstream validation, release, and master acceptance
remain open, so theorem completion is not claimed.

## Commands and results

Commands ran from base revision
`1cda77577c5e5df2828f773bcfbf7f113ff9927b` on 2026-07-12 (validation
timestamp `2026-07-11T19:45:17Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0397
  exit 0: execution rank 10; planned; theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0397/check_proof.sh
  exit 0: Statement, ObligationTree, and Proof elaborated in a temporary
  module directory; all four proof declarations report only propext,
  Classical.choice, and Quot.sound

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0397/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder
```

No update, build, clone, fetch, or mutation of `.lake` was performed. The
temporary `.olean` files were removed by the validation script's trap.
