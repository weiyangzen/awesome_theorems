# THM-M-1355 rev-5.6 intake

`THM-M-1355` is the ordinary-differential-equations catalog item "stability of linear
systems." The repository supplies only the gloss "stability criterion for linear systems," an
attribution to many mathematicians, the twentieth century, and an untrusted `verified` label.
Those fields identify a theorem family, not a binder-complete proposition.

## Intake result

This directory is a fail-closed `planned` dossier. It preserves the catalog wording instead of
choosing a familiar result from memory. In particular, the record does not say whether the system
is continuous-time `x' = A x`, discrete-time `x (k + 1) = A (x k)`, time varying, controlled, or
an infinite-dimensional semigroup. It does not fix finite dimension, scalar field, solution model,
equilibrium, or whether "stability" means boundedness, Lyapunov stability, asymptotic stability,
exponential stability, input-output stability, or another convention.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems* was inspected as an
authoritative source-family lead. Its Corollaries 3.5 and 3.6 and Theorem 9.1 distinguish bounded
stability from asymptotic stability for finite-dimensional continuous-time autonomous systems;
the zero-real-part Jordan condition is material in the former but the latter requires all real
parts to be negative. The catalog does not cite this source or select either claim, and the adjacent
Routh-Hurwitz target is a separate coefficient criterion. No candidate is adopted as the canonical
statement or credited as `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned matrix-exponential, eigenvalue/spectrum, and integral-
curve interfaces. A bounded name search found no terminal linear-system stability declaration in
pinned mathlib or the repository-local Lean source. These are intake discovery observations, not
the downstream formal anchor audit and not a global absence claim.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: a published source family is known, but exact root selection, assumption and source
mapping, errata review, and independent review remain open; no exact usable formal artifact is
credited; and no source-faithful reconstruction can attach to an unfrozen root. All six downstream
tasks remain open. No accepted state, audit completion, theorem completion, or master acceptance is
claimed.
