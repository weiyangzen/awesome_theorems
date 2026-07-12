# Scope map

## Included theorem family

- Independent Bernoulli bond percolation with edge-open parameter `p` on the infinite square
  lattice, provisionally represented by vertices `Z x Z` and nearest-neighbor undirected edges.
- The critical parameter defined from positive probability of an infinite open cluster from a
  fixed origin, or an exactly proved equivalent convention selected from the primary source.
- The planar duality, crossing, connectivity, and infinite-volume probability notions needed to
  state the equality `p_c = 1/2` without building the desired result into a definition.

## Decisions required at statement freeze

The statement phase must select and inspect an immutable primary edition and exact result. It must
freeze: bond rather than site percolation; the concrete square-lattice graph and dual graph;
unoriented rather than oriented edges; product probability space and edge independence; the event
used to define the percolation probability; whether `p_c` is an infimum of positive percolation
probability or a supremum of vanishing probability; the treatment of `p = 0, 1, 1/2`; and whether
the root is stated as `p_c = 1/2` alone or together with absence of an infinite cluster at
criticality. The order of all graph, vertex, configuration, event, and real-parameter binders must
be explicit.

The source's notation may identify the square lattice with `Z^2`, a planar embedded graph, or its
edge set. Those encodings require checked transports; informal isomorphism does not transfer proof
credit.

## Explicit exclusions

- Site percolation on the triangular or square lattice, oriented percolation, continuum
  percolation, higher-dimensional lattices, or a general planar graph.
- The elementary lower or upper bound on `p_c` alone, or only one direction of `p_c = 1/2`.
- A finite-box crossing estimate, duality identity, Russo-Seymour-Welsh lemma, or sharp-threshold
  result used as a substitute for the infinite-volume root theorem.
- A definition or hypothesis asserting `p_c = 1/2`, or a structure carrying the desired equality
  as data.
- Monte Carlo evidence, finite-grid enumeration, asymptotic heuristic, or the repository metadata
  value `已验证` as mathematical or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose the lattice, edge
configuration law, connectivity event, infinite-cluster predicate, critical parameter, and exact
equality concretely.
