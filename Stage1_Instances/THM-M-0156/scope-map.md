# Scope map

## Included claim

- A finite-dimensional Euclidean ambient space, with dimension and scalar field to be fixed from
  the selected source.
- A compact region `Omega` with enough boundary regularity for volume and outward-oriented surface
  integration.
- A vector field `F` defined on a neighborhood of `Omega`, with enough differentiability and
  integrability for `div F` and boundary flux.
- Equality between the volume integral of `div F` and the boundary integral of the outward normal
  component of `F`.

At intake level the mathematical display is

```text
integral_Omega div(F) dV = integral_boundary(Omega) <F, n_out> dS.
```

This display fixes the theorem family and the direction/orientation convention. It is not yet the
canonical Lean proposition because the source metadata does not determine its binders or exact
hypotheses.

## Statement-phase decisions

The pinpoint primary or authoritative source must determine the ambient dimension; whether the
region is a `C^1`, piecewise smooth, Lipschitz, Jordan, or rectangular domain; the regularity of
`F`; scalar versus vector-valued integration; the measure and surface-measure normalization; and
the representation of the outward normal. It must also settle empty or degenerate regions,
disconnected regions, corners, zero-dimensional faces, and whether compact support replaces a
bounded-domain assumption.

The binder order, universes, orientation data, integrability hypotheses, and equality expression
must follow those decisions. Mutation checks in the statement phase must test removal of domain and
field regularity, reversal of boundary orientation, replacement of boundary flux by an unsigned
integral, and restriction to a single dimension or rectangle.

## Explicit exclusions

- Green's theorem, Stokes' theorem for differential forms, or the fundamental theorem of calculus
  presented as a substitute rather than a checked specialization or transport.
- Only a zero-divergence/zero-flux corollary, a single numerical example, or a conservation-law
  application.
- A rectangular-box theorem silently advertised as the unrestricted classical domain theorem.
- A structure or hypothesis that already contains the desired equality.
- The Stage0 label `已验证` or a theorem/module name treated as kernel or source evidence.

## Formalization boundary

The pinned mathlib source file
`Mathlib/MeasureTheory/Integral/DivergenceTheorem.lean` states a Bochner-integral result on boxes in
`Fin (n + 1) -> Real`, including countably many exceptional interior points. That is a substantive
candidate for an exact box-scoped target. Intake does not decide whether the source theorem should
be that result or a broader regular-domain theorem; the statement phase must either justify the box
scope from a selected source or record the missing boundary-integration API as a blocker.
