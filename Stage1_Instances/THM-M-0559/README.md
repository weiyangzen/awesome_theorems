# THM-M-0559 rev-5.6 dossier

This directory is the `planned` intake dossier for the Whitehead theorem. It freezes the
human-level target as follows: a continuous weak homotopy equivalence between CW complexes is a
homotopy equivalence, with weak equivalence meaning a bijection on path components and
isomorphisms on every positive-dimensional based homotopy group at every basepoint.

The source metadata's phrase "weak homotopy equivalence and homotopy equivalence" does not by
itself fix connectedness, basepoints, or whether the conclusion concerns the given map. The scope
map makes those choices explicit. The conclusion requires the given map to be the forward map of
a homotopy equivalence, not merely the existence of some unrelated equivalence of the spaces.

The exact Lean target is now frozen in `Statement.lean`. It defines quotient-respecting maps on
`ZerothHomotopy` and `HomotopyGroup.Pi`, uses whole-space `CWComplex Set.univ` instances, and
requires the resulting homotopy equivalence to have forward map exactly `f`.

Lifecycle remains `planned`, with provisional root vector `[H3, M4, R4]`. Statement elaboration is
worker-self-tested pending master acceptance. No primary-source fidelity, machine proof, audit
completion, or theorem completion is claimed.
