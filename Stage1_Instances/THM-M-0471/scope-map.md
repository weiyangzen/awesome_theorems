# Scope map

## Preserved human claim

For every natural number `n` with `1 < n`, there is a finite nonempty list of prime natural
numbers whose product is `n`; if two lists of prime naturals both have product `n`, they differ
only by permutation.

This is the human statement frozen at intake. It interprets the catalog's Chinese word `整数` in
its explicitly positive range, so the formal carrier is conservatively `Nat` with `1 < n`.
`Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget` is now the exact elaborated Lean
target, pending master acceptance of the statement-phase receipt.

| Surface | In-scope meaning | Intake boundary |
|---|---|---|
| Number domain | Natural `n` with `1 < n`, representing positive integers greater than one | An `Int` statement needs an explicit positivity, sign, and unit transport before credit |
| Existence | A finite list of primes has product `n` | Mere existence without uniqueness is not the root |
| Uniqueness | Any two prime lists with product `n` are permutation-equivalent | Literal list equality would require a sorting convention and is not silently substituted |
| Repetition | Repeated primes are allowed, so prime powers are included | A squarefree-only formulation is a weakening |
| Exponent form | A finitely supported map from primes to natural exponents reconstructs the number uniquely | Candidate equivalent representation; no checked root transport is credited at intake |
| Formal foundation | Lean 4 and manifest-pinned mathlib | Exact statement import/expression fingerprint is recorded; terminal body, provenance, and full TCB closure remain downstream |

## Boundary cases

- `n = 2` and every prime `n` must yield a one-element factor list.
- Prime powers such as `8 = 2 * 2 * 2` test repeated factors and exponent multiplicity.
- Products with distinct factors test invariance under reordering.
- `n = 0` and `n = 1` are outside the literal `n > 1` root. Their empty-list behavior in one
  library representation must not broaden the theorem.
- Negative integers are outside this positive target. A later integer encoding must state how the
  unit `-1` and factor signs are normalized.

The statement phase mutation suite distinguishes removal of `1 < n`, a `Nat`-to-`Int` domain
change, moving the factor-list existential outside the `n` binder, and replacing `1 < n` by
`2 < n`. The boundary witness separately checks `1 < (2 : Nat)`. None supplies proof credit.

## Alternate encodings and exclusions

The selected root uses arbitrary prime lists and uniqueness up to `List.Perm`. The canonical sorted
list `Nat.primeFactorsList`, the multiplicity function `Nat.factorization`, and the positive-natural
equivalence `Nat.factorizationEquiv` are related encodings, but no checked transport from those
representations to the selected root is credited by the statement phase.

The following are not substitutes for this target:

- existence of a prime divisor or factorization existence alone;
- uniqueness or injectivity alone without reconstruction/existence;
- Euclid's lemma that a prime dividing a product divides a factor;
- a theorem only for primes, prime powers, squarefree numbers, or concrete numerals;
- unique factorization for arbitrary integers, Gaussian integers, polynomials, ideals, UFDs, or
  other rings; and
- a declaration name, catalog `verified` label, or successful API probe treated as proof closure.

## Downstream work

`STATEMENT` has selected the list/permutation proposition, minimized its pinned import, serialized
its elaborated expression and environment, checked the credited direct expansion, and run the
required mutations. Master acceptance of that provisional work remains pending. Formal-candidate
provenance, obligation architecture, proof integration, trust validation, readable reconstruction,
and release remain later nodes.
