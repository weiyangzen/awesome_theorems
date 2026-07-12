# THM-M-1138 frozen obligation architecture

Item: `S56-M-1138-OBLIGATION_TREE`.

Registry version 1 freezes 15 semantic obligations before proof execution. Thirteen are required
machine obligations; the source and provenance overlays are informational and cannot supply proof
credit. Any correction, split, merge, or eligibility change requires a new registry version and an
append-only delta.

## Typed proof route

```text
M1138-ROOT [open M3]
`-- M1138-T-ROOT-TRANSPORT [checked conditional composition]
    `-- M1138-T-BOUNDARY-MAX [remaining root cut, M4]
        |-- M1138-C-CLOSURE-MAXIMIZER
        |   |-- M1138-N-COMPACT-CLOSURE
        |   `-- M1138-S-DEFINITIONS
        |-- M1138-B-MAXIMIZER-LOCATION
        |-- M1138-L-INTERIOR-LOCAL
        |   `-- M1138-S-DEFINITIONS
        |-- M1138-L-CONNECTED-PROPAGATION
        |-- M1138-L-FRONTIER-NONEMPTY
        |-- M1138-L-CONTINUITY-EXTENSION
        `-- M1138-S-BOUNDARIES
```

The root is also refined by the definitions, boundary, and foundation layers. Separate provenance,
evidence, trust, documentation, and workflow graphs keep non-proof relationships from being counted
as proof premises. Every proof requirement has a reciprocal composition edge.

## Node ledger

### m1138-root
The exact elaborated target. It remains open at `M3`.

### m1138-s-definitions
The Euclidean, harmonicity, topology, and order vocabulary already elaborated in `Statement.lean`.

### m1138-s-boundaries
Positive dimension, nonemptiness, empty-frontier avoidance, and closure membership obligations.

### m1138-s-foundation
The open transitive import, axiom, classical-choice, TCB, and no-oracle certificate.

### m1138-n-compact-closure
Heine-Borel normalization from boundedness to a compact nonempty closure.

### m1138-c-closure-maximizer
Extreme-value construction of a maximizer on `closure U`, including membership and maximality.

### m1138-b-maximizer-location
Exhaustive split of that maximizer into the frontier case or the interior case.

### m1138-l-interior-local
The central mean-value step: an interior maximum of a harmonic function forces local constancy.

### m1138-l-connected-propagation
Propagation of the maximum level through connected `U`.

### m1138-l-frontier-nonempty
Existence of a frontier point for a nonempty bounded open domain in positive dimension.

### m1138-l-continuity-extension
Extension of constancy from `U` to its closure using density and closure continuity.

### m1138-t-boundary-max
Branch merge producing a frontier point that dominates every value on the closure. This is the
minimal open root cut and remains `M4`.

### m1138-t-root-transport
`ObligationTree.lean` kernel-checks that the exact terminal package yields the public root. This
conditional composition does not prove its premise.

### m1138-x-source
Open primary-source theorem/page, assumption, proof-step, and errata mapping for required nodes.

### m1138-x-provenance
Open terminal-body, import, axiom, TCB, and replay provenance inventory.

## Status boundary

This phase freezes and structurally validates an architecture. It proves neither the local strong
maximum lemma nor the terminal boundary-maximum package. Root `[H1, M3, R3]`, audit completion,
theorem completion, release evidence, and master acceptance remain open.
