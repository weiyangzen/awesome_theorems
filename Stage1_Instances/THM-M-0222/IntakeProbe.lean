import Mathlib.Analysis.Complex.CauchyIntegral

/-!
# THM-M-0222 discovery-only intake probe

These checks authenticate strong pinned Cauchy-integral-formula candidates and their current axiom
reports. They do not select the catalog's exact source variant, declare the target proposition,
audit proof-body provenance, or supply proof credit.
-/

#check Complex.two_pi_I_inv_smul_circleIntegral_sub_inv_smul_of_differentiable_on_off_countable
#check Complex.circleIntegral_sub_inv_smul_of_differentiable_on_off_countable
#check DiffContOnCl.circleIntegral_sub_inv_smul
#check DiffContOnCl.two_pi_i_inv_smul_circleIntegral_sub_inv_smul
#check DifferentiableOn.circleIntegral_sub_inv_smul
#check Complex.circleIntegral_div_sub_of_differentiable_on_off_countable

#print axioms Complex.two_pi_I_inv_smul_circleIntegral_sub_inv_smul_of_differentiable_on_off_countable
#print axioms Complex.circleIntegral_div_sub_of_differentiable_on_off_countable
