# THM-M-0929 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0929`, the catalog entry
named `Burnside引理` (Burnside's lemma). The repository gives only the gloss
`群作用下的轨道计数` (orbit counting under a group action), attributes it to William Burnside
in 1897, and labels it `已验证`. Under rev-5.6 that label is untrusted metadata, not a source audit
or a machine-proof claim.

The gloss identifies the classical Burnside orbit-counting family. It does not specify the exact
formula, domains, ordered binders, finiteness assumptions, fixed-point and orbit conventions,
number system, or whether the multiplication, average/division, or structural-bijection form is
the root. It also supplies no primary citation, edition, theorem/page locator, definition chain,
proof boundary, correction history, errata review, or independent source review. The canonical
human statement and canonical Lean expression therefore remain null at intake. A zbMATH record
identifies Burnside's 1897 *Theory of Groups of Finite Order* as a matching primary-book lead, but
no book text or pinpoint theorem/proof passage was admitted.

Pinned mathlib contains directly named Burnside interfaces in
`Mathlib.GroupTheory.GroupAction.Quotient`. The cardinality theorem
`MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group` says, under its explicit finiteness
instances, that the sum of fixed-point counts is the number of action orbits times the group
cardinality. The preceding `MulAction.sigmaFixedByEquivOrbitsProdGroup` supplies the structural
bijection behind that identity. `IntakeProbe.lean` elaborates their types, additive analogues, and
axiom reports. This authenticates a strong pinned candidate surface and supports provisional `M3`,
but it does not choose a source-identical root, freeze an expression fingerprint, audit terminal
proof provenance, or grant proof credit.

The provisional root vector is `[H1, M3, R4]`: the classical theorem family is recognizable but no
exact human source is accepted; direct pinned formal interfaces exist but no canonical target is
frozen; and no source-faithful readable proof reconstruction is attached to an exact root. All six
downstream phases remain open. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
