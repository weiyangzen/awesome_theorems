# Scope map

## Included theorem family

- A nonlinear Schrodinger initial-value problem on Euclidean space, with the sign and normalization
  of the Laplacian and nonlinearity taken from the selected primary theorem.
- Initial data in the scaling-critical space specified by that theorem.
- Local existence, uniqueness in the stated solution class, and continuous dependence where the
  source theorem states them.
- Maximal lifespan, continuation/blow-up alternative, small-data global existence, or scattering
  only if they belong to the exact selected theorem rather than a neighboring result.

## Decisions required before statement freeze

The statement phase must inspect a stable primary-source copy and fix the equation, spatial
dimension, nonlinearity and exponent range, critical regularity/index, real or complex scalar
field, time interval convention, mild/Duhamel solution definition, all auxiliary spacetime norms,
and every endpoint or smallness restriction. It must distinguish homogeneous from inhomogeneous
Sobolev spaces and determine whether uniqueness is conditional on an auxiliary Strichartz class.
Degenerate data, zero lifespan, focusing/defocusing signs, and endpoint exclusions must be mapped
explicitly. Binder order and universes must follow these choices.

## Explicit exclusions

- A generic Banach fixed-point theorem or linear Schrodinger estimate as a substitute for NLS
  well-posedness.
- A subcritical Sobolev theorem substituted for the source's scaling-critical result.
- Global existence or scattering inferred from local existence without the source hypotheses.
- An abstract structure that assumes existence, uniqueness, or the Duhamel identity as fields.
- Neighboring results by Cazenave and Weissler for a different nonlinearity, space, or exponent.

The subsequent formal statement must expose the concrete evolution equation, solution notion,
critical data space, and quantifiers, or record a precise mathlib API blocker.
