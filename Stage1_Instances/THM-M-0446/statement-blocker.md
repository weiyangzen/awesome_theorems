# Statement gate blocker

Item: `S56-M-0446-STATEMENT`  
Theorem: `THM-M-0446`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The intake selects Wiles's published root: every semistable elliptic curve over
the rational numbers is modular. The pinned Lean environment cannot express
that claim exactly. Mathlib provides `WeierstrassCurve`, its `IsElliptic`
predicate, and local good, multiplicative, and additive reduction predicates
in `Mathlib.AlgebraicGeometry.EllipticCurve.Reduction`. It does not provide:

- a global semistability predicate for a rational elliptic curve, quantified
  over all finite primes and invariant under the necessary local models; or
- elliptic-curve modularity, a weight-two eigenform/newform object with its
  eigenform property, or the required curve-to-form L-series or Galois-
  representation compatibility relation.

The local reduction API is parameterized by a discrete valuation ring `R`, its
fraction field `K`, and a chosen Weierstrass equation. Simply defining
semistability as `HasGoodReduction R W ∨ HasMultiplicativeReduction R W` for
one arbitrary `R` would omit the all-primes quantifier and the transport from a
curve over `ℚ` to its local minimal models. Likewise, `Nonempty (ModularForm
Γ 2)` is not modularity of a curve: the zero modular form inhabits it and it
contains no Hecke-eigenform or compatibility condition.

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_064.lean` does not repair this
gap. Its input structure stores `semistable`,
`residualRepresentationAttached`, and all three modular compatibility
conditions as unconstrained `Prop` fields. Its `StatementShape` also adds the
residual-representation premise to the intake root. Reusing it would therefore
substitute an abstract interface and broaden the hypotheses rather than
elaborate the exact theorem. It receives no rev-5.6 statement credit.

`StatementProbe.lean` is consequently only a checked substrate probe. It uses
the minimal relevant import, prints the available local declarations, and
defines the honest domain abbreviation
`Stage1Instances.THM_M_0446.RationalEllipticCurve`. It declares no proxy
predicate and makes no theorem claim.

The required exact ordered binders, semistability hypothesis, modularity
conclusion, expression fingerprint, checked alternate encoding, and meaningful
hypothesis mutations therefore cannot be produced truthfully. The root remains
`M4`, theorem completion is false, and no statement-node self-test manifest is
emitted.

## Environment fingerprint

- Repository base revision: `91cf43768c2b03b5c98d8ca436c450ba5a70babb`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned reduction source SHA-256:
  `59f3978ec479a63e9f3d71bfd564114c613bcf7f189a38bf66dd5566b617918f`.

## Validation evidence

Commands ran inside this worker clone using only the existing pinned `.lake`
artifacts. No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0446/StatementProbe.lean` | 0 | Minimal-import probe elaborated; the local reduction declarations and rational elliptic-curve domain printed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'semistable\|semi-stable\|multiplicative reduction\|isMultiplicativeReduction\|elliptic.*modular\|modular.*elliptic\|newform\|eigenform' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only reduction documentation/declaration and an FLT bibliography hit; no global semistability or elliptic modularity declaration |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0446` | 0 | Rank 64, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Retry condition

Supply pinned Lean definitions for global semistability of elliptic curves over
`ℚ` and for association with a normalized weight-two Hecke eigenform,
including the precise level and a concrete compatibility relation. The next
statement run must then elaborate `∀ E : RationalEllipticCurve, Semistable E
→ Modular E`, check that the definitions match the primary-source meanings,
and mutation-test removal of semistability, restriction of the curve domain,
the all-primes scope, and the weight/level/compatibility conditions.

Until those definitions exist in the pinned dependency closure, statement
acceptance and theorem completion remain false. Because the assigned phase is
not self-tested to its completion gate, `.stage1-worker-selftest.json` is not
written.
