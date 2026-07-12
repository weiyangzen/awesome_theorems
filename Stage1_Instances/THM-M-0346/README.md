# THM-M-0346 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Carleson's theorem. The repository
claim is that the Fourier series of an `L^2` function converges almost everywhere. At intake this is
scoped to the classical one-dimensional periodic theorem: symmetric Fourier partial sums of a
complex-valued square-integrable function on the circle converge to the function almost everywhere.

The scope map records the normalization, representative, convergence, and boundary decisions that
must be fixed from an inspected primary source before an exact Lean proposition is frozen. The
source crosswalk identifies Carleson's 1966 paper as a primary-source candidate, but does not award
source-proof credit without a pinpoint inspection and errata review.

A pinned Lean probe confirms that mathlib provides the circle Fourier coefficient and `L^2` series
interfaces needed to begin an encoding. It does not assert Carleson's pointwise theorem. The root
remains `[H3, M4, R4]`; no exact statement, proof, audit completion, or theorem completion is claimed.

