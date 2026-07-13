# THM-M-0044 frozen obligation architecture

Item `S56-M-0044-OBLIGATION_TREE` freezes registry version 1 against the exact `Statement.lean`
and bounded `anchor-audit.json` inputs recorded in `obligation-registry.json`. The 39 canonical IDs
are the inventory denominator. A correction, split, merge, exclusion, eligibility change, or risk
change requires a new version and an append-only delta; later proof discovery cannot shrink the
frozen denominator.

## Exact proof route

```text
M0044-ROOT exact Real-and-Complex conjunction
`-- M0044-T-ASSEMBLE checked conditional conjunction
    |-- M0044-T-REAL exact FullSVDOver Real
    |   `-- M0044-B-REAL-DIMENSIONS
    |       |-- M0044-S-BOUNDARY checked empty dimensions
    |       `-- M0044-T-REAL-NONEMPTY
    `-- M0044-T-COMPLEX exact FullSVDOver Complex
        `-- M0044-B-COMPLEX-DIMENSIONS
            |-- M0044-S-BOUNDARY checked empty dimensions
            `-- M0044-T-COMPLEX-NONEMPTY
```

The two nonempty packages use the same mathematical architecture without requiring the stronger
open-class proposition `forall K, RCLike K -> FullSVDOver K`. This keeps the proof DAG on the exact
closed target. Each nonempty branch consumes unitary-factor construction, singular-value
nonnegativity, the exact rectangular Sigma, and the final entrywise equality.

The construction path linearizes `A`, forms `A† A`, proves it symmetric and positive, and applies
the pinned linear-map eigenvector-basis interface. The graph separately freezes the eigenbasis,
`LinearMap.singularValues`, rank bounds by both dimensions, alignment of the eigenvector and
singular-value indices, the exhaustive positive/zero split, normalized positive left vectors and
their orthonormality, zero-kernel and rectangular-tail equations, full left-basis extension,
unitary-matrix conversion, dependent `Fin (min m n)` normalization, explicit Sigma construction,
and the equality `A = U * Sigma * star V`. A short spectral-theorem invocation remains a bridge
obligation, not a proof of the factorization.

## Node ledger

### m0044-root
Exact canonical proposition. `[H1, M3, R3]`; no root inhabitant is credited.

### m0044-s-interface
Exact square-factor, nonnegative-diagonal, rectangular-Sigma, star-orientation interface. `[H1, M3, R3]`.

### m0044-s-boundary
Real and complex zero-row/zero-column witnesses, assembled in `selectedEmptyDimensions`. `[H1, M3, R3]` provisional interface evidence only.

### m0044-s-encoding
Exact direct-expansion Iff and one-way stronger-RCLike transport. `[H1, M3, R3]`; no alternate receives root credit.

### m0044-s-foundation
Open classical-choice, square-root, quotient, extensionality, axiom, TCB, and no-oracle audit. `[H1, M4, R3]`.

### m0044-b-real-dimensions
Exhaustive real zero-row, zero-column, and both-positive split. `[H1, M4, R3]`.

### m0044-b-complex-dimensions
Exhaustive complex zero-row, zero-column, and both-positive split. `[H1, M4, R3]`.

### m0044-t-real-nonempty
Positive-dimensional real factorization package. `[H1, M4, R3]`.

### m0044-t-complex-nonempty
Positive-dimensional complex factorization package. `[H1, M4, R3]`.

### m0044-n-linear-map
Matrix/Euclidean-linear-map and adjoint/orientation transport. `[H1, M4, R3]`.

### m0044-c-gram
Construction of the right Gram endomorphism `A† A`. `[H1, M4, R3]`.

### m0044-l-gram-hermitian
Hermitian/self-adjoint and positive-semidefinite Gram interface. `[H1, M3, R3]`; pinned support is not exact SVD closure.

### m0044-x-spectral
Pinned linear-map eigenvector-basis bridge with terminal-body audit still open. `[H1, M3, R3]`.

### m0044-c-right-eigenbasis
Full indexed right orthonormal eigenbasis. `[H1, M4, R3]`.

### m0044-c-singular-values
Pinned singular-value sequence restricted to the exact finite diagonal data. `[H1, M4, R3]`; the restriction/alignment is open.

### m0044-l-singular-nonneg
Nonnegativity and squared-eigenvalue equations. `[H1, M4, R3]`.

### m0044-l-rank-bounds
Prove `rank A <= m`, `rank A <= n`, and therefore `rank A <= min m n`. `[H1, M4, R3]`.

### m0044-b-singular-split
Exhaustive positive/zero split for every relevant singular direction. `[H1, M4, R3]`.

### m0044-b-positive
Positive singular-value branch. `[H1, M4, R3]`.

### m0044-c-positive-left
Construct `u_j = sigma_j^-1 A v_j` and its column equation. `[H1, M4, R3]`.

### m0044-l-positive-left-on
Prove the positive left family is orthonormal. `[H1, M4, R3]`.

### m0044-b-zero
Zero singular-value branch without division. `[H1, M4, R3]`.

### m0044-l-zero-kernel
Derive `A v_j = 0` from the zero Gram eigenvalue. `[H1, M4, R3]`.

### m0044-c-left-complete
Extend only the positive left family to a full `Fin m` orthonormal basis. `[H1, M3, R3]`; the exact construction is open.

### m0044-l-basis-invariants
Preserve index, orthonormality, and positive/zero column equations across extension. `[H1, M4, R3]`.

### m0044-c-unitary
Convert both oriented bases to square matrices in `Matrix.unitaryGroup`. `[H1, M3, R3]`; no witnesses are constructed yet.

### m0044-n-min-index
Transport rank, zero, and tail indices to `Fin (min m n)`. `[H1, M4, R3]`.

### m0044-n-order-align
Bind `sq_singularValues_fin`, its eigenvector, the support cutoff, and the same right-matrix column. `[H1, M4, R3]`.

### m0044-l-zero-tail
Prove every position at or beyond rank is zero, including columns `j >= m` when `m < n`. `[H1, M4, R3]`.

### m0044-c-sigma
Build the exact dependent rectangular Sigma and its off-diagonal-zero proof. `[H1, M4, R3]`.

### m0044-l-entrywise
Prove the frozen multiplication equality for every rectangular entry. `[H1, M4, R3]`.

### m0044-t-real
Exact real package, still conditional on its nonempty branch. `[H1, M4, R3]`.

### m0044-t-complex
Exact complex package, still conditional on its nonempty branch. `[H1, M4, R3]`.

### m0044-t-assemble
Kernel-checked conjunction composition from the exact real and complex packages. `[H1, M3, R3]`; both premises remain open.

### m0044-x-source
Node-specific primary/historical source, assumptions, empty-dimension, orientation, and errata crosswalk. `[H1, M4, R3]`.

### m0044-x-provenance
Terminal-body, wrapper, immutable-origin, license, and revocation inventory. `[H1, M4, R3]`.

### m0044-x-trust
Transitive axiom, dependency, compiled-artifact, oracle, TCB, and replay audit. `[H1, M4, R3]`.

### m0044-x-readable
Complete independently reviewed mathematical reconstruction. `[H1, M4, R3]`.

### m0044-x-workflow
Dependency-ordered proof, validation, independent-verification, and release acceptance. `[H1, M4, R3]`.

## Typed graphs and boundary

The proof graph has reciprocal `proof_requires` and `composes` edges. Refinement, provenance/source,
evidence, trust, documentation, and workflow remain separate graphs; the evidence graph is empty
because no content-addressed node receipt is accepted. Source and governance nodes cannot supply a
proof premise. All leaf budgets are at most 100 substantive steps, and every ledger records exact
child IDs and outgoing uses.

The current open proof cut is the real and complex packages. Source, foundation, provenance, trust,
readability, workflow, proof implementation, validation, and release also remain open. This phase
does not establish H0, accepted M0, R0, AUDIT-Z, theorem completion, release, or master acceptance.
