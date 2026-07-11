import Mathlib.NumberTheory.NumberField.Basic

universe u

open scoped NumberField

-- Expected rejection: the number-field instance cannot be bound before its field instance exists.
example : ∀ (K : Type u) [NumberField K] [Field K],
    IsDedekindDomain (NumberField.RingOfIntegers K) := by
  intro K _ _
  infer_instance
