# THM-M-0557 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes nine root-relevant obligations against the exact
`Statement.lean` and pinned anchor-audit digests. The denominator is computed
from stable IDs, statement fingerprints, kinds, eligibility classes, risks,
exclusions, and terminal-body identities. Any later correction or split must
create registry version 2 and retain an append-only old/new ID delta.

## Typed proof route

```text
M0557-ROOT exact conjunction [open M3]
`-- M0557-COMPOSE checked conditional composition [M0-L]
    |-- M0557-GROUP [remaining cut]
    |   `-- M0557-GROUP-TRANSFER
    `-- M0557-COMM [remaining cut]
        `-- M0557-EH
            `-- M0557-DISTRIB
```

`M0557-GROUP-TRANSFER` owns the bridge from generalized cube loops to the
fundamental group. `M0557-EH` owns the Eckmann-Hilton bridge, while
`M0557-DISTRIB` owns coordinate-wise interchange. The separate
`M0557-PROVENANCE` and `M0557-SOURCE` nodes govern transitive body/trust and
human-source acceptance; neither is a mathematical proof premise.

The bundle separately records proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs. Proof edges have reciprocal
`proof_requires`/`composes` records. Every semantic ledger is capped at 100
steps; a node exceeding that budget must be split by a new registry version.

## Composition and status

`ObligationTree.lean` kernel-checks the exact child-to-parent conjunction from
explicit group and commutative-structure branch premises. It also resolves the
pinned declarations that later proof work must integrate. It does not discharge
either branch and therefore does not turn the anchor probe into proof credit.

The remaining root cut is `{M0557-GROUP, M0557-COMM}`. Transitive provenance,
trust, human-source mapping, readable reconstruction, independent verification,
and release remain open. The root stays `[H1, M3, R4]`; audit completion and
theorem completion are false.
