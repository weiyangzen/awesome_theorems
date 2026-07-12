# THM-M-0557 rev-5.6 dossier

This directory is the fail-closed `planned` intake for the repository label "homotopy groups". The
source inventory gives only "higher homotopy groups of topological spaces", attributed to Witold
Hurewicz in 1935. That phrase names a construction and theorem family, not one proposition with a
fixed domain, binder order, and conclusion.

The statement phase selects the construction proposition: for every pointed topological space,
`pi_(n+1)` carries a group structure and `pi_(n+2)` carries a commutative group structure.
`Statement.lean` elaborates this dimension-parametric target against the pinned mathlib
generalized-cube-loop quotient, with no connectedness or separation hypotheses. Structural
mutations protect the dimension cutoffs, generality, and pointed binder.

Functoriality, homotopy invariance, sphere-map transports, and computations are excluded from this
exact root. The provisional root vector remains `[H1, M4, R4]`: exact statement elaboration does
not supply historical source acceptance, formal-anchor audit, proof, audit completion, or theorem
completion.

The scope map records the proposition-changing choices, the crosswalk separates repository
metadata from source evidence, and the task DAG keeps every downstream phase open. The performed
intake checks and their limits are recorded in `validation.md`.
