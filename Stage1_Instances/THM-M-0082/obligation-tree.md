# THM-M-0082 frozen obligation architecture

Item: `S56-M-0082-OBLIGATION_TREE`.

The registry freezes 13 semantic obligations before proof integration. It
separates the exact root and checked explicit-to-typeclass transport from the
central pinned mathlib bridge, expands the mathematical body of that bridge,
and keeps source, trust, provenance, documentation, and workflow edges outside
the proof-credit graph.

## Typed proof route

```text
M0082-ROOT exact explicit-hypothesis proposition
`-- M0082-S-TRANSPORT checked conditional composition
    `-- M0082-X-BRIDGE exact general adjoint-functor theorem interface
        |-- M0082-C-STRUCTURED reduce to structured-arrow initial objects
        |-- M0082-C-SOLUTION-FAMILY build a small weakly initial family
        |-- M0082-L-WEAKLY-INITIAL combine it by products
        `-- M0082-L-INITIAL refine it by wide equalizers
```

The four indented nodes below the bridge are typed logical refinements of the
central imported body. They do not receive separate proof credit merely because
one opaque theorem invocation can hide them.

## Node ledger

### m0082-root
Exact elaborated `GeneralRightAdjointTarget`. `[H2, M3, R4]`; open.

### m0082-s-definitions
Exact categorical vocabulary and hypotheses. `[H2, M0-L, R4]`.

### m0082-s-universes
Independent universes and `vD`-small solution family. `[H2, M0-L, R4]`.

### m0082-s-boundary
No hidden nonempty, well-powered, coseparating, or equal-universe premise.
`[H2, M0-L, R4]`.

### m0082-s-transport
`root_of_bridge` kernel-checks exact composition and consumes the bridge as an
explicit hypothesis. `[H2, M0-L, R4]`; it does not prove that hypothesis.

### m0082-x-bridge
Exact pinned type of
`isRightAdjoint_of_preservesLimits_of_solutionSetCondition`. `[H2, M4, R4]`.

### m0082-c-structured
For every `A`, reduce adjoint existence to an initial object in
`StructuredArrow A G`. `[H2, M4, R4]`.

### m0082-c-solution-family
Build structured arrows from solution-set witnesses and show they map to every
structured arrow. `[H2, M4, R4]`.

### m0082-l-weakly-initial
Use products to combine the small family into a weakly initial object.
`[H2, M4, R4]`.

### m0082-l-initial
Use wide equalizers to obtain an initial object. `[H2, M4, R4]`.

### m0082-s-foundation
Pending transitive report for `propext`, `Classical.choice`, `Quot.sound`, the
kernel, and the no-oracle boundary. `[H2, M4, R4]`.

### m0082-x-source
Pending pinpoint primary-source and errata crosswalk. `[H2, M4, R4]`.

### m0082-x-provenance
Pending terminal-body, import, license, and replay closure. `[H2, M4, R4]`.

## Freeze boundary

The minimal open machine root cut is `M0082-X-BRIDGE`. The checked conditional
composition is not a proof of that bridge. Human-source, trust, and provenance
overlays also remain open. This phase claims no root closure, audit completion,
or theorem completion. Registry changes require a new version and append-only
delta.
