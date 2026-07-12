# THM-M-1368 rev-5.6 intake

`THM-M-1368` is the ordinary-differential-equations catalog item "Morse-Smale systems." The
repository attributes it to Marston Smale in 1961 and supplies only the gloss "characteristics of
structurally stable systems" plus an untrusted `verified` label. Those fields name a recognizable
dynamical-systems family, not a proposition with fixed binders, assumptions, and conclusion.

## Intake result

This dossier records a fail-closed `planned` instance. It preserves the ambiguity instead of
silently replacing the catalog entry by one familiar result. The catalog does not decide between a
flow and a diffeomorphism, define a Morse-Smale system, fix the compact manifold or regularity, or
say whether the root is a definition/characterization, structural-stability theorem, gradient-flow
genericity theorem, Morse-theoretic decomposition, or surface-specific equivalence.

Stephen Smale's 1961 *On Gradient Dynamical Systems* is a plausible historical source lead and
exposes the catalog's literal "Marston Smale" first-name discrepancy, but its full theorem text was
not available from the inspected metadata endpoints. A fixed revision of
Michael Shub's reviewed Scholarpedia article distinguishes the finite-hyperbolic-periodic-orbit and
stable/unstable-transversality definition from the later Palis-Smale structural-stability theorem.
This confirms that the catalog gloss does not select one root. Neither source is adopted as the
canonical claim or credited as `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned ODE, flow, invariance, periodic-point, manifold
integral-curve, and tangent-derivative APIs. A bounded exact-topic search found no terminal
Morse-Smale declaration in repo-local Lean or pinned mathlib. These are intake discovery facts
only, not an exhaustive anchor audit or an external-project absence claim.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: `H5` classifies the received family label and gloss as not yet a stable proposition;
it does not say that properly stated Morse-Smale theorems are false or open. No usable exact formal
artifact is identified, and no source-faithful reconstruction can attach to an unfrozen root. All
six downstream tasks remain open. No accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
