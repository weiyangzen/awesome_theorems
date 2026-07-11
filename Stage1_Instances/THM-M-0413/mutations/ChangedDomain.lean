import Mathlib.NumberTheory.NumberField.Basic

universe u

open scoped NumberField

-- Expected rejection: a commutative ring is not the number-field domain required by the claim.
example : ∀ (K : Type u) [CommRing K], IsDedekindDomain (NumberField.RingOfIntegers K) := by
  intro K _
  infer_instance
