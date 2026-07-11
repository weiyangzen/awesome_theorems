# Scope map

## Included theorem family

- The classical Dirichlet problem for a harmonic function on a domain `Ω` with continuous real
  boundary data `f`.
- A boundary point `x ∈ ∂Ω` called regular through a barrier, Perron resolutivity, or an equivalent
  definition certified by the selected source.
- The local conclusion `u y -> f x` as interior points `y ∈ Ω` approach a regular `x`.
- The global corollary that appropriate continuous boundary data have a harmonic solution extending
  continuously to the boundary when every boundary point is regular, if the source states it.

## Decisions deferred to exact statement

The inspected source must fix Euclidean dimension (the legacy file chooses `ℂ`, but that choice is
not authoritative), boundedness and connectedness of `Ω`, compactness of its boundary, Laplace
versus a more general elliptic operator, real versus extended-real Perron solutions, and uniqueness.
It must also fix the topology of boundary convergence, the admissible boundary-data class, the
regularity definition, and degenerate cases such as an empty domain or boundary.

## Explicit exclusions

- Mere existence for arbitrary domains without a regular-boundary or resolutivity hypothesis.
- A weak Sobolev solution substituted for the classical harmonic/Perron claim without a proved
  equivalence and matching trace conclusion.
- Poisson-kernel solvability for a ball or disk substituted for the general regular-point theorem.
- A structure that carries the desired solution or convergence result as assumed data.
- The legacy `S1_M_144.lean` statement shape or its local bookkeeping declarations as terminal proof.

The statement phase must stop rather than guess if primary-source inspection does not disambiguate
the source phrase.
