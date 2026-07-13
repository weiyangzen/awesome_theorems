# THM-M-0096 rev-5.6 intake

`THM-M-0096` is the representation-theory catalog item named the Chevalley theorem. The repository
attributes it to Claude Chevalley in 1948 and gives only the gloss "an integral basis of a
semisimple Lie algebra." The attribution and `verified` label are untrusted inventory metadata
under rev-5.6.

## Intake result

This directory is a fail-closed `planned` dossier. The gloss points toward the Chevalley-basis
theorem family, but it is not an exact proposition. It does not select the scalar field, define
semisimplicity or "integral basis," distinguish integer structure constants from a Lie-ring
`Z`-form, name the Cartan and root data, state existence versus normalization or uniqueness, or
settle boundary cases. Filling those clauses from mathematical familiarity would invent a target.

Pinned mathlib's bibliography and module documentation name Serre's *Complex Semisimple Lie
Algebras*, Chapter V, Sections 4 and 6, as a reference for the stronger Weyl/Chevalley-basis
concept. That book was not independently inspected in this intake, the catalog does not cite it,
and no definition, assumption, proof-node, correction, or independent-review crosswalk has been
admitted. It is an `H1` bibliographic lead, not `H0` evidence.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned APIs. `LieAlgebra.Basis` captures an integer Cartan
matrix and part of the Chevalley-Serre relations, but its own module says further structure is
needed for a Weyl or Chevalley basis and lists both that definition and existence for every
semisimple Lie algebra as TODOs. The Geck construction supplies such a weaker basis only for the Lie
algebra it constructs from reduced irreducible crystallographic root data. The Serre construction
likewise constructs a new quotient Lie algebra from a Cartan matrix. Neither result is the received
existence theorem for an arbitrary semisimple Lie algebra.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: a standard published-source lead exists but exact source fidelity is open; no usable
exact formal artifact is credited; and no source-faithful reconstruction can attach to an unfrozen
root. All six downstream tasks remain open. No accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
