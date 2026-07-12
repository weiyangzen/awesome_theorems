# THM-M-0044 rev-5.6 intake

`THM-M-0044` is the singular value decomposition catalog item. The repository says that an
arbitrary matrix decomposes in the form `U Sigma V*`, attributes the result to Eugenio Beltrami and
Camille Jordan in 1873, and labels it verified. That label is untrusted metadata, not source or
machine-proof evidence.

## Planned scope

This intake preserves the conventional finite-dimensional matrix theorem for later source review:
every finite rectangular real or complex matrix admits square orthogonal/unitary left and right
factors and a conforming rectangular diagonal factor with nonnegative real diagonal entries. The
right star is transpose in the real case and conjugate transpose in the complex case. Existence is
in scope; uniqueness of the factors, numerical algorithms, conditioning, and low-rank approximation
are not.

This is a provisional theorem-family selection. The catalog does not choose the scalar field,
matrix dimensions, full versus thin factorization, diagonal-padding convention, ordering of
singular values, or exact meaning of `*`. The statement phase must ratify those choices against an
admitted source and freeze the exact Lean proposition.

## Source and formal boundary

Sheldon Axler's *Linear Algebra Done Right*, fourth edition, Section 7E, Theorem 7.70, is an
inspected modern source lead. It proves an SVD for linear maps between finite-dimensional real or
complex inner product spaces and then derives the rectangular matrix form by extending the two
orthonormal lists to bases. Intake did not admit an immutable repository-owned source packet,
complete the historical attribution or errata audit, or obtain independent review, so it does not
credit `H0`.

Pinned mathlib defines singular values of finite-dimensional linear maps and proves their
nonnegativity, ordering, eigenvalue relation, and support. It also provides spectral, diagonal,
adjoint, and unitary-matrix infrastructure. The bounded intake search found no terminal theorem
constructing both factors and proving `A = U * Sigma * Vᴴ`. `IntakeProbe.lean` authenticates only
these adjacent interfaces; it is not the downstream anchor audit and gives no proof credit.

The planned vector is `[H1, M3, R3]`: a published proof and source lead are known but exact source
fidelity and independent review are open; useful formal definitions and prerequisite interfaces are
present but no exact decomposition declaration is credited; and this dossier maps scope rather than
reconstructing a proof. All six downstream tasks remain open. No accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
