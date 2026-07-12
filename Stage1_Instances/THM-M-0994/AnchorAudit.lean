import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-0994: pinned Hoeffding anchor audit

This checks the two mathlib declarations that compose the candidate for the
frozen target.  The conclusion deliberately retains mathlib's nonnegative
variance proxy; transporting it to the denominator in `HoeffdingTarget` is a
later proof obligation, not anchor-audit credit.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Real
open scoped BigOperators ENNReal NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_0994

universe u v

/-- The strongest directly compositional candidate found in pinned mathlib. -/
theorem mathlibCandidateProxy
    (I : Type v) [Fintype I]
    (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : I -> Omega -> Real) (a b : I -> Real)
    (hX : forall i, Measurable (X i))
    (hindep : iIndepFun X mu)
    (hbound : forall i, ∀ᵐ omega ∂mu, X i omega ∈ Set.Icc (a i) (b i))
    (epsilon : Real) (hepsilon : 0 <= epsilon) :
    mu.real {omega | epsilon <=
        Finset.univ.sum (fun i => X i omega - ∫ x, X i x ∂mu)} <=
      exp (-epsilon ^ 2 /
        (2 * (Finset.univ.sum
          (fun i => ((nnnorm (b i - a i) / 2) ^ 2)) : NNReal))) := by
  have hcentered : iIndepFun (fun i omega => X i omega - ∫ x, X i x ∂mu) mu := by
    simpa [Function.comp_def] using
      hindep.comp (fun i x => x - ∫ y, X i y ∂mu) (fun _ => by fun_prop)
  exact HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
    hcentered
    (fun i _ => hasSubgaussianMGF_of_mem_Icc (hX i).aemeasurable (hbound i))
    hepsilon

end Stage1Instances.THM_M_0994

#check ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc
#check ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
#print axioms ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc
#print axioms ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
#print axioms Stage1Instances.THM_M_0994.mathlibCandidateProxy
