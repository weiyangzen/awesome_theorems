# Scope map

## Included claim

- The binomial random graph `G(n,p)` on a finite labelled vertex set, with
  edges present independently with probability `p`.
- The sparse scaling `p = c/n`, or a source-equivalent asymptotic formulation.
- The threshold parameter `c = 1` for component sizes.
- A subcritical result for fixed `0 <= c < 1`: every connected component is
  small with probability tending to one.
- A supercritical result for fixed `c > 1`: with probability tending to one a
  unique component has linear order and the remaining components are small.

This is one two-regime theorem family. The statement phase must not silently
replace it by only the easier subcritical or supercritical half.

## Decisions reserved for the statement phase

An inspected primary theorem must determine the precise random-graph model,
whether `p = c/n` exactly or `np -> c`, the constants and quantifiers in
`O(log n)` and linear-size assertions, and whether the conclusion is with high
probability, convergence in probability, or an explicit limiting law. It must
also settle the formulation of uniqueness, the size bound on non-giant
components, rounding of `cn/2` edge counts in the uniform graph process, and
the relationship between `G(n,p)` and `G(n,m)`.

The critical case `c = 1` and its `n^(2/3)` component scale are within the
broader topic but are not credited as part of the frozen two-regime claim
unless the chosen primary theorem packages them together. Binder order,
limits, measurability, and all universes remain statement-phase work.

## Degenerate and boundary cases to test later

- `n = 0` and `n = 1` finite vertex sets.
- `c = 0`, `c = 1`, and values of `c` incompatible with `p <= 1` for small
  `n`.
- Empty and complete graphs.
- Ties between largest component sizes and the exact meaning of uniqueness.
- The distinction between fixed `c` and an `n`-dependent sequence approaching
  the critical window.

## Explicit exclusions

- Connectivity at `p` of order `(log n)/n`, which is a different threshold.
- The mere definition of the Erdos-Renyi model.
- Bond percolation on a general infinite graph.
- A deterministic extremal graph theorem or a simulation-based observation.
- Assuming the giant-component conclusion as a field of an abstract package.
- Treating the repository's untrusted source label `已验证` as source or
  machine evidence.

## Expected formal surface

The later target needs finite simple graphs, a probability measure for
independent Bernoulli edges, connected components and their cardinalities,
largest-component predicates with tie handling, and asymptotic probability
statements. No claim is made at intake that pinned mathlib already provides
this complete interface.
