# THM-M-0342 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Plancherel's theorem. The repository
claim is that the Fourier transform is an isometry on `L^2`. The intended scope is the normalized
Fourier transform on complex-valued square-integrable functions over finite-dimensional real
Euclidean space, with equality of `L^2` norms (and the corresponding inner-product preservation).

The source record does not fix the Fourier-character normalization, Haar/Lebesgue measure
normalization, scalar versus Hilbert-valued formulation, or an exact primary-source theorem. Those
choices remain statement-phase work. A pinned Lean API probe confirms that mathlib contains an
`L^2` Fourier linear isometry and its norm and inner-product theorems. This is discovery evidence
only: no canonical expression, accepted proof state, audit completion, or theorem completion is
claimed.

The provisional root is `[H1, M3, R4]`. Exact intake commands and results are in `validation.md`.
