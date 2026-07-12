# THM-M-0320 obligation tree

Item: `S56-M-0320-OBLIGATION_TREE`. This is a frozen proof architecture, not a
proof-completion claim. The machine-readable authority is
`obligation-registry.json` plus `typed-graphs.json`.

```text
M0320-ROOT  exact KakutaniFixedPointTarget
`-- M0320-T-ASSEMBLE  checked conditional composition
    |-- M0320-T-COMPACT  closed + bounded -> compact [checked]
    |-- M0320-T-GRAPH  upper hemicontinuity + closed values -> closed graph [open]
    `-- M0320-C-CORE  closed-graph Kakutani theorem [open]
        `-- M0320-T-SUBTYPE  external subtype/ambient wrapper and integration [open]

Overlays: M0320-S-STATEMENT, M0320-S-FOUNDATION, M0320-X-SOURCE,
M0320-X-PROVENANCE.
```

## M0320-ROOT

The root is exactly `KakutaniFixedPointTarget`, including nonempty, closed,
bounded and convex domain hypotheses, nonempty closed convex values contained
in the domain, upper hemicontinuity, and the membership fixed point. It remains
`M1`; the external near-match is neither locally integrated nor exact.

## M0320-T-COMPACT

`compact_of_closed_bounded` checks the Euclidean compactness transport against
the pinned mathlib API. It closes only this transport.

## M0320-T-GRAPH

This bridge owns the nontrivial regularity conversion. It must prove closedness
of the explicitly frozen `CorrespondenceGraph K F`; naming it as a premise in
the composition theorem does not close it.

## M0320-C-CORE

The core consumes compact convex `K`, nonempty closed convex values contained
in `K`, and graph closedness. The audited harfe theorem is a credible source
candidate, but license, toolchain compatibility, terminal provenance, and
local kernel checking remain open.

## M0320-T-SUBTYPE

This node owns all ambient-to-subtype conversions and the exact wrapper from
the external declaration. It cannot be merged into the core or hidden as
"integration" work.

## M0320-T-ASSEMBLE

`root_of_closedGraph_packages` is checked Lean composition from the compactness
transport, graph bridge, and core to the exact root. Its two package arguments
are an explicit open cut set, not axioms or accepted proof bodies.

## M0320-S-STATEMENT

The existing canonical statement and its mutations remain the scope boundary.

## M0320-S-FOUNDATION

The final transitive axiom, TCB, import, no-oracle, freshness, and replay
profiles remain release work.

## M0320-X-SOURCE

Primary-source premise and transition review remains required independently of
machine proof work. The existing crosswalk is not an `H0` review receipt.

## M0320-X-PROVENANCE

This informational overlay must identify every wrapper and terminal body,
including the external archive and license. It supplies no proof credit.

## Frozen boundary

There are 10 unique obligations. Eight are machine-required, nine are
human-source-required where applicable, and all 10 require readable coverage.
Any split, merge, exclusion, or eligibility correction requires registry v2
and an append-only delta. The root is open and theorem completion is false.
