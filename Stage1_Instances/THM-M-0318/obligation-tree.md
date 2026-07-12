# THM-M-0318 obligation tree

This version freezes 12 canonical obligations. It deliberately records the missing Schauder
mathematics before proof execution and gives no credit for planned signatures or for the checked
conditional composition harness.

## M0318-ROOT

The exact root is `SchauderFixedPointTarget`. It requires the statement/foundation layer, the
approximation branch, the compact-limit branch, terminal composition, and the release trust record.

## M0318-S

`Statement.lean` fixes the real normed space, nonempty compact convex set, continuous-on self-map,
and member fixed-point conclusion. Source fidelity remains H2.

## M0318-S-TRANSPORT

`target_iff_expanded` checks the API-to-expanded statement transport and proves no fixed point.

## M0318-C

The construction must turn compactness into a finite-dimensional approximation scheme with
continuous barycentric maps, membership in `K`, and uniform error bounds.

## M0318-C-NET

For each positive tolerance, compactness must produce a finite net with centers and covering
inequalities in the exact representation needed downstream.

## M0318-C-MAP

Subordinate weights and their barycenter must be well-defined, continuous, K-valued, uniformly
close to the identity, and carried by a finite-dimensional span. This central node is marked
split-required rather than hidden behind "standard partition of unity".

## M0318-B-BROUWER

A finite-dimensional Brouwer theorem must be integrated at the local pin and matched to the
constructed carrier. The audited external theorem is only an immutable source anchor at a different
toolchain, so this bridge is open.

## M0318-L-APPROX

The construction and Brouwer branches must yield an `x` in `K` with `dist (f x) x < ε` for every
positive `ε`. `ApproximationEngine` is an elaborated interface, not its proof.

## M0318-L-LIMIT

Choose approximate fixed points at vanishing tolerances and use compactness to extract convergence
to a point of `K`, retaining the vanishing displacement estimate.

## M0318-L-CONT

Continuity on `K` must transport the limit through `f`; the limit of the displacement is zero, hence
`f x = x`.

## M0318-X-TRUST

Validation must later inventory axioms, terminal bodies, the external Brouwer boundary, dependency
pins, and replay evidence. This is a release dependency, not a proof premise.

## M0318-T-COMPOSE

`compose_schauder` kernel-checks that `ApproximationEngine` and `CompactLimitEngine` consume exactly
the frozen hypotheses and yield the exact root. Both engines remain abstract open hypotheses, so
this local closure cannot be promoted to root closure.

The current open root cut set is `C-NET`, `C-MAP`, `B-BROUWER`, `L-LIMIT`, and `L-CONT`.
