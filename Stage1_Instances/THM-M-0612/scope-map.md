# Scope map

## Included claim

- Standard finite-dimensional symplectic vector space of real dimension `2n`, with `n >= 1`.
- The open Euclidean ball `B^(2n)(r)` and cylinder `B^2(R) x R^(2n-2)` using the same standard symplectic normalization.
- A genuine symplectic embedding from the ball into the cylinder.
- The sharp radius obstruction `r <= R` (equivalently, no such embedding when `R < r`) for positive radii.

## Decisions deferred to statement phase

The selected primary statement must fix whether embeddings are defined only on the open ball or by
a global ambient map, the differentiability class, the coordinate ordering and two-form sign, and
whether the theorem is expressed by radii, areas, or capacity. It must also settle `n = 1`, strict
versus non-strict inequalities, and zero or negative radii. Universes and binder order will follow
that source-level freeze rather than the legacy module.

## Explicit exclusions

- Gromov compactness, the existence theorem for pseudoholomorphic curves, or another theorem merely bearing Gromov's name.
- A volume-only obstruction, a linear-symplectic special case, or a two-dimensional area theorem as a substitute.
- A structure that assumes form preservation or the desired capacity inequality without connecting it to the source notion of a symplectic embedding.
- The existing `StatementShape`, capacity targets, audit strings, or reflexive wrapper theorems as terminal proof evidence.

The later statement must use a local embedding on the source ball or supply a checked equivalence
showing that any chosen ambient-map encoding has exactly the primary theorem's scope.
