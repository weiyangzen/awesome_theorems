# THM-M-0281 scope map

## Received claim

The repository supplies the named family "Jensen's inequality" and the gloss "integral inequality
for convex functions." Intake preserves that integral convex-function family. The gloss is not an
exact truth-valued statement, so this record does not choose a canonical proposition.

## Candidate integral boundary

A common probability-measure formulation says that for an integrable random element `f` and a
convex function `g`, under conditions which make both integrals and the domain constraint valid,

```text
g (integral f dmu) <= integral (g compose f) dmu.
```

This displayed shape is explanatory only. Source and statement review must decide:

1. probability measure, nonzero finite measure with normalized average, or integration over a
   positive finite-measure set;
2. real-valued inputs versus a complete real normed vector space, and real versus ordered-vector
   output;
3. global convexity versus `ConvexOn` on a specified set;
4. whether the set must be closed and whether `g` must be continuous on it;
5. strong measurability and Bochner integrability of `f` and `g compose f`;
6. pointwise versus almost-everywhere membership of `f` in the convex domain;
7. convex inequality versus the concave dual, strict form, or equality characterization;
8. the ordered binders, universes, typeclass instances, notation, exact conclusion, foundation
   profile, and every alternate encoding with a checked relationship.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Convex.Integral` provides these exact-topic candidates:

- `ConvexOn.map_integral_le`: probability-measure integral inequality for a real-valued convex
  function on a closed convex set, with almost-everywhere range and two integrability premises;
- `ConvexOn.map_average_le`: corresponding normalized average for a nonzero finite measure;
- `ConvexOn.map_set_average_le`: corresponding average over a set of nonzero finite measure;
- `ConcaveOn.le_map_integral`: the order-dual concave form;
- `StrictConvexOn.ae_eq_const_or_map_average_lt`: a strict normalized-average alternative.

The import also exposes the finite forms `ConvexOn.map_centerMass_le` and
`ConvexOn.map_sum_le` from `Mathlib.Analysis.Convex.Jensen`. They are related but cannot replace the
catalog's explicit integral-family gloss. The usable candidates justify provisional `M3`, not
`M0`: no source-selected expression, checked transport, proof-body audit, or accepted receipt exists.

## Boundary cases

Statement work must explicitly settle the zero measure and nonzero-measure assumption, empty
spaces and empty restricted sets, zero-dimensional domains, constant functions, affine functions,
nonintegrable functions, functions leaving the convex domain on a null set, nonclosed domains,
extended-real-valued variants, and equality or strictness when the input is almost everywhere
constant. No degenerate case is excluded at intake.

## Explicit exclusions

- A finite weighted-sum theorem substituted for the requested integral family.
- Conditional Jensen inequality, Jensen's formula in complex analysis, or a special inequality for
  one named convex function.
- A concave, strict, or equality-case theorem used as the convex non-strict integral root without
  a source-approved relationship.
- A probability-only or finite-dimensional special case used as a more general theorem.
- A hypothesis or structure field that already stores the desired inequality.
- Numerical quadrature, sampling, floating-point evidence, an oracle, or an unchecked certificate.
- The untrusted `已验证` label, a theorem-name match, `#check`, or `#print axioms` used as proof
  credit.

## Neighbor boundary

`THM-M-0279` (Holder inequality), `THM-M-0280` (Minkowski inequality), and `THM-M-0282`
(Chebyshev inequality) remain separate targets. Their future artifacts grant no source or proof
credit here. This intake owns only `Stage1_Instances/THM-M-0281`.
