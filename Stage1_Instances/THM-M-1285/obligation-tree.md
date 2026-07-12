# THM-M-1285 frozen obligation architecture

Item: `S56-M-1285-OBLIGATION_TREE`.

The registry freezes 16 semantic obligations before proof execution. It uses
the distribution-function, generalized-inverse, and centered-ball route
identified by the anchor audit. No primary-source node map has been accepted,
so this architecture does not improve human-source debt.

## Typed proof route

```text
M1285-ROOT exact canonical proposition
`-- M1285-T-ASSEMBLE checked conditional composition
    `-- M1285-T-PACKAGE construct witness and package four properties
        |-- M1285-C-WITNESS witness from inverse/radius data
        |   |-- M1285-C-INVERSE generalized inverse
        |   |   |-- M1285-D-DISTRIBUTION finite distribution function
        |   |   `-- M1285-L-DISTRIBUTION monotonicity/limit package
        |   `-- M1285-C-RADIUS centered-ball radius realization
        |-- M1285-L-MEASURABLE witness measurability
        |-- M1285-L-RADIAL radiality
        |-- M1285-L-ANTITONE radial antitonicity
        `-- M1285-L-EQUIMEASURABLE exact strict-superlevel volumes
```

`M1285-S-INTERFACE`, `M1285-S-FOUNDATION`, `M1285-X-SOURCE`, and
`M1285-X-PROVENANCE` live in separate refinement, trust, documentation,
provenance, evidence, and workflow graphs. They cannot be counted as proof
premises.

## Semantic ledger

Every node has a stable ID, formal target, input/output ledger, debt vector,
step budget no greater than 100, validation ID, ownership, reviewer, and
invalidation policy in `typed-graphs.json`. The high-risk leaves distinguish
strict from non-strict superlevels and must account for threshold zero,
threshold infinity, null boundaries, zero functions, and finite positive
superlevel volume. The source overlay requires theorem/page/assumption/errata
evidence for each substantive node. The provenance overlay requires terminal
body, import, axiom, toolchain, license, and replay evidence.

## Freeze boundary

The minimal open root cut is `M1285-T-PACKAGE`. `ObligationTree.lean` checks
that this package composes to the exact root, but does not inhabit the package.
Thus the root remains `M3`; human-source and readable reconstruction debt also
remain open. Any correction, split, merge, or eligibility change requires a
new registry version and append-only delta. This phase supplies no theorem
proof, audit completion, or theorem completion.
