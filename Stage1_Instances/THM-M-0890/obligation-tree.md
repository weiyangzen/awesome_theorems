# THM-M-0890 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 33 semantic obligations against the exact statement and immutable
anchor audit. The denominator was derived before observed candidate status. No obligation was
excluded because a proof was hard or unavailable, no terminal proof body was found, and no
obligation is marked closed. A target correction, split, merge, exclusion, eligibility, risk,
edge-role, or proof-body-identity change requires version 2 and an append-only delta.

The selected proof family is Haemers' Theorem 1 route. It expands the regular all-ones eigenpair,
least-eigenvalue minimality and strict negativity, the Hoffman matrix, common eigenbasis, positive
semidefiniteness, restriction to a maximum independent set, exact quadratic-form evaluation,
positive-cardinality cancellation, denominator positivity, and the final quotient transport.

## Proof route

```text
M0890-ROOT [open M3]
`-- M0890-T-ASSEMBLE [conditional composition checked]
    |-- M0890-N-DENOMINATOR
    |   `-- M0890-L-LEAST-NEGATIVE
    `-- M0890-T-DIVISION-FREE
        |-- M0890-N-MAX-WITNESS [pinned witness wrapper checked]
        `-- M0890-L-SCALAR-ESTIMATE
            |-- M0890-L-QUADRATIC-EVAL
            |   |-- M0890-L-PSD-PRINCIPAL
            |   |   `-- M0890-L-HOFFMAN-PSD
            |   `-- M0890-T-RESTRICTED-FORM
            `-- M0890-B-ALPHA-POSITIVE
```

Only three parent certificates at the top spine are elaborated. The pinned witness wrapper is a
checked interface rather than a child-to-parent certificate. Ten deeper parents remain explicitly
unverified `logical_decomposition` plans. The separate proof, refinement, provenance, evidence,
trust, documentation, and workflow graphs are authoritative; this projection gives no proof credit.

## Obligation ledger

### m0890-root
The exact frozen `HoffmanRatioBoundTarget`; it remains H1/M3/R4 with no accepted proof state.

### m0890-s-target
Preserve the finite nonempty vertex type, decidability instances, regular natural degree, strict
positive-degree premise, natural-to-real casts, and exact quotient orientation.

### m0890-s-least
Freeze `leastAdjacencyEigenvalue` as the final entry of mathlib's descending Hermitian eigenvalue
enumeration. Merely naming this entry does not prove its required minimality properties.

### m0890-s-independence
Freeze `indepNum` and the maximum independent Finset witness. Maximum and merely maximal independent
sets are not interchangeable.

### m0890-s-boundary
Empty carriers and zero-degree regular graphs are excluded. Degree one, disconnected positive-degree
regular graphs, complete graphs, and repeated least eigenvalues stay in scope.

### m0890-s-transport
`ObligationTree.lean` checks only the one-way maximum-witness-to-`indepNum` transport and the final
division by a strictly positive denominator. No alternate form receives independent root credit.

### m0890-s-foundation
Classical finite spectral infrastructure is expected. Full axiom, imported artifact, compiler,
kernel, TCB, computation, and replay acceptance remains open.

### m0890-n-max-witness
Select an independent Finset with cardinality exactly `G.indepNum`. The local wrapper checks the
pinned mathlib interface, not the spectral estimate.

### m0890-n-least-min
Prove that the selected final eigenvalue is a lower bound for every adjacency eigenvalue and align
the enumeration with the basis used in the Hoffman-matrix proof.

### m0890-l-least-negative
Prove strict negativity of the least eigenvalue from positive regular degree. This omitted source
fact is material and cannot be hidden inside scalar automation.

### m0890-n-denominator
Derive `0 < (k : Real) - leastAdjacencyEigenvalue G`; this is an explicit child of the final
composition and the exact condition used by `le_div_iff₀`.

### m0890-l-regular-ones
Show that the real adjacency matrix sends the constant-one vector to `k` times that vector.

### m0890-l-ones-orthogonal
Establish the all-ones matrix action on the constant line and its orthogonal complement.

### m0890-c-hoffman-matrix
Construct `E = A - ((k - lambda_min) / n) J - lambda_min I`, with casts and `n > 0` explicit.

### m0890-l-common-eigenbasis
Build or import the exact simultaneous spectral description of `A` and `J`; a short appeal to a
deep spectral theorem remains a bridge obligation.

### m0890-l-hoffman-psd
Use least-eigenvalue minimality and the common eigenbasis to prove `E` positive semidefinite.

### m0890-c-principal
Restrict `E` along the subtype inclusion of the chosen maximum independent set.

### m0890-l-psd-principal
Apply the pinned `Matrix.PosSemidef.submatrix` boundary to retain positive semidefiniteness.

### m0890-l-independent-zero
Use independence to prove the selected adjacency principal block is zero entrywise.

### m0890-t-restricted-form
Simplify the restriction to `-((k-lambda_min)/n) J_alpha - lambda_min I_alpha` exactly.

### m0890-c-ones-vector
Construct the legal finitely supported all-ones test vector on the selected finite subtype.

### m0890-l-quadratic-eval
Evaluate the positive-semidefinite quadratic form as
`0 <= alpha * (-lambda_min - alpha * (k-lambda_min) / n)`.

### m0890-b-alpha-positive
Prove the maximum independent-set cardinality is positive from `Nonempty V`. This makes the scalar
cancellation exhaustive rather than silently discarding an alpha-zero case.

### m0890-l-scalar-estimate
Use positive graph order and alpha to turn the quadratic inequality into
`alpha * (k-lambda_min) <= n * (-lambda_min)`.

### m0890-t-division-free
Transport the selected witness and scalar estimate to the exact `indepNum` division-free child.

### m0890-t-assemble
Pair denominator positivity with the division-free estimate as `RatioAssemblyTarget`. The root
certificate separately transports that exact package to the canonical quotient. Neither child is
proved by this composition harness.

### m0890-x-mathlib
The pinned independent-set, regular adjacency, Hermitian spectrum, submatrix, and PSD APIs are
imported proof boundaries. None states Hoffman's bound.

### m0890-x-source
Haemers 2021, Theorem 1 supplies the route, but pinpoint premise/transition/errata mapping,
publication-history disposition, omitted denominator work, and independent H0 review remain open.

### m0890-x-provenance
Terminal body, wrapper, import, revision, license, source slice, and transitive origin closure remain
open and never become proof premises.

### m0890-x-evidence
Structured node receipts and immutable output bindings remain open and provide no semantic credit.

### m0890-x-trust
Full declaration/axiom/olean/executable/unsafe/oracle/TCB and independent replay closure remains open.

### m0890-x-readable
This architecture ledger is not an independently reviewed R0 reconstruction.

### m0890-x-workflow
Proof, validation, release, freshness, revocation, and independent verification remain task-state
boundaries, not mathematical premises.

## Status boundary

Every ledger budget is at most 85, but that is an expansion limit rather than proof evidence or
R0. There are zero accepted closed obligations and no installed terminal proof body. The minimal
open machine root cut is denominator positivity plus the maximum-independent-set scalar estimate.
H0, R0, transitive provenance/trust, hermetic replay, independent verification, `AUDIT-Z`,
`THEOREM-Z`, master acceptance, and theorem completion all remain open.
