# Proof outline — Konyagin lower bound

<a id="node-frozen-root"></a>
## N0 — frozen root

For each natural number `N`, let `F(N)` be the supremum of the cardinalities of
finite sets `A ⊆ [1,N]` for which every member of the pointwise sum `A+A` is
squarefree. The required output is the at-top estimate
`log(log N) · (log N)^2 = O(F(N))`. There are no mathematical hypotheses.

<a id="node-sieve-family"></a>
## N1 — squarefree-sum family

Choose a small-prime cutoff `y`, put every candidate in one admissible residue
class modulo the product of `p^2` for primes `p ≤ y`, and sieve the remaining
pair sums against squares of primes above `y`. The diagonal sums are included.
The construction yields a finite `A_N ⊆ [1,N]`, all of whose pair sums are
squarefree, with `|A_N| ≥ c · log(log N) · (log N)^2` beyond one absolute
threshold. Empty small ranges are absorbed into that threshold.

<a id="node-supremum"></a>
## N2 — pass to the extremal function

The witness `A_N` places `|A_N|` in the defining bounded set for `F(N)`, hence
`|A_N| ≤ F(N)`. Combining this comparison with N1 gives the eventual pointwise
bound by `F(N)`. Casting the natural supremum to the reals preserves the order.

<a id="node-asymptotic"></a>
## N3 — package the asymptotic estimate

Use the positive reciprocal of the construction constant as the Big-O witness.
The eventual inequality from N2 is exactly the norm inequality required by
`Asymptotics.IsBigO atTop`. This produces the frozen unconditional root.

<a id="node-transport"></a>
## N4 — semantic transport and release boundary

Expand the pinned definition of `Erdos1109.f` in both directions. The source
and target root expressions then coincide without a local alias or substituted
symbol. The worker records both transports; the Master must independently
re-elaborate the expression, audit all transitive constants and replay the
claim-owned proof at trust zero before acceptance.
