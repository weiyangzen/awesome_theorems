import Mathlib.Probability.Moments.Basic

/-!
# THM-M-0993: pinned anchor audit

This module independently restates the frozen finite-family target and checks
the exact composition of the pinned mathlib Chernoff and MGF-factorization
declarations. It is audit evidence, not acceptance of a proof node.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0993.AnchorAudit

universe u v

/-- Independently elaborated copy of the statement-phase target. -/
def AuditedChernoffUpperTailTarget : Prop :=
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
          ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu

#check ProbabilityTheory.measure_ge_le_exp_mul_mgf
#check ProbabilityTheory.iIndepFun.integrable_exp_mul_sum
#check ProbabilityTheory.iIndepFun.mgf_sum

/-- The frozen target follows exactly from three declarations in the pinned
mathlib module `Probability.Moments.Basic`. -/
theorem exactTarget_from_pinned_mathlib :
    AuditedChernoffUpperTailTarget.{u, v} := by
  intro Omega _ mu _ I _ X a t ht hmeas hindep hint
  have hsum :
      Integrable (fun omega => Real.exp (t * (∑ i, X i) omega)) mu :=
    hindep.integrable_exp_mul_sum hmeas (fun i _ => hint i)
  calc
    mu.real {omega | a <= ∑ i, X i omega}
        <= Real.exp (-t * a) * mgf (∑ i, X i) mu t := by
          simpa only [Finset.sum_apply] using
            measure_ge_le_exp_mul_mgf (X := (∑ i, X i)) a ht.le hsum
    _ = Real.exp (-t * a) *
          ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu := by
      rw [hindep.mgf_sum hmeas Finset.univ]
      rfl

end Stage1Instances.THM_M_0993.AnchorAudit

#print axioms Stage1Instances.THM_M_0993.AnchorAudit.exactTarget_from_pinned_mathlib
