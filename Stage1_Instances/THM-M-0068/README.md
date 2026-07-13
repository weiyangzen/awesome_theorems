# THM-M-0068 intake dossier

This directory is the fail-closed `planned` intake dossier for `THM-M-0068`, the catalog item
`弗罗贝尼乌斯定理` (Frobenius theorem). The received claim is only:

> Orthogonality relations of group characters.

The gloss identifies a representation-theoretic theorem family, but not one exact theorem.
It does not choose row orthogonality of irreducible characters, column orthogonality, or a
completeness consequence; nor does it fix the group, scalar field, normalization, involution,
irreducibility convention, or equality criterion. Intake therefore preserves the family while
leaving the canonical mathematical statement and Lean target unset.

Pinned mathlib contains strong direct leads in `Mathlib.RepresentationTheory.Character`.
`FDRep.char_orthonormal` and `Representation.char_orthonormal` prove a normalized irreducible-
character row-orthogonality relation for a finite group over an algebraically closed field when
the group cardinal is invertible. The same module identifies the scalar product with the dimension
of an equivariant Hom space. The discovery probe authenticates these declarations and their
reported axioms, but does not treat one as the catalog's exact claim or as accepted proof evidence.

The structured scope authority is [instance.json](instance.json). Proposition-changing decisions
and exclusions are in [scope-map.md](scope-map.md), the source and formal-candidate mapping is in
[source-statement-crosswalk.md](source-statement-crosswalk.md), and all downstream phases remain
open in [task-dag.json](task-dag.json).

Status boundary: provisional, self-tested planned intake only. No exact source proposition,
canonical target, accepted proof state, audit completion, theorem completion, or master acceptance
is claimed.
