# THM-M-0317 frozen obligation architecture

Item: `S56-M-0317-OBLIGATION_TREE`.

Version 1 freezes 17 semantic obligations before proof execution. The proof route is the classical
finite-dimensional approximation argument: construct approximate fixed points at every locally
convex neighbourhood scale, then use compactness and Hausdorff separation to obtain equality.

## Typed proof route

```text
M0317-ROOT exact canonical proposition
`-- M0317-T-ASSEMBLE checked conditional composition
    |-- M0317-T-APPROX arbitrarily small displacement
    |   |-- M0317-C-FINITE-COVER compact-image finite control cover
    |   |-- M0317-C-PARTITION continuous barycentric weights
    |   |-- M0317-C-FINITE-MAP finite-rank approximating self-map
    |   |-- M0317-L-BROUWER finite-dimensional fixed-point bridge
    |   `-- M0317-L-APPROX-FIXED transfer to small displacement
    `-- M0317-T-LIMIT exact fixed point from all scales
        |-- M0317-N-NEIGHBORHOODS displacement/equality normalization
        `-- M0317-L-COMPACT-LIMIT compactness and separation argument
```

The statement-definition, ambient/subtype transport, mutation boundary, foundation, source,
provenance, documentation, trust, and workflow nodes are separate typed graphs and cannot become
proof premises or inflate machine coverage.

## Node ledger

### m0317-root
Exact elaborated target. `[H1, M3, R4]`; no inhabitant is supplied.

### m0317-s-definitions
Checked exact statement and approximate-displacement vocabulary. `[H1, M0-L, R4]`.

### m0317-s-domains
Checked ambient/subtype fixed-point conclusion transport. `[H1, M0-L, R4]`.

### m0317-s-boundary
Checked rejection of removed nonemptiness, changed domain, moved binder, and removed invariance.
`[H1, M0-L, R4]`.

### m0317-s-foundation
Open classical-choice, axiom-closure, import, TCB, and no-oracle audit. `[H1, M4, R4]`.

### m0317-n-neighborhoods
Open exact reduction between equality and displacement in every zero neighbourhood. `[H1, M4, R4]`.

### m0317-c-finite-cover
Open compact-image finite cover by translates of a chosen convex zero neighbourhood. `[H1, M4, R4]`.

### m0317-c-partition
Open continuous subordinate weights, nonnegativity, support, and sum-one invariants. `[H1, M4, R4]`.

### m0317-c-finite-map
Open finite-rank barycentric map, hull invariance, continuity, and approximation estimate. `[H1, M4, R4]`.

### m0317-l-brouwer
Open finite-dimensional compact-convex fixed-point theorem, including affine-span and degenerate
cases. This major theorem is a bridge, not a primitive citation. `[H1, M4, R4]`.

### m0317-l-approx-fixed
Open transfer from the approximating-map fixed point to `f x - x` in the chosen neighbourhood.
`[H1, M4, R4]`.

### m0317-l-compact-limit
Open compactness and Hausdorff-separation engine turning all approximate fixed points into an exact
one. `[H1, M4, R4]`.

### m0317-t-approx
Open assembly of the five finite-dimensional approximation children. `[H1, M4, R4]`.

### m0317-t-limit
Open assembly of neighbourhood normalization and compactness limit. `[H1, M4, R4]`.

### m0317-t-assemble
Kernel-checked conditional composition from the two packages into the exact target. Its explicit
premises prevent root proof credit. `[H1, M0-L, R4]`.

### m0317-x-source
Open node-level primary-source theorem/page/assumption/errata crosswalk. `[H1, M4, R4]`.

### m0317-x-provenance
Open terminal-body, import, axiom, TCB, and replay inventory. `[H1, M4, R4]`.

## Freeze boundary

The minimal open root cut is `M0317-T-APPROX` plus `M0317-T-LIMIT`. The checked composition proves
neither premise. Any correction, split, merge, exclusion, or eligibility change requires registry
version 2 and an append-only delta. This phase supplies no proof, audit completion, accepted receipt,
or theorem completion.
