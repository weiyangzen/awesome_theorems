# THM-M-0043 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `谱定理`
(spectral theorem). The repository's only target-specific claim is `正规矩阵可酉对角化`
("normal matrices are unitarily diagonalizable"), attributed to David Hilbert in 1906 and labeled
`已验证`. Under rev-5.6, the attribution, date, and status are untrusted metadata, not a source
audit or proof receipt.

The gloss identifies the finite matrix spectral-theorem family but omits the scalar field, finite
index type and zero-dimensional convention, star and normality definitions, unitary convention,
the orientation of conjugation, and the exact diagonal witness. Over real scalars, a normal matrix
need not be orthogonally diagonalizable over the reals. Choosing the standard complex formulation
without a pinpoint source would therefore add a proposition-changing hypothesis.

A current authoritative textbook lead, Sheldon Axler's *Linear Algebra Done Right*, fourth
edition, Theorem 7.31, states a complex finite-dimensional operator version: normality is
equivalent to diagonal form in an orthonormal basis. It corroborates the intended family but is not
the catalog's cited source, and no independent source review or matrix/linear-map transport has
been accepted.

Pinned mathlib exposes `IsStarNormal` for the prospective normality premise and a strong adjacent
candidate, `Matrix.IsHermitian.spectral_theorem`. That candidate gives a unitary diagonalization
only for Hermitian matrices, a strict specialization of the catalog's normal-matrix claim. The
intake probe authenticates these APIs and the candidate's axiom report; it does not state or prove
the target.

The provisional vector is `[H1, M3, R4]`: a standard theorem statement and source lead are known
but the exact source and assumptions are not crosswalked; useful formal interfaces and a strict
special-case theorem exist but no exact Lean target is frozen; and no source-faithful proof
reconstruction exists. `instance.json` is the structured scope authority, and all six downstream
phases remain open in `task-dag.json`. No H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
