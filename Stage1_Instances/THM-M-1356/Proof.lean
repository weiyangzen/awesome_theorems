import Statement

/-!
# THM-M-1356 partial proof execution

This module proves the exact degree-one specialization of the frozen
Routh-Hurwitz target.  The arbitrary-degree forward and reverse directions
remain open; no conditional package is treated as a proof body.
-/

namespace Stage1Instances.THM_M_1356

open Polynomial

/-- In degree one, the descending coefficient adapter produces `a₀ X + a₁`. -/
theorem complexPolynomial_fin_one (a : Fin 2 → Real) :
    complexPolynomial a = Polynomial.C (a 0 : Complex) * Polynomial.X +
      Polynomial.C (a 1 : Complex) := by
  rw [complexPolynomial]
  have hr :
      realPolynomial a = Polynomial.C (a 0) * Polynomial.X + Polynomial.C (a 1) := by
    rw [realPolynomial, Polynomial.ofFn_eq_sum_monomial]
    rw [Fin.sum_univ_two]
    change monomial 0 (a 1) + monomial 1 (a 0) = _
    rw [monomial_zero_left, ← C_mul_X_eq_monomial]
    ac_rfl
  rw [hr]
  simp

/-- A positive-leading linear polynomial is strictly stable exactly when its
constant coefficient is positive. -/
theorem strictlyStable_fin_one (a : Fin 2 → Real) (ha : 0 < a 0) :
    IsStrictlyStable a ↔ 0 < a 1 := by
  rw [show IsStrictlyStable a = ∀ z : Complex,
      (Polynomial.C (a 0 : Complex) * Polynomial.X + Polynomial.C (a 1 : Complex)).IsRoot z →
        z.re < 0 by
    unfold IsStrictlyStable
    rw [complexPolynomial_fin_one]]
  constructor
  · intro hs
    let z : Complex := -((a 1 : Real) / a 0)
    have hz :
        (Polynomial.C (a 0 : Complex) * Polynomial.X +
          Polynomial.C (a 1 : Complex)).IsRoot z := by
      rw [Polynomial.IsRoot.def]
      simp only [Polynomial.eval_add, Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_X]
      dsimp [z]
      rw [mul_neg, ← Complex.ofReal_div, ← Complex.ofReal_mul]
      simp [mul_div_cancel₀ _ (ne_of_gt ha)]
    have hneg := hs z hz
    dsimp [z] at hneg
    simp only [Complex.div_ofReal_re, Complex.ofReal_re] at hneg
    have hposdiv : 0 < a 1 / a 0 := neg_lt_zero.mp hneg
    exact (div_pos_iff_of_pos_right ha).mp hposdiv
  · intro ha1 z hz
    rw [Polynomial.IsRoot.def] at hz
    simp only [Polynomial.eval_add, Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_X] at hz
    have hzero : (a 0 : Complex) * z + (a 1 : Complex) = 0 := hz
    have hz_eq : z = -((a 1 : Complex) / (a 0 : Complex)) := by
      calc
        z = -(a 1 : Complex) / (a 0 : Complex) :=
          (eq_div_iff (Complex.ofReal_ne_zero.mpr (ne_of_gt ha))).mpr
            (by simpa [mul_comm] using eq_neg_of_add_eq_zero_left hzero)
        _ = -((a 1 : Complex) / (a 0 : Complex)) := neg_div _ _
    rw [hz_eq]
    rw [← Complex.ofReal_div]
    simp only [Complex.neg_re, Complex.ofReal_re]
    exact neg_lt_zero.mpr (div_pos ha1 ha)

/-- The unique degree-one leading Hurwitz minor is the constant coefficient. -/
theorem hurwitzMinor_fin_one (a : Fin 2 → Real) : hurwitzMinor a 0 = a 1 := by
  simp [hurwitzMinor, hurwitzMatrix, sourceCoefficient]

/-- Exact degree-one instance of the frozen stability/minor equivalence. -/
theorem routhHurwitz_fin_one (a : Fin 2 → Real) (ha : IsPositiveDegreeN a) :
    IsStrictlyStable a ↔ ∀ k : Fin 1, 0 < hurwitzMinor a k := by
  rw [strictlyStable_fin_one a ha]
  constructor
  · intro ha1 k
    fin_cases k
    simpa [hurwitzMinor_fin_one]
  · intro h
    simpa [hurwitzMinor_fin_one] using h 0

#print axioms complexPolynomial_fin_one
#print axioms strictlyStable_fin_one
#print axioms hurwitzMinor_fin_one
#print axioms routhHurwitz_fin_one

end Stage1Instances.THM_M_1356
