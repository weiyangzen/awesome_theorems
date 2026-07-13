# Scope map

## Received claim

The repository names `THM-M-0487` as `弱哥德巴赫猜想` and states
`大于5的奇数可表为三素数之和`: every odd number greater than five can be represented as
a sum of three primes. This is the modern weak, ternary, or three-primes Goldbach theorem.

## Candidate mathematical boundary

The received family has:

- every odd integer `n` satisfying the strict lower bound `n > 5`;
- three positive prime summands;
- exact additive equality with `n`;
- no requirement that the three primes be distinct or ordered; and
- an unconditional conclusion for every qualifying input, not merely sufficiently large inputs.

For Lean, the natural-number encoding is canonical because `n > 5` makes every source-admissible
integer positive, and positive integers correspond uniquely to naturals. `Statement.lean` freezes
three independent `Nat` witnesses with `Nat.Prime` predicates and equality `n = p + q + r`.

## Boundary cases to freeze

1. The threshold is strict: `n = 5` is excluded, while `n = 7` is included.
2. The included boundary `7 = 2 + 2 + 3` requires repeated primes and permits the even prime `2`.
3. Even inputs are outside the implication even when greater than five.
4. Prime means a positive natural prime, excluding `0`, `1`, negative integers, prime powers, and
   almost-primes.
5. The summands need not be pairwise distinct, odd, increasing, or canonically ordered.
6. Equality orientation is frozen; the reversed orientation has a checked `Iff` transport. Addition
   uses Lean's left-associated `p + q + r` syntax.
7. The source's integer domain is restricted to naturals using the source premise `n > 5`; no
   negative or zero input satisfies that premise.

## Source and proof boundary

Helfgott's inspected Main Theorem matches the received sentence, but its proof has two material
parts: an analytic proof for odd inputs at least `10^27`, and the Helfgott-Platt finite verification
covering the remaining range. A later source audit must inspect and admit the main paper, its
major-arc and minor-arc dependencies, the computational paper and artifacts, all assumptions and
errata, and obtain independent review. Historical origin in the Goldbach-Euler correspondence is
not proof authorship.

## Explicit exclusions

- Binary or strong Goldbach: every even integer greater than two is a sum of two primes.
- `THM-M-0508`, Vinogradov's weaker eventual theorem for sufficiently large odd inputs.
- An almost-all, density, bounded-exception, or fixed-cutoff theorem.
- A sum of prime powers, almost-primes, signed primes, or any number other than exactly three primes.
- A strengthened root requiring distinct summands or three odd summands; both reject the `n = 7`
  boundary of the received claim.
- A finite computation alone, without the analytic proof above its verified range.
- A predicate, structure, hypothesis, custom axiom, oracle, or unchecked certificate that assumes
  the requested representation.
- The catalog's `已验证` label, a theorem name, or successful API elaboration as proof evidence.

The canonical Lean expression and fingerprint are recorded in `statement.json`. This statement
freeze supplies no proof or source-review credit.
