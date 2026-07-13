# THM-M-1449 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the numerical-analysis catalog entry
named singular value decomposition. The repository supplies only the gloss `矩阵的SVD分解`
("SVD decomposition of a matrix"), attributes it to Eugenio Beltrami and Camille Jordan in 1873,
and labels it `已验证`. Under rev-5.6 that label is untrusted inventory metadata, not a
source-reviewed proposition or machine-proof evidence.

The gloss identifies the classical SVD family but is not binder-complete. It does not select real
or complex scalars, rectangular dimensions and finite index types, full versus thin or compact
factors, orthogonal versus unitary conventions, the orientation of the right factor, the encoding
and ordering of singular values, existence versus uniqueness, or empty-dimensional cases. Intake
does not silently choose among those proposition-changing conventions, so the canonical statement
and Lean target remain null.

Sheldon Axler's author-hosted *Linear Algebra Done Right*, fourth edition, Section 7E, was inspected
as an authoritative modern source lead. Definition 7.65 defines singular values and Theorem 7.70
proves an orthonormal-list SVD for finite-dimensional real or complex linear maps; the following
text derives the rectangular diagonal matrix form by extending the lists to orthonormal bases.
This corroborates the family, but it is not cited by the catalog, excludes zero-dimensional spaces
through the book's standing convention, and has no admitted immutable source packet, complete
transport, errata audit, or independent review here. It receives no `H0` credit.

The repository separately owns `THM-M-0044`, whose sharper gloss says every matrix decomposes in
`U Sigma V*` form. The two entries are likely duplicates, but no identity, root-ownership, or
evidence-sharing decision has been accepted. This dossier records that collision and inherits no
source, statement, proof, or status from the other target.

Pinned mathlib defines singular values and supplies spectral and unitary-matrix prerequisites. The
intake probe checks those interfaces at the pinned revision. The bounded repo-wide search also
located `THM-M-0044/Proof.lean`, which contains a kernel-checked full rectangular Real-and-Complex
SVD for that sibling's explicitly selected target, plus a separately written validation body. This
is the strongest formal candidate for later identity review, but it belongs to the unresolved
duplicate, its statement was not selected by this catalog gloss, and all its receipts remain
provisional. It receives no root credit here.

The provisional vector is `[H1, M3, R4]`: a complete modern proof lead and the classical family are
known, but exact source fidelity is open; a substantive repo-local candidate proof and target exist
under the unresolved duplicate but no source-identical canonical root is frozen or credited; and no
source-faithful proof reconstruction exists. `instance.json` freezes this boundary and
`task-dag.json` leaves all six downstream phases open. No accepted state, `H0`, `M0`, `R0`, audit
completion, theorem completion, or master acceptance is claimed.
