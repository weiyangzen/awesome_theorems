# THM-M-0341 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Fourier
transform inversion formula". The source inventory says only "the inverse transform of the Fourier
transform" and does not specify a function space, transform normalization, hypotheses, equality
mode, or source theorem.

Those omissions distinguish materially different theorems: pointwise inversion at continuity
points under `L1` assumptions, equality of continuous functions, almost-everywhere inversion,
`L2` inversion, Schwartz-space inversion, and Fourier-series inversion are not interchangeable.
The intake therefore freezes that scope ambiguity rather than silently choosing one theorem.

Pinned mathlib contains a directly relevant finite-dimensional real inner-product-space theorem,
`MeasureTheory.Integrable.fourierInv_fourier_eq`, and a continuous-function corollary. The bounded
Lean probe checks their types and the transform definitions. This is discovery evidence only: the
next statement phase must crosswalk an exact source statement before selecting and elaborating the
canonical target. The root remains `[H1, M3, R3]`; no accepted proof or completion is claimed.
