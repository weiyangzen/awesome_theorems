# THM-M-0557 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "homotopy groups". The
source inventory gives only "higher homotopy groups of topological spaces", attributed to Witold
Hurewicz in 1935. That phrase names a construction and theorem family, not one proposition with a
fixed domain, binder order, and conclusion.

The intended family is the construction of the pointed homotopy sets `pi_n(X, x)` from based maps
of an `n`-sphere (equivalently iterated loops), together with their group structure, abelianness in
higher degrees, and functorial/homotopy-invariant behavior. The statement phase must select one
exact source proposition rather than conflate these results. The provisional root vector is
`[H1, M4, R4]`; no exact Lean target, source acceptance, formal-anchor audit, proof, audit
completion, or theorem completion is claimed.

The scope map records the proposition-changing choices, the crosswalk separates repository
metadata from source evidence, and the task DAG keeps every downstream phase open. The performed
intake checks and their limits are recorded in `validation.md`.
