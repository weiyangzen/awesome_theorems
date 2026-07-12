# THM-M-1391 rev-5.6 intake

`THM-M-1391` is the ordinary-differential-equations catalog item "Pruefer transformation." The
repository attributes it to Heinz Pruefer in 1926 and supplies only the gloss "phase analysis of
Sturm-Liouville problems" plus an untrusted `verified` label. A transformation and its purpose name
a mathematical method, not a proposition with fixed binders, hypotheses, and a conclusion.

## Intake result

This dossier records a fail-closed `planned` instance. It preserves the intended Sturm-Liouville
phase-analysis family without silently choosing among materially different claims: existence of
amplitude and a continuous lifted phase, equivalence of a second-order equation with a first-order
amplitude/phase system, reconstruction, zero counting, phase monotonicity, eigenvalue ordering, or
an oscillation theorem. The source record does not fix the differential-equation normalization,
coefficient regularity and signs, interval, solution class, amplitude normalization, angle branch,
behavior at zeros, endpoint data, or conclusion.

Pruefer's 1926 paper, *Neue Herleitung der Sturm-Liouvilleschen Reihenentwicklung stetiger
Funktionen*, is a strong historical source lead. Its digitized pages 499-518 were inspected: pages
503-505 introduce polar coordinates for the solution curve and use the phase equation in an
oscillation argument, while the paper's larger result concerns Sturm-Liouville expansion. The
catalog cites no passage and does not choose the coordinate transformation, its equivalence
claim, or a spectral consequence as the root. The paper is therefore a discriminator, not an
accepted `H0` source crosswalk.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned ODE, derivative, polar-coordinate, and complex-angle
APIs. Mathlib's principal-branch polar chart is not a continuous lifted Pruefer phase, and the
bounded topic search found no terminal Sturm-Liouville Pruefer-transform declaration. These are
intake discovery facts only, not the downstream anchor audit or proof evidence.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: `H5` records that the received method label and purpose gloss are not yet a stable
truth-valued proposition, not that established Pruefer mathematics is false. All six downstream
tasks remain open. No accepted execution state, audit completion, theorem completion, or master
acceptance is claimed.
