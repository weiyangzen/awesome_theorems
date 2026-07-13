# THM-M-0060 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item named the Smith
normal form theorem. The repository attributes it to Henry John Stephen Smith in 1861, describes it
only as `整数矩阵的等价标准形` (an equivalent normal form of integer matrices), and labels it
verified. The label is untrusted inventory metadata, not an exact source statement or proof
evidence.

## Planned boundary

The usual modern theorem family says that a rectangular matrix over a principal ideal domain can
be diagonalized by invertible row and column changes, often with nonzero diagonal entries arranged
in a divisibility chain; over the integers, signs can be normalized. The catalog does not specify
matrix dimensions, the meaning of equivalence, diagonal and divisibility conventions, existence
versus uniqueness, rank and zero cases, or whether the intended claim is matrix-level or the
equivalent submodule/module structure statement. Intake records that family without selecting any
one variant as the canonical root.

Smith's 1861 paper *On systems of linear indeterminate equations and congruences* is a strong
primary-source lead matching the catalog attribution and year. Bibliographic metadata and its
abstract were inspected, but no immutable theorem passage, complete proof boundary, corrections,
or errata were admitted and independently reviewed. It supports `H1`, not `H0`.

Pinned mathlib contains substantive Smith-normal-form infrastructure in
`Mathlib.LinearAlgebra.FreeModule.PID`. `IntakeProbe.lean` authenticates the basis/submodule
structure and existence APIs. That formalization is over a PID and expresses diagonalization of a
submodule inclusion through bases; its `SmithNormalForm` structure has no divisibility-chain or
integer sign-normalization field. No checked crosswalk currently identifies it with the
underspecified integer-matrix catalog root. It is therefore an `M3` formal interface/shape lead,
not root proof credit.

The provisional vector is `[H1, M3, R4]`. All six downstream tasks remain open. No canonical Lean
expression, accepted execution state, `H0`, `M0`, `R0`, audit completion, theorem completion, or
master acceptance is claimed.
