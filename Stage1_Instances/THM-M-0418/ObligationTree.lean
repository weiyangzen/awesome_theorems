import Mathlib.NumberTheory.NumberField.ClassNumber

/-!
# THM-M-0418 obligation composition

This checks the single terminal body and the exact repo-local adapter selected
by the frozen architecture. It does not duplicate the upstream proof body.
-/

open scoped nonZeroDivisors Real
open Module NumberField Ideal Nat

namespace Stage1Instances.THM_M_0418

universe u

/-- Exact root composition through the one audited terminal proof body. -/
theorem minkowskiIdealClassBound_obligationRoot :
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

#print axioms NumberField.exists_ideal_in_class_of_norm_le
#print axioms minkowskiIdealClassBound_obligationRoot

end Stage1Instances.THM_M_0418
