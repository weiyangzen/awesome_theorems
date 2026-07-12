# Scope map

## Provisional included claim

- Natural-number additive representation of sufficiently large even integers.
- One summand is prime.
- The other summand is a positive `P_2` (almost-prime) number: provisionally, its total number of
  prime factors counted with multiplicity is at most two.
- An existential threshold followed by a universal statement for even numbers above it.

## Decisions required at statement freeze

The primary source must determine whether `P_2` means exactly two prime factors or at most two,
whether multiplicity is counted, whether a prime is admitted, and whether the second summand may be
a prime square. It must also fix the integer/natural domain, positivity, the threshold formulation,
the ordering of the two summands, and the treatment of zero, one, and small even numbers.

For Lean, the statement phase must choose between a factorization-support sum, an existential
product of at most two primes, or another definition and prove any credited transports. It must not
hide the theorem inside an assumed `IsChenNumber` predicate or structure field.

## Explicit exclusions

- Goldbach's strong conjecture, which requires both summands to be prime.
- The weak Goldbach theorem or Vinogradov's three-primes theorem.
- Results saying only that infinitely many primes `p` have `p + 2` almost prime.
- A bounded computational verification or an explicit finite cutoff as a substitute for the
  unbounded sufficiently-large theorem.
- A definition of "Chen representation" followed by a tautological existence statement.
- The repository label `已验证` as source or machine-proof evidence.

No canonical Lean target is frozen during intake because the exact source and `P_2` convention have
not been independently inspected.

