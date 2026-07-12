# Scope map

## Included claim

- The ordinary partition function `p(n)`: the cardinality of unordered multisets of positive
  natural numbers whose sum is `n`.
- The natural-number limit `n -> infinity`.
- The leading asymptotic term `exp(pi * sqrt(2*n/3)) / (4*n*sqrt(3))`.
- Asymptotic equivalence, meaning that the ratio tends to one (subject to a checked equivalence with
  the chosen Lean `IsEquivalent` encoding).

## Decisions required at statement freeze

- Confirm the exact displayed formula, numbering, domain, and conventions against an immutable copy
  of the 1918 source, including corrections or errata.
- Decide whether the Lean target uses `Fintype.card (Nat.Partition n)`, a separately named partition
  counting function, or a checked equivalent representation.
- Freeze coercions and parentheses in `sqrt (2*n/3)`, behavior of the comparison function at zero,
  and the precise `Filter.atTop` formulation.
- Record the normalized kernel expression and execute removed-component, changed-domain,
  changed-binder-scope, and boundary mutations before inspecting proof closure.

## Explicit exclusions

- Rademacher's later convergent exact series, partition congruences, and restricted partitions.
- Ordered compositions, plane partitions, Young-tableau enumeration, and statistical-mechanics
  partition functions.
- A big-O estimate or equality with only the same exponential growth rate in place of asymptotic
  equivalence with the full constant factor.
- A tautological theorem assuming the asymptotic formula as a hypothesis.
- The repository label `已验证` as human-source or machine-proof evidence.

The intake fixes this boundary but leaves exact source acceptance and canonical Lean elaboration to
their later, dependency-ordered phases.
