# THM-M-1387 rev-5.6 intake

`THM-M-1387` is the ordinary-differential-equations catalog item `振荡理论` (oscillation
theory). The catalog gives only the gloss `解的振荡性` (oscillatory behavior of solutions), a
collective attribution, the twentieth century, and an untrusted `verified` label. Those fields
identify a subject family, not a binder-complete proposition.

## Intake result

This dossier creates a fail-closed `planned` instance and preserves that ambiguity. The record does
not name an equation, interval, solution class, coefficient assumptions, definition of
oscillation, quantifier over solutions, or conclusion. Oscillation theory contains distinct results
about zero counts, comparison and separation, eigenfunction nodal counts, spectral criteria,
oscillation/nonoscillation tests, and asymptotic zero behavior. Choosing any one from memory would
substitute mathematics not supplied by the repository.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 5.5, is an
inspected authoritative source-family lead. It separates several regular Sturm-Liouville results
from the half-line definition of an oscillating equation and Kneser's criterion; the official
errata also corrects formulas and arguments in the section. The catalog does not cite this book or
select one of those results, so none is adopted as the canonical claim or credited as `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates only adjacent pinned integral-curve, derivative, iterated-derivative,
filter, and infinite-set APIs. A bounded local search found no ODE oscillation, Sturm-Liouville, or
Kneser theorem in pinned mathlib or repo-local Lean. The similarly named
`Mathlib.Analysis.Oscillation` concerns pointwise oscillation of arbitrary functions and continuity,
not zeros of differential-equation solutions. These are intake observations, not an exhaustive
anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: the supplied theory/property phrase is not yet one stable proposition; no usable
exact formal artifact is credited; and no source-faithful reconstruction can attach to an unfrozen
root. All six downstream tasks remain open. No accepted state, audit completion, theorem
completion, or master acceptance is claimed.
