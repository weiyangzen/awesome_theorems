import Mathlib.Analysis.ODE.Gronwall

/-! Discovery-only checks for pinned APIs adjacent to Gronwall's inequality. -/

#check gronwallBound
#check gronwallBound_K0
#check gronwallBound_x0
#check le_gronwallBound_of_liminf_deriv_right_le
#check norm_le_gronwallBound_of_norm_deriv_right_le

#print axioms le_gronwallBound_of_liminf_deriv_right_le
#print axioms norm_le_gronwallBound_of_norm_deriv_right_le
