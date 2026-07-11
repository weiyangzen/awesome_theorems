# THM-M-0394 Statement Validation

## Frozen Target

`Stage1Rev56.THMM0394.Statement` is the number-field form of Siegel's theorem selected by the
accepted intake scope. Its ordered parameters are the number field `K`, a finite set `S` of finite
primes, and a `CurveModel K`. `IsSiegelCurve C` requires a dimension-one affine smooth
geometrically integral curve, a compatible smooth proper completion and geometric boundary, and
either positive genus or genus zero with at least three geometric boundary points. The conclusion
is finiteness of the rational section points whose frozen affine coordinates are `S`-integers.

The finite-prime encoding incorporates the usual requirement that `S` contain the archimedean
places: archimedean places do not occur in the valuation definition of the `S`-integer ring. The
empty integral-point set is allowed. Singular, reducible, non-affine, and non-dimension-one objects
are outside the target. The statement does not assert model independence, effective bounds, or
uniformity.

The pinned mathlib snapshot has concrete predicates for affineness, smoothness, geometric
integrality, properness, open immersions, rational sections, and `S`-integers. It lacks a complete
curve genus/geometric boundary/integral-model interface. `CurveModel` therefore carries explicit
genus, geometric boundary, and coordinate data together with named semantic compatibility
predicates. These predicates are hypotheses about one selected mathematical object model, not
arbitrary hypotheses passed independently to the theorem. Replacing them requires checked
transports; weakening or deleting them changes the target.

`statement_iff_expanded` checks the complete binder order and proposition by definitional
equality. `mem_integralPointSet_iff` checks the integral-point set encoding. Neither declaration
proves Siegel's theorem.

## Pinned Environment

- Repository base: `f87604acb61507f0c9c8d5de4ba3085b97a1de69`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`
- `Statement.lean` SHA-256: `7db337b7285aa5908d1504574e09bb3ba02d13bdada499da93f3d79035a27cc8`

## Commands And Results

Run from the repository root unless a working directory is specified.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots,
  1546 uniform-L0 Lean 4 targets, execution skill present)
python3 scripts/stage1_target.py check
  exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
python3 scripts/stage1_target.py show THM-M-0394
  exit 0: rank 7; baseline L0; rework_required true; lifecycle planned; theorem_complete false
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0394/Statement.lean
  exit 0: Stage1Rev56.THMM0394.Statement.{u, v} : Prop
cd Formalizations/Lean && lake env lean --version
  exit 0: Lean (version 4.29.0, x86_64-unknown-linux-gnu,
  commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)
git diff --check -- Stage1_Instances/THM-M-0394
  exit 0: no output
```

This evidence establishes statement elaboration only. Source pinpointing, anchor audit, a proof
body, trust/provenance and hermetic release gates, independent review, and master acceptance remain
open. No theorem completion is claimed.
