# THM-M-0007 rev-5.6 intake

This directory is the `planned` intake for the Grothendieck spectral sequence. The target is the
cohomological spectral sequence for a composite of left-exact functors, under the usual condition
that the first functor sends injectives to objects acyclic for the second.

The legacy Lean module is discovery evidence only. It provides a useful proposed object-level
boundary, but its abstract `spectralSequence : Type` does not encode pages, differentials, or
convergence and is not accepted as the exact statement or a proof. The provisional root vector is
`[H2, M4, R4]`; no theorem completion is claimed.

The scope map and source crosswalk identify the source edition and the choices that the statement
phase must freeze. The remaining rev-5.6 nodes are recorded in `task-dag.json`, and reproducible
intake checks are recorded in `validation.md`.
