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

The statement artifact freezes the intake-selected reading as a conjunction of the `Real` and
`Complex` full rectangular matrix propositions over `Fin m` and `Fin n`. It uses square unitary
factors, an explicit zero-padded rectangular diagonal with `min m n` nonnegative real entries, and
matrix `star` for the right conjugate transpose. Ordering is not part of the catalog claim. Master
acceptance and independent source/duplicate review remain pending.

## Source and formal boundary

Sheldon Axler's *Linear Algebra Done Right*, fourth edition, Section 7E, Theorem 7.70, is an
inspected modern source lead. It proves an SVD for linear maps between finite-dimensional real or
complex inner product spaces and then derives the rectangular matrix form by extending the two
orthonormal lists to bases. Intake did not admit an immutable repository-owned source packet,
complete the historical attribution or errata audit, or obtain independent review, so it does not
credit `H0`.

Pinned mathlib defines singular values of finite-dimensional linear maps and proves their
nonnegativity, ordering, eigenvalue relation, and support. It also provides spectral, diagonal,
adjoint, basis-extension, and unitary-matrix infrastructure. The anchor audit authenticates eleven
such interfaces at mathlib revision `8a178386...ea95`, but finds no terminal theorem constructing
both factors and proving `A = U * Sigma * Vᴴ`.

Two external Lean 4 near-misses were inspected at immutable revisions. Atlas defines a Real-only
rank-indexed `SVD` record whose vector fields are not required to be orthonormal and supplies no
existence theorem. Gaussian-field proves an SVD-like result for summable nuclear sequences into an
infinite-dimensional real Hilbert space, not arbitrary finite Real-and-Complex matrices with two
square unitary factors. Neither statement matches or implies the frozen target, and neither project
was added to the local dependency closure.

The planned vector remains `[H1, M3, R3]`: a published proof and source lead are known but exact source
fidelity and independent review are open; useful formal definitions and prerequisite interfaces are
present and the exact target elaborates, but no decomposition proof is credited; and this dossier
maps scope rather than reconstructing a proof. The anchor node is self-tested pending master
acceptance; the obligation-tree and later tasks remain open. No accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
