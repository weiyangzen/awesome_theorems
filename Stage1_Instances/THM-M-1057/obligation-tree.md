# Frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 15 root-relevant obligations before proof execution.
Eligibility is independent of known closure. Planned fingerprints identify
intended interfaces, not Lean evidence. Corrections, splits, merges, and
exclusions require a new registry version with an append-only delta.

## Typed proof route

```text
M1057-ROOT exact canonical proposition
`-- M1057-T-ASSEMBLE checked conditional composition
    `-- M1057-T-LIMIT-PACKAGE
        |-- M1057-L-AE-CONVERGENCE
        |   |-- M1057-C-BLOCK-DECOMPOSITION
        |   `-- M1057-L-MAXIMAL-INEQUALITY
        |       `-- M1057-C-BLOCK-DECOMPOSITION (shared body)
        |-- M1057-L-INVARIANCE
        `-- M1057-L-ERGODIC-IDENTIFICATION
            |-- M1057-L-INVARIANCE (shared body)
            `-- M1057-L-FEKETE
                `-- M1057-N-EXPECTATION-SUBADDITIVE
```

Statement vocabulary and boundaries, foundation policy, source mapping,
provenance, evidence, documentation, and workflow order live in separate typed
graphs. None supplies proof credit.

## Node ledger

- `M1057-ROOT`: exact elaborated Kingman target, `[H1, M3, R3]`.
- `M1057-S-DEFINITIONS`: checked process and normalization vocabulary, `[H1, M0-L, R3]`.
- `M1057-S-BOUNDARY`: checked expansion and zero/positive-index boundaries, `[H1, M0-L, R3]`.
- `M1057-S-FOUNDATION`: pending import, axiom, TCB, and no-oracle certificate, `[H1, M4, R3]`.
- `M1057-N-EXPECTATION-SUBADDITIVE`: integrate the cocycle inequality and prove expectation subadditivity, budget 100, `[H1, M4, R3]`.
- `M1057-L-FEKETE`: target-specific boundedness bridge to the audited Fekete anchor, budget 60, `[H1, M3, R3]`.
- `M1057-C-BLOCK-DECOMPOSITION`: measurable fixed-block decomposition and remainder control, budget 100, `[H1, M4, R3]`.
- `M1057-L-MAXIMAL-INEQUALITY`: subadditive maximal/ergodic estimate controlling oscillation, budget 100, `[H1, M4, R3]`.
- `M1057-L-AE-CONVERGENCE`: finite measurable almost-everywhere limit, budget 100, `[H1, M4, R3]`.
- `M1057-L-INVARIANCE`: almost-everywhere invariance of that limit, budget 80, `[H1, M4, R3]`.
- `M1057-L-ERGODIC-IDENTIFICATION`: ergodic constancy plus identification with the expectation infimum, budget 100, `[H1, M4, R3]`.
- `M1057-T-LIMIT-PACKAGE`: combine convergence, invariance, and value identification, `[H1, M4, R3]`.
- `M1057-T-ASSEMBLE`: checked exact conditional composition, `[H1, M0-L, R3]`.
- `M1057-X-SOURCE`: pending theorem/page/hypothesis/convention/errata map, `[H1, M4, R3]`.
- `M1057-X-PROVENANCE`: pending terminal-body, import, trust, replay, and license inventory, `[H1, M4, R3]`.

## Status boundary

The frozen minimal open root cut is `M1057-T-LIMIT-PACKAGE`. The checked
assembly introduces no proof of that premise. This phase claims no H0, root
closure, audit completion, theorem completion, or accepted receipt.
