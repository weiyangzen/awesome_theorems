import Mathlib.NumberTheory.NumberField.Cyclotomic.Basic

universe uK

-- Expected failure: the canonical target cannot be formed after removing `Field K`.
#check fun (K : Type uK) [Algebra ℚ K] [NumberField K]
    [IsAbelianGalois ℚ K] =>
  ∃ n : ℕ, n ≠ 0 ∧
    letI : Algebra ℚ (CyclotomicField n ℚ) :=
      CyclotomicField.algebraBase n ℚ ℚ
    Nonempty (K →ₐ[ℚ] CyclotomicField n ℚ)
