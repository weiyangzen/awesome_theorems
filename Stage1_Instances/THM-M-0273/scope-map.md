# Scope map

## Received claim

`Docs/researches/math_theorems.md` supplies only the title "Radon-Nikodym theorem" and the gloss
"absolute continuity of measures and density functions." That is a theorem-family description,
not a truth-valued proposition. This intake freezes the family boundary and the choices which the
statement phase must make; it does not invent a canonical theorem.

## Candidate classical boundary

A common positive-measure formulation has two measures `mu` and `nu` on one measurable space and
says that absolute continuity of `mu` with respect to `nu` is equivalent to representation of
`mu` by integration against a nonnegative measurable density. This is a candidate shape only. The
source review must fix:

- whether measures are finite, sigma-finite, s-finite, localizable, or subject to another
  decomposition hypothesis;
- whether the target concerns positive measures or signed, complex, or vector measures;
- which measure is absolutely continuous with respect to which;
- whether the conclusion is existence, an equivalence, an integral identity on every measurable
  set, equality with a density-weighted measure, or identification with a named derivative;
- the density codomain (`Real`, nonnegative reals, or `ENNReal`), measurability, integrability,
  finiteness, and almost-everywhere uniqueness clauses;
- all universes, measurable-space data, ordered binders, and empty/zero/infinite boundary cases.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.MeasureTheory.Measure.Decomposition.RadonNikodym` provides
`Measure.absolutelyContinuous_iff_withDensity_rnDeriv_eq`:

```text
[Measure.HaveLebesgueDecomposition mu nu] ->
  mu << nu <-> nu.withDensity (mu.rnDeriv nu) = mu
```

Here `mu` and `nu` are positive `Measure alpha` values, `rnDeriv` is `ENNReal`-valued, and
`HaveLebesgueDecomposition` packages a singular measure plus a measurable density decomposition.
The same pinned source supplies the one-way theorem `withDensity_rnDeriv_eq`. An instance obtains
the decomposition for an s-finite first measure and sigma-finite reference measure; a separate
theorem covers finite measures.

Module `Mathlib.MeasureTheory.VectorMeasure.Decomposition.RadonNikodym` separately provides
`SignedMeasure.absolutelyContinuous_iff_withDensityᵥ_rnDeriv_eq` for a signed measure and a
sigma-finite positive reference measure. Nikodym's historical Theorem III is phrased for a real-
valued perfectly additive set function, making this a material candidate rather than a variant
which intake may discard. The historical theorem is an implication plus an almost-everywhere
uniqueness clause, not literally the modern `iff`. A complete definition, convention, and direction
crosswalk is still open.

This is a strong exact-topic formal candidate, hence provisional `M3` rather than `M4`. It is not
`M0`: the source variant, normalized expression match, exact wrapper or transport, terminal proof-
body provenance, axiom policy, and node-specific accepted receipt remain downstream work.

## Required statement decisions

1. Admit and independently review an immutable source edition and pinpoint theorem passage.
2. Crosswalk every incorporated definition, binder, premise, direction, conclusion, and erratum.
3. Select the measure category and finiteness/decomposition hypotheses without strengthening or
   weakening the source.
4. Fix the density codomain, measurability/integrability requirements, measure orientation,
   equality/integral form, and uniqueness clause.
5. Decide whether the pinned mathlib declaration is the canonical target, an alternate encoding,
   or only an anchor, and compile any required relationship witness.
6. Resolve zero measures, the empty measurable space, infinite densities, non-sigma-finite cases,
   and equality up to almost everywhere equivalence.

## Explicit exclusions

- Lebesgue decomposition alone without the absolute-continuity/density conclusion.
- The Lebesgue differentiation theorem, Riesz representation, disintegration, conditional
  expectation, or change-of-variables results.
- Signed-, complex-, or vector-measure variants substituted for a positive-measure source, or the
  converse substitution.
- A finite/probability-measure special case used as an unrestricted general theorem.
- A structure or hypothesis that stores the desired density representation as data.
- The untrusted `已验证` label, theorem-name match, source URL, or intake probe used as proof credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion, checked alternate encoding,
or degenerate-case exclusion is frozen by this intake.
