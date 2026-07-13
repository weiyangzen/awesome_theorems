import Mathlib.Analysis.Complex.Schwarz

/-!
# THM-M-0226 discovery-only intake probe

These checks authenticate pinned Schwarz-lemma interfaces and one prospective two-inequality
specialization. The repository source does not say whether both inequalities or the equality case
belong to its root, so this file does not freeze a canonical target or claim proof credit.
-/

open Metric Set

#check Complex.norm_le_norm_of_mapsTo_ball
#check Complex.norm_deriv_le_one_of_mapsTo_ball
#check Complex.norm_dslope_le_div_of_mapsTo_ball
#check Complex.affine_of_mapsTo_ball_of_norm_dslope_eq_div
#check Complex.affine_of_mapsTo_ball_of_exists_norm_dslope_eq_div'
#check ball_subset_closedBall

theorem prospective_two_inequality_probe (f : ℂ → ℂ)
    (hd : DifferentiableOn ℂ f (ball 0 1))
    (hself : MapsTo f (ball 0 1) (ball 0 1))
    (hzero : f 0 = 0) :
    (∀ z ∈ ball (0 : ℂ) 1, ‖f z‖ ≤ ‖z‖) ∧ ‖deriv f 0‖ ≤ 1 := by
  have hclosed : MapsTo f (ball (0 : ℂ) 1) (closedBall (0 : ℂ) 1) :=
    fun z hz => ball_subset_closedBall (hself hz)
  constructor
  · intro z hz
    exact Complex.norm_le_norm_of_mapsTo_ball hd hclosed hzero (by simpa using hz)
  · exact Complex.norm_deriv_le_one_of_mapsTo_ball hd (by simpa [hzero] using hclosed) one_pos

#print axioms Complex.norm_le_norm_of_mapsTo_ball
#print axioms Complex.norm_deriv_le_one_of_mapsTo_ball
#print axioms Complex.affine_of_mapsTo_ball_of_norm_dslope_eq_div
#print axioms prospective_two_inequality_probe
