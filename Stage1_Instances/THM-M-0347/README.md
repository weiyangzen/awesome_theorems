# THM-M-0347 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Fejer's theorem in periodic Fourier
analysis. The repository gloss says only that the Cesaro means for a continuous function converge.
The standard theorem concerns the first-order Cesaro means of the Fourier partial sums of a
continuous periodic function and gives uniform convergence back to that function.

The mathematical family is identified, but the source record does not fix the circle period,
real- versus complex-valued functions, Fourier normalization, indexing of symmetric partial sums,
whether the zeroth or first mean starts the sequence, or whether its word "converges" means the
standard uniform conclusion. Those decisions, a primary-source pinpoint, and an exact Lean target
remain for the statement phase.

A bounded pinned Lean probe confirms that mathlib has the additive-circle, normalized Haar
measure, continuous-map, Fourier coefficient, monomial, and uniform-convergence APIs needed to
state the theorem. It does not assert Fejer's theorem and receives no proof credit. The root remains
`[H1, M4, R4]`; exact commands and results are recorded in `validation.md`.
