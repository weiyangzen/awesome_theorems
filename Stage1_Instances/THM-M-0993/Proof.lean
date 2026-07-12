import Mathlib.Probability.Moments.Basic

/-!
# THM-M-0993: proof of the frozen Chernoff upper-tail target

This module discharges the three interfaces frozen in obligation-registry
version 1 and composes them into the exact finite-family product-form target.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0993.Proof

universe u v

/-- The statement-phase target, repeated definitionally so the narrow proof
check remains independent of generated local object files. -/
def ChernoffUpperTailTarget : Prop :=
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

/-- `M0993-L-SUM-INT`: exponential integrability passes to the finite sum. -/
theorem sum_integrable
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    {I : Type v} [Fintype I] (X : I -> Omega -> Real) (t : Real)
    (hmeas : forall i, Measurable (X i)) (hindep : iIndepFun X mu)
    (hint : forall i, Integrable (fun omega => Real.exp (t * X i omega)) mu) :
    Integrable (fun omega => Real.exp (t * (∑ i, X i) omega)) mu := by
  exact hindep.integrable_exp_mul_sum hmeas (fun i _hi => hint i)

/-- `M0993-L-MARKOV`: the exponential Markov/Chernoff bridge. -/
theorem exponential_markov
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (Y : Omega -> Real) (a t : Real) (ht : 0 <= t)
    (hint : Integrable (fun omega => Real.exp (t * Y omega)) mu) :
    mu.real {omega | a <= Y omega} <= Real.exp (-t * a) * mgf Y mu t := by
  exact measure_ge_le_exp_mul_mgf a ht hint

/-- `M0993-L-FACTOR`: independence factors the MGF of the finite sum. -/
theorem sum_mgf_factorization
    {Omega : Type u} [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    {I : Type v} [Fintype I] (X : I -> Omega -> Real) (t : Real)
    (hmeas : forall i, Measurable (X i)) (hindep : iIndepFun X mu) :
    mgf (∑ i, X i) mu t =
      ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu := by
  simpa only [mgf] using hindep.mgf_sum hmeas Finset.univ (t := t)

/-- `M0993-B-EMPTY`: the sum and product conventions used by the root have
the expected values for an empty finite family. -/
theorem empty_family_boundary :
    (∑ _i : Fin 0, (0 : Real)) = 0 ∧ (∏ _i : Fin 0, (1 : Real)) = 1 := by
  simp

/-- `M0993-ROOT` and `M0993-T-ASSEMBLE`: the exact frozen target. -/
theorem chernoff_upper_tail :
    ChernoffUpperTailTarget.{u, v} := by
  intro Omega _ mu _ I _ X a t ht hmeas hindep hint
  have hsum : Integrable (fun omega => Real.exp (t * (∑ i, X i) omega)) mu :=
    sum_integrable mu X t hmeas hindep hint
  calc
    mu.real {omega | a <= ∑ i, X i omega}
        <= Real.exp (-t * a) * mgf (∑ i, X i) mu t := by
          simpa only [Finset.sum_apply] using
            exponential_markov mu (∑ i, X i) a t ht.le hsum
    _ = Real.exp (-t * a) *
          ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu := by
      rw [sum_mgf_factorization mu X t hmeas hindep]

#print axioms sum_integrable
#print axioms exponential_markov
#print axioms sum_mgf_factorization
#print axioms empty_family_boundary
#print axioms chernoff_upper_tail

end Stage1Instances.THM_M_0993.Proof
