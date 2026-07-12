# Scope map

## Included claim

- A real normed vector space `E`; completeness of all of `E` is not part of the compact-convex
  formulation and must not be added merely because Stage0 says "Banach space."
- A subset `K` that is nonempty, compact, and convex.
- A function `f : E -> E` continuous on `K` and satisfying `f(K) subset K`.
- Existence of `x in K` with `f x = x`; uniqueness is not asserted.

## Binder and boundary decisions for statement phase

The statement phase must reconcile the frozen compact-convex claim with the inspected primary
source. It must decide whether to express the map on the ambient space or on the subtype `K`,
whether continuity is global or only on `K`, and whether the chosen source instead uses a closed
convex set whose image is relatively compact. Any alternate form needs a checked relationship to
the canonical target. Universe, scalar, topology, and typeclass binder order must be recorded from
the elaborated Lean expression.

Boundary tests must cover empty `K`, singleton `K`, failure of the self-map condition, replacement
of compactness by closedness or boundedness, and removal of convexity. The source statement decides
which of these are excluded cases and which are non-equivalent mutations.

## Explicit exclusions

- Banach's contraction mapping theorem, which assumes a contraction and gives uniqueness.
- Brouwer's finite-dimensional fixed-point theorem as the terminal claim.
- Tychonoff's or Markov-Kakutani's fixed-point theorem without a checked specialization.
- Schauder basis results, Schauder estimates for PDE, or a generic structure containing a fixed
  point as a field.
- A proof that assumes the desired fixed point or an unverified external theorem anchor.

## Formal surface discovered at intake

The pinned mathlib tree exposes `Set`, `Convex`, `IsCompact`, `ContinuousOn`, and `Set.MapsTo`.
`IntakeProbe.lean` checks those names under one broad discovery import. This is vocabulary evidence
only: minimal imports, the exact proposition, candidate terminal declarations, and proof closure
belong to later nodes.
