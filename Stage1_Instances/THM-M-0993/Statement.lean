import Mathlib.Probability.Independence.Integration

/-!
# THM-M-0993: Chernoff exponential-moment upper-tail statement

This module freezes the exact finite-family product-form target selected at
intake. It elaborates the proposition and statement-boundary probes; it does
not prove the Chernoff bound.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0993

universe u v

/-- The exact selected Chernoff bound. The probability is represented by the
real value of the finite measure so that both sides of the inequality are real. -/
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

/-- Direct expansion of the selected target, used as a checked transport. -/
def ExpandedIntakeShape : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (I : Type v) [Fintype I]
    (X : I -> Omega -> Real) (a t : Real),
      0 < t ->
      (forall i, Measurable (X i)) ->
      ProbabilityTheory.iIndepFun X mu ->
      (forall i,
        MeasureTheory.Integrable (fun omega => Real.exp (t * X i omega)) mu) ->
      mu.real {omega | a <= Finset.univ.sum fun i => X i omega} <=
        Real.exp (-t * a) *
          Finset.univ.prod fun i =>
            ∫ omega, Real.exp (t * X i omega) ∂mu

theorem target_iff_expandedIntakeShape :
    ChernoffUpperTailTarget.{u, v} <-> ExpandedIntakeShape.{u, v} := by
  rfl

-- Separately elaborated, deliberately non-equivalent structural mutations.
def mutationRemovedPositiveTilt : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (I : Type v) [Fintype I]
    (X : I -> Omega -> Real) (a t : Real),
      (forall i, Measurable (X i)) ->
      iIndepFun X mu ->
      (forall i, Integrable (fun omega => Real.exp (t * X i omega)) mu) ->
      mu.real {omega | a <= ∑ i, X i omega} <=
        Real.exp (-t * a) *
          ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu

def mutationRemovedIndependence : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (I : Type v) [Fintype I]
    (X : I -> Omega -> Real) (a t : Real),
      0 < t ->
      (forall i, Measurable (X i)) ->
      (forall i, Integrable (fun omega => Real.exp (t * X i omega)) mu) ->
      mu.real {omega | a <= ∑ i, X i omega} <=
        Real.exp (-t * a) *
          ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu

def mutationUnfactoredMoment : Prop :=
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
          ∫ omega, Real.exp (t * ∑ i, X i omega) ∂mu

def mutationStrictTail : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (I : Type v) [Fintype I]
    (X : I -> Omega -> Real) (a t : Real),
      0 < t ->
      (forall i, Measurable (X i)) ->
      iIndepFun X mu ->
      (forall i, Integrable (fun omega => Real.exp (t * X i omega)) mu) ->
      mu.real {omega | a < ∑ i, X i omega} <=
        Real.exp (-t * a) *
          ∏ i, ∫ omega, Real.exp (t * X i omega) ∂mu

/-- The random sum for the empty finite family is zero. -/
theorem empty_family_sum : (∑ _i : Fin 0, (0 : Real)) = 0 := by
  simp

end Stage1Instances.THM_M_0993

set_option pp.explicit true in
#print Stage1Instances.THM_M_0993.ChernoffUpperTailTarget
