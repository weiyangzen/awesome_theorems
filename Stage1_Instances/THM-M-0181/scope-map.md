# Scope map

## Included subject boundary

- A smooth finite-dimensional manifold equipped with a smooth Riemannian metric.
- A one-parameter metric family satisfying `partial_t g = -2 Ric(g)` with prescribed initial
  metric, on a nonzero interval starting at zero.
- Short-time existence, regularity in space and time, preservation of positive definiteness, and
  the precise uniqueness notion selected from the primary source.
- The DeTurck gauge reduction, strict parabolic existence/uniqueness, and pullback by the generated
  diffeomorphisms are expected proof-architecture branches, not facts credited at intake.

## Decisions required before statement freeze

The generated metadata says only "short-time existence and uniqueness." The statement phase must
use a stable primary-source edition to freeze: compact/closed versus complete noncompact scope;
boundary and connectedness assumptions; regularity; whether time is `[0,T]` or `[0,T)`; the exact
quantification of `T`; and whether uniqueness is literal for Ricci flow or expressed through the
gauge construction. It must also decide a workable mathlib model of time-dependent metrics without
replacing Ricci curvature by an uninterpreted predicate.

## Explicit exclusions

- Hamilton's long-time convergence theorem for three-manifolds with positive Ricci curvature.
- Later complete-noncompact, bounded-curvature, weak, surgical, or normalized-flow variants.
- A generic parabolic PDE theorem without a checked bridge back to the Ricci-flow equation.
- Assuming the desired flow or its uniqueness as a hypothesis.
- Any historical Stage1 wrapper as rev-5.6 statement or proof evidence.

The later statement phase must freeze universes, dimension, smoothness classes, metric and Ricci
objects, ordered binders, degenerate cases, imports, declaration type, environment fingerprint,
checked transports, and hypothesis mutations.
