import Mathlib.NumberTheory.NumberField.ClassNumber

/-!
# THM-M-0418: exact pinned anchor adapter

This module checks the exact representative-form target against the terminal
mathlib declaration selected by the rev-5.6 anchor audit. The proof body is in
the pinned mathlib source; this file is only the repo-local wrapper.
-/

open scoped nonZeroDivisors Real

open Module NumberField Ideal Nat

namespace Stage1Instances.THM_M_0418

universe u

/-- Exact wrapper for the frozen target, backed by the pinned mathlib theorem. -/
theorem minkowskiIdealClassBound_mathlibAnchor :
    ∀ (K : Type u) [Field K] [NumberField K]
      (C : ClassGroup (RingOfIntegers K)),
        ∃ I : (Ideal (RingOfIntegers K))⁰,
          ClassGroup.mk0 I = C ∧
            absNorm (I : Ideal (RingOfIntegers K)) ≤
              (4 / Real.pi) ^ NumberField.InfinitePlace.nrComplexPlaces K *
                ((finrank ℚ K).factorial / (finrank ℚ K) ^ (finrank ℚ K) *
                  Real.sqrt |NumberField.discr K|) := by
  intro K _ _ C
  exact NumberField.exists_ideal_in_class_of_norm_le C

#check NumberField.exists_ideal_in_class_of_norm_le
#print axioms NumberField.exists_ideal_in_class_of_norm_le
#print axioms minkowskiIdealClassBound_mathlibAnchor

end Stage1Instances.THM_M_0418
