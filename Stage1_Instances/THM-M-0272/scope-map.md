# Scope map

## Received claim

`Docs/researches/math_theorems.md:1957-1962` fixes only the title `托内利定理`, Leonida Tonelli,
the year 1909, and `非负函数的重积分` ("multiple integrals of nonnegative functions"). It gives
no primary citation, formula, definitions, premises, theorem locator, proof boundary, correction
record, reviewer, or formal artifact. This intake freezes that sparse boundary rather than choosing
a theorem from its name.

## Candidate classical boundary

A common modern Tonelli formulation concerns a nonnegative measurable extended-real-valued function
on the product of two sigma-finite measure spaces. It equates its integral against the product
measure with either iterated integral and permits the common value to be infinite. That is a
candidate family, not the accepted root. Statement review must fix:

- the measurable spaces, measures, and sigma-finite, s-finite, finite, or other assumptions;
- how the product measure is defined and whether completed measures or completions are involved;
- whether the function is measurable, almost-everywhere measurable, or represented modulo almost-
  everywhere equality;
- whether the codomain is nonnegative reals, extended nonnegative reals, or an encoding of the
  positive and negative parts of a real-valued function;
- which equality directions and integration orders are included, and whether equality of both
  iterated integrals is explicit;
- whether measurability of the inner integral is a conclusion or a prerequisite;
- whether the root is the whole-space theorem, a theorem on measurable rectangles, a set-integral
  theorem, or a sums/counting-measure specialization;
- every universe, typeclass, binder, coercion, infinity convention, and boundary case.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.MeasureTheory.Measure.Prod` directly labels `MeasureTheory.lintegral_prod` as Tonelli's
theorem. Its candidate interface uses measurable spaces `alpha` and `beta`, measures `mu` and `nu`,
an `[SFinite nu]` instance, a function `f : alpha x beta -> ENNReal`, and
`AEMeasurable f (mu.prod nu)`. It concludes that the product `lintegral` equals the `mu`-then-`nu`
iterated `lintegral.

The same module provides distinct interfaces:

- `lintegral_prod_symm` additionally assumes `[SFinite mu]` and reverses the iteration order;
- `lintegral_lintegral` uses a curried function and the reverse equality orientation;
- `lintegral_lintegral_swap` states equality of the two iterated integrals;
- `setLIntegral_prod` and `setLIntegral_prod_symm` restrict to product sets;
- `Measurable.lintegral_prod_right'` establishes measurability of the inner integral under a
  stronger pointwise measurability premise.

These direct interfaces establish feasibility and justify provisional M3. None is selected merely
because mathlib calls it Tonelli's theorem. Exact expression serialization, minimal-import proof,
source transport, mutations, proof-body provenance, and trust acceptance belong downstream.

## Degenerate and boundary cases to resolve

- empty measurable spaces and zero measures;
- an integrand identically zero, infinite, or infinite only on a null set;
- integrals and iterated integrals equal to infinity;
- a nonmeasurable function, an only almost-everywhere measurable representative, or a measurable
  modification;
- failure of sigma-finiteness or s-finiteness and whether the product-measure construction still
  gives the intended statement;
- non-complete versus completed measures and product sigma-algebra conventions;
- singleton/counting-measure reductions and whether infinite double series are in scope;
- whole-space versus restricted-set integration and null-set changes of the integrand.

No case is excluded at intake. The source-approved statement must decide each one or prove that the
chosen representation handles it uniformly.

## Excluded substitutions

- `THM-M-0271` Fubini's theorem for integrable signed or real-valued functions;
- `THM-M-1266`, the distinct calculus-of-variations Tonelli existence theorem;
- finite sums, finite products, counting measures, Euclidean Lebesgue measure, probability spaces,
  or indicator functions used as the unrestricted root;
- a one-sided inequality such as `lintegral_prod_le` in place of the requested equality family;
- a proposition whose premises or structure fields already store the desired iterated-integral
  equality;
- the untrusted `已验证` label, a theorem name, or the discovery probe used as source or proof credit;
- the unrelated legacy slot file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_272.lean`, which
  identifies itself as `THM-M-0992` and formalizes Chebyshev's inequality.

## Exit condition for statement work

An independently reviewed immutable source must select one exact Tonelli proposition and map every
definition, premise, binder, conclusion, order, infinity convention, exceptional case, proof
boundary, correction, and erratum. Only then may the statement phase freeze a minimal-import Lean
expression, environment and expression fingerprints, checked alternate transports, and required
mutations.
