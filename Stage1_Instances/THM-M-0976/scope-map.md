# Scope map

## Received claim

`Docs/researches/math_theorems.md` repeats the same six-field McDiarmid record in combinatorics,
probability, and stochastic-process sections. Each says only "concentration of bounded-difference
functions." The generated manifest retains the combinatorics category. This is a theorem-family
description, not a binder-complete proposition, so intake preserves it without selecting a modern
variant.

## Candidate classical boundary

A common finite-coordinate formulation takes independent random variables `X_i`, a real-valued
measurable function `f` of their tuple, and nonnegative constants `c_i` such that changing only
coordinate `i` changes `f` by at most `c_i`. It then gives a sub-Gaussian upper-tail estimate around
`E[f(X)]`, commonly displayed with exponent `-2*t^2 / sum c_i^2`. This is a candidate family only,
not the frozen target.

The source and statement phases must decide:

1. The finite index type and each coordinate's carrier, measurable space, probability law, and
   independence/product-measure encoding.
2. Whether the input is a family of random variables on one probability space, a product-space
   identity map, or another source-faithful encoding.
3. The codomain and measurability/integrability assumptions for `f`, including whether values or
   expectations are real, nonnegative real, or extended real.
4. The exact replacement relation: all tuples differing only at coordinate `i`, essential
   coordinate ranges, one-sided oscillation, or absolute oscillation.
5. Whether each `c_i` is nonnegative, whether the bound is `<` or `<=`, pointwise or almost surely,
   and whether constants may depend on other coordinates.
6. The centered quantity: `f(X) - E[f(X)]`, `E[f(X)] - f(X)`, median centering, conditional
   centering, or absolute deviation.
7. Upper, lower, two-sided, or moment/expectation conclusion; strict or closed event; threshold
   domain and sign; and `Real` versus `ENNReal` probability comparison.
8. The exponent constant and denominator normalization, especially `-2*t^2 / sum c_i^2` versus
   conventions using interval widths, half-widths, or a factor `1/2`.
9. Ordered binders, universes, coercions, minimal imports, foundation/TCB/computation profiles,
   elaborated expression and environment fingerprints, and checked transports.

## Boundary cases

Source review must resolve an empty index type, singleton coordinates, empty or subsingleton
coordinate spaces, constant `f`, zero `c_i`, `sum c_i^2 = 0`, negative and zero thresholds, null-set
modifications, infinite/nonintegrable expectations, nonmeasurable functions, probability-zero
events, and whether tuple replacement requires decidable equality on indices. No case is excluded
at intake.

## Neighbor and substitution exclusions

- `THM-M-0975` is Azuma-Hoeffding concentration for martingale differences, not automatically the
  independent-coordinate function theorem.
- `THM-M-0977`, `THM-M-0978`, and `THM-M-0994` own Chernoff or Hoeffding sum bounds. A bounded sum is
  a special application, not a substitute for a general coordinate-sensitive function.
- `THM-M-0974` owns a Talagrand concentration family; convex distance or convex-Lipschitz hypotheses
  cannot replace bounded coordinate differences.
- `THM-M-1080` separately owns Azuma's inequality in the stochastic-process category.
- A variance-sensitive Bernstein/Freedman result, Efron-Stein expectation bound, concentration about
  a median, or infinite-coordinate extension is not silently interchangeable with the selected root.
- A hypothesis or structure that stores the desired tail inequality is circular.
- The catalog's `已验证` label, a theorem-name match, source URL, API probe, finite experiment, or
  Hoeffding wrapper supplies no target proof credit.

## Formal boundary and handoff

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides
`ProbabilityTheory.iIndepFun`, probability measures and real-valued measure, integration,
`Function.update`, finite sums, and `Real.exp`. It also contains Hoeffding/Azuma sub-Gaussian
infrastructure, but the bounded search located no exact function-of-independent-coordinates
McDiarmid theorem. These are adjacent interfaces only.

The statement phase must first admit and independently review an immutable source proposition, then
freeze and mutation-test its exact Lean expression. Only later phases may audit formal candidates,
freeze obligations and typed graphs, implement proof bodies, or claim closure.
