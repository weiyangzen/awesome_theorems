# THM-M-1452 scope map

## Preserved repository scope

The repository identifies the Lanczos algorithm with computing eigenvalues of large sparse
matrices. This intake preserves that eigenvalue-algorithm family and its historical Lanczos
attribution. It does not infer a convergence theorem, a complexity theorem, or even one precise
exact-arithmetic invariant from the gloss.

## Proposition-changing decisions

An approved source correction must freeze:

- the scalar field (`Real`, `Complex`, or an admitted generalization), finite matrix dimensions,
  square shape, Hermitian/symmetric premise, and whether mathematical sparsity is a hypothesis or
  only an implementation concern;
- the start vector, its normalization and nonzero/cyclic assumptions, iteration count, indexing,
  Krylov subspace convention, exact three-term recurrence, coefficient orientation, and every
  denominator or normalization side condition;
- the breakdown policy when a residual norm vanishes, early termination, repeated eigenvalues,
  invariant subspaces, zero-dimensional and zero-matrix cases, and whether look-ahead or restart is
  excluded;
- the exact output and conclusion: orthonormal Lanczos vectors, span equality with a Krylov
  subspace, a tridiagonal compression, an intertwining/decomposition identity, exact recovery at
  termination, Ritz-value interlacing or approximation, residual bounds, convergence, or an exact
  conjunction;
- whether the theorem is full `n`-step tridiagonalization or a truncated `m`-step result, the
  quantifier order for `m` and `n`, and how unused columns or early termination are represented;
- exact versus finite-precision arithmetic, sparsity/storage and matrix-vector cost models,
  reorthogonalization, loss of orthogonality, ghost eigenvalues, stopping rules, error norms, and
  rounding assumptions; and
- alternate matrix/linear-map encodings, checked transport directions, logical profiles, all
  universes/typeclass context, and every boundary case.

These decisions yield inequivalent propositions. They are a resolution checklist, not a canonical
statement.

## Candidate families not credited

- Exact-arithmetic three-term recurrence for a Hermitian or real-symmetric matrix.
- Pairwise orthogonality of nonbreakdown Lanczos vectors.
- Equality between the generated span and a Krylov subspace.
- A partial relation such as `A * Q_m = Q_m * T_m + r_m e_m^*`, with `T_m` tridiagonal.
- Full tridiagonalization after termination in finite dimension.
- Ritz-value interlacing, residual estimates, or convergence toward extremal eigenvalues.
- A finite-precision, restarted, block, look-ahead, or reorthogonalized Lanczos theorem.

No family in this list is selected or credited at intake.

## Explicit exclusions

- Arnoldi iteration (`THM-M-1453`), GMRES (`THM-M-1454`), conjugate gradients
  (`THM-M-1455`), power iteration (`THM-M-1450`), or QR iteration (`THM-M-1451`).
- The unrelated diffusion-process and Krylov-Safonov uses of the name Krylov elsewhere in the
  repository.
- Hermitian spectral diagonalization by itself; it supplies eigenstructure but not the Lanczos
  construction or its invariants.
- Generic Gram-Schmidt orthogonalization by itself; it does not establish the three-term Lanczos
  recurrence or tridiagonal relation.
- A theorem that assumes the desired orthogonality, span equality, tridiagonal decomposition,
  convergence, residual estimate, or eigenvalue output as an unexplained field.
- A numerical run, sampled matrix, residual plot, benchmark, or floating-point experiment.
- The catalog label `已验证` as source, statement, kernel, or proof evidence.

## Degenerate and boundary ledger

No boundary case is excluded because no proposition is selected. Statement work must explicitly
decide the empty and one-dimensional index types, zero and scalar matrices, zero or eigenvector
starts, starts orthogonal to eigenspaces, invariant-subspace starts, repeated eigenvalues, exact
breakdown before the requested step, full-dimensional termination, vanishing recurrence
coefficients, sign/phase choices, and exact versus rounded arithmetic.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.Matrix.Spectrum` provides Hermitian eigenvalues, an eigenvector basis, an
eigenvector unitary, and the spectral theorem. `Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho`
provides orthogonalization, span preservation, linear independence, and triangular coefficient
facts. A bounded name/topic search found no Lanczos, Krylov-subspace, or tridiagonalization terminal
declaration for this target. This is intake discovery, not an exhaustive anchor audit or a global
absence result.
