import Mathlib.NumberTheory.NumberField.Cyclotomic.Basic

-- Expected failure: the excluded zero boundary is not definitionally nonzero.
example (n : ℕ) : (n = 0) = (n ≠ 0) := by
  rfl
