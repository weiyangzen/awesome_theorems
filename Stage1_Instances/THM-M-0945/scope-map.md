# Scope map

## Preserved theorem family

The repository fixes target `THM-M-0945`, the name Green-Tao theorem, the attribution Ben Green and
Terence Tao, the year 2004, and the slogan "the primes contain arbitrarily long arithmetic
progressions." Green and Tao's matching Theorem 1.1 states that the prime numbers contain
infinitely many arithmetic progressions of length `k` for all `k`.

This intake preserves that theorem family but does not yet freeze a binder-complete proposition.
The paper's Theorem 1.2 is a stronger relative-density result and is not silently substituted for
the catalog root.

## Proposition-changing decisions

The statement phase must freeze the following from a lawfully preserved, independently reviewed
source passage and explicit mathematical conventions:

1. The domain of the length binder `k`: positive naturals, all naturals with trivial small cases,
   or a lower-bounded domain such as `k >= 1` or `k >= 2`.
2. The carrier of primes: prime natural numbers, positive integers, or positive prime integers,
   together with every checked transport between representations.
3. The arithmetic-progression witnesses, normally a starting value `a` and common difference `d`,
   and the index convention `0 <= i < k` versus `1 <= i <= k`.
4. Nondegeneracy: `d > 0` in naturals or integers, rather than allowing the constant progression
   with `d = 0`; also the sign convention if integer differences are used. The paper's proof of
   Theorem 1.1 explicitly discards the degenerate `r = 0` case, supporting this boundary.
5. Whether the root directly says that at least one progression exists for every length, says
   infinitely many exist for every length, or records both with a checked implication.
6. Ordered binders and witness dependence: `forall k, exists a d` rather than one progression or
   one difference serving all lengths.
7. Whether all terms must be pairwise distinct or whether positivity of `d` supplies that fact;
   whether ordering of terms is part of the target or a derived lemma.
8. The cases `k = 0`, `k = 1`, and `k = 2`, overflow-free natural arithmetic, finite index
   coercions, and any requirement that the first term itself be positive.

These choices yield different Lean expressions. This list is a resolution ledger, not a theorem.

## Candidate encodings not credited

- For every positive natural `k`, there are natural numbers `a` and `d > 0` such that every
  `a + i * d` with `i < k` is prime.
- For every positive natural `k`, the set of pairs `(a, d)` producing a `k`-term prime progression
  with `d > 0` is infinite.
- For every `k >= 1`, there exist strictly increasing primes `p_0, ..., p_(k-1)` with constant
  consecutive difference.
- A checked transport from the source's infinite-many wording to a weaker existence-only catalog
  reading.

No candidate is canonical, asserted, or credited at intake.

## Explicit exclusions and neighbors

Dirichlet's theorem on infinitely many primes in one residue class is not a long finite progression
of primes. `THM-M-0947` Roth and pinned `roth_3ap_theorem_nat` concern length three, while
`THM-M-0948` Szemeredi concerns positive-density ambient sets. `THM-M-0946` Green-Tao-Ziegler is a
distinct linear-equations result. Green and Tao Theorem 1.2, density-in-the-primes variants,
polynomial progressions, multidimensional patterns, quantitative counts, and bounded-length
computations do not replace Theorem 1.1 without checked relationships.

A predicate, structure field, hypothesis, axiom, oracle, or unchecked certificate containing the
desired progression cannot prove the target. The catalog's `verified` label, the paper title, a
URL, or the discovery probe supplies no proof credit.

## Boundary cases and formal boundary

The eventual source-to-Lean decision must explicitly resolve progression lengths zero through two,
zero common difference, the prime `2`, starting value zero or one, natural versus integer
subtraction/sign conventions, and indexing endpoints. Intake excludes no case before a proposition
is selected.

Pinned mathlib supplies `Nat.Prime`, infinitude of primes, a predicate for three-term-progression-
free sets, Roth's three-term theorem, and a finite-color homothetic-copy theorem. These APIs
elaborate but do not state the arbitrary-length prime-progression root. Exact imports, expression
identity, statement mutations, candidate provenance, and proof closure belong to later phases.
