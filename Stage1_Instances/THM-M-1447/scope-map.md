# Scope map

## Frozen catalog boundary

The repository record names `Cholesky分解` and says only `对称正定矩阵的分解`. It attributes the
entry to Andre-Louis Cholesky in 1910 and labels it verified. The label is explicitly untrusted in
the rev-5.6 target manifest. The record has no citation, formula, definition chain, binders,
hypotheses, conclusion, proof boundary, correction record, or reviewer.

Consequently this intake freezes a theorem family, not a completed proposition. No canonical
statement, ordered binder, hypothesis, conclusion, formal expression, alternate encoding, or
excluded boundary case is selected.

## Proposition-changing choices

A source-approved statement must decide all of the following together:

- real symmetric matrices versus complex Hermitian matrices or a more general ordered star field;
- square matrices indexed by `Fin n` versus another finite linearly ordered index type;
- the precise positive-definiteness predicate and its relationship to symmetry/Hermitian symmetry;
- lower factorization `A = L * Lᵀ` or `A = L * Lᴴ` versus an upper orientation such as
  `A = Uᵀ * U` or `A = Uᴴ * U`;
- the exact lower/upper triangular predicate and multiplication orientation;
- strictly positive, nonnegative, phase-normalized, or unrestricted diagonal entries;
- existence alone versus uniqueness under a positive-diagonal normalization;
- zero and one dimensions and all other boundary conventions.

## Candidate family, not credited

The familiar real theorem says that each finite symmetric positive-definite matrix has a lower
triangular factor with positive diagonal and equals that factor times its transpose, often uniquely.
The complex theorem replaces symmetry and transpose by Hermitian symmetry and conjugate transpose.
Upper-triangular orientations are equivalent only after checked transpose/conjugate-transpose
transport. These are candidates for source selection, not this intake's canonical claim.

Netlib's LAPACK Users' Guide section 2.3.4 is an inspected authoritative lead for the real/complex
and upper/lower computational factorization family. It is not a catalog citation or an accepted,
independently reviewed source crosswalk and does not by itself freeze the exact Lean theorem.

## Excluded substitutions

- LU, LDU, QR, singular-value, Schur, spectral, polar, or Jordan decomposition is not Cholesky.
- A positive-semidefinite or rank-deficient Gram factorization cannot replace the positive-definite
  theorem without a source-selected statement and exact transport.
- A positive square root need not supply the requested triangular factor or normalization.
- `Matrix.PosDef.isUnit`, diagonal positivity, Schur-complement lemmas, an `LDLᴴ` decomposition, or
  one implication from a factor to positive definiteness does not construct a normalized `LLᴴ`
  Cholesky factor.
- A numerical routine, floating-point residual, successful algorithm run, or unchecked certificate
  is not an exact existence proof.
- A structure or hypothesis already storing the desired factor supplies no proof.
- The catalog's `已验证` label and successful `#check` commands give no H or M credit.

## Neighbor boundaries

`THM-M-1446` owns LU decomposition, `THM-M-1448` QR decomposition, and `THM-M-1449` singular-value
decomposition. Their statements and evidence cannot be transferred. Earlier algebra targets
`THM-M-0046` and `THM-M-0047` separately own QR and LU theorem families; any duplicate reconciliation
is an independently accepted identity task, not intake proof credit.

## Cases still open

The statement phase must resolve empty indices, dimension one, real versus complex scalars, zero and
identity matrices, singular and merely positive-semidefinite matrices, lower versus upper factors,
positive-diagonal normalization, uniqueness, and all coercion and ordering conventions. No case is
silently excluded now.
