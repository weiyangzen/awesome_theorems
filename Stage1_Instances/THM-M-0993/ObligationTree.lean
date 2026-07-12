import Mathlib.Probability.Moments.Basic

/-!
# THM-M-0993: obligation-tree composition probe

This module checks the typed interfaces and child-to-parent composition frozen
by registry version 1. The three mathematical interfaces remain explicit
premises, so this is architecture evidence rather than proof-phase closure.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0993.ObligationTree

universe u v

def Root : Prop :=
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

def SumIntegrabilityInterface : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    (I : Type v) [Fintype I] (X : I -> Omega -> Real) (t : Real),
      (forall i, Measurable (X i)) -> iIndepFun X mu ->
      (forall i, Integrable (fun omega => Real.exp (t * X i omega)) mu) ->
      Integrable (fun omega => Real.exp (t * (∑ i, X i) omega)) mu

def MarkovInterface : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    (Y : Omega -> Real) (a t : Real), 0 <= t ->
      Integrable (fun omega => Real.exp (t * Y omega)) mu ->
      mu.real {omega | a <= Y omega} <= Real.exp (-t * a) * mgf Y mu t

def FactorizationInterface : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    (I : Type v) [Fintype I] (X : I -> Omega -> Real) (t : Real),
      (forall i, Measurable (X i)) -> iIndepFun X mu ->
      mgf (∑ i, X i) mu t =
        ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu

/-- Checked child-to-parent composition. Each substantive imported bridge is
kept as a typed premise until the proof phase discharges it. -/
theorem root_compose
    (sum_integrable : SumIntegrabilityInterface.{u, v})
    (markov : MarkovInterface.{u})
    (factor : FactorizationInterface.{u, v}) : Root.{u, v} := by
  intro Omega _ mu _ I _ X a t ht hmeas hindep hint
  have hsum := sum_integrable Omega mu I X t hmeas hindep hint
  calc
    mu.real {omega | a <= ∑ i, X i omega}
        <= Real.exp (-t * a) * mgf (∑ i, X i) mu t := by
          simpa only [Finset.sum_apply] using
            markov Omega mu (∑ i, X i) a t ht.le hsum
    _ = Real.exp (-t * a) *
          ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu := by
      rw [factor Omega mu I X t hmeas hindep]

#check ProbabilityTheory.measure_ge_le_exp_mul_mgf
#check ProbabilityTheory.iIndepFun.integrable_exp_mul_sum
#check ProbabilityTheory.iIndepFun.mgf_sum
#print axioms root_compose

end Stage1Instances.THM_M_0993.ObligationTree
