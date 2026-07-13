# THM-M-1451 scope map

## Preserved theorem family

The intake preserves the QR eigenvalue-iteration family indicated by the catalog. In its basic
unshifted form, a square matrix sequence satisfies

```text
A_0 = A,
A_(k-1) = Q_k R_k,
A_k = R_k Q_k,
```

where each `Q_k` is unitary/orthogonal and each `R_k` is upper triangular under a selected QR
convention. This is a method-family description, not the canonical statement.

## Proposition-changing decisions

The statement phase must obtain an approved source and fix all of the following:

1. Choose the exact conclusion: recurrence well-definedness, one-step spectral invariance,
   cumulative similarity, Hessenberg preservation, convergence, rate, termination, backward
   stability, or end-to-end eigenvalue correctness.
2. Choose real or complex scalars and arbitrary, normal, Hermitian/symmetric, diagonalizable,
   Hessenberg, nonsingular, or another source-specified square-matrix class.
3. Define the QR factorization convention, including rank assumptions, diagonal phases/signs,
   uniqueness, and how a factor is selected when the factorization is not unique.
4. Select unshifted, single-shift, double-shift, implicit Francis, deflating, or another algorithm;
   specify the shift rule and exceptional-shift behavior.
5. If convergence is claimed, fix eigenvalue separation or other hypotheses, the ordering and
   repeated/equal-modulus cases, diagonalizability/Jordan restrictions, and generic overlap between
   the initial coordinate flag and invariant/eigenvector flags (often expressed through nonzero
   leading minors). Also fix topology/norm, upper-triangular versus real quasi-triangular endpoint,
   convergence of iterates and/or accumulated unitary factors, and rate/uniformity.
6. Distinguish exact-field mathematics from floating-point arithmetic, rounding, overflow,
   stopping tolerances, backward error, and any computation/certificate policy.
7. Freeze all ordered binders, dimensions, hypotheses, conclusions, universes, minimal imports,
   degenerate cases, and checked transports to equivalent encodings.

These choices change the proposition and its proof architecture. Intake does not infer them from
the phrase "QR iteration for eigenvalues" or the untrusted status label.

## Boundary cases

Source review must decide dimension zero and one, the zero and identity matrices, singular and
rank-deficient iterates, already triangular matrices, nonunique QR factorizations, repeated
eigenvalues, equal eigenvalue magnitudes, zero eigenvalues, complex-conjugate pairs in a real
formulation, stalled or exceptional shifts, deflation at an exact zero subdiagonal, and finite
precision breakdown. The unconditional identity `A_k = Q_k^* A_(k-1) Q_k` must not be advertised
as convergence in any of these cases.

## Excluded substitutions

- QR factorization existence alone is an ingredient, not QR iteration correctness or convergence.
- `charpoly (Q * R) = charpoly (R * Q)` proves a one-step invariant, not convergence or numerical
  stability.
- Schur decomposition proves existence of a triangular form, not that an iteration reaches it.
- Power, Lanczos, Arnoldi, Jacobi, inverse, or Rayleigh-quotient iteration cannot replace QR.
- A proof only for symmetric, normal, distinct-modulus, invertible, fixed-size, or unshifted input
  cannot close a broader root unless that restriction is source-frozen.
- A finite numerical run, residual plot, floating-point experiment, or assumed factor sequence is
  not exact theorem evidence.
- The catalog's `已验证` label, a matching name, or a successful API probe supplies no H or M credit.

## Neighbor boundaries

`THM-M-0046` and `THM-M-1448` own QR factorization theorem families, not the iterative eigenvalue
algorithm. `THM-M-1450` owns power iteration, `THM-M-1452` Lanczos, and `THM-M-1453` Arnoldi.
Their sources, artifacts, status, and proof credit are not inherited. Schur decomposition is a
possible endpoint specification but cannot substitute for an algorithm theorem.

## Downstream handoff

The statement phase must admit and independently review a pinpoint source, select one exact root,
then elaborate it with a normalized expression/environment fingerprint and the required mutations
and transports. Only later phases may exhaustively audit formal anchors, freeze the obligation and
typed-graph registries, implement proof bodies, or claim kernel closure.
