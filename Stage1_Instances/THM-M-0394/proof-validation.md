# THM-M-0394 proof-phase validation

## Implemented bodies

`Proof.lean` closes the exact logical expansion of frozen obligation `M0394-S3`: the common model
compatibility fields together with the positive-genus versus genus-zero/three-boundary disjunction.
It also supplies a proof-phase declaration for `M0394-B`, composing explicit proofs of the two
finiteness branches into the canonical `Statement`.

These are genuine proof bodies, but neither branch premise is asserted. In particular, this artifact
does not prove Siegel's theorem, does not declare the root, and does not change the root vector
`[H3, M3, R3]`. The positive-genus Diophantine approximation engine and the genus-zero S-unit
finiteness engine are absent from pinned mathlib and remain deep formalization debt.

## Commands and results

Commands ran from base revision `dcd0f230f4229c83e14c59ed981b3e5232bc594a` on 2026-07-12
(validation timestamp `2026-07-11T19:29:54Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0394
  exit 0: execution rank 7; planned; theorem_complete=false

cd Formalizations/Lean && \
  bash ../../Stage1_Instances/THM-M-0394/check_proof.sh
  exit 0: statement, obligation tree, and proof module elaborated; both local
  proof declarations report only propext, Classical.choice, and Quot.sound

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0394/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0394
  exit 0: no whitespace errors
```

The validation script removes its temporary local `.olean` files. No update, build, clone, fetch, or
mutation of `.lake` was performed. This proof phase is a truthful partial execution result pending
master acceptance. `M0394-N`, `M0394-N1`, `M0394-B1`, `M0394-B2`, their substantive children, and
`M0394-T` remain open; validation, release, H0, R0, and theorem completion are unclaimed.
