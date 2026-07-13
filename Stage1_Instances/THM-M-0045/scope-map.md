# Scope map

## Received claim

The repository supplies the title "Schur decomposition theorem" and only the gloss "a complex
square matrix can be unitarily triangularized." Intake preserves that finite complex matrix
family. It does not silently choose a conjugation equation, an order on matrix indices, or a Lean
expression that the catalog does not state.

## Selected mathematical boundary

A modern matrix reading is frozen provisionally as follows, still subject to master acceptance and
independent source/transport review:

- a natural dimension `n` and `A : Matrix (Fin n) (Fin n) Complex`;
- a unitary matrix `U` under a fixed left/right star-inverse convention;
- upper triangularity under the canonical `Fin n` order, encoded by `Matrix.BlockTriangular _ id`;
- the conjugated matrix `star U * A * U`; and
- dimensions zero and one, without any normality or invertibility premise on `A`.

The alternate equation `A = U * T * star U` and the operator/orthonormal-basis formulation are not
credited without checked transports.

## Statement decisions and remaining review

1. Preserve and independently review a lawful primary or authoritative source passage with
   edition, theorem/page, definitions, assumptions, conclusion, proof boundary, and errata state.
2. Separate the truth of the modern theorem from the unverified details of the Schur/1909
   historical attribution.
3. Complex scalars, `Fin n`, the canonical order, and inclusion of zero dimension are now frozen in
   the worker statement proposal.
4. `Matrix.unitaryGroup`, matrix star, `star U * A * U`, and upper `BlockTriangular id` are now
   frozen in the worker statement proposal.
5. The target existentially returns only `U`; separate `T` and reconstruction equations remain
   uncredited alternates.
7. Register alternate operator/orthonormal-basis and matrix/unitary encodings only after a checked
   transport preserves all binders, assumptions, and boundary cases.
8. The statement self-test covers removed unitarity, changed scalar domain, changed matrix-binder
   scope, and exclusion of the zero-dimensional boundary.

## Degenerate and boundary cases

The statement includes:

- zero-by-zero and one-by-one matrices;
- zero, scalar, already triangular, diagonal, normal, and nilpotent matrices;
- singular and nonnormal matrices;
- repeated eigenvalues and defective matrices;
- defective and repeated-eigenvalue matrices, because no diagonalizability premise is present.

It selects upper triangular form on `Fin n`; lower triangular form and arbitrary finite index types
remain alternate encodings requiring checked transports.

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

The canonical declaration is `Stage1Instances.THM_M_0045.SchurTriangularizationTarget`, with
expression SHA-256 `275e1e43027f442607fc48e78ce4e189de66b328d39c61044e87a4c8f85c001b`.
The discovery probe remains interface-only. The statement module defines a proposition and
mutations, not an inhabitant. Anchor audit, obligation tree, proof, validation, and release remain
open.
