# THM-M-1119 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "Kesten theorem". The
source inventory gives Harry Kesten, the year 1980, and only the gloss "critical probability of
two-dimensional percolation". That wording strongly points to the bond-percolation theorem
`p_c = 1/2` for the square lattice, but it does not state the graph, percolation model, definition of
the critical parameter, or exact source proposition.

The intended family is therefore frozen as Kesten's critical-probability result for independent
bond percolation on the planar square lattice. The exact primary-source statement, endpoint and
infinite-cluster formulation, graph encoding, and Lean expression remain open for the statement
phase. The provisional root vector is `[H2, M4, R4]`. No exact Lean target, source review, formal
candidate, audit completion, or theorem completion is claimed.

`scope-map.md` records proposition-changing choices,
`source-statement-crosswalk.md` records the source lead and missing mapping, and `task-dag.json`
leaves every downstream phase open. The intake checks are recorded in `validation.md`.
