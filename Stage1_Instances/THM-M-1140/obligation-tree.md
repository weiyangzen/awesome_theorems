# THM-M-1140 frozen obligation architecture

Item: `S56-M-1140-OBLIGATION_TREE`.

Registry version 1 freezes 16 semantic obligations before proof execution. Fourteen are required
machine obligations; the human-source boundary is machine-inapplicable and the provenance overlay
is informational. Neither receives proof credit. Any semantic correction, split, merge, exclusion,
or eligibility change requires registry version 2 and an append-only delta.

## Typed proof route

```text
M1140-ROOT [open M3]
`-- M1140-T-ASSEMBLE [checked conditional composition]
    |-- M1140-T-LOCAL-PACKAGE [open M4]
    |   `-- M1140-L-MEAN-VALUE [open M4, critical]
    |-- M1140-T-PROPAGATION-PACKAGE [open M4]
    |   |-- M1140-N-MAX-LEVEL
    |   |-- M1140-L-LEVEL-CLOSED
    |   |   `-- M1140-L-CONTINUITY [pinned mathlib bridge]
    |   |-- M1140-L-LEVEL-OPEN
    |   |   `-- M1140-L-MEAN-VALUE
    |   `-- M1140-L-CONNECTED
    `-- M1140-L-CONTINUITY
```

The root also has statement/foundation refinement children. Separate provenance, evidence, trust,
documentation, and workflow graphs prevent support relationships from being counted as proof
premises. Every proof requirement owns a reciprocal composition edge.

## Node ledger

### m1140-root
The exact elaborated target. It remains `M3` because no proof body closes the proposition.

### m1140-s-definitions
The Euclidean, harmonicity, topology, connectedness, and order vocabulary elaborated by
`Statement.lean`.

### m1140-s-domain
The exact ordered binders and hypotheses, including explicit nonemptiness and dimension zero.

### m1140-s-boundary
The dimension-zero case and the semantic effects of deleting core hypotheses.

### m1140-s-foundation
The open transitive import, axiom, classical-topology, TCB, and no-oracle audit.

### m1140-n-max-level
The relative set of points where `u x = u x0`, with its witness `x0`.

### m1140-l-mean-value
The central arbitrary-dimensional bridge: an attained interior maximum forces local constancy.
The anchor audit found no pinned theorem supplying it, so this remains a critical `M4` leaf.

### m1140-l-continuity
The pinned bridge `HarmonicOnNhd.continuousOn`, consumed only for level-set closedness.

### m1140-l-level-closed
Relative closedness of the maximum-level set from continuity.

### m1140-l-level-open
Relative openness of the level set by applying local rigidity at every one of its points.

### m1140-l-connected
Connectedness propagation from a nonempty relatively clopen level set to all of `Omega`.

### m1140-t-local-package
The exact `InteriorLocalRigidity` interface. Its mean-value body remains open.

### m1140-t-propagation-package
The exact `ConnectedLevelPropagation` interface, expanded into level-set obligations.

### m1140-t-assemble
`ObligationTree.lean` kernel-checks that both packages and harmonic continuity yield the exact root.
The theorem is conditional and does not manufacture either package.

### m1140-x-source
Open primary-source theorem/page, assumption, proof-step, and errata mapping.

### m1140-x-provenance
Open terminal-body, import, axiom, TCB, immutable-revision, and replay inventory.

## Status boundary

This phase freezes and structurally validates the architecture. It does not prove local harmonic
rigidity, connected propagation, or the root, and it does not establish human-source/readability,
release, or master-acceptance gates. Root `[H2, M3, R3]`; theorem completion is false.
