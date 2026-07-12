# Scope map

## Received claim

The repository supplies the title "spectral theorem" and the gloss "normal matrices are unitarily
diagonalizable." The statement gate selects the finite complex matrix reading fixed by Axler,
*Linear Algebra Done Right*, fourth edition, Theorem 7.31, and preserves the catalog's one-way
normal-to-diagonal claim.

## Frozen mathematical boundary

The canonical target includes:

- a finite index type `n` and a square matrix `A : Matrix n n Complex`;
- normality through `IsStarNormal A`, whose field gives `star A * A = A * star A`;
- a subtype witness `U : Matrix.unitaryGroup n Complex`, carrying the unitary inverse equations;
- diagonal entries `d : n -> Complex`; and
- the equality `A = U * Matrix.diagonal d * star U`.

Axler explicitly fixes complex scalars. The checked theorem
`spectralTheoremTarget_iff_conjugatedDiagonalTarget` connects the canonical equality to
`star U * A * U = Matrix.diagonal d` rather than treating the orientations as definitionally equal.
The second checked transport expands the unitary subtype witness into matrix membership.

## Decisions frozen at statement

1. Scalars are `Complex`, not `Real` or an arbitrary `RCLike` domain.
2. `n : Type u` has `Fintype n`, `DecidableEq n`, and `Nonempty n`, matching Axler's standing
   convention that the space is nonzero.
3. `IsStarNormal A` is the sole mathematical antecedent.
4. The unitary witness uses `Matrix.unitaryGroup`, and the diagonal witness is `d : n -> Complex`.
5. The root is the catalog's implication, not Axler's stronger three-way equivalence.
6. Eigenvalue order and witness uniqueness are not part of the conclusion.
7. The historical Hilbert/1906 attribution and independent source review remain open on the human
   source axis and do not prevent freezing the modern theorem statement at `H1`.

## Degenerate and boundary cases

Empty `n` and the zero-by-zero matrix are excluded by `Nonempty n`. Zero and identity matrices in
positive dimension, repeated eigenvalues, and singular normal matrices remain included. The
changed-boundary mutation removes `Nonempty n` and is rejected as a term of the source-exact root.
The changed-domain mutation is broader than the complex source and is also rejected.

## Neighbor and substitution exclusions

- `THM-M-0313` is the functional-analysis normal-operator spectral-decomposition target. A
  projection-valued measure, multiplication representation, or infinite-dimensional functional
  calculus statement does not replace this finite matrix target.
- `THM-M-0314` is the compact self-adjoint operator theorem and is not this target.
- `THM-M-0044` is singular value decomposition; two unitary factors for an arbitrary matrix are not
  a unitary similarity diagonalization of a normal square matrix.
- `Matrix.IsHermitian.spectral_theorem` and the legacy wrapper for `THM-M-1524` handle Hermitian
  matrices. They are strict specializations, not a normal-matrix root.
- The real spectral theorem for self-adjoint matrices is not a substitute for the complex normal
  theorem.
- Jordan form, Schur triangularization, diagonalizability by an arbitrary invertible matrix,
  eigenvalue existence, and continuous functional calculus do not alone prove the root.
- The catalog's `已验证` label and the intake API probe supply no proof credit.

The canonical expression, two checked transports, and four statement mutations are frozen by
`Statement.lean` and `statement.json`. No proof body for the spectral theorem, obligation registry,
or typed proof graph is supplied by this phase.
