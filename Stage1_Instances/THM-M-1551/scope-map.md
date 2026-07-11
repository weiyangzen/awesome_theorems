# Scope map

## Included claim family

- An explicitly selected auxiliary linear system in two evolution variables.
- Matrix- or Lie-algebra-valued connection coefficients with domains and differentiability fixed.
- Equality of mixed evolutions expressed as the zero-curvature equation, with the sign convention
  derived from the selected ordering of the auxiliary equations.
- A spectral parameter only if, and with exactly the quantification and domain that, the source uses.
- The concrete nonlinear integrable equation only through a proved coefficient comparison or other
  source-prescribed equivalence; it is not inferred from the phrase "integrable system."

## Decisions reserved for statement freeze

The statement phase must select one exact source theorem and freeze: the underlying equation, base
field, matrix size or Lie algebra, independent-variable domain, regularity, derivative convention,
operator ordering, commutator sign, spectral-parameter domain, and whether compatibility is claimed
pointwise, formally, or as an operator identity. It must also cover degenerate constant potentials
and boundary values where the source does.

## Explicit exclusions

- Defining `ZeroCurvature` to be the desired equality and proving it by unfolding.
- A generic implication from an equality algebraically rearranged to flatness as a substitute for a
  concrete source theorem.
- Claims that flatness alone proves inverse scattering, global solvability, conserved quantities,
  or integrability in every accepted sense.
- Variable gauge covariance, principal-bundle curvature, monodromy, or analytic PDE results unless
  they occur in the frozen source statement.

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_210.lean` supplies a useful abstract vocabulary but
is legacy discovery evidence only and receives no rev-5.6 proof credit.
