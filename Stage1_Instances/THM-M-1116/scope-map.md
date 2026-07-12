# Scope map

## Included theorem family

- A discrete-time random graph process that adds vertices and edges and preferentially chooses
  existing endpoints according to current degree, after the exact source variant is selected.
- A degree-count observable, such as the number or proportion of vertices of degree `k` at time
  `n`, with the order of the `n` and `k` quantifiers made explicit.
- A source-specified power-law conclusion, potentially an exact limiting mass function with tail
  exponent three rather than merely an informal log-log slope.
- The probability mode and uniformity actually proved by the selected source: expectation, in
  probability, with high probability, or almost surely.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary theorem. It must freeze: the initial
multigraph or seed; whether loops and parallel edges are allowed; the number of new edges at each
step; sequential versus simultaneous endpoint sampling; whether degree is updated between choices;
the normalization and any additive attractiveness/initial-degree offset; the handling of a new
vertex and self-selection; the sample space and independence structure; the degree-count random
variable; fixed degree versus a growing degree range; the exact limiting formula or asymptotic
notation; the convergence mode and rate; and the order of all time, degree, error, and probability
quantifiers. Small-time states, zero-degree vertices, and zero total degree require explicit rules.

These choices change both the stochastic process and the theorem. The popular Barabasi-Albert
description and later rigorous linearized-chord-diagram or affine preferential-attachment models
must not be treated as definitionally interchangeable.

## Explicit exclusions

- The assertion that a plotted or simulated network "looks scale-free".
- A deterministic graph whose degree sequence is assumed to obey a power law.
- Existence of preferential attachment as a generative algorithm without a theorem about its
  distribution.
- A result only about expected degree, maximum degree, connectivity, diameter, clustering, or
  community structure as a substitute for the selected degree-distribution theorem.
- A uniform-attachment, configuration, Erdos-Renyi, small-world, or affine-fitness model unless an
  audited transport proves it is the exact selected process.
- A structure or hypothesis that contains the desired limiting distribution as input data.
- The repository metadata value `已验证` as source or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose the graph process,
probability law, degree counts, normalization, convergence predicate, and boundary conventions.
