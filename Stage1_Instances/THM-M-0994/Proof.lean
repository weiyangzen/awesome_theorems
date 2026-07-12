import Mathlib.Probability.Moments.SubGaussian

/-!
# THM-M-0994: proof

This closes the frozen one-sided finite-family Hoeffding target by composing
mathlib's interval subgaussian MGF bound with its independent-sum tail bound.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Real
open scoped BigOperators ENNReal NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_0994

universe u v

/-- A local restatement, kept definitionally identical to the frozen target
because target artifacts are elaborated as standalone files outside Lake's
module roots. -/
def HoeffdingTarget : Prop :=
  ∀ (I : Type v) [Fintype I]
    (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : I → Omega → ℝ) (a b : I → ℝ),
      (∀ i, Measurable (X i)) →
      iIndepFun X mu →
      (∀ i, ∀ᵐ omega ∂mu, X i omega ∈ Set.Icc (a i) (b i)) →
      ∀ epsilon : ℝ, 0 ≤ epsilon →
        mu.real {omega | epsilon ≤ ∑ i, (X i omega - ∫ x, X i x ∂mu)} ≤
          exp ((-2 * epsilon ^ 2) / ∑ i, (b i - a i) ^ 2)

theorem hoeffding : HoeffdingTarget.{u, v} := by
  intro I _ Omega _ mu _ X a b hX hindep hbound epsilon hepsilon
  have hcentered : iIndepFun (fun i omega => X i omega - ∫ x, X i x ∂mu) mu := by
    simpa [Function.comp_def] using
      hindep.comp (fun i x => x - ∫ y, X i y ∂mu) (fun _ => by fun_prop)
  have hproxy :
      mu.real {omega | epsilon <=
          Finset.univ.sum (fun i => X i omega - ∫ x, X i x ∂mu)} <=
        exp (-epsilon ^ 2 /
          (2 * (Finset.univ.sum
            (fun i => ((nnnorm (b i - a i) / 2) ^ 2)) : NNReal))) :=
    HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun
    hcentered
    (fun i _ => hasSubgaussianMGF_of_mem_Icc (hX i).aemeasurable (hbound i))
    hepsilon
  apply hproxy.trans_eq
  congr 1
  push_cast
  rw [show (∑ i, (‖b i - a i‖ / 2) ^ 2 : ℝ) =
      (∑ i, (b i - a i) ^ 2) / 4 by
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i _
    rw [div_pow]
    norm_num [Real.norm_eq_abs, sq_abs]]
  ring

#print axioms Stage1Instances.THM_M_0994.hoeffding

end Stage1Instances.THM_M_0994
