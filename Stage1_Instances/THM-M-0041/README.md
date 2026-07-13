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
empty-matrix boundary. The statement phase below freezes these conventional repository-scope choices;
their primary-source fidelity remains open for independent review.

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
with the pinned toolchain. That historical intake snapshot did not freeze an elaborated canonical
declaration, establish a source transport, audit terminal bodies or transitive trust, or credit proof
closure; the statement handoff below supersedes only the canonical-elaboration part of that boundary.

## Statement phase handoff

`Statement.lean` now freezes the exact intake-selected target as
`Stage1Instances.THM_M_0041.CayleyHamiltonTarget`. It expands the characteristic polynomial as
`det (X I - A)` and uses only `Mathlib.Algebra.Polynomial.AlgebraMap` and
`Mathlib.LinearAlgebra.Matrix.Determinant.Basic`. This keeps the Cayley-Hamilton candidate
`Matrix.aeval_self_charpoly` module outside the statement boundary. `statement.json` records the
expression/environment fingerprints, a literal removed-hypothesis failure, three distinct
structural mutations, and concrete empty-index/zero-ring elaboration probes.

## Anchor and obligation handoff

`anchor-audit.json` classifies a bounded immutable candidate inventory. It checks the definitional
transport to `Matrix.charpoly` and an exact wrapper around pinned
`Matrix.aeval_self_charpoly`, while retaining M3 until release-grade E1 and master acceptance.

Registry v1 now freezes 17 canonical obligations and seven typed graph classes. The root proof
requires the exact characteristic-polynomial transport and pinned mathlib bridge. The imported
body is expanded, without duplicate proof credit, into adjugate construction, `matPolyEquiv`
normalization, right-factor evaluation, and scalar-evaluation conversion. `ObligationTree.lean`
checks the transport and conditional child composition but does not install an accepted proof.

The vector remains `[H1, M3, R3]`. No obligation is accepted closed. Pinpoint H0, independently
reviewed R0, release-grade E1, full provenance/trust, proof installation, hermetic and independent
validation, release, audit completion, and theorem completion remain open.
