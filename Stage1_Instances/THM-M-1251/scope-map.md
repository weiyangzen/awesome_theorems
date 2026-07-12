# Scope map

## Included claim

- A finite-dimensional real vector space, canonically specialized to `R^n` if the source does so.
- The Schwartz space of smooth rapidly decreasing scalar-valued functions.
- Tempered distributions as continuous linear functionals on that Schwartz space.
- The exact locally convex topology used on Schwartz space and any asserted topology on its dual.

## Statement decisions

The canonical Lean target uses a general finite-dimensional real normed space, complex-valued
Schwartz maps and distributions, equality of types, and mathlib's pointwise-convergence topology.
Dimension zero is included. These choices give an exact elaborated interpretation of the repository
phrase without upgrading it to a strong-dual homeomorphism. Primary-source review must still decide
whether this formal target exhausts the intended historical claim before `H0` can be assigned.

## Explicit exclusions

- Ordinary distributions, compactly supported distributions, or distributions on a different test
  function space as substitutes.
- The claim that every tempered distribution is induced by an integrable function.
- Fourier-transform, structure, or representation theorems not present in the selected source.
- Treating the definitional alias `TemperedDistribution` as proof of a stronger strong-dual claim.
- Crediting the legacy wrapper before exact-source and exact-type review.
