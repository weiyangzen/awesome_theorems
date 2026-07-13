# Scope map

## Received claim

`Docs/researches/math_theorems.md` supplies only the title "Markov inequality" and the gloss
"probability upper bound for a nonnegative random variable." The same six-field record appears in
both the real-analysis and probability sections; the generated target retains the former category.
This is a theorem-family description, not an exact truth-valued proposition. Intake preserves that
boundary rather than inventing a canonical theorem.

## Candidate classical boundary

A common formulation says that, for a nonnegative random variable `X` and a positive real threshold
`epsilon`, the probability of `X >= epsilon` is at most `E[X] / epsilon`. This is a candidate shape
only. Source review and statement freeze must decide:

- whether the ambient object is a probability space or an arbitrary measure space;
- whether `X` is real-, nonnegative-real-, or extended-nonnegative-real-valued;
- whether nonnegativity and measurability hold pointwise or almost everywhere, and whether
  integrability or finiteness of expectation is required;
- whether the threshold is real or extended nonnegative, strictly positive, nonzero, and finite;
- whether the event is `{X >= epsilon}` or `{X > epsilon}`;
- whether probability, measure, expectation, and integral values live in `Real` or `ENNReal`;
- whether the conclusion is product form or division form and how zero and infinite values behave;
- all universes, measurable-space data, ordered binders, coercions, and empty/zero/infinite cases.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.MeasureTheory.Integral.Lebesgue.Markov` provides:

```text
mul_meas_ge_le_lintegral₀:
  AEMeasurable f mu -> epsilon * mu {x | epsilon <= f x} <= integral f

meas_ge_le_lintegral_div:
  AEMeasurable f mu -> epsilon != 0 -> epsilon != infinity ->
  mu {x | epsilon <= f x} <= integral f / epsilon
```

Here `f : alpha -> ENNReal`, so nonnegativity is encoded in the codomain. The measurable wrapper
`mul_meas_ge_le_lintegral` uses the same product conclusion. Module
`Mathlib.MeasureTheory.Integral.Bochner.Basic` separately provides
`mul_meas_ge_le_integral_of_nonneg` for an integrable real-valued function with almost-everywhere
nonnegativity and a `Real` threshold, using `mu.real` and product form.

These are strong exact-topic formal candidates, hence provisional `M3` rather than `M4`. They are
not `M0`: source identity, canonical encoding, normalized expression match, wrapper or transport,
terminal-body provenance, transitive trust, and node-specific acceptance remain downstream work.

## Required statement decisions

1. Admit an immutable primary or authoritative source and independently review the exact theorem,
   incorporated definitions, assumptions, proof boundary, corrections, and errata.
2. Map every source binder, premise, inequality direction, event convention, and conclusion.
3. Select the ambient measure and value codomains without strengthening or weakening the source.
4. Freeze nonnegativity, measurability, integrability, threshold, and boundary assumptions.
5. Decide whether one pinned declaration is canonical, an alternate encoding, or only an anchor,
   and compile every credited relationship witness.
6. Resolve the zero measure, zero random variable, empty sample type, zero/infinite threshold,
   infinite expectation, null modification, and strict-versus-closed event cases.

## Explicit exclusions

- Chebyshev's second inequality, Chernoff bounds, Hoeffding bounds, or martingale inequalities.
- A finite/counting/cardinality Markov inequality substituted for the random-variable theorem.
- A signed or arbitrary real-valued function without the source-required nonnegativity premise.
- A probability-space special case used as an unrestricted general-measure theorem, or conversely.
- A strict-tail statement silently substituted for a closed-tail statement.
- A hypothesis or structure that stores the desired bound as data.
- The untrusted `已验证` label, theorem-name match, source URL, or intake probe used as proof credit.

No canonical Lean expression, ordered binders, hypotheses, conclusion, checked alternate encoding,
or degenerate-case exclusion is frozen by this intake.
