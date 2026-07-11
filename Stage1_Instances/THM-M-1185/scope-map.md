# Scope map

## Preserved source scope

- Named result: Brenier theorem, attributed by the repository to Yann Brenier (1991).
- Subject: optimal transport.
- Structural feature: a convex potential participates in the transport.
- Available wording: `凸势的最优传输` ("optimal transport by a convex potential").

This is all the mathematical scope fixed by the repository record. The familiar quadratic-cost
Euclidean formulation is a likely theorem family, but is not silently adopted as the exact claim.

## Decisions required before statement freeze

The statement phase must identify a primary edition and freeze the ambient finite-dimensional
Euclidean spaces and dimension, source and target measures, probability/finite-mass convention,
moment assumptions, absolute-continuity or non-charging hypotheses, quadratic-cost normalization,
coupling and pushforward definitions, existence and almost-everywhere meaning of the gradient,
convex-potential regularity, optimality conclusion, and uniqueness (map, gradient, or potential up
to constants). It must say whether a converse and cyclic-monotonicity characterization belong to
the source theorem, and treat zero mass, dimension zero, null sets, infinite moments, and cost ties.

## Explicit exclusions

- Substitution of Kantorovich duality, general existence of an optimal plan, or McCann's theorem.
- A statement assuming an optimal convex-gradient map and merely returning that supplied fact.
- Arbitrary cost functions or manifolds unless the primary source variant explicitly requires them.
- Treating the metadata label `已验证` as either human-source or kernel evidence.
- Crediting adjacent optimal-transport Lean files before exact-type and provenance audit.
