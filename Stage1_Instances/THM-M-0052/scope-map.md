# Scope map

## Received claim

- Target name: `潘罗斯-穆尔广义逆` (Moore-Penrose generalized inverse).
- Catalog gloss: `任意矩阵的广义逆存在唯一` ("every matrix has a unique generalized inverse").
- Attribution and date: Roger Penrose / Eliakim Moore, 1955.
- Intake interpretation: the theorem family is recognizable, but "generalized inverse" is undefined
  and the terse gloss alone is not a proposition that can be frozen or elaborated.

## Proposition-changing decisions for the statement phase

1. Select and independently approve a source proposition. Penrose's Theorem 1 is the current
   primary lead; the catalog does not cite it, and the joint Moore attribution requires review.
2. Decide whether the canonical root follows Penrose literally over finite rectangular complex
   matrices or includes a separately checked real-matrix formulation.
3. Fix row and column binders (`m n : Nat` with `Fin` indices or arbitrary finite types), their
   order, universes, and all `Fintype`/`DecidableEq` instances.
4. Define the candidate inverse shape. For an `m` by `n` matrix `A`, `X` must be `n` by `m` so all
   four equations type-check.
5. Transcribe and approve the four defining equations, conventionally `A X A = A`, `X A X = X`,
   `(A X)H = A X`, and `(X A)H = X A`, without reordering or weakening the source silently.
6. Fix `H` as conjugate transpose over `Complex` and document any transport to transpose over
   `Real` or to adjoints of finite-dimensional linear maps.
7. Decide whether the root is a direct `ExistsUnique`, uniqueness of a defined function, or an
   existence theorem plus a separate uniqueness theorem. Checked equivalences are required.
8. Resolve zero dimensions, zero matrices, rank-deficient matrices, full row/column rank, and the
   square invertible case rather than adding nonempty, rank, or invertibility premises.
9. Reconcile the catalog's compound name and joint attribution with the exact 1955 Penrose theorem
   and an inspected Moore source before accepting source identity.

## Degenerate cases that stay in scope

- `m = 0`, `n = 0`, and either dimension zero while the other is positive.
- The zero matrix of any selected finite rectangular shape.
- Square invertible matrices, where the selected object should agree with ordinary inverse.
- Square singular and genuinely rectangular rank-deficient matrices.
- Full row rank and full column rank specializations.

No case is excluded at intake. Exact witnesses and transports belong to the statement phase after
source approval.

## Explicit exclusions

- An arbitrary inner inverse satisfying only `A X A = A`; such witnesses are generally nonunique.
- A reflexive generalized inverse satisfying only the first two Penrose equations.
- Square nonsingular inverse theory, determinant inversion, or a fixed-size special case.
- SVD, polar decomposition, or Hermitian spectral decomposition without the four-equation root.
- Least-squares solvability or minimum-norm characterization alone.
- Approximate, floating-point, tolerance-dependent, or oracle-computed pseudoinverses.
- A structure field, premise, axiom, or certificate that assumes the desired inverse.
- Transfer of proof or source status from SVD or any neighboring target.

## Lean boundary

Pinned mathlib authenticates `Matrix.conjTranspose`, conjugate-transpose multiplication laws,
`Matrix.IsHermitian`, and determinant-based square inverses. The module documentation for
`Mathlib.LinearAlgebra.Matrix.NonsingularInverse` explicitly says pseudoinverses are not considered.
A bounded search of pinned mathlib and repo-local Lean found no Moore-Penrose or matrix
pseudoinverse declaration. These are discovery facts, not an exhaustive anchor audit or M0 evidence.

The statement node may retry only after source identity, definitions, binders, scalar domain,
adjoint convention, equation transcription, and boundary cases are independently approved. It must
then elaborate only that exact proposition, record the expression and environment fingerprints,
check any alternate encodings, and mutation-test domain, equation, binder, and boundary changes.
