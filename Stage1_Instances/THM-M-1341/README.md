# THM-M-1341 rev-5.6 intake

`THM-M-1341` is the ordinary-differential-equations catalog item "variational equation." The
catalog supplies only the gloss "solution sensitivity equation," an attribution to many
mathematicians, a twentieth-century date, and an untrusted `verified` label. These fields identify
a theorem family, not a binder-complete proposition.

## Intake result

This dossier records a `planned` instance and freezes the ambiguity rather than choosing a
convenient standard variant. The gloss does not say whether sensitivity is taken with respect to
initial state, initial time, or an external parameter. It also leaves open the equation and
solution model, state and parameter spaces, regularity, base trajectory, common interval,
homogeneous versus inhomogeneous linearization, operator orientation, and initial tangent data.

An inspected modern source lead, Gerald Teschl's *Ordinary Differential Equations and Dynamical
Systems*, makes the ambiguity concrete. Section 2.4, pages 46-48, treats the derivative of a local
flow with respect to initial state through the homogeneous first variational equation and separately
states smooth parameter dependence. Section 2.5, page 49, derives an inhomogeneous parameter
sensitivity equation. The repository does not cite this book or select one of these inequivalent
roots, so none is adopted as the canonical claim or credited as `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned ODE and Frechet-calculus APIs. A bounded name search
found no exact ODE variational- or sensitivity-equation declaration in repo-local Lean or pinned
mathlib. This is discovery-only evidence, not the downstream anchor audit and not proof of absence
from every Lean project.

The canonical mathematical statement and Lean expression therefore remain null. The provisional
vector is `[H1, M4, R4]`: an authoritative source lead and recognizable theorem family are known,
but the exact source proposition is not selected or independently reviewed, no usable exact formal
artifact is located, and no proof reconstruction can attach to an unfrozen root. All six downstream
tasks remain open. Neither audit completion nor theorem completion is claimed.
