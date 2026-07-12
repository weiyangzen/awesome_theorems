import Mathlib.FieldTheory.Galois.Abelian
import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.NumberField.ClassNumber
import Mathlib.Topology.Algebra.Group.Quotient

/-!
Discovery-only checks for pinned APIs adjacent to the under-specified THM-M-0015 catalog entry.

These declarations do not define source-faithful multiplicative ideles, norm maps, a global Artin
map, Frobenius normalization, or the Artin reciprocity theorem. They provide no statement or proof
credit.
-/

open scoped NumberField

#check NumberField
#check NumberField.AdeleRing
#check NumberField.AdeleRing.algebraMap_injective
#check NumberField.AdeleRing.principalSubgroup
#check ClassGroup
#check IsAbelianGalois
#check QuotientGroup.mk'
#check QuotientGroup.ker_mk'
