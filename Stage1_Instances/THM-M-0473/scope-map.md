# Scope map

## Received claim

The repository names `THM-M-0473` as `裴蜀定理` and gives the gloss
`ax+by=gcd(a,b)有整数解`: the equation `a*x + b*y = gcd(a,b)` has integer solutions. The target is
the elementary two-integer Bezout identity, not the algebraic-geometry theorem also commonly
called Bezout's theorem.

## Candidate mathematical boundary

The intended family has:

- inputs `a` and `b` in the integers;
- a nonnegative greatest common divisor `gcd(a,b)`, viewed as an integer;
- integer witnesses `x` and `y`; and
- equality `gcd(a,b) = a*x + b*y` (equivalently the displayed sum equals the gcd).

This family includes negative inputs and the `(0,0)` boundary unless a reviewed source explicitly
chooses another convention. Pinned mathlib implements `Int.gcd a b : Nat`, so a Lean encoding must
make the coercion to `Int` explicit. A related natural-input form still has integer coefficient
witnesses; it is not automatically identical to the integer-input form without a checked
transport.

## Decisions required at statement freeze

1. Admit and independently review an immutable primary or authoritative source passage, including
   the definition of gcd, all assumptions, proof boundary, corrections, and errata.
2. Freeze whether the inputs are integers or naturals and whether the coefficient witnesses are
   explicitly integers.
3. Freeze ordered binders, equality orientation, multiplication orientation, and the cast of a
   nonnegative gcd into the integers.
4. Resolve sign conventions and negative inputs, including whether `gcd(a,b)` means
   `gcd(|a|,|b|)` and is always nonnegative.
5. Resolve `(0,0)`, one-zero inputs, equal inputs, coprime inputs, and unit or negative-unit inputs.
6. Supply kernel-checked transports for every credited alternate formulation, then run the four
   rev-5.6 mutation classes before inspecting proof closure.

## Related forms, not substitutes

- `Nat.gcd_eq_gcd_ab` computes integer coefficients for natural inputs. It is a strong candidate
  anchor, but a natural-input root narrows an integer-input reading unless a transport is checked.
- `Int.gcd_eq_gcd_ab` directly covers signed integer inputs and uses mathlib's nonnegative natural
  gcd cast to `Int`.
- `EuclideanDomain.gcd_eq_gcd_ab` generalizes the identity to arbitrary Euclidean domains. That is
  broader than the catalog's elementary integer theorem.
- `IsBezout.exists_gcd_eq_mul_add_mul` states an abstract Bezout-ring result and depends on a
  chosen gcd convention. It is not the received root by name alone.
- The coprime corollary `a*x + b*y = 1` is only the gcd-one specialization, not the full theorem.
- The divisibility characterization of all integer linear combinations is stronger than bare gcd
  representability and requires a checked relationship before credit.

## Explicit exclusions

- Bezout's theorem on intersections of projective algebraic curves.
- Bezout rings/domains, polynomial gcd identities, ideals, or arbitrary Euclidean domains used as
  a substituted root.
- A coprime-only, nonzero-only, positive-input-only, or fixed-number special case.
- Natural coefficient witnesses; negative coefficients are essential in general.
- A structure or hypothesis that already stores the requested witnesses or equality.
- The catalog's `已验证` label, a theorem name, API output, or successful probe as proof evidence.

No canonical Lean expression or expression fingerprint is frozen by this intake. The direct
mathlib declarations are candidate anchors for the dependent statement and anchor-audit phases.
