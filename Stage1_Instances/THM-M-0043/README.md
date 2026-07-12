# THM-M-0043 rev-5.6 statement

This directory is the `planned` dossier for the catalog item `谱定理`
(spectral theorem). The repository's only target-specific claim is `正规矩阵可酉对角化`
("normal matrices are unitarily diagonalizable"), attributed to David Hilbert in 1906 and labeled
`已验证`. Under rev-5.6, the attribution, date, and status are untrusted metadata, not a source
audit or proof receipt.

The statement worker resolves the gloss through Sheldon Axler's *Linear Algebra Done Right*, fourth
edition, Section 7B, Theorem 7.31, pages 246-247. That theorem fixes a finite-dimensional complex
space and states that normality is equivalent to diagonal form in an orthonormal basis. The selected
root is exactly its normal-to-diagonal direction expressed for a square complex matrix:
`Stage1Instances.THM_M_0043.SpectralTheoremTarget`.

The root includes every nonempty finite index type, matching Axler's standing convention that the
space is nonzero, and uses `IsStarNormal A` for commutation with conjugate transpose. It concludes
that there are a unitary matrix `U` and diagonal
entries `d` with `A = U * Matrix.diagonal d * star U`. Checked transports cover the explicit
unitary-membership encoding and the equivalent orientation
`star U * A * U = Matrix.diagonal d`. Real normal matrices are deliberately not substituted for
the source's complex domain.

`Statement.lean` elaborates under the pinned environment with direct imports
`Mathlib.Data.Complex.Basic` and `Mathlib.LinearAlgebra.UnitaryGroup`; deleting either import fails.
`check_statement.py` fingerprints the fully explicit expression, distinguishes all four required
mutations, and rechecks both transports. It does not invoke the adjacent Hermitian theorem or prove
the canonical root.

The vector remains `[H1, M3, R4]`: the exact interface is frozen, while independent source review,
historical Hilbert/1906 provenance, the anchor audit, proof, and readable reconstruction remain
open. This statement work is provisional pending master acceptance. No H0, M0, R0, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
