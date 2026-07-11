import Mathlib.NumberTheory.NumberField.ClassNumber

/-!
# THM-M-0415 anchor-audit probes

This module checks the exact pinned mathlib instance and its immediate general
class-number construction. It is an audit probe, not release evidence.
-/

open scoped NumberField

namespace Stage1Instances.THM_M_0415.AnchorAudit

universe u

def CanonicalTarget : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    Finite (ClassGroup (NumberField.RingOfIntegers K))

/-- Exact wrapper candidate from the pinned mathlib `Fintype` instance to the
canonical source-level `Finite` conclusion. -/
theorem canonicalTarget_mathlib_candidate : CanonicalTarget.{u} := by
  intro K _ _
  letI : Fintype (ClassGroup (NumberField.RingOfIntegers K)) :=
    NumberField.RingOfIntegers.instFintypeClassGroup K
  exact Finite.of_fintype (ClassGroup (NumberField.RingOfIntegers K))

end Stage1Instances.THM_M_0415.AnchorAudit

#check NumberField.RingOfIntegers.instFintypeClassGroup
#check ClassGroup.fintypeOfAdmissibleOfFinite
#check ClassGroup.fintypeOfAdmissibleOfAlgebraic
#check ClassGroup.mkMMem_surjective
#print axioms NumberField.RingOfIntegers.instFintypeClassGroup
#print axioms ClassGroup.fintypeOfAdmissibleOfFinite
#print axioms Stage1Instances.THM_M_0415.AnchorAudit.canonicalTarget_mathlib_candidate
