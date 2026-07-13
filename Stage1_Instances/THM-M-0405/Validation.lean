import Statement
import Mathlib.Tactic
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0405 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
independently reconstructs four small algebraic consequences of the frozen
pair definitions. It does not prove a primitive-divisor branch or the exact
Bilu-Hanrot-Voutier root.
-/

namespace Stage1.THM_M_0405.Validation

/-- Differential reconstruction of nonvanishing of the second Lucas
component from the stored nonzero product. -/
theorem lucas_beta_ne_zero (L : LucasPair) : L.beta ≠ 0 := by
  have hproduct : (L.product : Complex) ≠ 0 := by
    exact_mod_cast L.product_ne_zero
  rw [← L.product_eq] at hproduct
  intro hbeta
  exact hproduct (by simp [hbeta])

/-- Differential reconstruction of distinctness of the Lucas components. -/
theorem lucas_alpha_ne_beta (L : LucasPair) : L.alpha ≠ L.beta := by
  intro halpha
  apply L.ratio_not_root_of_unity 1 Nat.zero_lt_one
  simp [halpha, lucas_beta_ne_zero L]

/-- Differential reconstruction of the zeroth Lucas term. -/
theorem lucas_term_zero (L : LucasPair) : L.term 0 = 0 := by
  have hmul : (L.term 0 : Complex) * (L.alpha - L.beta) = 0 := by
    simpa using L.term_spec 0
  have hdenominator : L.alpha - L.beta ≠ 0 :=
    _root_.sub_ne_zero.mpr (lucas_alpha_ne_beta L)
  have hcast : (L.term 0 : Complex) = 0 :=
    (mul_eq_zero.mp hmul).resolve_right hdenominator
  exact_mod_cast hcast

/-- Differential reconstruction of the first Lucas term. -/
theorem lucas_term_one (L : LucasPair) : L.term 1 = 1 := by
  have hmul : (L.term 1 : Complex) * (L.alpha - L.beta) =
      1 * (L.alpha - L.beta) := by
    simpa using L.term_spec 1
  have hdenominator : L.alpha - L.beta ≠ 0 :=
    _root_.sub_ne_zero.mpr (lucas_alpha_ne_beta L)
  have hcast : (L.term 1 : Complex) = 1 :=
    mul_right_cancel₀ hdenominator hmul
  exact_mod_cast hcast

assert_no_sorry lucas_beta_ne_zero
assert_no_sorry lucas_alpha_ne_beta
assert_no_sorry lucas_term_zero
assert_no_sorry lucas_term_one
#print sorries lucas_beta_ne_zero
#print sorries lucas_alpha_ne_beta
#print sorries lucas_term_zero
#print sorries lucas_term_one
#print axioms lucas_beta_ne_zero
#print axioms lucas_alpha_ne_beta
#print axioms lucas_term_zero
#print axioms lucas_term_one

end Stage1.THM_M_0405.Validation
