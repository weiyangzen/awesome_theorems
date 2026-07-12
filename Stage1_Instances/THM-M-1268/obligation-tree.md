# THM-M-1268 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 12 stable obligations before proof execution. The ordered machine,
human-source, and readable denominators are recorded in `obligation-registry.json`; no mathematical
node is excluded because its proof is unavailable. `M1268-X-PROVENANCE` is informational and
cannot earn proof credit. Any later split, merge, correction, or eligibility change requires a new
registry version and an append-only ID delta.

## Typed proof route

```text
M1268-ROOT
`-- M1268-T-ASSEMBLE (checked conditional composition)
    |-- M1268-T-NORM-TO-WEAK (checked conditional composition)
    |   |-- M1268-L-CONVEX-SUBLEVEL
    |   |-- M1268-L-NORM-CLOSED
    |   `-- M1268-L-WEAK-CLOSURE
    `-- M1268-T-WEAK-TO-NORM
```

`M1268-S-DEFINITIONS`, `M1268-S-BOUNDARIES`, and `M1268-S-FOUNDATION` refine and constrain the
route. `M1268-X-SOURCE` and `M1268-X-PROVENANCE` remain separate source/trust overlays. The seven
graphs in `typed-graphs.json` prevent source, evidence, trust, documentation, or workflow edges
from masquerading as proof premises.

## Semantic leaves

### M1268-L-CONVEX-SUBLEVEL

For every threshold `r`, use the frozen EReal Jensen inequality to prove real convexity of
`f ⁻¹' Set.Iic r`. The proof must account for EReal multiplication by nonnegative real weights and
the explicit exclusion of negative infinity.

### M1268-L-NORM-CLOSED

Use `lowerSemicontinuous_iff_isClosed_preimage` at codomain `EReal`. This exact interface is already
kernel checked in `ObligationTree.lean`, but it supplies no convexity or weak transport.

### M1268-L-WEAK-CLOSURE

For each convex norm-closed sublevel, compose `Convex.toWeakSpace_closure` with explicit
`toWeakSpace` image/preimage identities. A short use of the separation theorem remains a substantive
bridge and must receive terminal-body provenance.

### M1268-T-WEAK-TO-NORM

Transport weak lower semicontinuity along the continuous norm-to-weak identity. The exact topology
direction and `OnWeakSpace` definitional transport must be checked; continuity cannot be inferred
from a prose claim that one topology is coarser.

## Composition and status

`ObligationTree.lean` checks the closed-sublevel equivalences, the substantive-direction assembly,
and final root assembly as conditional theorems. The conditions themselves remain open, so these
wrappers receive no root proof credit. Every current semantic ledger has a budget at most 100;
proof work must split a node if its exact implementation reveals hidden high-risk structure.

The frozen remaining root cut set is `M1268-L-CONVEX-SUBLEVEL`,
`M1268-L-WEAK-CLOSURE`, and `M1268-T-WEAK-TO-NORM`. Root debt remains `M4`; no H0, M0, R0,
audit completion, or theorem completion is claimed.
