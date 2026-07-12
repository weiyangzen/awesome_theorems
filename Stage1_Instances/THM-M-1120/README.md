# THM-M-1120 rev-5.6 intake

This directory is the fail-closed `planned` intake for Cardy's formula. The repository inventory
only says "crossing probability for percolation" and dates the entry to 1992. That is not enough
to select one proposition: the lattice/model, critical parameter, discrete domains and boundary
arcs, convergence mode, conformal normalization, and the exact hypergeometric or triangular form
all change the theorem.

The intended theorem family is the conformally invariant scaling limit of a critical planar
percolation crossing probability in a simply connected domain with four ordered boundary points.
The limit is the Cardy function of the conformal cross-ratio (equivalently, a coordinate after a
normalized conformal map to a triangle). The rigorous theorem commonly associated with this
formula is Smirnov's result for critical site percolation on the triangular lattice; Cardy's 1992
paper is the original physics derivation. The statement phase must select and inspect the exact
rigorous source formulation rather than silently treating the prediction as its own proof.

The provisional root vector is `[H2, M4, R4]`. No exact Lean target, source acceptance, formal
anchor, audit completion, or theorem completion is claimed. [scope-map.md](scope-map.md) records
the proposition-changing choices, [source-statement-crosswalk.md](source-statement-crosswalk.md)
records the source boundary, and [task-dag.json](task-dag.json) leaves all dependent work open.
The exact intake checks are in [validation.md](validation.md).
