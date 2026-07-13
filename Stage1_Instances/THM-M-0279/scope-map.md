# Scope map

## Preserved catalog scope

This intake preserves the catalog's real-analysis product-integral Holder family. In conventional
modern notation, a likely interior-exponent member bounds the integral of the pointwise magnitude
or norm product of two functions by the product of their `L^p` and `L^q` norms when `p` and `q` are
conjugate. That is a resolution target, not the frozen canonical statement: the catalog contains no
formula or source locator from which to choose all binders and hypotheses.

The phrase `L^p空间的乘积积分` distinguishes this target from the separately cataloged
`THM-M-0310` duality/representation family. It does not distinguish the following mutually
nonidentical variants.

## Proposition-changing decisions

The statement phase must resolve every item from an admitted source and independently reviewed
crosswalk:

1. The underlying measurable or measure space, whether the measure is arbitrary or Lebesgue, and
   whether the integral is over the whole space or a specified measurable subset.
2. Raw functions versus almost-everywhere equivalence classes in `Lp`, and the scalar or value
   carrier: `ENNReal`, `NNReal`, `Real`, `Complex`, or a normed additive group with a bilinear map.
3. Pointwise multiplication versus `|f * g|`, `norm f * norm g`, a scalar action, or an abstract
   bounded bilinear operation; for complex pairings, whether conjugation is present.
4. Lebesgue `lintegral`, real/Bochner integral, or an `eLpNorm` conclusion, including coercions and
   whether the left side is signed, absolute, or norm-valued.
5. Finite real conjugates `1 < p, q < infinity` versus extended exponents that include the
   `p = 1, q = infinity` endpoints, and the exact conjugacy predicate.
6. `AEMeasurable`, `AEStronglyMeasurable`, `MemLp`, integrability, nonnegativity, finiteness, or
   sigma-finiteness assumptions and their binder order.
7. The source edition, exact theorem/page or archival passage, incorporated definitions, proof
   boundary, translation, attribution, correction or errata record, and independent review.
8. The foundation, axiom, TCB, computation, freshness, and revocation profiles for the selected
   target and its minimal import closure.

## Boundary and mutation cases

The source crosswalk must explicitly decide zero or almost-everywhere-zero functions, the zero
measure, infinite measure, divergent seminorms, functions changed on null sets, and exponent
endpoints. For extended nonnegative integrals, `0` and `infinity` values are meaningful boundary
cases; for finite Bochner variants, `MemLp` rules them out differently.

Required statement mutations must reject removal of a source-required measurability or `MemLp`
hypothesis, a nonconjugate exponent pair, a changed function/value domain, a binder-scope change,
and an endpoint or infinite-norm interpretation not covered by the selected source. No equality
characterization, best-constant theorem, converse, representation/surjectivity claim, or finite-sum
form is silently included by the catalog gloss.

## Explicit exclusions

- `THM-M-0310`'s `L^p`-duality or continuous-functional representation theorem. Holder's
  inequality may be a dependency of that result but is not equivalent to it.
- Finite-sum or sequence Holder inequality, the multi-function generalized inequality, or a general
  Holder-triple bilinear theorem used as the root without a checked source-approved specialization.
- Young's inequality, Minkowski's inequality, or only the `p = q = 2` Cauchy-Schwarz case.
- A structure or hypothesis that stores the desired inequality, an `Lp` pairing interface whose
  boundedness is already assumed, or a preselected proof-bearing witness.
- The catalog's verified label, a mathlib theorem name, successful `#check`, or axiom output used as
  source identity, statement identity, or proof credit.

## Pinned formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the closest literal
surfaces include `ENNReal.lintegral_mul_le_Lp_mul_Lq`,
`NNReal.lintegral_mul_le_Lp_mul_Lq`,
`MeasureTheory.integral_mul_norm_le_Lp_mul_Lq`, and
`MeasureTheory.integral_mul_le_Lp_mul_Lq_of_nonneg`. The first two use nonnegative extended or
nonnegative real functions and `lintegral`; the latter two use finite real conjugate exponents and
`MemLp`, with norm-product or nonnegative-real conclusions. The generalized
`MeasureTheory.eLpNorm_le_eLpNorm_mul_eLpNorm_of_nnnorm` supports extended exponent triples and a
bilinear operation.

These APIs justify provisional `M3` discovery status only. Their exact types and reported axioms do
not decide which statement the catalog means, do not freeze minimal canonical imports or an
expression fingerprint, and do not transfer terminal proof-body or completion credit. The later
statement and anchor-audit phases must select and check one exact mapping before proof inspection.
