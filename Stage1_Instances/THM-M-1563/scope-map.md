# Scope map

## Repository scope

The target is the Kardar-Parisi-Zhang (KPZ) stochastic growth equation introduced by Mehran
Kardar, Giorgio Parisi, and Yi-Cheng Zhang in 1986. The repository gloss is only "random surface
growth". That identifies a subject and an equation family, not a proposition with a truth value.
This intake therefore freezes the subject boundary but does not invent a theorem.

A familiar continuum notation is

```text
partial_t h = nu Delta h + (lambda / 2) |grad h|^2 + eta,
```

where `eta` is noise. This display is a discovery description only. Its domain, dimension,
coefficients, noise covariance, initial/boundary data, renormalization, and interpretation have not
been selected as the canonical statement.

## Decisions required by the statement phase

- Select one exact mathematical theorem, not merely the SPDE definition, from an immutable primary
  source with theorem/page and errata review.
- Freeze spatial dimension, time interval, spatial domain, boundary conditions, coefficient signs
  and nondegeneracy, probability space, filtration, and noise law/covariance.
- Freeze initial-data regularity and the solution notion: classical, mild, energy, Cole-Hopf, or a
  renormalized/distributional formulation.
- State the exact conclusion, such as existence, uniqueness, regularity, approximation convergence,
  invariant measure, or another source-selected result, with all quantifiers and exceptional sets.
- Separate the one-dimensional classical/Cole-Hopf theory from higher-dimensional singular models,
  and record every renormalization constant and convention that affects the proposition.
- Specify degenerate cases including `lambda = 0`, zero noise, zero viscosity, empty/zero time,
  smooth rather than white noise, and domain boundaries.

These are mathematical choices, not interchangeable encoding details. Until they are sourced, the
ordered binders, universes, hypotheses, conclusion, alternate encodings, and foundation profile are
open.

## Explicit exclusions

- The bare definition or physical derivation of the KPZ equation as a theorem.
- KPZ universality, fluctuation exponents, Tracy-Widom laws, directed polymers, stochastic Burgers,
  or regularity structures as substitutes without a checked equivalence to the selected claim.
- A deterministic heat equation, a smooth-noise toy problem, or a finite-dimensional discretization
  silently substituted for the singular stochastic equation.
- An abstract Lean structure that takes existence, uniqueness, or convergence as a field.
- The metadata value `已验证` as either human-source or kernel evidence.

## Formalization boundary

The later Lean target must expose concrete analytic and probabilistic data rather than package the
desired result as an assumption. Repository and pinned-mathlib discovery is reserved for the anchor
audit after an exact source theorem is selected. Current debt is `[H4, M4, R4]`.
