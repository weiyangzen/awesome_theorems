# THM-M-0042 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the Jordan
canonical form theorem. The repository supplies the gloss "a complex matrix is similar to Jordan
normal form," attributes it to Camille Jordan in 1870, and labels it verified. Under rev-5.6 that
label is untrusted inventory metadata, not a source audit, an exact Lean proposition, or proof
evidence.

The gloss identifies a standard theorem family, but it does not define a Jordan block or Jordan
normal form, fix the matrix dimension and index type, state the similarity witness and conjugation
orientation, choose a block-order convention, or settle the zero-dimensional case. Intake does not
silently supply those proposition-changing clauses from memory.

Sheldon Axler's author-hosted *Linear Algebra Done Right*, fourth edition, was inspected as an
authoritative modern source lead. Definition 8.44 specifies Jordan bases, and Theorem 8.46 states,
under the chapter's finite-dimensional nonzero-space convention, that every complex linear
operator has such a basis. This strongly
disambiguates the intended family, but the catalog does not cite that edition, its operator/basis
statement still needs an approved transport to the matrix/similarity wording, and no independent
source review is recorded. It is therefore a lead, not `H0` evidence.

Pinned mathlib supplies generalized eigenspaces, invertible matrices, matrix representations of
linear maps, and a Jordan-Chevalley-Dunford decomposition. `IntakeProbe.lean` authenticates those
interfaces. A bounded search found no Jordan-block, Jordan-basis, or Jordan-normal-form declaration.
The Jordan-Chevalley theorem and generalized-eigenspace decomposition are ingredients or related
results, not substitutes for the requested canonical-form theorem.

The provisional vector is `[H1, M4, R4]`: a complete modern human proof source lead is known but
the exact source-to-catalog statement and assumptions are not accepted; no usable exact formal
artifact is credited; and no source-faithful proof reconstruction is available. `instance.json` is
the structured scope authority, while `task-dag.json` keeps all six downstream phases open. No H0,
M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
