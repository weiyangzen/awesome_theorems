# THM-M-0391 proof-phase validation

## Implemented body

`Proof.lean` closes frozen obligation `M0391-B-EE`: if `X,Y > 1`, then
`X^2 = Y^2 + 1` is impossible. The proof first derives `Y < X` by monotonicity
of squaring, then compares `(Y+1)^2` with `X^2`; polynomial normalization and
Presburger arithmetic yield the contradiction. This is a genuine local proof
body, but it is only one branch. It does not declare or close the Mihailescu
root, and it does not change the root vector `[H1, M4, R4]`.

## Commands and results

Commands ran from base revision
`c15bbbe61f10abb7d0cf2bc6e8de86f572733d01` on 2026-07-12 (validation
timestamp `2026-07-11T19:18:34Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0391
  exit 0: execution rank 5; planned; theorem_complete=false

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0391/Proof.lean
  exit 0: evenEvenImpossible elaborated; #print axioms reported only
  propext and Quot.sound

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0391/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

git diff --check -- Stage1_Instances/THM-M-0391
  exit 0: no whitespace errors
```

No update, build, clone, fetch, or mutation of `.lake` was performed. The
proof phase is self-tested as a truthful partial execution result. The open
root cut set still includes exponent normalization, power lifting, the EO/OE/OO
branches, lift-back, and exact child-to-parent root composition. Validation,
release, H0, R0, hermetic replay, and theorem completion remain unclaimed.

