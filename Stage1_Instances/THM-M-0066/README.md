# THM-M-0066 intake dossier

This directory is the fail-closed `planned` intake dossier for `THM-M-0066`, the catalog item
`舒尔引理` (Schur's lemma). The received claim is only:

> A homomorphism between irreducible representations is either zero or an isomorphism.

The catalog does not identify a source edition or theorem, the acting group or algebra, the scalar
field, finite-dimensionality, the representation and irreducibility conventions, or the exact
meaning of homomorphism and isomorphism. Those choices change the proposition. Consequently this
intake records the recognizable theorem family but deliberately leaves the canonical mathematical
statement and Lean target unset. Selecting a standard formulation here would invent missing
mathematics and would exceed the assigned intake phase.

Pinned mathlib contains a strong direct candidate in
`Mathlib.RepresentationTheory.Irreducible`:
`Representation.IsIrreducible.bijective_or_eq_zero` proves that an intertwining map between two
irreducible monoid representations over a field is bijective or zero. The same module provides
`IntertwiningMap.ofBijective`, which packages the bijective branch as a representation
equivalence. `Mathlib.RingTheory.SimpleModule.Basic` and
`Mathlib.CategoryTheory.Preadditive.Schur` contain related generalizations. These are authentic
discovery leads, not an accepted source-to-target transport or proof receipt.

The authoritative structured scope record is [instance.json](instance.json). The proposition-
changing choices and exclusions are in [scope-map.md](scope-map.md), the received-source and Lean
candidate mapping is in [source-statement-crosswalk.md](source-statement-crosswalk.md), and the
remaining phases are open in [task-dag.json](task-dag.json).

Status boundary: provisional, self-tested planned intake only. No canonical target, source `H0`,
machine `M0`, readable `R0`, accepted state, audit completion, theorem completion, or master
acceptance is claimed.
