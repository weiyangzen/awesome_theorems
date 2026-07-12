# THM-M-1119 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "Kesten theorem". The
source inventory gives Harry Kesten, the year 1980, and only the gloss "critical probability of
two-dimensional percolation". That wording strongly points to the bond-percolation theorem
`p_c = 1/2` for the square lattice, but it does not state the graph, percolation model, definition of
the critical parameter, or exact source proposition.

The statement phase now freezes the title-selected equality from Kesten's 1980 paper: for
independent bond percolation on the nearest-neighbor square lattice `Z x Z`, the critical parameter
defined from positive probability that the origin lies in an infinite open cluster is `1/2`.
`Statement.lean` elaborates the exact target, its graph and product-measure definitions, a checked
expanded form, and four non-equivalent mutations using the pinned Lean environment. Absence of an
infinite cluster at criticality is not silently added to the title-selected root.

This remains a `planned` dossier pending master acceptance. The root vector stays
`[H2, M4, R4]`: statement elaboration supplies no Kesten proof, `H0` source review, formal-anchor
audit, audit completion, or theorem completion.

`statement.json` and `statement-validation.md` record the formal target, expression fingerprint,
environment, mutations, and exact commands. The intake artifacts remain as discovery history, and
all later task-DAG phases remain open.
