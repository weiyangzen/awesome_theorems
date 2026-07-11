# Scope map

## Candidate included root

- For each natural number `n`, use the finite symmetric group `S_n`.
- Work over the complex numbers and with finite-dimensional representations.
- Restrict the codomain to isomorphism classes of irreducible representations.
- Index those classes by integer partitions of `n`.
- Require a bijection/classification, not merely equality of cardinalities.

These choices capture the conventional partition classification suggested by
the legacy discovery artifact. They are frozen as the intake candidate so that
later work cannot silently broaden it, but they are not source-certified.

## Boundary cases and encoding decisions

- `n = 0` and `n = 1` are included unless the primary source explicitly uses a
  different convention; transports must cover any convention mismatch.
- The exact model `Equiv.Perm (Fin n)`, the category of representations, the
  finite-dimensional condition, and the quotient by representation
  isomorphism remain statement-phase decisions.
- The eventual classification should identify the Specht-module construction
  (or a source-equivalent construction), prove irreducibility, pairwise
  non-isomorphism, and exhaustiveness.
- The ordered binders, universe levels, minimal imports, environment
  fingerprint, and classical/choice profile remain open.

## Explicit exclusions

- Burnside's `p^a q^b` solvability theorem and Burnside's lemma/orbit-counting
  lemma.
- Young's rule, the branching rule, Young's orthogonal form, or the
  hook-length formula when offered alone.
- Representations over positive-characteristic fields, real representations,
  projective representations, and alternating-group classification.
- A cardinality-only statement or a statement merely asserting that partitions
  and irreducibles are finite.
- The legacy `S1_M_050.lean` statement shape as accepted rev-5.6 evidence.

The exclusions are necessary because the repository label is ambiguous and a
nearby Burnside or Young theorem must not be substituted for the intended root.
