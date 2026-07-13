# THM-M-0050 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named
Sylvester's law of inertia. The repository gloss is: "the positive and negative inertia indices
of a real symmetric matrix are invariant under congruence." Its `已验证` label is untrusted
inventory metadata, not source or machine evidence.

The gloss identifies a standard theorem family but leaves proposition-changing choices open: the
matrix dimension and index type, the exact invertible congruence witness and equation orientation,
the definition of the positive and negative indices, the role of the zero index, and all boundary
cases. Sergei Treil's *Linear Algebra Done Wrong* gives a complete modern proof lead in Chapter 7,
Section 3, printed pages 206-208. It states that the positive and negative counts in an invertible
diagonalization equal maximal definite-subspace dimensions. The catalog does not cite this book,
the source is stated for Hermitian matrices, and the specialization and arbitrary-congruence
transport have not been independently reviewed. It is therefore an `H1` lead, not `H0` evidence.

Pinned mathlib provides `QuadraticForm.sigPos`, `QuadraticForm.sigNeg`, their invariance under
`QuadraticMap.Equivalent`, real `-1/0/1` diagonalization, and matrix/quadratic-form transport APIs.
`IntakeProbe.lean` authenticates those interfaces. They strongly indicate a prospective exact
formal route but do not freeze or close the catalog's real-symmetric-matrix statement.

The provisional vector is `[H1, M3, R4]`: a complete human proof lead has unresolved source and
statement mapping; usable formal interfaces and closely related checked declarations exist, but no
exact catalog-to-Lean statement or matrix transport is credited; and no source-faithful readable
reconstruction has been accepted. `instance.json` is the structured scope authority and
`task-dag.json` keeps all six downstream phases open. No accepted receipt, `H0`, `M0`, `R0`, audit
completion, theorem completion, or master acceptance is claimed.
