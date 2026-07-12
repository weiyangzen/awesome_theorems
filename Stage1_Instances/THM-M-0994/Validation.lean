import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-0994 independent validation probe

This module does not import the local proof or obligation-tree modules. It
separately reconstructs the exact frozen Hoeffding root from pinned mathlib.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Real
open scoped BigOperators ENNReal NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_0994.Validation

universe u v

/-- A separately written reconstruction of the exact frozen Hoeffding root. -/
theorem independentlyReconstructedRoot :
    forall (I : Type v) [Fintype I]
      (Omega : Type u) [MeasurableSpace Omega]
      (mu : Measure Omega) [IsProbabilityMeasure mu]
      (X : I -> Omega -> Real) (a b : I -> Real),
        (forall i, Measurable (X i)) ->
        iIndepFun X mu ->
        (forall i, ∀ᵐ omega ∂mu, X i omega ∈ Set.Icc (a i) (b i)) ->
        forall epsilon : Real, 0 <= epsilon ->
          mu.real {omega | epsilon <= ∑ i, (X i omega - ∫ x, X i x ∂mu)} <=
            exp ((-2 * epsilon ^ 2) / ∑ i, (b i - a i) ^ 2) := by
  intro I _ Omega _ mu _ X a b hmeas hindep hbound epsilon hepsilon
  have hcentered : iIndepFun (fun i omega => X i omega - ∫ x, X i x ∂mu) mu := by
    simpa [Function.comp_def] using
      hindep.comp (fun i x => x - ∫ y, X i y ∂mu) (fun _ => by fun_prop)
  have htail :
      mu.real {omega | epsilon <=
          Finset.univ.sum (fun i => X i omega - ∫ x, X i x ∂mu)} <=
        exp (-epsilon ^ 2 /
          (2 * (Finset.univ.sum
            (fun i => ((nnnorm (b i - a i) / 2) ^ 2)) : NNReal))) :=
    HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
      hcentered
      (fun i _ => hasSubgaussianMGF_of_mem_Icc (hmeas i).aemeasurable (hbound i))
      hepsilon
  refine htail.trans_eq ?_
  congr 1
  push_cast
  rw [show (∑ i, (‖b i - a i‖ / 2) ^ 2 : Real) =
      (∑ i, (b i - a i) ^ 2) / 4 by
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i _
    rw [div_pow]
    norm_num [Real.norm_eq_abs, sq_abs]]
  ring

#print axioms independentlyReconstructedRoot
#print axioms ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
#print axioms ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc

end Stage1Instances.THM_M_0994.Validation
