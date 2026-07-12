import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.ODE.Gronwall

/-!
Discovery-only checks for APIs adjacent to the ambiguous THM-M-1336 catalog wording.

These declarations have different statements. Their availability does not select a canonical
target and provides no source-fidelity or proof credit for THM-M-1336.
-/

#check image_le_of_deriv_right_lt_deriv_boundary
#check image_le_of_deriv_right_le_deriv_boundary
#check le_gronwallBound_of_liminf_deriv_right_le
#check norm_le_gronwallBound_of_norm_deriv_right_le
#check dist_le_of_approx_trajectories_ODE
#check dist_le_of_trajectories_ODE
#check ODE_solution_unique
