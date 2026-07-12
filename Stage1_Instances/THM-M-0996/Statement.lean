import Mathlib.Probability.Distributions.Gaussian.Multivariate

/-!
# THM-M-0996: Gaussian isoperimetric enlargement statement

This module freezes the finite-dimensional standard-Gaussian half-space
comparison target.  It elaborates the statement boundary; it does not prove
the Gaussian isoperimetric inequality.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0996

universe u

/-- A set is a closed affine half-space with a unit normal.  Requiring a unit
normal fixes the metric normalization used by the enlargement comparison. -/
def IsUnitHalfspace {E : Type u} [NormedAddCommGroup E]
    [NormedSpace Real E] (H : Set E) : Prop :=
  exists (L : E →L[Real] Real) (c : Real), ‖L‖ = 1 /\ H = {x | L x <= c}

/-- The exact selected Gaussian isoperimetric target.  For every positive
radius, a measurable set has at least as much standard-Gaussian measure after
open metric enlargement as any unit-normal half-space of equal measure. -/
def GaussianIsoperimetricTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (A H : Set E),
      MeasurableSet A ->
      IsUnitHalfspace H ->
      stdGaussian E A = stdGaussian E H ->
      forall r : Real, 0 < r ->
        stdGaussian E (Metric.thickening r H) <=
          stdGaussian E (Metric.thickening r A)

/-- Fully qualified expansion, serving as a checked transport. -/
def ExpandedStatementShape : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (A H : Set E),
      MeasurableSet A ->
      (exists (L : E →L[Real] Real) (c : Real),
        ‖L‖ = 1 /\ H = {x | L x <= c}) ->
      ProbabilityTheory.stdGaussian E A = ProbabilityTheory.stdGaussian E H ->
      forall r : Real, 0 < r ->
        ProbabilityTheory.stdGaussian E (Metric.thickening r H) <=
          ProbabilityTheory.stdGaussian E (Metric.thickening r A)

theorem target_iff_expandedStatementShape :
    GaussianIsoperimetricTarget.{u} <-> ExpandedStatementShape.{u} := by
  rfl

-- Separately elaborated structural mutations.  These receive no equivalence claim.
def mutationRemovedMeasurability : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (A H : Set E),
      IsUnitHalfspace H ->
      stdGaussian E A = stdGaussian E H ->
      forall r : Real, 0 < r ->
        stdGaussian E (Metric.thickening r H) <=
          stdGaussian E (Metric.thickening r A)

def mutationRemovedEqualMeasure : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (A H : Set E),
      MeasurableSet A -> IsUnitHalfspace H ->
      forall r : Real, 0 < r ->
        stdGaussian E (Metric.thickening r H) <=
          stdGaussian E (Metric.thickening r A)

def mutationNonpositiveRadius : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (A H : Set E),
      MeasurableSet A -> IsUnitHalfspace H ->
      stdGaussian E A = stdGaussian E H ->
      forall r : Real, 0 <= r ->
        stdGaussian E (Metric.thickening r H) <=
          stdGaussian E (Metric.thickening r A)

def mutationArbitraryGaussianMeasure : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (mu : Measure E) [IsGaussian mu] (A H : Set E),
      MeasurableSet A -> IsUnitHalfspace H -> mu A = mu H ->
      forall r : Real, 0 < r ->
        mu (Metric.thickening r H) <= mu (Metric.thickening r A)

end Stage1Instances.THM_M_0996

set_option pp.explicit true in
#print Stage1Instances.THM_M_0996.GaussianIsoperimetricTarget
