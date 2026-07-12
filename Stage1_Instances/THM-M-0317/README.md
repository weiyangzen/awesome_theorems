# THM-M-0317 rev-5.6 intake

This directory is the `planned` intake for the Tychonoff fixed-point theorem. It freezes the
intended theorem family as existence of a fixed point for a continuous self-map of a nonempty
compact convex subset of a locally convex topological real vector space. The source article is
identified, while its exact theorem text and separation conventions remain statement-phase work.

There is no legacy Stage1 Lean slot for this target. A scoped inspection of pinned mathlib found
the constituent `LocallyConvexSpace`, `Convex`, `IsCompact`, `Continuous`, and `IsFixedPt` APIs but
did not locate a Tychonoff fixed-point declaration. This is discovery evidence only, not a complete
anchor audit. The provisional root vector is `[H1, M4, R4]`; no formal statement, proof credit,
audit completion, or theorem completion is claimed.

The scope map, source-statement crosswalk, and open task DAG define the downstream work. Exact
intake checks and results are recorded in `validation.md`.
