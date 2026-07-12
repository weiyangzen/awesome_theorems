import Mathlib.Probability.Moments.Basic

/-!
# THM-M-0993 independent validation probe

This module does not import the local proof or obligation-tree modules. It
independently reconstructs the frozen root from the pinned mathlib interfaces.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0993.Validation

universe u v

/-- A separately written reconstruction of the exact frozen Chernoff root. -/
theorem independentlyReconstructedRoot :
    forall (Omega : Type u) [MeasurableSpace Omega]
      (mu : Measure Omega) [IsProbabilityMeasure mu]
      (I : Type v) [Fintype I]
      (X : I -> Omega -> Real) (a t : Real),
        0 < t ->
        (forall i, Measurable (X i)) ->
        iIndepFun X mu ->
        (forall i, Integrable (fun omega => Real.exp (t * X i omega)) mu) ->
        mu.real {omega | a <= ∑ i, X i omega} <=
          Real.exp (-t * a) *
            ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu := by
  intro Omega _ mu _ I _ X a t ht hmeas hindep hint
  have hsum : Integrable (fun omega => Real.exp (t * (∑ i, X i) omega)) mu :=
    hindep.integrable_exp_mul_sum hmeas (fun i _hi => hint i)
  calc
    mu.real {omega | a <= ∑ i, X i omega}
        <= Real.exp (-t * a) * mgf (∑ i, X i) mu t := by
          simpa only [Finset.sum_apply] using
            measure_ge_le_exp_mul_mgf a ht.le hsum
    _ = Real.exp (-t * a) *
          ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu := by
      rw [show mgf (∑ i, X i) mu t =
          ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu by
        simpa only [mgf] using hindep.mgf_sum hmeas Finset.univ (t := t)]

#print axioms independentlyReconstructedRoot
#print axioms ProbabilityTheory.measure_ge_le_exp_mul_mgf
#print axioms ProbabilityTheory.iIndepFun.integrable_exp_mul_sum
#print axioms ProbabilityTheory.iIndepFun.mgf_sum

end Stage1Instances.THM_M_0993.Validation
