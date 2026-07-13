# Scope map

## Preserved theorem family

The intake preserves the family identified by the catalog title, attribution, date, and gloss:
Maynard's 2013 work on improved upper bounds for small gaps and bounded clusters of primes. It does
not select one formula from that family by memory.

The strongest contextual candidate is Theorem 1.3 of the published paper,
`liminf (p_(n+1) - p_n) <= 600`, because the introduction explicitly contrasts it with Zhang's
70,000,000 bound and a later 4,680 bound. The broader Theorem 1.1, the tuple-density Theorem 1.2,
and the conditional Theorem 1.4 are nevertheless also compatible with the catalog's vague words.
Candidate priority is not canonical-statement selection.

## Decisions required at statement freeze

An approved source-reviewed statement must decide all of the following:

1. Which source result is the root: published Theorem 1.1, 1.2, 1.3, 1.4, the sieve engine in
   Propositions 4.2-4.3, or another explicitly justified result.
2. Whether the gap is adjacent `p_(n+1) - p_n`, an `m`-step span `p_(n+m) - p_n`, a bounded
   interval containing a fixed number of primes, or a tuple property.
3. The exact quantifiers over `m`, `n`, constants, admissible sets, and sufficiently large
   parameters, including the indexing convention for the first prime.
4. How `liminf` is encoded, including the codomain, extended-value conventions, and a checked
   transport to an "infinitely many indices" formulation if that alternate form is credited.
5. For Theorem 1.1, the precise meaning of Vinogradov notation, positivity and independence of the
   implied absolute constant, the source convention `N = {1, 2, ...}`, and whether an explicit
   existential constant with binder order `exists C, forall m >= 1` is the canonical encoding.
6. For Theorem 1.2, the representations of finite sets and subsets, distinctness, cardinality,
   positivity of the denominator, the meanings of "sufficiently large depending on m" and
   `gg_m 1`, and the simultaneous-primality infinitude predicate.
7. For Theorem 1.3, whether `<= 600` is represented directly as a liminf statement or as infinitely
   many adjacent prime gaps at most 600, with the equivalence checked rather than assumed.
8. For Theorem 1.4 or Proposition 4.2, the paper's exact level-of-distribution definition,
   Elliott-Halberstam premise, admissibility predicate, variational `M_k`, ceiling convention, and
   every analytic side condition.
9. Every ordered binder, universe, coercion, hypothesis, conclusion, alternate encoding,
   foundation choice, source correction, and exceptional case.

If Theorem 1.1 or 1.3 is selected, its root remains unconditional. Bombieri-Vinogradov and the
sieve criterion are proof dependencies, not hypotheses that may be added to make the root easier.
A conditional bridge can close only its own explicitly typed child obligation.

These choices change the proposition or proof boundary. Intake leaves them open.

## Boundary cases to resolve

- `m = 0` if Lean's `Nat` is used, versus the source's intended positive-integer convention;
- `n = 0` versus the source's one-based `p_1 = 2`, Lean's zero-based nth-prime API, and the checked
  translation between those indexing conventions;
- subtraction on naturals versus integers or reals, and why consecutive nth primes make truncation
  harmless in a chosen encoding;
- empty and singleton finite sets, repeated offsets, negative offsets, and `r < m` for tuple forms;
- zero or negative implied constants and the exact dependency of all asymptotic constants;
- finite prefixes, equality at 600, infinite liminf, and the difference between infinitely often,
  eventually, and universally bounded gaps; and
- the off-by-one distinction between an `m`-step span `p_(n+m)-p_n` (which contains `m+1` listed
  primes) and an interval claimed to contain at least `m` primes; and
- conditional hypotheses being absent, explicit, or accidentally incorporated into a definition.

## Excluded substitutions

- Zhang's separately scheduled 70,000,000 theorem (`THM-M-0490`) is not this target.
- The twin-prime, prime-tuples, and Polignac conjectures are stronger open statements and cannot
  replace Maynard's bounded-gap or bounded-cluster conclusions.
- Bertrand's postulate, Euclid's infinitude of primes, a prime-counting upper bound, or the prime
  number theorem does not establish a fixed recurrent prime-gap bound.
- A statement saying some two primes differ by at most 600 is vastly weaker than an infinite
  subsequence or liminf conclusion.
- A statement saying every or eventually every adjacent prime gap is at most 600 is much stronger
  than Maynard's Theorem 1.3 and is not licensed by the source.
- The conditional 12 bound cannot be presented as unconditional, and the unconditional 600 bound
  cannot silently inherit Elliott-Halberstam as an assumption.
- A structure, hypothesis, axiom, or function field containing the desired prime-gap conclusion
  supplies no proof.
- Generic Selberg-sieve, nth-prime, prime-counting, or von Mangoldt APIs are substrate, not the root.
- A theorem name, search result, numerical computation, or the catalog's `已验证` label supplies no
  human or machine proof credit.

## Neighbor boundaries

`THM-M-0488` (Hardy-Littlewood conjecture), `THM-M-0489` (twin-prime conjecture), `THM-M-0490`
(Zhang's theorem), and `THM-M-0492` (Polignac's conjecture) are distinct catalog records. They may
eventually appear as historical context, dependencies, or consequences only after exact statements
and typed graph edges are frozen. No proof or status is shared by proximity.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe checks the nth-prime function and
primality theorem, prime counting and its divergence, the generic `BoundingSieve`/`SelbergSieve`
interfaces and upper-bound inequality, and von Mangoldt infrastructure. Pinned mathlib also has a
one-dimensional Selberg upper-bound sieve, not Maynard's multidimensional weights or conclusions.
A bounded exact-topic search found no Maynard, small/bounded prime-gap, or matching nth-prime
liminf declaration. This is scoped intake discovery, not an exhaustive external audit or global
absence claim.
