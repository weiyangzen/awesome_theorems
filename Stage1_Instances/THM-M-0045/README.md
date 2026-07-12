# THM-M-0045 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `舒尔分解定理`
(Schur's theorem / Schur triangularization). The repository supplies only the gloss `复方阵可酉三角化`
("a complex square matrix can be unitarily triangularized"), attributes it to Issai Schur in
1909, and labels it `已验证`. Under rev-5.6 those fields are untrusted inventory metadata, not a
pinpoint source audit, exact Lean proposition, or proof receipt.

The gloss identifies the finite complex Schur-triangularization family, but it does not fix a
dimension/index type, upper-versus-lower triangular convention, unitary witness predicate,
conjugation orientation, or degenerate-case convention. Intake therefore does not silently choose
one matrix equation from the familiar equivalent formulations.

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

The provisional vector is `[H1, M3, R4]`: primary and modern complete-theorem source leads are
known but exact source-statement admission and transport are open; substantial interfaces exist but no canonical
Lean root or exact formal closure is frozen; and no source-faithful proof reconstruction exists.
`instance.json` is the structured scope authority, while `task-dag.json` keeps all six downstream
phases open. No H0, M0, R0, accepted state, audit completion, theorem completion, or master
acceptance is claimed.
