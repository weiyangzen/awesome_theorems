# THM-M-0992 obligation tree

This v1 registry was frozen from the exact statement and immutable anchor
audit before downstream proof acceptance was observed. The proof architecture
is deliberately small because the pinned mathlib declaration exposes the exact
substantive inequality; its depth is still represented as a terminal bridge
obligation rather than hidden inside a one-line wrapper.

| Obligation | Typed output | Current boundary |
|---|---|---|
| `M0992-ROOT` | Exact `ChebyshevTarget` | open |
| `M0992-S-STATEMENT` | Frozen universes, binders, event, and quotient | checked interface |
| `M0992-B-PROB-FINITE` | `IsProbabilityMeasure` supplies `IsFiniteMeasure` | checked by composition |
| `M0992-A-VARIANCE` | Exact finite-measure variance bound | pinned M0-W candidate |
| `M0992-T-COMPOSE` | Anchor package implies exact root | kernel checked conditionally |
| `M0992-X-SOURCE` | Primary-source crosswalk | open |
| `M0992-X-PROVENANCE` | Terminal and transitive provenance certificate | open |
| `M0992-X-TRUST` | Foundation, TCB, axiom, and no-oracle certificate | open |

The proof graph requires `M0992-T-COMPOSE` for the root, and composition in
turn requires both `M0992-B-PROB-FINITE` and `M0992-A-VARIANCE`. Reciprocal
`composes` edges make every child-to-parent use explicit. Separate refinement,
provenance, evidence, trust, documentation, and workflow graphs prevent source
or audit evidence from receiving proof credit.

No node in this phase is an accepted proof receipt. Root closure, H0, full
provenance/trust validation, readable reconstruction, hermetic replay, and
independent verification remain downstream gates.
