# Scope map

## Included claim

- The beta-2 random-matrix edge law for a sequence of complex Hermitian GUE matrices.
- The GUE density proportional to `exp(-(N/2) Tr(H^2))`, giving limiting spectral edge `2`, and
  the scaled variable `N^(2/3) (lambda_max - 2)`. Source audit must verify these conventions.
- Convergence in distribution of the scaled largest eigenvalue to a probability distribution
  function `F_2`.
- Identification of `F_2(s)` with the Fredholm determinant `det(I - K_Ai)` on `L2(s, infinity)`,
  where the Airy kernel and determinant are concretely defined.

The determinant identification belongs to the target because otherwise "the Tracy-Widom law" is
only an opaque name. A later obligation tree may separate convergence from the analytic
identification, but checked composition must reconnect both to this root scope.

## Statement-phase decisions

The statement phase must freeze the GUE probability density or entrywise law, matrix indexing,
Hermitian eigenvalue ordering, the exact edge/scaling constant, and the definition of convergence
in distribution. It must also decide whether `F_2` is introduced through the Airy-kernel determinant
or an equivalent Painleve II expression. Any alternate encoding needs a checked relationship, not
a prose assertion.

The Lean target must expose real thresholds, probability measures, measurability, the limit as
`N -> infinity`, the Airy function/kernel, the operator space, trace-class condition, and Fredholm
determinant. If pinned mathlib lacks any interface, the statement phase must record the precise API
blocker rather than replacing the theorem by an abstract structure that assumes the conclusion.

## Explicit exclusions

- GOE/beta-1 and GSE/beta-4 variants.
- Universality for arbitrary Wigner, covariance, or beta ensembles.
- Baik-Deift-Johansson, KPZ, longest-increasing-subsequence, or stochastic-Airy-operator results.
- A finite-dimensional numerical approximation, simulation, moment computation, or histogram.
- A theorem saying a distribution exists without proving it is the scaled GUE edge limit.
- An abstract package containing convergence or the determinant identity as a field.
- The repository source label `verified`, which is untrusted metadata and grants no proof credit.

## Boundary cases

Matrix size zero is excluded. Positive sizes are required, but the limit is asymptotic, so no
single finite size establishes the result. Different GUE normalizations are admissible only through
an explicit normalization choice and checked scaling transport. Thresholds range over all real
numbers; tails at infinity may be derived but cannot replace pointwise convergence at finite `s`.
