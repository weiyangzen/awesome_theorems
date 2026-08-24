# Machine-checked audit candidate

The proposed root is classified `M0-L`: a claim-owned exact wrapper over a
complete local proof composition. The frozen FormalConjectures declaration is
statement provenance only; its `sorryAx` body is excluded. The candidate
declaration census and edge list are in `machine-closure.json`.

Worker validation is intentionally `--no-lean`. Therefore `M0-L`, trust zero,
the observed axiom set, semantic identity, cold from-source replay, and all
mutation outcomes remain subject to independent canonical Master compilation
and recomputation after harvest. Release is forbidden if that recomputation
changes the root expression, finds an unreviewed bodyless constant, observes
`sorryAx`, or leaves a root-relevant node open.
