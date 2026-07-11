import Mathlib.NumberTheory.NumberField.Cyclotomic.Basic

-- Expected failure: `n` is intentionally referenced outside its existential scope.
#check letI : Algebra ℚ (CyclotomicField n ℚ) :=
    CyclotomicField.algebraBase n ℚ ℚ
  ∃ n : ℕ, Nonempty (ℚ →ₐ[ℚ] CyclotomicField n ℚ)
