import Mathlib.NumberTheory.NumberField.Basic

/-!
An independently written narrow kernel probe for THM-M-0413 validation. This deliberately does
not import `Proof.lean`; it reconstructs the exact root from the pinned number-field instance.
-/

namespace Stage1.THMM0413.Validation

universe u

open scoped NumberField

/-- Independent exact-type probe for the frozen root statement. -/
theorem independentExactRoot :
    forall (K : Type u) [Field K] [NumberField K],
      IsDedekindDomain (NumberField.RingOfIntegers K) := by
  intro K _ _
  exact NumberField.RingOfIntegers.instIsDedekindDomain K

#check independentExactRoot
#print axioms independentExactRoot

end Stage1.THMM0413.Validation
