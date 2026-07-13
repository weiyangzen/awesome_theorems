# Scope map

## Received claim

- Target: `THM-M-0056`, Weyl's inequality.
- Catalog gloss: perturbation theory for eigenvalues of Hermitian matrices.
- Attribution and date: Hermann Weyl, 1912.
- Intake boundary: a recognizable theorem family, but not a binder-complete truth-valued claim.

## Candidate readings, not selected

For eigenvalues listed in decreasing order, familiar finite Hermitian-matrix readings include:

1. The upper additive family
   `lambda_(i+j-1)(A+B) <= lambda_i(A) + lambda_j(B)` for admissible positive indices.
2. The lower companion
   `lambda_(i+j-n)(A+B) >= lambda_i(A) + lambda_j(B)` when its index is admissible.
3. The conjunction of the complete upper and lower families.
4. The perturbation corollary
   `abs(lambda_i(A+B) - lambda_i(A)) <= operatorNorm(B)` for every eigenvalue index.
5. The two-matrix form
   `abs(lambda_i(A) - lambda_i(B)) <= operatorNorm(A-B)`.

These are mathematical discriminators only. None is the canonical statement at intake.

## Proposition-changing decisions for the statement phase

1. Select and independently approve an immutable source proposition, including its complete proof
   boundary, rather than inferring a formula from the title.
2. Reconcile Weyl's 1912 symmetric-integral-kernel Satz I with the catalog's finite Hermitian-matrix
   wording and justify any specialization, translation, or modern replacement.
3. Select the upper family, lower family, conjunction, endpoint formulation, or norm-perturbation
   corollary. Do not broaden one into the others without checked implications.
4. Fix real symmetric versus complex Hermitian matrices, matrix dimension, index type, universes,
   and `Fintype` and `DecidableEq` data.
5. Fix decreasing or increasing eigenvalue enumeration, multiplicity semantics, and the transport
   between mathlib's `eigenvalues0 : Fin (card n) -> Real` and any alternate indexing.
6. Encode admissible index arithmetic without hidden one-based/zero-based conversion or overflow.
7. For a perturbation statement, fix the matrix/operator norm and its transport through the
   Euclidean-space matrix-to-linear-map interface.
8. Decide whether both matrices must be Hermitian and record why their sum or difference satisfies
   the required hypothesis.
9. Resolve zero dimension, singleton dimension, repeated eigenvalues, endpoints, zero perturbation,
   and scalar, singular, positive-semidefinite, indefinite, and commuting matrices.
10. Freeze ordered binders, hypotheses, conclusion, foundation/TCB/computation profiles, exact Lean
    expression, environment fingerprint, checked alternate transports, and statement mutations.

## Cases that remain in scope

- Zero and singleton dimensions until a source explicitly excludes them.
- Repeated eigenvalues, counted with the selected multiplicity convention.
- Zero, scalar, singular, positive-semidefinite, and indefinite Hermitian matrices.
- Zero perturbations and endpoint indices.
- Commuting and noncommuting pairs.
- Real symmetric matrices only through a source-approved checked transport if the root is complex.

No case is excluded at intake.

## Explicit exclusions

- Weyl's asymptotic spectral law, Weyl's criterion, and essential-spectrum results.
- Weyl groups, root systems, chambers, and the Weyl character formula.
- Singular-value Weyl inequalities, Hoffman-Wielandt, Lidskii, Schur-Horn, Cauchy interlacing, or
  Loewner monotonicity as substitutes for the selected root.
- The spectral theorem or reality of Hermitian eigenvalues alone.
- Arbitrary normal, nonsymmetric, infinite-dimensional, fixed-size, or commuting-only variants.
- Numerical eigensolvers, experiments, oracles, or unchecked certificates.
- A hypothesis, structure field, or axiom that stores the desired inequality.
- Proof or source credit transferred from `THM-M-0055`, `THM-M-0057`, `THM-M-0058`, or the distinct
  Weyl asymptotic-law target `THM-M-1389`.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the matrix spectrum API
provides decreasing `Matrix.IsHermitian.eigenvalues₀`, its antitonicity, an eigenvector basis,
diagonalization, and spectrum identification. The Rayleigh API provides quotient addition, a norm
bound, and a symmetric-operator norm characterization. A bounded exact-topic and minimax search
found no terminal Weyl inequality, eigenvalue perturbation declaration, or indexed Courant-Fischer
theorem. These are intake discovery observations, not an exhaustive anchor audit or M0 evidence.

The statement node may retry only after all source, variant, domain, index, norm, and boundary
choices above are approved. It must then elaborate exactly that claim with minimal pinned imports,
record expression and environment fingerprints, check credited alternate encodings, and mutation-
test hypotheses, domains, binder scope, index boundaries, and degenerate cases.
