import Mathlib.NumberTheory.NumberField.Basic

universe u

open scoped NumberField

-- Expected rejection: removing the finite-extension hypothesis changes and under-specifies the claim.
example : ∀ (K : Type u) [Field K], IsDedekindDomain (NumberField.RingOfIntegers K) := by
  intro K _
  infer_instance
