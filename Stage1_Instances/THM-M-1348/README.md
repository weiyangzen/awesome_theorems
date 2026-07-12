# THM-M-1348 rev-5.6 intake

`THM-M-1348` is the ordinary-differential-equations catalog item "Poincare-Bendixson theorem."
The catalog supplies only the gloss "limit sets of two-dimensional systems," an attribution to
Henri Poincare and Ivar Bendixson, the year 1901, and an untrusted `verified` label. These fields
identify a theorem family, not a binder-complete proposition.

## Intake result

This dossier records a fail-closed `planned` instance. It freezes the ambiguity instead of choosing
a familiar variant from memory. The record does not say whether the dynamics is a `C1` autonomous
planar vector field or a more general flow; whether an orbit is global, bounded, or precompact;
whether compactness and nonemptiness of its omega-limit set are assumed or derived; whether fixed
points are excluded or finitely many are allowed; or whether the conclusion is one periodic orbit
or a broader equilibrium/connection classification.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 7.3, is an
inspected authoritative source lead. It distinguishes the no-fixed-point Poincare-Bendixson lemma
from a generalized finite-fixed-point classification. Its current official errata also repairs a
proof omission in the named lemma and observes that a connectedness hypothesis in the generalized
theorem is superfluous. The repository does not cite this book or choose either result, so neither
is adopted as the canonical claim or credited as `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned ODE, flow, omega-limit, invariance, and periodic-point
APIs. A bounded name search found no terminal Poincare-Bendixson declaration in pinned mathlib;
the only repo-local exact-topic Lean file belongs to the duplicate target `THM-M-1400` and expressly
denies theorem completion. These are discovery observations only, not the downstream anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: an established theorem family and authoritative source lead are known, but exact
root selection, complete assumption and errata mapping, and independent review remain open; no
usable exact formal artifact is credited; and no source-faithful proof reconstruction can attach to
an unfrozen root. All six downstream tasks remain open. Neither audit completion nor theorem
completion is claimed.
