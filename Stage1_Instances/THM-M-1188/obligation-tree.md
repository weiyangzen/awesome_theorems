# THM-M-1188 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 17 semantic obligations before proof execution. Fifteen are
machine-required; `X-SOURCE` is human-source-only and `X-PROVENANCE` is an informational release
overlay. No analytic obligation is marked closed. Four checked statement/composition interfaces
are listed separately and give no root-closure credit. Any correction, split, merge, eligibility,
exclusion, or risk change requires a version-2 append-only delta.

## Typed proof route

```text
M1188-ROOT [open M3]
`-- M1188-T-ASSEMBLE [conditional composition checked]
    `-- M1188-T-ENGINE [open]
        |-- M1188-C-COMPACT
        |   `-- M1188-L-ATTAIN
        |-- M1188-C-PERTURB
        |   `-- M1188-B-INTERIOR
        |       |-- M1188-L-SPATIAL
        |       `-- M1188-L-TEMPORAL
        |-- M1188-N-BOUNDARY
        `-- M1188-L-EPSILON
```

The typed JSON graph records the exact edge orientation. The tree above is a readable dependency
summary; shared prerequisites appear once.

## m1188-root

The root is exactly the attained-boundary proposition elaborated by `Statement.lean`, including its
binder order, sign convention, and terminal-face exclusion.

## m1188-s-domain

This interface retains positive finite dimension, nonempty bounded open `U`, positive `T`, and
`closure U x [0,T]`. Empty, zero-time, dimension-zero, and unbounded variants remain excluded.

## m1188-s-boundary

The parabolic boundary is `closure U x {0}` union `frontier U x [0,T]`. The positive-time terminal
face over the interior is not silently admitted as boundary data.

## m1188-s-regularity

Continuity on the closed cylinder, spatial `C2`, temporal `C1`, and `u_t - Laplacian u <= 0` on
`U x (0,T]` remain separate explicit inputs.

## m1188-s-foundation

Classical compact extrema and finite-dimensional differential calculus are permitted. Exact
transitive axioms and trusted artifacts remain a release obligation.

## m1188-c-compact

This construction must prove compactness of the closed cylinder and parabolic boundary and must
provide boundary nonemptiness without strengthening the frozen assumptions.

## m1188-l-attain

This node packages actual maximizers using continuity and compactness. A supremum-only result does
not close the target's existential witness conclusion.

## m1188-c-perturb

For every positive epsilon, construct `v(x,t) = u(x,t) - epsilon*t` and establish the strict heat
inequality with all derivative and Laplacian transports checked.

## m1188-l-spatial

At a positive-time maximum whose spatial point lies in `U`, show the spatial Laplacian of the
perturbed function is nonpositive. The coordinate Hessian-to-Laplacian bridge is substantive.

## m1188-l-temporal

At a maximum relative to earlier times show the temporal derivative is nonnegative. This must
handle `t = T` by a one-sided argument rather than assuming an open time neighborhood.

## m1188-b-interior

Combine the strict subsolution inequality with both derivative signs to exclude a positive-time
maximum whose spatial coordinate is in `U`.

## m1188-n-boundary

Identify every remaining cylinder maximizer with the exact initial-or-lateral boundary. This owns
the topology fact connecting `closure U \ U` to `frontier U` under openness.

## m1188-l-epsilon

Remove epsilon while preserving an attained boundary witness. Because the witness may depend on
epsilon, this node must use compactness/subsequence or an equivalent checked argument; pointwise
limit prose alone is insufficient.

## m1188-t-engine

This terminal analytic package consumes compactness, attainment, strict perturbation, interior
exclusion, boundary identification, and epsilon removal to produce `AnalyticMaximumEngine`.

## m1188-t-assemble

`root_compose` checks that the engine has the exact root type. It proves only conditional
composition; the analytic engine remains an open premise.

## m1188-x-source

Evans is only a secondary statement anchor at present. Exact pages, assumptions, errata, and a
premise-to-node proof crosswalk remain `H2` work.

## m1188-x-provenance

Terminal body provenance, axiom closure, compiled dependencies, reproducible replay, and independent
verification remain open release work.

## Status boundary

All semantic step budgets are at most 100. Separate proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs are frozen in `typed-graphs.json`. This phase claims no analytic
proof closure, H0, R0, audit completion, theorem completion, release readiness, or master acceptance.
