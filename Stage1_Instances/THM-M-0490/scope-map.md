# Scope map

## Preserved theorem family

The intended root family is Zhang's published bounded-gap consequence for **consecutive** primes:
if `p_n` is the nth prime, then

```text
lim inf as n tends to infinity of (p_(n+1) - p_n) < 70,000,000.
```

This is stronger and more precise than the repository gloss "there are infinitely many pairs of
primes whose difference is less than seventy million." The paper uses a strict `<` bound and the
successive terms of the increasing prime sequence. Neither arbitrary unordered pairs nor a
non-strict `<=` bound may replace it.

## Candidate Lean shape, not yet canonical

Pinned mathlib zero-indexes the increasing prime enumeration as `Nat.nth Nat.Prime n`. A direct
discrete candidate for the source consequence is:

```lean
forall N : Nat, exists n : Nat,
  N <= n and Nat.nth Nat.Prime (n + 1) - Nat.nth Nat.Prime n < 70000000
```

This candidate has no hypotheses. Natural subtraction is well behaved because
`Nat.nth_strictMono Nat.infinite_setOf_prime` proves the next prime is larger. It is not frozen as
the canonical expression at intake: the statement phase must check its relationship to the
paper's liminf over the positive integer index convention and decide whether an `atTop` frequent
predicate or another exact encoding better preserves the source.

## Decisions required at statement freeze

1. Obtain independent review of the primary source's abstract, Theorem 1, definitions, proof
   boundary, publication history, and any correction or erratum.
2. Freeze zero- versus one-indexing and a checked correspondence with the source's `p_n`.
3. Freeze the infinitude encoding: an eventually-unbounded witness formula, `Frequently atTop`,
   or a literal real `liminf`, and kernel-check every credited transport.
4. Freeze natural versus integer or real gaps, coercions, and subtraction semantics.
5. Preserve strict `< 70,000,000`; reject `<=`, a different bound, or a finite cutoff.
6. Resolve whether the root is only the bounded-gap consequence or the stronger admissible-tuple
   assertion. This intake preserves the consequence and treats Theorem 1 as its proof source.
7. Mutation-test removed/changed semantic requirements, the prime domain, binder scope, and
   boundary indices before any proof evidence is inspected.

## Source theorem versus root

Theorem 1 in Zhang's paper assumes an admissible set `H = {h_1, ..., h_k0}` of distinct
nonnegative integers with `k0 >= 3.5 * 10^6` and proves that infinitely many positive integers `n`
make at least two of the `n + h_i` prime. It then derives the displayed consecutive-prime bound.
The admissible-tuple theorem is a critical future obligation and source node, but installing it as
the root would broaden the repository target.

## Neighbor and substitution boundaries

- `THM-M-0489`, the twin-prime conjecture, asks for gap exactly two and remains a different target.
- `THM-M-0491`, Maynard's theorem, records later bounded-gap improvements and cannot replace the
  historical seventy-million result or its proof provenance.
- `THM-M-0492`, Polignac's conjecture, concerns every positive even gap and is not this theorem.
- Euclid's infinitude of primes, prime-counting asymptotics, and arbitrary pairs of primes are
  insufficient. A pair may be nonconsecutive, repeated, unordered, or drawn from a bounded set.
- A structure, premise, custom axiom, oracle, generated certificate, or unchecked external result
  containing the desired bounded-gap conclusion receives no credit.

## Formal boundary

`IntakeProbe.lean` checks `Nat.nth`, `Nat.Prime`, `Nat.infinite_setOf_prime`,
`Nat.prime_nth_prime`, and `Nat.nth_strictMono`, then elaborates the prospective discrete type and
the adjacent-prime ordering fact. It does not freeze the root, prove a bounded gap, inspect a
terminal proof body, or establish absence outside the bounded search. There is no expression hash,
checked source transport, obligation registry, or machine-proof claim at intake.
