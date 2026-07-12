# THM-M-1360 rev-5.6 intake

`THM-M-1360` is the ordinary-differential-equations catalog item "Hopf bifurcation." The
repository attributes it to Eberhard Hopf in 1942 and supplies only the gloss "bifurcation in
which periodic solutions arise" plus an untrusted `verified` label. These fields identify a
recognizable theorem family, not a proposition with fixed binders, assumptions, and conclusion.

## Intake result

This dossier records a fail-closed `planned` instance. It preserves the catalog wording without
choosing among materially different Hopf results: the classical analytic finite-dimensional
existence theorem, a smooth finite-dimensional normal-form theorem, a supercritical or subcritical
stability classification, a Banach/PDE/delay-equation theorem, or a degenerate bifurcation result.
The source record does not fix the state space, vector-field regularity, equilibrium branch,
critical spectrum, transversality, nonresonance, Lyapunov coefficient, period normalization,
parameter side, local uniqueness, phase-shift quotient, or stability conclusion.

Hopf's paper, *Abzweigung einer periodischen Loesung von einer stationaeren Loesung eines
Differentialsystems*, is a strong historical source lead. A library record identifies its 1943
publication and an inspected scan says the work was presented on 19 January 1942. A modern
finite-dimensional account and a recent Banach-space theorem expose materially different contracts.
The catalog does not cite a passage or select one contract, so none is adopted as the canonical
claim or credited as `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned periodicity, ODE, flow, differentiability, eigenvalue,
and spectrum APIs. A bounded exact-topic search found no terminal Hopf-bifurcation declaration in
repo-local Lean or pinned mathlib. These are intake discovery facts only, not the later exhaustive
anchor audit and not evidence of absence from external projects.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: an established theorem family and credible source leads are known, but exact result
selection, complete source mapping, correction review, and independent review remain open; no usable
exact formal artifact is identified; and no source-faithful reconstruction can attach to an unfrozen
root. All six downstream tasks remain open. No accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
