# THM-M-0541 rev-5.6 intake

This directory is the `planned` intake for simplicial homology. The repository source phrase,
"homology of a simplicial complex," names a construction rather than one uniquely determined
theorem. This intake therefore freezes the intended result family: simplicial chains with their
alternating boundary form a chain complex, its degreewise homology defines simplicial homology, and
simplicial maps induce the corresponding maps on homology.

The statement phase now freezes ordered, unreduced integral finite chains and the alternating
boundary-square construction in `Statement.lean`. The increasing vertex order fixes orientations;
empty simplices and degree `-1` are excluded. Functoriality is deferred because non-injective and
order-changing vertex maps require a separately checked signed chain-map construction. The mathlib
probe records adjacent APIs only; it is not a proof. The provisional root vector remains
`[H2, M3, R4]`. No accepted proof state, audit completion, or theorem completion is claimed.

The exact formal target and statement-only evidence are recorded in `statement.json` and
`statement-validation.md`. The scope map, source crosswalk, and open task DAG define downstream
work. Intake checks remain recorded in `validation.md`.

The obligation-tree phase freezes registry version 1 in `obligation-registry.json` and all seven
typed graphs in `typed-graphs.json`. Its 35 required mathematical obligations expose the direct
Finsupp boundary construction, ordered-deletion normalization, cancellation branches, and exact
root assembly; `M0541-X3` is a non-proof trust overlay. The registry is architecture only: all
obligations remain open and the first root cut is recorded in `obligation-tree.md`.
