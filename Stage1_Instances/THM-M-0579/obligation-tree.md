# THM-M-0579 frozen obligation architecture

Item: `S56-M-0579-OBLIGATION_TREE`.

The registry freezes 16 semantic obligations before proof execution. It uses
the Ricci-flow-with-surgery and finite-extinction route. No primary-source
crosswalk is accepted here, so freezing this route does not improve H debt.

## Typed proof route

```text
M0579-ROOT exact canonical proposition
`-- M0579-T-ASSEMBLE checked conditional composition
    |-- M0579-T-RECOGNITION homotopy equivalence with Sphere3
    |   |-- M0579-N-SMOOTH compatible smooth/PL structure
    |   |-- M0579-N-PRIME orientability and prime normalization
    |   |-- M0579-C-FLOW Ricci flow with surgery
    |   |-- M0579-C-INVARIANTS surgery control and topology tracking
    |   |-- M0579-L-ANALYTIC noncollapsing and canonical neighborhoods
    |   |-- M0579-L-EXTINCTION finite-time extinction
    |   `-- M0579-B-SURGERY exhaustive component recomposition
    `-- M0579-T-RIGIDITY homotopy sphere to homeomorphic sphere
```

Statement object-model, boundary, foundation, source, trust, documentation,
and workflow nodes live in separate typed graphs and cannot count as proof
premises. Every node's full required ledger is in `typed-graphs.json`.

## Node debt ledger

- `m0579-root`: exact elaborated target, `[H3, M3, R4]`.
- `m0579-s-object`: checked definitions and target expression, `[H3, M0-L, R4]`.
- `m0579-s-boundary`: connectedness/nonemptiness/boundary analysis, `[H3, M4, R4]`.
- `m0579-s-foundation`: axiom, TCB, choice, and no-oracle certificate, `[H3, M4, R4]`.
- `m0579-n-smooth`: topological-to-smooth reduction, `[H3, M4, R4]`.
- `m0579-n-prime`: orientability and prime normalization, `[H3, M4, R4]`.
- `m0579-c-flow`: Ricci-flow-with-surgery construction, `[H3, M4, R4]`.
- `m0579-c-invariants`: surgery invariants and choice independence, `[H3, M4, R4]`.
- `m0579-l-analytic`: analytic continuation estimates, `[H3, M4, R4]`.
- `m0579-l-extinction`: finite-time extinction, `[H3, M4, R4]`.
- `m0579-b-surgery`: surgery component branches and recomposition, `[H3, M4, R4]`.
- `m0579-t-recognition`: homotopy-sphere recognition package, `[H3, M4, R4]`.
- `m0579-t-rigidity`: three-dimensional topological rigidity package, `[H3, M4, R4]`.
- `m0579-t-assemble`: kernel-checked conditional composition, `[H3, M0-L, R4]`.
- `m0579-x-source`: pending node-level primary-source map, `[H3, M4, R4]`.
- `m0579-x-provenance`: pending body/import/axiom/replay inventory, `[H3, M4, R4]`.

## Freeze boundary

The minimal open root cut is `M0579-T-RECOGNITION` plus
`M0579-T-RIGIDITY`. The checked assembly accepts both as explicit premises and
does not prove either one. This phase supplies no root closure, audit
completion, or theorem completion. Any split, merge, correction, or eligibility
change requires registry version 2 and an append-only delta.
