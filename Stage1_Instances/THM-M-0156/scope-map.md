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

This display fixes the theorem family and direction/orientation convention. The canonical Lean
proposition below selects its rectangular-box realization without claiming arbitrary-domain scope.

## Statement-phase decision

The canonical Lean target is the positive-dimensional closed rectangular-box theorem encoded in
`Statement.lean`. It uses `Fin (n + 1) -> Real`, coordinatewise `a <= b`, continuity on `Icc a b`,
Frechet differentiability throughout the open box, integrability of the coordinate derivative
trace, product Lebesgue volume, and signed upper-minus-lower coordinate-face integrals. Degenerate
boxes remain included.

## Source-audit decisions still open

The pinpoint primary or authoritative source must determine the ambient dimension; whether the
region is a `C^1`, piecewise smooth, Lipschitz, Jordan, or rectangular domain; the regularity of
`F`; scalar versus vector-valued integration; the measure and surface-measure normalization; and
the representation of the outward normal. It must also settle empty or degenerate regions,
disconnected regions, corners, zero-dimensional faces, and whether compact support replaces a
bounded-domain assumption.

The anchor/source audit must still identify and independently review an exact human edition and
page. A later general-domain statement needs its own checked transport and cannot retroactively
broaden this declaration.

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
`Fin (n + 1) -> Real`, including countably many exceptional interior points. Its documented box
formulation fixes the exact statement scope here, while the canonical target uses the ordinary
every-interior-point differentiability specialization. Existing proof bodies receive no statement-
phase credit; provenance and trust inspection belong to the anchor audit.
