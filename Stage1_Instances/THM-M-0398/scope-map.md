# Scope map

## Included root claim

- Domain: `alpha` is a real algebraic number and is irrational.
- Quantifier: every real `epsilon > 0`.
- Approximants: rational values represented mathematically as `p/q`, with integer `p`, positive integer `q`; normalization to reduced fractions is not yet selected.
- Conclusion: the approximants satisfying `|alpha - p/q| < q^(-(2 + epsilon))` form a finite set (equivalently, only finitely many solutions occur).
- Degenerate boundaries: `epsilon = 0` is excluded; `q = 0` is excluded; rational `alpha` is excluded. Duplicate integer pairs representing one rational must not spuriously change the finite-rational conclusion.

## Encoding decisions left to the statement node

- Choose the exact mathlib predicate for algebraicity over `ℚ` and checked coercions into `ℝ`.
- Decide whether the canonical object is a finite set of rationals bounded by denominator/height or a finite set of coprime integer pairs.
- Prove transports between the selected height/denominator formulation and the displayed `p/q` formulation.
- Freeze ordered Lean binders, universes, imports, foundation profile, and environment fingerprint.
- Mutation-test irrationality, algebraicity, positivity of `epsilon`, positivity of the denominator, and strictness of the exponent bound.

## Explicit exclusions

- Roth's theorem for three-term arithmetic progressions.
- Schmidt's Subspace Theorem and simultaneous approximation as substitute roots.
- Liouville's weaker algebraic-degree exponent bound.
- Effective bounds, number-field generalizations, and approximation by algebraic numbers of bounded degree.
- Any legacy `S1_M_011.lean` declaration as accepted rev-5.6 evidence; it is discovery input only.

The exclusions prevent a nearby theorem, special case, or stronger named family from silently replacing the root.
