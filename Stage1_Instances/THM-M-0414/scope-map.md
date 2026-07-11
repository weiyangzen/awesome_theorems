# Scope map

## Included claim

- The ambient ring is a Dedekind domain (commutative, with the exact convention to be reconciled
  against the selected source and mathlib's `IsDedekindDomain`).
- The factored object is a nonzero integral ideal. Proper nonzero ideals have nonempty prime
  support; the unit ideal is retained as the empty-product case.
- Existence means a finite product of nonzero prime ideals.
- Uniqueness is equality of the factor multisets, equivalently equality of every prime valuation,
  and is insensitive to ordering. The unit ideal is the empty product boundary case.

## Statement encoding decision

The canonical target in `Statement.lean` combines the explicit `finprod` over height-one primes
with `UniqueFactorizationMonoid (Ideal R)`. The historical candidate has a checked definitional
identity with this target. An explicit factor-multiset presentation and the fractional-ideal
strengthening remain uncredited alternate encodings until separately bridged.

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
