# THM-M-0041 rev-5.6 intake

`THM-M-0041` is the Cayley-Hamilton theorem catalog item. The repository says that a matrix
satisfies its characteristic polynomial, attributes the result to William Hamilton and Arthur
Cayley in 1858, and labels it verified. That label is untrusted metadata, not human-source or
machine-proof evidence.

## Planned scope

This intake selects the conventional finite square-matrix claim for later source review: every
finite square matrix over a commutative ring is annihilated by its characteristic polynomial. The
conclusion means polynomial evaluation in the matrix algebra is the zero matrix. No field,
nontriviality, invertibility, diagonalizability, or nonempty-dimension hypothesis is added.

This selection preserves the catalog theorem family but does not pretend that the catalog supplied
the coefficient domain, index type, characteristic-polynomial convention, evaluation operation, or
empty-matrix boundary. The statement phase must ratify these choices against an admitted source and
freeze the exact elaborated Lean target.

## Source and formal boundary

Crossref metadata identifies Arthur Cayley's 1858 paper *A memoir on the theory of matrices*, DOI
`10.1098/rstl.1858.0002`, pages 17-37, and exposes an abstract containing the named claim. Intake did
not admit an immutable primary text, pinpoint the theorem and proof passage, reconcile the catalog's
joint Hamilton/Cayley attribution, inspect corrections, or obtain independent review. The lead is
therefore not `H0` evidence.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.LinearAlgebra.Matrix.Charpoly.Basic` contains the close candidate
`Matrix.aeval_self_charpoly`; `Mathlib.LinearAlgebra.Charpoly.Basic` contains the finite free-module
form `LinearMap.aeval_self_charpoly`. `IntakeProbe.lean` authenticates their types and reported axioms
with the pinned toolchain. Intake does not freeze an elaborated canonical declaration, establish a
source transport, audit terminal bodies or transitive trust, or credit proof closure.

The planned vector is `[H1, M3, R3]`: the theorem and historical lead are stable but the exact source
mapping is incomplete; exact formal interfaces are located but have not passed statement or anchor
audit; and this dossier maps scope without reconstructing the proof. All six downstream tasks remain
open. No accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
