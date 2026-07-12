import Mathlib.Probability.StrongLaw

/-!
# THM-M-0983: exact Bernoulli strong-law statement

This module freezes the statement boundary only. It does not prove the law of
large numbers or claim credit for the historical wrapper.
-/

noncomputable section

open MeasureTheory Filter Finset
open scoped BigOperators MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_0983

universe u

/-- The empirical success frequency, with the empty average fixed to zero. -/
def empiricalFrequency {Omega : Type u} (X : Nat -> Omega -> Real)
    (n : Nat) (omega : Omega) : Real :=
  (∑ i ∈ range n, X i omega) / (n : Real)

/-- The exact selected Bernoulli-frequency strong law. The `0/1` condition and
common distribution make the real-valued observations Bernoulli trials, while
the expectation equation identifies their success probability with `p`. -/
def BernoulliStrongLawTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (p : Real),
      Integrable (X 0) mu ->
      ProbabilityTheory.iIndepFun X mu ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      (forall i, ∀ᵐ omega ∂mu,
        X i omega = 0 \/ X i omega = 1) ->
      mu[X 0] = p ->
      ∀ᵐ omega ∂mu,
        Tendsto (fun n : Nat => empiricalFrequency X n omega) atTop (nhds p)

/-- Direct expansion used to check that the named target adds no hidden data. -/
def ExpandedIntakeShape : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (p : Real),
      Integrable (X 0) mu ->
      ProbabilityTheory.iIndepFun X mu ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      (forall i, ∀ᵐ omega ∂mu,
        X i omega = 0 \/ X i omega = 1) ->
      mu[X 0] = p ->
      ∀ᵐ omega ∂mu,
        Tendsto
          (fun n : Nat => (∑ i ∈ range n, X i omega) / (n : Real))
          atTop (nhds p)

theorem target_iff_expandedIntakeShape :
    BernoulliStrongLawTarget.{u} <-> ExpandedIntakeShape.{u} := by
  rfl

-- Separately elaborated structural mutations; these are not equivalence claims.
def mutationRemovedIndependence : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (p : Real),
      Integrable (X 0) mu ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      mu[X 0] = p ->
      ∀ᵐ omega ∂mu,
        Tendsto (fun n => empiricalFrequency X n omega) atTop (nhds p)

def mutationChangedDomainToNatural : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (_X : Nat -> Omega -> Nat), True

def mutationChangedBinderScope : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real),
      exists p : Real, mu[X 0] = p /\
        (∀ᵐ omega ∂mu,
          Tendsto (fun n => empiricalFrequency X n omega) atTop (nhds p))

def mutationRemovedProbabilityMeasure : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) (X : Nat -> Omega -> Real) (p : Real),
      mu[X 0] = p -> True

/-- The explicit empty-average convention used by the target. -/
theorem empiricalFrequency_zero {Omega : Type u} (X : Nat -> Omega -> Real)
    (omega : Omega) : empiricalFrequency X 0 omega = 0 := by
  simp [empiricalFrequency]

end Stage1Instances.THM_M_0983

set_option pp.explicit true in
#print Stage1Instances.THM_M_0983.BernoulliStrongLawTarget
