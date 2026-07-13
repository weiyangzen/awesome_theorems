# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:391-396` supplies exactly the title
`潘罗斯-穆尔广义逆`, attribution to Roger Penrose and Eliakim Moore, year 1955, the gloss
`任意矩阵的广义逆存在唯一` ("every matrix has a unique generalized inverse"), high importance,
and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
definition of generalized inverse, scalar field, dimensions, ordered binders, exact assumptions,
proof boundary, correction history, or reviewer.

`Docs/Stage0_Blueprint.md:1537-1562` repeats the gloss while leaving the target formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted
metadata and resets this target to `L0 / rework_required`.

## Inspected primary source lead

R. Penrose, *A generalized inverse for matrices*, *Proceedings of the Cambridge Philosophical
Society* 51(3) (1955), printed pages 406-413, DOI `10.1017/S0305004100030401`, was inspected from
the publisher-served eight-page PDF on 2026-07-13. The observed PDF SHA-256 is
`cec01678759dbde2759e1881fc931a0d4f704cbad33033c3b2ab8fb992992a36`.

- The opening paragraph says the unique generalized inverse exists for every possibly rectangular
  matrix with complex entries.
- The notation paragraph makes capital letters arbitrary complex matrices and `A*` conjugate
  transpose.
- Theorem 1 on printed page 406 states that four displayed equations have a unique solution for
  every `A`: `A X A = A`, `X A X = X`, `(A X)* = A X`, and `(X A)* = X A`.
- The proof on printed pages 406-407 derives existence using a polynomial relation in `A* A` and
  proves uniqueness by comparing two solutions. It notes that `A` need not be square and may be
  zero.

This is a complete primary proof lead, but it is not yet `H0`. The repository catalog does not cite
the article; the exact OCR-to-symbol transcription and all implicit finite-matrix conventions need
independent verification; no immutable repository-owned source packet, errata/correction audit, or
reviewer acceptance exists; and the compound Moore-Penrose name and joint Moore attribution have
not been reconciled with a pinpoint Moore source.

Crossref metadata independently matches the article title, author, journal, volume 51, issue 3,
July 1955, pages 406-413, and DOI. That metadata supports bibliographic identity only and is not
proof evidence.

## Clause crosswalk

| Catalog component | Penrose 1955 component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "every matrix" | every possibly rectangular complex matrix | `A : Matrix (Fin m) (Fin n) Complex` or finite index types | finite dimensions are implicit; exact binders and universes open |
| "generalized inverse" | unique solution `X` to four equations | transposed-shape `X : Matrix (Fin n) (Fin m) Complex` | definition must be approved and encoded, not inferred from the name |
| first equation | `A X A = A` | rectangular matrix multiplication and equality | source transcription and association convention require review |
| second equation | `X A X = X` | rectangular matrix multiplication and equality | source transcription and association convention require review |
| third equation | `(A X)* = A X` | `Matrix.conjTranspose`; Hermitian `A * X` | exact notation and import surface open |
| fourth equation | `(X A)* = X A` | `Matrix.conjTranspose`; Hermitian `X * A` | exact notation and import surface open |
| "exists" | constructive finite-dimensional algebra proof | `ExistsUnique` or separated existence and uniqueness | exact Lean root and foundation profile open |
| "unique" | direct comparison of arbitrary solutions | uniqueness field of `ExistsUnique` | no uniqueness proof body or formal candidate located |
| attribution | Penrose article; Moore only in catalog compound attribution | source provenance records | Moore source and historical relationship uninspected |

## Pinned Lean crosswalk

| Required role | Pinned declaration or source | Boundary |
|---|---|---|
| rectangular matrices and multiplication | `Matrix`, `HMul.hMul` through matrix instances | substrate only |
| conjugate transpose | `Matrix.conjTranspose` | definition only |
| adjoint involution and products | `Matrix.conjTranspose_conjTranspose`, `Matrix.conjTranspose_mul` | adjacent identities only |
| Hermitian square products | `Matrix.isHermitian_mul_conjTranspose_self`, `Matrix.isHermitian_conjTranspose_mul_self` | adjacent facts only |
| ordinary inverse comparison | `Matrix.mul_nonsing_inv`, `Matrix.nonsing_inv_mul` | square invertible special case, not the root |
| pseudoinverse construction | no declaration found by bounded search | M4; anchor audit remains open |

`Mathlib.LinearAlgebra.Matrix.NonsingularInverse` explicitly states that it does not consider the
more general pseudoinverses for nonsquare or non-full-rank matrices. The absence search is scoped
discovery evidence, not a global nonexistence claim.

## Gate assessment

The source lead supports provisional `H1`: a primary complete theorem and proof were inspected, but
exact catalog identity, incorporated conventions, corrections, preservation, Moore attribution, and
independent review remain open. It cannot support `H0`, a canonical statement fingerprint, or proof
credit. The statement phase must approve one exact source proposition and then produce a checked
source-to-Lean transport without weakening any of the four equations or adding rank assumptions.
