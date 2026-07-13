# Source-statement crosswalk

## Repository source identity

The originating record is `Docs/researches/math_theorems.md:377-382`, introduced by commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It names James Sylvester, gives 1852, and states
`实对称矩阵正负惯性指数在合同下不变`. It has no citation, formula, dimension, definition,
assumption, proof, errata record, or formal artifact. `Docs/Stage0_Blueprint.md:1483-1508` repeats
the gloss while explicitly leaving exact premises, proof, equivalent statements, foundations, and
machine status open. Therefore the catalog's `已验证` label supplies no assurance credit.

## Inspected human source leads

Sergei Treil, *Linear Algebra Done Wrong* (2017), Chapter 7, Section 3, printed pages 206-208,
was inspected from the author-hosted PDF at
`https://www.math.brown.edu/streil/papers/LADW/LADW_2017-09-04.pdf` (observed 2026-07-13,
SHA-256 `d4659dd7b1c1f9d6a8f78cda7a636354d191eb8a8cbd40f12042d59e83c4074f`). The section says
that for a Hermitian matrix and any invertible diagonalization `D = S* A S`, the positive,
negative, and zero diagonal counts depend only on `A`. Theorem 3.1 identifies positive and negative
counts with maximal dimensions of positive and negative subspaces; Lemma 3.2 and the proof on
pages 207-208 establish the dimension comparison and transport through `S`.

The historical primary-source lead is J. J. Sylvester, "A demonstration of the theorem that every
homogeneous quadratic polynomial is reducible by real orthogonal substitutions to the form of a
sum of positive and negative squares," *Philosophical Magazine*, series 4, volume 4, issue 23
(1852), pages 138-142, DOI `10.1080/14786445208647087`. Only bibliographic metadata was
inspected; the text and proof were unavailable. Its title supports a classification lead, not an
accepted arbitrary-congruence uniqueness crosswalk.

Neither source is accepted as `H0`: the catalog cites neither, the historical proof was not
inspected, and the modern Hermitian diagonalization statement still needs an approved real
specialization, arbitrary-congruence derivation, correction/errata audit, and independent review.

## Clause crosswalk

| Catalog clause | Human-source lead | Prospective Lean surface | Unresolved gate |
|---|---|---|---|
| real symmetric matrix | Treil's real specialization of Hermitian `A = A*` | `A : Matrix i i Real`, `Matrix.IsSymm A` | index type, binders, bundled/unbundled symmetry, source-ratified specialization |
| congruence | Treil uses invertible `D = S* A S` and transports definite subspaces through `S` | `Matrix.toQuadraticMap'`, `QuadraticMap.toMatrix'_comp`, `QuadraticMap.Equivalent` | exact equation orientation and invertible witness; bridge for arbitrary congruent `A,B` |
| positive inertia index | Treil Theorem 3.1: maximal positive-subspace dimension equals positive diagonal count | `QuadraticForm.sigPos`, `Equivalent.sigPos_eq`, `sigPos_of_equiv_weightedSumSquares` | choose maximal-dimension, diagonal-count, or eigenvalue-count definition and prove transports |
| negative inertia index | Treil Theorem 3.1 and the analogous negative argument | `QuadraticForm.sigNeg`, `Equivalent.sigNeg_eq`, `sigNeg_of_equiv_weightedSumSquares` | same definition and transport issue; source leaves one analogous detail to the reader |
| invariant | sign counts do not depend on diagonalization; proof identifies intrinsic maxima | conjunction of equalities for `sigPos` and `sigNeg` | exact matrix theorem and composition from congruence to equivalence are not frozen |
| zero index | Treil's section statement includes zero count, while the catalog names only positive/negative | radical finrank or fixed-dimension consequence | decide explicit triple versus derived nullity and cover degenerate cases |

## Pinned formal crosswalk

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.LinearAlgebra.QuadraticForm.Signature` defines `sigPos` and `sigNeg` as maximal definite
subspace dimensions and proves their equality under `QuadraticMap.Equivalent`. Its weighted-sum
theorems compute positive and negative counts. `Mathlib.LinearAlgebra.QuadraticForm.Real` proves
existence of a real `-1/0/1` form. `QuadraticForm.Basic` supplies the matrix map and congruence
formula. The pinned `Real.lean` module-level prose appears to swap the nondegenerate theorem names,
so declaration types, not that prose, must govern downstream work.

The repo-local `AwesomeTheorems.Stage1.S1_M_067.realLocalQuadraticClassification_anchor` wraps
only the real diagonalization declaration for another target's local leaf and explicitly limits its
scope. It is discovery input, never inherited status.

## Freeze decision

The crosswalk supports `[H1, M3, R4]`, not an exact target. The statement phase must select and
independently review a source proposition, freeze every binder and boundary case, elaborate the
matrix statement, and kernel-check all claimed transports before any located declaration can be
credited. Source edition/errata review, canonical expression and environment fingerprints,
mutation tests, proof provenance, and master acceptance remain open.
