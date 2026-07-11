# THM-M-0545 frozen obligation architecture

Item: `S56-M-0545-OBLIGATION_TREE`.

## Freeze boundary

Registry version 1 freezes 17 semantic obligations before proof execution. Fifteen are
root-relevant machine obligations; two are source/provenance overlays. Eligibility was assigned
from the exact statement and the classical analytic route, not from the availability of a proof.
The canonical denominator digest is recorded in `obligation-registry.json` and checked against all
typed nodes. Any correction, split, merge, or exclusion requires a new version and append-only
delta.

## Typed proof route

```text
M0545-ROOT exact canonical proposition [M4]
`-- M0545-T-ASSEMBLE exact child-to-root composition
    |-- M0545-T-EXISTENCE
    |   |-- M0545-A-GREEN harmonic projection and Green operator
    |   |   |-- M0545-A-LAPLACIAN
    |   |   |   |-- M0545-A-D closed exterior derivative
    |   |   |   `-- M0545-A-ADJOINT codifferential as adjoint
    |   |   |       `-- M0545-A-COMPLETION L2/Sobolev completion
    |   |   `-- M0545-A-ELLIPTIC elliptic regularity and compact resolvent
    |   |-- M0545-L-CLOSED-RANGES closed ranges and orthogonality
    |   `-- M0545-S-BOUNDARY degree-zero/high-degree behavior
    `-- M0545-T-UNIQUENESS
        `-- M0545-L-CLOSED-RANGES
```

`M0545-S-INTERFACE`, `M0545-S-REALIZATION`, and `M0545-S-FOUNDATION` refine the
root without masquerading as proof premises. The provenance, evidence, trust, documentation, and
workflow graphs are separately typed. The realization bridge is especially important: the
predicates in `HodgeAnalyticData` must be eliminated into genuine geometric analytic data, and may
not hide decomposition itself.

## Node ledger

### m0545-root
The exact elaborated `HodgeDecompositionTarget`. `[H3, M4, R4]`.

### m0545-s-interface
Checked statement definitions, binders, and direct expansion. `[H3, M0-L, R4]`; statement closure
is not theorem closure.

### m0545-s-realization
Faithful interpretation of forms and operators from the frozen realization predicates.
`[H3, M4, R4]`.

### m0545-s-boundary
Degree zero and above-dimension behavior, including the predecessor condition in exactness.
`[H3, M4, R4]`.

### m0545-s-foundation
Classical, TCB, transitive-axiom, and no-oracle certificate. `[H3, M4, R4]`.

### m0545-a-completion
L2 and Sobolev completions of smooth forms with dense smooth inclusions. `[H3, M4, R4]`.

### m0545-a-d
Closed densely defined exterior derivative and `d^2 = 0`. `[H3, M4, R4]`.

### m0545-a-adjoint
Hilbert adjoint codifferential and compatibility with the smooth operator. `[H3, M4, R4]`.

### m0545-a-laplacian
Correct-domain nonnegative self-adjoint Hodge Laplacian. `[H3, M4, R4]`.

### m0545-a-elliptic
Elliptic regularity and compact resolvent on the compact boundaryless manifold. `[H3, M4, R4]`.

### m0545-a-green
Harmonic projection and Green operator with the required identities and commutation laws.
`[H3, M4, R4]`.

### m0545-l-closed-ranges
Closed exact/coexact ranges and all pairwise orthogonality relations. `[H3, M4, R4]`.

### m0545-t-existence
The Green-operator formula yields smooth harmonic, exact, and coexact summands. `[H3, M4, R4]`.

### m0545-t-uniqueness
Orthogonality forces equality of competing triples. `[H3, M4, R4]`.

### m0545-t-assemble
Checked composition of existence and uniqueness into every `k` and `omega` at the exact root.
`[H3, M4, R4]`.

### m0545-x-source
Primary theorem/page/assumption/transition/errata crosswalk. `[H3, M4, R4]`.

### m0545-x-provenance
Terminal bodies, imports, licenses, placeholders, axioms, TCB, and replay ledger.
`[H3, M4, R4]`.

## Status boundary

This phase freezes architecture only. Planned signatures, the classical paper proof, and adjacent
mathlib APIs close no obligation. The root remains `M4`; there is no proof body, accepted primary
source map, readable review, audit completion, or theorem completion.
