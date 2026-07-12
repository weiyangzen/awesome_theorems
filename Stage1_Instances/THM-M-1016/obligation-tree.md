# Frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 14 root-relevant obligations for
`S56-M-1016-OBLIGATION_TREE` before proof execution. Planned fingerprints name intended
interfaces, not Lean evidence. Any correction, split, merge, or eligibility change requires a new
version and append-only delta.

## Typed proof route

```text
M1016-ROOT exact frozen proposition
`-- M1016-T-ASSEMBLE checked conditional Slutsky composition
    |-- M1016-L-LINEAR-MAP checked continuous mapping by g'
    `-- M1016-T-REMAINDER scaled Frechet remainder tends to zero in measure
        |-- M1016-C-REMAINDER measurable algebraic remainder package
        |-- M1016-L-LITTLE-O Frechet little-o evaluated along X_n
        |   |-- M1016-N-CONCENTRATION X_n tends to theta in probability
        |   |   `-- M1016-N-TIGHTNESS normalized input is bounded in probability
        |   `-- M1016-C-REMAINDER (shared body)
        `-- M1016-L-PRODUCT bounded-in-probability times o-in-probability
            |-- M1016-N-TIGHTNESS (shared body)
            `-- M1016-L-LITTLE-O (shared body)
```

Definitions, boundary cases, foundation, provenance, evidence, trust, documentation, source, and
workflow edges live in separate typed graphs and cannot masquerade as proof premises.

## Node ledger

- `M1016-ROOT`: exact `StatementShape`; `[H2, M3, R4]`, open.
- `M1016-S-DEFINITIONS`: elaborated domains, scaling, weak convergence, and derivative; `[H2, M0-L, R4]`.
- `M1016-S-BOUNDARIES`: frozen mutation/boundary policy; `[H2, M0-L, R4]`.
- `M1016-S-FOUNDATION`: pending import, axiom, TCB, and no-oracle certificate; `[H2, M4, R4]`.
- `M1016-N-TIGHTNESS`: weak convergence implies boundedness in probability; budget 100, `[H2, M4, R4]`.
- `M1016-N-CONCENTRATION`: divergent positive scaling forces concentration at `theta`; budget 100, `[H2, M4, R4]`.
- `M1016-C-REMAINDER`: measurable Frechet remainder and exact decomposition; budget 100, `[H2, M4, R4]`.
- `M1016-L-LITTLE-O`: probabilistic evaluation of `HasFDerivAt` little-o; budget 100, `[H2, M4, R4]`.
- `M1016-L-PRODUCT`: bounded times vanishing product theorem; budget 100, `[H2, M4, R4]`.
- `M1016-L-LINEAR-MAP`: checked continuous-mapping invocation; `[H2, M0-L, R4]`.
- `M1016-T-REMAINDER`: exact scaled remainder convergence, the minimal open root cut; `[H2, M4, R4]`.
- `M1016-T-ASSEMBLE`: checked `deltaMethod_of_remainder`; `[H2, M0-L, R4]`, conditional only.
- `M1016-X-SOURCE`: pending theorem/page/assumption/errata crosswalk; `[H2, M4, R4]`.
- `M1016-X-PROVENANCE`: pending bodies/imports/axioms/replay inventory; `[H2, M4, R4]`.

## Status boundary

The minimal root cut is `M1016-T-REMAINDER`. The checked composition keeps that premise explicit.
This freeze claims no H0, root closure, audit completion, theorem completion, or accepted receipt.
