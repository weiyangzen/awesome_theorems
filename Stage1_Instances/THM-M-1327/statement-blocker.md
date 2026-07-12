# Statement-phase blocker

## Verdict

`S56-M-1327-STATEMENT` is blocked. No canonical Lean target is asserted, and this artifact does
not claim completion of the statement node or of the theorem.

The intake correctly froze a theorem family rather than an exact proposition. Its prerequisite for
this phase is an inspected, pinpoint primary-source theorem fixing the curvature-bound direction,
smooth domain, Hessian and curvature conventions, model coefficient, exceptional radii, and exact
inequality. The available dossier contains only uninspected book-level discovery candidates. The
repository phrase "Hessian of the distance function" does not decide these choices: standard
upper- and lower-curvature variants have opposite comparison directions. Selecting one from memory
would substitute an invented canonical member for the repository target.

## Pinned Lean substrate

The worker used Lean `v4.29.0` with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. In that exact tree, the Riemannian directory contains
only `Basic.lean` and `PathELength.lean`. A case-insensitive source search found no definitions or
declarations for a Hessian, sectional curvature, cut locus, or exponential map under
`Mathlib/Geometry/Manifold`. Covariant derivatives are present, but no pinned Levi-Civita
connection or second-covariant-derivative interface connects them to the Riemannian distance.

`StatementInfrastructureProbe.lean` elaborates the nearest honest interfaces using the two direct
imports needed for the probe. It is not the requested exact target. Encoding abstract functions
named "Hessian" and "curvature", or accepting the desired comparison as a hypothesis, would evade
rather than satisfy the exact-statement gate and is therefore excluded.

## Retry condition

Retry this node only after both of the following are available:

1. A stable primary-source edition, theorem/page, definitions, errata check, and transcription that
   fixes every variant choice listed above.
2. Concrete pinned Lean interfaces for distance smoothness away from the cut locus, the Riemannian
   Hessian, sectional curvature, and the selected model coefficient, or an explicitly scoped local
   implementation of those definitions that does not assume the comparison conclusion.

Until then the intake's `[H3, M4, R4]` vector and `planned` lifecycle remain unchanged.
