import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-1080: pinned Azuma anchor audit

This module checks the strongest Azuma-Hoeffding candidate found in the pinned
mathlib snapshot. Its conditional sub-Gaussian increment hypotheses are not
silently identified with the frozen target's bounded martingale increments.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Real
open scoped BigOperators ENNReal NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1080

universe u

/-- The pinned mathlib Azuma-Hoeffding theorem, exposed with all relevant binders. -/
theorem mathlibConditionalSubgaussianCandidate
    {Omega : Type u} [mOmega : MeasurableSpace Omega] [StandardBorelSpace Omega]
    {mu : Measure Omega} [IsZeroOrProbabilityMeasure mu]
    {Y : Nat -> Omega -> Real} {cY : Nat -> NNReal}
    {G : Filtration Nat mOmega}
    (h_adapted : StronglyAdapted G Y)
    (h0 : HasSubgaussianMGF (Y 0) (cY 0) mu) (n : Nat)
    (h_subG : forall i, i < n - 1 ->
      HasCondSubgaussianMGF (G i) (G.le i) (Y (i + 1)) (cY (i + 1)) mu)
    {t : Real} (ht : 0 <= t) :
    mu.real {omega | t <= Finset.sum (Finset.range n) (fun i => Y i omega)} <=
      exp (-t ^ 2 / (2 * Finset.sum (Finset.range n) cY)) :=
  measure_sum_ge_le_of_hasCondSubgaussianMGF h_adapted h0 n h_subG ht

end Stage1Instances.THM_M_1080

#check ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF
#check ProbabilityTheory.HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF
#check ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero
#print axioms ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF
#print axioms ProbabilityTheory.HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF
#print axioms ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero
#print axioms Stage1Instances.THM_M_1080.mathlibConditionalSubgaussianCandidate
