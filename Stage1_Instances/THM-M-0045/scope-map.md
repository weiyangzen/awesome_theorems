# Scope map

## Received claim

The repository supplies the title "Schur decomposition theorem" and only the gloss "a complex
square matrix can be unitarily triangularized." Intake preserves that finite complex matrix
family. It does not silently choose a conjugation equation, an order on matrix indices, or a Lean
expression that the catalog does not state.

## Candidate mathematical boundary

A standard matrix reading would include the following, all still subject to accepted source
transport:

- a natural dimension or finite linearly ordered index type and `A : Matrix n n Complex`;
- a unitary matrix `U` under a fixed left/right star-inverse convention;
- a matrix `T` upper triangular under a fixed row/column ordering; and
- a unitary-similarity equation such as `star U * A * U = T` or `A = U * T * star U`.

Those equations are mathematically interderivable using unitary inverse identities but are not
textually identical. They need a checked Lean transport after one is selected as canonical.

## Decisions required at statement freeze

1. Preserve and independently review a lawful primary or authoritative source passage with
   edition, theorem/page, definitions, assumptions, conclusion, proof boundary, and errata state.
2. Separate the truth of the modern theorem from the unverified details of the Schur/1909
   historical attribution.
3. Fix complex scalars, matrix dimension and index type, universes, finite-order and decidable
   equality instances, and whether zero dimension is included.
4. Fix the unitary predicate, star/conjugate-transpose operation, multiplication convention,
   conjugation orientation, and equality direction.
5. Fix upper versus lower triangular form and the order used by the triangular predicate; do not
   replace triangularity by diagonalizability or a block form.
6. Decide whether the theorem existentially returns only `U` with its conjugated matrix proved
   triangular, or separate witnesses `U` and `T` plus an equation.
7. Register alternate operator/orthonormal-basis and matrix/unitary encodings only after a checked
   transport preserves all binders, assumptions, and boundary cases.
8. Mutation-test complex versus real scalars, removed unitarity, reversed triangular orientation,
   altered conjugation order, and the empty-index boundary.

## Degenerate and boundary cases

No case is excluded at intake. The statement phase must explicitly decide:

- zero-by-zero and one-by-one matrices;
- zero, scalar, already triangular, diagonal, normal, and nilpotent matrices;
- singular and nonnormal matrices;
- repeated eigenvalues and defective matrices;
- upper versus lower triangular form after index-order reversal; and
- arbitrary finite types versus a canonical `Fin n` ordering.

## Non-substitution boundary

The target is not closed by any of the following alone:

- triangularizability with an arbitrary, nonorthonormal basis;
- eigenvalue existence or generalized-eigenspace spanning;
- a Gram-Schmidt theorem only about the basis-change matrix;
- the spectral theorem or unitary diagonalization restricted to normal or Hermitian matrices;
- Jordan canonical form, Jordan-Chevalley decomposition, QR decomposition, or singular-value
  decomposition;
- a fixed-dimension, diagonalizable-only, normal-only, nilpotent-only, or numerical case;
- a structure or hypothesis that already stores the desired unitary triangularization; or
- the catalog's untrusted status, a theorem-name search, or a successful API `#check`.

## Neighbor boundaries

`THM-M-0042` owns Jordan canonical form, `THM-M-0043` the spectral theorem, `THM-M-0044`
singular-value decomposition, and `THM-M-0046` QR decomposition. Those targets may supply future
dependencies only after exact statement and obligation freezes. No status or proof credit crosses
target boundaries by proximity.

## Formal boundary

No canonical Lean expression is frozen at intake. The discovery probe checks real pinned APIs for
eigenvalues, generalized eigenspaces, Gram-Schmidt, upper triangular matrices, unitary
change-of-basis matrices, and matrix representation. It defines no root theorem and contains no
proof body. The statement, anchor audit, obligation tree, proof, validation, and release nodes
remain open.
