# Scope map

## Included theorem boundary

- The ordinary partition number `p(n)`, represented canonically as
  `Fintype.card (Nat.Partition n)` after the representation crosswalk is proved.
- Rademacher's exact, convergent infinite series for `p(n)`.
- The source-specified finite exponential sum `A_k(n)`, including the coprimality range and the
  precise Dedekind-sum or multiplier convention.
- The hyperbolic-sine/derivative summand, its real domain, and convergence strong enough to justify
  equality to the natural-number-valued partition count after coercion.
- The exact range of `n` and all boundary values required by the primary theorem.

## Candidate mathematical shape, not a frozen statement

A common modern display has the shape

```text
p(n) = 1 / (pi * sqrt 2) * sum_(k >= 1) A_k(n) * sqrt(k)
       * d/dn [sinh((pi/k) * sqrt((2/3) * (n - 1/24))) / sqrt(n - 1/24)].
```

This display is deliberately not authoritative. Sources vary in the definition and sign convention
for `A_k(n)`, placement of constants, indexing, and whether the derivative is expanded. The
statement phase must transcribe one primary-source version and prove transports to any modern
encoding rather than choosing conventions by familiarity.

## Explicit exclusions

- The Hardy-Ramanujan asymptotic `p(n) ~ exp(pi * sqrt(2n/3)) / (4n sqrt 3)`.
- Any finite truncation, error estimate, decimal computation, recurrence, or congruence for `p(n)`.
- Euler's generating-function identity alone.
- A theorem where `p`, `A_k`, or the summand is assumed abstractly so the conclusion is tautological.
- Integer partitions of a set, graph partitions, partitions of unity, or ordered compositions.
- The repository label `已验证` as source or kernel evidence.

## Boundary decisions still open

Primary-source inspection must decide `n > 0` versus `n >= 0`, the real-variable neighborhood used
by the derivative, the coercion of `p(n)` into `Real` or `Complex`, the exact meaning of the infinite
sum, and whether equality is stated after showing the complex expression is real. No canonical Lean
target is frozen at intake.
