# THM-M-0559 rev-5.6 intake

This directory is the `planned` intake dossier for the Whitehead theorem. It freezes the
human-level target as follows: a continuous weak homotopy equivalence between CW complexes is a
homotopy equivalence, with weak equivalence meaning a bijection on path components and
isomorphisms on every positive-dimensional based homotopy group at every basepoint.

The source metadata's phrase "weak homotopy equivalence and homotopy equivalence" does not by
itself fix connectedness, basepoints, or whether the conclusion concerns the given map. The scope
map makes those choices explicit. The conclusion requires the given map to be the forward map of
a homotopy equivalence, not merely the existence of some unrelated equivalence of the spaces.

The pinned Lean environment contains CW-complex, homotopy-group, continuous-map, and homotopy-
equivalence interfaces. `IntakeSurface.lean` checks those names only; it is not a formal statement
or proof of Whitehead's theorem. The exact induced maps on homotopy groups and their compatibility
with the chosen CW interface remain statement-phase work.

Lifecycle is `planned`, with provisional root vector `[H3, M4, R4]`. No exact Lean target, primary-
source fidelity, machine proof, audit completion, or theorem completion is claimed.
