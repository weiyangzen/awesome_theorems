# Scope map

## Included claim

- The ambient ring is a Dedekind domain (commutative, with the exact convention to be reconciled
  against the selected source and mathlib's `IsDedekindDomain`).
- The factored object is a nonzero proper integral ideal.
- Existence means a finite product of nonzero prime ideals.
- Uniqueness is equality of the factor multisets, equivalently equality of every prime valuation,
  and is insensitive to ordering. The unit ideal is the empty product boundary case.

## Encoding decision deferred to statement phase

The classical source formulation may be represented in Lean by explicit finitely supported
exponents, an explicit `finprod` over height-one primes, or the
`UniqueFactorizationMonoid (Ideal R)` instance. These are not definitionally the same statement.
The statement phase must select one canonical expression and provide checked transports for any
other presentation rather than silently broadening the theorem.

## Boundaries and exclusions

- Zero ideals are excluded from factorization; the field/zero-dimensional convention must be
  mutation-tested rather than inferred from the title.
- Fractional ideals and their integer exponents are a strengthening, not part of this root claim.
- Principal-ideal factorization, element factorization, class-group consequences, and number-ring
  specializations do not substitute for the general theorem.
- The legacy `S1_M_069.lean` wrapper and the untrusted `已验证` metadata label are discovery only.
- No abstract assumption of the desired factorization or uniqueness may be used to restate the
  conclusion tautologically.

Later phases must freeze universes, ring hypotheses, ideal nonzeroness/properness, empty-product
behavior, exact imports, environment fingerprint, source definitions, and hypothesis mutations.
