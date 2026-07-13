import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.Analysis.Meromorphic.TrailingCoefficient

/-!
# THM-M-0223 discovery-only intake probe

These checks authenticate adjacent pinned circle-integral, Cauchy, and meromorphic local-data APIs.
They do not define the classical residue of a general pole, select a contour theorem, or supply
target statement or proof credit.
-/

#check circleIntegral
#check Complex.circleIntegral_sub_center_inv_smul_eq_of_differentiable_on_annulus_off_countable
#check Complex.circleIntegral_sub_center_inv_smul_of_differentiable_on_off_countable
#check Complex.circleIntegral_sub_inv_smul_of_differentiable_on_off_countable
#check MeromorphicAt
#check MeromorphicOn
#check meromorphicOrderAt
#check meromorphicTrailingCoeffAt
