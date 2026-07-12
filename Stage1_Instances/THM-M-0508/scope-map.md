# Scope map

## Included theorem family

- One uniform threshold beyond which the assertion holds for every odd input.
- An additive representation `n = p + q + r` by three natural primes.
- Unconditional existence, not a density-one or almost-all assertion.
- Repeated primes provisionally allowed, subject to confirmation by the pinpoint source.
- A checked equivalence between explicit-threshold and `Filter.Eventually` encodings if both are
  advertised.

## Statement decisions still open

The statement phase must inspect an immutable source and freeze:

1. the exact source theorem or displayed formula and its surrounding hypotheses;
2. whether inputs and summands are naturals, positive integers, or another stated domain;
3. whether "sufficiently large" is encoded by an existential threshold or an eventual filter;
4. whether equality is literal, whether summands may repeat, and whether ordered triples matter;
5. whether Vinogradov's source claim is an asymptotic representation-count formula from which the
   existence statement follows, or directly the existence corollary;
6. all endpoint conventions and the relationship to the later all-odd-integers theorem.

## Explicit exclusions

- The modern weak Goldbach theorem that every odd integer greater than five is a sum of three
  primes; it is stronger and separately listed as `THM-M-0487`.
- An almost-all-odd-integers result, a positive-density result, or a bounded exceptional set.
- A sum involving almost-primes, prime powers, signed primes, or fewer/more than three primes.
- A mere asymptotic count without a checked implication to the root existence statement.
- A finite computation up to a chosen cutoff as proof of the eventual analytic assertion.
- The repository label `已验证` as source, formalization, or proof evidence.

No canonical Lean target is frozen at intake. The API probe establishes only that the elementary
statement vocabulary exists in the pinned environment.
