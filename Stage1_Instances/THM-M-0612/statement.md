# Statement freeze

Item: `S56-M-0612-STATEMENT`

`Statement.lean` freezes the intake claim as the local-domain form of Gromov's symplectic
nonsqueezing theorem. For a finite nonempty coordinate index type `Q`, positive radii `r` and `R`,
and a chosen conjugate coordinate pair `i`, it says that a smooth symplectic embedding of the open
standard ball into the standard cylinder implies `r <= R`.

## Encoding decisions

- `PhaseSpace Q = (Q ⊕ Q) -> Real` gives real dimension `2 * |Q|` and coordinate order `(q,p)`.
- The binder `i : Q` enforces `|Q| >= 1`; no separate, weaker dimension side condition is hidden.
- Ball and cylinder use strict inequalities, hence are open. Both radii are explicitly positive.
- The standard form is `sum_i (dq_i wedge dp_i)` with its sign fixed by the displayed formula.
- A local embedding is represented by a total Lean function, but smoothness, injectivity, and
  derivative form preservation are all restricted to the ball. No condition outside the source
  domain is assumed.
- `Set.MapsTo` states that the image lies in the cylinder. The conclusion is the sharp radius
  inequality, not a volume obstruction, linear special case, or capacity assumption.

The canonical declaration is `Stage1.THM_M_0612.StatementShape`. It is deliberately a `def : Prop`:
this phase elaborates the exact target but supplies no proof and claims no machine closure.

## Minimal pinned import

The only direct import is `Mathlib.Analysis.Calculus.ContDiff.Basic`, from repository-pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. It supplies `ContDiffOn`, `fderiv`, and their
transitive foundational dependencies. No differential-form or symplectic-group module is needed
because the standard form is given explicitly in coordinates.

## Statement checks

The scoped Lean check elaborates the declaration and prints its type. Text checks separately verify
that the statement retains positive radii, local smoothness, local injectivity, derivative form
preservation, image containment, and the sharp `r <= R` conclusion. These are statement-phase
checks only; primary-source pinpoint review remains an H-status task and proof closure remains open.
