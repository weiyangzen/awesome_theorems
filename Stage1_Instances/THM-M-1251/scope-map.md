# Scope map

## Included claim

- A finite-dimensional real vector space, canonically specialized to `R^n` if the source does so.
- The Schwartz space of smooth rapidly decreasing scalar-valued functions.
- Tempered distributions as continuous linear functionals on that Schwartz space.
- The exact locally convex topology used on Schwartz space and any asserted topology on its dual.

## Decisions deferred to statement phase

The inspected source must determine whether the result is a definition, an algebraic/topological
identification, or a representation theorem; whether scalars are real or complex; whether the base
is `R^n` or a general finite-dimensional real normed space; and whether the dual carries pointwise,
weak-star, strong, or another topology. It must also fix dimension-zero behavior, universes, binder
order, continuity structures, and whether equality, equivalence, or homeomorphism is asserted.

## Explicit exclusions

- Ordinary distributions, compactly supported distributions, or distributions on a different test
  function space as substitutes.
- The claim that every tempered distribution is induced by an integrable function.
- Fourier-transform, structure, or representation theorems not present in the selected source.
- Treating the definitional alias `TemperedDistribution` as proof of a stronger strong-dual claim.
- Crediting the legacy wrapper before exact-source and exact-type review.
