import Mathlib.Analysis.Analytic.Order
import Mathlib.Analysis.Complex.CauchyIntegral
import Mathlib.Analysis.Meromorphic.Divisor

/-!
# THM-M-0232 discovery-only intake probe

These checks authenticate adjacent pinned vanishing-order, divisor, and circle-integral APIs. They
do not select a contour or zero-count encoding, state Rouché's theorem, or prove THM-M-0232.
-/

#check analyticOrderAt
#check analyticOrderNatAt
#check meromorphicOrderAt
#check MeromorphicOn.divisor
#check MeromorphicOn.divisor_apply
#check MeromorphicOn.AnalyticOnNhd.divisor_nonneg
#check DiffContOnCl.circleIntegral_sub_inv_smul
#check DifferentiableOn.circleIntegral_sub_inv_smul

#print axioms MeromorphicOn.AnalyticOnNhd.divisor_nonneg
#print axioms DiffContOnCl.circleIntegral_sub_inv_smul
#print axioms DifferentiableOn.circleIntegral_sub_inv_smul
