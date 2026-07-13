# Scope map

## Preserved human claim

For every natural number `n` with `1 < n`, there is a finite nonempty list of prime natural
numbers whose product is `n`; if two lists of prime naturals both have product `n`, they differ
only by permutation.

This is the provisional human statement frozen at intake. It interprets the catalog's Chinese word
`整数` in its explicitly positive range, so the formal carrier can conservatively be `Nat` with
`1 < n`. The dependent statement phase owns selection and elaboration of the exact Lean target.

| Surface | In-scope meaning | Intake boundary |
|---|---|---|
| Number domain | Natural `n` with `1 < n`, representing positive integers greater than one | An `Int` statement needs an explicit positivity, sign, and unit transport before credit |
| Existence | A finite list of primes has product `n` | Mere existence without uniqueness is not the root |
| Uniqueness | Any two prime lists with product `n` are permutation-equivalent | Literal list equality would require a sorting convention and is not silently substituted |
| Repetition | Repeated primes are allowed, so prime powers are included | A squarefree-only formulation is a weakening |
| Exponent form | A finitely supported map from primes to natural exponents reconstructs the number uniquely | Candidate equivalent representation; no checked root transport is credited at intake |
| Formal foundation | Lean 4 and manifest-pinned mathlib | Exact imports, expression fingerprint, terminal body, axioms, and TCB closure remain downstream |

## Boundary cases

- `n = 2` and every prime `n` must yield a one-element factor list.
- Prime powers such as `8 = 2 * 2 * 2` test repeated factors and exponent multiplicity.
- Products with distinct factors test invariance under reordering.
- `n = 0` and `n = 1` are outside the literal `n > 1` root. Their empty-list behavior in one
  library representation must not broaden the theorem.
- Negative integers are outside this positive target. A later integer encoding must state how the
  unit `-1` and factor signs are normalized.

The statement phase must mutation-test at least removal of `1 < n`, a `Nat`-to-`Int` domain
change, altered binder scope, and the `n = 2` boundary before any proof candidate is credited.

## Alternate encodings and exclusions

The canonical sorted list `Nat.primeFactorsList`, uniqueness of arbitrary prime lists up to
`List.Perm`, the multiplicity function `Nat.factorization`, and the positive-natural equivalence
`Nat.factorizationEquiv` are related encodings. Intake does not declare them definitionally or
propositionally identical to a yet-unselected root.

The following are not substitutes for this target:

- existence of a prime divisor or factorization existence alone;
- uniqueness or injectivity alone without reconstruction/existence;
- Euclid's lemma that a prime dividing a product divides a factor;
- a theorem only for primes, prime powers, squarefree numbers, or concrete numerals;
- unique factorization for arbitrary integers, Gaussian integers, polynomials, ideals, UFDs, or
  other rings; and
- a declaration name, catalog `verified` label, or successful API probe treated as proof closure.

## Downstream work

`STATEMENT` must choose an exact list/permutation or exponent-map proposition, minimize its pinned
imports, serialize its elaborated expression and environment, check all credited representation
transports, and run the required mutations. Formal-candidate provenance, obligation architecture,
proof integration, trust validation, readable reconstruction, and release remain later nodes.
