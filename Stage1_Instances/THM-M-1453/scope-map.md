# THM-M-1453 scope map

## Preserved method family

The intake preserves the finite-dimensional Arnoldi family named by the catalog: starting from a
nonzero vector, repeatedly apply a square linear operator and orthogonalize to construct a basis of
a Krylov subspace, an upper-Hessenberg projected operator, and Ritz approximations to eigenvalues.
This is a scope description, not a frozen theorem.

The inspected Netlib chapter describes Arnoldi both as the original direct reduction of a general
matrix to upper-Hessenberg form and as an iterative eigenvalue-approximation technique for large
sparse non-Hermitian matrices. Its basic-algorithm section states multiple mathematical relations,
not one canonical target. An accepted statement must select an exact correctness boundary rather
than merging construction, projection, exact-breakdown, approximation, convergence, and numerical
stability claims.

## Proposition-changing decisions

An independently reviewed source correction must decide all of the following:

1. The coefficient domain (`Real`, `Complex`, or a sourced abstraction), inner-product convention,
   and whether "nonsymmetric" means non-Hermitian or merely that symmetry is not assumed.
2. The finite dimension and ordered indices for the square operator, Krylov vectors, basis matrix,
   and Hessenberg matrix, including relations between the iteration count and ambient dimension.
3. The starting vector, its nonzero or unit-norm hypothesis, normalization, and the exact definition
   of the order-`m` Krylov subspace.
4. Classical Gram-Schmidt, modified Gram-Schmidt, Householder orthogonalization, reorthogonalization,
   or an abstract exact-arithmetic orthogonalization relation.
5. The recurrence coefficients and normalization convention, including conjugation orientation and
   whether the basis is stored as vectors, an isometry, or a rectangular matrix.
6. The zero-residual/breakdown policy: exclude it, stop early, or state the invariant-subspace and
   exact-Ritz conclusion when it occurs.
7. The target conclusion: orthonormal Krylov basis, entrywise recurrence, matrix Arnoldi relation,
   projected Hessenberg identity, Ritz residual formula, exactness, convergence, or a conjunction.
8. For an approximation theorem, which eigenvalues or invariant subspaces are approximated, the
   ordering/selection rule, error metric, spectral hypotheses, tolerance, and quantitative bound.
9. Exact versus floating-point arithmetic, rounding model, loss of orthogonality, stability, and
   whether restarting, shifts, deflation, or implementation complexity belongs to the root.
10. The ordered binders, universes, hypotheses, equality orientation, checked alternate encodings,
    foundation/TCB profiles, and every boundary case.

## Boundary cases

The statement phase must resolve dimension zero and one; iteration count zero, one, or larger than
the ambient dimension; a zero or already normalized starting vector; the zero, identity, scalar,
diagonal, Hermitian, defective, or nondiagonalizable matrix; early and final-step breakdown;
repeated eigenvalues; nontrivial Jordan blocks; a Krylov subspace of deficient dimension; zero
subdiagonal Hessenberg entries; real matrices with complex eigenvalues; empty Ritz spectra; and
exact versus finite-precision arithmetic.

## Excluded substitutions

- Gram-Schmidt orthogonalization or span preservation alone is an ingredient, not an Arnoldi
  recurrence, Hessenberg relation, or eigenvalue-approximation theorem.
- Existence of an arbitrary Hessenberg or Schur reduction does not show that the iterative Arnoldi
  construction produces it from the selected start vector.
- Lanczos iteration (`THM-M-1452`) is a symmetry-specialized neighbor and cannot silently replace
  the general non-Hermitian target.
- QR factorization, the QR eigenvalue algorithm, GMRES, power iteration, or a characteristic-
  polynomial theorem is not Arnoldi iteration.
- Ritz values without a source-selected residual, exactness, or convergence conclusion do not prove
  the catalog's unspecified eigenvalue gloss.
- A structure or hypothesis storing the desired basis, recurrence, approximation, convergence, or
  stability result supplies no proof.
- Numerical examples, benchmark residuals, source-code execution, a theorem-name match, API checks,
  and the untrusted `已验证` label supply no source or machine-proof credit.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, Gram-Schmidt has checked
orthogonality, span-preservation, nonvanishing-under-independence, and normalized orthonormality
results. Linear maps have matrix representations compatible with application, composition, and
powers. A bounded search found no Arnoldi-, upper-Hessenberg-, or matrix-Krylov-subspace-named
terminal theorem in pinned mathlib or the repository's Lean sources. The probe is bounded intake
discovery, not the downstream exhaustive anchor audit, and unrelated PDE occurrences of "Krylov"
are not candidates for this numerical-linear-algebra target.
