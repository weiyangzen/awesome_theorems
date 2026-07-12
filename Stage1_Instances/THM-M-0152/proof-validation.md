# THM-M-0152 proof-phase validation

## Implemented body

`Proof.lean` closes the algebraic content of frozen obligation
`M0152-B-ORIENTATION`: reversing the chosen unit normal negates `L`, `M`, and
`N` together while leaving `(L*N-M^2)/D` unchanged. The proof is a genuine
local Lean body using ring normalization. It does not prove that a geometric
normal reversal produces those three negations; that relationship is already
the frozen meaning of this sign branch.

This is one noncritical branch only. It does not declare or close
`TheoremaEgregiumTarget`, and it does not change the open root classification
`[H1, M4, R3]`. The minimal root cut remains
`M0152-L-INTRINSIC-FORMULA` together with `M0152-T-INVARIANCE`.

## Commands and results

Commands ran in the worker clone from base revision
`bcb28c5ba8db59ba986fdca6d4669097b6c98b3e` on 2026-07-12. Existing canonical
pinned Lake artifacts were reused. No update, build, clone, fetch, or mutation
of `.lake` was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0152
  exit 0: execution rank 651; planned; theorem_complete=false

python3 Stage1_Instances/THM-M-0152/check_obligation_tree.py
  exit 0: 17 obligations and 41 typed edges passed; registry denominator
  fa50f18f390428eeadcb5308decdcc9f9cce7cf2377a1675c74e033b557f634b;
  root open M4

cd Formalizations/Lean && \
  lake env lean ../../Stage1_Instances/THM-M-0152/Proof.lean
  exit 0: gaussianQuotient_neg_normal elaborated; #print axioms reported
  propext, Classical.choice, and Quot.sound

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0152/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit
  98dc76e3c0a9b856c9b98726b713fb04fab16740, Release

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95
```

The proof source SHA-256 is
`af4248cf6607df0b7c0ab05d97773f2b92f1950c4f1ec95a8d74a59e158c99e3`.
This proof phase is self-tested as a truthful partial execution result. It is
not theorem completion and supplies no validation- or release-phase receipt.
