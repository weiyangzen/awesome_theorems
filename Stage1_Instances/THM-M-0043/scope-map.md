# Scope map

## Received claim

The repository supplies the title "spectral theorem" and only the gloss "normal matrices are
unitarily diagonalizable." Intake preserves that finite matrix family. It does not silently select
a scalar field, theorem orientation, or Lean expression that the source did not state.

## Candidate mathematical boundary

A standard complex-matrix reading would include all of the following, still subject to a pinpoint
source and checked formal transport:

- a finite index type `n` and a square matrix `A : Matrix n n ℂ`;
- normality in the sense `star A * A = A * star A`, up to the chosen equivalent orientation;
- a unitary matrix `U`, with the exact left/right inverse convention fixed;
- a diagonal matrix `D` over `ℂ`; and
- an equality such as `A = U * D * star U` or `star U * A * U = D`, linked by a checked
  equivalence rather than treated as identical text.

The catalog's word "unitarily" strongly suggests complex scalars, but the field is not explicit.
The statement phase must not infer it without source admission.

## Decisions required at statement freeze

1. Preserve and independently review an immutable primary or authoritative source passage, with
   edition, theorem/page, definitions, assumptions, conclusion, proof boundary, and errata.
2. Resolve the unverified Hilbert/1906 attribution separately from the truth of the modern theorem.
3. Fix complex scalars or another source-specified `RCLike` domain. Real normal matrices do not in
   general admit real orthogonal diagonalization.
4. Fix the finite dimension or index type, nonemptiness convention, decidable equality, matrix
   multiplication orientation, and conjugate-transpose operation.
5. Freeze the normality predicate and the unitary predicate, including whether one or both product
   equations are used and which follow from finite-dimensionality.
6. Freeze the conclusion's witnesses, quantifier order, diagonal encoding, eigenvalue enumeration,
   conjugation orientation, and whether the result is one direction or an equivalence.
7. Elaborate the exact expression with minimal pinned imports and mutation-test removed normality,
   a changed scalar domain, changed binder scope, and the zero-dimensional boundary.

## Degenerate and boundary cases

No case is excluded at intake. Source review must resolve an empty index type, a zero-by-zero
matrix, the zero and identity matrices, repeated eigenvalues, singular normal matrices, real normal
matrices with nonreal eigenvalues, and whether eigenvalue order or diagonal witness uniqueness is
part of the result. A conclusion that assumes an eigenbasis, diagonalization, or unitary conjugator
as data would be circular.

## Neighbor and substitution exclusions

- `THM-M-0313` is the functional-analysis normal-operator spectral-decomposition target. A
  projection-valued measure, multiplication representation, or infinite-dimensional functional
  calculus statement does not replace this finite matrix target.
- `THM-M-0314` is the compact self-adjoint operator theorem and is not this target.
- `THM-M-0044` is singular value decomposition; two unitary factors for an arbitrary matrix are
  not a unitary similarity diagonalization of a normal square matrix.
- `Matrix.IsHermitian.spectral_theorem` and the legacy wrapper for `THM-M-1524` handle Hermitian
  matrices. They are strict specializations, not a normal-matrix root.
- The real spectral theorem for self-adjoint matrices is not a substitute for the complex normal
  theorem.
- Jordan form, Schur triangularization, diagonalizability by an arbitrary invertible matrix,
  eigenvalue existence, and continuous functional calculus are related but do not alone prove the
  received claim.
- The catalog's `已验证` label and the intake API probe supply no proof credit.

No canonical Lean expression, statement fingerprint, checked transport, mutation result, proof
body, obligation registry, or typed proof graph is frozen at intake.
