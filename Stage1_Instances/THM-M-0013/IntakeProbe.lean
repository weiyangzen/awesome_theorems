import Mathlib.FieldTheory.Galois.Basic
import Mathlib.FieldTheory.Galois.Infinite

/-!
Discovery-only checks for the two standard Galois-correspondence scopes exposed by pinned mathlib.

The catalog does not select the finite correspondence with all subgroups or the infinite
correspondence with closed subgroups. This file deliberately defines no canonical target and
assigns no proof credit to either candidate.
-/

#check IntermediateField.fixedField
#check IntermediateField.fixingSubgroup
#check IntermediateField.fixingSubgroup_fixedField
#check IsGalois.fixedField_fixingSubgroup
#check IsGalois.intermediateFieldEquivSubgroup

#check InfiniteGalois.fixingSubgroup_isClosed
#check InfiniteGalois.fixedField_fixingSubgroup
#check InfiniteGalois.fixingSubgroup_fixedField
#check InfiniteGalois.IntermediateFieldEquivClosedSubgroup
#check InfiniteGalois.isOpen_iff_finite
#check InfiniteGalois.normalAutEquivQuotient
