# THM-M-1450 scope map

## Preserved repository scope

The repository identifies power iteration as an iterative method for a largest eigenvalue. This
intake preserves the standard dominant-eigenpair convergence family and its numerical-analysis
setting. It does not infer a particular matrix class, scalar field, recurrence, estimator, or
convergence conclusion from the untrusted `已验证` label.

## Proposition-changing decisions

An approved source correction must freeze:

- a finite matrix or a linear/continuous operator, scalar field, dimension and index types, norm
  and inner product, universes, topology, and all algebraic and analytic typeclass data;
- whether the operator is self-adjoint, normal, diagonalizable, positive, merely has a complete
  eigenbasis, or may have Jordan blocks, and whether arithmetic is exact or finite precision;
- the meaning of "largest": largest ordered eigenvalue, largest absolute value, a unique spectral-
  radius eigenvalue, or one dominant invariant subspace;
- strict dominance and multiplicity assumptions, including whether `|lambda_1| > |lambda_2|`,
  whether the dominant eigenvalue is nonzero and simple, and how ties by modulus are handled;
- a starting vector and its nonzero projection onto the dominant eigenspace, plus behavior for the
  zero vector or a vector orthogonal to that eigenspace;
- raw iterates `A^k z`, normalized iterates, normalization frequency and zero convention, sign or
  complex-phase alignment, iterate indexing, and a proof that every normalization is defined;
- the eigenvalue estimator, if any: Rayleigh quotient, component ratio, norm ratio, or another
  source-defined quantity; and
- the exact conclusion: projective/eigendirection convergence, vector convergence modulo sign or
  phase, eigenvalue convergence, residual convergence, a geometric error bound with constants, an
  asymptotic ratio, iteration complexity, stability, or a stated conjunction.

These decisions yield inequivalent propositions. They are a downstream resolution checklist, not
a canonical theorem statement.

## Candidate families not credited

- A diagonalizable real or complex matrix with a unique eigenvalue of greatest modulus, where a
  start with nonzero dominant coefficient yields projective convergence.
- A finite-dimensional self-adjoint operator with ordered eigenvalues and a strict absolute-value
  gap, using its orthonormal eigenbasis to prove convergence.
- A positive-matrix specialization whose Perron eigenvalue supplies the dominant eigenpair.
- Convergence of a Rayleigh-quotient estimate in addition to the normalized vectors.
- A finite-precision algorithm theorem with residual, stopping, rounding, or complexity bounds.

No family in this list is selected or credited at intake.

## Degenerate and boundary scope

The statement phase must decide zero-dimensional and one-dimensional spaces; the zero, identity,
nilpotent, scalar, and diagonal matrices; a zero dominant eigenvalue; repeated dominant eigenvalues;
distinct eigenvalues tied in modulus; positive and negative dominant eigenvalues; complex phases;
nonnormal and defective matrices; an initial zero vector; a start with zero dominant component;
an iterate that becomes zero; a start already in the dominant eigenspace; normalization by a zero
norm; and convergence claims when the spectral-gap ratio is zero, positive, or tends to one. No
case is silently excluded at intake.

## Explicit exclusions

- Merely proving that an exact eigenvector satisfies `A^k v = lambda^k v`.
- Generic eigenvalue existence, the spectral theorem, or an eigenbasis construction without the
  selected iteration and convergence conclusion.
- Perron-Frobenius, QR iteration (`THM-M-1451`), inverse iteration, Rayleigh-quotient iteration,
  Lanczos (`THM-M-1452`), or Arnoldi (`THM-M-1453`) used as a substitute.
- A theorem that assumes the desired convergence, error rate, nonzero normalization, or dominant
  decomposition as an unexplained stored field.
- A finite sampled trajectory, floating-point experiment, residual plot, fixed-size example,
  theorem name, `#check`, or the untrusted catalog status presented as a general proof.

## Neighbor boundaries

`THM-M-1451` is the QR eigenvalue algorithm, not power iteration. `THM-M-1452` and
`THM-M-1453` are Krylov-subspace methods, not the one-vector power recurrence. `THM-M-0054`
concerns Perron-Frobenius positivity and spectral structure; even if a selected power-method proof
later uses such a result, no statement or proof credit transfers between targets.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the eigenspace API
defines `Module.End.HasEigenvector` and proves `Module.End.HasEigenvector.pow_apply`; matrix APIs
provide `Matrix.mulVecLin`; and self-adjoint spectral theory provides sorted eigenvalues and an
orthonormal eigenbasis. `IntakeProbe.lean` checks representative interfaces in the pinned toolchain.
They are ingredients, not a source-selected power-iteration target or terminal proof body. No
canonical module, declaration, expression hash, environment fingerprint, alternate encoding,
checked transport, or mutation suite exists.

## Intake boundary

This scope map is a classification and non-substitution artifact. It supports a provisional
planned intake only. Source selection, exact statement work, formal anchor audit, obligation-tree
construction, proof, validation, and release remain separate open phases.
