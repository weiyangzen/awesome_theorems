# Scope map

## Included claim

- Standard finite-dimensional symplectic vector space of real dimension `2n`, with `n >= 1`.
- The open Euclidean ball `B^(2n)(r)` and cylinder `B^2(R) x R^(2n-2)` using the same standard symplectic normalization.
- A genuine symplectic embedding from the ball into the cylinder.
- The sharp radius obstruction `r <= R` (equivalently, no such embedding when `R < r`) for positive radii.

## Statement encoding decisions

`Statement.lean` uses a total function as Lean's representation of a map whose mathematical domain
is the open ball; smoothness, injectivity, and preservation of the displayed standard two-form are
all restricted to that ball. Coordinates are ordered `(q,p)`, the two-form sign is explicit, radii
are positive, sets use strict inequalities, and the conclusion is `r <= R`. A binder `i : Q`
includes the two-dimensional `|Q| = 1` case and excludes the zero-dimensional case. The universe and
binder order are printed by the recorded Lean check. Primary-source approval remains open and can
invalidate this proposal if its exact result differs.

## Explicit exclusions

- Gromov compactness, the existence theorem for pseudoholomorphic curves, or another theorem merely bearing Gromov's name.
- A volume-only obstruction, a linear-symplectic special case, or a two-dimensional area theorem as a substitute.
- A structure that assumes form preservation or the desired capacity inequality without connecting it to the source notion of a symplectic embedding.
- The existing `StatementShape`, capacity targets, audit strings, or reflexive wrapper theorems as terminal proof evidence.

The canonical statement uses a local embedding on the source ball. A future alternate encoding must
supply a checked equivalence rather than silently replacing it.
