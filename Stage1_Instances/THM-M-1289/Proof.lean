import ObligationTree

/-!
# THM-M-1289 proof-phase bodies

This module closes the positivity and smoothness components of the frozen
Aubin-Talenti architecture.  The PDE, integrability, and sharp-extremal
components remain explicit premises.
-/

namespace Stage1Instances.THM_M_1289

open scoped ENNReal RealInnerProductSpace
open MeasureTheory

private lemma dimension_factors_pos (n : Nat) (hn : 3 <= n) :
    0 < (n : Real) * ((n : Real) - 2) := by
  have hnR : (3 : Real) <= n := by exact_mod_cast hn
  have hn0 : (0 : Real) < n := lt_of_lt_of_le (by norm_num) hnR
  have hn2 : (0 : Real) < (n : Real) - 2 := by linarith
  exact mul_pos hn0 hn2

private lemma bubble_denominator_pos {n : Nat} (a x : Euclidean n)
    (lambda : Real) (hl : 0 < lambda) :
    0 < lambda ^ 2 + ‖x - a‖ ^ 2 := by
  nlinarith [sq_nonneg lambda, sq_nonneg ‖x - a‖]

/-- The normalized bubble is strictly positive at every point. -/
theorem bubble_pos {n : Nat} (hn : 3 <= n) (a : Euclidean n)
    {lambda : Real} (hl : 0 < lambda) (x : Euclidean n) :
    0 < bubble n a lambda x := by
  unfold bubble
  apply mul_pos
  · exact Real.rpow_pos_of_pos (dimension_factors_pos n hn) _
  · apply Real.rpow_pos_of_pos
    exact div_pos hl (bubble_denominator_pos a x lambda hl)

/-- Closed proof body for the frozen pointwise positivity component. -/
theorem positivityComponent_proof : PositivityComponent := by
  intro n hn a lambda hl x
  exact bubble_pos hn a hl x

private lemma contDiff_bubble_denominator {n : Nat} (a : Euclidean n)
    (lambda : Real) :
    ContDiff Real ⊤ (fun x : Euclidean n => lambda ^ 2 + ‖x - a‖ ^ 2) := by
  exact contDiff_const.add ((contDiff_id.sub contDiff_const).norm_sq Real)

/-- The denominator never vanishes at positive scale. -/
private lemma bubble_denominator_ne {n : Nat} (a : Euclidean n)
    {lambda : Real} (hl : 0 < lambda) (x : Euclidean n) :
    lambda ^ 2 + ‖x - a‖ ^ 2 ≠ 0 :=
  (bubble_denominator_pos a x lambda hl).ne'

/-- The normalized bubble is infinitely Frechet differentiable. -/
theorem contDiff_bubble {n : Nat} (a : Euclidean n)
    {lambda : Real} (hl : 0 < lambda) :
    ContDiff Real ⊤ (bubble n a lambda) := by
  unfold bubble
  apply contDiff_const.mul
  apply ContDiff.rpow_const_of_ne
  · exact contDiff_const.div (contDiff_bubble_denominator a lambda)
      (bubble_denominator_ne a hl)
  · intro x
    exact (div_ne_zero hl.ne' (bubble_denominator_ne a hl x))

/-- Closed proof body for the frozen smoothness component. -/
theorem smoothnessComponent_proof : SmoothnessComponent := by
  intro n _hn a lambda hl
  exact contDiff_bubble a hl

/-- Composition with the four analytic components still outside this proof
phase.  In particular, this theorem is not an unconditional root proof. -/
theorem aubinTalentiTarget_of_remaining_components
    (hpde : PDEComponent) (hfun : FunctionNormComponent)
    (hgrad : GradientNormComponent) (hext : ExtremalComponent) :
    AubinTalentiTarget :=
  aubinTalentiTarget_of_components positivityComponent_proof
    smoothnessComponent_proof hpde hfun hgrad hext

#print axioms bubble_pos
#print axioms contDiff_bubble
#print axioms aubinTalentiTarget_of_remaining_components

end Stage1Instances.THM_M_1289
