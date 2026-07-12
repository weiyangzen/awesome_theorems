# THM-M-1121 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "Smirnov theorem" and
the gloss "conformal invariance of triangular-lattice percolation". That wording does not yet
identify one proposition. Smirnov's result is commonly presented through convergence of critical
site-percolation crossing probabilities to Cardy's conformally invariant formula, while broader
accounts also discuss exploration paths and scaling limits. Those formulations require different
domains, observables, topology, and boundary regularity.

The intended family is critical independent site percolation on the triangular lattice (equivalently
hexagonal-face coloring), with mesh tending to zero in a planar domain and a source-specified
crossing observable converging to its conformally invariant/Cardy limit. The exact primary theorem,
domain class, boundary markings, discrete approximation, event, and convergence mode remain open
for the statement phase. The provisional root vector is `[H1, M4, R4]`. No exact Lean target,
accepted source review, formal candidate, audit completion, or theorem completion is claimed.

`scope-map.md` records the proposition-changing choices,
`source-statement-crosswalk.md` records the candidate source and unresolved mapping, and
`task-dag.json` leaves every downstream phase open. Intake checks are recorded in `validation.md`.
