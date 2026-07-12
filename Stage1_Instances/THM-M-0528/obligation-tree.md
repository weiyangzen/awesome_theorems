# THM-M-0528 frozen obligation architecture

Item: `S56-M-0528-OBLIGATION_TREE`.

Registry version 1 freezes 12 semantic obligations before proof-phase installation. Eligibility is
derived from the exact statement and the audited terminal body's covering-map architecture, not
from the availability of the pinned theorem.

## Typed proof route

```text
M0528-ROOT exact canonical proposition [open M3]
`-- M0528-T-ASSEMBLE checked conditional pointwise-to-composite transport
    `-- M0528-X-ANCHOR exact pinned Proposition 1.34 bridge [M1; not accepted here]
        |-- M0528-L-SEPARATED covering maps have separated fibers
        |-- M0528-L-LOCAL-INJECTIVE local homeomorphisms are locally injective
        `-- M0528-L-PROPAGATE equality propagates over a preconnected domain
```

The definition, domain/boundary, equivalent-form transport, foundation, source, and provenance
obligations live in separate refinement, trust, provenance, documentation, and workflow graphs.
They cannot be counted as duplicate proof premises. The machine proof graph alone has reciprocal
`proof_requires` and `composes` edges.

## Node ledger

### m0528-root
The exact universally quantified target from `Statement.lean`. `[H3, M3, R4]`.

### m0528-s-definitions
Covering-map, continuity, composition, and equality conventions. `[H3, M0-L, R4]`.

### m0528-s-domain
Independent universes/topologies, preconnectedness, and the explicit point witness. The witness
rules out an actually empty use without adding `Nonempty A`. `[H3, M0-L, R4]`.

### m0528-s-transport
Checked equivalence of composite equality and pointwise projection equality. `[H3, M0-L, R4]`.

### m0528-s-foundation
Transitive axiom, TCB, and no-oracle report, still pending. `[H3, M4, R4]`.

### m0528-l-separated
The covering trivialization separates distinct points in a discrete fiber. `[H3, M4, R4]`.

### m0528-l-local-injective
The covering local homeomorphism supplies local injectivity. `[H3, M4, R4]`.

### m0528-l-propagate
Separatedness plus local injectivity propagates equality from the witness across the preconnected
domain. This is the substantive general uniqueness engine. `[H3, M4, R4]`.

### m0528-x-anchor
The exact pinned `IsCoveringMap.eq_of_comp_eq` bridge, whose transparent terminal body consumes the
three preceding facts. It remains `M1` until proof-phase installation and validation acceptance.

### m0528-t-assemble
Kernel-checked conditional transport from the exact pointwise anchor to the canonical target.
`[H3, M0-L, R4]`; it is not an inhabitant of the anchor premise.

### m0528-x-source
Primary-edition proposition/page/assumption/errata mapping remains open. `[H3, M4, R4]`.

### m0528-x-provenance
Terminal-body, import, transitive trust, and replay closure remains open. `[H3, M4, R4]`.

## Freeze boundary

The minimal root cut is `M0528-X-ANCHOR`. This phase freezes its identity and internal semantic
dependencies but does not install it as the canonical proof body. Proof, validation, primary-source
acceptance, readable reconstruction, independent verification, and release remain downstream.
Any correction, split, merge, or eligibility change requires registry version 2 and an append-only
delta. No audit completion or theorem completion is claimed.
