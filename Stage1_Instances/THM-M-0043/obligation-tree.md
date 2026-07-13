# THM-M-0043 frozen obligation architecture

Item `S56-M-0043-OBLIGATION_TREE` freezes registry version 1 against the exact statement and the
immutable anchor audit. The 33 canonical IDs form the denominator for later machine, source, and
readable coverage. The inventory was derived from the claim and the visible Atlas/mathlib route,
not from candidate closure status. A target correction, split, merge, exclusion, eligibility or
risk change, or proof-body identity change requires a new registry version and append-only delta.

## Proof Route

```text
M0043-ROOT exact normal-matrix target [accepted M3]
`-- M0043-T-ROOT-COMPOSE checked conditional orientation adapter
    `-- M0043-T-CONJUGATED-DIAGONAL external Atlas anchor [M1/E2, uninstalled]
        |-- M0043-L-MATRIX-EIGEN-RELATION A*P=P*diagonal(ev)
        |   |-- M0043-L-BASIS-EIGENVECTORS
        |   |-- M0043-C-EIGENVALUES
        |   `-- M0043-C-UNITARY-MATRIX
        `-- M0043-C-UNITARY-MATRIX unitary orthonormal-basis matrix
            `-- M0043-C-BASIS-REINDEX
                `-- M0043-L-SUBORDINATE-BASIS
                    |-- M0043-B-NONZERO-SUBTYPE
                    |   |-- M0043-L-JOINT-DECOMP
                    |   |-- M0043-L-FINITE-EIGENVALUES
                    |   `-- M0043-C-JOINT-EIGENSPACE
                    `-- M0043-L-JOINT-ORTHOGONAL
```

The proof graph also expands the normality-to-commuting-Hermitian-parts route and every basis,
operator, and matrix transport. Each parent-to-child `proof_requires` edge has one reciprocal
child-to-parent `composes` edge. Statement refinements, source maps, provenance, evidence, trust,
documentation, and workflow are separate graphs and never become proof premises.

## Obligation Ledger

<a id="m0043-root"></a>
### M0043-ROOT
Exact frozen `SpectralTheoremTarget`; it remains H1/M3/R4 with no accepted proof state.

<a id="m0043-s-interface"></a>
### M0043-S-INTERFACE
Preserve `n`, `Fintype`, `DecidableEq`, `Nonempty`, `A`, normality, unitary witness, diagonal entries,
and the equation `A = U * diagonal d * star U` in their frozen order.

<a id="m0043-s-boundary"></a>
### M0043-S-BOUNDARY
Exclude only empty dimension. Zero, identity, singular normal matrices, and repeated eigenvalues
remain included; the Atlas child is stronger because it also covers the empty type.

<a id="m0043-s-encodings"></a>
### M0043-S-ENCODINGS
The two statement iff theorems check explicit unitary membership and conjugated-diagonal
orientation without creating duplicate root or terminal-body credit.

<a id="m0043-s-foundation"></a>
### M0043-S-FOUNDATION
The observed local and external interfaces report only `propext`, `Classical.choice`, and
`Quot.sound`; full transitive foundation, TCB, computation, and replay review stays open.

<a id="m0043-n-normal-commute"></a>
### M0043-N-NORMAL-COMMUTE
Unfold normality into commutation of the matrix with its conjugate transpose.

<a id="m0043-c-hermitian-parts"></a>
### M0043-C-HERMITIAN-PARTS
Construct `H=(A+A*)/2` and `K=(-i/2)(A-A*)`; their two Hermitian proofs stay distinct obligations.

<a id="m0043-l-h-hermitian"></a>
### M0043-L-H-HERMITIAN
Prove the real part `H` is Hermitian and hence induces a symmetric Euclidean linear map.

<a id="m0043-l-k-hermitian"></a>
### M0043-L-K-HERMITIAN
Prove the imaginary part `K` is Hermitian and hence induces a symmetric Euclidean linear map.

<a id="m0043-t-m-reconstruct"></a>
### M0043-T-M-RECONSTRUCT
Check entrywise that the original matrix is `H + i K`.

<a id="m0043-l-hk-commute"></a>
### M0043-L-HK-COMMUTE
Use normality to prove the two Hermitian parts commute as matrices.

<a id="m0043-t-linear-commute"></a>
### M0043-T-LINEAR-COMMUTE
Transport matrix commutation to commutation of the associated Euclidean linear maps.

<a id="m0043-c-joint-eigenspace"></a>
### M0043-C-JOINT-EIGENSPACE
Define each joint eigenspace as the intersection of one `H` eigenspace and one `K` eigenspace.

<a id="m0043-l-joint-decomp"></a>
### M0043-L-JOINT-DECOMP
Apply the pinned commuting-symmetric-operator bridge to obtain an internal direct sum.

<a id="m0043-l-joint-orthogonal"></a>
### M0043-L-JOINT-ORTHOGONAL
Apply the pinned symmetric-operator bridge giving orthogonality of distinct joint eigenspaces.

<a id="m0043-l-finite-eigenvalues"></a>
### M0043-L-FINITE-EIGENVALUES
Use finite dimensionality to make the subtype of nonzero joint eigenspaces finite.

<a id="m0043-b-nonzero-subtype"></a>
### M0043-B-NONZERO-SUBTYPE
Restrict to nonbottom joint eigenspaces and check that the restricted supremum still spans.

<a id="m0043-l-subordinate-basis"></a>
### M0043-L-SUBORDINATE-BASIS
Choose an orthonormal basis subordinate to the finite orthogonal internal direct sum.

<a id="m0043-c-basis-reindex"></a>
### M0043-C-BASIS-REINDEX
Reindex the subordinate `Fin` basis back to the canonical matrix index type `n`.

<a id="m0043-t-operator-decomp"></a>
### M0043-T-OPERATOR-DECOMP
Transport `A=H+iK` through `Matrix.toEuclideanLin`.

<a id="m0043-c-eigenvalues"></a>
### M0043-C-EIGENVALUES
For each basis vector, combine its `H` and `K` eigenvalues as `lambda_H + i lambda_K`.

<a id="m0043-l-basis-eigenvectors"></a>
### M0043-L-BASIS-EIGENVECTORS
Show every chosen orthonormal basis vector is an eigenvector of `A` with that combined value.

<a id="m0043-l-unitary-basis"></a>
### M0043-L-UNITARY-BASIS
Use the pinned orthonormal-basis change-of-basis theorem to prove unitary membership.

<a id="m0043-c-unitary-matrix"></a>
### M0043-C-UNITARY-MATRIX
Construct the matrix `P` whose columns are the chosen basis and retain its unitary proof.

<a id="m0043-l-matrix-eigen-relation"></a>
### M0043-L-MATRIX-EIGEN-RELATION
Convert the pointwise eigenvector equations to `A * P = P * diagonal ev`.

<a id="m0043-t-conjugated-diagonal"></a>
### M0043-T-CONJUGATED-DIAGONAL
Combine the eigen-relation with `star P * P = 1` to obtain the exact audited Atlas conclusion.

<a id="m0043-t-root-compose"></a>
### M0043-T-ROOT-COMPOSE
`ObligationTree.lean` conditionally converts that conclusion to the frozen root equation. The
external body remains an explicit premise, so this check installs no proof.

<a id="m0043-x-source"></a>
### M0043-X-SOURCE
Primary Hilbert/1906 provenance, pinpoint assumptions, errata, and independent H0 review remain open.

<a id="m0043-x-provenance"></a>
### M0043-X-PROVENANCE
Atlas and mathlib source identities are known, but full transitive provenance and the restrictive
Atlas license/reuse decision remain open.

<a id="m0043-x-evidence"></a>
### M0043-X-EVIDENCE
Node-specific immutable E1 evidence and deterministic release receipts remain open.

<a id="m0043-x-trust"></a>
### M0043-X-TRUST
Full root-reachable declaration, axiom, unsafe/oracle, kernel, compiler, and dependency review remains open.

<a id="m0043-x-readable"></a>
### M0043-X-READABLE
This ledger is an architecture projection, not an independently reviewed R0 reconstruction.

<a id="m0043-x-workflow"></a>
### M0043-X-WORKFLOW
Proof integration, hermetic validation, independent verification, release, freshness, and revocation
receipts remain open and never act as proof premises.

## Freeze Boundary

No induction, descent, numerical computation, reflection, solver, oracle, or additional mathematical
case split occurs in the visible route; each exclusion remains pending independent approval. Every
semantic ledger has a budget at most 80, and later proof work must split any node that exposes hidden
work. The external Atlas theorem is M1/E2 only and is not in the repository dependency closure.
Accepted state therefore stays empty and the authoritative root remains `[H1, M3, R4]`.
