# Scope map

## Included theorem family

- Independent bond or site percolation with occupation parameter `p` on a source-specified,
  locally finite infinite graph or lattice.
- The probability `theta(p)` that a distinguished vertex belongs to an infinite open cluster, or
  the source's precisely equivalent infinite-connectivity event.
- A critical parameter `p_c` defined from `theta`, susceptibility, or another source-specified
  order parameter, with the defining infimum/supremum and endpoint conventions made explicit.
- Only the phase-separation or critical conclusions in the selected primary theorem, such as
  absence below the threshold, positive percolation probability above it, or an endpoint result.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary result. It must freeze: bond versus
site percolation; graph vertex and edge types; lattice dimension and adjacency; rooted versus
translation-invariant formulation; product probability space and independence; open-object event;
finite-path and infinite-cluster definitions; whether cluster uniqueness is involved; the order
parameter and exact definition of `p_c`; whether the endpoints `p = 0`, `p = p_c`, and `p = 1` are
included; and whether the conclusion is mere existence of a nontrivial threshold, strict
subcritical/supercritical behavior, continuity, exponential decay, critical exponents, or scaling.

These choices change Lean domains, binders, hypotheses, and conclusions. In particular, defining
`p_c` as an infimum does not by itself prove nontriviality, endpoint behavior, or any critical
phenomenon.

## Explicit exclusions

- Kesten's exact planar critical-probability theorem, Cardy's crossing formula, Smirnov's conformal
  invariance theorem, or SLE scaling limits as substitutes for this earlier general entry.
- A finite-graph connectivity threshold or an Erdos-Renyi random-graph phase transition.
- A theorem only about oriented, dependent, continuum, invasion, or first-passage percolation
  unless that exact model is selected from the source.
- The tautology obtained by defining `p_c` as an infimum without proving the claimed phase facts.
- Assuming the existence, nontriviality, uniqueness, or critical behavior of clusters in a
  structure or hypothesis and then projecting that field.
- Monte Carlo evidence, numerical critical probabilities, finite-size scaling, or physical
  universality heuristics.
- The repository metadata value `已验证` as human-source or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose the graph, product
measure, open configuration, connectivity event, infinite-cluster predicate, threshold definition,
and precise phase conclusion rather than packaging the conclusion as assumed data.
