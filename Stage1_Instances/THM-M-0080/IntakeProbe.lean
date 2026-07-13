import Mathlib.GroupTheory.CoprodI

/-!
# THM-M-0080 discovery-only intake probe

These checks authenticate pinned free-product, reduced-word, free-group, and subgroup interfaces.
They do not select or prove a Kurosh subgroup-decomposition statement.
-/

#check Monoid.CoprodI
#check Monoid.CoprodI.of
#check Monoid.CoprodI.of_injective
#check Monoid.CoprodI.lift
#check Monoid.CoprodI.range_eq_iSup
#check Monoid.CoprodI.Word
#check Monoid.CoprodI.Word.equiv
#check Monoid.CoprodI.FreeGroupBasis.coprodI
#check freeGroupEquivCoprodI
#check Subgroup.map
#check Subgroup.comap
#check Subgroup.subtype
