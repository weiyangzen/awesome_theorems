# Scope map

## Included theorem family

- Independent Bernoulli bond percolation with edge-open parameter `p` on the infinite square
  lattice, provisionally represented by vertices `Z x Z` and nearest-neighbor undirected edges.
- The critical parameter defined from positive probability of an infinite open cluster from a
  fixed origin, or an exactly proved equivalent convention selected from the primary source.
- The planar duality, crossing, connectivity, and infinite-volume probability notions needed to
  state the equality `p_c = 1/2` without building the desired result into a definition.

## Statement-freeze decisions

The selected root is the equality stated in Kesten's paper title. `Statement.lean` freezes bond,
not site, percolation; the horizontal/vertical nearest-neighbor `SimpleGraph` on `Int x Int`;
unoriented bonds; Boolean bond configurations with `Measure.infinitePi` Bernoulli coordinates;
origin reachability outside every finite vertex set as the infinite-cluster event; and `p_c` as the
`NNReal` infimum of `p <= 1` with positive event measure. Parameters `0`, `1`, and `1/2` are admitted.
The root is only `p_c = 1/2`; absence of an infinite cluster at criticality is a distinguished
stronger mutation and is not credited.

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

The canonical Lean expression and these components are now frozen by the statement artifacts.
Planar duality is proof architecture rather than a root-statement binder. Pinpoint primary-source
definitions, errata, and independent review remain open for the human-source audit.
