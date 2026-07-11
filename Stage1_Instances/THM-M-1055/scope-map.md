# Scope map

## Included claim

- A probability space `(Ω, Σ, μ)` and a measurable, measure-preserving self-map `T : Ω → Ω`.
- Ergodicity of `T` with respect to `μ`.
- A real-valued `μ`-integrable observable `f`.
- Almost-everywhere convergence of `n⁻¹ ∑ k < n, f (T^[k] x)` to `∫ x, f x ∂μ` as positive
  natural `n` tends to infinity.

## Boundary decisions for the statement phase

The primary-source inspection must fix the precise measurability/completeness assumptions, the
definition of measure preservation and ergodicity, whether averages are indexed by `n` or `n+1`,
and the treatment of `n = 0`. The Lean target must explicitly type iteration, finite sums, division,
the almost-everywhere quantifier, and the topology of real convergence. It must also check empty or
degenerate probability spaces and equality only up to almost-everywhere equivalence.

## Explicit exclusions

- The mean ergodic theorem (norm convergence) or only an `L2` specialization.
- Kingman's subadditive theorem, a finite-state theorem, or a uniquely ergodic topological result.
- The non-ergodic conclusion alone unless the ergodic specialization to the space mean is checked.
- An abstract structure that assumes the limit, invariance, or convergence as fields.
- Birkhoff-sum definitions and adjacent mathlib lemmas as terminal proof credit.

The later statement may use a checked equivalent formulation, but every transport to this scoped
claim must be explicit and kernel checked.
