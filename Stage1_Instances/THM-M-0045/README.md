# THM-M-0045 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `舒尔分解定理`
(Schur's theorem / Schur triangularization). The repository supplies only the gloss `复方阵可酉三角化`
("a complex square matrix can be unitarily triangularized"), attributes it to Issai Schur in
1909, and labels it `已验证`. Under rev-5.6 those fields are untrusted inventory metadata, not a
pinpoint source audit, exact Lean proposition, or proof receipt.

The gloss identifies the finite complex Schur-triangularization family, but it does not itself fix
a dimension/index type, upper-versus-lower triangular convention, unitary witness predicate,
conjugation orientation, or degenerate-case convention. The statement phase therefore selects and
records one modern source-rooted encoding rather than treating the one-line gloss as exact.

Schur's primary 1909 paper was located in the GDZ scan of *Mathematische Annalen* 66. Its Satz I,
printed pages 490-492, gives a unitary matrix `P` for which `P' A P` is triangular (lower triangular
in the displayed historical convention), for arbitrary real or complex square `A`; printed page
489 defines `P'` as conjugate transpose and unitarity by `P'P = E`. This materially authenticates
the historical family but is broader than the catalog's complex-only gloss and uses a different
triangular orientation from the modern lead. Formula-level OCR, definition transport, archival
terms, errata, and independent review remain open.

Sheldon Axler's author-hosted *Linear Algebra Done Right*, fourth edition, was also inspected as an
authoritative modern source lead. Theorem 6.38, on printed page 204, says every operator on a
finite-dimensional complex inner-product space has an upper-triangular matrix with respect to some
orthonormal basis. Its short proof invokes the fundamental theorem of algebra and Theorem 6.37,
whose proof preserves invariant prefix spans through Gram-Schmidt. This disambiguates the intended
family, but the catalog does not cite either source, the operator/basis-to-matrix/unitary transport
is open, and no independent source review is recorded. The two source leads support `H1`, not
`H0`.

Pinned mathlib supplies eigenvalue existence, generalized eigenspace substrate, Gram-Schmidt's
orthonormal-basis construction with an upper-triangular change-of-basis result, matrix
`BlockTriangular`, unitary change-of-orthonormal-basis matrices, and matrix representation APIs.
`IntakeProbe.lean` authenticates those interfaces. A bounded local search found no declaration that
combines them into the exact Schur-triangularization root. Ingredients and the neighboring
Hermitian spectral theorem are not substitutes for the received theorem.

The statement proposal selects Axler's upper-triangular finite complex theorem, specializes it to
`Matrix (Fin n) (Fin n) Complex`, includes dimension zero, and uses a unitary `U` with
`Matrix.BlockTriangular (star U * A * U) id`. `Statement.lean` elaborates and fingerprints that
target with three individually necessary imports; `BoundaryProbe.lean` checks dimensions zero and
one plus the upper-triangular and unitary conventions. Four mutations remove unitarity, change the
domain, change binder scope, or exclude dimension zero. No target inhabitant is provided.

The provisional vector remains `[H1, M3, R4]`: the exact Lean statement is worker-self-tested, but
immutable source preservation, definition and matrix/operator transport, corrections, and
independent source review remain open; no formal root proof or source-faithful reconstruction
exists. No H0, M0, R0, accepted state, audit completion, theorem completion, or master acceptance
is claimed.

The version-1 obligation architecture now freezes 37 semantic obligations before proof closure is
credited. It expands the immutable historical source through the dimension split, eigenvalue and
eigenspace construction, orthogonal-complement recursion, finrank descent, collected orthonormal
basis, three coefficient cases plus one impossible index placement, matrix transport, unitary and
triangular witnesses, final equation,
source, provenance, trust, and readability boundaries. The seven typed graphs keep proof,
refinement, provenance, evidence, trust, documentation, and workflow roles separate.

`ObligationTree.lean` checks only the exact conditional adapter from a global equation witness
package to `SchurTriangularizationTarget`. It does not construct that package or install the
external source. Revision `0a539f0c` remains `M5/E3`, every internal reverse edge remains an
unverified logical decomposition, and the current classified vector remains `[H1, M3, R4]`.
