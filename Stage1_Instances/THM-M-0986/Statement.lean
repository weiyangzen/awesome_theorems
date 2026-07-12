import Mathlib.Probability.StrongLaw

/-!
# THM-M-0986: exact Khinchin weak-law statement

This module freezes and tests the real-valued statement boundary only. It does
not prove the weak law or credit the historical strong-law wrapper.
-/

noncomputable section

open Filter Finset MeasureTheory
open scoped BigOperators MeasureTheory ProbabilityTheory Topology
open scoped Function

namespace Stage1Instances.THM_M_0986

universe u

/-- The arithmetic mean of the first `n` observations. Lean's inverse convention
fixes the empty average at zero. -/
def empiricalAverage {Omega : Type u} (X : Nat -> Omega -> Real)
    (n : Nat) (omega : Omega) : Real :=
  (n : Real)⁻¹ * ∑ i ∈ range n, X i omega

/-- Khinchin's weak law in the exact real-valued form selected at intake:
integrable iid observations converge in probability to their common mean. -/
def KhinchinWeakLawTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real),
      Integrable (X 0) mu ->
      Pairwise ((fun f g => ProbabilityTheory.IndepFun f g mu) on X) ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      TendstoInMeasure mu (fun n omega => empiricalAverage X n omega) atTop
        (fun _omega => mu[X 0])

/-- Direct expansion checks that the named target hides no hypotheses or
change of convergence mode. -/
def ExpandedIntakeShape : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real),
      Integrable (X 0) mu ->
      Pairwise ((fun f g => ProbabilityTheory.IndepFun f g mu) on X) ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      TendstoInMeasure mu
        (fun (n : Nat) omega => (n : Real)⁻¹ * (∑ i ∈ range n, X i omega))
        atTop (fun _omega => mu[X 0])

/-- Checked identity with the fully expanded intake-selected statement. -/
theorem target_iff_expandedIntakeShape :
    KhinchinWeakLawTarget.{u} <-> ExpandedIntakeShape.{u} := by
  simp only [KhinchinWeakLawTarget, ExpandedIntakeShape, empiricalAverage]

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedIndependence : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real),
      Integrable (X 0) mu ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      TendstoInMeasure mu (fun n omega => empiricalAverage X n omega) atTop
        (fun _omega => mu[X 0])

def mutationChangedDomainToNatural : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (_X : Nat -> Omega -> Nat), True

def mutationChangedBinderScope : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu],
      exists X : Nat -> Omega -> Real,
        Integrable (X 0) mu /\
        TendstoInMeasure mu (fun n omega => empiricalAverage X n omega) atTop
          (fun _omega => mu[X 0])

def mutationRemovedIntegrability : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real),
      Pairwise ((fun f g => ProbabilityTheory.IndepFun f g mu) on X) ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      TendstoInMeasure mu (fun n omega => empiricalAverage X n omega) atTop
        (fun _omega => mu[X 0])

/-- The explicit empty-average convention used by the target. -/
theorem empiricalAverage_zero {Omega : Type u} (X : Nat -> Omega -> Real)
    (omega : Omega) : empiricalAverage X 0 omega = 0 := by
  simp [empiricalAverage]

end Stage1Instances.THM_M_0986

set_option pp.explicit true in
#print Stage1Instances.THM_M_0986.KhinchinWeakLawTarget
