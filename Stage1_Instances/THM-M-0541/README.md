# THM-M-0541 rev-5.6 intake

This directory is the `planned` intake for simplicial homology. The repository source phrase,
"homology of a simplicial complex," names a construction rather than one uniquely determined
theorem. This intake therefore freezes the intended result family: simplicial chains with their
alternating boundary form a chain complex, its degreewise homology defines simplicial homology, and
simplicial maps induce the corresponding maps on homology.

The precise coefficient category, orientation convention, treatment of the empty simplex, and
reduced versus unreduced theory remain statement-phase decisions tied to a selected source. The
mathlib probe records adjacent APIs only; it is not a canonical target or proof. The provisional
root vector is `[H2, M3, R4]`. No accepted proof state, audit completion, or theorem completion is
claimed.

The scope map, source crosswalk, and open task DAG define the downstream work. Exact intake checks
and their results are recorded in `validation.md`.
