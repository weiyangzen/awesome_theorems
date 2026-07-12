import Mathlib.Probability.Moments.Variance

/-!
# THM-M-0995: bounded-summand Bernstein inequality statement

This module freezes the exact upper-tail proposition selected at intake. It
contains statement transports and probes, but no proof of Bernstein's
inequality.
-/

noncomputable section

open Finset MeasureTheory ProbabilityTheory Real
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0995

universe u

/-- The finite sum of the first `n` random variables. -/
def partialSum {Omega : Type u} (n : Nat) (X : Nat -> Omega -> Real)
    (omega : Omega) : Real :=
  ∑ i ∈ range n, X i omega

/-- All data and assumptions in the selected bounded-summand formulation. -/
structure BoundedSummandProblem (Omega : Type u) [MeasurableSpace Omega] where
  mu : Measure Omega
  n : Nat
  X : Nat -> Omega -> Real
  varianceBudget : Real
  bound : Real
  isProbability : IsProbabilityMeasure mu
  varianceBudget_nonneg : 0 <= varianceBudget
  bound_nonneg : 0 <= bound
  aemeasurable : forall i, i < n -> AEMeasurable (X i) mu
  memLp_two : forall i, i < n -> MemLp (X i) 2 mu
  independent : iIndepFun X mu
  mean_zero : forall i, i < n -> mu[X i] = 0
  abs_bound_ae : forall i, i < n -> ∀ᵐ omega ∂mu, |X i omega| <= bound
  variance_sum_le : (∑ i ∈ range n, Var[X i; mu]) <= varianceBudget

/-- The exact one-sided upper-tail Bernstein target selected at intake. -/
def StatementShape : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega) (t : Real),
      0 <= t ->
      P.mu.real {omega | t <= partialSum P.n P.X omega} <=
        exp (-(t ^ 2) / (2 * (P.varianceBudget + P.bound * t / 3)))

/-- Direct expansion of the package-based target. -/
def ExpandedSourceShape : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega),
      forall t : Real, 0 <= t ->
        P.mu.real {omega | t <= partialSum P.n P.X omega} <=
          exp (-(t ^ 2) / (2 * (P.varianceBudget + P.bound * t / 3)))

/-- Checked transport to the direct quantified expansion. -/
theorem statementShape_iff_expandedSourceShape :
    StatementShape.{u} <-> ExpandedSourceShape.{u} := by
  rfl

/-! The following propositions are separately elaborated structural mutations. -/

/-- Mutation: omit the almost-sure boundedness premise. -/
def mutationRemovedAbsBound : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) (n : Nat) (X : Nat -> Omega -> Real)
    (varianceBudget bound : Real),
      IsProbabilityMeasure mu ->
      0 <= varianceBudget -> 0 <= bound ->
      (forall i, i < n -> AEMeasurable (X i) mu) ->
      (forall i, i < n -> MemLp (X i) 2 mu) ->
      iIndepFun X mu ->
      (forall i, i < n -> mu[X i] = 0) ->
      (∑ i ∈ range n, Var[X i; mu]) <= varianceBudget ->
      forall t : Real, 0 <= t ->
        mu.real {omega | t <= partialSum n X omega} <=
          exp (-(t ^ 2) / (2 * (varianceBudget + bound * t / 3)))

/-- Mutation: change the random-variable codomain from reals to integers. -/
def mutationChangedDomain : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) (n : Nat) (X : Nat -> Omega -> Int),
      IsProbabilityMeasure mu ->
      forall t : Int, mu.real {omega | t <= ∑ i ∈ range n, X i omega} <= 1

/-- Mutation: choose one threshold before choosing the probability problem. -/
def mutationChangedBinderScope : Prop :=
  exists t : Real, 0 <= t ∧
    forall (Omega : Type u) [MeasurableSpace Omega]
      (P : BoundedSummandProblem Omega),
        P.mu.real {omega | t <= partialSum P.n P.X omega} <=
          exp (-(t ^ 2) / (2 * (P.varianceBudget + P.bound * t / 3)))

/-- Mutation: exclude the zero-threshold boundary. -/
def mutationExcludedZeroThreshold : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega) (t : Real),
      0 < t ->
      P.mu.real {omega | t <= partialSum P.n P.X omega} <=
        exp (-(t ^ 2) / (2 * (P.varianceBudget + P.bound * t / 3)))

/-- The totalized formula evaluates to one at threshold zero. -/
theorem zeroThresholdBound (varianceBudget bound : Real) :
    exp (-(0 ^ 2) / (2 * (varianceBudget + bound * 0 / 3))) = 1 := by
  simp

/-- With zero variance budget and zero bound, the totalized formula is one. -/
theorem zeroBudgetAndBound (t : Real) :
    exp (-(t ^ 2) / (2 * (0 + 0 * t / 3))) = 1 := by
  simp

/-- The empty finite sum is zero. -/
theorem emptyPartialSum {Omega : Type u} (X : Nat -> Omega -> Real) (omega : Omega) :
    partialSum 0 X omega = 0 := by
  simp [partialSum]

end Stage1Instances.THM_M_0995

set_option pp.explicit true in
#print Stage1Instances.THM_M_0995.StatementShape
