# Scope map

## Included root

- `alpha` is an irrational real number algebraic over the rationals.
- `epsilon` is real and strictly positive, so the approximation exponent is strictly above two.
- Approximants are rational numbers, measured using their positive reduced denominators.
- The set satisfying the strict inequality `|alpha - x| < den(x)^(-(2 + epsilon))` is finite.

## Statement-phase decisions

- Select and inspect the exact mathlib algebraicity and irrationality predicates.
- Select a representation of reduced denominator and prove any transport from coprime integer pairs.
- Choose a type-correct encoding of real exponentiation and of the finite exceptional set.
- Freeze binder order, imports, toolchain, foundation profile, and normalized expression fingerprint.
- Mutation-test algebraicity, irrationality, positivity, strictness, denominator normalization, and the
  excluded `epsilon = 0` boundary.

## Explicit exclusions

- Roth's theorem on three-term arithmetic progressions (`THM-M-0947`).
- Schmidt's Subspace Theorem or simultaneous approximation as a substitute root.
- Liouville's weaker degree-dependent exponent, effective bounds, and number-field generalizations.
- A statement merely about infinitely many integer pairs without quotienting duplicate rational
  representations, unless a checked equivalence to the rational formulation is supplied.
- Any legacy file or the neighboring `THM-M-0398` dossier as accepted rev-5.6 evidence.

These boundaries prevent a namesake combinatorics theorem, a weaker approximation theorem, or a
duplicate metadata record from silently replacing this target.
