import ObligationTree

/-!
# THM-M-1248 partial proof execution

This module closes the lower-order endpoint of the frozen proof route.  The
positive and interior interpolation cases still require the weighted analytic
package recorded in the obligation tree.
-/

namespace Stage1Instances.THM_M_1248

/-- The endpoint/interior split forced by the frozen bounds `0 <= a <= 1`. -/
theorem admissible_parameter_split
    {n : Nat} {p q r alpha beta gamma sigma a : Real}
    (hadm : AdmissibleParameters n p q r alpha beta gamma sigma a) :
    a = 0 ∨ a = 1 ∨ (0 < a ∧ a < 1) := by
  rcases hadm with ⟨_, _, _, _, ha0, ha1, _⟩
  rcases eq_or_lt_of_le ha0 with rfl | ha0
  · exact Or.inl rfl
  rcases eq_or_lt_of_le ha1 with rfl | ha1
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr ⟨ha0, ha1⟩)

/-- At the `a = 0` endpoint, admissibility forces the target and lower-order
weights and exponents to agree. -/
theorem admissible_a_zero_forces_lower_order_parameters
    {n : Nat} {p q r alpha beta gamma sigma : Real}
    (hadm : AdmissibleParameters n p q r alpha beta gamma sigma 0) :
    gamma = beta /\ r = q := by
  rcases hadm with
    ⟨_, _, _, _, _, _, _, _, _, hgamma, hscale, _, _⟩
  norm_num at hgamma hscale
  subst gamma
  have hrqInv : r⁻¹ = q⁻¹ := by
    linarith [hscale]
  exact ⟨rfl, inv_injective hrqInv⟩

/-- The exact Caffarelli-Kohn-Nirenberg estimate at the lower-order endpoint
`a = 0`.  Here the admissibility equations reduce the estimate to reflexivity,
with constant `C = 1`. -/
theorem caffarelliKohnNirenberg_a_zero
    {n : Nat} {p q r alpha beta gamma sigma : Real}
    (hadm : AdmissibleParameters n p q r alpha beta gamma sigma 0) :
    ∃ C : Real, 0 < C ∧
      ∀ u : EuclideanSpace Real (Fin n) -> Real,
        ContDiff Real ⊤ u -> HasCompactSupport u ->
        weightedLp r gamma u ≤
          C * (weightedDerivativeLp p alpha u) ^ (0 : Real) *
            (weightedLp q beta u) ^ (1 - (0 : Real)) := by
  obtain ⟨hgamma, hrq⟩ :=
    admissible_a_zero_forces_lower_order_parameters hadm
  subst gamma
  subst r
  refine ⟨1, by norm_num, ?_⟩
  intro u _ _
  simp

#print axioms admissible_parameter_split
#print axioms admissible_a_zero_forces_lower_order_parameters
#print axioms caffarelliKohnNirenberg_a_zero
#print sorries admissible_parameter_split
#print sorries admissible_a_zero_forces_lower_order_parameters
#print sorries caffarelliKohnNirenberg_a_zero

end Stage1Instances.THM_M_1248
