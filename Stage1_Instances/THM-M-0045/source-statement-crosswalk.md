# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:342-347` supplies exactly the title `舒尔分解定理`, attribution to
Issai Schur, year 1909, the gloss `复方阵可酉三角化`, importance "high," and status `已验证`.
Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, theorem locator,
formula, definitions, ordered binders, assumptions, proof boundary, correction history, reviewer,
or formal artifact.

`Docs/Stage0_Blueprint.md:1348-1373` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets this target to `L0 / rework_required`.

## Inspected primary source lead

Issai Schur, "Über die charakteristischen Wurzeln einer linearen Substitution mit einer Anwendung
auf die Theorie der Integralgleichungen," *Mathematische Annalen* 66 (1909), 488-510, DOI
`10.1007/BF01450045`, was inspected through the GDZ public scan. The 24-page PDF (one terms page
plus printed pages 488-510) was observed on 2026-07-13 with SHA-256
`a32565f72b7ffa94806be14a96174ea716dc5265fd258b7caeb877ab91a5a488`.

- Section 1, printed page 489, defines `P'` as the conjugate transpose, displays `P'P = E`, and
  calls such a matrix unitary.
- Satz I, printed pages 490-492, says that for an arbitrary real or complex square matrix `A` one
  can choose a unitary `P` so that `P' A P` has the displayed triangular form. The display has
  zeros above the diagonal, hence lower triangular in that convention.
- The proof chooses a normalized eigenvector, completes it to a unitary matrix, reduces to an
  `(n-1)`-dimensional block, applies induction, and combines the unitary changes of basis.
- Satz I* on printed page 492 gives an equivalent invariant orthonormal linear-form formulation.

The GDZ scan is historically primary and materially confirms the theorem family, author, and year.
It does not yet support `H0`: the catalog narrows the domain to complex matrices, the source's
display is lower rather than upper triangular, formula OCR is imperfect, incorporated definitions
and translation have not been independently reviewed, and correction/errata plus lawful archival
and recovery policy remain open. The PDF was inspected read-only and was not added to the repo.

## Inspected authoritative modern source lead

Sheldon Axler, *Linear Algebra Done Right*, fourth edition, Section 6B, Theorems 6.37-6.38,
printed pages 203-204, author-hosted PDF observed on 2026-07-13, was inspected:

- Theorem 6.37 says that a finite-dimensional operator has an upper-triangular matrix with respect
  to some orthonormal basis iff its minimal polynomial splits into linear factors. Its proof begins
  with an arbitrary triangularizing basis and applies Gram-Schmidt; equality of every prefix span
  preserves the invariant-subspace flag.
- Theorem 6.38, labeled "Schur's theorem," says every operator on a finite-dimensional complex
  inner-product space has an upper-triangular matrix with respect to some orthonormal basis. Its
  proof invokes the fundamental theorem of algebra and Theorem 6.37.
- The text states that Issai Schur published a proof in 1909.

The observed PDF SHA-256 is
`45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`. This is an
author-hosted, mutable source lead and was not added to the repository. The catalog does not cite
it, and the theorem is phrased for operators and orthonormal bases rather than an explicit unitary
matrix equation. Pinpoint definition transport, immutable preservation or recovery, correction
audit, lawful archival policy, and independent review remain open. Thus it supports provisional
`H1`, not `H0`.

The primary and modern leads agree on unitary triangularization after accounting for transpose and
order conventions, but that agreement is not a checked mathematical or Lean transport.

## Clause crosswalk

| Repository component | Source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "complex square matrix" | operator on a finite-dimensional complex inner-product space | `Matrix n n Complex` or `Module.End Complex V` plus matrix representation | index type, universe, and matrix/operator transport open |
| "unitarily" | matrix in some orthonormal basis | `OrthonormalBasis`, `Matrix.unitaryGroup`, change-of-basis matrix | unitary witness and exact equation orientation open |
| "triangularized" | upper-triangular matrix in Theorems 6.37-6.38 | `Matrix.BlockTriangular T id` for an ordered finite index | upper/lower convention, order, and transported matrix open |
| existence theorem | every such complex operator admits the basis | existential orthonormal basis or unitary matrix plus triangular matrix | exact conclusion and zero-dimensional handling open |
| proof route | split minimal polynomial, triangularizing invariant flag, Gram-Schmidt | eigenvalue/invariant-subspace interfaces plus `InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular` | architecture lead only; no root composition credited |
| `已验证` | no cited source meaning | no declaration or proof body | rejected as evidence |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Module.End.exists_eigenvalue` provides eigenvalue existence for finite-dimensional nontrivial
  spaces over algebraically closed fields;
- `Module.End.iSup_maxGenEigenspace_eq_top` provides generalized-eigenspace spanning;
- `InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular` says the coefficient matrix of a basis relative
  to its Gram-Schmidt orthonormalization is upper triangular;
- `OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary` supplies the unitary property for a
  change of orthonormal bases; and
- `Matrix.BlockTriangular`, `LinearMap.toMatrix`, and `Matrix.unitaryGroup` supply prospective
  statement interfaces.

`IntakeProbe.lean` elaborates these exact declarations under the pinned environment. None has the
received theorem as its conclusion. In particular, Gram-Schmidt triangularizes the basis-change
matrix; it does not by itself prove that an arbitrary operator's matrix is triangular in that
basis. The generalized-eigenspace result does not construct an invariant flag and orthonormal
basis. A bounded exact-topic search found no exact Schur root in pinned mathlib or repo-local Lean.
That is intake discovery only, not an exhaustive external anchor or provenance audit.

## First source gate

The statement proposal selects Axler Theorem 6.38's finite complex upper-triangular form and maps it
to `Matrix (Fin n) (Fin n) Complex`, a unitary witness `U`, and
`Matrix.BlockTriangular (star U * A * U) id`. The exact expression elaborates and is mutation-tested
under pinned Lean; dimensions zero and one are checked. This freezes a provisional target while
keeping H1: the source edition is mutable, independent review and correction audit are open, and
the operator/orthonormal-basis to explicit matrix/unitary transport has not been accepted as a
checked alternate encoding. Schur's original lower-triangular convention is likewise untransported.
