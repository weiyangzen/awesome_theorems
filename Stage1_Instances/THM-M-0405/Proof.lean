import Statement
import Mathlib.Tactic

/-!
# THM-M-0405 proof execution

This module implements algebraic normalization leaves shared by the frozen
Lucas and Lehmer branches.  It does not assert the still-missing
Bilu-Hanrot-Voutier primitive-divisor bridge.
-/

namespace Stage1.THM_M_0405

/-- A nontorsion quotient with nonzero denominator cannot come from equal
numerator and denominator. -/
theorem ne_of_ratioNotRootOfUnity {alpha beta : Complex} (hbeta : beta ≠ 0)
    (hratio : RatioNotRootOfUnity alpha beta) : alpha ≠ beta := by
  intro halpha
  apply hratio 1 Nat.zero_lt_one
  simp [halpha, hbeta]

namespace LucasPair

/-- The first component of a Lucas pair is nonzero. -/
theorem alpha_ne_zero (L : LucasPair) : L.alpha ≠ 0 := by
  have hproduct : (L.product : Complex) ≠ 0 := by
    exact_mod_cast L.product_ne_zero
  rw [← L.product_eq] at hproduct
  intro halpha
  exact hproduct (by simp [halpha])

/-- The second component of a Lucas pair is nonzero. -/
theorem beta_ne_zero (L : LucasPair) : L.beta ≠ 0 := by
  have hproduct : (L.product : Complex) ≠ 0 := by
    exact_mod_cast L.product_ne_zero
  rw [← L.product_eq] at hproduct
  intro hbeta
  exact hproduct (by simp [hbeta])

/-- The two components of a Lucas pair are distinct. -/
theorem alpha_ne_beta (L : LucasPair) : L.alpha ≠ L.beta :=
  ne_of_ratioNotRootOfUnity L.beta_ne_zero L.ratio_not_root_of_unity

/-- The quotient denominator in every Lucas term identity is nonzero. -/
theorem denominator_ne_zero (L : LucasPair) : L.alpha - L.beta ≠ 0 :=
  _root_.sub_ne_zero.mpr L.alpha_ne_beta

/-- The stored integral discriminant is the square of the quotient
denominator. -/
theorem coe_discriminant (L : LucasPair) :
    (L.discriminant : Complex) = (L.alpha - L.beta) ^ 2 := by
  simp only [discriminant, Int.cast_sub, Int.cast_pow, Int.cast_ofNat,
    Int.cast_mul]
  rw [← L.sum_eq, ← L.product_eq]
  ring

/-- The defining identity forces the zeroth Lucas term to be zero. -/
theorem term_zero (L : LucasPair) : L.term 0 = 0 := by
  have hmul : (L.term 0 : Complex) * (L.alpha - L.beta) = 0 := by
    simpa using L.term_spec 0
  have hcast : (L.term 0 : Complex) = 0 :=
    (mul_eq_zero.mp hmul).resolve_right L.denominator_ne_zero
  exact_mod_cast hcast

/-- The defining identity forces the first Lucas term to be one. -/
theorem term_one (L : LucasPair) : L.term 1 = 1 := by
  have hmul : (L.term 1 : Complex) * (L.alpha - L.beta) =
      1 * (L.alpha - L.beta) := by
    simpa using L.term_spec 1
  have hcast : (L.term 1 : Complex) = 1 :=
    mul_right_cancel₀ L.denominator_ne_zero hmul
  exact_mod_cast hcast

end LucasPair

namespace LehmerPair

/-- The first component of a Lehmer pair is nonzero. -/
theorem alpha_ne_zero (L : LehmerPair) : L.alpha ≠ 0 := by
  have hproduct : (L.product : Complex) ≠ 0 := by
    exact_mod_cast L.product_ne_zero
  rw [← L.product_eq] at hproduct
  intro halpha
  exact hproduct (by simp [halpha])

/-- The second component of a Lehmer pair is nonzero. -/
theorem beta_ne_zero (L : LehmerPair) : L.beta ≠ 0 := by
  have hproduct : (L.product : Complex) ≠ 0 := by
    exact_mod_cast L.product_ne_zero
  rw [← L.product_eq] at hproduct
  intro hbeta
  exact hproduct (by simp [hbeta])

/-- The two components of a Lehmer pair are distinct. -/
theorem alpha_ne_beta (L : LehmerPair) : L.alpha ≠ L.beta :=
  ne_of_ratioNotRootOfUnity L.beta_ne_zero L.ratio_not_root_of_unity

/-- The odd-index quotient denominator is nonzero. -/
theorem oddDenominator_ne_zero (L : LehmerPair) : L.alpha - L.beta ≠ 0 :=
  _root_.sub_ne_zero.mpr L.alpha_ne_beta

/-- The sum of the two components is nonzero. -/
theorem add_ne_zero (L : LehmerPair) : L.alpha + L.beta ≠ 0 := by
  intro hsum
  have hsquare : (L.sumSquare : Complex) = 0 := by
    rw [← L.sumSquare_eq, hsum]
    simp
  have : L.sumSquare = 0 := by
    exact_mod_cast hsquare
  exact L.sumSquare_ne_zero this

/-- The even-index quotient denominator is nonzero. -/
theorem sq_sub_sq_ne_zero (L : LehmerPair) :
    L.alpha ^ 2 - L.beta ^ 2 ≠ 0 := by
  rw [show L.alpha ^ 2 - L.beta ^ 2 =
      (L.alpha - L.beta) * (L.alpha + L.beta) by ring]
  exact mul_ne_zero L.oddDenominator_ne_zero L.add_ne_zero

/-- The stored integral discriminant is the square of the odd-index
denominator. -/
theorem coe_discriminant (L : LehmerPair) :
    (L.discriminant : Complex) = (L.alpha - L.beta) ^ 2 := by
  simp only [discriminant, Int.cast_sub, Int.cast_ofNat, Int.cast_mul]
  rw [← L.sumSquare_eq, ← L.product_eq]
  ring

/-- The stored even-denominator factor is the square of the even-index
denominator. -/
theorem coe_squaredEvenDenominator (L : LehmerPair) :
    (L.squaredEvenDenominator : Complex) =
      (L.alpha ^ 2 - L.beta ^ 2) ^ 2 := by
  simp only [squaredEvenDenominator, Int.cast_mul]
  rw [L.coe_discriminant, ← L.sumSquare_eq]
  ring

/-- The odd-index defining identity forces the first Lehmer term to be one. -/
theorem term_one (L : LehmerPair) : L.term 1 = 1 := by
  have hmul : (L.term 1 : Complex) * (L.alpha - L.beta) =
      1 * (L.alpha - L.beta) := by
    simpa using L.term_spec_odd 1 (by decide)
  have hcast : (L.term 1 : Complex) = 1 :=
    mul_right_cancel₀ L.oddDenominator_ne_zero hmul
  exact_mod_cast hcast

/-- The even-index defining identity forces the second Lehmer term to be one. -/
theorem term_two (L : LehmerPair) : L.term 2 = 1 := by
  have hmul : (L.term 2 : Complex) * (L.alpha ^ 2 - L.beta ^ 2) =
      1 * (L.alpha ^ 2 - L.beta ^ 2) := by
    simpa using L.term_spec_even 2 (by decide)
  have hcast : (L.term 2 : Complex) = 1 :=
    mul_right_cancel₀ L.sq_sub_sq_ne_zero hmul
  exact_mod_cast hcast

end LehmerPair

#print axioms ne_of_ratioNotRootOfUnity
#print axioms LucasPair.alpha_ne_zero
#print axioms LucasPair.beta_ne_zero
#print axioms LucasPair.alpha_ne_beta
#print axioms LucasPair.denominator_ne_zero
#print axioms LucasPair.coe_discriminant
#print axioms LucasPair.term_zero
#print axioms LucasPair.term_one
#print axioms LehmerPair.alpha_ne_zero
#print axioms LehmerPair.beta_ne_zero
#print axioms LehmerPair.alpha_ne_beta
#print axioms LehmerPair.oddDenominator_ne_zero
#print axioms LehmerPair.add_ne_zero
#print axioms LehmerPair.sq_sub_sq_ne_zero
#print axioms LehmerPair.coe_discriminant
#print axioms LehmerPair.coe_squaredEvenDenominator
#print axioms LehmerPair.term_one
#print axioms LehmerPair.term_two

#eval IO.println "M0405_PROOF_AXIOM_AUDIT_END"

end Stage1.THM_M_0405
