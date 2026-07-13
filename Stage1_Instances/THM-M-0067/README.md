# THM-M-0067 intake dossier

This directory is the fail-closed `planned` intake dossier for `THM-M-0067`, the catalog item
`马施克定理` (Maschke's theorem). The received claim is only:

> A finite-group representation is completely reducible when the characteristic does not divide
> the group order.

The catalog does not identify a source edition or theorem, the scalar field, whether
finite-dimensionality is required, the representation convention, or the exact meaning of
"completely reducible." These choices change the proposition. Consequently this intake records
the recognizable Maschke theorem family but deliberately leaves the canonical mathematical
statement and Lean target unset. Selecting a standard formulation here would invent missing
mathematics and would exceed the assigned intake phase.

Pinned mathlib contains a very strong direct candidate in `Mathlib.RepresentationTheory.Maschke`.
For a finite group `G`, a field `k` in which `Nat.card G` is nonzero, and a representation `rho`,
it synthesizes `Representation.IsSemisimpleRepresentation rho`. That conclusion means every
subrepresentation has a complement. The module itself warns that the usual finite-dimensional
direct-sum-of-irreducibles statement is future work. The candidate is therefore an authentic
discovery lead, not an accepted source-to-target transport or proof receipt.

The authoritative structured scope record is [instance.json](instance.json). The proposition-
changing choices and exclusions are in [scope-map.md](scope-map.md), the received-source and Lean
candidate mapping is in [source-statement-crosswalk.md](source-statement-crosswalk.md), and the
remaining phases are open in [task-dag.json](task-dag.json).

Status boundary: provisional, self-tested planned intake only. No canonical target, source `H0`,
machine `M0`, readable `R0`, accepted state, audit completion, theorem completion, or master
acceptance is claimed.
