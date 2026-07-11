# THM-M-0390 proof-phase validation

## Implemented body

`Proof.lean` proves `solution_bases_coprime`: every natural-number solution of
`x^p + 1 = y^q` with positive exponents has coprime bases. The proof first
derives coprimality of the two powers from their difference of one, then uses
the positive-exponent power/coprime equivalences to descend to `x` and `y`.
The exact-root-hypothesis wrapper `catalan_solution_bases_coprime` is also
kernel checked.

This is a genuine proof body for coprimality step `NP.4` in the frozen
`THM-M-0390-N-PRIMITIVE` ledger. It does not close that whole normalization
obligation, any exponent branch, or the Catalan root. The root vector therefore
remains open and theorem completion is not claimed.

## Commands and results

Commands ran from base revision
`63ffe6d6785bf79248c8559737f408834081b07e` on 2026-07-12 (validation
timestamp `2026-07-11T19:24:17Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0390
  exit 0: execution rank 4; planned; theorem_complete=false

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0390/Proof.lean
  exit 0: both declarations elaborated; #print axioms reported only propext and
  Quot.sound

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0390/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0390
  exit 0: no whitespace errors
```

No update, build, clone, fetch, or mutation of `.lake` was performed. The
pre-existing untracked `Formalizations/Lean/.lake` link was reused as directed.
The remaining root cut set includes the rest of primitive normalization, both
exponent-two classifications, Cassels and Wieferich packages, the cyclotomic
construction, unit and class-group obstructions, residual contradiction, and
child-to-branch composition. Validation, release, H0, R0, hermetic replay, and
theorem completion remain unclaimed.
