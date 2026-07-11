# THM-M-0392 Proof-Phase Validation

Item: `S56-M-0392-PROOF`

## Implemented Bodies

`Proof.lean` implements three frozen root-relevant obligations without a
placeholder or added axiom:

- `M0392-C-CURVE`: constructs the short Weierstrass curve with coefficients
  `(0,0,0,0,k)` and proves its mathlib affine equation is exactly
  `y^2 = x^3 + k`.
- `M0392-L-NONSINGULAR`: calculates its discriminant as `-432*k^2` and proves
  it is nonzero when `k` is nonzero.
- `M0392-T-COORDINATES`: defines the coordinate-preserving map from the frozen
  solution subtype to mathlib affine curve points and proves it injective.

These are genuine local proof bodies, but they do not prove uniform finiteness.
The root remains `M2`: `M0392-X-SIEGEL` has no terminal Lean 4 declaration in
the pinned closure, and neither the canonical root nor theorem completion is
claimed.

## Commands And Results

Commands ran from base revision
`62c2c0315a74e39528d22069068ffe85fea50afd` on 2026-07-12 (receipt timestamp
`2026-07-11T19:27:02Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0392
  exit 0: execution rank 2; planned; theorem_complete=false

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0392/Proof.lean
  exit 0: all four declarations elaborated; each axiom report is a subset of
  propext, Classical.choice, and Quot.sound

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0392/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

python3 -m json.tool Stage1_Instances/THM-M-0392/proof-receipt.json
  exit 0: receipt is valid JSON

git diff --check -- Stage1_Instances/THM-M-0392 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No update, build, clone, fetch, or mutation of `.lake` was performed. This is
a self-tested partial proof execution. The exact remaining machine cut set is
a checked Lean 4 Siegel/integral-points finiteness theorem (or a direct uniform
Mordell-finiteness proof), followed by root composition and later validation.
