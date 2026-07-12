# THM-M-0344 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"uncertainty principle". The only supplied claim is that a function and its Fourier transform
cannot both be concentrated. That sentence identifies a theorem family, not one proposition:
variance, support, entropy, and quantitative concentration formulations have different domains,
normalizations, constants, hypotheses, and equality cases.

The intake freezes that ambiguity rather than silently choosing the familiar Heisenberg inequality.
The root remains `[H3, M4, R4]`. A pinned Lean probe checks that mathlib supplies the ordinary
Fourier integral, the `L2` Fourier isometry, and the Schwartz-space Fourier transform needed by
several candidate readings. It is not a target statement or proof. Exact commands and results are
recorded in `validation.md`.
